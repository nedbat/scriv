"""Scriv configuration."""

import configparser
import re
from pathlib import Path
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
    # The character to use for header underlines in rst files
    rst_header_char = attr.ib(type=str, default="-")


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

    Configuration will be read from setup.cfg, tox.ini, or
    changelog.d/scriv.ini.  If setup.cfg or tox.ini defines
    a new entry_directory, then scriv.ini is read from there.

    The section can be named ``[scriv]`` or ``[tool.scriv]``.

    """
    config = Config()
    for configfile in ["setup.cfg", "tox.ini"]:
        read_one_config(config, configfile)
    read_one_config(config, str(Path(config.entry_directory) / "scriv.ini"))
    return config


def read_one_config(config: Config, configfile: str) -> None:
    """
    Read one configuration file, adding values to `config`.
    """
    parser = configparser.ConfigParser()
    parser.read(configfile)
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
