import numpy as np
from skimage import io
import cv2
from scipy.interpolate import splprep, splev, interp1d


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


def spline_roi(roi, periodic=True, s=0):
    """
    Fits a spline to points specifying the coordinates of the cortex, then interpolates to pixel distances

    :param roi:
    :return:
    """

    # Append the starting x,y coordinates
    if periodic:
        x = np.r_[roi[:, 0], roi[0, 0]]
        y = np.r_[roi[:, 1], roi[0, 1]]
    else:
        x = roi[:, 0]
        y = roi[:, 1]

    # Fit spline
    tck, u = splprep([x, y], s=s, per=periodic)

    # Evaluate spline
    xi, yi = splev(np.linspace(0, 1, 10000), tck)

    # Interpolate
    return interp_roi(np.vstack((xi, yi)).T, periodic=periodic)


def interp_roi(roi, periodic=True):
    """
    Interpolates coordinates to one pixel distances (or as close as possible to one pixel)
    Linear interpolation

    :param roi:
    :return:
    """

    if periodic:
        c = np.append(roi, [roi[0, :]], axis=0)
    else:
        c = roi

    # Calculate distance between points in pixel units
    distances = ((np.diff(c[:, 0]) ** 2) + (np.diff(c[:, 1]) ** 2)) ** 0.5
    distances_cumsum = np.r_[0, np.cumsum(distances)]
    total_length = sum(distances)

    # Interpolate
    fx, fy = interp1d(distances_cumsum, c[:, 0], kind='linear'), interp1d(distances_cumsum, c[:, 1], kind='linear')
    positions = np.linspace(0, total_length, int(round(total_length)))
    xcoors, ycoors = fx(positions), fy(positions)
    newpoints = np.c_[xcoors[:-1], ycoors[:-1]]
    return newpoints
