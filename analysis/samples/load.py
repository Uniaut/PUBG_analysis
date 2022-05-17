import gzip
import json
import os
import urllib.request

from chicken_dinner.models.match import Match
from chicken_dinner.models.telemetry import Telemetry
from chicken_dinner.pubgapi import PUBG

def save_match_as_files(pubg: PUBG, match_id: str, path: str):
    match = pubg.match(match_id)
    match_path = os.path.join(path, f'match_{match.id}')
    os.makedirs(match_path, exist_ok=True)

    brief_path = os.path.join(match_path, 'match.json')
    with open(brief_path, 'w') as brief_file:
        brief_file.write(json.dumps(match.response, indent=4))

    telemetry = match.get_telemetry()
    
    telemetry_path = os.path.join(match_path, 'telemetry.json')
    with open(telemetry_path, 'w') as telemetry_file:
        telemetry_file.write(json.dumps(telemetry.response, indent=4))
    
    print(f'Match - {match.id} saved in {match_path}')
    return match, telemetry


def open_match_as_files(match_id: str, path: str):
    dir_path = os.path.join(path, f'match_{match_id}')
    match_path = os.path.join(dir_path, 'match.json')
    telemetry_path = os.path.join(dir_path, 'telemetry.json')

    with open(match_path, "r") as match_file:
        raw_json = json.load(match_file)
        match = Match.from_json(raw_json)
    
    with open(telemetry_path, "r") as telemetry_file:
        raw_json = json.load(telemetry_file)
        telemetry = Telemetry.from_json(raw_json)

    return match, telemetry


def load(match_id) -> tuple[Match, Telemetry]:
    samples_path = os.path.join(
        os.getcwd(),
        r'analysis\samples\samples',
    )
    try:
        match, telemetry = open_match_as_files(match_id, samples_path)
    except Exception as e:
        print(f'asfdasdf {e.with_traceback()}')
        match, telemetry = save_match_as_files(pubg, match_id, samples_path)
    
    return match, telemetry


def get_wrapper():
    api_key = None
    with open('my_api', mode='r') as api_key_file:
        api_key = api_key_file.read()
        print(api_key)
    
    return PUBG(api_key=api_key, shard='steam')


if __name__ == '__main__':
    pubg = get_wrapper()
    match_id_list = pubg.samples(start=None, shard='steam').match_ids

    for match_id in match_id_list[:1]:
        match, telemetry = load(match_id)
        print(match.id, telemetry.map_id())