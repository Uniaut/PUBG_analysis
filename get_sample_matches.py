from chicken_dinner.pubgapi import PUBG


api_key = None
with open('my_api', mode='r') as api_key_file:
    api_key = api_key_file.read()
    print(api_key)

pubg = PUBG(api_key=api_key, shard='steam')
match_list = pubg.samples(start=None, shard='steam').data['relationships']['matches']['data']
match_id_list = [d['id']for d in match_list]

for match_id in match_id_list:
    match = pubg.match(match_id)
    print(f'Summary of MATCH: {match_id}')
    print(f'game_mode: {match.game_mode}')
    print(f'map_name: {match.map_name}')
    print(f'duration: {match.duration}')
    print(f'telemetry_url: {match.telemetry_url}')