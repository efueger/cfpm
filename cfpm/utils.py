"""Misc utilities."""

import re
import sys
from typing import NoReturn, IO, Any
from .logging import logger


def error_exit() -> NoReturn:
    """Exit with return code 1."""
    logger.debug("Exited with error code 1.", exc_info=True)
    sys.exit(1)


def uncaught_exit() -> NoReturn:
    """Exit with return code 3."""
    logger.debug("Exited with error code 3.")
    sys.exit(3)


# Check if name only contains A-Z, a-z, 0-9 and underscore
vaild_name = re.compile(r"^[A-Za-z0-9_]+$")


def open_file(file, *args, **kwargs) -> IO[Any]:
    """Open a file with errors handled in cfpm's way."""
    try:
        return open(file, *args, **kwargs)
    except OSError as e:
        logger.error(e)
        error_exit()
