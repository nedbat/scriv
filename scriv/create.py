"""Creating entries."""

import datetime
import os.path
import re

from scriv.config import Config
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
