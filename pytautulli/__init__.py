"""
A python module to get information from Tautulli.

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import asyncio
import logging
import socket

import aiohttp
import async_timeout
from . import exceptions


_LOGGER = logging.getLogger(__name__)
_BASE_URL = '{schema}://{host}:{port}{path}/api/v2?apikey={api_key}&cmd='


class Tautulli():
    """A class for handling connections with a Tautulli instance."""

    def __init__(self, host, port, api_key, loop, session, ssl=False, path=""):
        """Initialize the connection to a Tautulli instance."""
        self._loop = loop
        self._session = session
        self.api_key = api_key
        self.schema = 'https' if ssl else 'http'
        self.host = host
        self.port = port
        self.path = path
        self.connection = None
        self.tautulli_session_data = {}
        self.tautulli_server_identity = None
        self.tautulli_home_data = {}
        self.tautulli_users = []
        self.tautulli_user_data = {}
        self.base_url = _BASE_URL.format(schema=self.schema,
                                         host=self.host,
                                         port=self.port,
                                         path=self.path,
                                         api_key=self.api_key)

    async def send_request(self, cmd):
        """Send request."""
        url = self.base_url + cmd
        try:
            async with async_timeout.timeout(8, loop=self._loop):
                response = await self._session.get(url)

            logger("Status from Tautulli: " + str(response.status))
            if response.status == 401:
                raise exceptions.AuthenticationError
            return response

        except (asyncio.TimeoutError, aiohttp.ClientError, socket.gaierror,
                AttributeError) as error:
            msg = "Can not load data from Tautulli: {} - {}".format(url, error)
            logger(msg, 40)
            raise exceptions.ConnectError from error

    async def initialize(self):
        """Initially connect and get Plex server identity."""
        await self.test_connection()
        await self.get_server_identity()

    
    async def test_connection(self):
        """Test the connection to Tautulli."""
        cmd = 'get_server_friendly_name'
        response = await self.send_request(cmd)
        connectionstate = await response.json()
        if connectionstate['response']['message']:
            self.connection = False
        else:
            self.connection = True
        logger("Status from Tautulli: " + str(response.status))

    async def get_data(self):
        """Get Tautulli data."""
        await self.get_session_data()
        await self.get_home_data()
        await self.get_users()
        await self.get_user_data()

    async def get_session_data(self):
        """Get Tautulli sessions."""
        cmd = 'get_activity'
        response = await self.send_request(cmd)
        self.tautulli_session_data = await response.json()
        logger(self.tautulli_session_data)

    async def get_server_identity(self):
        """Get Plex server identity."""
        cmd = 'get_server_identity'
        response = await self.send_request(cmd)
        self.tautulli_server_identity = await response.json()
        logger(self.tautulli_server_identity)

    async def get_home_data(self):
        """Get Tautulli home stats."""
        cmd = 'get_home_stats'
        request = await self.send_request(cmd)
        data = {}
        response = await request.json()
        for stat in response.get('response', {}).get('data', {}):
            if stat.get('stat_id') == 'top_movies':
                try:
                    row = stat.get('rows', {})[0]
                    data['movie'] = row.get('title')
                except (IndexError, KeyError):
                    data['movie'] = None
            if stat.get('stat_id') == 'top_tv':
                try:
                    row = stat.get('rows', {})[0]
                    data['tv'] = row.get('title')
                except (IndexError, KeyError):
                    data['tv'] = None
            if stat.get('stat_id') == 'top_users':
                try:
                    row = stat.get('rows', {})[0]
                    data['user'] = row.get('user')
                except (IndexError, KeyError):
                    data['user'] = None
            self.tautulli_home_data = data
            logger(self.tautulli_home_data)

    async def get_users(self):
        """Get Tautulli users."""
        cmd = 'get_users'
        response = await self.send_request(cmd)
        users = []
        all_user_data = await response.json()
        for user in all_user_data['response']['data']:
            if user['username'] != 'Local':
                users.append(user['username'])
        self.tautulli_users = users
        logger(self.tautulli_users)

    async def get_user_data(self):
        """Get Tautulli userdata."""
        userdata = {}
        sessions = self.session_data.get('sessions', {})
        try:
            async with async_timeout.timeout(8, loop=self._loop):
                for username in self.tautulli_users:
                    userdata[username] = {}
                    userdata[username]['Activity'] = None
                    for session in sessions:
                        if session['username'].lower() == username.lower():
                            userdata[username]['Activity'] = session['state']
                            for key in session:
                                if key != 'Username':
                                    userdata[username][key] = session[key]
                            break

            self.tautulli_user_data = userdata
        except (asyncio.TimeoutError, aiohttp.ClientError, KeyError) as error:
            msg = "Can not load data from Tautulli."
            logger(msg, 40)
            raise exceptions.ConnectError from error

    @property
    def connection_status(self):
        """Return the server stats from Tautulli."""
        return self.connection

    @property
    def session_data(self):
        """Return data from Tautulli."""
        return self.tautulli_session_data.get('response', {}).get('data', {})

    @property
    def users(self):
        """Return data from Tautulli."""
        return self.tautulli_users

    @property
    def user_data(self):
        """Return user activity data from Tautulli."""
        return self.tautulli_user_data

    @property
    def home_data(self):
        """Return data from Tautulli."""
        return self.tautulli_home_data

    @property
    def server_identity(self):
        """Return Plex server identity."""
        return self.tautulli_server_identity


def logger(message, level=10):
    """Handle logging."""
    logging.getLogger(__name__).log(level, str(message))

    # Enable this for local debug:
    # print('Log level: "' + str(level) + '", message: "' + str(message) + '"')
