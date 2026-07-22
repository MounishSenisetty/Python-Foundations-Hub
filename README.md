# Python-Foundations-Hub

A beginner-first, modular collection of **Data Structures**, **Algorithms**, and
**Machine Learning basics**, implemented in clean, well-documented Python.

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-orange)
![First Timers Friendly](https://img.shields.io/badge/first--timers-friendly-blueviolet)

## What is this?

Python-Foundations-Hub is a library of small, focused Python modules covering:

- **`algorithms/`** — sorting, searching, and math algorithms (e.g. bubble sort,
  binary search, GCD).
- **`data_structures/`** — classic data structures (e.g. linked lists, stacks,
  queues, trees).
- **`ml_basics/`** — small, dependency-light machine learning utilities, including
  common **metrics** and **preprocessing** helpers.
- **`foundations/`** — clean-code and best-practice modules: Pythonic idioms,
  common gotchas, effective function design, idiomatic OOP, and performance
  profiling (see the [foundations reference guide](docs/foundations/README.md)).

Every single file in this project follows the same contract:

- ✅ **Type hints** on every function signature.
- ✅ A clear **docstring** explaining what the function does, its arguments, and
  its return value.
- ✅ A **matching test file** in `tests/` that mirrors its location in the source
  tree, so it's easy to find and easy to verify.

This makes the codebase predictable to read, safe to extend, and — most
importantly — a great place to make your first open-source contribution.

## 🌱 A safe space for first-time contributors

**This project exists for you.** If you have never opened a pull request before,
you are exactly who we built this for.

- **No question is too basic.** Ask it in the issue, ask it in the PR, ask it in
  discussions. We'd rather answer ten "obvious" questions than watch someone
  give up in silence.
- **Every task is isolated.** Thanks to our one-file-per-contribution design (see
  below), you can work on your own file without worrying about stepping on
  someone else's changes or waiting on a shared "registry" file to be free.
  Twenty people can be contributing at the same time, on twenty different
  files, with zero merge conflicts.
- **Reviews are for learning, not gatekeeping.** Expect kind, specific feedback
  aimed at helping you grow — not at making you feel small. Maintainers are here
  to help you get your first (or fiftieth) PR merged.

Ready to jump in? Head over to [CONTRIBUTING.md](CONTRIBUTING.md) for a
step-by-step guide written for absolute beginners, and check the
[good first issue](../../issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
label for a task to claim.

## Local setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/Python-Foundations-Hub.git
   cd Python-Foundations-Hub
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**

   macOS / Linux:

   ```bash
   source venv/bin/activate
   ```

   Windows (PowerShell):

   ```powershell
   venv\Scripts\activate
   ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the test suite**

   ```bash
   pytest
   ```

If all tests pass, you're ready to start contributing!

## Project structure

```
Python-Foundations-Hub/
├── algorithms/          # sorting/, searching/, math/ — one algorithm per file
├── data_structures/      # one data structure per file
├── ml_basics/            # metrics/, preprocessing/ — small ML utilities
├── foundations/          # clean-code idioms, gotchas, OOP, profiling
├── tests/                 # mirrors the structure above, 1:1
├── docs/foundations/     # clean-code developer reference guide
├── docs/translations/    # community-contributed README translations
└── .github/               # issue templates, PR template, CI workflow
```

Every folder's `__init__.py` is intentionally **empty** and stays that way —
there is no central registry file to edit, so your contribution never conflicts
with anyone else's.

## Contributing

We'd love your help! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for the full,
beginner-friendly walkthrough — from claiming an issue to opening your first pull
request.

## License

This project is licensed under the [MIT License](LICENSE).
