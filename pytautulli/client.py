"""A class for handling connections with a Tautulli instance."""
from __future__ import annotations
from copy import copy
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

    _close_session = False
    _from_aenter = False

    def __init__(
        self,
        host_configuration: PyTautulliHostConfiguration | None = None,
        session: ClientSession | None = None,
        hostname: str | None = None,
        ipaddress: str | None = None,
        url: str | None = None,
        api_token: str | None = None,
        port: int | None = None,
        ssl: bool | None = None,
        verify_ssl: bool | None = None,
        base_api_path: str | None = None,
        request_timeout: float = 10,
        raw_response: bool = False,
        redact: bool = True,
    ) -> None:
        """Initialize"""
        if host_configuration is None:
            host_configuration = PyTautulliHostConfiguration(
                hostname=hostname, ipaddress=ipaddress, url=url, api_token=api_token
            )
        else:
            host_configuration = copy(host_configuration)

        if port is not None:
            host_configuration.port = port
        if ssl is not None:
            host_configuration.ssl = ssl
        if verify_ssl is not None:
            host_configuration.verify_ssl = verify_ssl
        if base_api_path is not None:
            host_configuration.base_api_path = base_api_path

        if session is None:
            session = ClientSession()
            self._close_session = True

        self._host = host_configuration
        self._session = session
        self._request_timeout = request_timeout
        self._raw_response = raw_response
        self._redact = redact

    async def __aenter__(self) -> PyTautulli:
        """Async enter."""
        self._from_aenter = True
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        if self._session and self._close_session:
            await self._session.close()

    def redact_string(self, string: str) -> str:
        """Redact a api token from a string if needed."""
        if not self._redact:
            return string

        return string.replace(self._host.api_token, "[REDACTED_API_TOKEN]")

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

    @api_command(command="command")
    async def async_command(self, command: str, **kwargs) -> dict[str, Any]:
        """Send any command to the server, returns a raw non-typed response dictionary."""
