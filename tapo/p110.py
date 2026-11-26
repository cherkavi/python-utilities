import asyncio
import os
from tapo import ApiClient


async def main() -> None:
  email = os.environ["TAPO_USERNAME"]
  password = os.environ["TAPO_PASSWORD"]
  ip = os.environ["IP_ADDRESS"]

  client = ApiClient(email, password)
  device = await client.p110(ip)
  
  #   await device.on()
  energy = await device.get_current_power()
  print(energy)
  # print(dir(energy))
  print(energy.to_dict())
  print(energy.current_power)

asyncio.run(main())