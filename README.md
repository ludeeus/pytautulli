# pytautulli [![Build Status](https://travis-ci.org/ludeeus/pytautulli.svg?branch=master)](https://travis-ci.org/ludeeus/pytautulli) [![PyPI version](https://badge.fury.io/py/pytautulli.svg)](https://badge.fury.io/py/pytautulli)

_A python module to get information from Tautulli._

## Notes

This module require API key from Tautulli.  

## Install

```bash
pip install pytautulli
```

## Example usage

```python
import pytautulli

api_key = 'VHLZFXXXP5SBL4OWSAPM0G8KCCXX0A9MA9E3XWNG'
host = '192.168.1.43'
port = '8181'
username = 'username'

pytautulli.get_users(host, port, api_key)
> ['user1', 'user3']

pytautulli.verify_user(host, port, api_key, user)
> True

pytautulli.get_server_stats(host, port, api_key)
> {'direct_plays': 0, 'wan_bandwidth': 0, 'count_transcode': 0, 'total_bandwidth': 0, 'direct_streams': 0, 'count': '0', 'lan_bandwidth': 0}

pytautulli.get_user_state(host, port, api_key, user)
> 'playing'

pytautulli.get_user_activity(host, port, api_key, user)
> This return a BIG list of all possible values from the activity endpoint.

pytautulli.get_most_stats(host, port, api_key)
> {'User': 'user3', 'TV': 'NCIS', 'Movie': 'Bad Boys 2'}
```

All functions has `schema='http'`, this can be ovverwritten by;

```python
schema = 'https'
pytautulli.get_users(host, port, api_key, schema)
```