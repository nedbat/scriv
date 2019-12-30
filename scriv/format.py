"""Dispatcher for format-based knowledge."""

from scriv.config import Config


class FormatTools:
    """Methods and data about specific formats."""

    NEW_TEMPLATE = ""


def get_format_tools(config: Config) -> FormatTools:
    """Return the FormatTools to use."""
    if config.format == "rst":
        from scriv import format_rst  # pylint: disable=cyclic-import

        return format_rst.RstTools()
    elif config.format == "md":
        from scriv import format_md  # pylint: disable=cyclic-import

        return format_md.MdTools()
    else:
        raise Exception("Unknown format: {}".format(config.format))
