"""
Third-party modules that might or might not be available.
"""

# pylint: disable=unused-import

from types import ModuleType
from typing import Optional

tomllib: Optional[ModuleType]

try:
    try:
        import tomllib  # type: ignore[no-redef]
    except ModuleNotFoundError:
        import tomli as tomllib  # type: ignore[no-redef]
except ImportError:
    tomllib = None


yaml: Optional[ModuleType]

try:
    import yaml  # type: ignore[no-redef]
except ImportError:
    yaml = None
