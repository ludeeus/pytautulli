"""Decorator for pytautulli"""
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import aiohttp
import async_timeout

from .const import API_HEADERS, ATTR_RESPONSE, LOGGER
from .models import PyTautulliApiResponse
from .exceptions import (
    PyTautulliConnectionException,
    PyTautulliException,
)

if TYPE_CHECKING:
    from .client import PyTautulli


def api_command(command: str, method: str = "GET"):
    """Decorator for Tautulli API request"""

    def decorator(func):
        """Decorator"""

        async def wrapper(*args, **kwargs):
            """Wrapper"""
            client: PyTautulli = args[0]
            url = client._host.api_url(command)
            log_friendly_url = url.replace(client._host.api_key, "[REDACTED]")
            if kwargs:
                for key, value in kwargs.items():
                    url += f"&{key}={value}"

            LOGGER.debug("Requesting %s", log_friendly_url)
            try:
                async with async_timeout.timeout(10, loop=asyncio.get_event_loop()):
                    request = await client._session.request(
                        method=method,
                        url=url,
                        headers=API_HEADERS,
                        verify_ssl=client._host.verify_ssl,
                    )

                    if request.status != 200:
                        raise PyTautulliConnectionException(
                            f"Request for '{log_friendly_url}' failed with status code '{request.status}'"
                        )

                result = await request.json()
            except aiohttp.ClientError as exception:
                raise PyTautulliConnectionException(
                    f"Request exception for '{log_friendly_url}' with - {exception}"
                ) from exception

            except asyncio.TimeoutError:
                raise PyTautulliConnectionException(
                    f"Request timeout for '{log_friendly_url}'"
                )

            except PyTautulliConnectionException as exception:
                raise PyTautulliConnectionException(exception) from exception

            except PyTautulliException as exception:
                raise PyTautulliException(exception) from exception

            except (Exception, BaseException) as exception:
                raise PyTautulliException(
                    f"Unexpected exception for '{log_friendly_url}' with - {exception}"
                ) from exception

            LOGGER.debug("Requesting %s returned %s", log_friendly_url, result)

            response = PyTautulliApiResponse(
                {**result.get(ATTR_RESPONSE, {}), "_command": command}
            )

            #            if response.status == APIStatus.FAIL:
            #                if response.error.message == "api_key parameter is missing.":
            #                    raise PyTautulliAuthenticationException("No API key was provided")

            return response

        return wrapper

    return decorator
