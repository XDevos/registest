# -*- coding: utf-8 -*-

import functools
from datetime import datetime

from registest._version import __version__


def timing_main(func):
    """Decorator to print runtime info of _main()."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        begin_time = datetime.now()
        print(f"[VERSION] RegisTest {__version__}")
        result = func(*args, **kwargs)
        print("\n==================== Normal termination ====================\n")
        print(f"Elapsed time: {datetime.now() - begin_time}")
        return result

    return wrapper
