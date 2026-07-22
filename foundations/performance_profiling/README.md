# Performance & Profiling

Measure first, optimise second. These modules show how to benchmark code
honestly and how to spend memory deliberately — only after you have numbers.

## Files, in reading order

Read the benchmarking module first (how to measure), then the optimisation
module (what the measurements justify changing).

| # | File | What it covers |
| --- | --- | --- |
| 1 | [`benchmarking_timeit.py`](benchmarking_timeit.py) | Programmatic micro-benchmarking with `timeit.repeat`: why to report the minimum of several runs, and helpers to `benchmark`, `compare`, and format results. |
| 2 | [`memory_and_complexity.py`](memory_and_complexity.py) | Memory-lean patterns: `__slots__` for compact instances, and generators over eager lists for O(1) peak memory (including a constant-memory sliding-window mean). |

## How to read each file

1. Read the **module docstring** for the measurement or optimisation technique.
2. Read the functions/classes; docstrings note the trade-offs (e.g. `__slots__`
   forbids dynamic attributes; generators are single-pass).
3. Run the file to see live numbers on your machine:

   ```bash
   python foundations/performance_profiling/benchmarking_timeit.py
   python foundations/performance_profiling/memory_and_complexity.py
   ```

   Timing and memory figures vary by machine and Python build — the tests
   assert *relative* behaviour (e.g. slotted instances are smaller), not
   absolute numbers.

## Tests

```bash
pytest tests/foundations/test_performance_profiling.py -q
```
