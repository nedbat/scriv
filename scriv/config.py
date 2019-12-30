"""Scriv configuration."""

import attr


@attr.s
class Config:
    """
    All the settable options for Scriv.
    """

    entry_directory = attr.ib(type=str, default="changelog.d")
    format = attr.ib(type=str, default="rst")
    categories = attr.ib(type=list, default=["Removed", "Added", "Changed", "Deprecated", "Fixed", "Security"])


def read_config() -> Config:
    """
    Read the configuration to use.
    """
    return Config()
