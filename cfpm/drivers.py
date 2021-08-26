"""Command line program drivers."""

import pathlib
import os
import subprocess
from typing import List, Optional, Dict
from .logging import logger
from .utils import ensure_path, Pathlike


class CLIDriver:
    """
    A generic driver to exectute command line programs.

    Use CLIFactory to create the driver.
    """

    def __init__(
        self, program_name: Pathlike, default_options: List[str] = list()
    ):
        """
        Initialize the CLIDriver with program_name.

        The function will look for the executable if program_name is not a
        path. A RuntimeError will be raised if it's not found in PATH.

        Args:
            program_name: A string, stands for the cli exectuable. Can be
                either a name or a path. If it's a path that doesn't exist, a
                BadConfigurationError will be raised.
            default_options: An optional list contains arguments that will be
                included everytime the driver is created.
        """
        self.program: str = ""
        if "/" in str(program_name) or "\\" in str(program_name):
            path = ensure_path(program_name)
            self.program = str(path)
        else:  # Searches for the executable in PATH.
            path_list = list(map(pathlib.Path, os.environ["PATH"].split(":")))
            for p in path_list:
                possible_path = p / program_name
                if possible_path.is_file():
                    logger.debug(
                        "Found {} in {}.".format(program_name, possible_path)
                    )
                    self.program = str(possible_path)
                    return
            raise RuntimeError(
                "Program {} is not found in PATH.".format(program_name)
            )

    def run(self, args: List[str], **kwargs) -> subprocess.CompletedProcess:
        """
        Execute self with arguments and args blocked.

        Extra args and kwargs will be passed into the underlying
        subprocess.call.
        """
        a = [self.program]
        a.extend(args)
        logger.debug("Running {}.".format(a))
        return subprocess.run(a, **kwargs)


class GenericDriver:
    """An abstract base class representing a CLI driver."""

    def __init__(self) -> None:
        """Initialize the driver."""
        self.program: Optional[CLIDriver] = None

    def adapts(self, program: Pathlike) -> bool:
        """
        Test if the driver supports the program.

        If adapted, the crossponding executable is adapted as the program.

        Args:
            program: The program to be tested.

        Returns: If the program is adapted.
        """
        raise NotImplementedError


class GenericCompilerDriver(GenericDriver):
    """An abstract base class declared with some generic compiler options."""

    def __init__(self) -> None:
        """Initialize the compiler driver."""
        super().__init__()
        self.definations: Dict[str, Optional[str]] = {}
        self.includes: List[pathlib.Path] = []
        self.link_dir: List[pathlib.Path] = []
        self.links: List[str] = []

    # Arguments
    def add_definition(self, key: str, value: Optional[str] = None) -> None:
        """Add a new preprocessor definition."""
        self.definations[key] = value
        self._gen_definition(key, value)

    def add_include_directory(self, dir: Pathlike) -> None:
        """Add a new include directory."""
        dir = ensure_path(dir, is_dir=True)
        self.includes.append(dir)
        self._gen_include_directory(dir)

    def add_link_library(self, name: str) -> None:
        """
        Add a new library to link.

        Add .a to the name if you perfer link to static library.
        """
        self.links.append(name)
        self._gen_link_library(name)

    def add_link_directory(self, dir: Pathlike) -> None:
        """Add a new directory to the searching path while linking."""
        dir = ensure_path(dir, True)
        self.link_dir.append(dir)

    def _gen_link_directory(self, directory: pathlib.Path) -> None:
        raise NotImplementedError

    def _gen_link_library(self, name: str) -> None:
        raise NotImplementedError

    def _gen_include_directory(self, dir: pathlib.Path) -> None:
        raise NotImplementedError

    def _gen_definition(self, key: str, value: Optional[str]) -> None:
        raise NotImplementedError

    # Actions
    def compile_obj(
        self, src: Pathlike, obj: Pathlike
    ) -> subprocess.CompletedProcess:
        """Compile src to obj."""
        raise NotImplementedError

    def link_shared(
        self, objs: List[Pathlike], out: Pathlike
    ) -> subprocess.CompletedProcess:
        """Link objs to a shared library."""
        raise NotImplementedError

    def link_executable(
        self, objs: List[Pathlike], out: Pathlike
    ) -> subprocess.CompletedProcess:
        """Link objs to an executable."""
        raise NotImplementedError


class GCC(GenericCompilerDriver):
    """GNU Compiler Collection and gcc-style stuff."""

    def __init__(self) -> None:  # noqa: D107
        super().__init__()
        self._link_dirs: List[str] = []
        self._links: List[str] = []
        self._includes: List[str] = []
        self._definitions: List[str] = []

    def adapts(self, compiler: Pathlike) -> bool:  # noqa: D400
        """$compiler --version"""
        driver = CLIDriver(compiler)
        output = driver.run(["--version"], text=True, capture_output=True)
        if output.returncode != 0:
            return False
        else:
            # Clang is GCC-compatitable
            if "gcc" in output.stdout or "clang version" in output.stdout:
                self.program = driver
                return True
            else:
                return False

    def _gen_link_directory(self, directory: pathlib.Path) -> None:
        self._link_dirs.append("-L{}".format(directory))

    def _gen_link_library(self, name: str) -> None:
        self._links.append("-l{}".format(name))

    def _gen_include_directory(self, dir: pathlib.Path) -> None:
        self._includes.append("-I{}".format(dir))

    def _gen_definition(self, key: str, value: Optional[str]) -> None:
        flag = "-D{}".format(key)
        if value:
            flag += "={}".format(value)
        self._definitions.append(flag)

    # Actions
    def compile_obj(
        self, src: Pathlike, obj: Pathlike
    ) -> subprocess.CompletedProcess:  # noqa: D400
        """$cc -fPIC -Wall -O3 -pthread ... -o obj -c src"""
        if not self.program:
            raise RuntimeError("CC hasn't been adapted.")
        args: List[str] = []
        args.append("-fPIC")
        args.append("-Wall")
        args.append("-O3")
        args.append("-pthread")
        args.extend(self._includes)
        args.extend(self._definitions)
        args.append("-o")
        args.append(str(obj))
        args.append("-c")
        args.append(str(src))
        return self.program.run(args, text=True, capture_output=True)

    def link_shared(
        self, objs: List[Pathlike], out: Pathlike
    ) -> subprocess.CompletedProcess:  # noqa: D400
        """$cc -shared -pthread -o out objs"""
        if not self.program:
            raise RuntimeError("CC hasn't been adapted.")
        args: List[str] = []
        args.append("-shared")
        args.append("-o")
        args.append("-pthread")
        args.append(str(out))
        args.extend(map(str, objs))
        return self.program.run(args, text=True, capture_output=True)

    def link_executable(
        self, objs: List[Pathlike], out: Pathlike
    ) -> subprocess.CompletedProcess:  # noqa: D400
        """$cc -pthread ... -o out objs"""
        if not self.program:
            raise RuntimeError("CC hasn't been adapted.")
        args: List[str] = []
        args.append("-pthread")
        args.extend(self._link_dirs)
        args.extend(self._links)
        args.append("-o")
        args.append(str(out))
        args.extend(map(str, objs))
        return self.program.run(args, text=True, capture_output=True)
