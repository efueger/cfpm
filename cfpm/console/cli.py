"""Click group of the main cli."""
import click
from ..log import logger, simple_verbosity_option


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@simple_verbosity_option(logger, envvar="CFPM_VERBOSITY")
def cli():  # noqa: D400, D401
    """C-Family Package Manager"""
    logger.debug("Logging level is " + str(logger.getEffectiveLevel()))
