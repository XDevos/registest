import json

import tifffile


def load_tiff(filepath):
    return tifffile.imread(filepath)


def save_tiff(image, filepath):
    tifffile.imwrite(filepath, image)


def load_json(filepath):
    # Load the JSON data
    with open(filepath, "r") as f:
        return json.load(f)
