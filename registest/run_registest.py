#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

from registest._version import __version__
from registest.config.parameters import Parameters
from registest.core.data_manager import DataManager
from registest.core.pipeline import Pipeline
from registest.core.run_args import parse_run_args


def _main():
    run_args = parse_run_args()
    datam = DataManager(run_args.reference, run_args.output)
    params = Parameters(run_args.parameters)
    pipe = Pipeline(datam, params)
    pipe.run()


def main():
    begin_time = datetime.now()
    print(f"[VERSION] RegisTest {__version__}")
    _main()
    print("\n==================== Normal termination ====================\n")
    print(f"Elapsed time: {datetime.now() - begin_time}")


if __name__ == "__main__":
    main()
