import datetime

import chicken_dinner.models.match as Match
import chicken_dinner.models.telemetry as Telemetry
from chicken_dinner.pubgapi import PUBG

import analysis.utils.auth as Auth
import analysis.samples.load as Load


def preprocess_location(location) -> tuple:
    return tuple(map(lambda v: v / 100, (location.x, location.y, location.z)))


def get_kills(telemetry_obj: Telemetry.Telemetry):
    modded_events = [
        (preprocess_location(event.killer.location), preprocess_location(event.victim.location))
        for event in telemetry_obj.filter_by('log_player_kill_v2')
        if event.killer is not None
    ]
    return modded_events

def test(telemetry_obj: Telemetry.Telemetry):
    modded_events = [
        (preprocess_location(event.killer.location), preprocess_location(event.victim.location), event)
        for event in telemetry_obj.filter_by('log_player_kill_v2')
        if event.killer is not None
    ]
    for a, b, event in modded_events:
        if int(sum(a)) * int(sum(b)) == 0:
            print([event])
    return modded_events

if __name__ == "__main__":
    pubg = Auth.pubg()

    samples = pubg.samples().match_ids[:2]
    for s_id in samples:
        print(f'Loading {s_id}')
        match = Load.load_match(pubg, s_id)
        telemetry = Load.load_telemetry(match)
        test(telemetry)
