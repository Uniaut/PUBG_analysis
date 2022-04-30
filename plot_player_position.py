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
    '''
    axis_key_pos = {
        axis: [pos[axis] for pos in positions] for axis in ['x', 'y']
    }
    plt.plot(*axis_key_pos.values(), 'ro')
    '''
    for idx, pos in enumerate(positions):
        plt.plot(pos['x'], pos['y'], color=spectrum(idx / len(positions)), marker='o')


def test_positions(step: int):
    return [
        {
            'x': sin(i * 5 / step) * 200 + 400,
            'y': cos(i * 5 / step) * 200 + 400,
            'z': sin(i * 5 / step) * 200 + 400,
        } for i in range(step)
    ]

if __name__ == '__main__':
    # plot_map_img('Erangel', 'Low')
    plot_positions(test_positions(100))
    plt.show()