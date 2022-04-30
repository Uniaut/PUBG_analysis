from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import PIL.Image
import os.path
import urllib.request as req

def plot_map_img(map_name=None, res_option='Low'):
    url = f'https://github.com/pubg/api-assets/raw/master/Assets/Maps/{map_name}_Main_{res_option}_Res.png'
    img_np = np.array(PIL.Image.open(req.urlopen(url)))
    img_plot = plt.imshow(img_np)
    return img_plot

if __name__ == '__main__':
    plot_map_img('Taego')
    plt.show()