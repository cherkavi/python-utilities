import kopf
import os

from pathlib import Path
from datetime import datetime


FILE_PATH = os.getenv(
    "TIMESTAMP_FILE",
    "/tmp/timestamps.log"
)


@kopf.timer(
    'example.org',
    'v1alpha1',
    'timestampwriters',
    interval=60,
)
def write_timestamp(spec, name, namespace, logger, **kwargs):

    if not spec.get("enabled", True):
        return

    path = Path(FILE_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().astimezone().isoformat(
        timespec="seconds"
    )

    with path.open("a") as file:
        file.write(f"{timestamp}\n")

    logger.info(
        f"Timestamp written for {namespace}/{name}: {timestamp}"
    )