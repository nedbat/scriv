"""
Third-party modules that might or might not be available.
"""

# pylint: disable=unused-import

from types import ModuleType

tomllib: ModuleType | None

try:
    try:
        import tomllib  # type: ignore[no-redef]
    except ModuleNotFoundError:
        import tomli as tomllib  # type: ignore[no-redef]
except ImportError:
    tomllib = None


yaml: ModuleType | None

try:
    import yaml  # type: ignore[no-redef]
except ImportError:
    yaml = None
