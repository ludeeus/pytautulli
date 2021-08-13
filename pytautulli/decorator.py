"""Decorator for pytautulli"""
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import aiohttp
import async_timeout

from .const import API_HEADERS, ATTR_DATA, ATTR_RESPONSE, LOGGER, HTTPMethod
from .exceptions import (
    PyTautulliAuthenticationException,
    PyTautulliConnectionException,
    PyTautulliException,
)
from .models import PyTautulliApiBaseModel, PyTautulliApiResponse

if TYPE_CHECKING:
    from .client import PyTautulli


def api_command(
    command: str,
    datatype: PyTautulliApiBaseModel | None = None,
    method: HTTPMethod = HTTPMethod.GET,
):
    """Decorator for Tautulli API request"""

    def decorator(func):
        """Decorator"""

        async def wrapper(*args, **kwargs):
            """Wrapper"""
            client: PyTautulli = args[0]
            url = client._host.api_url(command if command != "command" else args[1])
            if kwargs:
                for key, value in kwargs.items():
                    url += f"&{key}={value}"

            LOGGER.debug("Requesting %s", client.redact_string(url))
            try:
                async with async_timeout.timeout(
                    client._request_timeout, loop=asyncio.get_event_loop()
                ):
                    request = await client._session.request(
                        method=method.value,
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
                            raise PyTautulliAuthenticationException(
                                client, response.message
                            )
                        raise PyTautulliConnectionException(
                            client,
                            f"Request for '{url}' failed with status code '{request.status}'",
                        )

                LOGGER.debug(
                    "Requesting %s returned %s", client.redact_string(url), result
                )

                if func_response := await func(
                    *args, **{**kwargs, ATTR_DATA: response.data}
                ):
                    return func_response

                if client._raw_response or command == "command":
                    return result

            except aiohttp.ClientError as exception:
                raise PyTautulliConnectionException(
                    client,
                    f"Request exception for '{url}' with - {exception}",
                ) from exception

            except asyncio.TimeoutError:
                raise PyTautulliConnectionException(
                    client, f"Request timeout for '{url}'"
                )

            except PyTautulliAuthenticationException as exception:
                raise PyTautulliAuthenticationException(
                    client, exception
                ) from exception

            except PyTautulliConnectionException as exception:
                raise PyTautulliConnectionException(client, exception) from exception

            except PyTautulliException as exception:
                raise PyTautulliException(client, exception) from exception

            except (Exception, BaseException) as exception:
                raise PyTautulliException(client, exception) from exception

            else:
                return response.data

        return wrapper

    return decorator
