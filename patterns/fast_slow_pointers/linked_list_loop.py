"""Detect a cycle in a linked list with Floyd's algorithm.

A linked list contains a cycle if some node's ``next`` pointer references an
earlier node, making traversal loop forever. Recording visited nodes in a set
detects this in O(n) space. Floyd's "tortoise and hare" needs only two
pointers.

Intuition:
    Move a slow pointer one step and a fast pointer two steps per iteration. If
    the list ends, there is no cycle. If there is a cycle, the fast pointer
    laps the slow one and they eventually land on the same node — the way a
    faster runner catches a slower one on a circular track.

Time complexity: O(n).
Space complexity: O(1).
"""

from __future__ import annotations

from typing import Optional


class ListNode:
    """A node in a singly linked list.

    Attributes:
        val: The value stored at this node.
        next: The following node, or ``None`` at the tail.
    """

    def __init__(self, val: int = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next


def has_cycle(head: Optional[ListNode]) -> bool:
    """Report whether the linked list contains a cycle.

    Args:
        head: The head of the list.

    Returns:
        ``True`` if a cycle is present, otherwise ``False``.
    """
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next  # type: ignore[union-attr]
        fast = fast.next.next
        if slow is fast:
            return True
    return False


if __name__ == "__main__":
    a, b, c = ListNode(1), ListNode(2), ListNode(3)
    a.next, b.next, c.next = b, c, a  # 1 -> 2 -> 3 -> 1 (cycle)
    print(has_cycle(a))  # True

    x, y = ListNode(1), ListNode(2)
    x.next = y
    print(has_cycle(x))  # False
