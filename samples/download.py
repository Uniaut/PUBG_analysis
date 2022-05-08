'''
get_sample_matches

get matches from sample in pubg api

1. get wrapper
2. get samples
3. iterating samples if it is solo:
    3.1. load & save match.json
    3.2. load & save telemetry.json

directory
matches
L match_0
  L breif
  L telemetry
L match_1
  L breif
  L telemetry
.
.
.

'''
import gzip
import json
import os
import urllib.request

from chicken_dinner.models.match import Match as PUBGMatch
from chicken_dinner.pubgapi import PUBG

import chicken_dinner

def save_match_as_files(match: PUBGMatch, path):
    match_path = os.path.join(path, f'match_{match.id}')
    os.makedirs(match_path, exist_ok=True)

    brief_path = os.path.join(match_path, 'brief.json')
    with open(brief_path, 'w') as brief_file:
        brief_file.write(json.dumps(match.data, indent=4))

    telemetry_url = match.telemetry_url
    telemetry_reqest = urllib.request.Request(
        telemetry_url,
        headers={
            'Accept':'application/vnd.api+json',
            'Accept-Encoding': 'gzip',
        }
    )
    with urllib.request.urlopen(telemetry_reqest) as telemetry_response:
        telemetry_json = json.loads(gzip.decompress(telemetry_response.read()))
    
    telemetry_path = os.path.join(match_path, 'telemetry.json')
    with open(telemetry_path, 'w') as telemetry_file:
        telemetry_file.write(json.dumps(telemetry_json, indent=4))
    
    print(f'Match - {match_id} saved in {match_path}')


def get_wrapper():
    api_key = None
    with open('my_api', mode='r') as api_key_file:
        api_key = api_key_file.read()
        print(api_key)
    
    return PUBG(api_key=api_key, shard='steam')


if __name__ == '__main__':
    request_wrapper = get_wrapper()
    match_id_list = request_wrapper.samples(start=None, shard='steam').match_ids

    for match_id in match_id_list[:]:
        match = request_wrapper.match(match_id)
        print(f'Summary of MATCH: {match_id}')
        print(f'game_mode: {match.game_mode}')
        print(f'map_name: {match.map_name}')
        print(f'duration: {match.duration}')
        if match.game_mode == 'solo' and match.map_id != 'Range_Main':
            save_match_as_files(match, '.\\samples\\samples')
    
