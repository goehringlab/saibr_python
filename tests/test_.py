from saibr import *
import glob
import numpy as np
import os
import pytest

# Load images and ROIs
cal_basepath = os.path.dirname(os.path.abspath(__file__)) + '/../data/dataset1/n2'
cal_image_paths = sorted(glob.glob(cal_basepath + '/*.tif'))
cal_roi_paths = sorted(glob.glob(cal_basepath + '/*.txt'))
cal_images = [load_image(p) for p in cal_image_paths]
cal_rois = [np.loadtxt(p) for p in cal_roi_paths]

# Extract channels
cal_images_gfp = [i[:, :, 0] for i in cal_images]
cal_images_af = [i[:, :, 1] for i in cal_images]


def test_1():
    # Testing that Calibration runs to completion
    sc = SaibrCalibrate(gfp=cal_images_gfp, af=cal_images_af, roi=cal_rois, sigma=2)
    sc.run()

def test_2():
    # Testing that Calibration gives correct answer
    sc = SaibrCalibrate(gfp=cal_images_gfp, af=cal_images_af, roi=cal_rois, sigma=2)
    sc.run()
    assert sc.params[0] == pytest.approx(0.9506699286602773)
    assert sc.params[1] == pytest.approx(-457.7097277898565)

def test_3():
    # Testing that Correction gives correct answer
    img = saibr_correct(cal_images_gfp[0], cal_images_af[0], 0.9506699286602773, -457.7097277898565)
    assert img[0, 0] == pytest.approx(422.5635553021118)

