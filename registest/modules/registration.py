# -*- coding: utf-8 -*-

from skimage.registration import phase_cross_correlation


def phase_cross_correlation_wrapper(ref_3d, target_3d):
    shift, _, _ = phase_cross_correlation(ref_3d, target_3d, upsample_factor=100)
    return shift
