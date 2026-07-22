# Code Smells & Gotchas

Traps that compile and run fine, then bite later — often far from where the
mistake was made. Each module keeps the buggy version alongside the fix so you
can see both, and the tests assert the buggy behaviour so the demonstration
stays honest.

## Files, in reading order

These are independent, but the suggested order runs from the most notorious
Python gotcha to the more situational ones.

| # | File | What it covers |
| --- | --- | --- |
| 1 | [`mutable_defaults.py`](mutable_defaults.py) | The mutable default argument trap (`def func(val=[])`): why the default is shared across calls, and the `None`-sentinel and private-sentinel fixes. |
| 2 | [`float_precision.py`](float_precision.py) | Why `0.1 + 0.2 != 0.3`, comparing floats with `math.isclose`, and exact money handling with `decimal.Decimal` (including an exact bill-splitter). |
| 3 | [`shadow_variables.py`](shadow_variables.py) | Refactoring variables that shadow built-ins (`list`, `dict`, `str`, `type`) and the crashes that shadowing causes further down the scope. |

## How to read each file

1. Read the **module docstring** for the trap being demonstrated.
2. Note the deliberately "broken" helper (e.g. `append_to_shared`,
   `naive_float_equal`) — its docstring flags it as an anti-pattern — then read
   the corrected version that follows.
3. Run the file to watch the difference:

   ```bash
   python foundations/code_smells_and_gotchas/mutable_defaults.py
   ```

## Tests

```bash
pytest tests/foundations/test_code_smells_and_gotchas.py -q
```
