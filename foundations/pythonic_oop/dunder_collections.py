"""Building a native-feeling container with dunder methods.

A class earns ``len(x)``, ``x[i]``, ``for item in x``, ``item in x`` and
``==`` not by inheriting from ``list`` but by implementing the protocol
methods Python looks for: ``__len__``, ``__getitem__``, ``__repr__``,
``__eq__``, and ``__contains__``. Implementing ``__len__`` and
``__getitem__`` alone already makes the class iterable and sliceable —
the rest sharpen semantics and debugging output.

Example:
    >>> shelf = Bookshelf(["Dune", "Emma"])
    >>> len(shelf)
    2
    >>> "Dune" in shelf
    True
"""

from __future__ import annotations

from typing import Iterable, Iterator, List, Union


class Bookshelf:
    """An ordered, case-insensitively searchable collection of titles.

    Wraps a list through composition rather than subclassing ``list``,
    so only the operations that make sense for a shelf are exposed, and
    membership tests get shelf-specific behaviour (case-insensitive
    matching).

    Args:
        titles: Initial book titles, kept in the given order.

    Example:
        >>> shelf = Bookshelf(["Dune"])
        >>> shelf[0]
        'Dune'
    """

    def __init__(self, titles: Iterable[str] = ()) -> None:
        self._titles: List[str] = list(titles)

    def add(self, title: str) -> None:
        """Place a title at the end of the shelf.

        Args:
            title: A non-empty book title.

        Raises:
            ValueError: If ``title`` is empty or only whitespace.
        """
        if not title or not title.strip():
            raise ValueError("title must be a non-empty string")
        self._titles.append(title)

    def __len__(self) -> int:
        """Number of books on the shelf; also makes ``bool(shelf)`` work."""
        return len(self._titles)

    def __getitem__(self, index: Union[int, slice]) -> Union[str, "Bookshelf"]:
        """Index or slice the shelf.

        Integer indexing returns a title; slicing returns a new
        ``Bookshelf`` (not a bare list), so slices stay in the domain.

        Args:
            index: A position or slice.

        Returns:
            The title at ``index``, or a new shelf for a slice.

        Raises:
            IndexError: If an integer index is out of range.
            TypeError: For unsupported index types.
        """
        if isinstance(index, slice):
            return Bookshelf(self._titles[index])
        return self._titles[index]

    def __iter__(self) -> Iterator[str]:
        """Iterate titles in shelf order."""
        return iter(self._titles)

    def __contains__(self, title: object) -> bool:
        """Case-insensitive membership: ``"dune" in shelf`` matches ``"Dune"``."""
        if not isinstance(title, str):
            return False
        needle = title.casefold()
        return any(existing.casefold() == needle for existing in self._titles)

    def __eq__(self, other: object) -> bool:
        """Shelves are equal when they hold the same titles in the same order."""
        if not isinstance(other, Bookshelf):
            return NotImplemented
        return self._titles == other._titles

    def __repr__(self) -> str:
        """Unambiguous, ``eval``-able developer representation."""
        return f"Bookshelf({self._titles!r})"


if __name__ == "__main__":
    shelf = Bookshelf(["Dune", "Emma", "Ficciones"])
    print(repr(shelf), "holds", len(shelf), "books")
    print("emma in shelf:", "emma" in shelf)
    print("first two:", repr(shelf[:2]))
    for title in shelf:
        print("-", title)
