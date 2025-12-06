"""Example usage of pytautulli."""

import asyncio

from pytautulli import PyTautulli, PyTautulliHostConfiguration

IP = "192.168.100.3"
TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


async def async_example():
    """Example usage of pytautulli."""
    host_configuration = PyTautulliHostConfiguration(ipaddress=IP, api_token=TOKEN)
    async with PyTautulli(host_configuration=host_configuration) as client:
        print(await client.async_command("get_activity"))


asyncio.run(async_example())
