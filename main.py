import math
import os
from copy import deepcopy
import numpy as np
import rasterio
import earthpy.plot as ep

PATH = r'/home/iakhmetev/datasets/SEN12MS/ROIs2017_winter_s2/s2_21/ROIs2017_winter_s2_21_p'
S2_BANDS = 13
S2_LEN = 256
S2_LEN_HALF = int(S2_LEN / 2)
S2_SCALE = 10
S2_LEN_INTERSECTION = int((S2_LEN + S2_LEN_HALF) * S2_SCALE)


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
                if not are_horizontal_neighbours(i + j - 1, i + j, path):
                    return False
        for j in range(int(math.sqrt(size)) - 1):
            if not are_vertical_neighbours(begin + 29 * j, begin + 29 * (j + 1), path):
                return False
        return True
    else:
        return False


def are_vertical_neighbours(top, bottom, path):
    with rasterio.open(path + f'{top}.tif') as src:
        q1 = src.bounds[3]
    with rasterio.open(path + f'{bottom}.tif') as src:
        q2 = src.bounds[1]
    if q1 - q2 == S2_LEN_INTERSECTION:
        return True
    else:
        return False


def are_horizontal_neighbours(left, right, path):
    p1 = rasterio.open(path + f'{left}.tif').bounds[0]
    p2 = rasterio.open(path + f'{right}.tif').bounds[2]
    if p2 - p1 == S2_LEN_INTERSECTION:
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
    dim_matrix_2d = S2_LEN_HALF * int(math.sqrt(size) + 1)
    dim_3d = (S2_BANDS, dim_matrix_2d, dim_matrix_2d)
    return np.zeros(dim_3d)


def cut_piece(i, j, src_r, combined):
    match i, j:
        case 0, 0:
            combined[:, 0:S2_LEN, 0:S2_LEN] = deepcopy(src_r[:, 0:S2_LEN, 0:S2_LEN])
        case 0, j:
            combined[:, 0:S2_LEN, S2_LEN + S2_LEN_HALF * (j - 1): S2_LEN + S2_LEN_HALF * j] = deepcopy(src_r[:, 0:S2_LEN, S2_LEN_HALF:S2_LEN])
        case i, 0:
            combined[:, S2_LEN + S2_LEN_HALF * (i - 1): S2_LEN + S2_LEN_HALF * i, 0:S2_LEN] = deepcopy(src_r[:, S2_LEN_HALF:S2_LEN, 0:S2_LEN])
        case i, j:
            combined[:, S2_LEN + S2_LEN_HALF * (i - 1): S2_LEN + S2_LEN_HALF * i, S2_LEN + S2_LEN_HALF * (j - 1): S2_LEN + S2_LEN_HALF * j] = deepcopy(
                src_r[:, S2_LEN_HALF:S2_LEN, S2_LEN_HALF:S2_LEN])
    return combined


def combine(size, path, begin):
    combined = generate_base(size)
    for j in range(int(math.sqrt(size))):
        for i in range(int(math.sqrt(size))):
            pic_number_str = f'{begin + j + 29 * i}.tif'
            if os.path.exists(path + pic_number_str):
                with rasterio.open(path + pic_number_str) as src:
                    src_r = src.read()
                    combined = cut_piece(i, j, src_r, combined)
    return combined


s2 = combine(841, PATH, 30)
ep.plot_rgb(s2, rgb=[3, 2, 1])
