from typing import Literal
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mplc
import cv2


def sticker(xx, yy, pos: tuple, sigma: float):
    '''
    add gaussian kernel sticker
    '''
    var = sigma ** 2
    pos_x, pos_y = pos
    dist = (xx - pos_x) ** 2 + (yy - pos_y) ** 2
    sticker_map = np.exp(-dist / (2 * var)) / (2 * np.pi * var)
    return sticker_map


def ready_heatmap():
    value_map = np.zeros((1600, 1600))

    x = np.linspace(0, 10000, 400)
    y = np.linspace(0, 10000, 400)

    xx, yy = np.meshgrid(x, y, indexing='xy', sparse=True)
    z = xx * yy * 0

    return xx, yy, z


def add_sticker(xx, yy, z, *, pos: tuple, amp: float):
    z += sticker(xx, yy, pos, 200.0) * amp


def plot_heatmap(xx, yy, z):
    plt.pcolormesh(xx, yy, z, cmap='RdBu', alpha=0.5)
    plt.colorbar()