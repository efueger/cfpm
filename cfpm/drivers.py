"""Command line program drivers."""


class CLIDriver:
    """A generic driver to exectute command line programs."""

    def __init__(self, program_name: str):
        """
        Initialize the driver.

        Args:
            program_name: A string, stands for the cli exectuable. Can be
                either a name or a path.
        """
        raise NotImplementedError("TODO!")
