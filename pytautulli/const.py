"""Pytautulli constants."""
from logging import Logger, getLogger

API_HEADERS = {"Content-Type": "application/json"}

LOGGER: Logger = getLogger(__package__)

ATTR_RESPONSE = "response"
ATTR_DATA = "data"
