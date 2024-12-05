#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from registest._version import __version__


def main(command_line_arguments=None):
    pass


if __name__ == "__main__":
    begin_time = datetime.now()
    print(f"[VERSION] registest {__version__}")
    main()
    print("\n==================== Normal termination ====================\n")
    print(f"Elapsed time: {datetime.now() - begin_time}")
