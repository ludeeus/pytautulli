import asyncio
import json

import aiohttp
import pytest
from aiohttp.client import ClientSession

from pytautulli import (
    PyTautulli,
    PyTautulliApiResponse,
    PyTautulliAuthenticationException,
    PyTautulliConnectionException,
    PyTautulliException,
    PyTautulliHostConfiguration,
    PyTautulliJJSONEncoder,
)
from pytautulli.const import HTTPMethod
from pytautulli.decorator import api_command
from tests.common import TEST_HOST_CONFIGURATION, MockedRequests, MockResponse, fixture


@pytest.mark.asyncio
async def test_create_client():
    target_url = f"http://{TEST_HOST_CONFIGURATION.ipaddress}:8181/api/v2?apikey={TEST_HOST_CONFIGURATION.api_token}&cmd="

    async with ClientSession() as session:
        client = PyTautulli(session=session, host_configuration=TEST_HOST_CONFIGURATION)
        assert client._host.api_url("") == target_url

    async with PyTautulli(
        host_configuration=TEST_HOST_CONFIGURATION,
        ssl=False,
        port=8181,
        verify_ssl=True,
        base_api_path="/test",
    ) as client:
        assert (
            client._host.api_url("")
            == f"http://{TEST_HOST_CONFIGURATION.ipaddress}:8181/test/api/v2?apikey={TEST_HOST_CONFIGURATION.api_token}&cmd="
        )

    async with PyTautulli(
        api_token=TEST_HOST_CONFIGURATION.api_token,
        url=f"http://{TEST_HOST_CONFIGURATION.ipaddress}:8181",
    ) as client:
        assert client._host.api_url("") == target_url

    with pytest.raises(
        PyTautulliException, match="No api token to the tautulli server was provided"
    ):
        async with PyTautulli(ipaddress=TEST_HOST_CONFIGURATION.ipaddress):
            pass

    with pytest.raises(
        PyTautulliException,
        match="No url, hostname or ipaddress to the tautulli server was provided",
    ):
        async with PyTautulli(api_token=TEST_HOST_CONFIGURATION.api_token):
            pass

    async with PyTautulli(host_configuration=TEST_HOST_CONFIGURATION) as client:
        assert client._host.api_url("") == target_url


@pytest.mark.asyncio
async def test_redact_token(client: PyTautulli, caplog: pytest.LogCaptureFixture):
    """Test method for token redaction."""
    async with PyTautulli(host_configuration=TEST_HOST_CONFIGURATION) as client:
        assert (
            client.redact_string(f"String with {client._host.api_token}")
            == "String with [REDACTED_API_TOKEN]"
        )
    async with PyTautulli(
        host_configuration=TEST_HOST_CONFIGURATION, redact=False
    ) as client:
        assert (
            client.redact_string(f"String with {client._host.api_token}")
            == f"String with {client._host.api_token}"
        )


@pytest.mark.asyncio
async def test_redact_token_log(client: PyTautulli, caplog: pytest.LogCaptureFixture):
    """Test method for token redaction."""
    await client.async_command("test_command")
    assert "?apikey=[REDACTED_API_TOKEN]&" in caplog.text
    assert client._host.api_token not in caplog.text


@pytest.mark.asyncio
async def test_async_command(client: PyTautulli, requests: MockedRequests):
    """Test async command."""
    data = await client.async_command("test_command")
    assert isinstance(data, dict)
    assert data.get("response").get("data") == {}

    assert requests.count == 1
    assert requests.has("&cmd=test_command")

    data = await client.async_command("test_command", **{"limit": 1})
    assert requests.count == 2
    assert requests.has("&cmd=test_command&limit=1")


@pytest.mark.asyncio
async def test_async_authentication_failure(client: PyTautulli, response: MockResponse):
    """test_async_authentication_failure."""
    response.mock_status = 401
    response.mock_message = "No authentication"

    with pytest.raises(PyTautulliAuthenticationException, match="No authentication"):
        await client.async_command("test_command")


@pytest.mark.asyncio
async def test_async_connection_error(client: PyTautulli, response: MockResponse):
    """test_async_authentication_failure."""
    response.mock_status = 500

    with pytest.raises(
        PyTautulliConnectionException, match="failed with status code '500'"
    ):
        await client.async_command("test_command")

    response.mock_status = 200
    response.mock_raises = aiohttp.ClientError

    with pytest.raises(PyTautulliConnectionException):
        await client.async_command("test_command")

    response.mock_raises = asyncio.TimeoutError
    with pytest.raises(PyTautulliConnectionException):
        await client.async_command("test_command")

    response.mock_raises = PyTautulliException
    with pytest.raises(PyTautulliException):
        await client.async_command("test_command")

    response.mock_raises = Exception
    with pytest.raises(PyTautulliException):
        await client.async_command("test_command")

    response.mock_raises = BaseException
    with pytest.raises(PyTautulliException):
        await client.async_command("test_command")


@pytest.mark.asyncio
async def test_method_data(client: PyTautulli):
    """test_method_data."""

    @api_command("command")
    async def async_command(self, command: str, **kwargs):
        return "lorem ipsum"

    client.async_command = async_command

    await client.async_command(client, "test_command")


@pytest.mark.asyncio
async def test_base(client: PyTautulli):
    """test_method_data."""
    data = await client.async_get_activity()
    assert "PyTautulliApiActivity" in repr(data)


def test_json():
    """Test json."""
    encoder = PyTautulliJJSONEncoder()

    assert encoder.default(PyTautulliApiResponse(fixture("test_command"))) == {}
    assert encoder.default(HTTPMethod.GET) == "GET"
    with pytest.raises(TypeError):
        assert encoder.default(None)


def test_api_url():
    """Test api_url."""
    config = PyTautulliHostConfiguration(api_token="test", url="http://test.com")
    assert config.api_url("") == "http://test.com:80/api/v2?apikey=test&cmd="

    config = PyTautulliHostConfiguration(api_token="test", url="http://test.com/")
    assert config.api_url("") == "http://test.com:80/api/v2?apikey=test&cmd="

    config = PyTautulliHostConfiguration(api_token="test", url="http://test.com//")
    assert config.api_url("") == "http://test.com:80/api/v2?apikey=test&cmd="

    config = PyTautulliHostConfiguration(api_token="test", url="http://test.com/test")
    assert config.api_url("") == "http://test.com:80/test/api/v2?apikey=test&cmd="

    config = PyTautulliHostConfiguration(api_token="test", url="http://test.com/test/")
    assert config.api_url("") == "http://test.com:80/test/api/v2?apikey=test&cmd="

    config = PyTautulliHostConfiguration(api_token="test", url="http://test.com/test//")
    assert config.api_url("") == "http://test.com:80/test/api/v2?apikey=test&cmd="

    config = PyTautulliHostConfiguration(api_token="test", url="https://test.com/")
    assert config.api_url("") == "https://test.com:443/api/v2?apikey=test&cmd="

    config = PyTautulliHostConfiguration(api_token="test", url="https://test.com:80/")
    assert config.api_url("") == "https://test.com:80/api/v2?apikey=test&cmd="

    config = PyTautulliHostConfiguration(api_token="test", url="https://test.com:80/")
    assert config.api_url("") == "https://test.com:80/api/v2?apikey=test&cmd="
