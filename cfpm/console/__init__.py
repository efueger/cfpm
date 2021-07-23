"""Command line entries for cfpm."""

from ..log import logger
from .cli import cli

from .new import new  # noqa: F401, E402
from .version import version  # noqa: F401, E402

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
