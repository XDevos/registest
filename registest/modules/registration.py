# -*- coding: utf-8 -*-

from skimage.registration import phase_cross_correlation

from registest.core.run_args import parse_run_args
from registest.utils.metrics import timing_main


def phase_cross_correlation_wrapper(ref_3d, target_3d):
    shift, _, _ = phase_cross_correlation(ref_3d, target_3d, upsample_factor=100)
    return shift


@timing_main
def main():
    _ = parse_run_args()


if __name__ == "__main__":
    main()
