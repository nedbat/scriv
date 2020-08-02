"""Tests of literals.py"""

import pytest

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
    with open("foo.py", "w") as f:
        f.write(PYTHON_CODE)
    assert find_literal("foo.py", name) == value
