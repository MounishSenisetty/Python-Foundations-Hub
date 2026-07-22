"""The mutable default argument trap and its standard fixes.

Default argument values are evaluated **once**, when the ``def`` statement
runs — not on every call. A mutable default such as ``[]`` or ``{}`` is
therefore a single shared object that silently accumulates state across
calls.

This module keeps a deliberately broken function around so the behaviour
can be demonstrated and tested, alongside the two standard fixes:

* the ``None`` sentinel, when ``None`` is not itself a meaningful value;
* a private module-level sentinel object, when it is.

Example:
    >>> append_to(1)
    [1]
    >>> append_to(2)  # a fresh list every call — no leaked state
    [2]
"""

from __future__ import annotations

from typing import Any, List, Optional


def append_to_shared(item: int, bucket: List[int] = []) -> List[int]:  # noqa: B006
    """Append to a list default — the classic bug, preserved on purpose.

    The default list is created once at definition time, so every call
    that omits ``bucket`` appends to the *same* list.

    Args:
        item: Value to append.
        bucket: Target list; defaults to one shared instance (the bug).

    Returns:
        The bucket after appending — including items from earlier calls
        when the shared default is used.
    """
    bucket.append(item)
    return bucket


def append_to(item: int, bucket: Optional[List[int]] = None) -> List[int]:
    """Append to a list, creating a fresh one per call — the fix.

    The ``None`` sentinel moves list creation into the function body,
    which runs on every call.

    Args:
        item: Value to append.
        bucket: Target list, or ``None`` to start a new one.

    Returns:
        The bucket after appending.
    """
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket


_MISSING = object()


def report_value(value: Any = _MISSING) -> str:
    """Distinguish "argument omitted" from "``None`` passed explicitly".

    When ``None`` is a legitimate input, it cannot double as the sentinel.
    A private ``object()`` instance is unique by identity, so an ``is``
    check detects omission unambiguously.

    Args:
        value: Any value, including ``None``. Omit it entirely to get the
            "no value" report.

    Returns:
        A short description of what was received.
    """
    if value is _MISSING:
        return "no value provided"
    return f"received {value!r}"


if __name__ == "__main__":
    print(append_to_shared(1), append_to_shared(2))  # [1, 2] [1, 2] — shared!
    print(append_to(1), append_to(2))  # [1] [2] — isolated
    print(report_value(), "|", report_value(None))
