from saibr import *
import glob
import numpy as np
import pytest

# Load images and ROIs
cal_basepath = '../data/dataset1/n2'
cal_image_paths = glob.glob(cal_basepath + '/*.tif')
cal_roi_paths = glob.glob(cal_basepath + '/*.txt')
cal_images = [load_image(p) for p in cal_image_paths]
cal_rois = [np.loadtxt(p) for p in cal_roi_paths]
print(len(cal_rois))

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
    assert sc.params[0] == pytest.approx(0.9497859698053084)
    assert sc.params[1] == pytest.approx(-458.79346328784277)

def test_3():
    # Testing that Correction gives correct answer
    img = saibr_correct(cal_images_gfp[0], cal_images_af[0], 0.9497859698053084, -458.79346328784277)
    assert img[0, 0] == pytest.approx(225.81832595690582)

