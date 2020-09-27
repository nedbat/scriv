"""Test the code in scriv.extras"""

import scriv.extras


def test_extras_without():
    # pylint: disable=reimported,import-outside-toplevel
    from scriv.extras import toml as toml1

    with scriv.extras.without("toml"):
        from scriv.extras import toml as toml2
    from scriv.extras import toml as toml3

    assert toml1 is toml3 is not None
    assert toml2 is None
