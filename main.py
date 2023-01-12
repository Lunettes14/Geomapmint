import math
import os
from copy import deepcopy
import numpy as np
import pylab as p
import rasterio
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import matplotlib.pyplot as plt
from rasterio.plot import show

path = r'/home/aina/PycharmProjects/geomapmint/s2_21/ROIs2017_winter_s2_21_p'


def read_dataset(size, path, begin):
    for j in range(0, 29 * int(math.sqrt(size)), 29):
        for i in range(begin, begin + int(math.sqrt(size))):
            if not os.path.exists(path + f'{i + j}.tif'):
                return False
    return True


def is_compatible(size, path, begin):
    if read_dataset(size, path, begin):
        for j in range(0, 29 * int(math.sqrt(size)), 29):
            for i in range(begin + 1, begin + int(math.sqrt(size))):
                if not are_horizontal_neighbours(i + j - 1, i + j):
                    return False
        for j in range(int(math.sqrt(size)) - 1):
            if not are_vertical_neighbours(begin + 29 * j, begin + 29 * (j + 1)):
                return False
        return True
    else:
        return False


def are_vertical_neighbours(top, bottom):
    with rasterio.open(path + f'{top}.tif') as src:
        q1 = src.bounds[3]
    with rasterio.open(path + f'{bottom}.tif') as src:
        q2 = src.bounds[1]
    if q1 - q2 == 3840:
        return True
    else:
        return False


def are_horizontal_neighbours(left, right):
    p1 = rasterio.open(path + f'{left}.tif').bounds[0]
    p2 = rasterio.open(path + f'{right}.tif').bounds[2]
    if p2 - p1 == 3840:
        return True
    else:
        return False


def where_missing(size, path, begin):
    p = []
    for j in range(int(math.sqrt(size))):
        for i in range(int(math.sqrt(size))):
            if not os.path.exists(path + f'{begin + i + 29 * j}.tif'):
                p.append((j, i))
    return p


def combine(size, path, begin):
    dim = (13, 128 * int(math.sqrt(size) + 1), 128 * int(math.sqrt(size) + 1))
    combined = np.zeros(dim)
    for j in range(int(math.sqrt(size))):
        for i in range(int(math.sqrt(size))):
            if os.path.exists(path + f'{begin + j + 29 * i}.tif'):
                if i + j == 0:
                    with rasterio.open(path + f'{begin + j + 29 * i}.tif') as src:
                        p00 = src.read()
                        combined[:, 0:256, 0:256] = deepcopy(p00[:, 0:256, 0:256])
                elif j == 0:
                    with rasterio.open(path + f'{begin + j + 29 * i}.tif') as src:
                        p0n = src.read()
                        combined[:, 256 + 128 * (i - 1): 256 + 128 * i, 0:256] = deepcopy(
                            p0n[:, 128:256, 0:256])  # Нижняя полоса
                elif i == 0:
                    with rasterio.open(path + f'{begin + j + 29 * i}.tif') as src:
                        pn0 = src.read()
                        combined[:, 0:256, 256 + 128 * (j - 1): 256 + 128 * j] = deepcopy(
                            pn0[:, 0:256, 128:256])  # Правая полоса
                else:
                    with rasterio.open(path + f'{begin + j + 29 * i}.tif') as src:
                        pnn = src.read()
                        combined[:, 256 + 128 * (i - 1): 256 + 128 * i, 256 + 128 * (j - 1): 256 + 128 * j] = deepcopy(
                            pnn[:, 128:256, 128:256])
    return combined


s2 = combine(841, path, 30)
ep.plot_rgb(s2, rgb=[3, 2, 1])
print('push please')
