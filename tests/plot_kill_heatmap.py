import datetime
import json
import matplotlib.pyplot as plt
import os

import chicken_dinner.models.match as Match
import chicken_dinner.models.telemetry as Telemetry
from chicken_dinner.pubgapi import PUBG
import utils.kill


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


def plot_kill(kills: list, *, enable_lines: bool):
    for killer_loction, victim_lociton in kills:
        kx, ky, _ = killer_loction
        vx, vy, _ = victim_lociton
        plt.plot(kx, ky, color="#FF0000", marker="x")
        plt.plot(vx, vy, color="#00FF00", marker="o")

        if enable_lines:
            plt.arrow(
                kx,
                ky,
                vx - kx,
                vy - ky,
                color="white",
            )


def open_tel(match_id):
    tel_path = os.path.join(
        r"C:\Users\kunwo\Documents\PUBG_API_takealook\PUBG_analysis\samples\samples",
        f"match_{match_id}",
        "telemetry.json",
    )
    with open(tel_path, "r") as tel_file:
        raw_json = json.load(tel_file)

    return raw_json


if __name__ == "__main__":
    api_key = None
    with open(r".\my_api", mode="r") as api_key_file:
        api_key = api_key_file.read()
        print(api_key)

    pubg = PUBG(api_key=api_key, shard="steam")

    sample_match_id = "ca16964d-f44b-4714-b40c-78bb8607b688"
    match = pubg.match(sample_match_id)
    tel = Telemetry.Telemetry.from_json(open_tel(sample_match_id))

    kill_datas = utils.kill.get_kills(tel)

    map_id = match.map_id.replace(" ", "_")
    utils.plot_map(map_id, "High")
    plot_kill(kill_datas, enable_lines=True)
    plt.show()