# core 008: chapters 3 and 4

**Status:** Checkpoint written (2026-11-08), waiting for review.

If you've been told to read this file, this is the whole assignment.
Build it, check it, commit it, report, and stop.

## Goal

Chapters 3 and 4's examples ported onto the core, on the physics code
that 007 copied in. That means:

- **`Formula`** in `examples/answers.py`, beside `Answer`, for answers
  the book prints as formulas.
- **Twelve new modules,** six under `examples/up_15e/ch03/` and six
  under `examples/up_15e/ch04/`, from the catalog's port list, each
  with its `BOOK`.
- **The old outputs:** `tests/test_old_outputs.py` gets chapter 3 and
  4's rows.

This is the series' last increment. Stop when the checks pass and the
commit is in.

## Read first

- [The spec](../spec.md): "Examples in the repo", §007 and its note
  dated 2026-11-08 (the split), and "Not in this spec", which leaves
  out `clear_zero_denominators`, with its note dated 2026-11-08 (3.6).
- **The catalog,**
  [001-example-catalog/catalog.md](../../001-example-catalog/catalog.md),
  above all "Recommendations for 007":
  - its sections:
    - the chapter 3 and 4 tables of "The port list";
    - "Where the port differs from the old script";
    - "The physics code";
    - the user's answers to questions 1 to 4;
  - each problem's own entry, Example 3.6 to Example 4.7. These quote,
    verbatim, what each old script prints, and say which zeros were
    equations and which were values.
- **[Checkpoint 007](007-physics-code-and-chapter-2.md),** for how a
  port is written, and its modules in `examples/up_15e/ch02/`.
  `example_2_7.py` and `example_2_8.py` show a base with branches,
  and one module importing another. `exercise_2_23.py` shows units.
- `tests/test_examples.py` and `tests/test_old_outputs.py`, which this
  increment extends.
- **The old library, read-only,** in `~/src/combine-equations.py/`:
  - the scripts the port list names, under `examples/up/ch3/` and
    `examples/up/ch4/`;
  - `clear_zero_denominators` in `src/combine_equations/solve_system.py`,
    for 3.6.

  Don't edit that repo.

## Starting point

`master` at the commit that adds this checkpoint, on top of `b800741`
(007's review). `uv run pytest` passes 216 tests and deselects the 3
slow ones, in about 25 s. `tests/test_examples.py` alone takes 6 s.
`uv run pytest -m slow` passes those 3, in about 5 min. `uv run pyright`
reports 0 errors and 0 warnings.

A scratch prototype made every port on this page, on the real code
(2026-11-08). The results:

- **The formulas.** The catalog quotes 34 formula lines for these
  scripts' wants, and 33 come out verbatim. The 34th is 3.8's range,
  the old bug the port fixes.
- **The numbers.** All 32 old numbers match by value. For 3.7, 3.9 and
  4.7, that's after putting the old givens back into the port's
  formula.
- **The `BOOK`s.** All 41 lines match: 36 `Answer`s and 5 `Formula`s.
- **pyright** reports 0 errors over the ports and `Formula`, with 15
  narrowing asserts.
- **Speed.** Ten modules import in under 4 s each, most in under 2 s.
  3.9 takes 5.7 s and 3.10 8.9 s. All 12 together take about 22 s.

The prototype's files may still be in
`/tmp/claude-1000/-home-dharmatech-journal-2026-11-06-equations/37cebb80-fcee-4b88-8a97-5f6f1fa64bf3/scratchpad/proto008/`.
They're a reference, not the source: the old scripts and the catalog
are. They import `Formula` from a scratch `formula.py`, and their
`PROTOTYPE:` comments mark the steps this page lists.

## What the prototype found

The catalog doesn't say these. This page settles them.

1. **3.6 finds no roots as ported.** After `eliminate_zeros()`,
   equation (4) is `0 = (-m_0_v_x + m_1_v_x)/dt_m_0_1`. Both
   velocities are knowns, so its one unknown is `dt_m_0_1`, and
   `sp.solve` can't solve it for that. So every solve finds none, however
   the wants are grouped.
   - **Why the old script solved:** the old library's
     `clear_zero_denominators` turned (4) into
     `-m_0_v_x + m_1_v_x = 0`. That has no unknown, so the solve left
     it out. With that function patched to do nothing, the old 3.6
     fails at its first solve: `ValueError: No solutions found.`
   - The spec leaves `clear_zero_denominators` out, "added only if a
     check fails without it". This is that check: see question 2.
   - **The port** adds `eliminate(m01.dt)` after `eliminate_zeros()`,
     as the user chose. Then (4) has only knowns, and one solve gives
     the old six formulas verbatim, in 0.4 s.
2. **3.8's by-hand step isn't enough.** The old script eliminates
   `p_0_v_x` before each solve. On equarium, with `p_0_v_x` eliminated
   through `p_0_v_x = p_1_v_x`, the solves still find no roots: the
   two-way equations (12) and (13) still hold unknowns.
   - **Why the old script solved:** its `values` gave the magnitude
     and the angle the symbols `v0` and `a0`. Those became two more
     unknowns for `sp.solve`. With the values mapped to themselves,
     the old 3.8 fails at line 127 with `ValueError: No solutions found.`
   - **The port** eliminates `p0.vel.x` and `p0.vel.y` through the
     polar equations (10) and (11). That leaves (12) and (13) with
     knowns only, so the solve leaves them out. It gives the book's
     four formulas verbatim.
3. **3.7 keeps the old by-hand step,** `eliminate(b1_vel_angle)`
   before the degrees. Without it, `sp.solve left b1_vel_angle_deg
   undetermined`. So the radians formula, which the old script printed
   before that step, gets its own solve, `sol_a_radians`. (b) and (c)
   branch from after the step. Branched from before it, (c)'s time is
   left in terms of `dt_b_0_1`.
4. **3.9 solves x and t together,** with `eliminating()`, in about
   5.5 s. That's no slower than x alone, 6.0 s. So the catalog's
   `sol_t` is `sol`.
5. **3.10 imports in 8.9 s,** not the catalog's "a second or two". The
   dart's two-way polar substitutions take 5.6 s of it. See question 1.
6. **Displayed equations keep equarium's sides,** as in 007's third
   difference. 3.10's three kept equations and its last line, and 4.1
   step by step's (3) and (4), have their sides the other way round
   from the old output. They're equal. The test of 3.10's last line
   compares the sides as equarium has them.
7. **Fewer solves, the same formulas.** The old scripts solved one
   want, or a few, at a time. One solve per part gives the same
   formulas:
   - 3.6: six solves become one;
   - 3.7: (a) seven become two, (b) two become one, (c) three become one;
   - 3.13: two become one;
   - 4.1: three become one.
8. **The `BOOK` names.** The catalog writes `R_x`, `a_x` and `f_x`,
   the printed names. The ports use the physics objects' attributes:
   `R.x`, `a.x`, `f.x`.

## Questions for the user

The user answered both on 2026-11-08, each as recommended. The
questions stay as they were asked, for the record.

1. **The slow imports.** The `slow` marker means "takes more than
   5 s". `tests/test_examples.py` imports every example, and
   `tests/test_old_outputs.py` imports every module that has old rows.
   3.9 (5.7 s) and 3.10 (8.9 s) are over the line.
   - *Recommended and chosen: mark both slow.* `uv run pytest` grows
     by about 7 s. `-m slow` then checks 3.9's and 3.10's `BOOK`s,
     3.9's old rows and 3.10's show-that.
   - Without the marks, `uv run pytest` would grow by about 22 s.
2. **3.6's zero denominator.**
   - *Recommended and chosen: the by-hand `eliminate(m01.dt)` in the
     port,* listed as a difference. The core doesn't change.
   - The alternative was `clear_zero_denominators` in the core, as the
     spec's condition allows. That's a core change in this last
     increment. It would need its own tests, another prototype pass,
     and a check that no other port's formula changes. It stays a
     candidate for a later series.

## Build

### `examples/answers.py`: `Formula`

`Formula(solution, symbol, printed)` is a frozen dataclass beside
`Answer`, with the same `mismatch() -> str | None`. It checks a formula
as the book prints it, in SymPy's syntax and the script's symbols:
`Formula(sol_top, p1.pos.y, "p_0_v_mag**2*sin(p_0_v_angle)**2/(2*g)")`.

- **At construction:**
  - `symbol` must be a want of the solution, as for `Answer`.
  - `printed` is parsed with `parse_expr`, its names bound to the
    solution's symbols by name: those of its equations, knowns, wants
    and formulas.
  - Every name in `printed` must be one of those symbols, or a SymPy
    function or constant (`sin`, `sqrt`, `pi`). Anything else is a
    `UsageError`, since a typo would otherwise parse as a new symbol.
    So is text that doesn't parse, or isn't an expression.
- **`mismatch()`** is None when the solution has exactly one root, and
  that root's formula minus the printed one simplifies to 0
  (`safe_simplify`). That's the comparison the catalog's question 2
  chose. Otherwise it's a message naming the symbol, the printed
  formula and what was found, for:
  - no roots, with the reason;
  - several roots, with each formula;
  - a printed symbol that isn't in the formula;
  - a difference that doesn't simplify to 0.
- **Why equivalence, not `str`:** all five of the book's formulas here
  also come out verbatim. But a book's formula is written by hand, and
  the print order is SymPy's. The old formulas are still compared
  verbatim, in `test_old_outputs.py`.
- **A known hole:** a printed name that SymPy defines, such as `E` or
  `I`, means SymPy's constant, unless the solution has a symbol with
  that name. No system here has one.

The module's docstring says a `BOOK` is a `list[Answer | Formula]`.

### The packages

`examples/up_15e/ch03/__init__.py` and `ch04/__init__.py`, each a
docstring naming the chapter, as `ch02`'s does:

- "Chapter 3: motion in two or three dimensions."
- "Chapter 4: Newton's laws of motion."

### The ports

Twelve new modules, named and sourced as the catalog's chapter 3 and 4
tables say. Each has the catalog's `BOOK`, but for finding 8's names
and 3.9's `sol`. They follow 007's conventions:

- values at import, and printing only under `__main__`;
- a module docstring naming the book, the problem, and the old script
  it was ported from;
- the run command.

The zeros follow the spec's rules, and each catalog entry says which
zeros were equations and which were values. Where a port uses a field
the model types as optional, it narrows it with `assert`. Those fields
are `state.vel.mag`, `state.vel.angle`, `edge.v_av`, `Point3.mag` and
`Point3.angle`. The prototype needed 15 asserts, covering about 48 uses.

**Chapter 3, `ch03/`:**

| Module | From | Notes from the prototype |
|---|---|---|
| `example_3_6.py` | 3.6 v1-000 | The base and `a_y = -g`. Zero equations `m0.pos.x`, `m0.pos.y`, `m01.a.x` and `m0.t`, eliminated in the base, then `eliminate(m01.dt)` (finding 1). Values: `m0.vel.x` 9.0, `m0.vel.y` 0.0 (so it stays in the formulas), `m1.vel.x` 9.0, `g` 9.8, `m1.t` 0.50. The distance, speed, angle and degrees are written by hand, as in the old script. One solve of seven wants: the old six and `m1.vel.y`. |
| `example_3_7.py` | 3.7 v1-000 | g = 9.80. The base, `a_y = -g` and `b0.vel.x = b1.vel.x`, with 3.6's four zero equations. The launch is one-way, in the script's own `b0_vel_mag` (37.0) and `b0_vel_angle` (53.1° in radians). Stages: `speed` adds the speed and angle by hand; `flight` adds the degrees, then `eliminate(b1_vel_angle)` (finding 3). (a): `known(b1.t, 2.00)` on `flight`, six wants, and `sol_a_radians` on `speed`. (b): `known(b1.vel.y, 0)`, then `eliminate_zeros()`. (c): `known(b1.pos.y, 0)`, then `eliminate_zeros()`, five wants with the time and the angle. |
| `example_3_8.py` | 3.8 v1-000, its bug fixed | The base, `a_y = -g` and `p0.vel.x = p1.vel.x`, with 3.6's four zero equations. Then the two-way polar equations (10) to (13), on `p0.vel.mag` and `p0.vel.angle`. `g`, the magnitude and the angle are knowns with no number (the old 9.81 was never used). `top`: `known(p1.vel.y, 0)`, `eliminate_zeros()`. `back`: `known(p1.pos.y, 0)`, `eliminate_zeros()`. Each then eliminates `p0.vel.x` using "10" and `p0.vel.y` using "11" (finding 2). `sol_top` solves t and y, `sol_range` t and x. The 90° and 45° are a comment. |
| `example_3_9.py` | 3.9 v2 | g = 9.80. The base, `a_y = -g` and `b0.vel.x = b1.vel.x`. Zero equations `b0.pos.x`, `b01.a.x`, `b0.t` and `b1.pos.y`, eliminated in the base. `b0.pos.y` 8.0. Then `magnitude_and_angle_equations(b0)`, with 10.0 and −20.0° in radians. `sol = window.solve(b1.pos.x, b1.t, strategy=eliminating())`, two roots. |
| `example_3_10.py` | 3.10 v1-001 | See below. |
| `example_3_13.py` | 3.13 001-eq | Written out, `v_TE = v_TY + v_YE` and `v_YT = -v_TY` (3.32 and 3.33), with 88 km/h and −104 km/h. One solve of both. |

**`example_3_10.py`.** Two models, each eliminated in its own system,
in the old script's order. `g`, `D`, the magnitude and the angle are
knowns with no number.

- **`dart`:** the base, `magnitude_and_angle_equations(d0)`,
  `a_y = -g`, `d0.vel.x = d1.vel.x` and its four zero equations. Then 8
  eliminations: `d01.dt`, `d01.v_av.x`, `d0.vel.x`, `d1.vel.x`,
  `d0.vel.y`, `d01.v_av.y`, `d01.a.y`, `d1.vel.y`.
- **`monkey`:** the base, `m0.pos.x = D`, `m0.pos.y = D*tan(angle)`,
  `a_y = -g` and its five zero equations. Then 5 eliminations:
  `m0.pos.y`, `m01.dt`, `m01.v_av.y`, `m1.vel.y`, `m01.a.y`.
- **`meet`:** the dart's (8) and (9) and the monkey's (9), picked by
  label where the old script picked by index, linked through `t` and
  `y`. `proved` eliminates `d1.t`, `m1.t`, `d1.pos.y`, `m1.pos.y`, `y`
  and `t`, and leaves one equation, the stated condition.
- **`reached`:** `meet` with `d1.pos.x = D` added, which the old script
  had commented out. It eliminates `d1.pos.x` too, and leaves none.
- **`agree`,** for the book's time, a new want: the dart's (8), the
  monkey's x equations (2), (6) and (8), which the old script dropped,
  and the links `d1.t = t`, `m1.t = t` and `d1.pos.x = m1.pos.x`.
  `sol_t = agree.solve(d1.t)`, in 0.1 s.

**Chapter 4, `ch04/`:**

| Module | From | Notes from the prototype |
|---|---|---|
| `example_4_1.py` | 4.1 v1-007 | The old script's local `make_force`, `polar_to_components` and `components_to_polar`, and `superposition_equations` from the physics code. `F1.angle = sp.rad(0)` is a value, with no `eliminate_zeros()`. One solve of five wants: `R.x`, `R.y`, `R.mag`, `R.angle` and `R_angle_deg`. `book_step` holds R's polar and degrees equations, with `R.x` −100 and `R.y` 80 known, and gives `sol_book`. |
| `example_4_1_step_by_step.py` | 4.1 v1-006 | Imports the forces, the helpers, `R_angle_deg` and `sol_book` from `example_4_1`, as 2.8 imports from 2.7. Stages: `start`, `xs` (`F1.x`, `F2.x`, `F3.x` eliminated), `ys` (the y's). `sol = ys.solve(R.x, R.y, R.mag, R.angle)`. Then `degrees` adds `R_angle_deg = deg(R.angle)`, and `sol_deg` solves it. |
| `example_4_4.py` | 4.4 000 | `make_point` and `newtons_second_law` from the physics code, for the old local copies. `F.y`, `a.y`, `n.x` and `w.x` are zero values, with no `eliminate_zeros()`. |
| `example_4_5.py` | 4.5 001 | `kinematics_fundamental(b, axes=["x"])`, `newtons_second_law([n, w, f], m, a)` and the link `a.x = b01.a.x`. The zeros are values. |
| `example_4_5_two_steps.py` | 4.5 000, finished | Step 1, `slide`, solves `b01.a.x`. Step 2, `push`, is Newton's law with `a.x` known as `sol_1.number(b01.a.x)`, and solves `f.x`. |
| `example_4_7.py` | 4.7 000 | Written out, `w = m*g` and `F_x = m*a_x`, with units: w = 2.49e4 N, with a comment on the book's 2.45e4; F_x = −1.83e4 N; g = 9.80 m/s². One solve of `a_x` and `m`. The `BOOK` converts twice, as the catalog's lines do. |

### The formulas the old scripts didn't print

The additions, as the prototype found them. Each `BOOK` checks its
numbers; nothing compares these formulas with old ones.

- **3.6:** `m_1_v_y = -g*m_1_t + m_0_v_y`, −4.9.
- **3.7 (c):** `b_1_t = 2*b0_vel_mag*sin(b0_vel_angle)/g`, 6.038, and
  `b1_vel_angle_deg = 180*atan2(-b0_vel_mag*sin(b0_vel_angle), b0_vel_mag*cos(b0_vel_angle))/pi`,
  −53.1.
- **3.8:**
  - `sol_top`: `p_1_t = p_0_v_mag*sin(p_0_v_angle)/g`;
  - `sol_range`: `p_1_t = 2*p_0_v_mag*sin(p_0_v_angle)/g` and
    `p_1_x = p_0_v_mag**2*sin(2*p_0_v_angle)/g`.
- **3.9:** `b_1_t = (b_0_v_mag*sin(b_0_v_angle) - sqrt(b_0_v_mag**2*sin(b_0_v_angle)**2 + 2*b_0_y*g))/g`,
  −1.674, and the same with `+`, 0.9756.
- **3.10:**
  - `d_1_t = D/(d_0_v_mag*cos(d_0_v_angle))`;
  - `proved`'s equation:
    `D*d_0_v_mag*sin(d_0_v_angle)/d_1_x = d_0_v_mag*sin(d_0_v_angle)`.
- **4.1:**
  - `R_x = F1_mag*cos(F1_angle) + F2_mag*cos(F2_angle) + F3_mag*cos(F3_angle)`,
    −100.45, and `R_y`, the same with `sin`, 79.66. That's v1-002's
    output, verbatim.
  - `sol_book`: `R_angle_deg = 180*atan2(R_y, R_x)/pi`, 141.340.
- **4.5 two steps:** `f_x = a_x*m - n_x - w_x`, −0.9.
- **4.7:** `m = w/g`, `2540.81632653061*newton*second**2/meter`, so
  2540.8 kg after `in_units(kilogram)`.

With the book's givens, the old formulas' numbers change:

- **3.7:** the speed at 2.00 s is 24.358 (old 24.350), and the height
  is 44.667 (old 44.621).
- **3.9:** x is −15.726 and 9.167 (old −15.716 and 9.164).
- **4.7:** `a_x` is −7.2024 m/s² (old −7.3275).

### Differences from the old scripts

The catalog's "Where the port differs from the old script" lists the
expected differences. This page adds findings 1, 2, 3, 6 and 7:

- 3.6's `eliminate(m01.dt)`;
- 3.8's eliminations through (10) and (11), and its `g` with no number;
- 3.7's `sol_a_radians`;
- the sides of displayed equations;
- fewer solves.

Any other difference between a port's formula or number and the old
output stops the work. Report it rather than adjusting anything, as the
spec says.

### Tests

**`tests/test_examples.py`:**

- **`test_book`** accepts `Answer` and `Formula`.
- **`test_the_examples_are_found`:** the 12 new names.
- **The slow marks (question 1):** the parameters for 3.9 and 3.10
  get `pytest.mark.slow`, through `pytest.param`. The set of slow
  example modules lives in one place, which both test files use: a
  small helper module in `tests/`, as `kinematics_005.py` is.
- **`Formula`'s own tests,** on small written-out systems, like
  `Answer`'s:
  - an equivalent form matches, such as `"sin(2*a)"` for
    `2*sin(a)*cos(a)`, and so does the verbatim form;
  - a different formula is a mismatch, and its message names both;
  - several roots, and no roots, are mismatches;
  - a printed symbol that isn't in the formula is a mismatch;
  - a symbol that isn't a want, a printed name that isn't one of the
    solution's symbols, and text that doesn't parse are each a
    `UsageError`.

**`tests/test_old_outputs.py`:**

- **The module column names the chapter,** as in `"ch02.example_2_4"`,
  and the test imports `examples.up_15e.<module>`. So the 33 rows gain
  `ch02.` and are otherwise unchanged.
- **33 new rows,** every formula the catalog quotes for a ported
  script's want:
  - 3.6: 6;
  - 3.7: 12, `sol_a_radians`'s among them;
  - 3.8: 1, `p_1_y`;
  - 3.9: 2;
  - 3.13: 2;
  - 4.1: 3;
  - 4.1 step by step: 3, `R_angle_deg`'s from `sol_deg`;
  - 4.4, 4.5 and 4.5 two steps: 1 each;
  - 4.7: 1.

  That's 66 rows in all, and the count test says so.
- **3.8's rows:**
  - `p_1_y` has no old number, so the number column is `str | None`.
  - Its range isn't a row. The old line is the bug, and the `BOOK`'s
    `Formula` checks the fixed one.
- **`OLD_GIVENS`:** the old givens that differ.
  - They are g = 9.81 for 3.7 and 3.9, and w = 2.45e4 N and
    g = 9.81 m/s² for 4.7.
  - For those modules' rows, the number check takes the solution's
    knowns, puts these values in place of the port's, and substitutes
    them into the port's formula.
  - So every other given is checked against the old script's.
- **3.10's show-that,** a test of its own in this file:
  - `proved` has one equation, the old last line with its sides
    swapped (above), as a `str` of each side;
  - it becomes `true` at `d1.pos.x = D`;
  - `reached` has no equations.
- **Slow (question 1):** 3.9's two rows and 3.10's test.
  - Import a slow module inside its test, never at the top of a file,
    or the fast run pays for it at collection.

**The tests that exist** stay as they are. They test the core on
written-out systems:

- `tests/test_roots.py`: 3.9 one-way;
- `tests/test_strategies.py`: 3.9 and 4.1 two-way;
- `tests/test_rewrite.py`: 3.10, and 4.1 by hand.

The ports add the physics code and the book's numbers.
`test_rewrite.py`'s "141.6" is the old number on the by-hand system,
and stays.

If a check here or in the catalog turns out wrong, work out which side
is. If it's the check, use the right answer, keep going, and say so in
your report. Don't edit `spec.md`, the catalog's recommendations, or
this page.

## Docs

- **The series [README](../README.md):** mark 008 done in its
  increments table, and update its status line: 001 to 008 are done.
  Leave the commit cell, this page's status line and the series'
  closing for the manager.
- **The [series map](../../README.md):** 002's status says 8 of 8 are
  done.
- **The catalog's Index:** in its "In equarium" column, each chapter 3
  and 4 problem names its new module or modules, beside the tests that
  are there. Touch nothing else in the catalog.
- **The package `README.md`:** no change. Its sentence on
  `examples/up_15e/` still holds.

## Check and commit

- **`uv run pytest`** passes: the 216 fast tests, plus yours. Report
  how long `tests/test_examples.py` takes now.
- **`uv run pytest -m slow`** passes the 3 slow tests, plus the ones
  this page marks. It takes over 5 minutes, so run it in the
  background.
- **`uv run pyright`:** 0 errors and 0 warnings, over `src`, `tests` and
  `examples`.
- **Every new module** runs with
  `uv run python -m examples.up_15e.ch03.<name>` or `….ch04.<name>`.
- **No files outside the repo.** Keep scratch output in your own
  scratch folder, not in `~/journal/2026-11-06-equations/`.
- **One commit on `master`,** with the code, tests and docs, in the
  style of `git log`: a subject line, then a wrapped paragraph saying
  what and why. Don't push.

## Report

When done, say in a few lines:

- the commit, the number of tests, fast and slow, and how long
  `tests/test_examples.py` takes;
- the number of narrowing asserts in the ports;
- any formula or number that differed from the old output beyond the
  listed differences;
- what you decided where this page left a choice;
- anything in the spec, the catalog or this checkpoint that was wrong
  or unclear, and what you did instead.

Then stop. This is the series' last increment. The manager reviews it
and closes the series.
