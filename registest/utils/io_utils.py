import tifffile


def load_tiff(filepath):
    return tifffile.imread(filepath)


def save_tiff(image, filepath):
    tifffile.imwrite(filepath, image)
