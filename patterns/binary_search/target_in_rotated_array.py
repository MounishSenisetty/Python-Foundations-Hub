"""Search a rotated sorted array in logarithmic time.

A sorted array rotated at an unknown pivot (for example ``[4, 5, 6, 7, 0, 1,
2]``) is no longer globally sorted, but any midpoint still splits it into one
sorted half and one rotated half. Identifying the sorted half at each step lets
binary search decide which way to go, preserving O(log n) time.

Intuition:
    Compare the midpoint with the low end to learn which half is sorted. If the
    target falls inside that sorted half's value range, search there; otherwise
    search the other half. Each step halves the search space.

Assumes all elements are distinct.

Time complexity: O(log n).
Space complexity: O(1).
"""

from __future__ import annotations

from typing import List


def search_rotated(numbers: List[int], target: int) -> int:
    """Return the index of ``target`` in a rotated sorted array, or ``-1``.

    Args:
        numbers: A sorted array of distinct integers, rotated at an unknown
            pivot.
        target: The value to find.

    Returns:
        The index of ``target``, or ``-1`` if it is not present.
    """
    low, high = 0, len(numbers) - 1
    while low <= high:
        mid = (low + high) // 2
        if numbers[mid] == target:
            return mid

        if numbers[low] <= numbers[mid]:
            # Left half [low, mid] is sorted.
            if numbers[low] <= target < numbers[mid]:
                high = mid - 1
            else:
                low = mid + 1
        else:
            # Right half [mid, high] is sorted.
            if numbers[mid] < target <= numbers[high]:
                low = mid + 1
            else:
                high = mid - 1
    return -1


if __name__ == "__main__":
    print(search_rotated([4, 5, 6, 7, 0, 1, 2], 0))  # 4
    print(search_rotated([4, 5, 6, 7, 0, 1, 2], 3))  # -1
    print(search_rotated([1], 1))  # 0
