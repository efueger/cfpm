"""Click group of the main cli."""

import click
import pathlib
from os.path import expanduser
from ..utils import handle
from ..logging import logger, simple_verbosity_option


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@simple_verbosity_option(logger, envvar="CFPM_VERBOSITY")
@click.option(
    "--cfpm-home",
    default=expanduser("~/.cfpm"),
    envvar="CFPM_HOME",
    help="Home directory for cfpm to store all the build cache and "
    "configuration and stuff.",
)
@click.pass_context
def cli(ctx: click.Context, cfpm_home: str):  # noqa: D400, D401
    """C-Family Package Manager"""
    ctx.obj = dict()
    cfpm_home_path = pathlib.Path(cfpm_home).absolute()
    if not cfpm_home_path.exists():
        handle(cfpm_home_path.mkdir, OSError, parents=False)
    ctx.obj["cfpm_home"] = cfpm_home_path
    logger.debug("cfpm home path {}.".format(cfpm_home_path))
