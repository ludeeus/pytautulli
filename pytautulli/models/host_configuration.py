"""PyTautulliHostConfiguration."""
from __future__ import annotations

from dataclasses import dataclass

from ..exceptions import PyTautulliException


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
