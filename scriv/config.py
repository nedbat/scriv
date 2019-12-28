"""Scriv configuration."""

import attr


@attr.s(auto_attribs=True)
class Config:
    entry_directory: str = "changelog.d"
