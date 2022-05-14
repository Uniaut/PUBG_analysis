import numpy as np

import matplotlib.pyplot as plt
import PIL.Image
import urllib.request as req


def plot_map(map_name=None, res_option='Low'):
    url = f'https://github.com/pubg/api-assets/raw/master/Assets/Maps/{map_name}_Main_{res_option}_Res.png'
    img_np = np.array(PIL.Image.open(req.urlopen(url)))
    plt.imshow(img_np)