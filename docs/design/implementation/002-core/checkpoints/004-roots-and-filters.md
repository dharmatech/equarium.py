# core 004: roots and filters

**Status:** Done at `e4d4498` and reviewed (2026-11-08).

If you've been told to read this file, this is the whole assignment.
Build it, check it, commit it, report, and stop.

## Goal

**Filters on roots.** `Solution.where(relation)` keeps the roots for
which a SymPy relation holds, such as `t1 > 0`. The checks are 2.7's
four parts from one base, with a known replaced between them, 2.8's
two roots with t and v kept in pairs, and 3.9's two roots.

**Three small changes from the reviews of 001 to 003,** which the user
chose to add here:

1. A formula that still contains unknowns is a fourth reason for no
   roots.
2. An `eliminate_zeros` step records only the zeros that are new, or
   that still rewrote an equation.
3. The text helpers move to their own module.

Stop when the checks pass and the commit is in.

## Read first

- [The spec](../spec.md): the decisions "Solving" (above all "Filter")
  and "SymPy to watch", and §004, which this checkpoint carries out.
  The later increments are context, not work. Where this page is more
  exact than the spec, follow this page.
- Checkpoints [001](001-state-and-display.md) to
  [003](003-eliminate-and-isolate.md), for the layout and conventions,
  and the code itself: `src/equarium/`, `examples/` and `tests/`.
- The old scripts, read-only, in `~/src/combine-equations.py/examples/up/`:
  `ch2/up-example-2.7/up-example-2.7-v1-000.py` (2.7 and 2.8) and
  `ch3/up-example-3.9-v2.py`. Don't edit that repo.

## Starting point

`master` at the commit that adds this checkpoint, on top of `bb28627`
(increment 003). `uv run pytest` passes 105 tests in about 9 s, and
`uv run pyright` reports 0 errors and 0 warnings.

A scratch prototype on the real code produced every number and formula
on this page. Each 3.9 solve took about 1.4 s, and everything else
well under a second.

## Build

### `text.py`, new

`listing`, `labels` and `plural` move here from `display.py`, unchanged.
`display.py`, `rewrite.py` and `solve.py` import them from `text.py`,
so neither `rewrite.py` nor `solve.py` imports `display.py` for them
any more. `solve.py` still imports it for `Solution.show()`. `text.py`
imports nothing from the package, so it sits at the bottom of the
layers.

### `solve.py`

- **`Solution.where(relation) -> Solution`.**
  - **The relation** is a SymPy boolean over the wants and the knowns:
    a relation such as `t1 > 0`, or relations joined with `&`, `|` and
    `~`. Anything else, a Python `bool` included, raises `UsageError`.
  - **Each root** is tested by substituting its numbers for the wants,
    then the values of the knowns that have one.
    - The root is kept if the result is SymPy's `true`, and dropped if
      it's `false`.
    - Anything else raises `UsageError`, naming the relation and what
      it became, as in `t1 > D became 3.36451028118484 > D`. That
      happens with a known that has no number, or an unknown that isn't
      a want.
    - SymPy raises `TypeError` for a comparison with a number that
      isn't real (`-2.0*I > 0`). That is also a `UsageError`: the
      relation doesn't reduce.
  - **The result** is a new `Solution` with the same system and
    `elapsed`, and the roots kept, in their order.
    - If none are kept, there are no roots, with the reason
      `no root satisfies t1 > 10`, the relation as SymPy prints it.
    - `where` on a solution with no roots returns it as it is.
- **A fourth reason for no roots.** After the check for a want left
  undetermined, `all_at_once` checks each root's formula for each want,
  in that order. If a formula has a free symbol that isn't a known, the
  solution has no roots. The reason is
  `sp.solve left x in terms of the unknowns y, z`, naming the first
  such want and its unknowns sorted by name.
  - **Why.** The spec defines a formula as being in terms of the
    knowns. Before this, `System().add(Eq(x, y + z)).want(x).solve()`
    gave one root, `x = y + z`, whose number still had y and z in it.
  - **A known with no number still counts as a known,** so `x = 2*D`
    with `known(D)` stays a root.

### `rewrite.py`

`eliminate_zeros` still substitutes every known that is zero, and
still fixes them all. But its step's `zeros` now lists only the zeros,
in the knowns' order, that weren't fixed before this step, or that
rewrote or dropped an equation in it. The second case is a zero that
an equation added since the last call still contained. With none
listed, the step renders `eliminate zeros: none`, as it does with no
zeros at all.

The step-by-step example's history is where this shows. Lines 12 and
14 become `eliminate zeros m_0_t, p_0_t: into (1), (4), (5)` and
`eliminate zeros m_0_x: into (1)`. Before, they repeated `p_0_v` and
`p_0_x`.

### Not in this increment

Units, `in_units` and `Answer`'s `unit` come in 005, and `eliminating`
in 006. Branching over replaced knowns and roots with several wants
need no new code: `known` already replaces a value, and `all_at_once`
already keeps each root's wants together. This increment only checks
them.

### Tests

**`tests/test_roots.py`,** new. Use `Answer` for the book's numbers.

**2.7, written out like 2.4.** The base, `ball`:

- **Symbols:** `y0 y1 v0 v1 t0 t1 v_av a`.
- **Equations:** `(2.2) v_av = (y1 - y0)/(t1 - t0)`,
  `(2.7) a = (v1 - v0)/(t1 - t0)` and `(2.10) v_av = (v0 + v1)/2`.
- **Knowns:** `known(t0, 0)`, `known(y0, 0)` and `eliminate_zeros()`,
  as the old script's zero equations, then `known(v0, 15.0)` and
  `known(a, -9.8)`.

The book prints the numbers quoted below.

- **(a)** `part_a = ball.known(t1, 1.0).want(y1, v1)` gives
  `y1 = a*t1**2/2 + t1*v0` and `v1 = a*t1 + v0`, with "10.1" and "5.2".
- **(b)** `part_a.known(t1, 4.0)` replaces t1 and gives "-18.4" and
  "-24.2". `part_a.knowns[t1]` is still `1.0`.
- **(c)** `ball.known(y1, 5.0).solve(v1)` gives two roots, which match
  "-11.3", "11.3". Their formulas are `-sqrt(2*a*y1 + v0**2)` and
  `sqrt(2*a*y1 + v0**2)`, as a set.
- **(d)** `ball.known(v1, 0.0).solve(y1)` gives
  `y1 = (-v0**2 + v1**2)/(2*a)`, the old script's formula, and "11.5".
  - v1 stays a symbol, because it became zero after `eliminate_zeros()`.
  - The book's last part asks for the acceleration at the top, which is
    the known a: `ball.knowns[a]` is `-9.8`.

**2.8,** on the same base.

- **Two roots.** `ball.known(y1, -5.0).solve(t1)` gives two roots,
  which match "3.36", "-0.30". `.number(t1)` raises a `UsageError`
  that contains `2 roots`.
- **The filter.** `.where(t1 > 0)` keeps one root. That root matches
  "3.36", and `.number(t1)` works.
- **Pairs.** `solve(t1, v1)` keeps each root's pair. Rounded to two
  places, the pairs are `{(3.36, -17.97), (-0.3, 17.97)}`.
  - `.where((t1 > 0) & (v1 < 0))` keeps the first pair.
  - `.where((t1 > 10) | (v1 > 0))` keeps the second.
- **Nothing kept.** `.where(t1 > 10)` gives no roots, with the reason
  `no root satisfies t1 > 10`.

**3.9, written out with one-way polar.** Use 003's 3.10 scheme of
symbols for one object `b`: `b0x b1x b0y b1y b0vx b1vx b0vy b1vy b0t
b1t`, plus `b_dt b_vav_x b_vav_y b_a_x b_a_y`, and `g v_mag angle`.

- **The equations,** in this order:
  1. The seven, in the old physics code's order, as for 3.10's dart.
  2. `eq_flat(b_a_y, -g, b0vx, b1vx)`.
  3. `eq_flat(b0vx, v_mag*sp.cos(angle), b0vy, v_mag*sp.sin(angle))`.

  These are polar to components only. The old v2 script's two-way
  equations belong to 006.
- **The zeros:** `b0x`, `b_a_x`, `b0t` and `b1y` (it hits the ground).
  Then `eliminate_zeros()`.
- **The knowns:** g 9.81, `b0y` 8.0, `v_mag` 10.0 and `angle`
  `sp.rad(-20)`.
- **The checks:**
  - `solve(b1x)` gives two roots, which match "-15.7", "9.2". The book
    prints 9.2 m, and the old script 9.16.
  - `.where(b1x > 0)` keeps the one that matches "9.2".
  - `solve(b1x, b1t).where(b1t > 0)` keeps one root, which matches
    "9.2" for `b1x` and "0.98" for `b1t`, the book's time.

**`where` refusals:**

- **No number.** `ball.known(D).known(y1, -5.0).solve(t1).where(t1 > D)`,
  with D known and no number, raises `UsageError`.
- **An unknown that isn't a want:** `.where(v_av > 0)` on 2.8's
  solution raises `UsageError`.
- **Complex roots.** `x**2 = -4` solved for x, then `.where(x > 0)`,
  raises `UsageError`.
- **Not a relation.** `.where(True)` raises `UsageError`.

**The three changes:**

- **Unknowns in a formula.** `System().add(sp.Eq(x, y + z)).want(x).solve()`
  has no roots, with the reason
  `sp.solve left x in terms of the unknowns y, z`.
- **New zeros only:**
  - On 2.4's base, `known(x0, 0).eliminate_zeros()` has the step zeros
    `(x0,)`, not `(t0, x0)`.
  - Calling `eliminate_zeros()` again on the base gives
    `EliminateZerosStep((), (), ())`.
  - After `base.add(sp.Eq(x1, x0 + t0))`, another `eliminate_zeros()`
    lists `t0`, which rewrote the new equation.
  - The step-by-step example's history lines 12 and 14 are the two
    quoted above.
- **`text.py`** needs no test of its own. The existing tests cover the
  helpers through the display.

If a check here or in the spec turns out wrong, work out by hand which
side is. If it's the check, use the right answer, keep going, and say
so in your report. Don't edit `spec.md` or this page.

## Docs

- **The series [README](../README.md):** mark 004 done in its
  increments table, and update its status line. Leave the commit cell
  and this page's status line for the manager.
- **The [series map](../../README.md):** 002's status says 004 of 7 is
  done.
- **The package `README.md`:** a few lines after the usage example,
  showing `where` picking the physical root on the same system.
  `motorcycle.known(x1, 55).solve(t1)` has two roots, -10.0 and 2.5,
  and `.where(t1 > 0)` keeps 2.5 s, the time the book's check of part
  (b) finds.

## Check and commit

- `uv run pytest` passes: the 105 tests from 001 to 003, plus yours.
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
- the slowest test and its time;
- where you needed a `cast` for SymPy's types;
- anything in the spec or this checkpoint that was wrong or unclear,
  and what you did instead.

Then stop; increment 005 is a separate checkpoint.
