"""Command line entries for cfpm."""

import sys
from ..logging import logger
from .cli import cli

from .build import build
from .new import new
from .version import version

cli.add_command(build)
cli.add_command(new)
cli.add_command(version)


def main():
    """
    Call this function as an entrypoint.

    Uncaught exception will be caught here as a critical message. Since it may
    left the project in a broken middle state.
    """
    try:
        cli()
    except Exception as e:
        logger.critical("Uncaught exception!")
        logger.critical(e, exc_info=True)
        sys.exit(3)
