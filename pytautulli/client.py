"""A class for handling connections with a Tautulli instance."""
from __future__ import annotations
from aiohttp import ClientSession

from .decorator import api_command
from .models import PyTautulliApiResponse, PyTautulliHostConfiguration


class PyTautulli:
    """A class for handling connections with a Tautulli instance."""

    def __init__(
        self,
        host_configuration: PyTautulliHostConfiguration | None = None,
        session: ClientSession | None = None,
        hostname: str | None = None,
        ipaddress: str | None = None,
        api_key: str | None = None,
        port: int | None = None,
        ssl: bool | None = None,
        verify_ssl: bool | None = None,
        base_api_path: str | None = None,
    ) -> None:
        """Initialize"""
        if host_configuration is None:
            host_configuration = PyTautulliHostConfiguration(
                hostname=hostname, ipaddress=ipaddress, api_key=api_key
            )
            for key in (port, ssl, verify_ssl, base_api_path):
                if key is not None:
                    host_configuration[key] = key

        self._host = host_configuration
        self._session = session

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
