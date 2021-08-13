"""A class for handling connections with a Tautulli instance."""
from __future__ import annotations

from typing import Any

from aiohttp import ClientSession

from .decorator import api_command
from .models import (
    PyTautulliApiActivity,
    PyTautulliApiHomeStats,
    PyTautulliApiServerInfo,
    PyTautulliApiUser,
    PyTautulliHostConfiguration,
)


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
        request_timeout: float = 10,
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
        self._request_timeout = request_timeout

    @api_command(command="get_activity", datatype=PyTautulliApiActivity)
    async def async_get_activity(self, **kwargs) -> PyTautulliApiActivity:
        """Get the current activity on the PMS."""

    @api_command(command="get_home_stats", datatype=PyTautulliApiHomeStats)
    async def async_get_home_stats(self, **kwargs) -> PyTautulliApiHomeStats:
        """Get the homepage watch statistics."""

    @api_command(command="get_users", datatype=PyTautulliApiUser)
    async def async_get_users(self, **kwargs) -> list[PyTautulliApiUser]:
        """Get a list of all users that have access to your server."""

    @api_command(command="get_server_info", datatype=PyTautulliApiServerInfo)
    async def async_get_server_info(self, **kwargs) -> PyTautulliApiServerInfo:
        """Get the PMS server information."""
