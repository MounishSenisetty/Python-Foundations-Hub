"""Tests for the ``patterns.linked_lists`` modules."""

import pytest

from patterns.linked_lists.linked_list_intersection import (
    ListNode as IntersectionNode,
)
from patterns.linked_lists.linked_list_intersection import (
    linked_list_intersection,
)
from patterns.linked_lists.linked_list_reversal import (
    build_linked_list,
    linked_list_to_list,
    reverse_iterative,
    reverse_recursive,
)
from patterns.linked_lists.lru_cache import LRUCache
from patterns.linked_lists.remove_kth_last_node import (
    build_linked_list as build_kth,
)
from patterns.linked_lists.remove_kth_last_node import (
    linked_list_to_list as kth_to_list,
)
from patterns.linked_lists.remove_kth_last_node import remove_kth_last_node


class TestLinkedListReversal:
    def test_iterative_reversal(self) -> None:
        head = build_linked_list([1, 2, 3, 4, 5])
        assert linked_list_to_list(reverse_iterative(head)) == [5, 4, 3, 2, 1]

    def test_recursive_reversal(self) -> None:
        head = build_linked_list([1, 2, 3])
        assert linked_list_to_list(reverse_recursive(head)) == [3, 2, 1]

    def test_single_node(self) -> None:
        assert linked_list_to_list(reverse_iterative(build_linked_list([7]))) == [7]
        assert linked_list_to_list(reverse_recursive(build_linked_list([7]))) == [7]

    def test_empty_list(self) -> None:
        assert reverse_iterative(None) is None
        assert reverse_recursive(None) is None


class TestRemoveKthLastNode:
    def test_remove_middle(self) -> None:
        head = build_kth([1, 2, 3, 4, 5])
        assert kth_to_list(remove_kth_last_node(head, 2)) == [1, 2, 3, 5]

    def test_remove_tail(self) -> None:
        head = build_kth([1, 2, 3])
        assert kth_to_list(remove_kth_last_node(head, 1)) == [1, 2]

    def test_remove_head(self) -> None:
        head = build_kth([1, 2, 3])
        assert kth_to_list(remove_kth_last_node(head, 3)) == [2, 3]

    def test_single_node(self) -> None:
        assert kth_to_list(remove_kth_last_node(build_kth([1]), 1)) == []

    def test_invalid_k(self) -> None:
        with pytest.raises(ValueError):
            remove_kth_last_node(build_kth([1, 2, 3]), 0)
        with pytest.raises(ValueError):
            remove_kth_last_node(build_kth([1, 2, 3]), 4)


class TestLinkedListIntersection:
    def test_intersecting_lists(self) -> None:
        shared = IntersectionNode(8, IntersectionNode(10))
        list_a = IntersectionNode(3, IntersectionNode(7, shared))
        list_b = IntersectionNode(99, shared)
        assert linked_list_intersection(list_a, list_b) is shared

    def test_non_intersecting_lists(self) -> None:
        list_a = IntersectionNode(1, IntersectionNode(2))
        list_b = IntersectionNode(3, IntersectionNode(4))
        assert linked_list_intersection(list_a, list_b) is None

    def test_one_empty_list(self) -> None:
        assert linked_list_intersection(None, IntersectionNode(1)) is None

    def test_identical_head(self) -> None:
        shared = IntersectionNode(5)
        assert linked_list_intersection(shared, shared) is shared


class TestLRUCache:
    def test_basic_get_put(self) -> None:
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        assert cache.get(1) == 1

    def test_eviction_of_least_recently_used(self) -> None:
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        assert cache.get(1) == 1  # 1 is now most recent
        cache.put(3, 3)  # evicts 2
        assert cache.get(2) == -1
        assert cache.get(3) == 3

    def test_update_existing_key(self) -> None:
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(1, 10)
        assert cache.get(1) == 10

    def test_missing_key_returns_minus_one(self) -> None:
        cache = LRUCache(1)
        assert cache.get(42) == -1

    def test_capacity_one_evicts_immediately(self) -> None:
        cache = LRUCache(1)
        cache.put(1, 1)
        cache.put(2, 2)
        assert cache.get(1) == -1
        assert cache.get(2) == 2

    def test_invalid_capacity(self) -> None:
        with pytest.raises(ValueError):
            LRUCache(0)
