"""Expressing function contracts with the ``typing`` module.

Type hints turn implicit assumptions into checked, documented contracts:

* ``Callable[[X], Y]`` — "give me a function from X to Y", the contract
  of every higher-order function.
* ``TypeVar`` — links input and output types ("returns the same type it
  was given") without collapsing to ``Any``.
* ``Generic`` — classes parameterised over an element type, so
  ``TypedRegistry[int]`` and ``TypedRegistry[str]`` are distinct,
  checkable types.
* ``Optional[X]`` — an honest signature for "X or ``None``", forcing
  callers to handle the miss case.

Example:
    >>> first_matching([1, 4, 6], lambda n: n % 2 == 0)
    4
"""

from __future__ import annotations

from typing import Callable, Dict, Generic, Iterable, List, Optional, TypeVar

T = TypeVar("T")
U = TypeVar("U")


def first_matching(items: Iterable[T], predicate: Callable[[T], bool]) -> Optional[T]:
    """Return the first item satisfying ``predicate``, or ``None``.

    The ``Optional[T]`` return type makes the "not found" case part of
    the contract instead of a surprise.

    Args:
        items: The values to scan, in order.
        predicate: Decides whether an item matches.

    Returns:
        The first matching item, or ``None`` when nothing matches.
    """
    for item in items:
        if predicate(item):
            return item
    return None


def apply_twice(func: Callable[[T], T], value: T) -> T:
    """Apply a type-preserving function two times.

    The single ``TypeVar`` ties the function's input, its output, and
    ``value`` together: passing a ``Callable[[int], str]`` here is a
    type error, caught before runtime.

    Args:
        func: A function whose output type matches its input type.
        value: The starting value.

    Returns:
        ``func(func(value))``.
    """
    return func(func(value))


def map_optional(value: Optional[T], func: Callable[[T], U]) -> Optional[U]:
    """Apply ``func`` to a value that may be ``None``.

    Collapses the repetitive ``if x is not None`` dance around optional
    values into one reusable, fully typed helper.

    Args:
        value: The possibly-missing input.
        func: Transformation applied only when ``value`` is present.

    Returns:
        ``func(value)``, or ``None`` when ``value`` is ``None``.
    """
    if value is None:
        return None
    return func(value)


class TypedRegistry(Generic[T]):
    """A name-to-value store parameterised over its value type.

    Annotating a variable as ``TypedRegistry[int]`` lets a type checker
    reject ``register("x", "not an int")`` at analysis time, while the
    runtime class stays a plain, simple dict wrapper.

    Example:
        >>> registry: TypedRegistry[int] = TypedRegistry()
        >>> registry.register("answer", 42)
        >>> registry.get("answer")
        42
    """

    def __init__(self) -> None:
        self._entries: Dict[str, T] = {}

    def register(self, name: str, value: T) -> None:
        """Store ``value`` under ``name``.

        Args:
            name: Unique key for the value.
            value: The value to store.

        Raises:
            KeyError: If ``name`` is already registered.
        """
        if name in self._entries:
            raise KeyError(f"{name!r} is already registered")
        self._entries[name] = value

    def get(self, name: str) -> Optional[T]:
        """Look up a value by name.

        Args:
            name: The key to look up.

        Returns:
            The stored value, or ``None`` when absent.
        """
        return self._entries.get(name)

    def names(self) -> List[str]:
        """List registered names in insertion order.

        Returns:
            The registered keys as a new list.
        """
        return list(self._entries)


if __name__ == "__main__":
    print(first_matching(["a", "bb", "ccc"], lambda word: len(word) > 1))
    print(apply_twice(lambda n: n + 3, 10))
    print(map_optional("shout", str.upper), map_optional(None, str.upper))

    registry: TypedRegistry[int] = TypedRegistry()
    registry.register("answer", 42)
    print(registry.names(), registry.get("answer"))
