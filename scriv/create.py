"""Creating entries."""

import datetime
import os.path
import re

import jinja2

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


NEW_TEMPLATE = """\
.. A new scriv entry.
..
.. Uncomment the header that is right (remove the leading dots).

{% for cat in config.categories -%}
.. {{ cat }}
.. {{ '=' * (cat|length) }}
..
.. - A bullet item for the {{ cat }} category.
..
{% endfor -%}
"""


def new_entry_contents(config: Config) -> str:
    """Produce the initial contents of a scriv entry."""
    return jinja2.Template(NEW_TEMPLATE).render(config=config)
