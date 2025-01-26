#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from registest.config.parameters import Parameters
from registest.core.data_manager import DataManager
from registest.core.pipeline import Pipeline
from registest.core.run_args import parse_run_args
from registest.utils.metrics import timing_main


@timing_main
def main():
    run_args = parse_run_args()
    datam = DataManager(run_args.folder)
    params = Parameters(run_args.parameters)
    pipe = Pipeline(datam, params, run_args.command)
    pipe.run()


if __name__ == "__main__":
    main()
