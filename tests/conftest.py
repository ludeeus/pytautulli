import logging

import pytest
from aiohttp import ClientSession

from pytautulli import PyTautulli

from .common import TEST_HOST_CONFIGURATION, MockedRequests, MockResponse

logging.basicConfig(level=logging.DEBUG)
pytestmark = pytest.mark.asyncio


@pytest.fixture()
def requests():
    yield MockedRequests()


@pytest.fixture()
def response():
    yield MockResponse()


@pytest.fixture()
async def client_session(response, requests):
    async def _mocked_request(*args, **kwargs):
        response.url = args[1]
        requests.add(args[1])
        return response

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
