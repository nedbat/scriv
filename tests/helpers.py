"""Testing helpers."""

from unittest import mock


def without_module(using_module, missing_module_name: str):
    """
    Hide a module for testing.

    Use this in a test function to make an optional module unavailable during
    the test::

        with without_module(scriv.something, 'toml'):
            use_toml_somehow()

    Arguments:
        using_module: a module in which to hide `missing_module_name`.
        missing_module_name: the name of the module to hide.

    """
    return mock.patch.object(using_module, missing_module_name, None)


def check_logs(caplog, expected):
    """
    Compare log records from caplog.

    Only caplog records from a logger mentioned in expected are considered.
    """
    logger_names = {r[0] for r in expected}
    records = [r for r in caplog.record_tuples if r[0] in logger_names]
    assert records == expected
