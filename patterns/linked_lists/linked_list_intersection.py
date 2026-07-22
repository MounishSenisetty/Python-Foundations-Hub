"""Find the node where two singly linked lists intersect.

Two lists intersect if they share a common tail — from the intersection node
onward, they are the same nodes (by identity, not merely by value). Comparing
every pair of nodes is O(m * n); a hash set of one list's nodes brings that to
O(m + n) time but O(m) space. The two-pointer method achieves O(m + n) time in
constant space.

Intuition:
    Advance one pointer through list A then list B, and another through list B
    then list A. Both pointers traverse exactly ``len(A) + len(B)`` nodes, so
    they arrive at the intersection simultaneously. If the lists do not
    intersect, both reach ``None`` at the same time.

Time complexity: O(m + n).
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


def linked_list_intersection(
    head_a: Optional[ListNode], head_b: Optional[ListNode]
) -> Optional[ListNode]:
    """Return the first shared node of two lists, or ``None``.

    Intersection is by node identity: the returned node is the actual object
    that both lists route through, not simply a node with an equal value.

    Args:
        head_a: Head of the first list.
        head_b: Head of the second list.

    Returns:
        The intersection node if the lists share a tail, otherwise ``None``.
    """
    pointer_a, pointer_b = head_a, head_b
    while pointer_a is not pointer_b:
        pointer_a = pointer_a.next if pointer_a is not None else head_b
        pointer_b = pointer_b.next if pointer_b is not None else head_a
    return pointer_a


if __name__ == "__main__":
    shared = ListNode(8, ListNode(10))
    list_a = ListNode(3, ListNode(7, shared))
    list_b = ListNode(99, shared)
    node = linked_list_intersection(list_a, list_b)
    print(node.val if node else None)  # 8
    print(linked_list_intersection(ListNode(1), ListNode(2)))  # None
