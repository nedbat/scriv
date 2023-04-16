"""Tests of scriv/util.py"""

import pytest

from scriv.util import Version, partition_lines


@pytest.mark.parametrize(
    "text, ver",
    [
        ("v1.2.3 -- 2022-04-06", "v1.2.3"),
        ("Oops, fixed on 6/16/2021.", None),
        ("2022-Apr-06: 12.3-alpha0 finally", "12.3-alpha0"),
        ("2.7.19beta1, 2022-04-08", "2.7.19beta1"),
    ],
)
def test_version_from_text(text, ver):
    if ver is not None:
        ver = Version(ver)
    assert Version.from_text(text) == ver


@pytest.mark.parametrize(
    "version",
    [
        "v1.2.3",
        "17.4.1.3",
    ],
)
def test_is_not_prerelease_version(version):
    assert not Version(version).is_prerelease()


@pytest.mark.parametrize(
    "version",
    [
        "v1.2.3a1",
        "17.4.1.3-beta.2",
    ],
)
def test_is_prerelease_version(version):
    assert Version(version).is_prerelease()


@pytest.mark.parametrize(
    "text, result",
    [
        ("one\ntwo\nthree\n", ("one\ntwo\nthree\n", "", "")),
        ("oXe\ntwo\nthree\n", ("", "oXe\n", "two\nthree\n")),
        ("one\ntXo\nthree\n", ("one\n", "tXo\n", "three\n")),
        ("one\ntwo\ntXree\n", ("one\ntwo\n", "tXree\n", "")),
        ("one\ntXo\ntXree\n", ("one\n", "tXo\n", "tXree\n")),
    ],
)
def test_partition_lines(text, result):
    assert partition_lines(text, "X") == result
