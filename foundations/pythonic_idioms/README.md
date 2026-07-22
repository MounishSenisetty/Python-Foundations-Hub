# Pythonic Idioms

Writing the Python the language wants you to write. These modules replace
verbose, manual patterns with the concise, purpose-built tools the standard
library already provides.

## Files, in reading order

Read them top to bottom — they move from everyday data access, to resource
management, to a small performance idiom.

| # | File | What it covers |
| --- | --- | --- |
| 1 | [`dictionary_traversal.py`](dictionary_traversal.py) | Idiomatic dict access with `.get()`, `.setdefault()`, and `collections.defaultdict` instead of `if key in mapping` guards. Worked examples: counting, grouping, and inverting mappings. |
| 2 | [`context_managers.py`](context_managers.py) | Building your own `with`-statement support two ways: a class with `__enter__`/`__exit__` (`Stopwatch`) and a generator with `@contextlib.contextmanager` (`temporary_env_var`, `rollback_on_error`). |
| 3 | [`string_building.py`](string_building.py) | Linear string construction with `str.join` versus the O(n²) `+=`-in-a-loop anti-pattern (kept side by side for comparison). |

## How to read each file

1. Start with the **module docstring** at the top — it states the problem and
   the idiom that solves it.
2. Read the functions/classes in order; each docstring explains its `Args`,
   `Returns`, and `Raises`.
3. Run the file to see the demo in the `if __name__ == "__main__"` block:

   ```bash
   python foundations/pythonic_idioms/dictionary_traversal.py
   ```

## Tests

```bash
pytest tests/foundations/test_pythonic_idioms.py -q
```
