#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

from modules.transformation import Transform

from registest._version import __version__
from registest.config.parameters import Parameters
from registest.core.data_manager import DataManager
from registest.core.run_args import parse_run_args


def main():
    run_args = parse_run_args()
    datam = DataManager(run_args.reference, run_args.output)
    param = Parameters(run_args.parameters)

    # pipe = Pipeline(datam, param)
    # pipe.execute()

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
    all_params = param.dict
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
