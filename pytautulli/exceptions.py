"""PyTautulli exceptions."""


class PyTautulliException(Exception):
    """Base pytautulli exception."""


class PyTautulliConnectionException(PyTautulliException):
    """pytautulli connection exception."""


class PyTautulliAuthenticationException(PyTautulliException):
    """pytautulli authentication exception."""
