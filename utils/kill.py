import datetime


import chicken_dinner.models.match as Match
import chicken_dinner.models.telemetry as Telemetry
from chicken_dinner.pubgapi import PUBG


def get_kills(telemetry_obj: Telemetry.Telemetry):
    modded_events = [(event.killer, event.victim) for event in telemetry_obj.filter_by('log_player_kill_v2')]
    return modded_events

if __name__ == "__main__":
    api_key = None
    with open(r".\my_api", mode="r") as api_key_file:
        api_key = api_key_file.read()
        print(api_key)

    pubg = PUBG(api_key=api_key, shard="steam")

    sample_match_id = "ca16964d-f44b-4714-b40c-78bb8607b688"
    match = pubg.match(sample_match_id)
    telem = match.get_telemetry()

    get_kills(telem)
