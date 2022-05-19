from chicken_dinner.pubgapi import PUBG


def pubg():
    api_key = None
    with open('my_api', mode='r') as api_key_file:
        api_key = api_key_file.read()
        print('Auth key:', api_key)
    
    return PUBG(api_key=api_key, shard='steam')