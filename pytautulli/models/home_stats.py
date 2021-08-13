"""PyTautulliApiHomeStats."""
from __future__ import annotations

from pytautulli.models.user import PyTautulliApiUser

from .base import APIResponseType, PyTautulliApiBaseModel


class PyTautulliApiHomeStatsRow(PyTautulliApiUser, PyTautulliApiBaseModel):
    """PyTautulliApiHomeStatsRow"""

    _responsetype = APIResponseType.DICT

    art: str | None = None
    content_rating: str | None = None
    count: int | None = None
    friendly_name: str | None = None
    grandparent_rating_key: str | None = None
    grandparent_thumb: str | None = None
    guid: str | None = None
    labels: list[str] | None = None
    last_play: str | None = None
    live: bool | None = None
    media_type: str | None = None
    platform: str | None = None
    platform_name: str | None = None
    rating_key: int | None = None
    row_id: int | None = None
    section_id: int | None = None
    started: str | None = None
    stopped: str | None = None
    thumb: str | None = None
    title: str | None = None
    total_duration: int | None = None
    total_plays: int | None = None
    user: str | None = None
    users_watched: str | None = None
    year: int | None = None


class PyTautulliApiHomeStats(PyTautulliApiBaseModel):
    """PyTautulliApiHomeStats."""

    _responsetype = APIResponseType.LIST

    stat_id: str | None = None
    stat_type: str | None = None
    stat_title: str | None = None
    rows: list[PyTautulliApiHomeStatsRow] = None

    def __post_init__(self):
        super().__post_init__()
        self.rows = [PyTautulliApiHomeStatsRow(row) for row in self.rows or []]
