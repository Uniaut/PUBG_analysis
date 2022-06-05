import matplotlib.pyplot as plt
import numpy as np

import tests.mapsize as Mapsize

DEFAULT_SIGMA = 20.0


def sticker(xx, yy, pos: tuple, sigma: float):
    """
    add gaussian kernel sticker
    """
    var = sigma ** 2
    pos_x, pos_y = pos
    dist = (xx - pos_x) ** 2 + (yy - pos_y) ** 2
    sticker_map = np.exp(-dist / (2 * var))
    return sticker_map


def ready_heatmap(map_id: str, num_split: int, x_range: tuple[float] = (0, 1), y_range: tuple[float] = (0, 1)):
    x_size, y_size = Mapsize.mapsize(map_id)
    x_range = np.float32(x_range) * x_size
    y_range = np.float32(y_range) * y_size

    print(
        f'Cell size: {(x_range[1] - x_range[0]) / num_split}x{(y_range[1] - y_range[0]) / num_split}'
    )
    x = np.linspace(*x_range, num_split)
    y = np.linspace(*y_range, num_split)
    xx, yy = np.meshgrid(x, y, indexing='xy', sparse=True)
    return xx, yy


def new_grid(xx, yy):
    return xx, yy, (xx + yy) * 0


def add_sticker(hset, *, pos: tuple, sigma: float = DEFAULT_SIGMA, amp: float):
    xx, yy, z = hset
    z += sticker(xx, yy, pos, sigma) * amp


def plot_heatmap(hset):
    xx, yy, z = hset
    plt.pcolormesh(xx, yy, z, cmap='RdBu', alpha=0.5)
    plt.colorbar()
