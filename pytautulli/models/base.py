"""PyTautulli base modal."""
from __future__ import annotations

import json
from enum import Enum
from typing import Any

from .const import CONVERT_TO_BOOL


class PyTautulliJJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder."""

    def default(self, obj):
        """Default JSON encoder."""
        if isinstance(obj, PyTautulliApiBaseModel):
            return obj.attributes
        if isinstance(obj, Enum):
            return obj.name
        return json.JSONEncoder.default(self, obj)


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
        for key, value in data.items():
            if hasattr(self, key):
                if hasattr(self, f"_generate_{key}"):
                    value = self.__getattribute__(f"_generate_{key}")(value)
                self.__setattr__(key, value)

        self.__post_init__()

    def __repr__(self) -> str:
        """Representation."""
        attrs = [
            f"{key}={json.dumps(self.__dict__[key], cls=PyTautulliJJSONEncoder)}"
            for key in self.attributes
            if self.__dict__[key] is not None and "token" not in key
        ]
        return f"{self.__class__.__name__}({', '.join(attrs)})"

    def __post_init__(self):
        for key in CONVERT_TO_BOOL:
            if hasattr(self, key) and self.__getattribute__(key) is not None:
                self.__setattr__(key, bool(self.__getattribute__(key)))

    @property
    def attributes(self) -> dict[str, Any]:
        """Return the class attributes."""
        return {
            key: json.dumps(self.__dict__[key], cls=PyTautulliJJSONEncoder)
            for key in self.__dict__
            if not key.startswith("_")
        }
