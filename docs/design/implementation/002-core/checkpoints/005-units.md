# core 005: units

**Status:** Done at `8f1a98d` and reviewed (2026-11-08).

If you've been told to read this file, this is the whole assignment.
Build it, check it, commit it, report, and stop.

## Goal

Numbers with units. Knowns already take values like `105*km/h`, since
001. This increment adds two things:

- **`Solution.in_units(...)`** converts every number to the given
  units.
- **`Answer(…, unit=...)`** checks a number given in a unit against
  the book.

The checks are Exercises 2.23 and 2.3, written out in tests: 2.3 both
in two steps and in one. Stop when the checks pass and the commit is
in.

## Read first

- [The spec](../spec.md): "What the prototype showed" (the units
  bullet), the decisions "The state" (knowns), "Solving" (above all
  "Units") and "Examples in the repo" (`Answer`), "SymPy to watch",
  and §005, which this checkpoint carries out. The later increments
  are context, not work. Where this page is more exact than the spec,
  follow this page.
- Checkpoints [001](001-state-and-display.md) to
  [004](004-roots-and-filters.md), for the layout and conventions, and
  the code itself: `src/equarium/`, `examples/` and `tests/`.
- The old scripts, read-only, in `~/src/combine-equations.py/examples/up/ch2/exercises/`:
  `2.23/up-exercise-2.23-000.py`, `2.3/up-exercise-2.3-000-two-steps.py`
  and `2.3/up-exercise-2.3-002-one-step.py`. Don't edit that repo.

## Starting point

`master` at the commit that adds this checkpoint, on top of `e4d4498`
(increment 004). `uv run pytest` passes 130 tests in about 14 s, and
`uv run pyright` reports 0 errors and 0 warnings.

A scratch prototype on the real code produced every number, formula and
SymPy behavior on this page. Each solve here takes well under a second.

## Build

### `solve.py`

**`Solution.in_units(*units) -> Solution`.**

- **The new solution.** It has the same system, `elapsed` and reason,
  and the same formulas. Each root's numbers become
  `convert_to(number, list(units))`, from `sympy.physics.units`.
- **What passes through unchanged.** A number with no units, and a
  known with no number left as a symbol, both come out of `convert_to`
  as they went in.
- **No roots.** A solution with no roots is returned as it is.
- **Refusals.** Called with no units, or with a unit that isn't a
  SymPy expression with no free symbols built from `Quantity` objects
  (such as `3`), it raises `UsageError`. Composite units such as
  `km/h` are allowed.

### `examples/answers.py`

**`Answer(solution, symbol, *printed, unit=None)`,** with `unit`
keyword-only.

- **With a unit,** each root's number is divided by it, and the
  result must have no `Quantity` left.
  - Don't simplify the quotient. `sp.simplify` cancels
    `kilometer/meter`, so a number left in kilometers would pass as
    meters.
  - Without simplifying, `1.70138888888889*meter/meter` is
    `1.70138888888889`, but `0.00170138888888889*kilometer/meter` and
    `1.70…*meter/second` keep their units.
  - A unit left over is a mismatch, `…, which isn't in meter`. So
    `unit=` asks the example to call `in_units` first. Then the
    quotient is compared as before.
- **Without a unit,** a number that has a `Quantity` is a mismatch,
  `…, which has units: give unit=`.
  - Today this case raises `TypeError` from `float()`. SymPy says
    `(1.7*meter).is_real` is True, so the "not real" check doesn't
    catch it.
- **Refusals.** A `unit` that isn't a units expression raises
  `UsageError` when the `Answer` is built, as the other argument
  checks do.

### What needs no new code

- **Knowns with units.** `known(v0, 105*km/h)` already works.
- **Zeros with units.** `0*m` and `0*m/s` are already `0`, so
  `eliminate_zeros` would treat them as zeros.
- **Filters with units.** `where` already works with units: SymPy
  evaluates `3.36*second > 0`, `2.75*hour > 2*hour`, and even
  `22.05*kilometer**2*second**2/(hour**2*meter) > 0` to `true`.
- **The display** prints a number with units as SymPy prints it.

### Not in this increment

`eliminating`, the time on the display and the `slow` marker come in
006. The package README doesn't change.

### Tests

**`tests/test_units.py`,** new. The systems use 003's 3.10 scheme of
symbols, in one dimension. The four equations, in the old physics
code's order, for an object `o`:

```
o_dt = o1t - o0t
o_vav_x = (o1x - o0x)/o_dt
o_a_x = (o1vx - o0vx)/o_dt
o_vav_x = (o0vx + o1vx)/2
```

The units come from `sympy.physics.units`: `meter`, `second`,
`kilometer`, `hour` and `minute`.

**2.23, the airbag.** Object `b`.

- **The knowns:** `b_a_x` is `-250*meter/second**2`, and `b0vx` is
  `105*kilometer/hour`. `b1vx` is `0*meter/second`, `b0t` is
  `0*second` and `b0x` is `0*meter`. Those three zeros are left as
  values, not eliminated, as in the old script.
- **The render.** It lists
  `knowns: b_a_x = -250*meter/second**2, b0vx = 105*kilometer/hour, b1vx = 0, b0t = 0, b0x = 0`.
- **The solve.** `want(b1x).solve()` gives one root.
  - **The formula** is the old one, zeros kept as symbols:
    `(-b0vx**2 + 2*b0x*b_a_x + b1vx**2)/(2*b_a_x)`.
  - **The raw number** prints as
    `22.05*kilometer**2*second**2/(hour**2*meter)`, as the old script
    printed it.
- **The conversion.** `.in_units(meter, second)` gives
  `1.70138888888889*meter`, and keeps the formula.
- **Matching the book** (Exercise 2.23's answer is 1.70 m):
  - `Answer(sol.in_units(meter, second), b1x, "1.70", unit=meter)`
    matches;
  - the same with `sol.in_units(kilometer, second)` doesn't match: a
    number in kilometers;
  - the same with `unit=second` doesn't: the wrong dimension;
  - the unconverted `sol` with `unit=meter` doesn't;
  - and the converted one with no `unit` doesn't, with "has units" in
    the message.
- **A filter with units.** `sol.in_units(meter, second).where(b1x > 0)`
  keeps the root.

**2.3, two steps,** as in the old `-000-two-steps`. Objects `ca` (the
usual trip) and `cb` (the slow one), each with its four equations.

- **The first system:**
  - **Its knowns:** `ca0t` is `0*hour`, `ca1t` is
    `hour + sp.Rational(50, 60)*hour`, `ca0x` is `0*kilometer` and
    `ca_vav_x` is `105*kilometer/hour`.
  - **The solve.** `want(ca1x)` gives the old formula
    `-ca0t*ca_vav_x + ca0x + ca1t*ca_vav_x` and `192.5*kilometer`.
- **The second system:**
  - **Its knowns:** `cb0t` is `0*hour`, `cb0x` is `0*kilometer`,
    `cb_vav_x` is `70*kilometer/hour`, and `cb1x` is the first
    solution's `number(ca1x)`.
  - **The solve.** `want(cb1t)` gives `(cb0t*cb_vav_x - cb0x + cb1x)/cb_vav_x`.
    `.in_units(hour, kilometer)` gives `2.75*hour`, which matches
    `Answer(…, cb1t, "2.75", unit=hour)`.

**2.3, one step,** as in the old `-002-one-step`.

- **The system.** Both trips' eight equations, then
  `eq_flat(ca1x, cb1x, longer, cb1t - ca1t)`, with both trips' knowns
  except `cb1x`. `longer` is new: the old script stopped at the slow
  trip's time, but the book asks how much longer it takes.
- **The slow trip's time.** `solve(cb1t)` gives the old formula
  `(-ca0t*ca_vav_x + ca0x + ca1t*ca_vav_x + cb0t*cb_vav_x - cb0x)/cb_vav_x`,
  and `2.75*hour` in `(hour, kilometer)`.
- **The book's answer** (Exercise 2.3's is 55 min). `solve(longer)`
  gives `0.916666666666667*hour`. `.in_units(minute)` gives
  `55.0*minute`, which matches `Answer(…, longer, "55", unit=minute)`.

**Refusals:**

- `sol.in_units()` and `sol.in_units(3)` raise `UsageError`.
- `Answer(…, unit=3)` raises `UsageError`.
- `in_units` on a solution with no roots returns it unchanged.

If a check here or in the spec turns out wrong, work out by hand which
side is. If it's the check, use the right answer, keep going, and say
so in your report. Don't edit `spec.md` or this page.

## Docs

- **The series [README](../README.md):** mark 005 done in its
  increments table, and update its status line. Leave the commit cell
  and this page's status line for the manager.
- **The [series map](../../README.md):** 002's status says 005 of 7 is
  done.

## Check and commit

- `uv run pytest` passes: the 130 tests from 001 to 004, plus yours.
  If a test takes more than 5 s, say so in the report rather than
  adding the `slow` marker, which comes in 006.
- `uv run pyright`: 0 errors, 0 warnings.
- The three examples still run with `uv run python -m …`.
- One commit on `master`, with the code, tests and docs, in the style
  of `git log`: a subject line, then a wrapped paragraph saying what
  and why. Don't push.

## Report

When done, say in a few lines:

- the commit and the number of tests;
- where you needed a `cast` for SymPy's types (`convert_to` is likely
  untyped);
- anything in the spec or this checkpoint that was wrong or unclear,
  and what you did instead.

Then stop; increment 006 is a separate checkpoint.
