"""Count anagrams of a pattern within a string (fixed-size sliding window).

An anagram of ``pattern`` is any window of the same length whose character
frequencies match. Recomputing the frequency table for every window is
O(n * m); a fixed-size sliding window updates the table incrementally — adding
the entering character and removing the leaving one — for O(n) total.

Intuition:
    Only lowercase letters appear, so two length-26 frequency arrays capture
    "does this window match the pattern?" as an equality check. Slide a window
    of the pattern's length across the string, adjusting one count in and one
    count out per step.

Time complexity: O(n), where ``n`` is the length of the string.
Space complexity: O(1) — the frequency arrays are a fixed size of 26.
"""

from __future__ import annotations


def substring_anagrams(text: str, pattern: str) -> int:
    """Count how many substrings of ``text`` are anagrams of ``pattern``.

    Both arguments are assumed to contain only lowercase English letters.

    Args:
        text: The string to search within.
        pattern: The pattern whose anagrams are counted.

    Returns:
        The number of starting positions in ``text`` where a substring equal in
        length to ``pattern`` is an anagram of it. Returns ``0`` when ``pattern``
        is longer than ``text`` or either string is empty.
    """
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return 0

    expected = [0] * 26
    window = [0] * 26
    base = ord("a")
    for char in pattern:
        expected[ord(char) - base] += 1

    count = 0
    for i in range(n):
        window[ord(text[i]) - base] += 1
        if i >= m:
            window[ord(text[i - m]) - base] -= 1
        if i >= m - 1 and window == expected:
            count += 1
    return count


if __name__ == "__main__":
    print(substring_anagrams("cbaebabacd", "abc"))  # 2
    print(substring_anagrams("abab", "ab"))  # 3
