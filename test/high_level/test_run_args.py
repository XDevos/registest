#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from unittest.mock import patch

import pytest

from registest.core.run_args import parse_run_args


# No arg
def test_parse_run_args_no_arg(monkeypatch):
    """Test parse_run_args with no arguments passed."""
    monkeypatch.setattr("sys.argv", ["registest"])
    args = parse_run_args()

    # Assert default values
    assert args.reference is None
    assert args.folder == os.getcwd()
    assert args.parameters == os.getcwd() + os.sep + "parameters.json"


# Unknown arg
def test_parse_run_args_with_unknown_option(monkeypatch):
    """Test parse_run_args with an unknown argument (-O)."""
    monkeypatch.setattr("sys.argv", ["registest", "-O", "/path/to/output"])

    with pytest.raises(SystemExit) as exc_info:
        parse_run_args()  # This should raise an error due to unknown argument

    assert exc_info.value.code != 0  # Ensure it exits with a non-zero error code


# all args
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


# default parameters arg
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


# reference arg
def test_parse_run_args_with_reference(monkeypatch):
    """Test parse_run_args with a reference argument."""
    monkeypatch.setattr("sys.argv", ["registest", "-R", "/path/to/reference"])
    args = parse_run_args()

    assert args.reference == "/path/to/reference"
    assert args.folder == os.getcwd()
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


# folder arg
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


# XYZ args
@pytest.mark.parametrize(
    "cli_args, expected_x, expected_y, expected_z",
    [
        (["-X", "10"], 10, None, None),
        (["-Y", "-1.555"], None, -1.555, None),
        (["-Z", "3.14"], None, None, 3.14),
        (["-X", "0.0", "-Y", "1.23", "-Z", "-13.0"], 0, 1.23, -13.0),
        ([], None, None, None),  # No arguments should result in all None
    ],
)
def test_parse_run_args_xyz(cli_args, expected_x, expected_y, expected_z):
    """Test parsing of -X, -Y and -Z command-line arguments for `regis_transform` script."""
    with patch.object(sys, "argv", ["regis_transform"] + cli_args):
        args = parse_run_args()
        assert args.X == expected_x
        assert args.Y == expected_y
        assert args.Z == expected_z


# method arg
@pytest.mark.parametrize(
    "cli_args, expected_method",
    [
        (["-M", "register_global"], "register_global"),
        (["--method", "register_local"], "register_local"),
        ([], "scipy"),  # No argument should result "scipy" method name
    ],
)
def test_parse_run_args_method(cli_args, expected_method):
    """Test parsing of -M/--method command-line argument."""
    with patch.object(sys, "argv", ["registest"] + cli_args):
        args = parse_run_args()
        assert args.method == expected_method


# command arg
@pytest.mark.parametrize(
    "cli_args, expected_method",
    [
        (["-C", "transform"], "transform"),
        (["--command", "register,compare"], "register,compare"),
        (
            [],
            "transform,register,compare",
        ),  # No argument should result default "transform,register,compare"
    ],
)
def test_parse_run_args_command(cli_args, expected_method):
    """Test parsing of -C/--command command-line argument."""
    with patch.object(sys, "argv", ["registest"] + cli_args):
        args = parse_run_args()
        assert args.command == expected_method
