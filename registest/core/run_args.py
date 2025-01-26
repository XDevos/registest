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
        "-T",
        "--target",
        type=str,
        help="Target 3D image filepath.",
    )
    parser.add_argument(
        "-F",
        "--folder",
        type=str,
        default=os.getcwd(),
        help="Folder path for data.\nDEFAULT: Current directory",
    )
    parser.add_argument(
        "-C",
        "--command",
        type=str,
        default="transform,register,compare",
        help="Comma-separated command list.\nDEFAULT: transform,register,compare",
    )
    parser.add_argument(
        "-P",
        "--parameters",
        type=str,
        default=os.getcwd() + os.sep + "parameters.json",
        help="Path of the parameters.json file.\nDEFAULT: We expect this file inside your current directory",
    )

    parser.add_argument(
        "-X",
        type=float,
        help="Transformation value for the X-axis",
    )

    parser.add_argument(
        "-Y",
        type=float,
        help="Transformation value for the Y-axis",
    )

    parser.add_argument(
        "-Z",
        type=float,
        help="Transformation value for the Z-axis",
    )

    parser.add_argument(
        "-M",
        "--method",
        type=str,
        default="scipy",
        help="Registration method name. Default: scipy",
    )

    return parser.parse_args()
