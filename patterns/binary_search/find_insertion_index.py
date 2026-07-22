"""Find the insertion index for a target (lower-bound binary search).

Given a sorted array, return the index of ``target`` if present, or otherwise
the index where it could be inserted to keep the array sorted. This is the
classic "lower bound": the first position whose value is greater than or equal
to the target.

Intuition:
    Binary search narrows a ``[low, high]`` range. Whenever the midpoint value
    is at least the target, that midpoint is a candidate answer, so move
    ``high`` to it; otherwise the answer lies strictly to the right. The range
    collapses onto the lower bound.

Time complexity: O(log n).
Space complexity: O(1).
"""

from __future__ import annotations

from typing import List


def find_insertion_index(numbers: List[int], target: int) -> int:
    """Return the leftmost index at which ``target`` is or could be inserted.

    Args:
        numbers: A list of integers sorted in non-decreasing order.
        target: The value to locate or place.

    Returns:
        The index of the first element greater than or equal to ``target``. If
        every element is smaller, ``len(numbers)`` is returned.
    """
    low, high = 0, len(numbers)
    while low < high:
        mid = (low + high) // 2
        if numbers[mid] >= target:
            high = mid
        else:
            low = mid + 1
    return low


if __name__ == "__main__":
    print(find_insertion_index([1, 3, 5, 6], 5))  # 2
    print(find_insertion_index([1, 3, 5, 6], 2))  # 1
    print(find_insertion_index([1, 3, 5, 6], 7))  # 4
