"""Validate whether a string is a palindrome, ignoring non-alphanumerics.

A phrase reads as a palindrome when, after discarding punctuation and spaces
and normalising case, it is identical forwards and backwards. Building a
cleaned copy of the string and comparing it to its reverse works but costs
O(n) extra space. Two pointers converging from the ends validate the string in
place.

Intuition:
    Walk one pointer inward from each end. Skip any character that is not
    alphanumeric, and compare the rest case-insensitively. A mismatch means the
    string is not a palindrome; meeting in the middle without a mismatch proves
    it is.

Time complexity: O(n).
Space complexity: O(1).
"""

from __future__ import annotations


def is_palindrome_valid(text: str) -> bool:
    """Report whether ``text`` is a palindrome over its alphanumeric characters.

    Comparison ignores case and any character that is not a letter or digit.
    The empty string (and any string with no alphanumeric characters) is
    considered a valid palindrome.

    Args:
        text: The string to validate.

    Returns:
        ``True`` if the alphanumeric content reads the same in both directions,
        otherwise ``False``.
    """
    left, right = 0, len(text) - 1
    while left < right:
        while left < right and not text[left].isalnum():
            left += 1
        while left < right and not text[right].isalnum():
            right -= 1
        if text[left].lower() != text[right].lower():
            return False
        left += 1
        right -= 1
    return True


if __name__ == "__main__":
    print(is_palindrome_valid("A man, a plan, a canal: Panama"))  # True
    print(is_palindrome_valid("race a car"))  # False
    print(is_palindrome_valid(" "))  # True
