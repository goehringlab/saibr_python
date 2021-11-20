import numpy as np
from skimage import io
import cv2


def load_image(filename):
    """
    Given the filename of a TIFF, creates numpy array with pixel intensities

    :param filename:
    :return:
    """

    # img = np.array(Image.open(filename), dtype=np.float64)
    # img[img == 0] = np.nan
    return io.imread(filename).astype(float)


def offset_coordinates(roi, offsets):
    """
    Reads in coordinates, adjusts according to offsets

    :param roi: two column array containing x and y coordinates. e.g. coors = np.loadtxt(filename)
    :param offsets: array the same length as coors. Direction?
    :return: array in same format as coors containing new coordinates

    To save this in a fiji readable format run:
    np.savetxt(filename, newcoors, fmt='%.4f', delimiter='\t')

    """

    # Calculate gradients
    xcoors = roi[:, 0]
    ycoors = roi[:, 1]
    ydiffs = np.diff(ycoors, prepend=ycoors[-1])
    xdiffs = np.diff(xcoors, prepend=xcoors[-1])
    grad = ydiffs / xdiffs
    tangent_grad = -1 / grad

    # Offset coordinates
    xchange = ((offsets ** 2) / (1 + tangent_grad ** 2)) ** 0.5
    ychange = xchange / abs(grad)
    newxs = xcoors + np.sign(ydiffs) * np.sign(offsets) * xchange
    newys = ycoors - np.sign(xdiffs) * np.sign(offsets) * ychange
    newcoors = np.swapaxes(np.vstack([newxs, newys]), 0, 1)
    return newcoors


def make_mask(shape, roi):
    return cv2.fillPoly(np.zeros(shape) * np.nan, [np.int32(roi)], 1)
