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
            request_data = f"api_key={client._api_key}&format=json"
            url = f"{'https' if client._ssl else 'http'}://{client._host}{':'+str(client._port) if client._port else ''}{client._base_api_path or ''}/api/v2?apikey={client._api_key}&cmd={command}"
            log_friendly_url = url.replace(client._api_key, "[REDACTED]")
            if kwargs:
                for key, value in kwargs.items():
                    request_data += f"&{key}={value}"

            LOGGER.debug("Requesting %s", url)
            try:
                async with async_timeout.timeout(10, loop=asyncio.get_event_loop()):
                    request = await client._session.request(
                        method=method,
                        url=url,
                        headers=API_HEADERS,
                        data=request_data,
                        verify_ssl=client._verify_ssl,
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

            response = PyTautulliApiResponse.from_dict(
                {**result.get(ATTR_RESPONSE, {}), "_command": command}
            )

            #            if response.status == APIStatus.FAIL:
            #                if response.error.message == "api_key parameter is missing.":
            #                    raise PyTautulliAuthenticationException("No API key was provided")

            return response

        return wrapper

    return decorator
