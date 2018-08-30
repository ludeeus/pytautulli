# pytautulli - A python module to get information from Tautulli

[![Build Status](https://travis-ci.org/ludeeus/pytautulli.svg?branch=master)](https://travis-ci.org/ludeeus/pytautulli)

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

pytautulli.get_user_state(host, port, api_key, user)
> 'playing'

pytautulli.get_user_activity(host, port, api_key, user)
> This return a BIG list of all possible values from the activity endpoint.

pytautulli.get_home_stats(host, port, api_key)
> {'User': 'user3', 'TV': 'NCIS', 'Movie': 'Bad Boys 2'}
```
