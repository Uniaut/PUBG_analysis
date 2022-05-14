import datetime
import json
import matplotlib.pyplot as plt
import os

import chicken_dinner.models.match as Match
import chicken_dinner.models.telemetry as Telemetry
from chicken_dinner.pubgapi import PUBG
import util


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
            plt.plot(
                pos["x"], pos["y"], color=spectrum(idx / len(positions)), marker="o"
            )
    else:
        axis_key_pos = {axis: [pos[axis] for pos in positions] for axis in ["x", "y"]}
        plt.plot(*axis_key_pos.values())


def winner_position(match: Match.Match):
    """
    available only in 'solo' mode

    param:
    """
    tel: Telemetry.Telemetry = match.get_telemetry()
    chicken_player = tel.winner()[0]
    locations = tel.filter_by("log_player_position")  # 텔레메트리: 포지션으로 필터
    # 음수 시간: 대기실에서의 이동
    locations = [location for location in locations if location.elapsed_time > 0]

    player_positions = []  # 1등 경로
    start = datetime.datetime.strptime(
        tel.filter_by("log_match_start")[0].timestamp, "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    # 시작 시간 설정
    for location in locations:
        timestamp = datetime.datetime.strptime(
            location.timestamp, "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        dt = (timestamp - start).total_seconds()
        player = location.character.name  # log_player_position에 기록된 플레이어의 이름
        if player == chicken_player:  # 1등만 추출
            player_positions.append(
                {
                    "player": player,
                    "timestamp": dt,
                    "x": location.character.location.x / 1000,
                    "y": location.character.location.y / 1000,
                    "z": location.character.location.z / 1000,
                }
            )  # 1등 이름, 경과시간, x,y,z

    return player_positions


def open_match(match_id):
    match_path = os.path.join(
        r'C:\Users\kunwo\Documents\PUBG_API_takealook\PUBG_analysis\samples\samples',
        f'match_{match_id}',
        'match.json',
    )
    with open(match_path, "r") as match_file:
        raw_json = json.load(match_file.read())

    return raw_json


if __name__ == "__main__":
    api_key = None
    with open(".\\my_api", mode="r") as api_key_file:
        api_key = api_key_file.read()
        print(api_key)

    pubg = PUBG(api_key=api_key, shard='steam')

    sample_match_id = 'ca16964d-f44b-4714-b40c-78bb8607b688'
    '''
    raw_json = open_match(sample_match_id)
    match = PUBGMatch(raw=raw_json)
    '''
    match = pubg.match(sample_match_id)
    sample_position = winner_position(match)

    map_id = match.map_id.replace(" ", "_")
    util.plot_map(map_id, "High")
    plot_positions(sample_position)
    plt.show()
