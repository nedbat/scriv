"""Tests of literals.py"""

import os
import sys

import pytest

import scriv.literals
from scriv.exceptions import ScrivException
from scriv.literals import find_literal
from scriv.optional import tomllib, yaml


def test_no_extras_craziness():
    # Check that if we're testing no-extras we didn't get the modules, and if we
    # aren't, then we did get the modules.
    if os.getenv("SCRIV_TEST_NO_EXTRAS", ""):
        if sys.version_info < (3, 11):
            assert tomllib is None
        assert yaml is None
    else:
        assert tomllib is not None
        assert yaml is not None


PYTHON_CODE = """\
# A string we should get.
version = "1.2.3"

typed_version: Final[str] = "2.3.4"

thing1.attr = "3.4.5"
thing2.attr: str = "4.5.6"

# Numbers don't count.
how_many = 123

# Complex names don't count.
a_thing[0] = 123

# Non-constant values don't count.
a_thing_2 = func(1)

# Non-strings don't count.
version = compute_version(1)

if 1:
    # It's OK if they are inside other structures.
    also = "xyzzy"
    but = '''hello there'''

def foo():
    # Even in a function is OK, but why would you do that?
    somewhere_else = "this would be an odd place to get the string"
"""


@pytest.mark.parametrize(
    "name, value",
    [
        ("version", "1.2.3"),
        ("typed_version", "2.3.4"),
        ("also", "xyzzy"),
        ("but", "hello there"),
        ("somewhere_else", "this would be an odd place to get the string"),
        ("a_thing_2", None),
        ("how_many", None),
    ],
)
def test_find_python_literal(name, value, temp_dir):
    with open("foo.py", "w", encoding="utf-8") as f:
        f.write(PYTHON_CODE)
    assert find_literal("foo.py", name) == value


def test_unknown_file_type(temp_dir):
    with open("what.xyz", "w", encoding="utf-8") as f:
        f.write("Hello there!")
    expected = "Can't read literals from files like 'what.xyz'"
    with pytest.raises(ScrivException, match=expected):
        find_literal("what.xyz", "hi")


TOML_LITERAL = """
version = "1"

[tool.poetry]
version = "2"

[metadata]
version = "3"
objects = { version = "4", other = "ignore" }

[bogus]
# Non-strings don't count.
number = 123
boolean = true
lists = [1, 2, 3]
bad_type = nan

# Sections don't count.
[bogus.section]

"""


@pytest.mark.skipif(tomllib is None, reason="No TOML support installed")
@pytest.mark.parametrize(
    "name, value",
    [
        ("version", "1"),
        ("tool.poetry.version", "2"),
        ("tool.poetry.version.too.deep", None),
        ("metadata.version", "3"),
        ("metadata.objects.version", "4"),
        ("bogus", None),
        ("bogus.number", None),
        ("bogus.boolean", None),
        ("bogus.lists", None),
        ("bogus.bad_type", None),
        ("bogus.section", None),
        ("bogus.section.too.deep", None),
    ],
)
def test_find_toml_literal(name, value, temp_dir):
    with open("foo.toml", "w", encoding="utf-8") as f:
        f.write(TOML_LITERAL)
    assert find_literal("foo.toml", name) == value


def test_find_toml_literal_fail_if_unavailable(monkeypatch):
    monkeypatch.setattr(scriv.literals, "tomllib", None)
    with pytest.raises(
        ScrivException, match="Can't read .+ without TOML support"
    ):
        find_literal("foo.toml", "fail")


YAML_LITERAL = """\
---
version: 1.2.3

myVersion:
  MAJOR: 2
  MINOR: 3
  PATCH: 5

myproduct:
  version: [mayor=5, minor=6, patch=7]
  versionString: "8.9.22"
...
"""


@pytest.mark.skipif(yaml is None, reason="No YAML support installed")
@pytest.mark.parametrize(
    "name, value",
    [
        ("version", "1.2.3"),
        ("myproduct.versionString", "8.9.22"),
        ("myproduct.version", None),
        ("myVersion", None),
    ],
)
def test_find_yaml_literal(name, value, temp_dir):
    with open("foo.yml", "w", encoding="utf-8") as f:
        f.write(YAML_LITERAL)
    assert find_literal("foo.yml", name) == value


def test_find_yaml_literal_fail_if_unavailable(monkeypatch):
    monkeypatch.setattr(scriv.literals, "yaml", None)
    with pytest.raises(
        ScrivException, match="Can't read .+ without YAML support"
    ):
        find_literal("foo.yml", "fail")


CFG_LITERAL = """\

[metadata]
name = myproduct
version = 1.2.3
url = https://github.com/nedbat/scriv
description = A nice description
long_description = file: README.md
long_description_content_type = text/markdown
license = MIT

[options]
zip_safe = false
include_package_data = true

[bdist_wheel]
universal = true

[coverage:report]
show_missing = true

[flake8]
max-line-length = 99
doctests = True
exclude =  .git, .eggs, __pycache__, tests/, docs/, build/, dist/
"""


@pytest.mark.parametrize(
    "name, value",
    [
        ("metadata.version", "1.2.3"),
        ("options.zip_safe", "false"),
        ("coverage:report", None),  # find_literal only supports string values
        ("metadata.myVersion", None),
        ("unexisting", None),
    ],
)
def test_find_cfg_literal(name, value, temp_dir):
    with open("foo.cfg", "w", encoding="utf-8") as f:
        f.write(CFG_LITERAL)
    assert find_literal("foo.cfg", name) == value


CABAL_LITERAL = """\
cabal-version:      3.0
name:               pkg
version:            1.2.3
"""


@pytest.mark.parametrize(
    "name, value",
    [
        ("version", "1.2.3"),
    ],
)
def test_find_cabal_literal(name, value, temp_dir):
    with open("foo.cabal", "w", encoding="utf-8") as f:
        f.write(CABAL_LITERAL)
    assert find_literal("foo.cabal", name) == value
