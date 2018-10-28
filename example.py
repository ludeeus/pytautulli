"""Example usage of pytautulli."""
import asyncio
import json
import aiohttp
from pytautulli import Tautulli


async def test():
    """Example usage of pytautulli."""
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        data = Tautulli('192.168.2.11', '8181', '13838dcabfc34f45a6152897fb84c29a', LOOP, session, True)
        await data.test_connection()
        await data.get_data()

        print("Connection status:", data.connection_status)
        print(json.dumps(data.session_data, indent=4, sort_keys=True))
        print(json.dumps(data.home_data, indent=4, sort_keys=True))


LOOP = asyncio.get_event_loop()
LOOP.run_until_complete(test())
