"""Scriv configuration."""

import configparser
import re
from typing import Any, List

import attr


@attr.s
class Config:
    """
    All the settable options for Scriv.
    """

    entry_directory = attr.ib(type=str, default="changelog.d")
    format = attr.ib(type=str, default="rst")
    categories = attr.ib(type=list, default=["Removed", "Added", "Changed", "Deprecated", "Fixed", "Security"])
    output_file = attr.ib(type=str, default="CHANGELOG.rst")
    insert_marker = attr.ib(type=str, default="scriv:insert-here")


def convert_list(val: str) -> List[str]:
    """
    Convert a string value from a config into a list of strings.

    Elements can be separated by commas or newlines.
    """
    vals = re.split(r"[\n,]", val)
    vals = [v.strip() for v in vals]
    vals = [v for v in vals if v]
    return vals


def read_config() -> Config:
    """
    Read the configuration to use.

    Configuration will be read from .scrivrc, setup.cfg, or tox.ini.
    The section can be named ``[scriv]`` or ``[tool.scriv]``.

    """
    config = Config()
    parser = configparser.ConfigParser()
    parser.read([".scrivrc", "setup.cfg", "tox.ini"])
    section_names = ["scriv", "tool.scriv"]
    section_name = next((name for name in section_names if parser.has_section(name)), None)
    if section_name:
        for attrdef in attr.fields(Config):
            try:
                val = parser[section_name][attrdef.name]  # type: Any
            except KeyError:
                pass
            else:
                if attrdef.type is list:
                    val = convert_list(val)
                setattr(config, attrdef.name, val)
    return config
