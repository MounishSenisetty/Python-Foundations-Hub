"""Programmatic micro-benchmarking with the ``timeit`` module.

``timeit`` exists because naive ``time.time()`` deltas mislead: a single
run is dominated by noise, and the garbage collector can fire mid-
measurement. ``timeit`` runs the target many times, disables GC by
default, and uses the highest-resolution clock available.

The helpers here wrap ``timeit.timeit``/``timeit.repeat`` for *callables*
(rather than source strings), which composes naturally with the rest of
a codebase. Two conventions worth internalising:

* Report the **minimum** of several repeats — it is the best estimate of
  the true cost; other samples are "true cost plus interference".
* Compare implementations with the **same** ``number`` of iterations.

Example:
    >>> result = benchmark(lambda: sum(range(100)), number=10)
    >>> result.seconds > 0
    True
"""

from __future__ import annotations

import timeit
from dataclasses import dataclass
from typing import Callable, Dict, Sequence


@dataclass(frozen=True)
class BenchmarkResult:
    """Outcome of timing one callable.

    Attributes:
        label: Human-readable name of the measured callable.
        number: How many times the callable ran per measurement.
        seconds: Best (minimum) total time across repeats, in seconds.
    """

    label: str
    number: int
    seconds: float

    @property
    def per_call_seconds(self) -> float:
        """Average seconds per single call within the best repeat."""
        return self.seconds / self.number


def benchmark(
    func: Callable[[], object],
    *,
    number: int = 1000,
    repeat: int = 3,
    label: str = "",
) -> BenchmarkResult:
    """Time a zero-argument callable with ``timeit.repeat``.

    Args:
        func: The code under test; close over any needed arguments with
            ``functools.partial`` or a ``lambda``.
        number: Calls per measurement; must be positive.
        repeat: Independent measurements taken; the minimum is kept.
        label: Optional display name; defaults to the function's name.

    Returns:
        A ``BenchmarkResult`` holding the best measurement.

    Raises:
        ValueError: If ``number`` or ``repeat`` is not positive.
    """
    if number <= 0 or repeat <= 0:
        raise ValueError("number and repeat must be positive")
    timings = timeit.repeat(func, number=number, repeat=repeat)
    return BenchmarkResult(
        label=label or getattr(func, "__name__", "callable"),
        number=number,
        seconds=min(timings),
    )


def compare(
    contenders: Dict[str, Callable[[], object]],
    *,
    number: int = 1000,
    repeat: int = 3,
) -> Dict[str, BenchmarkResult]:
    """Benchmark several implementations under identical conditions.

    Args:
        contenders: Mapping of display names to zero-argument callables.
        number: Calls per measurement, shared by every contender.
        repeat: Measurements per contender.

    Returns:
        Results keyed by name, ordered fastest first.

    Raises:
        ValueError: If ``contenders`` is empty.
    """
    if not contenders:
        raise ValueError("nothing to compare")
    results = {
        name: benchmark(func, number=number, repeat=repeat, label=name)
        for name, func in contenders.items()
    }
    return dict(sorted(results.items(), key=lambda pair: pair[1].seconds))


def format_comparison(results: Dict[str, BenchmarkResult]) -> str:
    """Render comparison results as an aligned text table.

    Args:
        results: Output of ``compare``.

    Returns:
        One line per contender: name, best time, and slowdown factor
        relative to the fastest entry.
    """
    fastest = min(result.seconds for result in results.values())
    width = max(len(name) for name in results)
    lines = [
        f"{result.label:<{width}}  {result.seconds:.6f}s"
        f"  ({result.seconds / fastest:.2f}x)"
        for result in results.values()
    ]
    return "\n".join(lines)


def _concat_join(chunks: Sequence[str]) -> str:
    return "".join(chunks)


def _concat_plus(chunks: Sequence[str]) -> str:
    text = ""
    for chunk in chunks:
        text += chunk
    return text


if __name__ == "__main__":
    words = ["chunk"] * 2000
    outcome = compare(
        {
            "str.join": lambda: _concat_join(words),
            "+= loop": lambda: _concat_plus(words),
        },
        number=200,
    )
    print(format_comparison(outcome))
