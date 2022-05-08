import gzip
import json
import os
import datetime
import numpy as np
from math import sin, cos
import PIL.Image
import os.path

import matplotlib.pyplot as plt
import matplotlib.patches as patches # 원 추가
import math
from matplotlib.animation import FuncAnimation
import pandas as pd
import urllib.request as req

from chicken_dinner.pubgapi import PUBG
#import chicken_dinner.types as PUBGType

def plot_map_img(map_name=None, res_option='Low'):
    url = f'https://github.com/pubg/api-assets/raw/master/Assets/Maps/{map_name}_Main_{res_option}_Res.png'
    img_np = np.array(PIL.Image.open(req.urlopen(url)))
    plt.imshow(img_np)

def Winner_Kill_Position(match):
    tel=match.get_telemetry()
    chicken_player=tel.winner()[0] #1등 플레이어 =chicken
    start = datetime.datetime.strptime(tel.filter_by("log_match_start")[0].timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    kill_log=tel.filter_by("log_player_kill_v2")
    global kill_position
    kill_position=[]

    for kill_event in kill_log:
        timestamp = datetime.datetime.strptime(kill_event.timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
        dt = (timestamp - start).total_seconds()
        
        try:
            player = kill_event.finisher.name
        except AttributeError:
            continue

        if player==chicken_player and player==kill_event.killer.name:
            kill_position.append( {
                'Killer' : player,
                'Victim' : kill_event.victim.name,
                'Time' : dt,
                'x' : kill_event.finisher.location.x/1000,
                'y' : kill_event.finisher.location.y/1000,
                'z' : kill_event.finisher.location.z/1000,
                'Victim_Location_X' : kill_event.victim.location.x/1000,
                'Victim_Location_Y' : kill_event.victim.location.y/1000,
                'Victim_Location_Z' : kill_event.victim.location.z/1000,} )

    return kill_position
 
def Winner_Engage_Position(match, input_kill_position):
    tel=match.get_telemetry()
    chicken_player=tel.winner()[0] #1등 플레이어 =chicken
    start = datetime.datetime.strptime(tel.filter_by("log_match_start")[0].timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    engage_log=tel.filter_by("log_player_take_damage")
    engage_position = {} #교전 중 동선
    victim_name = []
    for i in input_kill_position:
        victim_name.append(i.get('Victim'))
    for i in range(len(victim_name)):
        engage_position[victim_name[i]]=[]
    for engage_event in engage_log:
        try:
            attacker_name = engage_event.attacker.name
        except AttributeError:
            continue    
        if engage_event.victim.name in victim_name and attacker_name == chicken_player:
                # victim_num = engage_position.index(engage_event.victim.name)
                # temp_name=engage_event.victim.name
                # engage_position[].append(1)
                engage_timestamp = datetime.datetime.strptime(engage_event.timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
                engage_dt = (engage_timestamp - start).total_seconds() 
                engage_position[engage_event.victim.name].append({
                        'Victim': engage_event.victim.name,
                        'Attacker' : chicken_player,
                        'Victim' : engage_event.victim.name,
                        'Time' : engage_dt,
                        'x' : engage_event.attacker.location.x/1000,
                        'y' : engage_event.attacker.location.y/1000,
                        'z' : engage_event.attacker.location.z/1000,
                        'Victim_Location_X' : engage_event.victim.location.x/1000,
                        'Victim_Location_Y' : engage_event.victim.location.y/1000,
                        'Victim_Location_Z' : engage_event.victim.location.z/1000,
                    } )
    return engage_position

def winner_victim_engage_circumstance(engage_dictionary,positions:list):
    number_of_victims=len(engage_dictionary)
    list_victims=list(engage_dictionary.keys())
    for i in range(number_of_victims):
        engage_circle_radius=0
        center=()
        for engage_event in engage_dictionary[list_victims[i]]:
            winner_x, winner_y, victim_x, victim_y = engage_event['x'], engage_event['y'], engage_event['Victim_Location_X'], engage_event['Victim_Location_Y']
            plt.scatter(winner_x, winner_y, color = 'b')
            plt.scatter(victim_x, victim_y, color=[1,(1/number_of_victims)*i,0.4])
            plt.arrow(winner_x, winner_y, victim_x-winner_x, victim_y-winner_y,color='white')
            if engage_circle_radius < math.dist([winner_x,winner_y], [victim_x,victim_y])+0.1:
                engage_circle_radius = math.dist([winner_x,winner_y], [victim_x,victim_y])+0.1
                x= (winner_x+ victim_x)/2
                y= (winner_y+ victim_y)/2
                center=(x,y)
        killer_position_x, killer_position_y = positions[i]['x'], positions[i]['y']
        victim_killed_position_x, victim_killed_position_y = positions[i]['Victim_Location_X'], positions[i]['Victim_Location_Y']
        dist=math.dist([killer_position_x, killer_position_y], [victim_killed_position_x, victim_killed_position_y])+0.1
        if engage_circle_radius < dist:
            engage_circle_radius = dist
            x= (winner_x+ victim_x)/2
            y= (winner_y+ victim_y)/2
            center=(x,y)        
        plt.scatter(victim_killed_position_x, victim_killed_position_y, color=[1,(1/number_of_victims)*i,0.4],marker='x')    
        engage_circle=patches.Circle(center,engage_circle_radius,fill=False,ec='r')
        plt.gca().add_patch(engage_circle)


if __name__ == '__main__':
    api_key = None
    with open('.\\my_api', mode='r') as api_key_file:
        api_key = api_key_file.read()

    pubg = PUBG(api_key=api_key, shard="steam")
    match = pubg.match('c4b89079-795b-49ff-a134-c02b6aa73c77')
    winner_engage_position=Winner_Engage_Position(match,Winner_Kill_Position(match))
    winner_victim_engage_circumstance(winner_engage_position,Winner_Kill_Position(match))
    plot_map_img(match.map_name, 'Low')

    plt.show()

#잘죽는 위치, 잘 죽이는 위치 찾기. 시각화
