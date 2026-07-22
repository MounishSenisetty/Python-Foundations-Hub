# Sliding Window

When the answer concerns a contiguous sub-array or substring, adjacent windows
overlap almost entirely — so update the window's state incrementally instead of
recomputing it. This turns many O(n·k) scans into O(n).

## Files, in reading order

| # | File | What it covers |
| --- | --- | --- |
| 1 | [`substring_anagrams.py`](substring_anagrams.py) | Fixed-size window with frequency arrays to count a pattern's anagrams. |
| 2 | [`longest_substring_unique.py`](longest_substring_unique.py) | Dynamic window for the longest substring with no repeats, using last-seen indices. |
| 3 | [`longest_uniform_substring.py`](longest_uniform_substring.py) | Dynamic window allowing up to `k` character replacements. |

## How to read each file

1. Read the **module docstring** for the intuition and complexity.
2. Read the function docstrings for `Args`, `Returns`, and `Raises`. Note the
   distinction between a *fixed*-size window (module 1) and a *dynamic* one
   (modules 2–3) that grows and shrinks.
3. Run the demo:

   ```bash
   python patterns/sliding_window/longest_substring_unique.py
   ```

## Tests

```bash
pytest tests/patterns/test_sliding_window.py -q
```
