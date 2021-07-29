"""Misc utilities."""

import re
import sys
from typing import NoReturn, Callable
import traceback
import logging
from .logging import logger


def error_exit() -> NoReturn:
    """Exit with return code 1."""
    if logger.isEnabledFor(logging.DEBUG):
        traceback.print_exc()
    logger.debug("Exited with error code 1.")
    sys.exit(1)


def handle(func: Callable, *args, **kwargs):
    """
    Call function with errors handled in cfpm's way.

    Before using this function, make sure all of func's errors are known and
    can exit saftly after an error is raised whithout cleaning up.
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(e)
        error_exit()


# Check if name only contains A-Z, a-z, 0-9 and underscore
vaild_name = re.compile(r"^[A-Za-z0-9_]+$")
