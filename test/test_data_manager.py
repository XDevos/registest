#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from unittest.mock import patch

import numpy as np
import pytest

from registest.core.data_manager import OutFolder, ReferenceImg


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
