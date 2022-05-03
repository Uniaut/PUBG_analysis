from math import sin, cos
import cycler
from io import BytesIO
from turtle import position
import matplotlib as mpl
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image
import os.path
import urllib.request as req

import gzip
import json
import os
from chicken_dinner.pubgapi import PUBG
import datetime


def plot_map_img(map_name=None, res_option='Low'):
    url = f'https://github.com/pubg/api-assets/raw/master/Assets/Maps/{map_name}_Main_{res_option}_Res.png'
    img_np = np.array(PIL.Image.open(req.urlopen(url)))
    img_plot = plt.imshow(img_np)


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

    return '#%02x%02x%02x' % value

def plot_positions(positions:list):
    if False:
        for idx, pos in enumerate(positions):
            plt.plot(pos['x'], pos['y'], color=spectrum(idx / len(positions)), marker='o')
    else:
        axis_key_pos = {
            axis: [pos[axis] for pos in positions] for axis in ['x', 'y']
        }
        plt.plot(*axis_key_pos.values())


def test_positions(step: int):
    return [
        {
            'x': sin(i * 5 / step) * 200 + 400,
            'y': cos(i * 5 / step) * 200 + 400,
            'z': sin(i * 5 / step) * 200 + 400,
        } for i in range(step)
    ]


def winner_position(tmatch):
    match=pubg.match(tmatch)
    print(match.map_id)
    tel=match.get_telemetry()
    chicken=tel.winner()[0] #1등 플레이어 =chicken
    locations=tel.filter_by("log_player_position") #텔레메트리: 포지션으로 필터
    locations = [location for location in locations if location.elapsed_time > 0] 
    #게임 시작 후 경과시간 0 이상인 것들만 찾기// 찾아보니까 본 게임 시작하기 전에 다같이 모여 있는 광장이 있던데 여기서 움직이는 걸 제외한 것이라고 보여요

    player_positions=[] #1등 경로 
    start = datetime.datetime.strptime(tel.filter_by("log_match_start")[0].timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    #시작 시간 설정
    for location in locations:
        timestamp = datetime.datetime.strptime(location.timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
        dt = (timestamp - start).total_seconds()
        player = location.character.name#log_player_position에 기록된 플레이어의 이름 
        if player==chicken :#1등만 추출
            player_positions.append(
                {
                    'player': player, 
                    'timestamp': dt, 
                    'x': location.character.location.x / 1000,
                    'y': location.character.location.y / 1000,
                    'z': location.character.location.z / 1000,
                }
            )#1등 이름, 경과시간, x,y,z 

    return player_positions


if __name__ == '__main__':
    api_key = None
    with open('./my_api', mode='r') as api_key_file:
        api_key = api_key_file.read()
        print(api_key)
    
    pubg = PUBG(api_key=api_key, shard="steam")
    matches_list = pubg.samples(start=None, shard='steam').data['relationships']['matches']['data']
    match_id_list = [d['id']for d in matches_list]

    match_wanted=match_id_list[0]
    sample_position = winner_position(match_wanted)
    print(sample_position)

    plot_map_img('Taego', 'Low')
    plot_positions(sample_position)
    plt.show()
