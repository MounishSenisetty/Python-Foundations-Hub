# Fast & Slow Pointers

A specialised two-pointer technique where the pointers advance at different
speeds. It detects cycles and locates positional landmarks (like the middle) in
a single pass and constant space.

## Files, in reading order

| # | File | What it covers |
| --- | --- | --- |
| 1 | [`linked_list_loop.py`](linked_list_loop.py) | Floyd's tortoise-and-hare cycle detection. O(n) time, O(1) space. |
| 2 | [`linked_list_midpoint.py`](linked_list_midpoint.py) | Find the middle node in one pass (second middle for even lengths). |
| 3 | [`happy_number.py`](happy_number.py) | Apply cycle detection to a sequence of squared-digit sums. |

## How to read each file

1. Read the **module docstring** for the intuition and complexity.
2. Read the function docstrings for `Args`, `Returns`, and `Raises`.
3. Run the demo:

   ```bash
   python patterns/fast_slow_pointers/linked_list_loop.py
   ```

## Tests

```bash
pytest tests/patterns/test_fast_slow_pointers.py -q
```
