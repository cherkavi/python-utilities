# snapshot with low resolution

import asyncio
import os
from datetime import datetime
from tapo import ApiClient


async def main():
    client = ApiClient(os.environ["TAPO_USERNAME"],os.environ["TAPO_PASSWORD"])
    print(f"connecting to {os.environ["IP_ADDRESS"]}")
    device = await client.c210(os.environ["IP_ADDRESS"])
    print(f"connected to {device}")

    info = await device.get_device_info()
    print("Device info:", info.to_dict())

    camera_username = os.environ["TAPO_CAMERA_USERNAME"]
    camera_password = os.environ["TAPO_CAMERA_PASSWORD"]

    rtsp_url = await device.get_rtsp_stream_url(camera_username, camera_password)
    print("RTSP HD:", rtsp_url.hd)

    snapshot = await device.get_snapshot(camera_username, camera_password)
    with open(f"c210_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg", "wb") as file:
        file.write(snapshot.data)


for key in (
    "IP_ADDRESS",
    "TAPO_USERNAME",
    "TAPO_PASSWORD",
    "TAPO_CAMERA_USERNAME",
    "TAPO_CAMERA_PASSWORD",
):
    value = os.getenv(key)
    print(f"{key}: {'SET' if value else 'MISSING'}")

asyncio.run(main())