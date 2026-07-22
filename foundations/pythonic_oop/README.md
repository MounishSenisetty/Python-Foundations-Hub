# Pythonic OOP

Writing classes that feel like native Python: encapsulation without ceremony,
containers that support the built-in protocols, and flexible design through
composition rather than deep inheritance.

## Files, in reading order

Read them from the smallest concept (a single attribute) up to whole-design
structure.

| # | File | What it covers |
| --- | --- | --- |
| 1 | [`properties_and_validation.py`](properties_and_validation.py) | Encapsulation with `@property` and `@<attr>.setter` for validation and computed/read-only attributes — no Java-style `get_x()`/`set_x()` methods (`Thermostat`, `BankAccount`). |
| 2 | [`dunder_collections.py`](dunder_collections.py) | A custom container implementing `__len__`, `__getitem__`, `__iter__`, `__contains__`, `__eq__`, and `__repr__` so it supports `len()`, indexing, slicing, `for`, and `in` (`Bookshelf`). |
| 3 | [`composition_vs_inheritance.py`](composition_vs_inheritance.py) | Refactoring a deep class hierarchy into small, dependency-injected collaborators combined at runtime, with a `typing.Protocol` describing the interface structurally. |

## How to read each file

1. Read the **module docstring** for the OOP principle being demonstrated.
2. Read the class(es); docstrings cover construction, each method, and what it
   `Raises`. Notice how properties keep the call site simple
   (`account.balance`) while enforcing invariants behind the scenes.
3. Run the file to see the demo:

   ```bash
   python foundations/pythonic_oop/dunder_collections.py
   ```

## Tests

```bash
pytest tests/foundations/test_pythonic_oop.py -q
```
