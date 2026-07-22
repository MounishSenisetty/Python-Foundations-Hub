"""3-Sum: find all unique triplets that sum to zero.

The brute-force approach checks every triplet in O(n^3). By sorting first we
can fix one element and run a two-pointer scan over the remainder, collapsing
the inner search to linear time and giving an overall O(n^2) solution. Sorting
also makes it straightforward to skip duplicate values so the result contains
no repeated triplets.

Intuition:
    For each index ``i``, look for two numbers in the sub-array to its right
    that sum to ``-numbers[i]``. Because the array is sorted, a converging
    two-pointer pass finds those pairs in linear time, and advancing past equal
    values keeps every emitted triplet unique.

Time complexity: O(n^2).
Space complexity: O(1) auxiliary (excluding the sort and the output).
"""

from __future__ import annotations

from typing import List


def triplet_sum(numbers: List[int]) -> List[List[int]]:
    """Return all unique triplets that sum to zero.

    Args:
        numbers: An arbitrary list of integers.

    Returns:
        A list of ``[a, b, c]`` triplets, each sorted ascending and summing to
        zero, with no duplicate triplets. The triplets are returned in
        ascending order of their first, then second, element.
    """
    nums = sorted(numbers)
    triplets: List[List[int]] = []
    n = len(nums)

    for i in range(n - 2):
        # Once the smallest element of the triplet is positive, no sum of
        # three ascending values can reach zero.
        if nums[i] > 0:
            break
        # Skip duplicate anchors to avoid repeating triplets.
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        left, right = i + 1, n - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                triplets.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                # Skip duplicate second/third elements.
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1

    return triplets


if __name__ == "__main__":
    print(triplet_sum([-1, 0, 1, 2, -1, -4]))  # [[-1, -1, 2], [-1, 0, 1]]
    print(triplet_sum([0, 0, 0, 0]))  # [[0, 0, 0]]
