import datetime


import chicken_dinner.models.match as Match
import chicken_dinner.models.telemetry as Telemetry
from chicken_dinner.pubgapi import PUBG


class Position:
    def __init__(self, positions: list) -> None:
        self.positions = positions

    def __getitem__(self, _k) -> tuple[float, float, float]:
        # TODO: binary search + interpolation
        return (0.0, 0.0, 0.0)


def get_position(telemetry_obj: Telemetry.Telemetry, *, search_all: bool) -> dict[str, Position]:
    modded_events = [
        (event.character.name, event.character.location, event.timestamp)
        for event in telemetry_obj.events
        if hasattr(event, "character")
    ]
    start_timestamp = telemetry_obj.filter_by("log_match_start")[0].timestamp
    # print(modded_events[:10])

    temp_dict: dict[str, list] = {}
    for name, location, timestamp in modded_events:
        elapsed_time = datetime.datetime.strptime(
            timestamp, "%Y-%m-%dT%H:%M:%S.%fZ"
        ) - datetime.datetime.strptime(start_timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
        location_tuple = tuple(map(lambda v: v / 100, (location.x, location.y, location.z)))
        temp_dict.setdefault(name, []).append(
            (elapsed_time.total_seconds(), location_tuple)
        )

    return {k: Position(v) for k, v in temp_dict.items()}


if __name__ == "__main__":
    api_key = None
    with open(r".\my_api", mode="r") as api_key_file:
        api_key = api_key_file.read()
        print(api_key)

    pubg = PUBG(api_key=api_key, shard="steam")

    sample_match_id = "ca16964d-f44b-4714-b40c-78bb8607b688"
    match = pubg.match(sample_match_id)
    telem = match.get_telemetry()

    get_position(telem, None, search_all=True)
