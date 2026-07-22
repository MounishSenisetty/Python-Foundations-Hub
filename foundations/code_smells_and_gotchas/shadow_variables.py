"""Avoiding variable names that shadow Python built-ins.

Names like ``list``, ``dict``, ``str``, ``type``, ``id``, and ``input``
are ordinary identifiers, so Python happily lets you rebind them::

    list = [1, 2, 3]        # smell: the list() constructor is now gone
    other = list("abc")     # TypeError: 'list' object is not callable

The bug rarely bites on the line that shadows — it bites dozens of lines
later, with an error message that points at innocent code. Every function
here is the *refactored* version of code that originally shadowed a
built-in, with the offending name recorded in its docstring.

Naming strategies used, in order of preference:

1. A more descriptive name (``items``, ``mapping``, ``text``).
2. A domain-specific name (``user_id``, ``file_format``).
3. A trailing underscore (``type_``) — PEP 8's convention of last resort.
"""

from __future__ import annotations

from typing import Dict, Hashable, Iterable, List, Sequence, Tuple


def deduplicate(items: Iterable[Hashable]) -> List[Hashable]:
    """Remove duplicates while preserving first-seen order.

    Refactor note: the original signature was ``def deduplicate(list)``,
    which broke the ``list(...)`` constructor for the whole function body.

    Args:
        items: Iterable of hashable values.

    Returns:
        The distinct values in first-appearance order.
    """
    seen: Dict[Hashable, None] = {}
    for item in items:
        seen.setdefault(item)
    return list(seen)


def merge_mappings(base: Dict[str, int], overrides: Dict[str, int]) -> Dict[str, int]:
    """Merge two dicts, with ``overrides`` winning on key conflicts.

    Refactor note: originally ``def merge(dict, overrides)``, shadowing
    the ``dict`` constructor used in the return statement below.

    Args:
        base: Default key/value pairs.
        overrides: Pairs that take precedence over ``base``.

    Returns:
        A new dict; neither input is modified.
    """
    merged = dict(base)
    merged.update(overrides)
    return merged


def normalize_text(text: str) -> str:
    """Collapse internal whitespace and strip the ends of a string.

    Refactor note: originally ``def normalize(str)``, which made the
    ``str(...)`` conversion (and ``isinstance(x, str)`` checks) blow up
    anywhere inside the function.

    Args:
        text: The raw string to clean.

    Returns:
        The cleaned string with single spaces between words.
    """
    return " ".join(text.split())


def partition_by_type(
    values: Sequence[object], type_: type
) -> Tuple[List[object], List[object]]:
    """Split values into those matching a type and everything else.

    Refactor note: the parameter really is best described as a "type", so
    PEP 8's trailing-underscore convention (``type_``) keeps the built-in
    ``type`` callable while preserving the natural name.

    Args:
        values: The values to partition.
        type_: The class to match with ``isinstance``.

    Returns:
        A ``(matching, rest)`` pair of lists in input order.
    """
    matching: List[object] = []
    rest: List[object] = []
    for value in values:
        (matching if isinstance(value, type_) else rest).append(value)
    return matching, rest


if __name__ == "__main__":
    print(deduplicate([3, 1, 3, 2, 1]))
    print(merge_mappings({"retries": 3, "timeout": 30}, {"timeout": 60}))
    print(normalize_text("  too   many    spaces "))
    print(partition_by_type([1, "a", 2.0, "b", 3], str))
