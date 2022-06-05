import numpy as np
import os

import matplotlib.pyplot as plt
import PIL.Image as Image

import chicken_dinner.assets.maps as Maps

_4X4 = [819200, 819200]
_2X2 = [409600, 409600]
_3X3 = [614400, 614400]
_1X1 = [204800, 204800]
map_dimensions = {
    'Desert_Main': _4X4,
    'Baltic_Main': _4X4,
    'Erangel_Main': _4X4,
    'DihorOtok_Main': _3X3,
    'Taego_Main': _3X3,
    'Tiger_Main': _3X3,
    'Savage_Main': _2X2,
    'Range_Main': _1X1,
    'Summerland_Main': _1X1,
    'Haven_Main': _1X1,
    'Heaven_Main': _1X1,
}


def mapsize(map_name):
    map_name_list = list(map_dimensions.keys())

    map_x, map_y = 0, 0
    for i in range(len(map_name_list)):
        if map_name == map_name_list[i]:
            map_x = map_dimensions[map_name][0] // 100
            map_y = map_dimensions[map_name][1] // 100
            break
    return map_x, map_y

def plot_map(map_id: str = None, res_option: str = "Low"):
    for b, f in [('Heaven', 'Haven'), ('Tiger', 'Taego'), ('Baltic', 'Erangel')]:
        map_id = map_id.replace(b, f)
    map_path = os.path.join(Maps.MAP_ASSET_PATH, f"{map_id}_{res_option}_Res.png")
    img_np = np.array(Image.open(map_path).resize(mapsize(map_id), Image.NEAREST))
    size_x, size_y, _ = img_np.shape
    # plt.imshow(img_np)
    # plt.imshow(img_np, extent=(-1, size_x-1, size_y-1, -1))
    plt.imshow(img_np, extent=(0, size_x, size_y, 0))
