import numpy as np
import matplotlib.pyplot as plt

import tests.mapsize as Mapsize


STICKER_SIGMA = 20.0


def sticker(xx, yy, pos: tuple, sigma: float):
    """
    add gaussian kernel sticker
    """
    var = sigma ** 2
    pos_x, pos_y = pos
    dist = (xx - pos_x) ** 2 + (yy - pos_y) ** 2
    sticker_map = np.exp(-dist / (2 * var)) / (2 * np.pi * var)
    return sticker_map


def ready_heatmap(map_id: str, num_split: int):
    x_size, y_size = Mapsize.mapsize(map_id)
    x_range = (x_size * 0.4, x_size * 0.6)
    y_range = (y_size * 0.4, y_size * 0.6)
    x = np.linspace(*x_range, num_split)
    y = np.linspace(*y_range, num_split)
    print(f'Cell size: {x_size / num_split}x{x_size / num_split}')
    xx, yy = np.meshgrid(x, y, indexing='xy', sparse=True)
    return xx, yy


def new_grid(xx, yy):
    return xx, yy, (xx + yy) * 0


def add_sticker(xx, yy, z, *, pos: tuple, amp: float):
    z += sticker(xx, yy, pos, STICKER_SIGMA) * amp


def plot_heatmap(xx, yy, z):
    plt.pcolormesh(xx, yy, z, cmap='RdBu', alpha=0.5)
    plt.colorbar()
