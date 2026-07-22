"""Remove the k-th node from the end of a singly linked list.

Finding the k-th node from the end normally needs the list's length, implying
two passes. A leader/trailer pair removes the node in a single pass: advance a
leader pointer ``k`` steps ahead, then move both pointers together until the
leader reaches the end — at which point the trailer sits just before the target.

A dummy node in front of the head makes removing the head itself a
non-special-case, since the trailer always has a valid predecessor to rewire.

Time complexity: O(n).
Space complexity: O(1).
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
    """Build a linked list from an iterable and return its head."""
    head: Optional[ListNode] = None
    for value in reversed(list(values)):
        head = ListNode(value, head)
    return head


def linked_list_to_list(head: Optional[ListNode]) -> List[int]:
    """Collect a linked list's values into a Python list."""
    result: List[int] = []
    while head is not None:
        result.append(head.val)
        head = head.next
    return result


def remove_kth_last_node(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    """Remove the k-th node counting from the end of the list.

    Args:
        head: The head of the list.
        k: The 1-based position from the end (``k == 1`` removes the tail).

    Returns:
        The head of the modified list.

    Raises:
        ValueError: If ``k`` is not positive or exceeds the list length.
    """
    if k <= 0:
        raise ValueError("k must be a positive integer")

    dummy = ListNode(0, head)
    leader = dummy
    trailer = dummy

    # Advance the leader k nodes into the list, leaving a k-node gap.
    for _ in range(k):
        if leader.next is None:
            raise ValueError("k exceeds the length of the list")
        leader = leader.next

    # Move both pointers until the leader reaches the last node; the trailer
    # now sits immediately before the node to remove.
    while leader.next is not None:
        leader = leader.next
        trailer = trailer.next

    assert trailer.next is not None
    trailer.next = trailer.next.next
    return dummy.next


if __name__ == "__main__":
    print(linked_list_to_list(remove_kth_last_node(build_linked_list([1, 2, 3, 4, 5]), 2)))
    print(linked_list_to_list(remove_kth_last_node(build_linked_list([1]), 1)))  # []
