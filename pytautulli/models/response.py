"""API response model for PyTautulli Api.."""
from __future__ import annotations

from enum import Enum
from typing import Any

from .activity import PyTautulliApiActivity
from .base import APIResponseType, PyTautulliApiBaseModel
from .session import PyTautulliApiSession
from .user import PyTautulliApiUser


class APIResult(str, Enum):
    """ApiResult."""

    SUCCESS = "success"
    ERROR = "error"


class PyTautulliApiResponse(PyTautulliApiBaseModel):
    """API response model for PyTautulli Api."""

    data: dict[str, Any] | list[
        dict[str, Any]
    ] | PyTautulliApiActivity | PyTautulliApiSession | list[
        PyTautulliApiUser
    ] | None = None
    message: str | None = None
    result: APIResult | None = None

    def _generate_data(self, data: dict[str, Any] | list[dict[str, Any]]) -> None:
        """Generate data."""
        if self._datatype is None:
            return data

        if self._datatype._responsetype == APIResponseType.LIST:
            return [self._datatype(item, self._datatype) for item in data]

        return self._datatype(data, self._datatype)
