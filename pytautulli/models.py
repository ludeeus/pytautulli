"""Pytautulli models."""
from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Any


class APIResult(str, Enum):
    """ApiResult."""

    SUCCESS = "success"


class PyTautulliApiBaseModel:
    """PyTautulliApiBaseModel."""


@dataclass
class PyTautulliApiResponse(PyTautulliApiBaseModel):
    """API response model for PyTautulliApi."""

    _command: str | None = None

    data: dict[str, Any] | list[dict[str, Any]] | None = None
    message: str | None = None
    result: APIResult | None = None

    @staticmethod
    def from_dict(data: dict[str, Any]) -> PyTautulliApiResponse:
        """Generate object from json."""
        obj: dict[str, Any] = {}

        for key, value in data.items():
            if hasattr(PyTautulliApiResponse, key):
                obj[key] = value

        return PyTautulliApiResponse(**obj)
