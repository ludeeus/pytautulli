import logging

import pytest
from aiohttp import ClientSession

from pytautulli import PyTautulli

from .common import TEST_HOST_CONFIGURATION, MockResponse, MockedRequests

logging.basicConfig(level=logging.DEBUG)
pytestmark = pytest.mark.asyncio


@pytest.fixture()
def requests():
    yield MockedRequests()


@pytest.fixture()
async def client_session(requests):
    async def _mocked_request(*args, **kwargs):
        requests.add(args[1])
        return MockResponse(args[1])

    async with ClientSession() as session:
        requests.clear()
        session._request = _mocked_request
        yield session


@pytest.fixture()
async def client(client_session):
    async with PyTautulli(
        session=client_session, host_configuration=TEST_HOST_CONFIGURATION
    ) as obj:
        yield obj
