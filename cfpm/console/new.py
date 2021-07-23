"""Command new."""
import click


@click.command()
@click.argument("packagename", envvar="CFPM_NEW_PACKAGENAME")
def new(packagename: str):
    """Create a new package."""
    raise NotImplementedError("Command new is not implemented, yet.")  # TODO
