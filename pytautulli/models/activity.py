"""PyTautulliApiActivity."""
from __future__ import annotations

from .base import PyTautulliApiBaseModel
from .session import PyTautulliApiSession


class PyTautulliApiActivity(PyTautulliApiBaseModel):
    """PyTautulliApiActivity."""

    lan_bandwidth: int | None = None
    sessions: list[PyTautulliApiSession] | None = None
    stream_count_direct_play: int | None = None
    stream_count_direct_stream: int | None = None
    stream_count_transcode: int | None = None
    stream_count: int | None = None
    total_bandwidth: int | None = None
    wan_bandwidth: int | None = None

    def __post_init__(self):
        super().__post_init__()
        self.sessions = [PyTautulliApiSession(session) for session in self.sessions]
