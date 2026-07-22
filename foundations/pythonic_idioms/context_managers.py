"""Custom context managers for deterministic setup and teardown.

The ``with`` statement guarantees that cleanup code runs even when the
block raises. This module shows the two standard ways to build your own
context managers:

* A class implementing ``__enter__`` and ``__exit__`` — best when the
  manager carries state the caller wants to inspect afterwards.
* A generator decorated with ``contextlib.contextmanager`` — best for
  short, linear setup/teardown pairs.

Example:
    >>> with Stopwatch() as watch:
    ...     total = sum(range(1000))
    >>> watch.elapsed >= 0.0
    True
"""

from __future__ import annotations

import os
import time
from contextlib import contextmanager
from types import TracebackType
from typing import Iterator, Optional, Type


class Stopwatch:
    """Measure the wall-clock duration of a ``with`` block.

    The elapsed time is recorded in ``__exit__`` regardless of whether the
    block completed normally or raised, and stays available on the
    instance after the block ends.

    Attributes:
        elapsed: Seconds spent inside the ``with`` block, or ``0.0``
            before the block has finished.

    Example:
        >>> with Stopwatch() as watch:
        ...     _ = [n * n for n in range(100)]
        >>> isinstance(watch.elapsed, float)
        True
    """

    def __init__(self) -> None:
        self.elapsed: float = 0.0
        self._start: float = 0.0

    def __enter__(self) -> "Stopwatch":
        self._start = time.perf_counter()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> bool:
        self.elapsed = time.perf_counter() - self._start
        return False  # never swallow exceptions


@contextmanager
def temporary_env_var(name: str, value: str) -> Iterator[None]:
    """Set an environment variable for the duration of a ``with`` block.

    The previous value (or absence) is restored on exit, even if the body
    raises. Everything before ``yield`` is setup; everything after it —
    placed in a ``finally`` clause — is teardown.

    Args:
        name: Environment variable name.
        value: Value to expose inside the block.

    Yields:
        Nothing; the side effect is the modified environment.
    """
    original = os.environ.get(name)
    os.environ[name] = value
    try:
        yield
    finally:
        if original is None:
            os.environ.pop(name, None)
        else:
            os.environ[name] = original


@contextmanager
def rollback_on_error(items: list) -> Iterator[list]:
    """Restore a list to its previous contents if the block raises.

    A minimal transaction: mutate the list freely inside the block, and
    either the whole batch of changes sticks or none of it does.

    Args:
        items: The list to guard. It is mutated in place.

    Yields:
        The same list, for convenient in-block mutation.

    Example:
        >>> data = [1, 2]
        >>> try:
        ...     with rollback_on_error(data) as batch:
        ...         batch.append(3)
        ...         raise RuntimeError("boom")
        ... except RuntimeError:
        ...     pass
        >>> data
        [1, 2]
    """
    snapshot = list(items)
    try:
        yield items
    except BaseException:
        items[:] = snapshot
        raise


if __name__ == "__main__":
    with Stopwatch() as watch:
        sum(range(1_000_000))
    print(f"summed a million ints in {watch.elapsed:.4f}s")

    with temporary_env_var("APP_MODE", "demo"):
        print("inside block:", os.environ["APP_MODE"])
    print("after block:", os.environ.get("APP_MODE"))
