map_dimensions = {
    'Desert_Main': [819200, 819200],
    'Baltic_Main': [819200, 819200],
    'Savage_Main': [409600, 409600],
    'DihorOtok_Main': [614400, 614400],
    'Range_Main': [204800, 204800],
    'Baltic_Main': [819200, 819200],
    'Summerland_Main': [204800, 204800],
}


def mapsize(map_name):
    map_name_list = list(map_dimensions.keys())

    map_x, map_y = 0, 0
    for i in range(len(map_name_list)):
        if map_name == map_name_list[i]:
            map_x = map_dimensions[map_name][0] / 100
            map_y = map_dimensions[map_name][1] / 100
            break
    return map_x, map_y
