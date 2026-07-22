"""Pure functions, functional transformations, and composition.

A *pure* function computes its result solely from its inputs and touches
nothing outside itself — no globals, no mutation of arguments, no I/O.
Pure functions are trivially testable and safe to compose, which is what
this module does: small pure transforms are chained into pipelines with
``compose`` and ``pipeline``.

On ``map``/``filter`` versus comprehensions: both are shown, and the
comprehension versions are preferred for readability when the transform
is an inline expression. ``map``/``filter`` shine when a named function
already exists — then they read as a sentence.

Example:
    >>> pipeline(3, [double, increment])
    7
"""

from __future__ import annotations

import functools
from typing import Callable, Iterable, List, Sequence, TypeVar

T = TypeVar("T")

Transform = Callable[[T], T]


def double(number: int) -> int:
    """Return twice the input.

    Args:
        number: Any integer.

    Returns:
        ``number * 2``.
    """
    return number * 2


def increment(number: int) -> int:
    """Return the input plus one.

    Args:
        number: Any integer.

    Returns:
        ``number + 1``.
    """
    return number + 1


def is_positive(number: int) -> bool:
    """Report whether a number is strictly greater than zero.

    Args:
        number: Any integer.

    Returns:
        ``True`` for positive numbers.
    """
    return number > 0


def doubled_positives_functional(numbers: Iterable[int]) -> List[int]:
    """Double the positive numbers using ``map`` and ``filter``.

    Reads well precisely because ``double`` and ``is_positive`` are
    existing named functions — no ``lambda`` needed.

    Args:
        numbers: Any iterable of integers.

    Returns:
        The doubled positive values, in input order.
    """
    return list(map(double, filter(is_positive, numbers)))


def doubled_positives_comprehension(numbers: Iterable[int]) -> List[int]:
    """Double the positive numbers using a list comprehension.

    Equivalent to ``doubled_positives_functional``; the comprehension
    keeps the transform and the predicate visible in one expression.

    Args:
        numbers: Any iterable of integers.

    Returns:
        The doubled positive values, in input order.
    """
    return [number * 2 for number in numbers if number > 0]


def compose(*functions: Transform) -> Transform:
    """Combine unary functions right-to-left, as in mathematics.

    ``compose(f, g)(x)`` computes ``f(g(x))``.

    Args:
        *functions: Unary functions over a common type. With no
            arguments, the identity function is returned.

    Returns:
        A single function applying every input function, rightmost first.
    """
    return functools.reduce(
        lambda outer, inner: lambda value: outer(inner(value)),
        functions,
        lambda value: value,
    )


def pipeline(value: T, steps: Sequence[Callable[[T], T]]) -> T:
    """Thread a value through steps left-to-right, in reading order.

    The same idea as ``compose`` but ordered the way data flows, which
    many find easier to follow for longer chains.

    Args:
        value: The starting value.
        steps: Unary functions applied first-to-last.

    Returns:
        The value after every step has been applied.
    """
    for step in steps:
        value = step(value)
    return value


if __name__ == "__main__":
    data = [-2, -1, 0, 1, 2, 3]
    print(doubled_positives_functional(data))
    print(doubled_positives_comprehension(data))
    print(compose(double, increment)(10))  # double(increment(10)) == 22
    print(pipeline(10, [double, increment]))  # increment(double(10)) == 21
