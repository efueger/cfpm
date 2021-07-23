"""Logging utilities for cfpm."""

import click
import logging
from typing import Callable


# Originally comes from click-log
class ClickHandler(logging.Handler):
    """Logging handler that uses click.echo."""

    def __init__(self, use_stderr: bool = True):
        """
        Initialize the handler.

        Args:
            use_stderr: If set to true, the logger will print to stderr instead
                of stdout.
        """
        self._use_stderr = use_stderr
        logging.Handler.__init__(self)

    def emit(self, record):
        """Emit a record."""
        try:
            msg = self.format(record)
            level = record.levelname.lower()  # noqa: F841
            click.echo(msg, err=self._use_stderr)
        except Exception:
            self.handleError(record)


class ColorFormatter(logging.Formatter):
    """Colored formatter for logging."""

    colors = {
        "error": dict(fg="red"),
        "exception": dict(fg="red"),
        "critical": dict(fg="red"),
        "debug": dict(fg="blue"),
        "warning": dict(fg="yellow"),
    }

    def format(self, record):
        """Format the specified record as text."""
        if not record.exc_info:
            level = record.levelname.lower()
            msg = record.getMessage()
            if level in self.colors:
                prefix = click.style(
                    "[{}] ".format(level.upper()), **self.colors[level]
                )
                msg = "\n".join(prefix + x for x in msg.splitlines())
            return msg
        return logging.Formatter.format(self, record)


def simple_verbosity_option(
    logger: logging.Logger = None, *names: str, **kwargs
) -> Callable:
    """
    Add a `--verbosity, -v` option to the decorated command.

    Name can be configured through ``*names``. Keyword arguments are passed to
    the underlying ``click.option`` decorator.
    """
    if not names:
        names = ("--verbosity", "-v")

    kwargs.setdefault("default", "INFO")
    kwargs.setdefault("metavar", "LVL")
    kwargs.setdefault("expose_value", False)
    kwargs.setdefault(
        "help",
        "Change verbosity level. Either CRITICAL, ERROR, WARNING, INFO or "
        "DEBUG.",
    )
    kwargs.setdefault("is_eager", True)

    def decorator(f: Callable) -> Callable:
        def _set_level(ctx, param, value):
            x = getattr(logging, value.upper(), None)
            if x is None:
                raise click.BadParameter(
                    "Must be CRITICAL, ERROR, WARNING, INFO or DEBUG, not {}."
                )
            logger.setLevel(x)

        return click.option(*names, callback=_set_level, **kwargs)(f)

    return decorator


def logger_basic_config(logger: logging.Logger) -> None:
    """
    Configure a basic colored logger to stderr.

    Args:
        logger: The logger to configure.
    """
    handler = ClickHandler()
    handler.setFormatter(ColorFormatter())
    logger.handlers = [handler]


logger = logging.getLogger("cfpm")
logger_basic_config(logger)
