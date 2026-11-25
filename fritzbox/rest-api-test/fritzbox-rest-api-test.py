#!/usr/bin/env python3

## similar projects
# https://github.com/Meine-smarte-Welt
# https://github.com/Meine-smarte-Welt/zigbee2mqtt_manager/blob/main/README.en.md
# https://github.com/Meine-smarte-Welt/fritzbox_netzwerk

import hashlib
import os
import sys
import time
import json
import requests
import xml.etree.ElementTree as ET

FRITZ_HOST = os.getenv("FRITZ_HOST", "http://192.168.178.1")
FRITZ_USER = os.getenv("FRITZ_USER", "home-monitor")
FRITZ_PASSWORD = os.getenv("FRITZ_PASSWORD", "")

EMPTY_SID = "0000000000000000"

session = requests.Session()
session.timeout = 10


# --------------------------------------------------
# 1. Calculate challenge response
# --------------------------------------------------

def calculate_response(challenge, password):

    if challenge.startswith("2$"):

        print("[AUTH] Using PBKDF2-SHA256")

        _, iter1, salt1, iter2, salt2 = challenge.split("$")

        hash1 = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
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

    print("[AUTH] Using legacy MD5")

    digest = hashlib.md5(
        f"{challenge}-{password}".encode("utf-16le")
    ).hexdigest()

    return f"{challenge}-{digest}"


# --------------------------------------------------
# 2. Obtain AVM-SID
# --------------------------------------------------

def get_sid():

    url = f"{FRITZ_HOST}/login_sid.lua"

    print("[AUTH] Requesting challenge...")

    response = session.get(
        url,
        params={"version": "2"},
        timeout=10
    )

    response.raise_for_status()

    root = ET.fromstring(response.text)

    sid = root.findtext("SID")
    challenge = root.findtext("Challenge")
    blocktime = int(root.findtext("BlockTime", "0"))

    print("[AUTH] Initial SID:", sid)

    if sid and sid != EMPTY_SID:
        print("[AUTH] Already authenticated")
        return sid

    if not challenge:
        raise RuntimeError("Challenge not returned by FRITZ!Box")

    if blocktime > 0:
        print(f"[AUTH] Waiting {blocktime} seconds")
        time.sleep(blocktime)

    answer = calculate_response(
        challenge,
        FRITZ_PASSWORD
    )

    print("[AUTH] Sending authentication response...")

    response = session.post(
        url,
        params={"version": "2"},
        data={
            "username": FRITZ_USER,
            "response": answer
        },
        timeout=10
    )

    response.raise_for_status()

    root = ET.fromstring(response.text)

    sid = root.findtext("SID")
    blocktime = root.findtext("BlockTime", "0")

    if not sid or sid == EMPTY_SID:
        raise RuntimeError(
            f"Authentication failed. BlockTime={blocktime}"
        )

    print("[AUTH] Authentication successful")
    print("[AUTH] SID obtained (value hidden)")

    return sid


# --------------------------------------------------
# 3. First authenticated API request
# --------------------------------------------------

def test_api(sid):

    url = f"{FRITZ_HOST}/api/v0/monitor/online/0"

    print("\n[API] Requesting:", url)

    response = session.get(
        url,
        headers={
            "AUTHORIZATION": f"AVM-SID {sid}",
            "Accept": "application/json"
        },
        timeout=10
    )

    print("[API] HTTP status:", response.status_code)
    print("[API] Content-Type:", response.headers.get("Content-Type"))

    response.raise_for_status()

    try:
        payload = response.json()

        print("\n[API] JSON response:")
        print(json.dumps(payload, indent=2, ensure_ascii=False))

        print("\n[API] Top-level fields:")
        print(list(payload.keys()) if isinstance(payload, dict) else type(payload))

    except ValueError:
        print("\n[API] Response is not JSON:")
        print(response.text[:5000])


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    if not FRITZ_PASSWORD:
        sys.exit("Set FRITZ_PASSWORD environment variable")

    try:
        sid = get_sid()
        test_api(sid)

    except requests.RequestException as exc:
        print("[HTTP ERROR]", exc)
        sys.exit(1)

    except Exception as exc:
        print("[ERROR]", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
