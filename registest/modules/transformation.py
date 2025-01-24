#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from typing import Any, List

import numpy as np
from scipy.ndimage import shift

from registest._version import __version__
from registest.core.data_manager import OutImg, ReferenceImg
from registest.core.run_args import parse_run_args
from registest.utils.io_utils import save_json


def shift_3d_array_subpixel(array_3d, shift_values, filling_val=0.0):
    """
    Shifts a 3D numpy array along the X and Y axes with subpixel accuracy.

    Parameters:
    array_3d (numpy.ndarray): The 3D array to shift.
    shift_values (list): A list of two floats representing the shift values for the X and Y axes.

    Returns:
    numpy.ndarray: The shifted 3D array.
    """
    if not isinstance(array_3d, np.ndarray) or len(array_3d.shape) != 3:
        raise ValueError("Input must be a 3D numpy array.")
    if not isinstance(shift_values, list) or len(shift_values) != 3:
        raise ValueError("Shift values must be a list of three floats (z,x,y).")

    shift_vector = [shift_values[0], shift_values[1], shift_values[2]]
    shifted_array = shift(array_3d, shift_vector, mode="constant", cval=filling_val)

    return shifted_array


class Transform:
    def __init__(self, method="scipy", xyz_shifts=None, filling_value="0.0"):
        self.method: str = method
        self.xyz_shifts: List[float] = self.cast_shifts(xyz_shifts)
        self.filling_value: Any = self.cast_filling_value(filling_value)

    def cast_shifts(self, shifts: List[float]):
        if shifts is None:
            raise ValueError
        if len(shifts) != 3:
            raise ValueError
        return [float(i) for i in shifts]

    def cast_filling_value(self, value):
        if value.lower() == "nan":
            return np.nan
        else:
            return float(value)

    def execute(self, img):
        if self.method == "scipy":
            return shift_3d_array_subpixel(
                img, self.xyz_shifts, filling_val=self.filling_value
            )
        else:
            raise NotImplementedError(
                f"The method '{self.method}' is not implemented. Please use a supported method such as 'scipy'."
            )

    def save_shifts_used(self, prepa_path):
        out = {f"target_{i}.tif": self.shifts[i] for i in range(len(self.shifts))}
        path = os.path.join(prepa_path, "image_names_with_shifts.json")
        save_json(out, path)

    def generate_metadata(key_path: str, ref_path):
        # TODO
        pass


def _main():
    run_args = parse_run_args()
    ref_img = ReferenceImg(run_args.reference)
    out_img = OutImg(run_args.target)
    xyz_shifts = [run_args.x, run_args.y, run_args.z]
    transformation = Transform(xyz_shifts=xyz_shifts)
    transformed_img = transformation.execute(ref_img.data)
    out_img.save(transformed_img)
    transformation.generate_metadata(out_img.path, ref_path=ref_img.path)


def main():
    begin_time = datetime.now()
    print(f"[VERSION] RegisTest {__version__}")
    _main()
    print("\n==================== Normal termination ====================\n")
    print(f"Elapsed time: {datetime.now() - begin_time}")


if __name__ == "__main__":
    main()
