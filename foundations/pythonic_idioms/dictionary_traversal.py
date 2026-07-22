"""Idiomatic dictionary access and traversal patterns.

Reaching into a dictionary with ``if key in mapping`` guards quickly turns
into boilerplate. Python ships three purpose-built tools that express the
same intent in a single call:

* ``dict.get`` — read a key, falling back to a default when it is missing.
* ``dict.setdefault`` — read a key, inserting the default first if needed.
* ``collections.defaultdict`` — a dict that builds missing values on demand.

Each function below pairs the idiom with a realistic task (counting,
grouping, inverting) so the trade-offs are easy to compare.

Example:
    >>> count_occurrences(["a", "b", "a"])
    {'a': 2, 'b': 1}
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, Hashable, Iterable, List, Mapping, Tuple, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V", bound=Hashable)


def get_setting(settings: Mapping[str, str], key: str, default: str = "") -> str:
    """Read a configuration value with a graceful fallback.

    Prefer this over the verbose guard::

        if key in settings:        # non-idiomatic
            value = settings[key]
        else:
            value = default

    Args:
        settings: Mapping of configuration keys to values.
        key: The configuration key to look up.
        default: Value returned when ``key`` is absent.

    Returns:
        The stored value, or ``default`` when the key is missing.
    """
    return settings.get(key, default)


def count_occurrences(items: Iterable[K]) -> Dict[K, int]:
    """Count how many times each item appears in ``items``.

    Uses ``dict.get`` with a default of ``0`` so no membership check is
    needed before incrementing.

    Args:
        items: Any iterable of hashable values.

    Returns:
        A dict mapping each distinct item to its occurrence count.
    """
    counts: Dict[K, int] = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts


def group_by_first_letter(words: Iterable[str]) -> Dict[str, List[str]]:
    """Group words into buckets keyed by their first letter.

    ``dict.setdefault`` inserts an empty list the first time a letter is
    seen and returns the existing list on every later hit, so the append
    works unconditionally.

    Args:
        words: Iterable of non-empty words.

    Returns:
        A dict mapping a lowercase first letter to the words that start
        with it, in input order.

    Raises:
        ValueError: If any word is an empty string.
    """
    groups: Dict[str, List[str]] = {}
    for word in words:
        if not word:
            raise ValueError("cannot group an empty string")
        groups.setdefault(word[0].lower(), []).append(word)
    return groups


def tally_pairs(pairs: Iterable[Tuple[K, int]]) -> Dict[K, int]:
    """Sum integer values per key using ``collections.defaultdict``.

    ``defaultdict(int)`` calls ``int()`` (which returns ``0``) for every
    missing key, which removes the need for ``get``/``setdefault``
    entirely — the best fit when *every* access should auto-initialise.

    Args:
        pairs: Iterable of ``(key, amount)`` tuples.

    Returns:
        A plain ``dict`` mapping each key to the sum of its amounts.
    """
    totals: "defaultdict[K, int]" = defaultdict(int)
    for key, amount in pairs:
        totals[key] += amount
    return dict(totals)


def invert_mapping(mapping: Mapping[K, V]) -> Dict[V, List[K]]:
    """Invert a mapping, collecting keys that share a value.

    Because multiple keys may map to the same value, the inverse maps each
    value to a *list* of keys, built with ``defaultdict(list)``.

    Args:
        mapping: The mapping to invert. Values must be hashable.

    Returns:
        A dict mapping each original value to the list of keys that held
        it, in the mapping's iteration order.
    """
    inverse: "defaultdict[V, List[K]]" = defaultdict(list)
    for key, value in mapping.items():
        inverse[value].append(key)
    return dict(inverse)


if __name__ == "__main__":
    print(count_occurrences("mississippi"))
    print(group_by_first_letter(["apple", "avocado", "banana"]))
    print(tally_pairs([("food", 20), ("rent", 800), ("food", 15)]))
    print(invert_mapping({"a": 1, "b": 2, "c": 1}))
