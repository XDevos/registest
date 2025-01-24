#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from unittest.mock import patch

import numpy as np
import pytest

from registest.core.data_manager import DataManager, OutFolder, ReferenceImg


# Mocking utility for load_tiff function
@patch("registest.core.data_manager.load_tiff")
def test_reference_img_valid(mock_load_tiff, tmp_path):
    # Simulate a valid 3D array
    mock_load_tiff.return_value = np.zeros((10, 10, 10))

    # Create a temporary valid file
    temp_file = tmp_path / "image.tif"
    temp_file.touch()

    ref = ReferenceImg(str(temp_file))
    assert ref.data.shape == (10, 10, 10)
    mock_load_tiff.assert_called_once_with(str(temp_file))


@patch("registest.core.data_manager.load_tiff")
def test_reference_img_file_not_found(mock_load_tiff):
    with pytest.raises(FileNotFoundError):
        ReferenceImg("/invalid/path/to/image.tif")
    mock_load_tiff.assert_not_called()


@patch("registest.core.data_manager.load_tiff")
def test_reference_img_invalid_extension(mock_load_tiff, tmp_path):
    # Create a file with an invalid extension
    temp_file = tmp_path / "image.jpg"
    temp_file.touch()

    with pytest.raises(ValueError, match="Invalid file format"):
        ReferenceImg(str(temp_file))
    mock_load_tiff.assert_not_called()


@patch("registest.core.data_manager.load_tiff")
def test_reference_img_not_3d(mock_load_tiff, tmp_path):
    # Simulate a non-3D array
    mock_load_tiff.return_value = np.zeros((10, 10))

    temp_file = tmp_path / "image.tif"
    temp_file.touch()

    with pytest.raises(ValueError, match="The file is not a 3D image"):
        ReferenceImg(str(temp_file))
    mock_load_tiff.assert_called_once_with(str(temp_file))


def test_outfolder_creation(tmp_path):
    output_path = tmp_path / "output"
    out_folder = OutFolder(str(output_path))

    # Verify that the folders are created
    assert os.path.exists(out_folder.path)
    assert os.path.exists(out_folder.prepa)
    assert os.path.exists(out_folder.regis)
    assert os.path.exists(out_folder.comp)


def test_outfolder_creation_error(monkeypatch, tmp_path):
    # Simulate a permission error during folder creation
    def mock_makedirs(*args, **kwargs):
        raise PermissionError("Permission denied")

    monkeypatch.setattr("os.makedirs", mock_makedirs)

    with pytest.raises(RuntimeError, match="Error creating folders"):
        OutFolder(str(tmp_path / "output"))


def test_find_path_valid():
    """
    Test OutFolder.find_path with valid folder names.
    """
    out_folder = OutFolder("/tmp/test_output")
    assert out_folder.find_path("Preparation") == out_folder.prepa
    assert out_folder.find_path("Registration") == out_folder.regis
    assert out_folder.find_path("Comparison") == out_folder.comp


def test_find_path_invalid():
    """
    Test OutFolder.find_path raises ValueError for an invalid folder name.
    """
    out_folder = OutFolder("/tmp/test_output")
    with pytest.raises(ValueError, match="The folder name 'Invalid' doesn't exist."):
        out_folder.find_path("Invalid")


@patch("registest.core.data_manager.load_tiff")
@patch("registest.core.data_manager.save_tiff")
def test_save_tif_valid(mock_save_tiff, mock_load_tiff, tmp_path):
    """
    Test DataManager.save_tif with valid input.
    """

    # Mock load_tiff to return a valid 3D array during DataManager initialization
    mock_load_tiff.return_value = np.zeros((10, 10, 10))

    # Create temporary paths
    ref_path = tmp_path / "reference.tif"
    ref_path.touch()  # Ensure the reference file exists
    output_path = tmp_path / "output"
    output_path.mkdir()

    # Initialize DataManager
    manager = DataManager(str(ref_path), str(output_path))

    # Mock a 3D numpy array
    mock_data = np.zeros((10, 10, 10))

    # Test save_tif
    manager.save_tif(mock_data, "Preparation", "test_image")

    # Expected file path
    expected_path = os.path.join(manager.out_folder.prepa, "test_image.tif")

    # Verify the save_tiff function was called correctly
    mock_save_tiff.assert_called_once_with(mock_data, expected_path)


@patch("registest.core.data_manager.load_tiff")
@patch("registest.core.data_manager.save_tiff")
def test_save_tif_invalid_folder(mock_save_tiff, mock_load_tiff, tmp_path):
    """
    Test DataManager.save_tif raises ValueError for an invalid folder name.
    """
    # Mock load_tiff to return a valid 3D array during DataManager initialization
    mock_load_tiff.return_value = np.zeros((10, 10, 10))

    # Create temporary paths
    ref_path = tmp_path / "reference.tif"
    ref_path.touch()  # Ensure the reference file exists
    output_path = tmp_path / "output"
    output_path.mkdir()

    # Initialize DataManager
    manager = DataManager(str(ref_path), str(output_path))

    # Mock a 3D numpy array
    mock_data = np.zeros((10, 10, 10))

    # Test save_tif with an invalid folder name
    with pytest.raises(
        ValueError, match="The folder name 'InvalidFolder' doesn't exist."
    ):
        manager.save_tif(mock_data, "InvalidFolder", "test_image")
    mock_save_tiff.assert_not_called()
