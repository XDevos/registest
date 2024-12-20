#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from argparse import ArgumentParser


def parse_run_args():
    """Parse run arguments

    Returns
    -------
    ArgumentParser.args
        An accessor of run arguments
    """
    parser = ArgumentParser()
    parser.add_argument(
        "-R",
        "--reference",
        type=str,
        help="Reference 3D image filepath.",
    )
    parser.add_argument(
        "-O",
        "--output",
        type=str,
        default=os.getcwd(),
        help="Folder path for output data.\nDEFAULT: Current directory",
    )
    parser.add_argument(
        "-C",
        "--command",
        type=str,
        default="prepare,register,compare",
        help="Comma-separated command list.\nDEFAULT: prepare,register,compare",
    )
    parser.add_argument(
        "-P",
        "--parameters",
        type=str,
        default=os.getcwd() + os.sep + "parameters.json",
        help="Path of the parameters.json file.\nDEFAULT: We expect this file inside your current directory",
    )

    return parser.parse_args()
