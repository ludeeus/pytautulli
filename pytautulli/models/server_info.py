"""PyTautulliApiServerInfo."""
from __future__ import annotations

from .base import APIResponseType, PyTautulliApiBaseModel


class PyTautulliApiServerInfo(PyTautulliApiBaseModel):
    """PyTautulliApiServerInfo."""

    _responsetype = APIResponseType.DICT

    pms_identifier: str | None = None
    pms_ip: str | None = None
    pms_is_remote: bool | None = None
    pms_name: str | None = None
    pms_platform: str | None = None
    pms_plexpass: bool | None = None
    pms_port: str | None = None
    pms_ssl: bool | None = None
    pms_url_manual: bool | None = None
    pms_url: str | None = None
    pms_version: str | None = None
