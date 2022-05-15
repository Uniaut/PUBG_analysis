import datetime
import json
import matplotlib.pyplot as plt
import os

import chicken_dinner.models.match as Match
import chicken_dinner.models.telemetry as Telemetry
from chicken_dinner.pubgapi import PUBG
import utils


def spectrum(progress) -> str:
    if progress < 1 / 3:
        subprog = round(progress * 3 * 255)
        value = (255 - subprog, subprog, 0)
    elif progress < 2 / 3:
        subprog = round((progress * 3 - 1) * 255)
        value = (0, 255 - subprog, subprog)
    else:
        subprog = round((progress * 3 - 2) * 255)
        value = (subprog, 0, 255 - subprog)

    return "#%02x%02x%02x" % value


def plot_positions(positions: list, spectrum_dot_mode=True):
    if spectrum_dot_mode:
        for idx, pos in enumerate(positions):
            location = pos[1]
            x, y, z = location
            plt.plot(
                x, y, color=spectrum(idx / len(positions)), marker="o"
            )
    else:
        axis_key_pos = {axis: [pos[1][axis] for pos in positions] for axis in [0, 1]}
        plt.plot(*axis_key_pos.values())


def open_tel(match_id):
    tel_path = os.path.join(
        r'C:\Users\kunwo\Documents\PUBG_API_takealook\PUBG_analysis\samples\samples',
        f'match_{match_id}',
        'telemetry.json',
    )
    with open(tel_path, "r") as tel_file:
        raw_json = json.load(tel_file)

    return raw_json


if __name__ == "__main__":
    api_key = None
    with open(".\\my_api", mode="r") as api_key_file:
        api_key = api_key_file.read()
        print(api_key)

    pubg = PUBG(api_key=api_key, shard='steam')

    sample_match_id = 'ca16964d-f44b-4714-b40c-78bb8607b688'
    match = pubg.match(sample_match_id)
    tel = Telemetry.Telemetry.from_json(open_tel(sample_match_id))

    sample_position = utils.get_position(tel, search_all=True)[match.winner.player_names[0]].positions

    map_id = match.map_id.replace(" ", "_")
    utils.plot_map(map_id, "High")
    plot_positions(sample_position, spectrum_dot_mode=False)
    plt.show()
