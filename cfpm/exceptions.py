"""Exceptions raised by cfpm."""


class BadConfigurationError(ValueError):
    """Error caused by user's bad configuration on cfpm."""


class ExternalProgramError(RuntimeError):
    """Error caused by external command line programs."""
