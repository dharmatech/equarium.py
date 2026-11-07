# 000 project setup

**Status:** Done (2026-11-07), in the repository's first commit.

equarium set up as a uv library project, with SymPy, tests and a type
checker. Done in one conversation.

## Why

equarium is a rebuild of
[combine-equations.py](https://github.com/dharmatech/combine-equations.py)
(checked out at `~/src/combine-equations.py`). That library grew one
University Physics example at a time, which worked, but left its code
ad hoc and its examples in several styles. The old repo stays as it is,
as the first experiment, and equarium starts fresh with what it
taught.

## Decisions

- **Names.** The repo folder is `equarium.py`, for a future GitHub repo
  `dharmatech/equarium.py`. The package is `equarium`. Both names were
  free on 2026-11-07, on GitHub and on PyPI.
- **uv for everything:** the environment, dependencies, the build
  backend (`uv_build`) and running tools.
- **Python 3.14,** pinned in `.python-version` and `requires-python`.
  uv defaulted to 3.12 on this machine, so it's set explicitly. The old
  project also required 3.14.
- **A library layout:** `src/equarium/`, with `py.typed` so type
  checkers use the package's annotations.
- **Dependencies:** `sympy`. For development: `pytest`, and `pyright`
  in standard mode, since the user prefers static typing. SymPy's type
  hints are incomplete, so our code is fully typed and the checker
  stays lenient about SymPy calls.
- **Tests from the start.** Each example ported later gets a test that
  checks the textbook's answers.

## What changed

- `uv init --lib --name equarium --python 3.14`: `pyproject.toml`,
  `.python-version`, `.gitignore`, `src/equarium/__init__.py`,
  `src/equarium/py.typed`, and a git repository. Without `--name`, uv
  would have named the package `equarium-py` after the folder.
- `uv add sympy` (1.14.0), and `uv add --dev pytest pyright` (9.2.0 and
  1.1.414), with `uv.lock`.
- `pyproject.toml`: a description, pytest's `testpaths`, and pyright's
  settings (`src` and `tests`, Python 3.14, standard mode).
- `src/equarium/__init__.py`: only a docstring. uv's sample `hello()`
  is gone.
- `tests/test_package.py`: one check that the package imports, so
  pytest has something to run until the first real test.
- `README.md`: what equarium is, where it came from, and the
  development commands.

## What we checked

- `uv run pytest`: 1 passed.
- `uv run pyright`: 0 errors, 0 warnings.

## Next

[001 example catalog](../README.md#series), then the charter for 002
core.
