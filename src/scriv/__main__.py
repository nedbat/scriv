"""Enable 'python -m scriv'."""

from .cli import cli

# This type: pragma can be removed when click 8.1.6 is out, to fix
# https://github.com/pallets/click/issues/2558.
cli(prog_name="scriv")  # type: ignore[misc]
