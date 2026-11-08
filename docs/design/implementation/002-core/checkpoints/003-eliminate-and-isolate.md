# core 003: eliminate and isolate

**Status:** Done at `bb28627` and reviewed (2026-11-08).

If you've been told to read this file, this is the whole assignment.
Build it, check it, commit it, report, and stop.

## Goal

Elimination by hand, the old "combine equations": `eliminate` and
`isolate`, with cleanup inside every rewrite, their `Derived` origins,
`show(origins=True)` and `show_history()`, and the two errors they
raise. The checks are the derivation of kinematic-equations 005,
2.5 eliminated step by step as a new example, 3.10's proof by
elimination, and 4.1 eliminated by hand. Stop when the checks pass and
the commit is in.

## Read first

- [The spec](../spec.md): "What the prototype showed", the decisions
  "The state", "The operations" (eliminate, isolate, cleanup,
  simplifying, failures), "The display", "SymPy to watch", the 2.5
  sketch, and §003, which this checkpoint carries out. The later
  increments are context, not work. Where this page is more exact than
  the spec, follow this page.
- Checkpoints [001](001-state-and-display.md) and
  [002](002-all-at-once.md), for the layout and the conventions, and
  the code itself: `src/equarium/`, `examples/` and `tests/`.
- The old library, read-only, in `~/src/combine-equations.py/`:
  - `eliminate_variable_subst` in
    `src/combine_equations/eliminate_variable_subst.py`. It shows the
    choice by `count_ops`, and the whole-`Eq` `simplify` that this
    increment avoids.
  - The four scripts this increment ports, all under `examples/up/`:
    `ch2/kinematic-equations/kinematics-equations-005-eq-history.py`
    (its symbols and first derivation),
    `ch2/up-example-2.5/up-example-2.5-v3-001-step-by-step.py`,
    `ch3/up-example-3.10-v1-001.py` and
    `ch4/up-example-4.1/up-example-4.1-v1-006-ok-manual-elim.py`.

  Don't edit that repo.

## Starting point

`master` at the commit that adds this checkpoint, on top of `dcda22a`
(increment 002). `uv run pytest` passes 74 tests, and `uv run pyright`
reports 0 errors and 0 warnings.

A scratch prototype of the algorithm below, on the real `System`,
produced every exact result on this page. 3.10 took about 2.5 s for
each of its two runs, 4.1 about 2 s, and the rest well under a second,
so nothing here is slow.

## Build

### `errors.py`

`EliminationError` and `IsolationError`, both subclasses of
`EquariumError`, with the symbol, the labels and the reason.

### `equations.py` and `steps.py`

- **`Op`** becomes `Literal["eliminate zeros", "eliminate", "isolate"]`.
- **Two new steps** join the `Step` union:
  - `EliminateStep(symbol, using, replacement, rewritten, dropped)`.
    `using` is the label of the equation the symbol came from, whether
    it was given or chosen. `replacement` is the root that was
    substituted. `rewritten` and `dropped` are labels, in equation
    order, as for `EliminateZerosStep`.
  - `IsolateStep(symbol, label)`.

### `rewrite.py`

- **Roots of one equation for one symbol:** `sp.solve(eq, sym)`, less
  any root that still contains `sym`, each run through
  `safe_simplify`. A `NotImplementedError` means no usable roots. Any
  other exception propagates.
- **`eliminate(system, sym, using=None)`,** for one symbol:
  - **Refusals.** A known or a want raises `EliminationError`.
  - **With `using`.** A missing label raises `UsageError`. An equation
    without `sym`, or with other than exactly one root for it, raises
    `EliminationError`, and the reason gives the count.
  - **Without `using`.** The candidates are the equations that contain
    `sym` and give exactly one root. The root with the lowest
    `sp.count_ops` wins, and a tie goes to the earlier equation in the
    system's order. No candidate raises `EliminationError`, with the
    labels of the equations that contain `sym`.
  - **The rewrite.** The source equation is removed. Each other
    equation that contains `sym` gets `subs(sym, root)`. If the result
    is still an `Eq`, it's rebuilt as `sp.Eq(safe_simplify(lhs),
    safe_simplify(rhs))`, never `simplify` of the whole `Eq`. Then it
    goes through cleanup. A kept equation keeps its label and gets
    `Derived("eliminate", sym, (before, source))`.
  - **The step.** `EliminateStep`.
- **`isolate(system, sym, label)`.** A missing label raises
  `UsageError`. An equation without `sym`, or with other than exactly
  one root, raises `IsolationError` naming the count. The equation
  becomes `sp.Eq(sym, root)` under the same label, with
  `Derived("isolate", sym, (before,))`. The step is `IsolateStep`.
- **Cleanup** gains one rule, from the 001 review: a result that
  contains `sp.zoo` or `sp.nan` raises `Contradiction`, with a reason
  that says the equation is undefined. A zero alone in a denominator
  did that silently: `Eq(a, (v - x)/t1)` with `known(t1, 0)` became
  `a = zoo*(v - x)`. The rule applies to `eliminate_zeros` too.

### `system.py`

- **`eliminate(*syms, using=None)`** eliminates each symbol in turn,
  one step per symbol, so `s.eliminate(a, b)` is
  `s.eliminate(a).eliminate(b)`. That's an exception to 001's "one
  call is one step", and the spec's `show_history` sketch needs it.
  `using` with more than one symbol, or no symbols at all, raises
  `UsageError`.
- **`isolate(sym, label)`**, one line delegating to `rewrite.isolate`.
- **`show(origins=False)`** and **`show_history()`**, printing
  `render(self, origins=origins)` and `render_history(self)`.
- **`known`** also refuses `nan`, `zoo`, `oo` and `-oo` as values,
  with `UsageError`. Check with `.has(sp.nan, sp.zoo, sp.oo, -sp.oo)`,
  since `-oo` isn't `-1*oo`.

### `display.py`

- **Origins.** `render(system, symbol=terminal, origins=False)`. With
  `origins=True`, each derived equation's line is followed by its
  origin, indented by two spaces. Only the origin itself is shown, not
  its parents' origins. A `Given` equation gets no line.

  | Origin | Line |
  |---|---|
  | `Derived("eliminate", dt, ((2.2), (2.7)))` | `(2.2) ← (2.2) + (2.7), eliminate dt` |
  | `Derived("eliminate zeros", t0, ((2.2),))` | `(2.2) ← (2.2), t0 = 0` |
  | `Derived("isolate", v1, ((2.7),))` | `(2.7) ← (2.7), isolate v1` |

  The label before the arrow is the equation's own. The symbols go
  through the hook.
- **History.** `render_step` gains two forms:
  - `eliminate dt using (2.7): into (2.2)`, with `, dropped (3)` added
    when cleanup dropped something, and just `eliminate m_a using (2)`
    when nothing else contained the symbol;
  - `isolate v1 in (2.7)`.

### The example

**`examples/up_15e/ch02/example_2_5_handwritten_step_by_step.py`,**
ported from the old v3-001 script. It uses the same symbols and
equations as `example_2_5_handwritten.py`, and eliminates by hand in
the old order, a display after each stage. The old zero equations
become zero knowns plus `eliminate_zeros()`, at the point where the old
script eliminated them. The suggested stage names, each built from the
one before:

| Stage | Built by | What it shows |
|---|---|---|
| `start` | the motorist's three and the officer's three, the speed links `eq_flat(m_0_v, m_v, m_1_v, m_v)`, and `known(m_v, 15)` | (1) to (8) |
| `speeds` | `eliminate(m_0_v, m_1_v)` | `(3)  v_av_m_0_1 = m_v` (the old script printed `m_v = v_av_m_0_1`) |
| `motorist` | `eliminate(m_a, v_av_m_0_1)` | `(1)  m_v = (m_0_x - m_1_x)/(m_0_t - m_1_t)` |
| `officer` | `known({p_0_v: 0, p_0_x: 0})`, `eliminate_zeros()` | |
| `clocks` | `known({m_0_t: 0, p_0_t: 0})`, `eliminate_zeros()` | |
| `origin` | `known(m_0_x, 0)`, `eliminate_zeros()` | `(1)  m_v = m_1_x/m_1_t` |
| `place` | `known(p_a, 3)`, `add(*eq_flat(dist, m_1_x, dist, p_1_x))`, `eliminate(m_1_x, p_1_x)` | |
| `meet` | `add(*eq_flat(t_01, m_1_t, t_01, p_1_t))`, `eliminate(m_1_t, p_1_t)` | the four below |

`meet`, with the plain hook:

```
(1)  m_v = dist/t_01
(4)  v_av_p_0_1 = dist/t_01
(5)  p_a = p_1_v/t_01
(6)  v_av_p_0_1 = p_1_v/2
```

These are the old script's last four equations, except that `(6)` keeps
its shape. The old one printed `p_1_v = 2*v_av_p_0_1`. Then
`sol = meet.want(t_01, p_1_v, dist).solve()` gives the 002 formulas and
10, 30 and 150, and the `BOOK` holds those three. Under `__main__` it
shows each stage, then `meet.show(origins=True)`, `sol`, and
`meet.show_history()`.

### Tests

**`tests/test_rewrite.py`,** new:

- **kinematic-equations 005's first derivation,** with its symbols
  `x_1 x_2 v_1x v_2x v_av_x dt a_x`.
  - **The system.** (2.2) is `v_av_x = (x_2 - x_1)/dt`, (2.7) is
    `a_x = (v_2x - v_1x)/dt`, and (2.10) is `v_av_x = (v_1x + v_2x)/2`,
    with those labels.
  - **The derivation.** `eliminate(dt, using="2.7")` leaves
    `(2.2)  v_av_x = a_x*(x_1 - x_2)/(v_1x - v_2x)`, and
    `safe_simplify` of its difference from `a_x*(x_2 - x_1)/(v_2x - v_1x)`
    is 0.
  - **What it changed.** (2.7) is gone, and (2.10) is the same
    `Equation` with `Given()`. The origin of (2.2) is
    `Derived("eliminate", dt, (before, source))`. The step's
    replacement is `(-v_1x + v_2x)/a_x`.
- **The six links of 2.5,** on `chase` from `example_2_5_handwritten`.
  - **Eliminating them.**
    `chase.eliminate(m_0_v, m_1_v, m_1_x, p_1_x, m_1_t, p_1_t)` leaves
    none of the six in any equation. It adds six steps, which render
    as:

    ```
    eliminate m_0_v using (7): into (2), (3)
    eliminate m_1_v using (8): into (2), (3)
    eliminate m_1_x using (9): into (1)
    eliminate p_1_x using (10): into (4)
    eliminate m_1_t using (11): into (1)
    eliminate p_1_t using (12): into (4), (5)
    ```

  - **The solve.** The result still solves to 10, 30 and 150, with the
    002 formulas.
  - **The shape.** `(3)` reads `v_av_m_0_1 = m_v` and `(6)` reads
    `v_av_p_0_1 = p_1_v/2`, each with its left side kept.
- **The step-by-step example's `meet`** is the four equations above.
- **3.10's proof,** written out as one system, in two tests, one per
  run.
  - **Symbols.** For the dart: `d0x d1x d0y d1y d0vx d1vx d0vy d1vy
    d0t d1t`, plus `d_dt d_vav_x d_vav_y d_a_x d_a_y`. The same with
    `m` for the monkey. Then `D g v_mag angle t y`.
  - **The equations,** in this order, unlabeled:
    1. The dart's seven, in the old physics code's order:
       - `d_dt = d1t - d0t`;
       - 2.2 for x, then y: `d_vav_x = (d1x - d0x)/d_dt`;
       - 2.7 for x, then y: `d_a_x = (d1vx - d0vx)/d_dt`;
       - 2.10 for x, then y: `d_vav_x = (d0vx + d1vx)/2`.
    2. The dart's launch and fall:
       `eq_flat(d0vx, v_mag*sp.cos(angle), d0vy, v_mag*sp.sin(angle), d_a_y, -g, d0vx, d1vx)`.
       This is polar form one way, as the spec's 3.9 and 4.1 use. The
       old script used the two-way `magnitude_and_angle_equations`.
    3. The monkey's seven, the same way.
    4. The monkey's start:
       `eq_flat(m0x, D, m0y, D*sp.tan(angle), m_a_y, -g)`.
    5. The links: `eq_flat(d1t, t, m1t, t, d1y, y, m1y, y)`.
  - **The knowns.** `known(D)`, `known(v_mag)` and `known(angle)` with
    no number, and `known(g, 9.81)`. The zeros are
    `d0x d0y d_a_x d0t m_a_x m0t m0vx m0vy m1vx`, then
    `eliminate_zeros()`, which leaves 24 equations.
  - **The order of elimination.** First the monkey's x: `m_vav_x`,
    `m1x`, `m0x`. Then the old script's order:
    - the dart: `d_dt d_vav_x d0vx d1vx d0vy d_vav_y d_a_y d1vy`;
    - the monkey: `m0y m_dt m_vav_y m1vy m_a_y`;
    - the links: `d1t m1t d1y m1y y t`.
  - **The two runs:**
    - **The stated condition is all that's left:** one equation,
      `(9)  D*v_mag*sin(angle)/d1x = v_mag*sin(angle)`, which holds
      exactly when the dart reaches x = D.
    - **With `Eq(d1x, D)` added** after the links, and `d1x`
      eliminated last, no equations are left.
- **4.1 v1-006,** written out with the old names (`F1_x F1_y F1_mag
  F1_angle`, the same for F2, F3 and R, and `R_angle_deg`).
  - **The equations,** in this order:
    1. `R_x = F1_x + F2_x + F3_x`, and the same for y.
    2. `F_x = F_mag*cos(F_angle)` and `F_y = F_mag*sin(F_angle)` for
       F1, F2 and F3, in that order.
    3. `R_mag = sqrt(R_x**2 + R_y**2)`, `R_angle = atan2(R_y, R_x)`,
       and `R_angle_deg = sp.deg(R_angle)`.
  - **The knowns:** F1 50 at `0`, F2 120 at `3*sp.pi/2`, F3 250 at
    `sp.rad(127)`. The zero is a known left in place, as the old
    script's `values`, with no `eliminate_zeros()`.
  - **The eliminations.** Eliminate the three x components, then the
    three y components.
    - No `F1_x` … `F3_y` is left.
    - `F1_x` comes out of `(1)`, not `(3)`: the two roots are equally
      simple, and `(1)` comes first. The old library did the same.
  - **The solve.** `want(R_mag, R_angle_deg).solve()` gives one root,
    which matches `Answer(…, R_mag, "128")` and
    `Answer(…, R_angle_deg, "141.6")`: 128.2 N at 141.59°.
- **Isolate.** On 2.4's base, `isolate(v1, "2.7")` gives
  `(2.7)  v1 = a*t1 + v0`, with `Derived("isolate", v1, (before,))`.
- **Errors:**
  - **005's `eliminate(x_1, using="2.10")`** raises `EliminationError`.
  - **Two roots.** With `(q) y = x**2` and `(l) y = x + 2`,
    `eliminate(x)` uses `(l)`, and `eliminate(x, using="q")` raises
    `EliminationError`.
  - **Knowns and wants.** Eliminating a known (`x0` on 2.4's base) or
    a want (`x1` on `part_a`) raises `EliminationError`.
  - **Isolating.** `isolate(x, "q")` raises `IsolationError`.
  - **A contradiction.**
    `System().add(sp.Eq(x, y + 5), sp.Eq(x, y)).eliminate(x)` uses
    `(2)`, turns `(1)` into `y = y + 5`, and raises `Contradiction`.
  - **Misuse.** `using` with two symbols, `eliminate()`, a missing
    label in `using` and a missing label in `isolate` raise
    `UsageError`.
- **Undefined.** `System().add(sp.Eq(a, (v - x)/t1)).known(t1, 0).eliminate_zeros()`
  raises `Contradiction`. `known(x, sp.oo)`, `sp.nan`, `sp.zoo` and
  `-sp.oo` raise `UsageError`.

**`tests/test_display.py`,** added:

- **Origins.** After 005's elimination, `render(…, symbol=plain,
  origins=True)` has `  (2.2) ← (2.2) + (2.7), eliminate dt` under
  `(2.2)`, and nothing under `(2.10)`. On 2.4's base it has
  `  (2.2) ← (2.2), t0 = 0`. After the isolate, it has
  `  (2.7) ← (2.7), isolate v1`. Without `origins`, the render is the
  same as before.
- **History.** 005's history ends with `eliminate dt using (2.7): into (2.2)`.
  The isolate's ends with `isolate v1 in (2.7)`. `eliminate(m_a)` on
  `speeds` from the example renders as `eliminate m_a using (2)`. A
  drop shows as `, dropped (…)`: eliminating `x` from `x = y`,
  `x = y` and `z = x` drops `(2)`.

If a check here or in the spec turns out wrong, work out by hand which
side is. If it's the check, use the right answer, keep going, and say
so in your report. Don't edit `spec.md` or this page.

## Docs

- **The series [README](../README.md):** mark 003 done in its
  increments table, and update its status line. Leave the commit cell
  and this page's status line for the manager.
- **The [series map](../../README.md):** 002's status says 003 of 7 is
  done.
- **The package `README.md`** doesn't change.

## Check and commit

- `uv run pytest` passes: the 74 tests from 001 and 002, plus yours.
  If a test takes more than 5 s, say so in the report rather than
  adding the `slow` marker, which comes in 006.
- `uv run pyright`: 0 errors, 0 warnings.
- `uv run python -m examples.up_15e.ch02.example_2_5_handwritten_step_by_step`
  prints each stage, the origins, the answers and the history.
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

Then stop; increment 004 is a separate checkpoint.
