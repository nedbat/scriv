"""Scriv configuration."""

import attr


@attr.s(auto_attribs=True)
class Config:
    entry_directory: str = "changelog.d"
    format: str = "rst"


def read_config() -> Config:
    """
    Read the configuration to use.
    """
    return Config()
