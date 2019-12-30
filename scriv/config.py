"""Scriv configuration."""

from typing import List

import attr


@attr.s(auto_attribs=True)
class Config:
    """
    All the settable options for Scriv.
    """

    entry_directory: str = "changelog.d"
    format: str = "rst"
    categories: List[str] = [
        "Removed",
        "Added",
        "Changed",
        "Deprecated",
        "Fixed",
        "Security",
    ]


def read_config() -> Config:
    """
    Read the configuration to use.
    """
    return Config()
