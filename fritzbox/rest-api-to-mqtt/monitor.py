## FRITZ!Box challenge-response authentication, the Online Monitor API, persistent state and MQTT Discovery.
## installation 
# pip3 install -r requirements.txt

import os
import json
import time
import hashlib
import logging
import xml.etree.ElementTree as ET

from pathlib import Path
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import requests
import paho.mqtt.client as mqtt


# ==================================================
# CONFIGURATION
# ==================================================

FRITZ_HOST = os.getenv("FRITZ_HOST", "http://192.168.178.1").rstrip("/")
FRITZ_USER = os.getenv("FRITZ_USER", "")
FRITZ_PASSWORD = os.getenv("FRITZ_PASSWORD", "")

ANDROID_MAC = "".join(
    c for c in os.getenv("ANDROID_MAC", "").lower()
    if c in "0123456789abcdef"
)

DEVICE_NAME = os.getenv("DEVICE_NAME", "android_phone")

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER = os.getenv("MQTT_USER", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")

MQTT_PREFIX = os.getenv(
    "MQTT_PREFIX", "home/network/android_phone"
)

HA_PREFIX = os.getenv(
    "HA_DISCOVERY_PREFIX", "homeassistant"
)

POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "5"))
TRAFFIC_THRESHOLD = float(os.getenv("TRAFFIC_THRESHOLD", "512"))
MIN_ACTIVE_SAMPLES = int(os.getenv("MIN_ACTIVE_SAMPLES", "2"))
IDLE_TIMEOUT = int(os.getenv("IDLE_TIMEOUT", "30"))

RATE_UNIT = os.getenv("FRITZ_RATE_UNIT", "bytes").lower()

TZ = ZoneInfo(os.getenv("TZ", "Europe/Berlin"))

DATA_DIR = Path("/data")
STATE_FILE = DATA_DIR / "state.json"

ONLINE_ENDPOINT = "/api/v0/monitor/online/0"

EMPTY_SID = "0000000000000000"


# ==================================================
# LOGGING
# ==================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

log = logging.getLogger("fritz-monitor")


# ==================================================
# PERSISTENT STATE
# ==================================================

DATA_DIR.mkdir(parents=True, exist_ok=True)


def default_state():
    return {
        "active": False,
        "high_count": 0,
        "candidate_start": None,
        "last_activity": None,
        "first_activity_today": None,
        "activity_date": None,
        "last_sample_time": None,
        "download": 0,
        "upload": 0
    }


def load_state():
    if STATE_FILE.exists():
        try:
            return {
                **default_state(),
                **json.loads(STATE_FILE.read_text())
            }
        except (ValueError, OSError):
            log.exception("Could not load state")

    return default_state()


state = load_state()


def save_state():
    temporary = STATE_FILE.with_suffix(".tmp")

    temporary.write_text(
        json.dumps(state, indent=2)
    )

    temporary.replace(STATE_FILE)


# ==================================================
# TIME
# ==================================================

def local_now():
    return datetime.now(TZ)


def iso_timestamp(timestamp):
    return datetime.fromtimestamp(
        timestamp, timezone.utc
    ).astimezone(TZ).isoformat(timespec="seconds")


def local_date(timestamp):
    return datetime.fromtimestamp(
        timestamp, timezone.utc
    ).astimezone(TZ).date().isoformat()


# ==================================================
# FRITZ!BOX AUTHENTICATION
# ==================================================

session = requests.Session()


def solve_challenge(challenge, password):

    if challenge.startswith("2$"):
        _, iter1, salt1, iter2, salt2 = challenge.split("$")

        hash1 = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            bytes.fromhex(salt1),
            int(iter1)
        )

        hash2 = hashlib.pbkdf2_hmac(
            "sha256",
            hash1,
            bytes.fromhex(salt2),
            int(iter2)
        )

        return f"{salt2}${hash2.hex()}"

    cleaned = "".join(
        c if ord(c) <= 255 else "."
        for c in password
    )

    digest = hashlib.md5(
        f"{challenge}-{cleaned}".encode("utf-16le")
    ).hexdigest()

    return f"{challenge}-{digest}"


def session_info(response):
    root = ET.fromstring(response.text)

    return {
        "sid": root.findtext("SID", ""),
        "challenge": root.findtext("Challenge", ""),
        "blocktime": root.findtext("BlockTime", "0")
    }


def fritz_login():

    response = session.get(
        f"{FRITZ_HOST}/login_sid.lua",
        params={"version": "2"},
        timeout=10
    )

    response.raise_for_status()

    info = session_info(response)

    if info["sid"] != EMPTY_SID:
        return info["sid"]

    if info["blocktime"] not in ("", "0"):
        raise RuntimeError("FRITZ!Box login temporarily blocked")

    answer = solve_challenge(
        info["challenge"],
        FRITZ_PASSWORD
    )

    response = session.post(
        f"{FRITZ_HOST}/login_sid.lua",
        params={"version": "2"},
        data={
            "username": FRITZ_USER,
            "response": answer
        },
        timeout=10
    )

    response.raise_for_status()

    sid = session_info(response)["sid"]

    if not sid or sid == EMPTY_SID:
        raise RuntimeError("FRITZ!Box authentication failed")

    log.info("FRITZ!Box authenticated")

    return sid


sid = None


def get_online_monitor():

    global sid

    if sid is None:
        sid = fritz_login()

    url = FRITZ_HOST + ONLINE_ENDPOINT

    response = session.get(
        url,
        headers={
            "Authorization": f"AVM-SID {sid}",
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Referer": f"{FRITZ_HOST}/"
        },
        timeout=10
    )

    if response.status_code in (401, 403):
        sid = fritz_login()

        response = session.get(
            url,
            headers={
                "Authorization": f"AVM-SID {sid}",
                "Content-Type": "application/json",
                "Accept": "*/*",
                "Referer": f"{FRITZ_HOST}/"
            },
            timeout=10
        )

    response.raise_for_status()

    payload = response.json()

    if "devices" not in payload:
        raise RuntimeError("Unexpected Online Monitor response")

    return payload


# ==================================================
# TRAFFIC EXTRACTION
# ==================================================

def latest_value(values):

    if not isinstance(values, list) or not values:
        return 0.0

    value = values[-1]

    try:
        return max(0.0, float(value))
    except (TypeError, ValueError):
        return 0.0


def get_device_traffic(payload):

    for device in payload.get("devices", []):

        uid = str(device.get("UID", "")).lower()

        if uid != f"mac{ANDROID_MAC}":
            continue

        download = latest_value(
            device.get("downstream")
        )

        upload = latest_value(
            device.get("upstream")
        )

        if RATE_UNIT == "bits":
            download /= 8
            upload /= 8

        return download, upload

    raise RuntimeError(
        "Android device not found in Online Monitor. "
        "Check MAC and per-device monitoring settings."
    )


# ==================================================
# MQTT
# ==================================================

mqtt_client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="fritzbox-android-monitor"
)

if MQTT_USER:
    mqtt_client.username_pw_set(
        MQTT_USER,
        MQTT_PASSWORD
    )


def topic(name):
    return f"{MQTT_PREFIX}/{name}"


def publish(name, value, retain=True):

    mqtt_client.publish(
        topic(name),
        str(value),
        qos=1,
        retain=retain
    )


def publish_json(name, value):

    mqtt_client.publish(
        topic(name),
        json.dumps(value),
        qos=1,
        retain=False
    )


def discovery(entity, name, component, **extra):

    uid = f"fritz_android_{entity}"

    config = {
        "name": name,
        "unique_id": uid,
        "state_topic": topic(f"{entity}/state"),
        "availability_topic": topic("availability"),
        "device": {
            "identifiers": ["fritz_android_monitor"],
            "name": "Android Phone Traffic",
            "manufacturer": "Custom",
            "model": "FRITZ!Box Online Monitor"
        }
    }

    config.update(extra)

    mqtt_client.publish(
        f"{HA_PREFIX}/{component}/{uid}/config",
        json.dumps(config),
        qos=1,
        retain=True
    )


def setup_discovery():

    discovery(
        "active",
        "Android network activity",
        "binary_sensor",
        payload_on="ON",
        payload_off="OFF",
        icon="mdi:network"
    )

    discovery(
        "download",
        "Android download rate",
        "sensor",
        unit_of_measurement="B/s",
        state_class="measurement",
        icon="mdi:download"
    )

    discovery(
        "upload",
        "Android upload rate",
        "sensor",
        unit_of_measurement="B/s",
        state_class="measurement",
        icon="mdi:upload"
    )

    discovery(
        "last_activity",
        "Android last activity",
        "sensor",
        device_class="timestamp"
    )

    discovery(
        "first_activity_today",
        "Android first activity today",
        "sensor",
        device_class="timestamp"
    )


# ==================================================
# ACTIVITY DETECTION
# ==================================================

def process_traffic(download, upload, sample_time):

    total = download + upload

    current_date = local_date(sample_time)

    if state["activity_date"] != current_date:

        state["activity_date"] = current_date
        state["first_activity_today"] = None

        log.info("New activity day: %s", current_date)

    above_threshold = total >= TRAFFIC_THRESHOLD

    if above_threshold:

        if state["high_count"] == 0:
            state["candidate_start"] = sample_time

        state["high_count"] += 1
        state["last_activity"] = iso_timestamp(sample_time)

        if (
            not state["active"]
            and state["high_count"] >= MIN_ACTIVE_SAMPLES
        ):

            state["active"] = True

            start = state["candidate_start"]

            if state["first_activity_today"] is None:
                state["first_activity_today"] = iso_timestamp(start)

            event = {
                "device": DEVICE_NAME,
                "event": "activity_started",
                "timestamp": iso_timestamp(start),
                "download_bps": download,
                "upload_bps": upload,
                "total_bps": total
            }

            publish_json("events", event)

            log.info(
                "ACTIVITY STARTED: %s B/s",
                round(total, 1)
            )

    else:
        state["high_count"] = 0
        state["candidate_start"] = None

    # Return to idle after a period without significant traffic.
    last = state["last_activity"]

    if state["active"] and last:

        elapsed = (
            datetime.now(TZ) -
            datetime.fromisoformat(last)
        ).total_seconds()

        if elapsed > IDLE_TIMEOUT:

            state["active"] = False

            publish_json("events", {
                "device": DEVICE_NAME,
                "event": "activity_stopped",
                "timestamp": local_now().isoformat(
                    timespec="seconds"
                )
            })

            log.info("ACTIVITY STOPPED")


# ==================================================
# SENSOR PUBLISHING
# ==================================================

def publish_sensors():

    publish(
        "active/state",
        "ON" if state["active"] else "OFF"
    )

    publish(
        "download/state",
        round(state["download"], 2)
    )

    publish(
        "upload/state",
        round(state["upload"], 2)
    )

    publish(
        "last_activity/state",
        state["last_activity"] or "unknown"
    )

    first = state["first_activity_today"]

    publish(
        "first_activity_today/state",
        first or "unknown"
    )

    publish("availability", "online")


# ==================================================
# MAIN
# ==================================================

def main():

    if len(ANDROID_MAC) != 12:
        raise RuntimeError(
            "Set ANDROID_MAC to a valid 12-character MAC address"
        )

    if not FRITZ_USER or not FRITZ_PASSWORD:
        raise RuntimeError("FRITZ!Box credentials are required")

    if RATE_UNIT not in ("bytes", "bits"):
        raise RuntimeError("FRITZ_RATE_UNIT must be bytes or bits")

    mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
    mqtt_client.loop_start()

    setup_discovery()

    log.info("FRITZ!Box Android monitor started")
    log.info("Device MAC: %s", ANDROID_MAC)
    log.info("Threshold: %s B/s", TRAFFIC_THRESHOLD)

    try:

        while True:

            try:

                payload = get_online_monitor()

                download, upload = get_device_traffic(payload)

                timestamp = float(
                    payload["lastSampleTime"]
                )

                if timestamp > 1e11:
                    timestamp /= 1000

                # Process each new FRITZ!Box sample only once.
                if timestamp > (state["last_sample_time"] or 0):

                    state["last_sample_time"] = timestamp
                    state["download"] = download
                    state["upload"] = upload

                    process_traffic(
                        download,
                        upload,
                        timestamp
                    )

                    publish_sensors()
                    save_state()

            except Exception:
                log.exception("Monitoring error")

            time.sleep(POLL_INTERVAL)

    finally:

        publish("availability", "offline")
        save_state()

        mqtt_client.loop_stop()
        mqtt_client.disconnect()


if __name__ == "__main__":
    main()
