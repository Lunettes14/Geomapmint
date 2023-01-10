import math
import os
from copy import deepcopy
import numpy as np
import rasterio
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import matplotlib.pyplot as plt


path = r'/home/aina/PycharmProjects/geomapmint/s2_21/ROIs2017_winter_s2_21_p'


def _read_dataset(size, path, begin):
    for j in range(0, 29 * int(math.sqrt(size)), 29):
        for i in range(begin, begin + int(math.sqrt(size))):
            if not os.path.exists(path + f'{i+j}.tif'):
                return False
    return True


def _is_compatible(size, path, begin):
    if _read_dataset(size, path, begin):
        for j in range(0, 29 * int(math.sqrt(size)), 29):
                for i in range(begin+1, begin + int(math.sqrt(size))):
                    if not _are_horizontal_neighbours(i+j-1, i+j):
                        return False
        for j in range(int(math.sqrt(size))-1):
            if not _are_vertical_neighbours(begin + 29*j, begin + 29*(j+1)):
                return False
        return True
    else:
        return False


def _are_vertical_neighbours(top, bottom):
    p1 = rasterio.open(path + f'{top}.tif').bounds[3]
    p2 = rasterio.open(path + f'{bottom}.tif').bounds[1]
    if p1 - p2 == 3840:
        return True
    else:
        return False

    
def _are_horizontal_neighbours(left, right):
    p1 = rasterio.open(path + f'{left}.tif').bounds[0]
    p2 = rasterio.open(path + f'{right}.tif').bounds[2]
    if p2 - p1 == 3840:
        return True
    else:
        return False

print(_is_compatible(169, path, 30))





