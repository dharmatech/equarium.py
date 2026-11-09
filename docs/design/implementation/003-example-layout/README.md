# 003 example layout

**Status:** Done (2026-11-08). Done in one conversation, the one that
managed 002's last checkpoint.

Each example, exercise and table under `examples/up_15e/` moved into a
folder of its own. Nothing in a module changed but its imports, its run
command and the few lines that named other modules.

## Why

After 002, each chapter folder held its modules side by side:
`ch02/example_2_5.py`, `ch02/example_2_5_step_by_step.py`, and so on.
A folder per problem gives each one a place for its versions, its notes
and any diagrams we draw. The old library had folders for most
problems, but not all of chapter 3. The user wanted this before the
physics redesign, which will touch every example anyway.

## Decisions *(user)*

- **A folder per problem, in a folder per kind:** `ch02/examples/n04/`
  is Example 2.4, `ch02/exercises/n003/` is Exercise 2.3, and
  `ch02/tables/n05/` is Table 2.5.
- **The file names don't repeat the path.** A folder's main version is
  `main.py`. A version in another style adds the slug:
  `main_handwritten.py`, `main_step_by_step.py`, `main_two_steps.py`.
  The cost is that an editor tab shows only `main.py`, which the user
  accepted as a tooling issue. Each module's docstring names its
  problem on its first line.
- **An `n` before the number,** because a folder named `04` isn't a
  Python identifier. `python -m` would run it, but
  `from examples.up_15e.ch02.examples.07.main import ball` is a syntax
  error, and Example 2.8, 4.1 step by step and the tests import that
  way. The other prefixes considered were `ex04` (slightly redundant
  under `examples/`) and `_04` (reads as private).
- **Two digits for examples, three for exercises.** A chapter's
  end-of-chapter numbering runs through its exercises, problems,
  challenge problems and passage problems. Chapter 5's goes to 5.118 in
  the 15th edition's PDF. A chapter has only a dozen or so examples.
- **Each folder is a package.** Its `__init__.py` is a docstring, with
  the problem's number and the catalog's title. For a group folder, it
  says how its folders are numbered.
- **The book's figures still stay out.** The catalog's rule holds: the
  old repo's PNGs are the publisher's, so a module names its figure in
  its docstring. Diagrams we draw ourselves can go in the folder.

## What changed

- **`git mv` for all 29 modules,** so `git log --follow` keeps their
  history:

  | Was, under `examples/up_15e/` | Now |
  |---|---|
  | `ch02/example_2_4.py`, `example_2_4_handwritten.py` | `ch02/examples/n04/main.py`, `main_handwritten.py` |
  | `ch02/example_2_5.py`, `example_2_5_step_by_step.py`, `example_2_5_handwritten.py`, `example_2_5_handwritten_step_by_step.py` | `ch02/examples/n05/main.py`, `main_step_by_step.py`, `main_handwritten.py`, `main_handwritten_step_by_step.py` |
  | `ch02/example_2_6.py`, `example_2_7.py`, `example_2_8.py` | `ch02/examples/n06/main.py`, `n07/main.py`, `n08/main.py` |
  | `ch02/exercise_2_1.py` | `ch02/exercises/n001/main.py` |
  | `ch02/exercise_2_3.py`, `exercise_2_3_two_steps.py` | `ch02/exercises/n003/main.py`, `main_two_steps.py` |
  | `ch02/exercise_2_5.py`, `exercise_2_19.py`, `exercise_2_21.py`, `exercise_2_23.py` | `ch02/exercises/n005/main.py`, `n019/main.py`, `n021/main.py`, `n023/main.py` |
  | `ch02/table_2_5.py` | `ch02/tables/n05/main.py` |
  | `ch03/example_3_6.py` to `example_3_13.py` | `ch03/examples/n06/main.py`, `n07/`, `n08/`, `n09/`, `n10/`, `n13/` |
  | `ch04/example_4_1.py`, `example_4_1_step_by_step.py` | `ch04/examples/n01/main.py`, `main_step_by_step.py` |
  | `ch04/example_4_4.py` | `ch04/examples/n04/main.py` |
  | `ch04/example_4_5.py`, `example_4_5_two_steps.py` | `ch04/examples/n05/main.py`, `main_two_steps.py` |
  | `ch04/example_4_7.py` | `ch04/examples/n07/main.py` |

- **27 new `__init__.py` files:** one for each problem folder, and one
  for each chapter's `examples/`, `exercises/` and `tables/`.
- **Inside the modules:** the run command in each docstring, Example
  2.8's import of 2.7's base, and 4.1 step by step's import of 4.1's
  forces. 2.7's docstring and 4.1 step by step's docstring and one
  comment named a module the old way: now "which is `n08/main.py`" and
  "`main.py`, beside it".
- **`tests/test_examples.py`** finds the examples by where they are,
  not by name: every module, not package, whose parent's parent is an
  `examples/` or `exercises/` folder. `tables/` stays out, as
  `table_2_5.py` did, since it has no `BOOK`. Its list of expected
  names and its slow set, `tests/slow_examples.py`, use the new names.
- **The other tests' imports:** `test_display.py`, `test_old_outputs.py`
  (its module column and `OLD_GIVENS`), `test_rewrite.py`,
  `test_roots.py`, `test_solve.py`, `test_strategies.py` and
  `test_table_2_5.py`. `tests/example_2_4.py`, the written-out 2.4 the
  core's tests share, isn't an example module and keeps its name.
- **Docs:**
  - the package `README.md`: the run commands, and a sentence on the
    layout;
  - the catalog's Index: its "In equarium" column names the new
    folders;
  - the spec: a dated note under "Examples in the repo";
  - 002's README: a dated note under "What's next";
  - the series map: this series.

  The checkpoints and the catalog's per-problem entries keep the old
  names, as written at the time. The table above translates them.

## What we checked

- `uv run pytest`: 263 passed, 8 slow deselected, the same counts as
  before the move. 28 modules are found as examples, each with its
  `BOOK`.
- `uv run pytest -m slow`: 8 passed.
- `uv run pyright`: 0 errors, 0 warnings.
- All 29 modules run with `uv run python -m`, each under the command its
  docstring gives.

## Next

The physics redesign, as a new series, when the user chooses. See
[002's "What's next"](../002-core/README.md#whats-next).
