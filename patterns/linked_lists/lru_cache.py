"""A Least Recently Used (LRU) cache with O(1) get and put.

An LRU cache evicts the entry that has gone longest without use once it reaches
capacity. Achieving constant-time operations requires two structures working in
concert: a hash map for O(1) key lookup, and a doubly linked list that keeps
entries ordered by recency so the least-recently-used entry can be evicted in
O(1).

Design:
    The hash map maps each key to its node. The doubly linked list runs from a
    sentinel ``head`` (most recently used side) to a sentinel ``tail`` (least
    recently used side). Every access unlinks a node and re-inserts it next to
    the head; eviction removes the node before the tail.

Time complexity: O(1) for both ``get`` and ``put``.
Space complexity: O(capacity).
"""

from __future__ import annotations

from typing import Dict, Optional


class _Node:
    """An internal doubly linked list node holding one cache entry."""

    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: int = 0, value: int = 0) -> None:
        self.key = key
        self.value = value
        self.prev: Optional["_Node"] = None
        self.next: Optional["_Node"] = None


class LRUCache:
    """A fixed-capacity cache that evicts the least recently used entry.

    Example:
        >>> cache = LRUCache(2)
        >>> cache.put(1, 1)
        >>> cache.put(2, 2)
        >>> cache.get(1)
        1
        >>> cache.put(3, 3)  # evicts key 2, the least recently used
        >>> cache.get(2)
        -1
    """

    def __init__(self, capacity: int) -> None:
        """Initialise the cache.

        Args:
            capacity: The maximum number of entries; must be positive.

        Raises:
            ValueError: If ``capacity`` is not positive.
        """
        if capacity <= 0:
            raise ValueError("capacity must be a positive integer")
        self._capacity = capacity
        self._map: Dict[int, _Node] = {}
        # Sentinel nodes remove edge cases at the ends of the list.
        self._head = _Node()
        self._tail = _Node()
        self._head.next = self._tail
        self._tail.prev = self._head

    def _remove(self, node: _Node) -> None:
        """Unlink ``node`` from the list."""
        assert node.prev is not None and node.next is not None
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node: _Node) -> None:
        """Insert ``node`` just after the head sentinel (most recent)."""
        node.prev = self._head
        node.next = self._head.next
        assert self._head.next is not None
        self._head.next.prev = node
        self._head.next = node

    def get(self, key: int) -> int:
        """Return the value for ``key`` and mark it most recently used.

        Args:
            key: The key to look up.

        Returns:
            The stored value, or ``-1`` if the key is absent.
        """
        node = self._map.get(key)
        if node is None:
            return -1
        self._remove(node)
        self._add_to_front(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        """Insert or update ``key`` with ``value``, evicting if necessary.

        Args:
            key: The key to store.
            value: The value to associate with ``key``.
        """
        existing = self._map.get(key)
        if existing is not None:
            existing.value = value
            self._remove(existing)
            self._add_to_front(existing)
            return

        if len(self._map) >= self._capacity:
            lru = self._tail.prev
            assert lru is not None and lru is not self._head
            self._remove(lru)
            del self._map[lru.key]

        node = _Node(key, value)
        self._map[key] = node
        self._add_to_front(node)


if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    print(cache.get(1))  # 1
    cache.put(3, 3)  # evicts key 2
    print(cache.get(2))  # -1
    print(cache.get(3))  # 3
