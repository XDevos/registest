import json

import numpy as np
import tifffile
from PIL import Image
from reportlab.pdfgen import canvas


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


def load_png(filepath):
    """Load a PNG file and convert it in numpy array."""
    image = Image.open(filepath).convert("RGB")
    return np.array(image)


def save_png(data, path):
    """Save a numpy array as PNG image."""
    image = Image.fromarray(data)
    image.save(path, format="PNG")


def save_pdf(data, path):
    """Create PDF from text."""
    c = canvas.Canvas(path)
    c.drawString(100, 750, data)  # Text position on the page
    c.save()
