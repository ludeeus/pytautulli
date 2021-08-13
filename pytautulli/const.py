"""Pytautulli constants."""
from enum import Enum
from logging import Logger, getLogger

API_HEADERS = {"Content-Type": "application/json"}

LOGGER: Logger = getLogger(__package__)

ATTR_RESPONSE = "response"
ATTR_DATA = "data"


class HTTPMethod(Enum):
    """HTTPMethod Enum."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
