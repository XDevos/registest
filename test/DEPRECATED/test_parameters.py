#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest.mock import patch

import pytest

from registest.config.parameters import Parameters


@patch("registest.config.parameters.load_json")
def test_parameters_valid(mock_load_json, tmp_path):
    """
    Test Parameters class with a valid JSON file.
    """
    # Mock valid JSON data
    mock_load_json.return_value = {
        "prepare": {"method": "scipy", "shifts": [[0.5, 0, 0]], "filling_value": "0.0"},
        "register": {"method": "pyhim"},
    }

    # Create a temporary JSON file
    temp_file = tmp_path / "parameters.json"
    temp_file.touch()  # Ensure the file exists

    # Initialize Parameters
    params = Parameters(str(temp_file))

    # Assertions
    assert params.prepare == mock_load_json.return_value["prepare"]
    assert params.register == mock_load_json.return_value["register"]
    mock_load_json.assert_called_once_with(str(temp_file))


def test_parameters_file_not_found(tmp_path):
    """
    Test Parameters raises FileNotFoundError for missing file.
    """
    missing_file_path = tmp_path / "nonexistent.json"
    with pytest.raises(FileNotFoundError, match="'parameters.json' file not found"):
        Parameters(str(missing_file_path))


@patch("registest.config.parameters.load_json")
def test_parameters_invalid_json(mock_load_json, tmp_path):
    """
    Test Parameters raises ValueError for invalid JSON data.
    """
    # Mock an exception when loading JSON
    mock_load_json.side_effect = ValueError("Invalid JSON format")

    # Create a temporary JSON file
    temp_file = tmp_path / "parameters.json"
    temp_file.touch()

    with pytest.raises(ValueError, match="Invalid JSON format"):
        Parameters(str(temp_file))
    mock_load_json.assert_called_once_with(str(temp_file))
