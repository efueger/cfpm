"""Object representing projects and targets."""

from typing import Dict, List


class Build:
    """The object representing a build."""

    def __init__(self, config: Dict):
        """Initialize the build with all the configurations."""
        pass

    def build(self) -> None:
        """Acturally build the project."""
        pass


class GenericTarget:
    """An abstract class representing a target."""

    pass


class Project:
    """The object representing a project."""

    def __init__(self) -> None:
        """Initialize the project."""
        self.targets: List[GenericTarget] = []

    def add_target(self, target: GenericTarget):
        """Add a target to the project."""
        self.targets.append(target)
