"""PyTautulliApiUser."""
from __future__ import annotations

from .base import APIResponseType, PyTautulliApiBaseModel


class PyTautulliApiUser(PyTautulliApiBaseModel):
    """PyTautulliApiUser."""

    _responsetype = APIResponseType.LIST

    allow_guest: bool | None = None
    do_notify: bool | None = None
    email: str | None = None
    friendly_name: str | None = None
    is_active: bool | None = None
    is_admin: bool | None = None
    is_allow_sync: bool | None = None
    is_home_user: bool | None = None
    is_restricted: bool | None = None
    keep_history: bool | None = None
    row_id: int | None = None
    server_token: str | None = None
    shared_libraries: list[str] | None = None
    thumb: str | None = None
    user_id: int | None = None
    username: str | None = None

    def __post_init__(self):
        super().__post_init__()
        if self.shared_libraries:
            self.shared_libraries = self.shared_libraries.split(";")
