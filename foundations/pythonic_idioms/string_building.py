"""Efficient string construction with ``str.join``.

Python strings are immutable, so every ``result += piece`` inside a loop
copies the entire accumulated string — quadratic O(n²) work overall. The
idiomatic fix is to collect the pieces in a list and glue them together
once with ``str.join``, which is linear.

Both styles are implemented side by side here so the difference can be
benchmarked (see ``foundations/performance_profiling/benchmarking_timeit.py``)
and asserted equivalent in tests.

Example:
    >>> join_lines(["a", "b"]) == concat_lines_slow(["a", "b"])
    True
"""

from __future__ import annotations

from typing import Iterable, Mapping


def concat_lines_slow(lines: Iterable[str]) -> str:
    """Join lines with ``+=`` concatenation — the anti-pattern.

    Kept only as the "before" picture: each iteration copies everything
    accumulated so far, so runtime grows quadratically with input size.

    Args:
        lines: Iterable of text lines without trailing newlines.

    Returns:
        The lines joined by newline characters.
    """
    result = ""
    for line in lines:
        if result:
            result += "\n"
        result += line
    return result


def join_lines(lines: Iterable[str]) -> str:
    """Join lines with ``str.join`` — the idiomatic, linear approach.

    Args:
        lines: Iterable of text lines without trailing newlines.

    Returns:
        The lines joined by newline characters.
    """
    return "\n".join(lines)


def build_csv_row(fields: Iterable[object], separator: str = ",") -> str:
    """Render one delimited row from arbitrary field values.

    ``str.join`` only accepts strings, so non-string fields are converted
    explicitly — hiding an implicit ``str()`` call is a common source of
    surprising ``TypeError``s.

    Args:
        fields: Values for the row; each is converted with ``str``.
        separator: Delimiter placed between fields.

    Returns:
        The delimited row as a single string.
    """
    return separator.join(str(field) for field in fields)


def format_report(title: str, stats: Mapping[str, int]) -> str:
    """Compose a small multi-line report from parts.

    Demonstrates the standard pattern for building larger documents:
    accumulate logical chunks in a list, then ``join`` exactly once at
    the end.

    Args:
        title: Heading line for the report.
        stats: Mapping of metric names to integer values.

    Returns:
        The formatted report, one metric per line under the title.
    """
    parts = [title, "=" * len(title)]
    for name, value in stats.items():
        parts.append(f"{name}: {value}")
    return "\n".join(parts)


if __name__ == "__main__":
    print(format_report("Build Summary", {"passed": 42, "failed": 0}))
    print(build_csv_row(["id", 7, 3.5]))
