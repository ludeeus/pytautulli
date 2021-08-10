"""Decorator for pytautulli"""
from __future__ import annotations

import asyncio
import sys
from traceback import TracebackException
from typing import TYPE_CHECKING

import aiohttp
import async_timeout

from .const import API_HEADERS, ATTR_RESPONSE, LOGGER, ATTR_DATA
from .exceptions import (
    PyTautulliAuthenticationException,
    PyTautulliConnectionException,
    PyTautulliException,
)
from .models import PyTautulliApiBaseModel, PyTautulliApiResponse

if TYPE_CHECKING:
    from .client import PyTautulli


def api_command(command: str, datatype: PyTautulliApiBaseModel, method: str = "GET"):
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
                async with async_timeout.timeout(
                    client._request_timeout, loop=asyncio.get_event_loop()
                ):
                    request = await client._session.request(
                        method=method,
                        url=url,
                        headers=API_HEADERS,
                        verify_ssl=client._host.verify_ssl,
                    )

                    result = await request.json()
                    response = PyTautulliApiResponse(
                        data=result.get(ATTR_RESPONSE, {}),
                        datatype=datatype,
                    )

                    if request.status != 200:

                        if request.status == 401:
                            raise PyTautulliAuthenticationException(response.message)
                        raise PyTautulliConnectionException(
                            f"Request for '{log_friendly_url}' failed with status code '{request.status}'"
                        )

            except aiohttp.ClientError as exception:
                raise PyTautulliConnectionException(
                    f"Request exception for '{log_friendly_url}' with - {exception}"
                ) from exception

            except asyncio.TimeoutError:
                raise PyTautulliConnectionException(
                    f"Request timeout for '{log_friendly_url}'"
                )

            except PyTautulliAuthenticationException as exception:
                raise PyTautulliAuthenticationException(exception) from exception

            except PyTautulliConnectionException as exception:
                raise PyTautulliConnectionException(exception) from exception

            except PyTautulliException as exception:
                raise PyTautulliException(exception) from exception

            except (Exception, BaseException) as exception:
                exc_info = TracebackException.from_exception(exception)
                raise PyTautulliException(
                    f"Unexpected {exc_info.exc_type.__name__} for '{log_friendly_url}' with - {exc_info} ({exc_info.stack})"
                ) from exception

            LOGGER.debug("Requesting %s returned %s", log_friendly_url, result)

            if func_response := await func(client, **{ATTR_DATA: response.data}):
                return func_response

            return response.data

        return wrapper

    return decorator
