"""Maximise the sawblade height when cutting at least k metres of wood.

A sawblade set to height ``H`` cuts the portion of every tree that rises above
``H``, yielding ``sum(max(0, tree - H))`` metres of wood. We want the greatest
``H`` that still produces at least ``k`` metres — higher blades waste less of
the trees. The wood yield is monotonic: it never increases as ``H`` rises, so
the answer can be found by binary searching the *height range* rather than any
array of inputs.

Intuition:
    Candidate heights run from 0 to the tallest tree. For a given height,
    computing the yield is a linear scan. Because yield decreases monotonically
    with height, binary search discards half the height range at each step,
    keeping the largest height whose yield still meets the quota.

Time complexity: O(n log H), where ``H`` is the tallest tree's height.
Space complexity: O(1).
"""

from __future__ import annotations

from typing import List


def _wood_yield(heights: List[int], blade: int) -> int:
    """Total wood collected when the blade is set to ``blade`` metres."""
    return sum(height - blade for height in heights if height > blade)


def cutting_wood(heights: List[int], k: int) -> int:
    """Return the maximum blade height that still yields at least ``k`` wood.

    Args:
        heights: Heights of the trees.
        k: The minimum amount of wood required; must be non-negative.

    Returns:
        The greatest integer blade height whose yield is at least ``k``. If even
        a blade at height 0 cannot produce ``k`` wood, ``0`` is returned.

    Raises:
        ValueError: If ``k`` is negative.
    """
    if k < 0:
        raise ValueError("k must be non-negative")

    low, high = 0, max(heights, default=0)
    best = 0
    while low <= high:
        mid = (low + high) // 2
        if _wood_yield(heights, mid) >= k:
            best = mid  # feasible; try a taller (more efficient) blade
            low = mid + 1
        else:
            high = mid - 1
    return best


if __name__ == "__main__":
    print(cutting_wood([2, 6, 3, 8], 7))  # 3  (yields (6-3)+(8-3)=8 >= 7)
    print(cutting_wood([1, 2, 3], 100))  # 0
