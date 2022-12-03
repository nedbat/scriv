"""
Find literals in various kinds of files.
"""

import ast
import os.path
from typing import Any, MutableMapping, Optional

try:
    import tomli
except ImportError:  # pragma: no cover
    tomli = None  # type: ignore

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore


def find_literal(file_name: str, literal_name: str) -> Optional[str]:
    """
    Look inside a file for a literal value, and return it.

    Returns:
        The string value found, or None if not found.

    """
    ext = os.path.splitext(file_name)[-1]
    if ext == ".py":
        with open(file_name, encoding="utf-8") as f:
            node = ast.parse(f.read())
        return PythonLiteralFinder().find(node, literal_name)
    elif ext == ".toml":
        if tomli is None:
            msg = (
                "Can't read {!r} without TOML support. "
                + "Install with [toml] extra"
            ).format(file_name)
            raise Exception(msg)
        with open(file_name, encoding="utf-8") as f:
            data = tomli.loads(f.read())
        return find_nested_value(data, literal_name)
    elif ext in (".yml", ".yaml"):
        if yaml is None:
            msg = (
                "Can't read {!r} without YAML support. "
                + "Install with [yaml] extra"
            ).format(file_name)
            raise Exception(msg)
        with open(file_name, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return find_nested_value(data, literal_name)
    else:
        raise Exception(f"Can't read literals from files like {file_name!r}")


class PythonLiteralFinder(ast.NodeVisitor):
    """
    A NodeVisitor that will find assignments in Python code.
    """

    def __init__(self):  # noqa: D107
        super().__init__()
        self.name = None
        self.value = None

    def find(self, node: ast.AST, name: str) -> Optional[str]:
        """
        Search the AST in `node`, looking for an assignment to `name`.

        Returns:
            The string value found, or None if not found.

        """
        self.name = name
        self.value = None
        self.visit(node)
        return self.value

    def visit_Assign(self, node) -> None:  # noqa: D102 (inherited docstring)
        for target in node.targets:
            if isinstance(target, ast.Name):
                if target.id == self.name:
                    self.check_value(node.value)

    def check_value(self, value):
        """
        Check a value node to see if it's a string constant.

        If it is, save the string value as `self.value`.
        """
        ast_Constant = getattr(ast, "Constant", None)
        if ast_Constant and isinstance(value, ast_Constant):
            if isinstance(value.value, str):
                self.value = value.value
        elif isinstance(value, ast.Str):
            self.value = value.s


def find_nested_value(
    data: MutableMapping[str, Any], name: str
) -> Optional[str]:
    """
    Use a period-separated name to traverse a dictionary.

    Only string values are supported.
    """
    current_object = data
    for key in name.split("."):
        try:
            current_object = current_object[key]
        except (KeyError, TypeError):
            return None

    if isinstance(current_object, str):
        return current_object
    return None
