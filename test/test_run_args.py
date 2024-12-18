#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from registest.core.run_args import parse_run_args


def test_parse_run_args_no_args(monkeypatch):
    """Test parse_run_args with no arguments passed."""
    monkeypatch.setattr("sys.argv", ["run_registest"])
    args = parse_run_args()

    # Assert default values
    assert args.reference is None
    assert args.output == os.getcwd()
    assert args.parameters is None


def test_parse_run_args_with_reference(monkeypatch):
    """Test parse_run_args with a reference argument."""
    monkeypatch.setattr("sys.argv", ["run_registest", "-R", "/path/to/reference"])
    args = parse_run_args()

    assert args.reference == "/path/to/reference"
    assert args.output == os.getcwd()
    assert args.parameters is None


def test_parse_run_args_with_all_arguments(monkeypatch):
    """Test parse_run_args with all arguments provided."""
    monkeypatch.setattr(
        "sys.argv",
        [
            "run_registest",
            "-R",
            "/path/to/reference",
            "-O",
            "/path/to/output",
            "-P",
            "/path/to/parameters.json",
        ],
    )
    args = parse_run_args()

    assert args.reference == "/path/to/reference"
    assert args.output == "/path/to/output"
    assert args.parameters == "/path/to/parameters.json"


def test_parse_run_args_with_default_parameters(monkeypatch):
    """Test parse_run_args with default parameters file."""
    monkeypatch.setattr(
        "sys.argv",
        ["run_registest", "-R", "/path/to/reference", "-O", "/path/to/output"],
    )
    args = parse_run_args()

    assert args.reference == "/path/to/reference"
    assert args.output == "/path/to/output"
    assert args.parameters is None
