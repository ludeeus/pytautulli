import pytest
from aiohttp.client import ClientSession

from pytautulli import PyTautulli, PyTautulliException
from tests.common import TEST_HOST_CONFIGURATION


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
        base_api_path="",
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
async def test_redact_token():
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
