import os

import numpy as np
from scipy.ndimage import shift

from registest.utils.io_utils import save_tiff


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
    def __init__(self, params, out_folder):
        self.out_folder = out_folder
        self.params = params
        self.out_filenames = []

    def load_inputs(self):
        inputs = []
        for p_dict in self.params:
            inputs.append(p_dict["shift_value"])
            self.out_filenames.append(p_dict["filename"])
        return inputs

    def execute(self, img, shift_values):
        return shift_3d_array_subpixel(img, shift_values, filling_val=np.nan)

    def save(self, img_shifted):
        if not os.path.exists(self.out_folder):
            os.makedirs(self.out_folder)
        filename = self.out_filenames.pop(0)
        filepath = os.path.join(self.out_folder, filename)
        save_tiff(img_shifted, filepath)
