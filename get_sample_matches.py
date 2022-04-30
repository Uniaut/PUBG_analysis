from chicken_dinner.pubgapi import PUBG


api_key = None
with open('my_api', mode='r') as api_key_file:
    api_key = api_key_file.read()
    print(api_key)

pubg = PUBG(api_key=api_key, shard="steam")
matches_list = pubg.samples(start=None, shard='steam').data['relationships']['matches']['data']
match_id_list = [d['id']for d in matches_list]
print('\n'.join(match_id_list))