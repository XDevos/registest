#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

from core.command_parser import CommandParser
from core.pipeline import Pipeline
from core.run_args import InputHandler

from registest._version import __version__


def main(command_line_arguments=None):
    # Load the input image and commands
    image_path = "path/to/image.tiff"
    commands = [
        {"command": "transform", "params": {"type": "rotate", "angle": 45}},
        {"command": "extract", "params": {"region": [10, 20, 10, 50, 10, 50]}},
        {"command": "register", "params": {"method": "affine"}},
        {"command": "compare", "params": {"metric": "mse"}},
        {"command": "visualize", "params": {"slice": 30}},
        {"command": "report", "params": {"output": "report.pdf"}},
    ]

    # Initialize components
    input_handler = InputHandler(image_path)
    command_parser = CommandParser(commands)
    pipeline = Pipeline(input_handler, command_parser)

    # Execute the pipeline
    pipeline.run()


if __name__ == "__main__":
    begin_time = datetime.now()
    print(f"[VERSION] registest {__version__}")
    main()
    print("\n==================== Normal termination ====================\n")
    print(f"Elapsed time: {datetime.now() - begin_time}")
