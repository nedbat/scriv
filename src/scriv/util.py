"""Miscellanous helpers."""

import collections
from typing import Dict, Optional, Sequence, Tuple, TypeVar

T = TypeVar("T")
K = TypeVar("K")


def order_dict(
    d: Dict[Optional[K], T], keys: Sequence[Optional[K]]
) -> Dict[Optional[K], T]:
    """
    Produce an OrderedDict of `d`, but with the keys in `keys` order.

    Keys in `d` that don't appear in `keys` will be at the end in an
    undetermined order.
    """
    with_order = collections.OrderedDict()
    to_insert = set(d)
    for k in keys:
        if k not in to_insert:
            continue
        with_order[k] = d[k]
        to_insert.remove(k)

    for k in to_insert:
        with_order[k] = d[k]

    return with_order


def cut_at_line(text: str, marker: str) -> Tuple[str, str]:
    """
    Split text into two parts: up to the line with marker, and lines after.

    If `marker` isn't in the text, return ("", text)
    """
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if marker in line:
            return "".join(lines[: i + 1]), "".join(lines[i + 1 :])
    return ("", text)
