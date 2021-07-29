"""Command version."""

import click
from typing import Dict, List
from .. import __version__


# If you consider your work is important enough (decided by yourself), put
# yourself into this dictionary.
CREDITS: Dict[str, List[str]] = {"Author": ["Yi Cao"]}


@click.command()
@click.option("-c", "--credits", is_flag=True, help="Show credits")
def version(credits: bool):
    """Show the current version of cfpm."""
    version_message = "cfpm version {}".format(
        click.style(__version__, fg="bright_blue")
    )
    click.echo(version_message)
    if credits:
        print()
        for (key, value) in CREDITS.items():
            print(key)
            for name in value:
                print("  {}".format(name))
