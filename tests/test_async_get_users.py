import pytest

from pytautulli import PyTautulli


@pytest.mark.asyncio
async def test_async_get_users(client: PyTautulli):
    """test_async_get_users."""
    data = await client.async_get_users()
    assert data is not None
