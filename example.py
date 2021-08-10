"""Example usage of pytautulli."""
import asyncio
import json
import aiohttp
from pytautulli import PyTautulli

HOST = "192.168.100.3"
API_KEY = "392a2d57905341acb5bc58c95d4d2795"


async def async_example():
    """Example usage of pytautulli."""
    async with aiohttp.ClientSession() as session:
        client = PyTautulli(HOST, API_KEY, session)
        print(await client.async_get_users())


asyncio.get_event_loop().run_until_complete(async_example())
