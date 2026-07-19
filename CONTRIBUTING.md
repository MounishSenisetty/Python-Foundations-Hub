# Contributing to Python-Foundations-Hub

Welcome! 👋 This guide is written for **absolute beginners** — if this is your
very first open-source contribution, you're in the right place. Follow the
steps in order and you'll have a pull request open in no time.

If you get stuck at any point, that's completely normal. Ask a question on the
issue — no question is too basic here.

## 1. Claim an issue

Browse the [Issues tab](../../issues) and look for one labeled
**`good first issue`**. Leave a comment like "I'd like to work on this!" so
others know it's taken, and wait for a maintainer to assign it to you before
you start coding. This avoids two people accidentally working on the same
file.

## 2. Fork the repository

Click the **Fork** button at the top-right of the repository page. This
creates your own copy of the project under your GitHub account.

## 3. Clone your fork

```bash
git clone https://github.com/<your-username>/Python-Foundations-Hub.git
cd Python-Foundations-Hub
```

## 4. Create a branch

Always work on a new branch, never directly on `main`:

```bash
git checkout -b add-linear-search
```

Pick a short, descriptive branch name related to your task.

## 5. Set up your virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 6. Write your code

Every file in this project follows the same two rules: **type hints** on every
function, and a **Google-style docstring**. Here's a complete example of a
`linear_search` implementation to use as a template:

```python
def linear_search(items: list[int], target: int) -> int:
    """Search for a target value by checking each item in order.

    Args:
        items: The list of integers to search through.
        target: The value to look for.

    Returns:
        The index of the first occurrence of target in items, or -1 if
        the value is not found.
    """
    for index, value in enumerate(items):
        if value == target:
            return index
    return -1
```

A few things to notice:

- Every argument and the return value have type hints.
- The docstring has a one-line summary, an `Args:` section, and a `Returns:`
  section.
- The function does exactly one thing.

Place your file in the correct folder (e.g. `algorithms/searching/linear_search.py`)
and leave the matching `__init__.py` file **empty** — never add imports or
registrations to it.

## 7. Write a test

Add a test file that mirrors your source file's path, under `tests/`. For the
example above, that's `tests/algorithms/searching/test_linear_search.py`:

```python
from algorithms.searching.linear_search import linear_search


def test_linear_search_found() -> None:
    assert linear_search([4, 2, 7, 1], 7) == 2


def test_linear_search_not_found() -> None:
    assert linear_search([4, 2, 7, 1], 99) == -1
```

## 8. Run the tests

```bash
pytest
```

Make sure every test passes before moving on. You can also run the linter
locally:

```bash
ruff check .
```

## 9. Commit your changes

Use a [conventional commit](https://www.conventionalcommits.org/) prefix so
your commit history is easy to scan:

- `feat:` for a new algorithm/data structure/utility
- `test:` for test-only changes
- `docs:` for documentation-only changes

```bash
git add algorithms/searching/linear_search.py tests/algorithms/searching/test_linear_search.py
git commit -m "feat: add linear search algorithm"
```

## 10. Push your branch

```bash
git push -u origin add-linear-search
```

## 11. Open a Pull Request

Go to your fork on GitHub — you'll see a prompt to **Compare & pull request**.
Fill in the PR template, and make sure to include:

```
Closes #<IssueNumber>
```

Replace `<IssueNumber>` with the number of the issue you claimed in step 1
(e.g. `Closes #42`). This automatically links your PR to the issue and closes
it once your PR is merged.

## A note on code review

Code review here is about **learning, not gatekeeping**. If a maintainer
leaves comments on your PR, it doesn't mean you did something wrong — it means
we're taking the time to help you make it even better. Ask questions, push
back if something's unclear, and treat it as a conversation. Everyone who
reviews your code once wrote their first PR too.

Welcome aboard, and thank you for contributing! 🎉
