"""Misc utilities."""

import re
import sys
import pathlib
from typing import NoReturn, Callable, Type, Union, Tuple
import traceback
import logging
from .logging import logger

# Path-like
Pathlike = Union[str, pathlib.Path]

# Check if name only contains A-Z, a-z, 0-9 and underscore
vaild_name = re.compile(r"^[A-Za-z0-9_]+$")


def error_exit() -> NoReturn:
    """Exit with return code 1."""
    if logger.isEnabledFor(logging.DEBUG):
        traceback.print_exc()
    logger.debug("Exited with error code 1.")
    sys.exit(1)


def ensure_path(
    path: Pathlike, is_dir: bool = False
) -> pathlib.Path:
    """
    Ensure path exists and is a directory or a file.

    Args:
        path: Can be either a string or a path.
        is_dir: If set to True, ensure path is a directory, otherwise, a file.

    Returns:
        An absolute pathlib.Path object that exists. Raise an RuntimeError if
        not exists.
    """
    path = pathlib.Path(path).absolute()
    if not path.exists():
        raise RuntimeError("Path {} does not exist.".format(path))
    path_is_dir = path.is_dir()
    if path_is_dir != is_dir:  # Does not match check type.
        if is_dir:
            raise RuntimeError("Path {} is not a directory".format(path))
        else:
            raise RuntimeError("Path {} is a directory".format(path))
    return path


def error(e: Exception) -> NoReturn:
    """Report an error."""
    logger.error(e)
    error_exit()


def handle(
    func: Callable,
    exception_type: Union[Type[Exception], Tuple[Type[Exception]]],
    *args,
    **kwargs
):
    """
    Call function with errors handled in cfpm's way.

    Before using this function, make sure all of func's errors are known and
    can exit saftly after an error is raised whithout cleaning up.

    Args:
        func: The function to be called.
        exception_type: The type(s) of the exceptions that can be handled
            safely.
    """
    try:
        return func(*args, **kwargs)
    except exception_type as e:
        error(e)
