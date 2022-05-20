import glob
import json
import os

from chicken_dinner.models.match import Match
from chicken_dinner.models.telemetry import Telemetry
from chicken_dinner.pubgapi import PUBG

import analysis.utils.auth as Auth


SAMPLES_PATH = os.path.join(os.getcwd(), r'analysis\samples\samples')

def _save_telemetry_as_file(match: Match, path: str) -> Telemetry:
    telemetry = match.get_telemetry()
    
    telemetry_path = os.path.join(path, f'match_{match.id}', 'telemetry.json')
    with open(telemetry_path, 'w') as telemetry_file:
        telemetry_file.write(json.dumps(telemetry.response, indent=4))
    
    print(f'Telemetry saved in {telemetry_path}')
    return telemetry


def _open_telemetry_from_file(match_id: str, path: str) -> Telemetry:
    telemetry_path = os.path.join(path, f'match_{match_id}', 'telemetry.json')
    with open(telemetry_path, "r") as telemetry_file:
        raw_json = json.load(telemetry_file)
        telemetry = Telemetry.from_json(raw_json)

    return telemetry


def load_telemetry(match: Match) -> Telemetry:
    try:
        telemetry = _open_telemetry_from_file(match.id, SAMPLES_PATH)
    except Exception as e:
        print(f'[ERR]\t{e.__str__()}')
        print(f'[LOG]\tNo telemetry - {match.id}')
        telemetry = _save_telemetry_as_file(match, SAMPLES_PATH)
    
    return telemetry


def _save_match_as_file(pubg: PUBG, match_id: str, path: str):
    match = pubg.match(match_id)

    dir_path = os.path.join(path, f'match_{match_id}')
    os.makedirs(dir_path, exist_ok=True)
    match_path = os.path.join(dir_path, 'match.json')
    with open(match_path, 'w') as brief_file:
        brief_file.write(json.dumps(match.response, indent=4))
    
    print(f'Match saved in {match_path}')
    return match


def _open_match_from_file(pubg: PUBG, match_id: str, path: str) -> Match:
    match_path = os.path.join(path, f'match_{match_id}', 'match.json')
    with open(match_path, "r") as match_file:
        raw_json = json.load(match_file)
        match = Match.from_json(raw_json, pubg, None, pubg.shard)

    return match


def load_match(pubg: PUBG, match_id: str) -> Match:
    try:
        match = _open_match_from_file(pubg, match_id, SAMPLES_PATH)
    except Exception as e:
        print(f'[ERR]\t{e.__str__()}')
        print(f'[LOG]\tNo match - {match_id}')
        match = _save_match_as_file(pubg, match_id, SAMPLES_PATH)

    return match


def samples() -> list[str]:
    return [s[-36:] for s in glob.glob(f'{SAMPLES_PATH}/match_*', recursive=False)]


if __name__ == '__main__':
    print(samples())
    
    pubg = Auth.pubg()
    match_id_list = pubg.samples(start=None, shard='steam').match_ids

    for match_id in match_id_list[100:101]:
        print(f'[LOG]\tLoading {match_id}')
        match = load_match(pubg, match_id)
        telemetry = load_telemetry(match)
        print(f'[LOAD]\t{telemetry.map_id()}')
    
