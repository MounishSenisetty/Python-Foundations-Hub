"""Two-sum on an unsorted array using a hash map of complements.

When the input is not sorted, the two-pointer trick no longer applies. A single
pass that remembers each value it has seen lets us answer, for every new
element, "have I already seen the number that completes the target?" in
constant time.

Intuition:
    As we scan, we need ``target - current`` to have appeared earlier. Storing
    each value's index in a hash map turns that lookup into O(1), so one pass
    suffices.

Time complexity: O(n).
Space complexity: O(n).
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple


def pair_sum_unsorted(numbers: List[int], target: int) -> Optional[Tuple[int, int]]:
    """Find two indices whose values sum to ``target`` in an unsorted array.

    Args:
        numbers: An arbitrary list of integers.
        target: The desired sum.

    Returns:
        A ``(i, j)`` tuple of zero-based indices with ``i < j`` and
        ``numbers[i] + numbers[j] == target``, or ``None`` if no pair exists.
        The pair with the smallest right index is returned.
    """
    seen: Dict[int, int] = {}
    for index, value in enumerate(numbers):
        complement = target - value
        if complement in seen:
            return seen[complement], index
        seen[value] = index
    return None


if __name__ == "__main__":
    print(pair_sum_unsorted([2, 7, 11, 15], 9))  # (0, 1)
    print(pair_sum_unsorted([3, 2, 4], 6))  # (1, 2)
    print(pair_sum_unsorted([1, 2, 3], 100))  # None
