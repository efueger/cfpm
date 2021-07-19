"""Command line entries for cfpm."""

import click
import click_log  # type: ignore
from .log import logger
from . import __version__


@click.group()
@click_log.simple_verbosity_option(logger)
def cli():  # noqa: D401
    """The C-Family Package Manager."""
    logger.debug("Logging level is " + str(logger.getEffectiveLevel()))


@cli.command()
def version():
    """Show the current version of cfpm."""
    click.echo("cfpm version " + __version__)


if __name__ == "__main__":
    cli()
