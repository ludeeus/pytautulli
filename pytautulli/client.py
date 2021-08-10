"""A class for handling connections with a Tautulli instance."""
from __future__ import annotations
from aiohttp import ClientSession

from .decorator import api_command
from .models import PyTautulliApiResponse


class PyTautulli:
    """A class for handling connections with a Tautulli instance."""

    def __init__(
        self,
        host: str,
        api_key: str,
        session: ClientSession,
        port: int = 8181,
        ssl: bool = False,
        verify_ssl: bool = True,
        base_api_path: str | None = None,
    ) -> None:
        """Initialize"""
        self._host = host
        self._port = port
        self._ssl = ssl
        self._verify_ssl = verify_ssl
        self._api_key: str = api_key
        self._base_api_path = base_api_path
        self._session: ClientSession = session

    @api_command(command="get_server_friendly_name")
    async def async_get_server_friendly_name(self, **kwargs) -> PyTautulliApiResponse:
        """Get the name of the PMS.."""

    @api_command(command="get_activity")
    async def async_get_activity(self, **kwargs) -> PyTautulliApiResponse:
        """Get the current activity on the PMS."""

    @api_command(command="get_home_stats")
    async def async_get_home_stats(self, **kwargs) -> PyTautulliApiResponse:
        """Get the homepage watch statistics."""

    @api_command(command="get_users")
    async def async_get_users(self, **kwargs) -> PyTautulliApiResponse:
        """Get a list of all users that have access to your server."""
