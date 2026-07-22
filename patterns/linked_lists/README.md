# Linked Lists

Pointer rewiring on singly and doubly linked lists. A recurring trick here is
the *dummy head* node, which removes the special case where the first node
changes.

Each module defines its own small `ListNode` and the helpers
`build_linked_list` / `linked_list_to_list`, so every file stands alone.

## Files, in reading order

| # | File | What it covers |
| --- | --- | --- |
| 1 | [`linked_list_reversal.py`](linked_list_reversal.py) | Reverse a list iteratively (O(1) space) and recursively (O(n) stack). |
| 2 | [`remove_kth_last_node.py`](remove_kth_last_node.py) | Remove the k-th node from the end in one pass with a leader/trailer pair and a dummy node. |
| 3 | [`linked_list_intersection.py`](linked_list_intersection.py) | Find the shared-tail node of two lists with two pointers, O(1) space. |
| 4 | [`lru_cache.py`](lru_cache.py) | An O(1) LRU cache combining a hash map with a doubly linked list. |

## How to read each file

1. Read the **module docstring** for the intuition and complexity.
2. Read the class/function docstrings for `Args`, `Returns`, and `Raises`.
3. Run the demo:

   ```bash
   python patterns/linked_lists/lru_cache.py
   ```

## Tests

```bash
pytest tests/patterns/test_linked_lists.py -q
```
