"""Command new."""

import click
import pathlib
from typing import Dict
from ..utils import vaild_name, handle
from ..logging import logger
from ..exceptions import BadConfigurationError

# fmt: off
# Code templates
TEMPLATES: Dict[str, str] = {}

TEMPLATES["cfpm.toml"] = """[package]
name = "%NAME%"
version = "0.1.0"

c_standard = "99"
cpp_standard = "11"

[[targets]]
dir = "src"
name = "hello"
"""

TEMPLATES["src/hello.toml"] = """[target]
type = "bin"
headers = ["."]
sources = ["."]
"""

TEMPLATES["src/hello.h"] = """#ifndef _HELLO_H_
#define _HELLO_H_

#include <stdio.h>

#ifdef __cplusplus
extern "C" {
#endif

void hello();

#ifdef __cplusplus
}
#endif

#endif
"""

TEMPLATES["src/hello.c"] = """#include <hello.h>

void hello() {
    printf("Hello there!");
}
"""

TEMPLATES["src/main.cpp"] = """#include <hello.h>

int main(int argc, char const *argv[]) {
    hello();
    return 0;
}
"""
# fmt: on


def check_package_name(name: str) -> None:
    """Check if package name is avaliable. Raise exceptions otherwise."""
    if not vaild_name.match(name):
        raise BadConfigurationError(
            "Package name {} should contain only alphanumeric characters and "
            "underscores.".format(name)
        )
    cwd = pathlib.Path(".").absolute()
    logger.debug("Current path {}.".format(cwd))
    dest = cwd / name
    if dest.exists():
        raise BadConfigurationError(
            "Directory {} already exists.".format(dest)
        )


@click.command()
@click.argument("package_name", envvar="CFPM_NEW_PACKAGE_NAME")
def new(package_name: str):
    """Create a new package."""
    handle(check_package_name, BadConfigurationError, package_name)
    package_dir = pathlib.Path(".").absolute() / package_name
    for (dest, content) in TEMPLATES.items():
        write_file = package_dir / dest
        write_base_dir = pathlib.Path(*write_file.parts[:-1])
        handle(write_base_dir.mkdir, OSError, parents=True, exist_ok=True)
        with handle(open, OSError, write_file, "w") as f:
            logger.debug("Created file {}.".format(write_file))
            f.write(content.replace("%NAME%", package_name))
    logger.info(
        click.style(
            "Successfully created package {}.".format(package_name), fg="green"
        )
    )
