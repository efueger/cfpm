import click
import click_log
from .log import logger
from . import __version__


@click.group()
@click_log.simple_verbosity_option(logger)
def cli():
    logger.debug("Logging level is " + str(logger.getEffectiveLevel()))


@cli.command()
def version():
    """
    Show the current version of cfpm.
    """
    click.echo("cfpm version " + __version__)


if __name__ == "__main__":
    import sys

    cli(sys.argv)
