"""Example usage of pytautulli."""
import asyncio
import json

import aiohttp

from pytautulli import PyTautulli, PyTautulliHostConfiguration

HOST_CONFIGURATION = PyTautulliHostConfiguration(
    ipaddress="192.168.100.3", api_key="392a2d57905341acb5bc58c95d4d2795"
)


async def async_example():
    """Example usage of pytautulli."""
    async with aiohttp.ClientSession() as session:
        client = PyTautulli(host_configuration=HOST_CONFIGURATION, session=session)
        print(await client.async_get_settings())


asyncio.get_event_loop().run_until_complete(async_example())
