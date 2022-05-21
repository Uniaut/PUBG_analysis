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
from collections.abc import Callable
from functools import wraps
import glob
import json
import os
import pickle
from typing import Any 
from typing import TypeVar

from chicken_dinner.models.match import Match
from chicken_dinner.models.telemetry import Telemetry
from chicken_dinner.pubgapi import PUBG


SAMPLES_PATH = os.path.join(os.getcwd(), r'analysis\samples\samples')


def _file_path(match_id, file_name):
    return os.path.join(SAMPLES_PATH, f'match_{match_id}', file_name)


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
    print(f'[WARNING]\tDeprecated function: {load_telemetry.__name__}')
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
    print(f'[WARNING]\tDeprecated function: {load_match.__name__}')
    try:
        match = _open_match_from_file(pubg, match_id, SAMPLES_PATH)
    except Exception as e:
        print(f'[ERR]\t{e}')
        print(f'[LOG]\tNo match - {match_id}')
        match = _save_match_as_file(pubg, match_id, SAMPLES_PATH)

    return match


def _is_pickle_exists(match_id, file_name):
    pickle_path = _file_path(match_id, file_name)
    return os.path.exists(pickle_path)


def _open_obj_from_pickle(match_id, file_name):
    pickle_path = _file_path(match_id, file_name)
    with open(pickle_path, 'rb') as pickle_file:
        obj = pickle.load(pickle_file)
    return obj


def _save_obj_as_pickle(match_id, file_name, obj):
    pickle_path = _file_path(match_id, file_name)
    os.makedirs(os.path.dirname(pickle_path), exist_ok=True)
    with open(pickle_path, 'wb') as pickle_file:
        pickle.dump(obj, pickle_file)
    return obj


R = TypeVar('R')
def pickle_loader(_name: str):
    '''
    [Decorator] save result as pickle
    if pickle exists load else run func
    param:
    _name - file name
    _mid - match id
    *args - function arguments 
    '''
    def wrap(func: Callable[..., R]) -> Callable[..., R]:
        @wraps(func)
        def inside(_mid: str, *args, **kwargs) -> R:
            if _mid is None:
                return func(*args)

            if _is_pickle_exists(_mid, _name):
                obj = _open_obj_from_pickle(_mid, _name)
            else:
                print(f'[LOG]\tNo pickle \'{_name}\' in {_mid}')
                obj = _save_obj_as_pickle(_mid, _name, func(*args))
            return obj
        return inside
    return wrap


@pickle_loader('match.pickle')
def get_match(pubg: PUBG, match_id: str) -> Match:
    return pubg.match(match_id)


@pickle_loader('telemetry.pickle')
def get_telemetry(match: Match) -> Telemetry:
    return match.get_telemetry()


def samples() -> list[str]:
    return [s[-36:] for s in glob.glob(f'{SAMPLES_PATH}/match_*', recursive=False)]
