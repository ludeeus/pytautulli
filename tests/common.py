import json
import os

from pytautulli import PyTautulliHostConfiguration, PyTautulli

TEST_RESPONSE_HEADERS = {"Content-Type": "application/json"}

TEST_HOST_CONFIGURATION = PyTautulliHostConfiguration(
    ipaddress="127.0.0.1", api_token="ur1234567-0abc12de3f456gh7ij89k012"
)


def mock_response(client: PyTautulli, status=200, data=None, message=None, raises=None):
    """Mock a response from the API."""

    async def _mocked_request(*args, **kwargs):
        if raises:
            raise raises
        return MockResponse(args[1], status=status, data=data, message=message)

    client._session._request = _mocked_request


def fixture(filename, asjson=True):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), "fixtures", f"{filename}.json")
    with open(path, encoding="utf-8") as fptr:
        if asjson:
            return json.loads(fptr.read())
        return fptr.read()


class MockResponse:
    def __init__(self, url: str, status=200, data=None, message=None):
        self.url = url
        self.status = status
        self.data = data
        self.message = message

    async def json(self):
        if self.data or self.message:
            return {
                "response": {
                    "data": self.data,
                    "message": self.message,
                    "result": "success" if self.status == 200 else "failure",
                }
            }
        cmd = self.url.split("&cmd=")[1].split("&")[0]
        try:
            return fixture(cmd)
        except OSError:
            return {}


class MockedRequests:
    _calls = []

    def add(self, url: str):
        self._calls.append(url)

    def clear(self):
        self._calls.clear()

    def __repr__(self) -> str:
        return f"<MockedRequests: {self._calls}>"

    @property
    def count(self) -> int:
        return len(self._calls)

    def has(self, string: str) -> bool:
        return bool([entry for entry in self._calls if string in entry])
