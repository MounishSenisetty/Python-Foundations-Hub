"""Tests for the ``patterns.fast_slow_pointers`` modules."""

import pytest

from patterns.fast_slow_pointers.happy_number import is_happy
from patterns.fast_slow_pointers.linked_list_loop import ListNode, has_cycle
from patterns.fast_slow_pointers.linked_list_midpoint import (
    build_linked_list,
    linked_list_midpoint,
)


class TestLinkedListLoop:
    def test_detects_cycle(self) -> None:
        a, b, c = ListNode(1), ListNode(2), ListNode(3)
        a.next, b.next, c.next = b, c, a
        assert has_cycle(a) is True

    def test_no_cycle(self) -> None:
        a = ListNode(1, ListNode(2, ListNode(3)))
        assert has_cycle(a) is False

    def test_empty_list(self) -> None:
        assert has_cycle(None) is False

    def test_single_node_no_cycle(self) -> None:
        assert has_cycle(ListNode(1)) is False

    def test_single_node_self_loop(self) -> None:
        node = ListNode(1)
        node.next = node
        assert has_cycle(node) is True


class TestLinkedListMidpoint:
    def test_odd_length(self) -> None:
        node = linked_list_midpoint(build_linked_list([1, 2, 3, 4, 5]))
        assert node is not None and node.val == 3

    def test_even_length_returns_second_middle(self) -> None:
        node = linked_list_midpoint(build_linked_list([1, 2, 3, 4]))
        assert node is not None and node.val == 3

    def test_single_node(self) -> None:
        node = linked_list_midpoint(build_linked_list([9]))
        assert node is not None and node.val == 9

    def test_two_nodes(self) -> None:
        node = linked_list_midpoint(build_linked_list([1, 2]))
        assert node is not None and node.val == 2

    def test_empty_list(self) -> None:
        assert linked_list_midpoint(None) is None


class TestHappyNumber:
    def test_happy_number(self) -> None:
        assert is_happy(19) is True

    def test_one_is_happy(self) -> None:
        assert is_happy(1) is True

    def test_unhappy_number(self) -> None:
        assert is_happy(2) is False

    def test_another_happy_number(self) -> None:
        assert is_happy(7) is True

    def test_invalid_input(self) -> None:
        with pytest.raises(ValueError):
            is_happy(0)
        with pytest.raises(ValueError):
            is_happy(-19)
