# constant acceleration 001: explicit constant acceleration

**Status:** Done at `3788772` (2026-11-11), checked against this page.

If you've been told to read this file, this is the whole assignment.
Build it, check it, commit it, report, and stop.

## Goal

`m.kinematics()` stops assuming constant acceleration, and a new
`m01.constant_acceleration()` states it, for one edge. Every example
that calls `kinematics()` gets a `constant_acceleration()` for each of
the particle's edges, right after the kinematics. So every system holds
the same equations as today, in the same order and with the same
labels, and **no answer, formula, label or record row changes.** The
order matters: `sp.solve` can return a different form of a formula for
equations in a different order, and `tests/test_old_outputs.py` checks
the old formulas verbatim.

In short:

- **`kinematics_equations`** drops 2.10, and calls the acceleration's
  equation the book's 2.4, the definition of the average acceleration.
- **`Edge.constant_acceleration()`** returns 2.10 for its edge, one
  equation per axis, exactly as `kinematics()` writes it today.
- **The 19 example modules** add the call after each `kinematics()`, 25
  calls for 24 `kinematics()` calls, since Exercise 2.5's particle has
  two edges.
- **The tests:** the ones that test `kinematics()` itself lose 2.10,
  the ones that build a system from it add the call, and two new tests
  test `constant_acceleration()` and what 2.4 can solve without it.
- **The docs** that describe the kinematics equations say the new thing.

Why, and the decisions, are in the series' README:
`docs/design/implementation/005-constant-acceleration/README.md`. The
user approved them (2026-11-11).

**Not in this increment:**

- **Deciding which problems have constant acceleration.** That's
  checkpoint 002's audit. Here every example keeps its 2.10, even one
  whose problem may not have constant acceleration.
- **The projectile setup.** `m01.projectile(g)` doesn't change, and
  doesn't include 2.10 (decision 4).
- **Labels from the book's numbers** (decision 6).
- **The written-out versions and the core's tests**, which write their
  equations out and label one "2.7": `main_handwritten.py`,
  `main_handwritten_step_by_step.py`, `tests/example_2_4.py`,
  `tests/kinematics_005.py`, `examples/up_15e/ch02/tables/n05/`, and the
  core's tests. Nor `README.md`'s usage, which is the written-out 2.4.
- **The record:** `tests/test_old_outputs.py` and `tests/old_names.py`
  don't change, not a character.
- **Merging, pushing**, and the branch `2026-11-11-worksheet-displays`.

## Read first

1. The series' README, `docs/design/implementation/005-constant-acceleration/README.md`.
2. `src/equarium/physics/kinematics.py`, all of it (40 lines).
3. `src/equarium/physics/particles.py`: `Edge` and `Particle.kinematics`.
4. `src/equarium/physics/__init__.py`'s docstring.
5. `tests/test_physics.py`: "The kinematics" section, and the tests
   named below.
6. Two examples, to see the pattern: `examples/up_15e/ch02/examples/n04/main.py`
   and `examples/up_15e/ch03/examples/n10/main.py`.

## Starting point

- The worktree `~/journal/2026-11-06-equations/equarium-acceleration`,
  on the branch `2026-11-11-constant-acceleration`, at the commit that
  adds this checkpoint, on top of `836cad3`. Work there. Don't touch the
  review folder `equarium.py`, which is on `master` and has the user's
  uncommitted files.
- The tree is clean.
- **`uv run pytest`** passes 398 tests and deselects 3, in about 53 s.
- **`uv run pytest -m slow`** passes the 3 slow tests, in about 5 min.
- **`uv run pyright`:** 0 errors and 0 warnings.
- `git grep -c "kinematics()" -- examples` finds 24 calls in 19 files.

## Build

### `src/equarium/physics/kinematics.py`

- **`kinematics_equations(particle)`** keeps its first three loops, the
  Δt, 2.2 and acceleration loops, in their order, and drops the fourth,
  2.10. Its docstring lists Δt, 2.2 and **2.4** (not 2.7): "the average
  acceleration over the edge, which holds for any motion".
- **A new `constant_acceleration_equations(edge)`** returns, for each
  axis in `edge.axes`' order, 2.10:
  `sp.Eq(v_av, (v0 + v1) / 2)`, with `v_av`, `v0` and `v1` from
  `edge.v_av.components`, `edge.start.vel.components` and
  `edge.end.vel.components`. That's the expression the fourth loop
  builds today, character for character, so its `str` is the same:
  `Eq(m01.v_av.x, m0.vel.x/2 + m1.vel.x/2)`. Its docstring: 2.10, which
  holds only when the acceleration over the edge is constant.
- **The module docstring** says what's where now: `kinematics_equations`
  writes the definitions, which hold for any motion, in the old physics
  code's order (Δt, 2.2, 2.4), and `constant_acceleration_equations`
  writes 2.10 for one edge, the constant-acceleration assumption. An
  example that adds each edge's 2.10 right after the kinematics has the
  old code's order, so the core's automatic labels stay as they were.

### `src/equarium/physics/particles.py`

- **`Edge.constant_acceleration(self) -> list[sp.Eq]`**, calling
  `constant_acceleration_equations(self)`. Docstring, in the style of
  `newton`: the book's 2.10, one equation per axis: with constant
  acceleration over the edge, its average velocity is the mean of its
  start's and end's velocities. One call for each edge that has
  constant acceleration.
- **`Edge`'s docstring:** its time, average velocity and average
  acceleration (it says "acceleration" today), and that
  `m01.constant_acceleration()` states that the acceleration is
  constant over the edge.
- **`Particle.kinematics`' docstring:** every edge's Δt, then the
  book's 2.2 and 2.4 for each edge and axis, which hold for any motion.
  Constant acceleration is a step of its own, for each edge:
  `m01.constant_acceleration()`.

### `src/equarium/physics/__init__.py`

Its docstring's first paragraph names "the kinematics equations". Add
a short paragraph after the one on events or before the projectile's:
`m.kinematics()` writes the definitions, which hold for any motion, and
`m01.constant_acceleration()` adds 2.10 for an edge whose acceleration
is constant. In the projectile paragraph, say that a projectile's edge
calls `constant_acceleration()` too. Keep the rest.

### The 19 example modules

In each, right after each `.add(*x.kinematics())`, add one
`.add(*e.constant_acceleration())` for each of the particle's edges, in
edge order, using the edge variables the module already has. Add
nothing between them. Then fix any comment that numbers the equations,
such as `# (1) to (4)`, so that it's still right. A one-axis edge gives
3 kinematics equations and 1 for 2.10. An `XY` edge gives 5 and 2.

| Module, under `examples/up_15e/` | After | Add |
|---|---|---|
| `ch02/examples/n04/main.py` | `m.kinematics()` | `m01` |
| `ch02/examples/n05/main.py` | `m.kinematics()`, `p.kinematics()` | `m01`, `p01` |
| `ch02/examples/n05/main_step_by_step.py` | `m.kinematics()`, `p.kinematics()` | `m01`, `p01` |
| `ch02/examples/n06/main.py` | `c.kinematics()` | `c01` |
| `ch02/examples/n07/main.py` | `b.kinematics()` | `b01` |
| `ch02/exercises/n001/main.py` | `c.kinematics()` | `c01` |
| `ch02/exercises/n003/main.py` | `ca.kinematics()`, `cb.kinematics()` | `ca01`, `cb01` |
| `ch02/exercises/n003/main_two_steps.py` | `ca.kinematics()`, `cb.kinematics()` | `ca01`, `cb01` |
| `ch02/exercises/n005/main.py` | `p.kinematics()` | `p01`, then `p12` |
| `ch02/exercises/n019/main.py` | `o.kinematics()` | `o01` |
| `ch02/exercises/n021/main.py` | `b.kinematics()` | `b01` |
| `ch02/exercises/n023/main.py` | `b.kinematics()` | `b01` |
| `ch03/examples/n06/main.py` | `m.kinematics()` | `m01` |
| `ch03/examples/n07/main.py` | `b.kinematics()` | `b01` |
| `ch03/examples/n08/main.py` | `p.kinematics()` | `p01` |
| `ch03/examples/n09/main.py` | `b.kinematics()` | `b01` |
| `ch03/examples/n10/main.py` | `d.kinematics()`, `m.kinematics()` | `d01`, `m01` |
| `ch04/examples/n05/main.py` | `b.kinematics()` | `b01` |
| `ch04/examples/n05/main_two_steps.py` | `b.kinematics()` | `b01` |

For example, 2.5's

```python
    .add(*m.kinematics())  # (1) to (4)
    .add(*p.kinematics())  # (5) to (8)
```

becomes

```python
    .add(*m.kinematics())  # (1) to (3)
    .add(*m01.constant_acceleration())  # (4)
    .add(*p.kinematics())  # (5) to (7)
    .add(*p01.constant_acceleration())  # (8)
```

and 3.10's dart, whose `from_polar()` comes between its kinematics and
its projectile setup, keeps that order:

```python
    .add(*d.kinematics())  # (1) to (5)
    .add(*d01.constant_acceleration())  # (6), (7)
    .add(*d0.vel.from_polar())  # (8), (9)
    .add(*flight.equations)  # (10), (11): projectile motion
```

A module whose `kinematics()` line has no comment gets none, or a short
one if the lines around it have them. Check each module's docstring
too: where it describes the kinematics equations or their labels, make
it right. Don't change anything else in the modules, not even a
`BOOK`.

The user's untracked scratch copies in the review folder,
`main_000_check.py`, `main_incremental.py`, `main_watch_000.py` and
`main_watch_001.py`, aren't in this worktree. Leave them.

### `tests/test_physics.py`

- **`test_kinematics_of_two_states`:** the first three strings; the
  2.10 string goes.
- **`test_kinematics_of_three_states_in_the_old_order`:** the first six
  strings.
- **A new `test_constant_acceleration_of_an_edge`:** for `m01` (`X`),
  `["Eq(m01.v_av.x, m0.vel.x/2 + m1.vel.x/2)"]`; for `p12` of
  `Particle("p", 3, X)`, its 2.10; and for an `XY` edge, x then y.
- **`test_kinematics_renamed_back_are_the_old_codes`:** the old code's
  strings are the record, and they stay, character for character. What
  they're compared with changes: the particle's kinematics followed by
  each edge's 2.10, in edge order. A small helper in the test, such as
  `with_constant_acceleration(particle)`, returning
  `particle.kinematics() + [eq for e in particle.edges for eq in
  e.constant_acceleration()]`, keeps the three assertions readable.
  Say in the comment above them why the strings didn't change.
- **A new `test_the_kinematics_alone_leave_2_4s_position_open`:** 2.4's
  part (a) from `m.kinematics()` alone, with 2.4's knowns and units.
  Its analysis has 4 unknowns in 3 equations, solving for `m1.vel.x`
  gives `23.0*meter/second`, and solving for `m1.pos.x` gives no roots,
  with the reason `sp.solve left m1.pos.x undetermined`. These are
  measured (2026-11-11). It's the series' point in one test: the
  average acceleration gives the velocity, and only constant
  acceleration gives the position.
- **`test_the_projectile_setup_goes_into_a_system`:** add
  `.add(*d01.constant_acceleration())` right after the kinematics, so
  its labels, `"8"` and `"9"`, and the `"4"` of its last line still
  hold.
- **`test_newton_with_the_kinematics_needs_no_link`:** add
  `.add(*b01.constant_acceleration())` right after the kinematics, so
  its labels stay. Its comment calls (3) "the book's 2.7": make it 2.4.
- **`test_pickling_round_trips`** uses `m.kinematics()[2]`, which is
  still there. Leave it.

### `tests/test_sketch.py`

`test_a_sketch_labels_knowns_wants_and_unknowns` builds 2.4's part (a)
from `m.kinematics()`: add `.add(*m01.constant_acceleration())` right
after it.

### Docs

- **The series' README:** its status, "Checkpoint 001 built at
  `<commit>`, not yet reviewed", and the checkpoints table.
- **The series map,** `docs/design/implementation/README.md`: 005's
  row and its paragraph say 001 is built.
- **This file's status line:** "Built at `<commit>`, not yet reviewed."

You can't know the commit before you make it: write "this commit" and
let the user's review fill it in, or amend once, before reporting.

### If a test fails that this page doesn't list

Stop and report it, with the test and the line that differs. Don't
change a `BOOK`, a record row or an expected formula to make it pass:
a change in any of them means the order of some system's equations
changed.

## Check and commit

- **`uv run pytest`** passes 400 tests (398 and the two new ones) and deselects 3.
- **`uv run pytest -m slow`** passes the 3 slow tests. Run it in the
  background.
- **`uv run pyright`:** 0 errors and 0 warnings.
- **The calls.** `git grep -c "kinematics()" -- examples` still finds
  24 calls in 19 files, and `git grep -c "constant_acceleration()" --
  examples` finds 25 in the same 19 files.
- **The record and the answers are untouched.**
  `git diff HEAD --stat -- tests/test_old_outputs.py tests/old_names.py`
  prints nothing, and no line with `BOOK`, `Answer(` or `Formula(`
  changed: `git diff HEAD -- examples | grep '^[-+].*\(BOOK\|Answer(\|Formula(\)'`
  prints nothing.
- **2.4 looks right in a transcript.**
  `uv run python -m equarium.transcript -m examples.up_15e.ch02.examples.n04.main`
  shows the same results as before: in the system under
  `motorcycle = (...)`, equation (4) is
  `m01.v_av.x = m0.vel.x/2 + m1.vel.x/2`, and under `sol_a`,
  `m1.pos.x = 43.0*meter`.
- **No files outside the repo.** Keep scratch output in your own
  scratch folder.
- **One commit on `2026-11-11-constant-acceleration`,** staged by path,
  in the style of `git log`: a subject line, then a wrapped paragraph
  saying what and why.
- **Don't merge or push.** Don't switch branches.

## Report

When done, say in a few lines:

- the commit, the number of tests, fast and slow, and how long the fast
  run takes;
- that the record and every `BOOK` are untouched, and the two counts,
  24 and 25;
- each module whose comments or docstring you changed beyond adding the
  call, in a line each;
- anything you named or worded differently from this page, and why;
- anything here that was wrong or unclear, and what you did instead.

Then stop. Checkpoint 002, the audit, is written after the user's
review.
