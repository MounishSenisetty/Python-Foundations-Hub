"""Find the middle node of a linked list in a single pass.

Singly linked lists have no random access, so locating the middle by index
would take one pass to measure the length and another to walk halfway. A
fast/slow pointer pair finds it in one pass: when the fast pointer reaches the
end, the slow pointer is at the middle.

Intuition:
    The fast pointer moves twice as quickly as the slow one, so it covers the
    whole list in the time the slow pointer covers half of it. For an
    even-length list this returns the second of the two middle nodes.

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


def linked_list_midpoint(head: Optional[ListNode]) -> Optional[ListNode]:
    """Return the middle node of a linked list.

    For a list of even length, the second of the two middle nodes is returned
    (e.g. the third node of a four-node list).

    Args:
        head: The head of the list.

    Returns:
        The middle node, or ``None`` for an empty list.
    """
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next  # type: ignore[union-attr]
        fast = fast.next.next
    return slow


if __name__ == "__main__":
    node = linked_list_midpoint(build_linked_list([1, 2, 3, 4, 5]))
    print(node.val if node else None)  # 3
    node = linked_list_midpoint(build_linked_list([1, 2, 3, 4]))
    print(node.val if node else None)  # 3
