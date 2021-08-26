"""Command build."""

import click
import pathlib
import tomlkit
from tomlkit.exceptions import TOMLKitError
from typing import Dict
from ..logging import logger
from ..projects import Build
from ..utils import handle, error


@click.command()
@click.pass_obj
def build(obj: Dict):
    """Build your package."""
    config_path = pathlib.Path('./cfpm.toml').absolute()
    logger.debug("cfpm configuration file {}.".format(config_path))
    with handle(open, OSError, config_path, 'r') as f:
        content = f.read()
        config = handle(tomlkit.parse, TOMLKitError, content)
    try:
        build = Build(config)
    except TypeError as e:
        error(e)
    build.build()
