"""Two-sum on a sorted array using the two-pointer technique.

Given an array sorted in non-decreasing order, find a pair of elements that
adds up to a target. A hash map solves the unsorted version in O(n) time and
O(n) space; when the input is already sorted we can do better on space by
converging two pointers from both ends, trading no extra memory for the same
linear time.

Intuition:
    Start with the widest pair (smallest + largest). If the sum is too small,
    the only way to grow it is to move the left pointer right; if it is too
    large, move the right pointer left. Each element is visited at most once.

Time complexity: O(n).
Space complexity: O(1).
"""

from __future__ import annotations

from typing import List, Optional, Tuple


def pair_sum_sorted(numbers: List[int], target: int) -> Optional[Tuple[int, int]]:
    """Find two indices whose values sum to ``target`` in a sorted array.

    Args:
        numbers: A list of integers sorted in non-decreasing order.
        target: The desired sum.

    Returns:
        A ``(left, right)`` tuple of zero-based indices with
        ``numbers[left] + numbers[right] == target``, or ``None`` if no such
        pair exists. When several pairs qualify, the one with the smallest
        left index is returned.
    """
    left, right = 0, len(numbers) - 1
    while left < right:
        current = numbers[left] + numbers[right]
        if current == target:
            return left, right
        if current < target:
            left += 1
        else:
            right -= 1
    return None


if __name__ == "__main__":
    print(pair_sum_sorted([1, 2, 4, 7, 11, 15], 15))  # (1, 4)
    print(pair_sum_sorted([1, 2, 3], 7))  # None
