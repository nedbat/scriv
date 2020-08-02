"""
Find literals in various kinds of files.
"""

import ast
import os.path
from typing import Optional


def find_literal(file_name: str, literal_name: str) -> Optional[str]:
    """
    Look inside a file for a literal value, and return it.

    Returns:
        The string value found, or None if not found.

    """
    ext = os.path.splitext(file_name)[-1]
    if ext == ".py":
        with open(file_name) as f:
            node = ast.parse(f.read())
        return PythonLiteralFinder().find(node, literal_name)
    else:
        raise Exception("Can't read literals from files like {!r}".format(file_name))


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

    if hasattr(ast, "Constant"):

        def check_value(self, value):
            """
            Check a value node to see if it's a string constant.

            If it is, save the string value as `self.value`.
            This is the 3.8+ implementation.
            """
            if isinstance(value, ast.Constant):
                if isinstance(value.value, str):
                    self.value = value.value

    else:

        def check_value(self, value):
            """
            Check a value node to see if it's a string constant.

            If it is, save the string value as `self.value`.
            This is the pre-3.8 implementation.
            """
            if isinstance(value, ast.Str):
                self.value = value.s
