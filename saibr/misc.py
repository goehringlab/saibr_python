import numpy as np
from skimage import io
from typing import Optional
import glob
import matplotlib.pyplot as plt
import copy


def load_image(filename: str) -> np.ndarray:
    """
    Given the filename of a TIFF, creates numpy array with pixel intensities

    Args:
        filename: full path to the file to import (including extension)

    Returns:
        A numpy array of the image

    """

    return io.imread(filename).astype(float)


def save_img(img: np.ndarray, direc: str):
    """
    Saves 2D array as .tif file

    Args:
        img: numpy array of the image to save
        direc: file path to save to (including '.tif' extension)

    """

    io.imsave(direc, img.astype('float32'))


def save_img_jpeg(img: np.ndarray, direc: str, cmin: Optional[float] = None, cmax: Optional[float] = None,
                  cmap: str = 'gray'):
    """
    Saves 2D array as jpeg, according to min and max pixel intensities

    Args:
        img: numpy array of the image to save
        direc: file path to save to (including '.jpeg' extension)
        cmin: optional, sets intensity scaling (along with cmax)
        cmax: optional, sets intensity scaling (along with cmin)
        cmap: colour map (use string corresponding to matplotlib colormap)

    """

    plt.imsave(direc, img, vmin=cmin, vmax=cmax, cmap=cmap)


def _direcslist(dest: str, levels: int = 0, exclude: Optional[tuple] = ('!',),
                exclusive: Optional[tuple] = None) -> list:
    lis = sorted(glob.glob(f'{dest}/*/'))

    for level in range(levels):
        newlis = []
        for e in lis:
            newlis.extend(sorted(glob.glob(f'{e}/*/')))
        lis = newlis
        lis = [x[:-1] for x in lis]

    # Excluded directories
    lis_copy = copy.deepcopy(lis)
    if exclude is not None:
        for x in lis:
            for i in exclude:
                if i in x:
                    lis_copy.remove(x)
                    break

    # Exclusive directories
    if exclusive is not None:
        lis2 = []
        for x in lis_copy:
            for i in exclusive:
                if i in x:
                    lis2.append(x)
    else:
        lis2 = lis_copy

    return sorted(lis2)


def direcslist(dest: str, levels: int = 0, exclude: Optional[tuple] = ('!',),
               exclusive: Optional[tuple] = None) -> list:
    """
    Gives a list of directories within a given directory (full path)
    Todo: os.walk

    Args:
        dest: path of parent directory
        levels: number of levels to go down. E.g. if 0, only return folders within the parent folder; if 1, return
        folders within folders within the parent folder
        exclude: exclude directories containing any strings within this tuple
        exclusive: exclude directories that don't contain all the strings within this tuple

    Returns:
        list of directories

    """

    if type(dest) is list:
        out = []
        for d in dest:
            out.extend(_direcslist(d, levels, exclude, exclusive))
        return out
    else:
        return _direcslist(dest, levels, exclude, exclusive)
