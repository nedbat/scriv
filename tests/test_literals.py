"""Tests of literals.py"""

import pytest

import scriv.literals
from scriv.literals import find_literal

PYTHON_CODE = """\
# A string we should get.
version = "1.2.3"

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
    with pytest.raises(Exception, match=expected):
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
    monkeypatch.setattr(scriv.literals, "tomli", None)
    with pytest.raises(Exception, match="Can't read .+ without TOML support"):
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
    with pytest.raises(Exception, match="Can't read .+ without YAML support"):
        find_literal("foo.yml", "fail")
