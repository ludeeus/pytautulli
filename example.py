"""Example usage of pytautulli."""
import asyncio
from pytautulli import PyTautulli, PyTautulliHostConfiguration

IP = "192.168.100.3"
TOKEN = "392a2d57905341acb5bc58c95d4d2795"


async def async_example():
    """Example usage of pytautulli."""
    host_configuration = PyTautulliHostConfiguration(ipaddress=IP, api_key=TOKEN)
    async with PyTautulli(host_configuration=host_configuration) as client:
        print(await client.async_get_users())


asyncio.get_event_loop().run_until_complete(async_example())
