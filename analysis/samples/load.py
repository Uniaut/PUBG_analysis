'''
Hierachy:

samples
L match_0
  L match
  L telemetry
  L pickle_0
  L pickle_1
L match_1
  L match
  L telemetry
  L pickle_0
  L pickle_1
L ...

'''
import glob
import json
import os
import pickle

from chicken_dinner.models.match import Match
from chicken_dinner.models.telemetry import Telemetry
from chicken_dinner.pubgapi import PUBG


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
        print(f'[ERR]\t{e}')
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
        print(f'[ERR]\t{e}')
        print(f'[LOG]\tNo match - {match_id}')
        match = _save_match_as_file(pubg, match_id, SAMPLES_PATH)

    return match

'''
if exists(match_id, file_name):
    load(match_id, file_name)
else:
    save(match_id, file_name)
'''

def _is_pickle_exists(match_id, file_name):
    pickle_path = os.path.join(SAMPLES_PATH, f'match_{match_id}', file_name)
    return os.path.exists(pickle_path)


def _open_obj_from_pickle(match_id, file_name):
    pickle_path = os.path.join(SAMPLES_PATH, f'match_{match_id}', file_name)
    with open(pickle_path, 'rb') as pickle_file:
        obj = pickle.load(pickle_file)
    return obj


def _save_obj_as_pickle(match_id, file_name, obj):
    pickle_path = os.path.join(SAMPLES_PATH, f'match_{match_id}', file_name)
    with open(pickle_path, 'wb') as pickle_file:
        pickle.dump(obj, pickle_file)
    return obj


def pickle_loader(_name):
    '''
    [Decorator] save result as pickle
    if there is pickle, just load 
    '''
    def wrap(func):
        def inside(*args, match_id: str=None):
            if match_id is None:
                return func(*args)

            if _is_pickle_exists(match_id, _name):
                obj = _open_obj_from_pickle(match_id, _name)
            else:
                print(f'[LOG]\tNo pickle \'{_name}\' in {match_id}')
                obj = _save_obj_as_pickle(match_id, _name, func(*args))
            return obj
        return inside
    return wrap


@pickle_loader('modify')
def modify(telemetry: Telemetry):
    return telemetry.circle_positions()


def samples() -> list[str]:
    return [s[-36:] for s in glob.glob(f'{SAMPLES_PATH}/match_*', recursive=False)]
