"""
A python module to get information from Tautulli.

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import requests

__version__ = '0.0.2'

def get_users(host, port, api_key):
    """Get the last activity for the spesified user"""
    cmd = 'get_users'
    url = "http://{}:{}/api/v2?apikey={}&cmd={}".format(host, port, api_key, cmd)
    users = []
    try:
        result = requests.get(url, timeout=8).json()
        result = result['response']['data']
        for user_data in result:
            users.append(user_data['username'])
    except:
        users.append('None')
    return users

def verify_user(host, port, api_key, username):
    """Get the last activity for the spesified user"""
    cmd = 'get_users'
    url = "http://{}:{}/api/v2?apikey={}&cmd={}".format(host, port, api_key, cmd)
    try:
        result = requests.get(url, timeout=8).json()
        result = result['response']['data']
        for user_data in result:
            if user_data['username'].lower() == username.lower():
                user = True
                break
            else:
                user = False
    except:
        user = False
    return user

def get_user_state(host, port, api_key, username):
    """Get the last activity for the spesified user"""
    verify_user(host, port, api_key, username)
    cmd = 'get_activity'
    url = "http://{}:{}/api/v2?apikey={}&cmd={}".format(host, port, api_key, cmd)
    user_state = 'not available'
    try:
        result = requests.get(url, timeout=8).json()
        result = result['response']['data']['sessions']
        for sessions in result:
            if sessions['username'].lower() == username.lower():
                user_state = sessions['state']
                break
    except:
        user_state = 'not available'
    return user_state

def get_user_activity(host, port, api_key, username):
    """Get the last activity for the spesified user"""
    verify_user(host, port, api_key, username)
    cmd = 'get_activity'
    url = "http://{}:{}/api/v2?apikey={}&cmd={}".format(host, port, api_key, cmd)
    user_activity = 'not available'
    try:
        result = requests.get(url, timeout=8).json()
        result = result['response']['data']['sessions']
        for sessions in result:
            if sessions['username'].lower() == username.lower():
                user_activity = sessions
                break
    except:
        user_activity = 'not available'
    return user_activity

def get_home_stats(host, port, api_key):
    """Get the last activity for the spesified user"""
    cmd = 'get_home_stats'
    url = "http://{}:{}/api/v2?apikey={}&cmd={}".format(host, port, api_key, cmd)
    home_stats = {}
    try:
        result = requests.get(url, timeout=8).json()
        result = result['response']['data']
    except:
        home_stats.update(Status="not available")
    if result:
        try:
            if result[0]['rows'][0]['title']:
                home_stats.update(Movie=result[0]['rows'][0]['title'])
        except:
            home_stats.update(Movie="None")
        try:
            if result[3]['rows'][0]['title']:
                home_stats.update(TV=result[3]['rows'][0]['title'])
        except:
            home_stats.update(TV="None")
        try:
            if result[7]['rows'][0]['user']:
                home_stats.update(User=result[7]['rows'][0]['user'])
        except:
            home_stats.update(User="None")
    return home_stats
