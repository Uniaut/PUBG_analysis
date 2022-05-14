import gzip
import json
from optparse import Values
import os
from re import A, X
from tkinter import Y

import matplotlib
import chicken_dinner
from chicken_dinner.pubgapi import PUBG
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from math import sin, cos
import PIL.Image
import os.path
import urllib.request as req
import random
import matplotlib.patches as patches  # 원 추가
import math
from matplotlib.animation import FuncAnimation


# 교전시작시각 리스트(int형으로해서 중복제거 & 15초내 범위에 있는 교전 cluster)
def get_damage_start_time(playername):
    file_path = "player_damages/player_damages.json"
    with open(file_path, "r") as f:
        player_damages_json = json.load(f)

    # json파일에 있는 교전 시간 int형으로 변환해서 중복은 제거
    damage_start_time = []
    damage_start_time_dedup = []  # 중복 제거
    damage_start_time_new = []  # 최종 교전시작시간 리스트
    for t in player_damages_json[playername]:  # 유저의 교전 시간을 int형으로 리스트
        damage_start_time.append(int(t[0]))

    # 중복 제거 과정
    for v in damage_start_time:
        if v not in damage_start_time_dedup:
            damage_start_time_dedup.append(v)

    # 15초 내 범위에 있는 교전은 하나로 취급
    k = 0
    while k < len(damage_start_time_dedup) - 1:

        if damage_start_time_dedup[k + 1] - damage_start_time_dedup[k] >= 15:
            damage_start_time_new.append(damage_start_time_dedup[k + 1])
        k += 1

    damage_start_time_new.insert(0, damage_start_time_dedup[0])

    return damage_start_time_new


api_key = None
with open(".\\my_api", mode="r") as api_key_file:
    api_key = api_key_file.read()
    # print(api_key)
pubg = PUBG(api_key=api_key, shard="steam")
match = pubg.match("0b09c0b4-8815-49bb-8603-cac5c82b7d99")

match_model = chicken_dinner.models.match.Match(
    pubg, "0b09c0b4-8815-49bb-8603-cac5c82b7d99"
)  # 매치 디테일모델
match_get_telemetry = match_model.get_telemetry(map_assets=False)  # telemetry object


# player_damages json 파일 생성
file_path = "player_damages/player_damages.json"
player_damages = match_get_telemetry.player_damages(include_pregame=False)
with open(file_path, "w") as f:
    json.dump(player_damages, f, ensure_ascii=False, indent=4)


# 플레이어 목록 리스트
player_list = []
player_damages_json = match_get_telemetry.player_damages(include_pregame=False)
for player_name in player_damages_json.keys():
    player_list.append(player_name)


# 각 플레이어들의 교전시간갯수에 맞게 플레이어 index를 할당(scatter x축 = y축 갯수 맞추기 위함)
players_index = []
for i in player_list:
    line = []  # 열을 담을 빈 리스트
    for j in get_damage_start_time(i):
        line.append(player_list.index(i) + 1)
    players_index.append(line)


# 각 플레이어별 교전 시작 시간 출력
for i in player_list:
    print(i, ":", get_damage_start_time(i))


# 전체 플레이어들 산점도 출력
k = 0
while k < len(player_list):
    plt.scatter(get_damage_start_time(player_list[k]), players_index[k])
    k += 1
plt.show()
