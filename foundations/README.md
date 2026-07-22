# Foundations

A hands-on tour of Python clean-code practices, common gotchas, and
performance awareness — in the spirit of *Beyond the Basic Stuff with Python*.
Every module is small, fully type-hinted, documented with Google-style
docstrings, and directly runnable:

```bash
python foundations/<package>/<module>.py
```

Each package has its own `README.md` with a per-file breakdown and reading
order. A prose companion guide lives at
[`docs/foundations/README.md`](../docs/foundations/README.md).

## Suggested reading order

The packages build on one another. If you're working through the whole track,
read them in this order:

| # | Package | What you'll learn |
| --- | --- | --- |
| 1 | [`pythonic_idioms/`](pythonic_idioms/) | Writing the Python the language wants you to write |
| 2 | [`code_smells_and_gotchas/`](code_smells_and_gotchas/) | Traps that run fine and bite later |
| 3 | [`effective_functions/`](effective_functions/) | Function design, composition, and typed contracts |
| 4 | [`pythonic_oop/`](pythonic_oop/) | Objects that behave like native Python |
| 5 | [`performance_profiling/`](performance_profiling/) | Measure first, optimise second |

Packages 1–2 are foundational and worth reading first. Packages 3–5 are largely
independent of each other, so after the basics you can jump to whichever topic
you need.

## How to read a module

Every file follows the same shape, so once you've read one you know the layout
of all of them:

1. **Module docstring** (top of file) — the "why": the problem the module
   addresses and the rule of thumb it teaches.
2. **Functions / classes** — each with a Google-style docstring covering
   `Args`, `Returns`, and `Raises`. Where a concept has a right and a wrong
   way, the anti-pattern is kept alongside the fix and clearly labelled.
3. **`if __name__ == "__main__"` block** (bottom) — a runnable demo. Execute the
   file to see the ideas in action.

## Running the tests

Each package is mirrored by a test module under
[`tests/foundations/`](../tests/foundations/). Run everything with:

```bash
pytest tests/foundations -q
```

Or target a single package, e.g.:

```bash
pytest tests/foundations/test_pythonic_idioms.py -q
```
