"""Example usage of pytautulli."""
import asyncio
import json
import aiohttp
from pytautulli import Tautulli

HOST = '192.168.2.11'
PORT = '8181'
API_KEY = '13838dcabfc34f45a6152897fb84c29a'


async def test():
    """Example usage of pytautulli."""
    async with aiohttp.ClientSession() as session:
        data = Tautulli(HOST, PORT, API_KEY, LOOP, session, True)
        await data.test_connection()
        await data.get_data()

        print("Connection status:", data.connection_status)
        print(json.dumps(data.session_data, indent=4, sort_keys=True))
        print(json.dumps(data.home_data, indent=4, sort_keys=True))


LOOP = asyncio.get_event_loop()
LOOP.run_until_complete(test())
