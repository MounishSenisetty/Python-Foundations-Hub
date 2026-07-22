"""Longest substring without repeating characters (dynamic sliding window).

The window grows from the right and shrinks from the left only as much as
needed to keep every character unique. Remembering the last index at which each
character appeared lets the left edge jump directly past a repeat instead of
crawling one step at a time.

Intuition:
    Extend the right edge over each new character. If that character was seen
    inside the current window, snap the left edge to just after its previous
    occurrence. The best window width encountered along the way is the answer.

Time complexity: O(n).
Space complexity: O(min(n, alphabet size)).
"""

from __future__ import annotations

from typing import Dict


def longest_substring_unique(text: str) -> int:
    """Return the length of the longest substring with all distinct characters.

    Args:
        text: The input string (any characters).

    Returns:
        The length of the longest substring of ``text`` that contains no
        repeated character. Returns ``0`` for the empty string.
    """
    last_seen: Dict[str, int] = {}
    left = 0
    best = 0
    for right, char in enumerate(text):
        previous = last_seen.get(char)
        if previous is not None and previous >= left:
            left = previous + 1
        last_seen[char] = right
        best = max(best, right - left + 1)
    return best


if __name__ == "__main__":
    print(longest_substring_unique("abcabcbb"))  # 3 ("abc")
    print(longest_substring_unique("bbbbb"))  # 1 ("b")
    print(longest_substring_unique("pwwkew"))  # 3 ("wke")
