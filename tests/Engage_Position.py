import gzip
import json
import os
import datetime
import numpy as np
from math import sin, cos
import PIL.Image
import os.path

import matplotlib.pyplot as plt
import matplotlib.patches as patches  # 원 추가
import math
from matplotlib.animation import FuncAnimation
import pandas as pd
import urllib.request as req

import chicken_dinner.models.match as PUBG_match
import chicken_dinner.models.telemetry as PUBG_telemetry
from chicken_dinner.pubgapi import PUBG


def plot_map_img(map_name=None, res_option="Low"):
    url = f"https://github.com/pubg/api-assets/raw/master/Assets/Maps/{map_name}_Main_{res_option}_Res.png"
    img_np = np.array(PIL.Image.open(req.urlopen(url)))
    plt.imshow(img_np)


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


# 1등 플레이어만이 아니라 애가 죽인 애들 동선도 표시해야 해서 스펙트럼으로 표현하면 너무 복잡함
def plot_positions(positions: list, spectrum_dot_mode=True):
    if spectrum_dot_mode:
        for idx, pos in enumerate(positions):
            plt.plot(pos["x"], pos["y"], color="b", marker="o")
    else:
        axis_key_pos = {axis: [pos[axis] for pos in positions] for axis in ["x", "y"]}
        plt.plot(*axis_key_pos.values())


def winner_position(match: PUBG_match.Match):
    """
    available only in 'solo' mode
    param:
    """
    tel = match.get_telemetry()
    chicken_player = tel.winner()[0]
    locations = tel.filter_by("log_player_position")  # 텔레메트리: 포지션으로 필터
    locations = [location for location in locations if location.elapsed_time > 0]
    # 게임 시작 후 경과시간 0 이상인 것들만 찾기// 찾아보니까 본 게임 시작하기 전에 다같이 모여 있는 광장이 있던데 여기서 움직이는 걸 제외한 것이라고 보여요

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

    # log_player_attack#log_player_take_damage#log_player_use_throwable#log_weapon_fire_count


def Winner_Kill_Position(match: PUBG_match.Match):
    tel = match.get_telemetry()
    chicken_player = tel.winner()[0]  # 1등 플레이어 =chicken
    start = datetime.datetime.strptime(
        tel.filter_by("log_match_start")[0].timestamp, "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    kill_log = tel.filter_by("log_player_kill_v2")
    global kill_position
    kill_position = []

    for kill_event in kill_log:
        timestamp = datetime.datetime.strptime(
            kill_event.timestamp, "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        dt = (timestamp - start).total_seconds()

        try:
            player = kill_event.finisher.name
        except AttributeError:
            continue

        if player == chicken_player and player == kill_event.killer.name:
            kill_position.append(
                {
                    "Killer": player,
                    "Victim": kill_event.victim.name,
                    "Time": dt,
                    "x": kill_event.finisher.location.x / 1000,
                    "y": kill_event.finisher.location.y / 1000,
                    "z": kill_event.finisher.location.z / 1000,
                    "Victim_Location_X": kill_event.victim.location.x / 1000,
                    "Victim_Location_Y": kill_event.victim.location.y / 1000,
                    "Victim_Location_Z": kill_event.victim.location.z / 1000,
                }
            )
    return kill_position


def Winner_Engage_Position(match: PUBG_match.Match):
    tel = match.get_telemetry()
    chicken_player = tel.winner()[0]  # 1등 플레이어 =chicken
    start = datetime.datetime.strptime(
        tel.filter_by("log_match_start")[0].timestamp, "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    engage_log = tel.filter_by("log_player_take_damage")
    engage_position = []  # 교전 중 동선
    victim_name = []
    for i in kill_position:
        victim_name.append(i.get("Victim"))
    for engage_event in engage_log:
        engage_timestamp = datetime.datetime.strptime(
            engage_event.timestamp, "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        engage_dt = (engage_timestamp - start).total_seconds()
        if engage_event.victim.name in victim_name:
            engage_position.append(
                {
                    "Attacker": chicken_player,
                    "Victim": engage_event.victim.name,
                    "Time": engage_dt,
                    "x": engage_event.attacker.location.x / 1000,
                    "y": engage_event.attacker.location.y / 1000,
                    "z": engage_event.attacker.location.z / 1000,
                    "Victim_Location_X": engage_event.victim.location.x / 1000,
                    "Victim_Location_Y": engage_event.victim.location.y / 1000,
                    "Victim_Location_Z": engage_event.victim.location.z / 1000,
                }
            )
    print(engage_position)
    return engage_position


def engage_circle(positions: list):
    for idx, pos in enumerate(positions):
        winner_x, winner_y, victim_x, victim_y = (
            pos["x"],
            pos["y"],
            pos["Victim_Location_X"],
            pos["Victim_Location_Y"],
        )
        x = (winner_x + victim_x) / 2
        y = (winner_y + victim_y) / 2
        center = (x, y)  # 교전시 적과 나 사이의 가운데
        radius = (
            math.dist([winner_x, winner_y], [victim_x, victim_y]) + 2
        )  # 이 반지름은 교전시 죽인 녀석과 거리 / 2 보다 조금 크면 될듯
        engage_circle = patches.Circle(center, radius, fill=False, ec="r")
        plt.gca().add_patch(engage_circle)
        victim_rect = patches.Rectangle((victim_x, victim_y), 0.5, 0.5, color="white")
        plt.gca().add_patch(victim_rect)


# pubg.match()

api_key = None
with open(".\\my_api", mode="r") as api_key_file:
    api_key = api_key_file.read()
    print(api_key)
pubg = PUBG(api_key=api_key, shard="steam")
match = pubg.match("c4b89079-795b-49ff-a134-c02b6aa73c77")

winner_kill_position = Winner_Kill_Position(match)
plot_map_img(match.map_name, "Low")
winner_movement = winner_position(match)
plot_positions(winner_movement)
engage_circle(winner_kill_position)
# Winner_Engage_Position(match)

# plot_positions(winner_engage_position)
plt.show()


# plt.show()

# logplayer damage의 timestamp 분포
# 교전 발생 구역을logplayerdamage의 postion으로 clustering


#'x': location.character.location.x / 1000, # 맵마다 다른건지 1000으로 해야되는게 있고 100으로 해야되는 게 잇나?
