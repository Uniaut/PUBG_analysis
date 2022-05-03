import gzip
import json
import os
import urllib.request
from chicken_dinner.pubgapi import PUBG


def save_telemety_as_file(match_id, url):
    req = urllib.request.Request(
        url,
        headers={
            'Accept':'application/vnd.api+json',
            'Accept-Encoding': 'gzip',
        }
    )
    file_name = f'match_telemetry_{match_id}.json'
    file_path = os.path.join('./telemetry', file_name)
    with urllib.request.urlopen(req) as response, open(file_path, 'w') as match_telemetry:
        json_data = json.loads(
            gzip.decompress(response.read())
        )
        match_telemetry.write(
            json.dumps(json_data, indent=4)
        )
        print(f'Match - {match_id} saved in telemetry directory')


def get_position(tmatch):
    temp=pubg.match(tmatch)
    temp_url=temp.telemetry_url
    position=pubg.telemetry(temp_url).player_positions()
    return position

if __name__ == '__main__':
    api_key = None
    with open('my_api', mode='r') as api_key_file:
        api_key = api_key_file.read()
        print(api_key)

    pubg = PUBG(api_key=api_key, shard='steam')
    match_list = pubg.samples(start=None, shard='steam').data['relationships']['matches']['data']
    match_id_list = [d['id']for d in match_list]

    for match_id in match_id_list[:1]:
        match = pubg.match(match_id)
        print(f'Summary of MATCH: {match_id}')
        print(f'game_mode: {match.game_mode}')
        print(f'map_name: {match.map_name}')
        print(f'duration: {match.duration}')
        print(f'telemetry_url: {match.telemetry_url}')
        save_telemety_as_file(match_id, match.telemetry_url)
    
