# Effective Functions

Designing functions that are easy to reuse, compose, and reason about — from
flexible argument handling to pure-function pipelines and precise type
contracts.

## Files, in reading order

Read them in this order: mechanics of arguments first, then how to combine
functions, then how to type them precisely.

| # | File | What it covers |
| --- | --- | --- |
| 1 | [`variadic_wrappers.py`](variadic_wrappers.py) | `*args`/`**kwargs` unpacking, transparent argument forwarding, and the decorator pattern with `functools.wraps` (`call_with_retries`, `record_calls`, `memoize`). |
| 2 | [`higher_order_pipeline.py`](higher_order_pipeline.py) | Pure functions, `map`/`filter` versus list comprehensions, and function composition (`compose` right-to-left, `pipeline` left-to-right). |
| 3 | [`typed_contracts.py`](typed_contracts.py) | Expressing contracts with `typing`: `Callable`, `TypeVar`, `Generic`, and `Optional`. |

## How to read each file

1. Read the **module docstring** for the design idea being demonstrated.
2. Walk through the functions/classes; each docstring documents `Args`,
   `Returns`, and `Raises`. Pay attention to how `variadic_wrappers.py`
   forwards arguments unchanged — that mechanism underpins every wrapper.
3. Run the file to see the demo:

   ```bash
   python foundations/effective_functions/higher_order_pipeline.py
   ```

## Tests

```bash
pytest tests/foundations/test_effective_functions.py -q
```
