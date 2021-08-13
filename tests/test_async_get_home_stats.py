import pytest

from pytautulli import PyTautulli


@pytest.mark.asyncio
async def test_async_get_home_stats(client: PyTautulli):
    """test_async_get_home_stats."""
    data = await client.async_get_home_stats()
    assert data is not None
