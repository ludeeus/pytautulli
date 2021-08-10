"""PyTautulli base modal."""
from __future__ import annotations

import json
from enum import Enum
from typing import Any

from .const import CONVERT_TO_BOOL


class APIResponseType(str, Enum):
    """ApiResponseType."""

    LIST = "list"
    DICT = "dict"


class PyTautulliApiBaseModel:
    """PyTautulliApiBaseModel."""

    _datatype: PyTautulliApiBaseModel | None = None
    _responsetype: APIResponseType = APIResponseType.DICT

    def __init__(
        self, data: dict[str, Any], datatype: PyTautulliApiBaseModel = None
    ) -> None:
        """Init."""
        self._datatype = datatype
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
            f"{key}={json.dumps(self._attributes[key]) if not isinstance(self._attributes[key], object) and issubclass(self._attributes[key], PyTautulliApiBaseModel) else self._attributes[key]}"
            for key in self._attributes
            if not key.startswith("_") and key != "_command"
        ]
        return f"{self.__class__.__name__}({', '.join(attrs)})"

    def __post_init__(self):
        for key in CONVERT_TO_BOOL:
            if hasattr(self, key):
                self.__setattr__(key, bool(self.__getattribute__(key)))

    @property
    def _attributes(self) -> dict[str, Any]:
        """Return the attributes."""
        return {k: v for k, v in self.__dict__.items() if not k.startswith("__")}
