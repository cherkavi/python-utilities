import asyncio
import os
from datetime import datetime
from tapo import ApiClient
import logging

logging.basicConfig(level=logging.DEBUG)

async def main():
    ip = os.environ["IP_ADDRESS"]

    print(f"Connecting to camera: {ip}")
    print(f"HTTPS endpoint: https://{ip}:443/")

    client = ApiClient(
        os.environ["TAPO_USERNAME"],
        os.environ["TAPO_PASSWORD"],
    )

    device = await client.c210(ip)
    # device = await client.p110(ip)

    print(f"Connected to {ip} with {device}")

asyncio.run(main())