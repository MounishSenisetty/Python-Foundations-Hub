"""Container With Most Water via the two-pointer technique.

Each array entry is the height of a vertical line on the x-axis; picking two
lines forms a container whose water volume is the shorter height times the
horizontal distance between them. Checking every pair is O(n^2). Two pointers
starting at the widest possible container reduce this to a single linear pass.

Intuition:
    Begin with the outermost pair, which maximises width. The volume is bounded
    by the shorter line, so moving the taller line inward can only lose width
    without lifting that bound — the only move that might help is advancing the
    shorter line, hoping to find a taller one. Repeat until the pointers meet.

Time complexity: O(n).
Space complexity: O(1).
"""

from __future__ import annotations

from typing import List


def largest_container(heights: List[int]) -> int:
    """Compute the maximum water volume between two lines.

    Args:
        heights: Non-negative heights of the vertical lines.

    Returns:
        The largest volume ``min(height_i, height_j) * (j - i)`` over all pairs
        ``i < j``. Returns ``0`` when fewer than two lines are given.
    """
    left, right = 0, len(heights) - 1
    best = 0
    while left < right:
        volume = min(heights[left], heights[right]) * (right - left)
        best = max(best, volume)
        # Advance the pointer at the shorter line; keeping it can never yield a
        # taller bound for a narrower width.
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    return best


if __name__ == "__main__":
    print(largest_container([1, 8, 6, 2, 5, 4, 8, 3, 7]))  # 49
    print(largest_container([1, 1]))  # 1
