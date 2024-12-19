# -*- coding: utf-8 -*-

import os

from registest.utils.io_utils import load_tiff, save_tiff


class ReferenceImg:
    def __init__(self, filepath: str):
        """
        Initialize the ReferenceImg object.

        Parameters
        ----------
        filepath : str
            Path to the reference image file.
        """
        self.path = filepath
        self.data = self.load()

    def load(self):
        """
        Load the image file after performing various checks.

        Returns
        -------
        ndarray
            The loaded 3D image data.

        Raises
        ------
        FileNotFoundError
            If the file does not exist.
        ValueError
            If the file is not a TIFF file or not a 3D image.
        """
        # Check if the file exists
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"File not found: {self.path}")

        # Check if the file has a .tif or .tiff extension
        if not (self.path.endswith(".tif") or self.path.endswith(".tiff")):
            raise ValueError(
                f"Invalid file format: {self.path}. Expected a .tif or .tiff file."
            )

        # Load the TIFF file
        try:
            data = load_tiff(self.path)
        except Exception as e:
            raise ValueError(f"Error reading the TIFF file: {e}")

        # Check if the data is 3D
        if data.ndim != 3:
            raise ValueError(
                f"The file is not a 3D image. Found {data.ndim} dimensions."
            )

        return data


class OutFolder:
    def __init__(self, path: str):
        """
        Initialize the OutFolder object.

        Parameters
        ----------
        path : str
            Path to the main output folder.
        """
        self.path = path
        self.prepa = os.path.join(self.path, "Preparation")
        self.regis = os.path.join(self.path, "Registration")
        self.comp = os.path.join(self.path, "Comparison")
        self.create_folders()

    def create_folders(self):
        """
        Create the necessary folders if they do not already exist.
        """
        try:
            # Create the main output folder
            os.makedirs(self.path, exist_ok=True)
            # Create the subfolders
            os.makedirs(self.prepa, exist_ok=True)
            os.makedirs(self.regis, exist_ok=True)
            os.makedirs(self.comp, exist_ok=True)
        except Exception as e:
            # for the case of permission issues
            raise RuntimeError(f"Error creating folders: {e}")

    def find_path(self, name: str):
        if name == os.path.basename(self.prepa):
            return self.prepa
        elif name == os.path.basename(self.regis):
            return self.regis
        elif name == os.path.basename(self.comp):
            return self.comp
        else:
            raise ValueError(f"The folder name '{name}' doesn't exist.")


class DataManager:
    def __init__(self, reference_path: str, output_path: str):
        self.ref = ReferenceImg(reference_path)
        self.out_folder = OutFolder(output_path)

    def save_tif(self, data, folder, name):
        folder_path = self.out_folder.find_path(folder)
        if name[-4:] != ".tif":
            name = name + ".tif"
        filepath = os.path.join(folder_path, name)
        save_tiff(data, filepath)

    def get_prepa_img_paths(self):
        folder_to_explore = self.out_folder.prepa
        paths = get_tif_filepaths(folder_to_explore)
        return paths


def get_tif_filepaths(folder_path):
    """
    Retrieve all .tif and .tiff file paths from a given folder.

    Parameters
    ----------
    folder_path : str
        Path to the folder to search for TIFF files.

    Returns
    -------
    list of str
        A list of file paths to .tif or .tiff files in the folder.
    """
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder '{folder_path}' does not exist.")

    if not os.path.isdir(folder_path):
        raise ValueError(f"The path '{folder_path}' is not a directory.")

    tif_paths = [
        os.path.join(folder_path, file)
        for file in os.listdir(folder_path)
        if file.endswith((".tif", ".tiff"))
    ]

    return tif_paths
