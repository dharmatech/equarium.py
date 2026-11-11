# constant acceleration 002: the audit

**Status:** Written (2026-11-11), not built.

If you've been told to read this file, this is the whole assignment.
Build it, check it, commit it, report, and stop.

## Goal

Checkpoint 001 gave every edge in every example a
`constant_acceleration()`, so that no result would change. This
checkpoint keeps it only where the problem has constant acceleration,
and says why in a comment next to each call, in the problem's own
words, as the book's IDENTIFY step would. Where a problem doesn't have
it, the call goes, and a comment says why.

The audit is done: the table below has each problem, what the book says
and the verdict. Three exercises lose the call: **Exercises 2.1, 2.3
and 2.5**, which are about average velocities and speeds, and say
nothing about the acceleration. That's 7 calls in 4 modules. The other
13 problems keep theirs.

**Nothing changes in the results.** This was measured (2026-11-11) on
copies of the four modules without their calls: every `BOOK` answer
still matches, and the 6 record rows of those modules,
`tests/test_old_outputs.py`'s, have the same formulas and the same
numbers. These exercises only ever used the averages, 2.2. Their
equations after the kinematics get lower labels, but nothing refers to
those labels.

**Not in this increment:** any change to the code, the tests, a `BOOK`
or the record, and the labels from the book's numbers (the README's
decision 6). Only comments and docs change, and the 7 calls go.

## Read first

1. The series' README, `docs/design/implementation/005-constant-acceleration/README.md`.
2. Checkpoint 001, `checkpoints/001-explicit-constant-acceleration.md`,
   for what's in place now.
3. Each module in the table below, around its `kinematics()` lines.

## Starting point

- The worktree `~/journal/2026-11-06-equations/equarium-acceleration`,
  on the branch `2026-11-11-constant-acceleration`, at the commit that
  adds this checkpoint, on top of 001's `3788772`. Don't touch the
  review folder `equarium.py`.
- The tree is clean.
- **`uv run pytest`** passes 400 tests and deselects 3, in about 53 s.
- **`uv run pytest -m slow`** passes the 3 slow tests, in about 5 min.
- **`uv run pyright`:** 0 errors and 0 warnings.
- `git grep -c "constant_acceleration()" -- examples` finds 25 calls
  in 19 files.

## Build

### The audit

Each row is one problem; where it has two modules, both get the same
change. The quotes are from the modules' docstrings, which follow the
book.

| Problem | Modules, under `examples/up_15e/` | Edge | The problem says | Verdict |
|---|---|---|---|---|
| Example 2.4 | `ch02/examples/n04/main.py` | `m01` | "accelerates at a constant 4.0 m/s²" | keep |
| Example 2.5 | `ch02/examples/n05/main.py`, `main_step_by_step.py` | `m01` | the motorist "at a constant 15 m/s" | keep: zero acceleration is constant |
| | | `p01` | the officer starts "with a constant 3.0 m/s²" | keep |
| Example 2.6 | `ch02/examples/n06/main.py` | `c01` | the coin "falls freely" | keep: free fall |
| Example 2.7 | `ch02/examples/n07/main.py` | `b01` | the ball "falls freely" | keep: free fall |
| Exercise 2.1 | `ch02/exercises/n001/main.py` | `c01` | only "its average velocity is 6.25 m/s" | **drop** |
| Exercise 2.3 | `ch02/exercises/n003/main.py`, `main_two_steps.py` | `ca01`, `cb01` | only average speeds, "averages 105 km/h" and "70 km/h" | **drop** |
| Exercise 2.5 | `ch02/exercises/n005/main.py` | `p01`, `p12` | a walk, asking its "average velocity" and "average speed" | **drop** |
| Exercise 2.19 | `ch02/exercises/n019/main.py` | `o01` | "with constant acceleration" | keep |
| Exercise 2.21 | `ch02/exercises/n021/main.py` | `b01` | "accelerated uniformly" | keep |
| Exercise 2.23 | `ch02/exercises/n023/main.py` | `b01` | the deceleration "under 250 m/s²", and the minimum distance | keep: an assumption the problem implies, see below |
| Examples 3.6 to 3.9 | `ch03/examples/n06/` to `n09/main.py` | `m01`, `b01`, `p01`, `b01` | projectile motion, "no air resistance" | keep |
| Example 3.10 | `ch03/examples/n10/main.py` | `d01`, `m01` | the dart and the falling monkey, "no air resistance" | keep |
| Example 4.5 | `ch04/examples/n05/main.py`, `main_two_steps.py` | `b01` | "slowed by a constant horizontal friction force" | keep: a constant force gives a constant acceleration |

**Exercise 2.23** doesn't say "constant", but its answer needs it: the
shortest stop, with the deceleration never over 250 m/s², is the one
that decelerates at 250 m/s² all the way. The comment says so.

### The kept calls: a comment with the reason

Each kept `.add(*e.constant_acceleration())` gets a comment saying why,
in a few words, from the problem. Where the line has a label comment
from 001, such as `# (4)`, the reason follows it: `# (4): a constant
3.0 m/s²`. Suggested wording, to adapt so it reads well in its module:

| Problem | Comment |
|---|---|
| 2.4 | `a constant 4.0 m/s²` |
| 2.5, `m01` | `a constant 15 m/s, so a constant zero acceleration` |
| 2.5, `p01` | `a constant 3.0 m/s²` |
| 2.6, 2.7 | `free fall: a constant g` |
| 2.19 | `constant acceleration` |
| 2.21 | `accelerated uniformly` |
| 2.23 | `the shortest stop: the most deceleration, held constant` |
| 3.6 to 3.10 | `projectile motion: only gravity` |
| 4.5 | `a constant friction force` |

Keep each line within the module's width; if a comment won't fit, put
it on the line above. Don't reword the existing label comments.

### The dropped calls

In the 4 modules, delete the 7 `.add(*e.constant_acceleration())`
lines, and give each of their `kinematics()` lines a comment, for
example `# averages only: no constant acceleration`, so that a reader
sees the call is left out on purpose. Where a docstring describes the
equations, check it's still right.

### Docs

- **The series' README:**
  - its status: 002 built at this commit, not yet reviewed, and the
    series' work done once it's reviewed;
  - the checkpoints table;
  - a short "The audit" section after "Decisions": which three
    exercises lost the call and why, that no result changed, and the
    note on Exercise 2.23.
- **The series map,** `docs/design/implementation/README.md`: 005's
  row and paragraph.
- **This file's status line.**

## Check and commit

- **`uv run pytest`** passes 400 tests and deselects 3.
- **`uv run pytest -m slow`** passes the 3 slow tests. Run it in the
  background.
- **`uv run pyright`:** 0 errors and 0 warnings.
- **The calls.** `git grep -c "constant_acceleration()" -- examples`
  finds 18 calls in 15 files, and none in the 4 modules of the dropped
  rows. `git grep -c "kinematics()" -- examples` still finds 24 in 19.
- **Only comments and the 7 lines changed in the examples.** Read
  `git diff HEAD -- examples`: every changed line is the same code with
  a new or longer comment, or one of the 7 removed calls.
- **The record and the answers are untouched.**
  `git diff HEAD --stat -- tests src` prints nothing, and
  `git diff HEAD -- examples | grep '^[-+].*\(BOOK\|Answer(\|Formula(\)'`
  prints nothing.
- **No files outside the repo.**
- **One commit on `2026-11-11-constant-acceleration`,** staged by path,
  with a subject line and a wrapped paragraph saying what and why.
- **Don't merge or push.** Don't switch branches.

## Report

When done, say in a few lines:

- the commit, the number of tests, fast and slow, and how long the fast
  run takes;
- the two counts, 18 in 15 files and 24 in 19, and that `tests`, `src`,
  every `BOOK` and the record are untouched;
- any comment you worded differently from the table, and why;
- anything here that was wrong or unclear, and what you did instead;
- any problem whose book statement, read in its module, made you doubt
  the verdict here. Don't change a verdict on your own: report it.

Then stop. The series is done once the user reviews this. Merging into
`master` is the user's call.
