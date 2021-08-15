"""Command line program drivers."""

import pathlib
import os
import subprocess
from copy import deepcopy
from typing import List, Optional, Dict, Tuple
from .logging import logger
from .utils import ensure_path, Pathlike


class CLIDriver:
    """
    A generic driver to exectute command line programs.

    Use CLIFactory to create the driver.
    """

    def __init__(self):
        """Do not call this directly."""
        self.program = None
        self.args = None

    def add_argument(self, arg: str) -> None:
        """Add an argument to the program."""
        self.args.append(arg)

    def set_argument(self, args: List[str]) -> None:
        """Set the arguments to the program."""
        self.args = args

    def run(self, *args, **kwargs) -> subprocess.CompletedProcess:
        """
        Execute self with arguments. Note that this is a blocked function.

        Extra args and kwargs will be passed into the underlying
        subprocess.call. Commands finished with non-zero exit status will not
        be thrown as an exception.
        """
        a = list(self.program)
        a.extend(self.args)
        return subprocess.run(a, capture_output=True, *args, **kwargs)


class CLIFactory:
    """A factory for creating CLIDriver."""

    def __init__(
        self, program_name: str, default_options: List[str] = list()
    ) -> None:
        """
        Initialize the factory with program_name.

        The function will look for the executable if program_name is not a
        path. A RuntimeError will be raised if it's not found in PATH.

        Args:
            program_name: A string, stands for the cli exectuable. Can be
                either a name or a path. If it's a path that doesn't exist, a
                BadConfigurationError will be raised.
            default_options: An optional list contains arguments that will be
                included everytime the driver is created.
        """
        self.driver = CLIDriver()
        self.driver.args = default_options
        if "/" in program_name or "\\" in program_name:
            path = ensure_path(program_name)
            self.driver.program = path
        else:  # Searches for the executable in PATH.
            path_list = list(map(pathlib.Path, os.environ["PATH"].split(":")))
            for p in path_list:
                possible_path = p / program_name
                if possible_path.is_file():
                    logger.debug(
                        "Found {} in {}.".format(program_name, possible_path)
                    )
                    self.driver.program = possible_path
                    return
            raise RuntimeError(
                "Program {} is not found in PATH.".format(program_name)
            )

    def create(self) -> CLIDriver:
        """Create a new CLIDriver instance."""
        return deepcopy(self.driver)


class GenericCompilerDriver:
    """An abstract base class declared with some generic compiler options."""

    def __init__(self) -> None:
        """Initialize the compiler driver. Do not call this directly."""
        self.definations: Dict[str, Optional[str]] = {}
        self.includes: List[pathlib.Path] = []
        self.link_dir: List[pathlib.Path] = []
        self.links: List[Tuple[str, bool]] = []
        self.arguments: List[str] = []  # Generated arguments

    # Arguments
    def add_definition(self, key: str, value: str) -> None:
        """Add a new preprocessor definition."""
        self.definations[key] = value
        self._gen_args()

    def add_include_directory(self, dir: Pathlike) -> None:
        """Add a new include directory."""
        dir = ensure_path(dir, True)
        self.includes.append(dir)
        self._gen_args()

    def add_link_library(self, name: str, static: bool) -> None:
        """
        Add a new library to link.

        If static is True, the compiler will preper to link to a static
        library.
        """
        self.links.append((name, static))
        self._gen_args()

    def add_link_directory(self, dir: Pathlike) -> None:
        """Add a new directory to the searching path while linking."""
        dir = ensure_path(dir, True)
        self.link_dir.append(dir)
        self._gen_args()

    # Actions
    def compile_obj(self, src: Pathlike, obj: Pathlike) -> None:
        """Compile src to obj."""
        raise NotImplementedError

    def link(self, objs: List[Pathlike]) -> None:
        """Link objs to a lib or an executable."""
        raise NotImplementedError

    # Abstract methods
    def _gen_args(self):
        """
        Generate new arguments for the compiler.

        This differs from the compiler.
        """
        raise NotImplementedError
