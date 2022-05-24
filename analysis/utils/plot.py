import numpy as np
import os

import matplotlib.pyplot as plt
import PIL.Image
import urllib.request as req

import chicken_dinner.assets.maps as Maps


def plot_map(map_name: str = None, res_option: str = "Low"):
    map_path = os.path.join(Maps.MAP_ASSET_PATH, f"{map_name}_{res_option}_Res.png")
    img_np = np.array(PIL.Image.open(map_path))
    size_x, size_y, _ = img_np.shape
    # plt.imshow(img_np)
    plt.imshow(img_np, extent=(-1, size_x-1, size_y-1, -1))
    plt.imshow(img_np, extent=(0, size_x, size_y, 0))
