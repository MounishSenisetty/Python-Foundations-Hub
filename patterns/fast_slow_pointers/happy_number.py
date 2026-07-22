"""Determine whether a number is "happy" via cycle detection.

Repeatedly replacing a positive integer with the sum of the squares of its
digits either reaches 1 (a happy number) or falls into a cycle that never
includes 1. Detecting that cycle is exactly the fast/slow pointer problem, with
the "next node" being the next number in the sequence.

Intuition:
    Treat the transformation as walking a linked list of numbers. A slow
    pointer takes one step per iteration and a fast pointer two. If the fast
    pointer reaches 1, the number is happy; if the two pointers meet on any
    other value, the sequence has entered a cycle and 1 is unreachable.

Time complexity: O(log n) per step, over a bounded number of distinct values.
Space complexity: O(1).
"""

from __future__ import annotations


def _sum_square_digits(number: int) -> int:
    """Return the sum of the squares of a number's decimal digits."""
    total = 0
    while number > 0:
        number, digit = divmod(number, 10)
        total += digit * digit
    return total


def is_happy(number: int) -> bool:
    """Report whether ``number`` is a happy number.

    Args:
        number: A positive integer.

    Returns:
        ``True`` if repeatedly summing squared digits reaches 1, otherwise
        ``False``.

    Raises:
        ValueError: If ``number`` is not positive.
    """
    if number <= 0:
        raise ValueError("number must be a positive integer")

    slow = number
    fast = _sum_square_digits(number)
    while fast != 1 and slow != fast:
        slow = _sum_square_digits(slow)
        fast = _sum_square_digits(_sum_square_digits(fast))
    return fast == 1


if __name__ == "__main__":
    print(is_happy(19))  # True  (19 -> 82 -> 68 -> 100 -> 1)
    print(is_happy(2))  # False (enters a cycle)
