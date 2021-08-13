import pytest

from pytautulli import PyTautulli


@pytest.mark.asyncio
async def test_async_get_activity(client: PyTautulli):
    """test_async_get_activity."""
    data = await client.async_get_activity()
    assert data
