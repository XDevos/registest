#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from unittest.mock import patch

import pytest

from registest.core.run_args import parse_run_args


def test_parse_run_args_no_args(monkeypatch):
    """Test parse_run_args with no arguments passed."""
    monkeypatch.setattr("sys.argv", ["registest"])
    args = parse_run_args()

    # Assert default values
    assert args.reference is None
    assert args.folder == os.getcwd()
    assert args.parameters == os.getcwd() + os.sep + "parameters.json"


def test_parse_run_args_with_unknown_option(monkeypatch):
    """Test parse_run_args with an unknown argument (-O)."""
    monkeypatch.setattr("sys.argv", ["registest", "-O", "/path/to/output"])

    with pytest.raises(SystemExit) as exc_info:
        parse_run_args()  # This should raise an error due to unknown argument

    assert exc_info.value.code != 0  # Ensure it exits with a non-zero error code


def test_parse_run_args_with_reference(monkeypatch):
    """Test parse_run_args with a reference argument."""
    monkeypatch.setattr("sys.argv", ["registest", "-R", "/path/to/reference"])
    args = parse_run_args()

    assert args.reference == "/path/to/reference"
    assert args.folder == os.getcwd()
    assert args.parameters == os.getcwd() + os.sep + "parameters.json"


def test_parse_run_args_with_all_arguments(monkeypatch):
    """Test parse_run_args with all arguments provided."""
    monkeypatch.setattr(
        "sys.argv",
        [
            "run_registest",
            "-R",
            "/path/to/reference",
            "-F",
            "/path/to/data_folder",
            "-P",
            "/path/to/parameters.json",
        ],
    )
    args = parse_run_args()

    assert args.reference == "/path/to/reference"
    assert args.folder == "/path/to/data_folder"
    assert args.parameters == "/path/to/parameters.json"


def test_parse_run_args_with_default_parameters(monkeypatch):
    """Test parse_run_args with default parameters file."""
    monkeypatch.setattr(
        "sys.argv",
        ["run_registest", "-R", "/path/to/reference", "-F", "/path/to/data_folder"],
    )
    args = parse_run_args()

    assert args.reference == "/path/to/reference"
    assert args.folder == "/path/to/data_folder"
    assert args.parameters == os.getcwd() + os.sep + "parameters.json"


@pytest.mark.parametrize(
    "cli_args, expected_reference",
    [
        (["-R", "path/to/image.tif"], "path/to/image.tif"),
        (["--reference", "another_path.tif"], "another_path.tif"),
        ([], None),  # No argument should result in None
    ],
)
def test_parse_run_args_reference(cli_args, expected_reference):
    """Test parsing of -R/--reference command-line argument."""
    with patch.object(sys, "argv", ["registest"] + cli_args):
        args = parse_run_args()
        assert args.reference == expected_reference


@pytest.mark.parametrize(
    "cli_args, expected_folder",
    [
        (["-F", "path/to/data"], "path/to/data"),
        (["--folder", "path/to/data/"], "path/to/data/"),
        ([], os.getcwd()),  # No argument should result current directory
    ],
)
def test_parse_run_args_folder(cli_args, expected_folder):
    """Test parsing of -F/--folder command-line argument."""
    with patch.object(sys, "argv", ["registest"] + cli_args):
        args = parse_run_args()
        assert args.folder == expected_folder
