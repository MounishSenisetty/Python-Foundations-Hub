# Binary Search

Halve the search space at every step. Beyond finding a value in a sorted array,
the pattern applies to any *monotonic* predicate over a range of candidate
answers — "search on the answer."

## Files, in reading order

| # | File | What it covers |
| --- | --- | --- |
| 1 | [`find_insertion_index.py`](find_insertion_index.py) | Lower-bound search: find a target or where it would be inserted. |
| 2 | [`first_last_occurrences.py`](first_last_occurrences.py) | Lower- and upper-bound searches to bracket duplicates. |
| 3 | [`cutting_wood.py`](cutting_wood.py) | Binary search on the *answer range* of a monotonic yield function. |
| 4 | [`target_in_rotated_array.py`](target_in_rotated_array.py) | Modified search that identifies which half is sorted. |

## How to read each file

1. Read the **module docstring** for the intuition and complexity.
2. Read the function docstrings for `Args`, `Returns`, and `Raises`. Modules 1–2
   search over array *indices*; module 3 searches over a *value range*; module 4
   adapts the invariant to a rotated array.
3. Run the demo:

   ```bash
   python patterns/binary_search/find_insertion_index.py
   ```

## Tests

```bash
pytest tests/patterns/test_binary_search.py -q
```
