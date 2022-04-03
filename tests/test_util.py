"""Tests of scriv/util.py"""

import pytest

from scriv.util import extract_version, is_prerelease_version


@pytest.mark.parametrize(
    "text, ver",
    [
        ("v1.2.3 -- 2022-04-06", "v1.2.3"),
        ("Oops, fixed on 6/16/2021.", None),
        ("2022-Apr-06: 12.3-alpha0 finally", "12.3-alpha0"),
        ("2.7.19beta1, 2022-04-08", "2.7.19beta1"),
    ],
)
def test_extract_version(text, ver):
    assert extract_version(text) == ver


@pytest.mark.parametrize(
    "version",
    [
        "v1.2.3",
        "17.4.1.3",
    ],
)
def test_is_not_prerelease_version(version):
    assert not is_prerelease_version(version)


@pytest.mark.parametrize(
    "version",
    [
        "v1.2.3a1",
        "17.4.1.3-beta.2",
    ],
)
def test_is_prerelease_version(version):
    assert is_prerelease_version(version)
