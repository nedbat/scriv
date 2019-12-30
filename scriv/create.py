"""Creating entries."""

import datetime
import os.path
import re

import jinja2

from scriv.config import Config
from scriv.format import get_format_tools
from scriv.gitinfo import current_branch_name, user_nick


def new_entry_path(config: Config) -> str:
    """
    Return the file path for a new entry.
    """
    file_name = "{:%Y%m%d}_{}".format(datetime.datetime.now(), user_nick())
    branch_name = current_branch_name()
    if branch_name and branch_name != "master":
        branch_name = branch_name.rpartition("/")[-1]
        branch_name = re.sub(r"[^a-zA-Z0-9_]", "_", branch_name)
        file_name += "_{}".format(branch_name)
    file_name += ".{}".format(config.format)
    file_path = os.path.join(config.entry_directory, file_name)
    return file_path


def new_entry_contents(config: Config) -> str:
    """Produce the initial contents of a scriv entry."""
    tools = get_format_tools(config)
    return jinja2.Template(tools.NEW_TEMPLATE).render(config=config)
