from typing import Any, List

import numpy as np
from scipy.ndimage import shift


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
    def __init__(self, prepare_params: dict):
        self.method: str = prepare_params["method"]
        self.shifts: List[List[float]] = prepare_params["shifts"]
        self.filling_value: Any = self.cast_filling_value(
            prepare_params["filling_value"]
        )

    def cast_filling_value(self, value):
        if value == "nan" or value == "NaN":
            return np.nan
        else:
            return float(value)

    def execute(self, img, shift_index):
        if self.method == "scipy":
            return shift_3d_array_subpixel(
                img, self.shifts[shift_index], filling_val=self.filling_value
            )
        else:
            raise NotImplementedError(
                f"The method '{self.method}' is not implemented. Please use a supported method such as 'scipy'."
            )
