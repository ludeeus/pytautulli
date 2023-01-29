"""PyTautulliHostConfiguration."""
from __future__ import annotations

from dataclasses import dataclass

from yarl import URL

from ..exceptions import PyTautulliException


@dataclass
class PyTautulliHostConfiguration:
    """PyTautulliHostConfiguration."""

    api_token: str
    hostname: str | None = None
    ipaddress: str | None = None
    port: int | None = 8181
    ssl: bool = False
    verify_ssl: bool = True
    base_api_path: str | None = None
    url: str | None = None

    def __post_init__(self):
        """post init."""
        if self.api_token is None:
            raise PyTautulliException(
                message="No api token to the tautulli server was provided"
            )
        if self.hostname is None and self.ipaddress is None and self.url is None:
            raise PyTautulliException(
                message="No url, hostname or ipaddress to the tautulli server was provided"
            )

    def api_url(self, command: str) -> str:
        """Return the generated base URL based on host configuration."""
        base_url = self.base_url
        path = "/".join(x for x in f"{base_url.path}/api/v2".split("/") if x != "")
        return URL.build(
            scheme=base_url.scheme,
            host=base_url.host,
            port=base_url.port,
            path=f"/{path}",
            query={"apikey": self.api_token, "cmd": command},
        ).human_repr()

    @property
    def base_url(self) -> URL:
        """Return the base URL for the configured service."""
        return (
            URL(self.url)
            if self.url is not None
            else URL.build(
                scheme=f"http{'s' if self.ssl else ''}",
                host=self.hostname or self.ipaddress,
                port=str(self.port) if self.port else None,
                path=self.base_api_path or "",
            )
        )
