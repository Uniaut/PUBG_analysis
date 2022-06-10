import json
from collections import OrderedDict

def make_json(data):
    file_data = OrderedDict()
    
    file_data["land_x"] = float(data[3][0]) 
    file_data["land_y"] = float(data[3][1])
    file_data["end_x"] = float(data[4][0])
    file_data["end_y"] = float(data[4][1])
    file_data["circle_x"] = float(data[5][0])
    file_data["circle_y"] = float(data[5][1])
    file_data["winner_player_position"] = []
    for i in range(len(data[6])):
        file_data["winner_player_position"].append({
            "position_x" : float(data[6][i]),
            "position_y" : float(data[6][i])
        })
    file_data["match_id"] = str(data[7])
    match_id = str(data[7])
    map_name = str(data[8])

    print(json.dumps(file_data,ensure_ascii = False, indent = "\t"))

    filename = match_id + map_name
    with open(f'{filename}.json', 'w', encoding = "utf-8") as make_file:
        json.dump(file_data, make_file, ensure_ascii = False, indent = "\t")

