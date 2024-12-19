#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

from modules.transformation import Transform
from utils.io_utils import load_parameters

from registest._version import __version__
from registest.core.data_manager import DataManager

# from core.command_parser import CommandParser
# from core.pipeline import Pipeline
from registest.core.run_args import parse_run_args


def main():
    run_args = parse_run_args()
    datam = DataManager(run_args.reference, run_args.output)
    # param = Parameters(run_args.parameters)

    # pipe = Pipeline(datam, param)
    # pipe.execute()

    # Load the input image and commands
    params_path = run_args.parameters
    # commands = [
    #     {"command": "transform", "params": {"type": "rotate", "angle": 45}},
    #     {"command": "extract", "params": {"region": [10, 20, 10, 50, 10, 50]}},
    #     {"command": "register", "params": {"method": "affine"}},
    #     {"command": "compare", "params": {"metric": "mse"}},
    #     {"command": "visualize", "params": {"slice": 30}},
    #     {"command": "report", "params": {"output": "report.pdf"}},
    # ]

    # Initialize components
    command_list = [
        Transform,
        # Compare,
        # Extract,
        # Register,
        # Shift,
        # Extract,
        # Compare,
        # Visualize,
        # Report,
    ]
    # pipeline = Pipeline(run_args, command_list)

    # # Execute the pipeline
    # pipeline.run()
    all_params = load_parameters(params_path)
    ref = datam.ref.data
    for cmd in command_list:
        params = all_params[cmd.__name__]
        routine = cmd(params, datam.out_folder.path)
        input_list = routine.load_inputs()
        for input in input_list:
            output = routine.execute(ref, input)
            routine.save(output)


if __name__ == "__main__":
    begin_time = datetime.now()
    print(f"[VERSION] registest {__version__}")
    main()
    print("\n==================== Normal termination ====================\n")
    print(f"Elapsed time: {datetime.now() - begin_time}")
