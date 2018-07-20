# pytautulli - A python module to get information from Tautulli

## Notes

This has been tested with python 3.6  
This module require API key from Tautulli.  
This module uses these external libararies:

- requests

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

tautulli.get_users(host, port, api_key)
> ['user1', 'user3']

tautulli.verify_user(host, port, api_key, user)
> True

tautulli.get_user_state(host, port, api_key, user)
> 'playing'

tautulli.get_user_activity(host, port, api_key, user)
> This return a BIG list of all possible values from the activity endpoint.

tautulli.get_home_stats(host, port, api_key)
> {'User': 'user3', 'TV': 'NCIS', 'Movie': 'Bad Boys 2'}
```
