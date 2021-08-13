"""PyTautulli exceptions."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import PyTautulli


class PyTautulliException(Exception):
    """Base pytautulli exception."""

    def __init__(
        self, client: PyTautulli | None = None, message: str | Exception = ""
    ) -> None:
        super().__init__(
            client.redact_string(str(message)) if client is not None else message
        )


class PyTautulliConnectionException(PyTautulliException):
    """pytautulli connection exception."""


class PyTautulliAuthenticationException(PyTautulliException):
    """pytautulli authentication exception."""
