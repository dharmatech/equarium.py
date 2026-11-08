# core 007: the old physics code, and chapter 2

**Status:** Done at `ec3cef8` and reviewed (2026-11-08).

If you've been told to read this file, this is the whole assignment.
Build it, check it, commit it, report, and stop.

## Goal

The old physics code on the new core, with no design changes, and
chapter 2's examples ported onto it. That means:

- **A copy of the physics code.** `kinematics_states.py` and
  `newtons_laws.py` go to `src/equarium/physics/`, with typing-only
  fixes.
- **Two helpers.** `add_both_sides` and `multiply_both_sides` go into
  `equations.py`.
- **Fourteen new modules** under `examples/up_15e/ch02/`, from the
  catalog's port list: 13 examples and exercises, each with its `BOOK`,
  and `table_2_5.py`.
- **A test** that compares the ports' formulas with the old scripts'
  output.

Chapters 3 and 4 are increment 008, a separate checkpoint. Stop when
the checks pass and the commit is in.

## Read first

- [The spec](../spec.md): "Examples in the repo", §007, and the two
  notes dated 2026-11-08 under it and under the increments table. They
  record the split and the typing-only fixes.
- **The catalog,**
  [001-example-catalog/catalog.md](../../001-example-catalog/catalog.md),
  above all "Recommendations for 007":
  - its sections:
    - the chapter 2 table of "The port list";
    - "Where the port differs from the old script";
    - "The slugs";
    - "misc.py's both-sides helpers";
    - "The physics code";
    - the user's seven answers;
  - each chapter 2 problem's own entry, Example 2.4 to Exercise 2.23,
    and "kinematic-equations". These quote, verbatim, what each old
    script prints, and say which zeros were equations and which were
    values.
- Checkpoints [001](001-state-and-display.md) to
  [006](006-elimination-attempts.md), for the conventions, and the code
  itself: `src/equarium/`, `examples/` (the three existing chapter 2
  modules are the model of a module) and `tests/`.
- **The old library, read-only,** in `~/src/combine-equations.py/`:
  - `src/combine_equations/kinematics_states.py`, `newtons_laws.py`
    and `misc.py`;
  - the scripts the port list names, under `examples/up/ch2/`.

  Don't edit that repo.

## Starting point

`master` at the commit that adds this checkpoint, on top of `0ec6633`
(the catalog's answers). `uv run pytest` passes 160 tests and skips 3
slow ones, and `uv run pytest -m slow` passes those 3. `uv run pyright`
reports 0 errors and 0 warnings.

A scratch prototype made every port on this page, on the real code
(2026-11-08). The results:

- **The formulas.** The 13 example and exercise ports reproduce, verbatim,
  every formula the catalog quotes for their old scripts: 33 of 33
  lines.
- **The `BOOK`s.** Every answer in every `BOOK` matches.
- **pyright** reports 0 errors over the typed copy and the ports.
- **Speed.** Each module imports in under 0.6 s, except Exercise 2.3
  (1.6 s) and Exercise 2.5 (1.3 s). All 14 together take about 6 s.

The prototype's files may still be in
`/tmp/claude-1000/-home-dharmatech-journal-2026-11-06-equations/afc8433e-c119-4001-b238-c8d31019e305/scratchpad/proto007/`.
They're a reference, not the source: the old scripts and the catalog
are.

## Build

### `src/equarium/physics/`, new

- **What's in it.** `__init__.py` (a docstring only), plus copies of
  `kinematics_states.py` and `newtons_laws.py`.
- **The imports.** `eq_flat` now comes from equarium.
  `newtons_laws.py` imports `Point3` from `equarium.physics.kinematics_states`,
  and gains `import sympy as sp`. Without that import it only works
  because annotations are lazy.
- **The typing-only fixes,** all the prototype needed for 0 errors in
  standard mode:
  - **16 times `cast(sp.Eq, sp.Eq(...))`.** That's the 13 places that
    append an `sp.Eq(...)` to a `list[sp.Eq]`, and 3 in `link_same_time`'s
    returns. SymPy types `sp.Eq(...)` as a union that includes
    `Integer`.
  - **2 annotations, `kill: tuple[Axis, ...]`,** in
    `axis_zero_constraints` and `axis_zero_substitution_map`. A
    `tuple[str, ...]` goes to `Point3.get(axis: Axis)`.
  - **2 times `cast(sp.Symbol, …)`,** for `obj.vel.mag` and
    `obj.vel.angle` in `magnitude_and_angle_equations`.
  - **`cast`** added to the `typing` import.

  Nothing else changes: no name, no equation, no behavior. A
  `diff -u` against the old files shows only these lines and the
  imports. If pyright asks for more, make the same kind of fix and list
  it in the report.
- **What doesn't happen.** `equarium/__init__.py` doesn't import or
  re-export the physics code, and the core imports nothing from it.

### `equations.py`

- **`add_both_sides(eq, addend)` and `multiply_both_sides(eq, factor)`**
  come from `misc.py`, as plain functions `sp.Equality -> sp.Equality`.
  Read the sides through `sympy_compat.sides`.
- **When the result isn't an equation.** SymPy can evaluate the result
  to `true` or `false`, as when multiplying by 0. That raises
  `UsageError`, where `misc.py` returned the boolean.
- **What stays behind.** `misc.py`'s `divide_both_sides`, `expand_lhs`
  and `expand_rhs` don't come over; nothing in the port list uses them.

### The ports, `examples/up_15e/ch02/`

Fourteen new modules, named and sourced as the catalog's chapter 2
table says, each with the catalog's `BOOK`, character for character.
They follow the conventions of the three that exist:

- values at import, and printing only under `__main__`;
- a module docstring naming the book, the problem, and the old script
  it was ported from;
- the run command.

**How a port is written:**

- **Symbols.** They come through the physics code's objects
  (`make_states_model`, `.states`, `.edges`, `m1.pos.x`), and the
  equations from `kinematics_fundamental`, as in the old script. The
  old calls become `System` methods.
- **Zeros.** The spec's rules apply. A zero the old script wrote as an
  equation becomes `known(sym, 0)` plus `eliminate_zeros()`, where the
  old script eliminated it. A zero in `values` becomes `known(sym, 0)`
  alone. Each catalog entry says which is which.
- **Narrowing.** Where a port uses a field the model types as optional,
  it narrows it with `assert …`. In chapter 2 that's only an edge's
  `v_av`: in Exercises 2.1, 2.3 (both modules) and 2.21. In all, 4
  asserts cover 6 uses.

| Module | From | Notes from the prototype |
|---|---|---|
| `example_2_4.py` | 2.4 v4-001 | Zero equation `m0.t`, eliminated in the base before parts (a) and (b) branch. |
| `example_2_5.py` | 2.5 v4-000 | The links as written. The five zero equations, eliminated before the one solve of `t_01`, `p1.vel.x` and `dist`. |
| `example_2_5_step_by_step.py` | 2.5 v4-002 | Stages, each displayed: `start`; `links` (the links, the zeros as knowns, the values); `zeros` (`eliminate_zeros()`); `linked` (`eliminate(m0.vel.x, m1.vel.x, m1.pos.x, p1.pos.x, m1.t, p1.t)`). Then the solve. |
| `example_2_6.py` | 2.6 v2-000 | Zero equations `c0.t`, `c0.vel.y` and `c0.pos.y`, eliminated in the base. The velocity at 2.0 s and 3.0 s is the catalog's added want. |
| `example_2_7.py` | 2.7 v1-000 | Zero equations `b0.t` and `b0.pos.y`, eliminated in the base, which is named `ball`. Part (c)'s `b1.vel.y = 0.0` is a known on its branch, after that step, so its formula keeps `b_1_v_y`. Part (d) is a comment. |
| `example_2_8.py` | 2.7 v1-000's last part | Imports `ball` and `b1` from `example_2_7`, adds `b1.pos.y = -5.0`, and solves for `b1.t`. Then `where(b1.t > 0)`. |
| `exercise_2_1.py` | 2.1 000 | Zero values `c0.pos.x`, `c0.t`, with units. |
| `exercise_2_3.py` | 2.3 002 | Zero values. The added `Eq(longer, cb1.t - ca1.t)`. Keep the old script's `1*hour + 50/60*hour`, a Float, as the port of that script. |
| `exercise_2_3_two_steps.py` | 2.3 000 | Step 1 solves the usual trip's distance. Step 2 takes `distance.number(ca1.pos.x)` as a known, and adds `ca1.t` and `longer`. |
| `exercise_2_5.py` | 2.5 001 | A three-state model. The old `eq_flat` of the displacements and the averages, `Abs` included. |
| `exercise_2_19.py` | 2.19 000 | Zero value `o0.pos.x`. Two solves. |
| `exercise_2_21.py` | 2.21 000 | Without the GUI calls. Keep the old script's display-only elimination as a stage, `no_average = pitch.eliminate(b01.v_av.x)`, shown under `__main__`. |
| `exercise_2_23.py` | 2.23 000 | Zero values, with units. `in_units(meter, second)` in the `BOOK`. |
| `table_2_5.py` | kinematic-equations 003 | See below. |

**`table_2_5.py`.** One `System`, `kinematics`, holds 003's three
equations, labeled (2.2), (2.7) and (2.10), in 003's symbols. Its
five equations each come from a branch of it.

1. **`v_av_x` without `dt`:** `eliminate(dt, using="2.7")`, then
   equation (2.2).
2. **2.14:**
   - `eliminate(v_av_x, using="2.10")`, then (2.2).
   - `multiply_both_sides` by `dt`.
   - simplify;
   - `multiply_both_sides` by −1.
3. **2.8:** `isolate(v_2x, "2.7")`.
4. **2.13:**
   - Start from line 1's system, and `eliminate(v_av_x, using="2.10")`.
   - `multiply_both_sides` by `(-v_1x + v_2x)`, then by 2.
   - simplify;
   - `add_both_sides` with `v_1x**2`.
5. **2.12:** from line 2's system, `eliminate(v_2x, using="2.7")` and
   `isolate(x_2, "2.2")`.

The module exposes `EQUATIONS: list[tuple[str, sp.Equality]]`, in
003's order. Under `__main__` it prints each equation as `lhs = rhs`.

- **Simplifying.** pyright types `sp.simplify` of an `Equality` as
  `Boolean`. So the "simplify" steps go through a small helper in the
  module that narrows with `isinstance`.
- **No `BOOK`.** The module isn't named `example_…` or `exercise_…`,
  so `tests/test_examples.py` doesn't collect it.

The prototype's five equations:

```
v_av_x = a_x*(x_1 - x_2)/(v_1x - v_2x)
-x_1 + x_2 = dt*(v_1x + v_2x)/2
v_2x = a_x*dt + v_1x
2*a_x*(-x_1 + x_2) + v_1x**2 = v_2x**2
x_2 = a_x*dt**2/2 + dt*v_1x + x_1
```

### Differences from the old scripts

The catalog's "Where the port differs from the old script" lists the
expected differences. The prototype found three more, which this
checkpoint adds:

1. **Exact numbers now print as floats.** The old 2.4 and 2.5 scripts
   printed `formula.subs(values)` with integer knowns: `43`, `23`, `55`,
   `10`, `30`, `150`. equarium's number is `sp.N` of the formula, so
   it's `43.0000000000000`. Nine of the 33 quoted lines differ this way.
   Compare numbers by value.
2. **`table_2_5`'s first equation keeps equarium's form.** That's
   `v_av_x = a_x*(x_1 - x_2)/(v_1x - v_2x)`, where 003 printed
   `v_av_x = a_x*(-x_1 + x_2)/(-v_1x + v_2x)`.
   - The two are equivalent. equarium's `eliminate` simplifies each
     side, and `tests/test_rewrite.py` already pins this form.
   - Compare line 1 by equivalence, and lines 2 to 5 verbatim.
3. **The displayed systems of 2.5 step by step keep their shapes.**
   For example, `v_av_x_m_0_1 = m_v` stays, where v4-002 printed
   `m_v = v_av_x_m_0_1`, and `t_01 = dt_m_0_1` where it printed
   `dt_m_0_1 = t_01`. The formulas and answers are the same. Nothing
   compares these displays with the old ones.

Any other difference between a port's formula or number and the old
output stops the work. Report it rather than adjusting anything, as the
spec says.

### Tests

- **`tests/test_examples.py`** already collects every `example_…` and
  `exercise_…` module, and checks its `BOOK`. Extend
  `test_the_examples_are_found` with the 13 new names.
- **`tests/test_old_outputs.py`,** new. One table of rows: module,
  solution, symbol, the old formula as the catalog quotes it, and the
  old number. Parametrize over it.
  - **What the rows cover:** every formula the catalog quotes for a
    ported script's want, 33 rows in the prototype's count.
  - **Formulas** compare by `str()`, verbatim.
  - **Numbers** compare by value: `float(number)` against the old
    number, to within 1e-9 relative. A number with units is divided by
    its unit first.
  - **The listed additions** (2.6's velocities, 2.3's `longer`) have no
    old row. Their `BOOK` checks them.
- **`tests/test_table_2_5.py`,** new. `EQUATIONS` has the five names
  in 003's order. Line 1 is equivalent to 003's (its difference
  simplifies to 0) and is equarium's form above. Lines 2 to 5 equal
  003's output, verbatim and as SymPy objects.
- **`tests/test_equations.py`,** new, or added to an existing file:
  - `add_both_sides(Eq(x, y), 2)` is `Eq(x + 2, y + 2)`;
  - `multiply_both_sides(Eq(x, y), 3)` is `Eq(3*x, 3*y)`;
  - `multiply_both_sides(Eq(x, y), 0)` raises `UsageError`.
- **`tests/test_physics.py`,** new and small:
  - `kinematics_fundamental(make_states_model("m", 2), axes=("x",))`
    gives the same four equations as the old library's, as `str()`
    lists. Run the old one once, in the old repo's venv, to get them.
    The catalog doesn't quote them;
  - and `equarium` doesn't import `equarium.physics`.

If a check here or in the catalog turns out wrong, work out which side
is. If it's the check, use the right answer, keep going, and say so in
your report. Don't edit `spec.md`, the catalog's recommendations, or
this page.

## Docs

- **The series [README](../README.md):** mark 007 done in its
  increments table, and update its status line. Leave the commit cell
  and this page's status line for the manager.
- **The [series map](../../README.md):** 002's status says 007 of 8 is
  done.
- **The catalog's Index:** in its "In equarium" column, each chapter 2
  problem names its new module or modules. The catalog says it's
  updated as examples are ported. Touch nothing else in the catalog.
- **The package `README.md`:** one sentence in Usage saying that
  `examples/up_15e/` holds the ported examples, with one physics-code
  example's run command (`example_2_4`).

## Check and commit

- **`uv run pytest`** passes: the 160 fast tests, plus yours. Report
  how long `tests/test_examples.py` takes now.
- **`uv run pytest -m slow`** still passes its 3 tests.
- **`uv run pyright`:** 0 errors and 0 warnings, over `src`, `tests` and
  `examples`.
- **Every new module** runs with `uv run python -m examples.up_15e.ch02.<name>`.
- **One commit on `master`,** with the code, tests and docs, in the
  style of `git log`: a subject line, then a wrapped paragraph saying
  what and why. Don't push.

## Report

When done, say in a few lines:

- the commit, and the number of tests, fast and slow;
- the typing fixes in the physics copy, by kind and count, if they
  differ from the list above;
- the number of narrowing asserts in the ports;
- any formula or number that differed from the old output beyond the
  listed differences;
- anything in the spec, the catalog or this checkpoint that was wrong
  or unclear, and what you did instead.

Then stop. Increment 008, chapters 3 and 4, is a separate checkpoint.
