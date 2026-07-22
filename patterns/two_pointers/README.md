# Two Pointers

Replace an O(n²) nested scan with two indices that move across a sequence —
converging from the ends, or advancing under a rule that lets you rule out whole
regions.

## Files, in reading order

| # | File | What it covers |
| --- | --- | --- |
| 1 | [`pair_sum_sorted.py`](pair_sum_sorted.py) | Two-sum on a sorted array by converging pointers from both ends. O(n) time, O(1) space. |
| 2 | [`triplet_sum.py`](triplet_sum.py) | 3-Sum in O(n²): fix one element, two-pointer the rest, skip duplicates. |
| 3 | [`is_palindrome_valid.py`](is_palindrome_valid.py) | Validate a palindrome in place, skipping non-alphanumeric characters. |
| 4 | [`largest_container.py`](largest_container.py) | Container With Most Water by shrinking inward from the widest pair. |

## How to read each file

1. Read the **module docstring** for the intuition and complexity.
2. Read the function docstring for `Args`, `Returns`, and `Raises`.
3. Run the demo:

   ```bash
   python patterns/two_pointers/pair_sum_sorted.py
   ```

## Tests

```bash
pytest tests/patterns/test_two_pointers.py -q
```
