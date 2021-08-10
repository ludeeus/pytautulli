"""Pytautulli models."""
from __future__ import annotations
import json
from enum import Enum
from typing import Any

from dataclasses import dataclass
from .exceptions import PyTautulliException


class APIResult(str, Enum):
    """ApiResult."""

    SUCCESS = "success"


class APIResponseType(str, Enum):
    """ApiResponseType."""

    LIST = "list"
    DICT = "dict"


@dataclass
class PyTautulliHostConfiguration:
    """PyTautulliHostConfiguration."""

    api_key: str
    hostname: str | None = None
    ipaddress: str | None = None
    port: int | None = 8181
    ssl: bool = False
    verify_ssl: bool = True
    base_api_path: str | None = None

    def __post_init__(self):
        """post init."""
        if self.hostname is None and self.ipaddress is None:
            raise PyTautulliException("No hostname or ip provided.")

    def api_url(self, command: str) -> str:
        """Return the generated base URL based on host configuration."""
        protocol = f"http{'s' if self.ssl else ''}"
        host = self.hostname or self.ipaddress
        if self.port:
            host = f"{host}:{str(self.port)}"
        path = f"/api/v2?apikey={self.api_key}&cmd={command}"
        if self.base_api_path:
            path = f"{self.base_api_path}/{path}"
        return f"{protocol}://{host}{path}"


class PyTautulliApiBaseModel:
    """PyTautulliApiBaseModel."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Init."""
        if command := data.get("_command"):
            self.__setattr__("_command", command)
        for key, value in data.items():
            if hasattr(self, key):
                if hasattr(self, f"_generate_{key}"):
                    value = self.__getattribute__(f"_generate_{key}")(value)
                self.__setattr__(key, value)

        self.__post_init__()

    def __repr__(self) -> str:
        """Representation."""
        attrs = [
            f"{name}={json.dumps(value) if not isinstance(value, object) and issubclass(value, PyTautulliApiBaseModel) else value}"
            for name, value in self.__dict__.items()
            if not name.startswith("__")
        ]
        return f"{self.__class__.__name__}({', '.join(attrs)})"

    def __post_init__(self):
        pass


class PyTautulliApiUser(PyTautulliApiBaseModel):
    """PyTautulliApiUser."""

    row_id: int | None = None
    user_id: int | None = None
    username: str | None = None
    friendly_name: str | None = None
    thumb: str | None = None
    email: str | None = None
    is_active: bool | None = None
    is_admin: bool | None = None
    is_home_user: bool | None = None
    is_allow_sync: bool | None = None
    is_restricted: bool | None = None
    do_notify: bool | None = None
    keep_history: bool | None = None
    allow_guest: bool | None = None
    server_token: str | None = None
    shared_libraries: str | None = None

    def __post_init__(self):
        for key in (
            "is_active",
            "is_admin",
            "is_home_user",
            "is_allow_sync",
            "is_restricted",
            "do_notify",
            "keep_history",
            "allow_guest",
        ):
            if hasattr(self, key):
                self.__setattr__(key, bool(self.__getattribute__(key)))


class PyTautulliApiResponse(PyTautulliApiBaseModel):
    """API response model for PyTautulli Api."""

    __class_lookup = {"get_users": (PyTautulliApiUser, APIResponseType.LIST)}

    _command: str | None = None

    data: dict[str, Any] | list[dict[str, Any]] | None = None
    message: str | None = None
    result: APIResult | None = None

    def _generate_data(self, data: dict[str, Any] | list[dict[str, Any]]) -> None:
        """Generate data."""
        if (lookup := self.__class_lookup.get(self._command)) is None:
            return data

        if lookup[1] == APIResponseType.LIST:
            return [lookup[0](item) for item in data]

        return lookup[0](data)
