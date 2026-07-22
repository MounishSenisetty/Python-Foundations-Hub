# Patterns

Pattern-wise Data Structures & Algorithms: a curated set of interview-grade
problems grouped by the technique that solves them. Every module is small,
fully type-hinted, documents its intuition and its time/space complexity, and
is directly runnable:

```bash
python patterns/<pattern>/<module>.py
```

Each pattern folder has its own `README.md` with a per-file breakdown and a
suggested reading order. A prose companion guide — when to reach for each
pattern and its real-world uses — lives at
[`docs/patterns/README.md`](../docs/patterns/README.md).

## Suggested reading order

The patterns are ordered from the most broadly applicable to the more
specialised. If you're working through them all, this order builds intuition
step by step:

| # | Pattern | Core idea |
| --- | --- | --- |
| 1 | [`two_pointers/`](two_pointers/) | Converge or chase two indices across a sequence |
| 2 | [`hash_maps_sets/`](hash_maps_sets/) | Trade memory for O(1) lookup |
| 3 | [`linked_lists/`](linked_lists/) | Pointer rewiring with dummy nodes |
| 4 | [`fast_slow_pointers/`](fast_slow_pointers/) | Two pointers moving at different speeds |
| 5 | [`sliding_window/`](sliding_window/) | A moving sub-range with incremental state |
| 6 | [`binary_search/`](binary_search/) | Halve a sorted or monotonic search space |

The patterns are largely independent, so after the two-pointer basics you can
jump to whichever technique you want to drill.

## How to read a module

Every file follows the same layout:

1. **Module docstring** (top) — the problem, the intuition behind the approach,
   and the time/space complexity.
2. **Functions / classes** — each with a Google-style docstring covering
   `Args`, `Returns`, and `Raises`.
3. **`if __name__ == "__main__"` block** (bottom) — a runnable demo on small
   inputs.

## Running the tests

Each pattern is mirrored by a test module under
[`tests/patterns/`](../tests/patterns/):

```bash
pytest tests/patterns -q
```
