import json
import os

import tifffile


def load_tiff(filepath):
    return tifffile.imread(filepath)


def save_tiff(image, filepath):
    tifffile.imwrite(filepath, image)


def load_parameters(parameters_file):
    # Check if the file exists
    if not os.path.exists(parameters_file):
        raise FileNotFoundError(f"'parameters.json' file not found: {parameters_file}")

    # Load the JSON data
    with open(parameters_file, "r") as f:
        return json.load(f)
