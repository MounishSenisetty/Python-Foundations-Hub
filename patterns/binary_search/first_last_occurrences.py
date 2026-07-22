"""Find the first and last indices of a target in a sorted array.

When a sorted array contains duplicates, a single binary search finds *some*
occurrence but not necessarily the boundaries. Running two boundary searches —
one biased left, one biased right — pinpoints the first and last positions,
each in logarithmic time.

Intuition:
    The lower-bound search returns the first index whose value is at least the
    target. The upper-bound search returns the first index whose value is
    strictly greater than the target; the last occurrence sits just before it.
    Comparing the lower bound against the array confirms the target exists.

Time complexity: O(log n).
Space complexity: O(1).
"""

from __future__ import annotations

from typing import List, Tuple


def _lower_bound(numbers: List[int], target: int) -> int:
    """First index with value >= target (or ``len`` if none)."""
    low, high = 0, len(numbers)
    while low < high:
        mid = (low + high) // 2
        if numbers[mid] >= target:
            high = mid
        else:
            low = mid + 1
    return low


def _upper_bound(numbers: List[int], target: int) -> int:
    """First index with value > target (or ``len`` if none).

    The midpoint is right-biased in effect: values equal to the target push the
    lower boundary rightward until the window sits past the final match.
    """
    low, high = 0, len(numbers)
    while low < high:
        mid = (low + high) // 2
        if numbers[mid] > target:
            high = mid
        else:
            low = mid + 1
    return low


def first_last_occurrences(numbers: List[int], target: int) -> Tuple[int, int]:
    """Return the first and last indices of ``target`` in a sorted array.

    Args:
        numbers: A list of integers sorted in non-decreasing order.
        target: The value to locate.

    Returns:
        A ``(first, last)`` tuple of zero-based indices, or ``(-1, -1)`` if the
        target is absent.
    """
    first = _lower_bound(numbers, target)
    if first == len(numbers) or numbers[first] != target:
        return -1, -1
    last = _upper_bound(numbers, target) - 1
    return first, last


if __name__ == "__main__":
    print(first_last_occurrences([5, 7, 7, 8, 8, 10], 8))  # (3, 4)
    print(first_last_occurrences([5, 7, 7, 8, 8, 10], 6))  # (-1, -1)
