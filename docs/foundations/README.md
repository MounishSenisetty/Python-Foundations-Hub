# Clean Code Foundations — Developer Reference

A practical reference for the modules under [`foundations/`](../../foundations),
covering Pythonic conventions, effective function design, object-oriented
patterns, and performance awareness. Each section links the runnable module and
its matching test file, and every module can also be executed directly
(`python foundations/<package>/<module>.py`) to see a small demo.

## Contents

| Package | Modules | Theme |
| --- | --- | --- |
| `pythonic_idioms/` | `dictionary_traversal`, `context_managers`, `string_building` | Writing the Python the language wants you to write |
| `code_smells_and_gotchas/` | `mutable_defaults`, `float_precision`, `shadow_variables` | Traps that compile fine and bite later |
| `effective_functions/` | `variadic_wrappers`, `higher_order_pipeline`, `typed_contracts` | Function design, composition, and typed contracts |
| `pythonic_oop/` | `properties_and_validation`, `dunder_collections`, `composition_vs_inheritance` | Objects that behave like native Python |
| `performance_profiling/` | `benchmarking_timeit`, `memory_and_complexity` | Measure first, optimise second |

---

## Pythonic idioms

### Dictionary access without key-check boilerplate

Prefer the purpose-built tools over `if key in mapping` guards:

| Situation | Tool |
| --- | --- |
| Read with a fallback, no insertion | `mapping.get(key, default)` |
| Read-or-insert, then mutate in place | `mapping.setdefault(key, [])` |
| Every access should auto-initialise | `collections.defaultdict(factory)` |

```python
# before
if letter in groups:
    groups[letter].append(word)
else:
    groups[letter] = [word]

# after
groups.setdefault(letter, []).append(word)
```

See `pythonic_idioms/dictionary_traversal.py` for counting, grouping, and
mapping-inversion examples of all three.

### Context managers for guaranteed cleanup

Two ways to build your own `with` support:

- **Class-based** (`__enter__`/`__exit__`) when the manager carries state the
  caller inspects afterwards — see `Stopwatch`.
- **`@contextlib.contextmanager`** for linear setup/teardown pairs — the code
  before `yield` is setup, the `finally` block after it is teardown — see
  `temporary_env_var` and `rollback_on_error`.

Return `False` (or nothing) from `__exit__` so exceptions propagate; silently
swallowing them is its own smell.

### String building

String concatenation with `+=` in a loop is O(n²) because every step copies the
accumulated string. Collect parts in a list and call `"".join(parts)` once —
O(n), and the idiom reviewers expect. `string_building.py` keeps the slow
version alongside the fast one so the equivalence is testable and the speed
difference benchmarkable.

---

## Code smells & gotchas

### Mutable default arguments

Defaults are evaluated **once**, at `def` time:

```python
def append_to(item, bucket=[]):   # one shared list for every call!
    bucket.append(item)
    return bucket
```

Fix with the `None` sentinel (`bucket=None`, create inside the body), or a
private `object()` sentinel when `None` is itself a valid input. Both fixes —
and the preserved bug, for demonstration — live in `mutable_defaults.py`.

### Floating-point precision

`0.1 + 0.2 == 0.3` is `False`: binary floats cannot represent most decimal
fractions. Ground rules:

- Compare floats with `math.isclose`, never `==`.
- Handle money with `decimal.Decimal` constructed **from strings** —
  `Decimal(0.1)` faithfully copies the float's error.
- Round explicitly with `quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)`;
  the default is bankers' rounding, which surprises retail code.

`float_precision.py` includes an exact bill-splitter whose shares always sum
back to the original total.

### Shadowing built-ins

Naming a variable `list`, `dict`, `str`, or `type` rebinds the built-in for the
rest of the scope; the crash arrives later, on an unrelated line. Prefer a more
descriptive name (`items`, `mapping`, `text`), then a domain name, and only as
a last resort PEP 8's trailing underscore (`type_`). `shadow_variables.py`
documents each refactor next to the collision it removed.

---

## Effective functions

### `*args`, `**kwargs`, and wrappers

`(*args, **kwargs)` forwarding is the backbone of every transparent wrapper:
retry helpers, call recorders, and decorators all pass arguments through
without restating the wrapped signature. Always pair a decorator with
`functools.wraps` so `__name__`/`__doc__` survive wrapping — see
`variadic_wrappers.py` for `call_with_retries`, `record_calls`, and a minimal
`memoize`.

### Pure functions and composition

Pure functions (no globals, no argument mutation, no I/O) compose safely.
`higher_order_pipeline.py` shows the same transformation as `map`/`filter` over
named functions and as a comprehension — use `map`/`filter` when named
functions already exist, comprehensions when the logic is an inline expression
— plus `compose` (right-to-left, mathematical) and `pipeline` (left-to-right,
reading order).

### Typed contracts

- `Callable[[X], Y]` states the contract of a function argument.
- `TypeVar` links inputs to outputs without collapsing to `Any`.
- `Generic[T]` parameterises containers (`TypedRegistry[int]`).
- `Optional[X]` makes the "not found" case explicit instead of surprising.

`typed_contracts.py` exercises all four on small, checkable helpers.

---

## Pythonic OOP

### Properties instead of getters and setters

Start with plain attributes; introduce `@property` only when validation or
computation is genuinely needed — callers keep writing `unit.celsius = 25.0`
either way. `properties_and_validation.py` covers validated read/write
properties, computed read-only properties, and invariant-guarding methods
(`BankAccount` never exposes a settable balance).

### Dunder methods make containers feel native

Implementing `__len__`, `__getitem__`, `__iter__`, `__contains__`, `__eq__`,
and `__repr__` gives a class `len()`, indexing, slicing, `for` loops, `in`
tests, and honest comparisons — without inheriting from `list`. `Bookshelf` in
`dunder_collections.py` also shows two finer points: slices return a
`Bookshelf` (staying in the domain), and `__eq__` returns `NotImplemented` for
foreign types instead of guessing.

### Composition over inheritance

A hierarchy like `Notifier → EmailNotifier → RetryingEmailNotifier → ...`
doubles in size with every new behaviour. The refactor in
`composition_vs_inheritance.py` models each concern as a small object injected
through `__init__`: any channel, wrapped (or not) in `RetryingChannel`,
observed (or not) by a callback — combined at runtime and each piece testable
with a trivial fake. A `typing.Protocol` documents the collaborator interface
structurally, with no shared base class required.

---

## Performance & profiling

### Benchmark with `timeit`, not `time.time()`

`timeit` runs the target many times, disables the garbage collector, and uses
the best available clock. Report the **minimum** of several repeats and compare
contenders under identical iteration counts. `benchmarking_timeit.py` wraps
this into `benchmark`/`compare`/`format_comparison` for callables.

### Spend memory deliberately

- `__slots__` removes the per-instance `__dict__`: significantly smaller
  instances for classes created in bulk, at the cost of dynamic attributes.
- Generators (`yield`, generator expressions) stream values one at a time:
  O(1) peak memory instead of O(n), at the cost of single-pass consumption.

`memory_and_complexity.py` measures the `__slots__` savings with
`sys.getsizeof` and contrasts eager list building with lazy generation,
including a constant-memory sliding-window mean.

---

## Testing conventions

Every module has a matching test file under
[`tests/foundations/`](../../tests/foundations) covering the happy path, edge
cases (empty inputs, boundary windows), and negative cases (invalid property
assignments, float money rejection, exhausted retries). Run them with:

```bash
pytest tests/foundations -q
```
