# core 006: elimination attempts

**Status:** Done at `9ec5d88` and reviewed (2026-11-08).

If you've been told to read this file, this is the whole assignment.
Build it, check it, commit it, report, and stop.

## Goal

The `eliminating` strategy, the old library's version 2: when
`all_at_once` finds no roots, eliminate one connected unknown and try
again. Plus the time on the display, and the `slow` marker for tests
that take more than 5 s. The checks are 3.9 and 4.1 with the two-way
polar equations, which `all_at_once` alone can't solve. Stop when the
checks pass and the commit is in.

## Read first

- [The spec](../spec.md): "What the prototype showed" (the 3.9
  bullet), the decisions "Solving", "Strategies", "The display" and
  "SymPy's rough edges" (slow solves, slow tests), and §006, which this
  checkpoint carries out. Where this page is more exact than the spec,
  follow this page.
- Checkpoints [001](001-state-and-display.md) to
  [005](005-units.md), for the layout and conventions, and the code
  itself: `src/equarium/`, `examples/` and `tests/`. 004's 3.9 test is
  the starting point for this one.
- The old library, read-only, in `~/src/combine-equations.py/`:
  - `solve_with_elimination_attempts` in
    `src/combine_equations/solve_system.py`, the algorithm ported here;
  - `examples/up/ch3/up-example-3.9-v2.py` and
    `examples/up/ch4/up-example-4.1/up-example-4.1-v1-003-4-force-equations.py`.

  Don't edit that repo.

## Starting point

`master` at the commit that adds this checkpoint, on top of `8f1a98d`
(increment 005). `uv run pytest` passes 152 tests in about 18 s, and
`uv run pyright` reports 0 errors and 0 warnings.

## What the prototype found

A scratch prototype of the strategy below ran on the real code.

- **3.9 with the two-way polar equations.** `all_at_once` finds no
  roots, in 0.6 s. `eliminating()` makes seven eliminations and finds
  the two roots, −15.7 and 9.16, in 6.0 s.
- **4.1 v1-003, one want at a time.**
  - **R_x** comes out in 89 s, after four eliminations, against the
    old run's 1 min 37 s.
  - **R_y** comes out in 210 s, after seven, against the old run's
    3 min 45 s.
  - **|R| didn't finish in 20 minutes.** After three eliminations,
    `sp.solve` never returned.
  - **All four wants in one solve didn't finish in 25 minutes either.**
- **The spec is wrong about 4.1.** Its §006 expects |R| 128.2 and
  141.6° from v1-003. But the old script, run again on 2026-11-08,
  "solves" |R| and the angle as `R_mag = sqrt(R_x**2 + R_y**2)` and
  `R_angle = atan2(R_y, R_x)`. Those are formulas in terms of other
  unknowns, not numbers. Its last step, `R_angle_deg`, then raises
  "No solutions found". The 128.2 N and 141.6° come from the one-way
  versions, v1-006 and v1-007.
  - Since 004, `all_at_once` refuses such a formula with "left R_mag in
    terms of the unknowns R_x, R_y". So `eliminating` goes on, and
    SymPy then hangs.
  - So the 4.1 check here is R_x and R_y. |R| and the angle aren't
    reachable with the two-way equations, in the old library or the
    new.

## Build

### `strategies.py`, new

**`eliminating(max_eliminations: int = 10) -> Strategy`** returns a
strategy. A negative count raises `UsageError`. The strategy, given a
system:

1. **Start the clock.** Use `time.perf_counter()`.
2. **Run `all_at_once`.** If it finds roots, stop.
3. **Choose what to eliminate.** The candidates are the analysis's
   connected unknowns that aren't wants. Sort them the old way, by:
   1. whether the symbol occurs in any equation that contains a want
      (those that don't come first);
   2. then the number of equations that contain it, fewest first;
   3. then the name.
4. **Eliminate the first candidate that can be eliminated,** with
   `system.eliminate(sym)`, the real operation, so each elimination is
   a step in the history.
   - An `EliminationError` moves on to the next candidate.
   - A `Contradiction` propagates, since it means the equations can't
     all hold.
5. **Run `all_at_once` again** on the result, and repeat from step 3,
   up to `max_eliminations` eliminations in all.
6. **Return the last solution,** with `elapsed` set to the whole run.

Its system is the one after the eliminations, so
`solution.system.show_history()` lists them. If it ends with no roots,
because the count ran out or nothing could be eliminated, the reason
is the last `all_at_once` reason followed by
`, after 3 eliminations` (`1 elimination` for one). With no
eliminations made, the solution is exactly `all_at_once`'s, so
`eliminating(max_eliminations=0)` is `all_at_once`.

`strategies.py` imports `solve.py` and `errors.py` at runtime, and
`System` only under `TYPE_CHECKING`, as the other modules do.
`equarium` re-exports `eliminating`.

### `display.py`

`render_solution` ends with a line `time: 6.02 s`, two decimals, when
`elapsed` is at least 1 s. That holds after the roots and after
`no roots: …` alike. Below 1 s there's no line, so every earlier render
test still holds.

### `pyproject.toml`

Under `[tool.pytest.ini_options]`, register the marker and skip it by
default:

```toml
addopts = "-m 'not slow'"
markers = ["slow: takes more than 5 s; run with -m slow"]
```

`uv run pytest` then skips the slow tests. `uv run pytest -m slow` runs
only them, since `-m` on the command line overrides `addopts`, and
`-m "slow or not slow"` runs everything. A scratch project confirmed
all three.

### Tests

**`tests/test_strategies.py`,** new.

**3.9 with the two-way polar equations.** 004's 3.9 system, built the
same way, with the components-to-polar pair added to the polar `add`.
That gives the old `magnitude_and_angle_equations` order:

```python
eq_flat(b0vx, v_mag*sp.cos(angle), b0vy, v_mag*sp.sin(angle),
        v_mag, sp.sqrt(b0vx**2 + b0vy**2), angle, sp.atan2(b0vy, b0vx))
```

That's labels (1) to (13): the seven, then `(8) b_a_y = -g`,
`(9) b0vx = b1vx`, and the four. Then:

- the zeros `b0x b_a_x b0t b1y` and `eliminate_zeros()`;
- then `known` g 9.81, `b0y` 8.0, `v_mag` 10.0 and `angle`
  `sp.rad(-20)`, each its own call, in that order;
- then `want(b1x)`.

The checks:

- **All at once** (not slow): `solve()` has no roots, with the reason
  `sp.solve found no roots`.
- **Eliminating** (`slow`, about 6 s):
  - `solve(strategy=eliminating())` gives two roots, which match
    "-15.7", "9.2".
  - `.where(b1x > 0)` matches "9.2".
  - The last seven lines of `render_history(sol.system, symbol=plain)`
    are:

    ```
    eliminate b1t using (1)
    eliminate b1vy using (5): into (7)
    eliminate b_a_y using (8): into (7)
    eliminate b_vav_y using (3): into (7)
    eliminate b1vx using (4): into (6), dropped (9)
    eliminate b0vx using (6): into (10), (12), (13)
    eliminate b0vy using (11): into (7), (12), (13)
    ```

  - `render_solution(sol, symbol=plain)` ends with a line that matches
    `time: \d+\.\d\d s`.
- **Giving up** (not slow): `eliminating(max_eliminations=1)` gives no
  roots, with the reason `sp.solve found no roots, after 1 elimination`.
  Its history ends with `eliminate b1t using (1)`.
- **No eliminations** (not slow):
  - `eliminating(max_eliminations=0)` gives a solution equal to
    `all_at_once`'s, on this system (no roots) and on 2.4's `part_a`
    (43 and 23).
  - `eliminating()` on `part_a` equals `sol_a`, and its system is
    `part_a` itself.
- **Misuse:** `eliminating(-1)` raises `UsageError`.

**4.1 v1-003,** written out with 003's names for 4.1.

- **The equations,** in this order:
  1. `R_x = F1_x + F2_x + F3_x`, and the same for y.
  2. The two-way polar equations for F1, F2, F3 and R, in that order,
     four each: `F_x = F_mag*cos(F_angle)`, `F_y = F_mag*sin(F_angle)`,
     `F_mag = sqrt(F_x**2 + F_y**2)`, `F_angle = atan2(F_y, F_x)`.
  3. `R_angle_deg = sp.deg(R_angle)`.

  That makes (1) to (19).
- **The knowns** are 003's: F1 50 at `0`, F2 120 at `3*sp.pi/2`, F3
  250 at `sp.rad(127)`.
- **Two tests, both `slow`:**
  - **R_x.** `solve(R_x, strategy=eliminating())` takes about 90 s. It
    eliminates `R_angle_deg F1_y F2_y F3_y`, in that order, and gives
    `R_x = F1_mag*cos(F1_angle) + F2_mag*cos(F2_angle) + F3_mag*cos(F3_angle)`,
    which matches "-100.45", the old script's number.
  - **R_y.** `solve(R_y, strategy=eliminating())` takes about 210 s.
    It eliminates `R_angle_deg F1_x F2_x F3_x R_angle R_mag R_x`, and
    gives the same sum with `sin`, matching "79.66".
- **Not tested,** for the reason above: |R|, the angle, and all wants
  at once. Put a comment in the test file saying why, with the old
  script's output.

**`tests/test_display.py`,** added:

- `Solution(part_a, sol_a.roots, 1.5)` renders as the 002 block plus a
  last line `time: 1.50 s`.
- A no-roots solution with `elapsed` 2.0 ends with `time: 2.00 s`.
- `sol_a` itself has no time line.

If a check here or in the spec turns out wrong, work out by hand which
side is. If it's the check, use the right answer, keep going, and say
so in your report. Don't edit `spec.md` or this page.

## Docs

- **The series [README](../README.md):** mark 006 done in its
  increments table, and update its status line. Leave the commit cell
  and this page's status line for the manager.
- **The [series map](../../README.md):** 002's status says 006 of 7 is
  done.
- **The package `README.md`'s Development section:** add
  `uv run pytest -m slow` after `uv run pytest`, with a few words on
  what it runs.

## Check and commit

- `uv run pytest` passes the 152 earlier tests plus your fast ones,
  and skips the slow ones.
- `uv run pytest -m slow` passes the slow ones. Report each one's time.
- `uv run pyright`: 0 errors, 0 warnings.
- The three examples still run.
- One commit on `master`, with the code, tests and docs, in the style
  of `git log`: a subject line, then a wrapped paragraph saying what
  and why. Don't push.

## Report

When done, say in a few lines:

- the commit, the number of fast and slow tests, and each slow test's
  time;
- where you needed a `cast`;
- anything in the spec or this checkpoint that was wrong or unclear,
  and what you did instead.

Then stop. Increment 007 needs the example catalog (series 001) first,
so its checkpoint waits for that.
