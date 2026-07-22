"""Longest substring of one repeated character after at most k replacements.

Also known as "Longest Repeating Character Replacement." Within a window we may
change up to ``k`` characters; the window is valid when the number of
characters that are *not* the window's most frequent character is at most
``k``. The window expands greedily and only shrinks when that budget is
exceeded.

Intuition:
    Track each character's frequency inside the window and the highest of those
    counts. A window of width ``w`` is achievable when ``w - max_frequency <=
    k`` (the non-majority characters can all be replaced). When it is not, slide
    the left edge forward by one to restore validity.

Time complexity: O(n).
Space complexity: O(1) — at most 26 letter counts.
"""

from __future__ import annotations

from collections import defaultdict


def longest_uniform_substring(text: str, k: int) -> int:
    """Return the longest run of one character achievable with ``k`` swaps.

    Args:
        text: The input string of uppercase English letters.
        k: The maximum number of characters that may be replaced; must be
            non-negative.

    Returns:
        The length of the longest substring that can be made uniform by
        replacing at most ``k`` characters. Returns ``0`` for the empty string.

    Raises:
        ValueError: If ``k`` is negative.
    """
    if k < 0:
        raise ValueError("k must be non-negative")

    counts: "defaultdict[str, int]" = defaultdict(int)
    left = 0
    max_frequency = 0
    best = 0

    for right, char in enumerate(text):
        counts[char] += 1
        max_frequency = max(max_frequency, counts[char])

        # If more than k characters would need replacing, shrink from the left.
        if (right - left + 1) - max_frequency > k:
            counts[text[left]] -= 1
            left += 1

        best = max(best, right - left + 1)

    return best


if __name__ == "__main__":
    print(longest_uniform_substring("AABABBA", 1))  # 4
    print(longest_uniform_substring("ABBB", 2))  # 4
