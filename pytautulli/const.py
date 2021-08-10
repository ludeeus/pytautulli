"""Pytautulli constants."""
from logging import Logger, getLogger

API_HEADERS = {"Content-Type": "application/json"}


LOGGER: Logger = getLogger(__package__)


ATTR_RESPONSE = "response"


ATTR_CONVERT_TO_BOOL = (
    "is_active",
    "is_admin",
    "is_home_user",
    "is_allow_sync",
    "is_restricted",
    "do_notify",
    "keep_history",
    "allow_guest",
    "secure",
    "local",
    "live",
    "optimized_version",
    "selected",
)
