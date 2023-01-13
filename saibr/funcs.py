import numpy as np
from skimage import io
import cv2


def load_image(filename: str) -> np.ndarray:
    """
    Given the filename of a TIFF, creates numpy array with pixel intensities

    Args:
        filename: full path to the file to import (including extension)

    Returns:
        A numpy array of the image

    """

    return io.imread(filename).astype(float)


def make_mask(shape: tuple, roi: np.ndarray) -> np.ndarray:
    return cv2.fillPoly(np.zeros(shape) * np.nan, [np.int32(roi)], 1)
