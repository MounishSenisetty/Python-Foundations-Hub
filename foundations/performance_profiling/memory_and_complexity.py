"""Memory-lean patterns: ``__slots__`` and generators.

Two of the highest-leverage memory techniques in CPython:

* ``__slots__`` replaces each instance's ``__dict__`` with fixed slot
  descriptors. For classes instantiated millions of times (points,
  tokens, tree nodes) this cuts per-instance memory substantially and
  speeds up attribute access — at the cost of dynamic attributes.
* Generators produce values one at a time instead of materialising a
  whole list, turning O(n) peak memory into O(1) for streaming
  workloads, and allowing pipelines over unbounded sequences.

Example:
    >>> point = SlottedPoint(1.0, 2.0)
    >>> point.x
    1.0
    >>> sum(squares_up_to(4))
    14
"""

from __future__ import annotations

import sys
from typing import Iterator, List, Sequence


class RegularPoint:
    """A 2-D point backed by a normal per-instance ``__dict__``.

    Kept as the baseline for the memory comparison in
    ``instance_footprint``.

    Args:
        x: Horizontal coordinate.
        y: Vertical coordinate.
    """

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


class SlottedPoint:
    """A 2-D point using ``__slots__`` for a fixed, compact layout.

    Behaves like ``RegularPoint`` except that assigning any attribute
    outside ``x`` and ``y`` raises ``AttributeError`` — the flexibility
    traded away for the smaller footprint.

    Args:
        x: Horizontal coordinate.
        y: Vertical coordinate.
    """

    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


def instance_footprint(point: object) -> int:
    """Approximate the memory held by one point instance, in bytes.

    ``sys.getsizeof`` alone under-reports objects with a ``__dict__``,
    since the dict is a separate allocation; it is added when present.

    Args:
        point: Any object.

    Returns:
        The instance size plus its ``__dict__`` size, if it has one.
    """
    size = sys.getsizeof(point)
    instance_dict = getattr(point, "__dict__", None)
    if instance_dict is not None:
        size += sys.getsizeof(instance_dict)
    return size


def squares_list(limit: int) -> List[int]:
    """Materialise the squares of ``0..limit`` as a list.

    Fine for small ``limit``; peak memory grows linearly with input.

    Args:
        limit: Inclusive upper bound; must be non-negative.

    Returns:
        Every square from ``0**2`` through ``limit**2``.

    Raises:
        ValueError: If ``limit`` is negative.
    """
    if limit < 0:
        raise ValueError("limit must be non-negative")
    return [n * n for n in range(limit + 1)]


def squares_up_to(limit: int) -> Iterator[int]:
    """Yield the squares of ``0..limit`` lazily, one at a time.

    Constant memory regardless of ``limit``: only the current value
    exists at any moment. The trade-off is single-pass consumption —
    a generator cannot be re-iterated or indexed.

    Args:
        limit: Inclusive upper bound; must be non-negative.

    Yields:
        Each square in increasing order.

    Raises:
        ValueError: If ``limit`` is negative (raised on first ``next``).
    """
    if limit < 0:
        raise ValueError("limit must be non-negative")
    for n in range(limit + 1):
        yield n * n


def running_mean(samples: Sequence[float], window: int) -> Iterator[float]:
    """Stream the mean of a sliding window over ``samples``.

    A generator-based pipeline stage: it keeps only ``window`` values of
    state, however long the input, and composes with other iterator
    consumers (``max``, ``zip``, further generators).

    Args:
        samples: The numeric series to smooth.
        window: Sliding window width; must be positive.

    Yields:
        The mean of each full window, left to right.

    Raises:
        ValueError: If ``window`` is not positive (raised on first
            ``next``).
    """
    if window <= 0:
        raise ValueError("window must be positive")
    total = 0.0
    for index, sample in enumerate(samples):
        total += sample
        if index >= window:
            total -= samples[index - window]
        if index >= window - 1:
            yield total / window


if __name__ == "__main__":
    regular = RegularPoint(1.0, 2.0)
    slotted = SlottedPoint(1.0, 2.0)
    print("regular point:", instance_footprint(regular), "bytes")
    print("slotted point:", instance_footprint(slotted), "bytes")
    print("lazy sum of squares:", sum(squares_up_to(1_000_000)))
    print("smoothed:", list(running_mean([1, 2, 3, 4, 5, 6], window=3)))
