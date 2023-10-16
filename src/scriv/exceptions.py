"""Specialized exceptions for scriv."""

import functools
import sys


class ScrivException(Exception):
    """Any exception raised by scriv."""


def scriv_command(func):
    """Decorate a command so that ScrivException ends cleanly (no traceback)."""

    @functools.wraps(func)
    def _wrapped(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except ScrivException as exc:
            sys.exit(str(exc))

    return _wrapped
