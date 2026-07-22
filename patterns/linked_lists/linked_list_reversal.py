"""Reverse a singly linked list, iteratively and recursively.

Reversing a list means flipping every ``next`` pointer so the tail becomes the
head. Both approaches below run in linear time; they differ in space. The
iterative version rewires pointers with three references and uses constant
space, while the recursive version is often considered more elegant at the cost
of O(n) call-stack depth.

Time complexity: O(n) for both.
Space complexity: O(1) iterative, O(n) recursive (call stack).
"""

from __future__ import annotations

from typing import Iterable, List, Optional


class ListNode:
    """A node in a singly linked list.

    Attributes:
        val: The value stored at this node.
        next: The following node, or ``None`` at the tail.
    """

    def __init__(self, val: int = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next


def build_linked_list(values: Iterable[int]) -> Optional[ListNode]:
    """Build a linked list from an iterable and return its head.

    Args:
        values: The values to link, in order.

    Returns:
        The head node, or ``None`` for an empty iterable.
    """
    head: Optional[ListNode] = None
    for value in reversed(list(values)):
        head = ListNode(value, head)
    return head


def linked_list_to_list(head: Optional[ListNode]) -> List[int]:
    """Collect a linked list's values into a Python list.

    Args:
        head: The head node, or ``None``.

    Returns:
        The node values in order.
    """
    result: List[int] = []
    while head is not None:
        result.append(head.val)
        head = head.next
    return result


def reverse_iterative(head: Optional[ListNode]) -> Optional[ListNode]:
    """Reverse a linked list iteratively in constant space.

    Args:
        head: The head of the list to reverse.

    Returns:
        The head of the reversed list.
    """
    previous: Optional[ListNode] = None
    current = head
    while current is not None:
        following = current.next
        current.next = previous
        previous = current
        current = following
    return previous


def reverse_recursive(head: Optional[ListNode]) -> Optional[ListNode]:
    """Reverse a linked list recursively.

    Args:
        head: The head of the list to reverse.

    Returns:
        The head of the reversed list.
    """
    if head is None or head.next is None:
        return head
    new_head = reverse_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head


if __name__ == "__main__":
    source = build_linked_list([1, 2, 3, 4, 5])
    print(linked_list_to_list(reverse_iterative(source)))  # [5, 4, 3, 2, 1]

    source = build_linked_list([1, 2, 3])
    print(linked_list_to_list(reverse_recursive(source)))  # [3, 2, 1]
