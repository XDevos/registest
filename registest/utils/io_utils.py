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


def save_json(data, path):
    with open(path, "w") as file:
        json.dump(data, file, ensure_ascii=False, sort_keys=True, indent=4)
