# pytautulli

[![codecov](https://codecov.io/gh/ludeeus/pytautulli/branch/main/graph/badge.svg)](https://codecov.io/gh/ludeeus/pytautulli)
![python version](https://img.shields.io/badge/Python-3.8=><=3.10-blue.svg)
[![PyPI](https://img.shields.io/pypi/v/pytautulli)](https://pypi.org/project/pytautulli)
![Actions](https://github.com/ludeeus/pytautulli/workflows/Actions/badge.svg?branch=main)

_Python API wrapper for Tautulli._

## Installation

```bash
python3 -m pip install pytautulli
```

## Example usage

More examples can be found in the `tests` directory.

```python
"""Example usage of pytautulli."""
import asyncio
from pytautulli import PyTautulli, PyTautulliHostConfiguration

IP = "192.168.100.3"
TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


async def async_example():
    """Example usage of pytautulli."""
    host_configuration = PyTautulliHostConfiguration(ipaddress=IP, api_token=TOKEN)
    async with PyTautulli(host_configuration=host_configuration) as client:
        print(await client.async_command("get_activity"))


asyncio.get_event_loop().run_until_complete(async_example())
```

## Contribute

**All** contributions are welcome!

1. Fork the repository
2. Clone the repository locally and open the devcontainer or use GitHub codespaces
3. Do your changes
4. Lint the files with `scripts/lint`
5. Ensure all tests passes with `scripts/test`
6. Ensure 100% coverage with `scripts/coverage`
7. Commit your work, and push it to GitHub
8. Create a PR against the `main` branch