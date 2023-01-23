import math
import os
from copy import deepcopy
import numpy as np
import rasterio
import earthpy.plot as ep

path = r'/home/aina/PycharmProjects/geomapmint/s2_21/ROIs2017_winter_s2_21_p'
dim_two_pics_with_intersection = 3840
dim_bands = 13


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
    if q1 - q2 == dim_two_pics_with_intersection:
        return True
    else:
        return False


def are_horizontal_neighbours(left, right):
    p1 = rasterio.open(path + f'{left}.tif').bounds[0]
    p2 = rasterio.open(path + f'{right}.tif').bounds[2]
    if p2 - p1 == dim_two_pics_with_intersection:
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


def generate_base(size):
    dim_matrix_2d = 128 * int(math.sqrt(size) + 1)
    dim_3d = (dim_bands, dim_matrix_2d, dim_matrix_2d)
    return np.zeros(dim_3d)


def combine(size, path, begin):
    combined = generate_base(size)
    for j in range(int(math.sqrt(size))):
        for i in range(int(math.sqrt(size))):
            pic_number_str = f'{begin + j + 29 * i}.tif'
            if os.path.exists(path + pic_number_str):
                with rasterio.open(path + pic_number_str) as src:
                    src_r = src.read()
                    if i + j == 0:
                        combined[:, 0:256, 0:256] = deepcopy(src_r[:, 0:256, 0:256])
                    elif j == 0:
                        combined[:, 256 + 128 * (i - 1): 256 + 128 * i, 0:256] = deepcopy(
                            src_r[:, 128:256, 0:256])  # Нижняя полоса
                    elif i == 0:
                        combined[:, 0:256, 256 + 128 * (j - 1): 256 + 128 * j] = deepcopy(
                            src_r[:, 0:256, 128:256])  # Правая полоса
                    else:
                        combined[:, 256 + 128 * (i - 1): 256 + 128 * i, 256 + 128 * (j - 1): 256 + 128 * j] = deepcopy(
                            src_r[:, 128:256, 128:256])
    return combined


s2 = combine(841, path, 30)
ep.plot_rgb(s2, rgb=[3, 2, 1])
