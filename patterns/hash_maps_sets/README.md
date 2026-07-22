# Hash Maps & Sets

Trade memory for speed: a hash map or set turns a repeated linear search into an
O(1) lookup, collapsing quadratic algorithms to linear ones.

## Files, in reading order

| # | File | What it covers |
| --- | --- | --- |
| 1 | [`pair_sum_unsorted.py`](pair_sum_unsorted.py) | Single-pass two-sum on an unsorted array via a complement map. O(n) time and space. |
| 2 | [`verify_sudoku_board.py`](verify_sudoku_board.py) | Validate a 9x9 Sudoku grid with per-row/column/box sets. |
| 3 | [`zero_striping.py`](zero_striping.py) | Set Matrix Zeroes in place, reusing the first row/column as markers for O(1) auxiliary space. |

## How to read each file

1. Read the **module docstring** for the intuition and complexity.
2. Read the function docstring for `Args`, `Returns`, and `Raises`.
3. Run the demo:

   ```bash
   python patterns/hash_maps_sets/pair_sum_unsorted.py
   ```

## Tests

```bash
pytest tests/patterns/test_hash_maps_sets.py -q
```
