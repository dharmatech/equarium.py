# physics 002: chapters 3 and 4, renamed

**Status:** Done at `a5f848d` and reviewed (2026-11-08).

If you've been told to read this file, this is the whole assignment.
Build it, check it, commit it, report, and stop.

## Goal

The vectors of the new physics layer, and chapters 3 and 4 moved onto
it. As in 001, only names change: every equation is the same, in the
same order. That means:

- **`vectors.py` grows:** `Vec`, the arithmetic (`+`, `-`, unary `-`,
  `*` by a scalar, `sum()`), `.eq`, lone vectors (`Vector("F1", XY)`)
  and the polar parts (`mag`, `angle`, `angle_deg`).
- **`polar.py`, new:** `from_polar` and `to_polar`.
- **`notation.py` grows** the rows for the polar parts and lone vectors.
- **Chapters 3 and 4's 10 modules** use the new layer, with the same
  equations in the same order.
- **`Formula` takes an expression,** not a string.
- **The old formulas, renamed back.** `old_name` grows the lone-vector
  rule and the polar parts. All 66 rows of `tests/test_old_outputs.py`
  and 3.10's show-that come out verbatim, with their numbers.
- **New misuses** in `tests/physics_misuse.py`.

The old copy, `kinematics_states.py` and `newtons_laws.py`, stays until
007. After this increment no example imports it. Only
`tests/test_physics.py` does, to compare.

**Not in this increment:**

- `degrees`, one-way polar everywhere, and the symbols the examples
  make themselves (003). So `dist`, `vel_mag`, `vel_angle`,
  `vel_angle_deg`, `b0_vel_mag`, `b0_vel_angle`, `b1_vel_mag`,
  `b1_vel_angle`, `b1_vel_angle_deg` and `R_angle_deg` stay plain.
- `Event` (004), so 3.10's `t` and `y` stay plain.
- The projectile setup (005).
- `mass` and `newton` (006), so `m` stays plain, and 4.4's and 4.5's
  `a` stays a lone vector.
- No by-hand step is dropped. 3.6's `eliminate(m01.dt)`, 3.8's two
  `eliminate(…, using=…)` and 3.9's `eliminating()` stay. 3.9 and 3.10
  stay in `SLOW_EXAMPLES`.

## Read first

- **[The spec](../spec.md).** In "Decisions": "Vectors and vector
  equations", "Polar and degrees", "Book notation", "The examples" and
  "The tests". Then "### 002 chapters 3 and 4, renamed", "How each
  increment lands" and "SymPy to watch".
- **[Checkpoint 001](001-symbols-and-chapter-2.md),** and what it
  built in `src/equarium/physics/`: `symbols.py`, `axes.py`,
  `vectors.py`, `particles.py`, `kinematics.py`, `notation.py` and
  `__init__.py`. Also `tests/old_names.py`, `tests/physics_misuse.py`
  and `tests/test_physics.py`.
- **[002's checkpoint 008](../../002-core/checkpoints/008-chapters-3-and-4.md),**
  for how chapters 3 and 4 were ported, and which of their zeros are
  equations and which are values.
- **The old copy.** In `kinematics_states.py`: `make_point`,
  `make_states_model`'s names (`m_0_v_mag`, `m_0_v_angle`) and
  `magnitude_and_angle_equations`. In `newtons_laws.py`:
  `superposition_equations` and `newtons_second_law`.
- **The 10 modules,** listed in "The examples" below,
  `examples/answers.py` (`Formula`), `tests/test_examples.py`,
  `tests/test_old_outputs.py` and `tests/slow_examples.py`.
- **The prototype,** outside the repo, in
  `~/.config/Claude/side-session-notes/local_9ac850c1-eb15-42fc-bbb0-61739b724d16/004-spec-prototype/layer.py`:
  `Vec`, `Vector`'s arithmetic and `.eq`, `from_polar` and `to_polar`.
  It's data to reuse, not the source: the spec and this page win. Where
  it differs:
  - its `Vec` field is `parts`. This page calls it `components`, as
    `Vector.components`;
  - its `+` and `.eq` don't check the axes, so `XY + X` drops the `y`
    silently, through `zip`. Its `__radd__` takes anything;
  - its polar methods live in `Vector`. Here they delegate to
    `polar.py`;
  - it has `polar()`, both ways in one helper, which the spec rules out,
    and `degrees()`, which is 003;
  - it makes a lone vector with a function, `vector("F1", XY)`. Here
    it's `Vector("F1", XY)`.

## Starting point

The branch `2026-11-08-physics-redesign`, at the commit that adds this
checkpoint, on top of `45650a2` (the review of 001). Check it with
`git branch --show-current`. If you're on another branch, stop and ask.
Don't switch branches, stash or reset.

`uv run pytest` passes 294 tests and deselects 8 slow ones, in about
35 s. `uv run pytest -m slow` passes those 8. `uv run pyright` reports
0 errors and 0 warnings.

Checked in scratch while writing this page, on the repo at `45650a2`:

- **4.1 renames back verbatim.** The prototype's rename check left
  4.1's forces plain, since 4.1's local `make_force` made them. A
  scratch port with lone vectors, `R.eq(F1 + F2 + F3)`, `from_polar`
  and `to_polar`, gave all six 4.1 rows verbatim, renamed back. The
  numbers are the same: 128.2, 2.471 and 141.59. `main.py` took 1.3 s,
  and step by step 2.5 s. Step by step's four equations left print as
  `-F2.mag*cos(F2.angle) - F3.mag*cos(F3.angle) + R.x = F1.mag*cos(F1.angle)`,
  and so on.
- **The rest of chapters 3 and 4.** With the old copy made to produce
  the new `Var`s, as the prototype did, the other 27 rows of chapters 3
  and 4 came back verbatim, and so did 3.10's show-that.
- **The same equations,** as strings:
  - `*d0.vel.from_polar(), *d0.vel.to_polar()` is
    `magnitude_and_angle_equations(d0)`, renamed;
  - `(F + n + w).eq(a * m)` is `newtons_second_law([F, n, w], m, a)`;
  - `R.eq(F1 + F2 + F3)` is `superposition_equations(R, [F1, F2, F3])`.
- **Pyright** flags `.mag` and `.from_polar()` on an `X` vector
  (`reportAttributeAccessIssue`), `XY + X` (`reportOperatorIssue`) and
  `.eq` across dimensions (`reportArgumentType`), and nothing else. An
  ignore on a correct line fails the run.
- **`sum()` and pyright.** Pyright types `sum([F1, F2, F3])` as
  `Vector[XY] | Literal[0]`, from typeshed, since an empty sum is 0. So
  `.eq` doesn't take it. See "`sum()`" below.

## Build

### `vectors.py`: lone vectors and the polar parts

`Vector` keeps its fields, `x`, `y` and `components`.

- **A lone vector** is `Vector("F1", XY)`. 001's field defaults
  (`where=""`, `quantity=()`) already make it, and its components are
  `F1.x` and `F1.y`, `Var("F1", "", "x")`.
- **Its name is checked,** in `__post_init__`: a Python identifier,
  which may end in a digit, as `F1` does. Otherwise `UsageError`. A
  state's or an edge's vector passes, since the particle checked its
  name.
- **The polar parts** are properties: `mag`, `angle` and `angle_deg`.
  Each is `Var(owner, where, *quantity, part)`: `m0.vel.mag`,
  `F1.angle`, `R.angle_deg`. Each annotates `self: Vector[XY]`, so
  pyright flags them on an `X` or `Y` vector.
- **Every `XY` vector has them,** positions and edge vectors included.
  `angle_deg` has no use until 003's `degrees`, but it's a polar part.
- **At run time,** a polar part of a vector not in `XY` raises
  `UsageError`, as `x` and `y` do: `m0.pos is in X, so it has no mag`.

### `vectors.py`: `Vec`, the arithmetic and `.eq`

- **`Vec[A: Axes]`,** a frozen dataclass: a vector expression. Its
  fields are `axes: type[A]` and `components: tuple[sp.Expr, ...]`, one
  expression per axis, in the axes' order. It has no name, no `x` or
  `y`, and no polar parts.
- **The arithmetic,** on both `Vector` and `Vec`. Each result is a
  `Vec`, component by component:
  - `u + v` and `u - v`, where `v` is a `Vector[A]` or a `Vec[A]`;
  - `-u`;
  - `u * k` and `k * u`, for a scalar `k: sp.Expr | float`. Pyright
    takes an `int` as a `float`. `a * m` and `m * a` both work: SymPy
    returns `NotImplemented` for a vector, so Python calls `__rmul__`.
- **`.eq(other)`,** on both: one `sp.Eq` per axis, x first,
  `Eq(self's component, other's)`. `other` is a `Vector[A]` or a
  `Vec[A]`. Narrow each with `cast`, as `kinematics.py` does. As
  strings:

  ```
  R.eq(F1 + F2 + F3)
  Eq(R.x, F1.x + F2.x + F3.x)
  Eq(R.y, F1.y + F2.y + F3.y)

  (F + n + w).eq(a * m)
  Eq(F.x + n.x + w.x, m*a.x)
  Eq(F.y + n.y + w.y, m*a.y)
  ```

- **How a `Vector` becomes a `Vec`** is your choice. Keep it private.
- **Run time agrees with pyright.** `+`, `-` and `.eq` with a vector of
  other axes raise `UsageError`, naming both axes. So does an operand
  that isn't a vector, and a `k` that isn't a scalar (an `sp.Expr`, an
  `int` or a `float`). Without the check, `zip` would drop an axis
  silently.

### `sum()`

- **`sum()` works,** through `__radd__`, on both `Vector` and `Vec`.
  It takes `0`, the start of `sum()`, and gives the `Vec`. Any other
  left operand raises `UsageError`. Annotate it `other: int`, or
  typeshed's `sum` won't match it.
- **Pyright types `sum([F1, F2, F3])` as `Vector[XY] | Literal[0]`.**
  So `.eq` doesn't take it, and no example uses `sum()`: 4.1 writes
  `F1 + F2 + F3`. The tests check it by value:
  `sum([F1, F2, F3]) == F1 + F2 + F3`. Don't widen `.eq` for it.

### `polar.py`

- **Two plain functions,** each taking a `Vector[XY]` and returning
  `list[sp.Eq]`:

  | Function | Equations |
  |---|---|
  | `from_polar(v)` | `v.x = v.mag*cos(v.angle)`, `v.y = v.mag*sin(v.angle)` |
  | `to_polar(v)` | `v.mag = sqrt(v.x**2 + v.y**2)`, `v.angle = atan2(v.y, v.x)` |

- **The methods delegate:** `Vector.from_polar(self: Vector[XY])` and
  `Vector.to_polar(self: Vector[XY])` are one-line calls into it.
  Import `Vector` under `TYPE_CHECKING` in `polar.py`, as
  `kinematics.py` imports `Particle`, so the two modules don't import
  each other at run time.
- **One way each.** No helper for both ways, and no `degrees` (003).
- **`d0.vel`'s, as strings,** from-polar then to-polar:

  ```
  Eq(d0.vel.x, d0.vel.mag*cos(d0.vel.angle))
  Eq(d0.vel.y, d0.vel.mag*sin(d0.vel.angle))
  Eq(d0.vel.mag, sqrt(d0.vel.x**2 + d0.vel.y**2))
  Eq(d0.vel.angle, atan2(d0.vel.y, d0.vel.x))
  ```

### `notation.py`: the rows for this increment's symbols

The rows come with their symbols, as 001 said, and this increment adds
the polar parts and the lone vectors. The spec gives 003 the rows for
`degrees`. Nothing in chapters 3 and 4 prints the book's form, so the
rows can't move a formula.

- **This increment's rows** of the spec's table:

  | Symbol | Book | With owner `P` |
  |---|---|---|
  | `m0.pos.mag` | `r0` | `rP0` |
  | `m0.vel.mag` | `v0` | `vP0` |
  | `m0.vel.angle` | `α0` | `αP0` |
  | `m0.pos.angle` | `θ0` | `θP0` |
  | `F1.x`, `F1.y` | `F1x`, `F1y` | |
  | `F1.mag` | `F1` | |
  | `R.angle` | `θR` | |

- **The order is the book's,** as in 001: letter, owner, state. So
  `θP0` follows `rP0`, though the spec's table leaves that cell blank.
- **A lone vector's name is its own.** `owners` applies to particles,
  not to lone vectors.
- **Still printed as names:** `angle_deg` (until 003), an edge vector's
  polar parts (`m01.a.mag`), and any other `Var` the table doesn't
  cover.

### `__init__.py`

- **Re-export `Vec`** too, in `__all__`.
- **The docstring** says vectors add, subtract, scale, make equations
  with `.eq`, and have polar parts, with `from_polar` and `to_polar`.
  It says the old copy stays until increment 007, and that only
  `tests/test_physics.py` still uses it, to compare.

### The examples

The 10 modules:

| Module, under `examples/up_15e/` | Owners | Notes |
|---|---|---|
| `ch03/examples/n06/main.py` | `m`, `XY` | `eliminate(m01.dt)` stays. `dist`, `vel_mag`, `vel_angle` and `vel_angle_deg` stay plain. |
| `ch03/examples/n07/main.py` | `b`, `XY` | The launch stays written out, in its own `b0_vel_mag` and `b0_vel_angle`. Its five symbols stay plain. |
| `ch03/examples/n08/main.py` | `p`, `XY` | The four written-out polar equations become `*p0.vel.from_polar(), *p0.vel.to_polar()`: the same four. Its assert goes. The two `eliminate(…, using=…)` stay. `Formula` takes expressions. |
| `ch03/examples/n09/main.py` | `b`, `XY` | `*b0.vel.from_polar(), *b0.vel.to_polar()`. Its assert goes. `eliminating()` stays. |
| `ch03/examples/n10/main.py` | `d`, `m`, `XY` | `*d0.vel.from_polar(), *d0.vel.to_polar()`. Its three asserts go. `t` and `y` stay plain. `Formula` takes an expression. |
| `ch04/examples/n01/main.py` | lone `F1`, `F2`, `F3`, `R`, `XY` | The local helpers go. `R.eq(F1 + F2 + F3)`, `*F1.from_polar()` and so on, and `*R.to_polar()`. Its four asserts go. `R_angle_deg` stays plain. |
| `ch04/examples/n01/main_step_by_step.py` | the same | Imports the vectors, `R_angle_deg` and `sol_book` from `main.py`, as now, but not the helpers. Its four asserts go. |
| `ch04/examples/n04/main.py` | lone `F`, `n`, `w`, `a`, `XY` | `(F + n + w).eq(a * m)`. `m` stays plain. |
| `ch04/examples/n05/main.py` | `b`, `X`; lone `n`, `w`, `f`, `a`, `XY` | `(n + w + f).eq(a * m)`, then the link `sp.Eq(a.x, b01.a.x)`, as now. |
| `ch04/examples/n05/main_two_steps.py` | `b`, `X`; lone `n`, `w`, `f`, `a`, `XY` | Step 2's `(n + w + f).eq(a * m)`. |

**Why 4.4's and 4.5's forces are `XY`.** `make_point` made x and y, and
`newtons_second_law` always wrote both. So (5) and (6) stay two
equations. 006 moves the bottle's forces to `X`.

**How each one changes:**

- `make_states_model("m", 2)` becomes `Particle("m", 2, XY)`. Chapter
  3's particles are `XY`: their kinematics call had `axes=["x", "y"]`.
  4.5's bottle is `Particle("b", 2, X)`: its call had `axes=["x"]`.
- `m.edges[0]` becomes `m.edge(0, 1)`.
- `kinematics_fundamental(m, axes=…)` becomes `m.kinematics()`.
- `magnitude_and_angle_equations(s)` becomes
  `*s.vel.from_polar(), *s.vel.to_polar()`.
- `make_point("n")` becomes `Vector("n", XY)`, and so does 4.1's
  `make_force("F1")`.
- `newtons_second_law([n, w, f], m, a)` becomes `(n + w + f).eq(a * m)`,
  with the forces in the old order.
- `superposition_equations(R, [F1, F2, F3])` becomes
  `R.eq(F1 + F2 + F3)`.
- 4.1's `polar_to_components(F)` becomes `*F.from_polar()`, and
  `components_to_polar(R)` becomes `*R.to_polar()`.
- **The asserts on `mag`, `angle` and `v_av` go,** 13 of them: 3.8 (1),
  3.9 (1), 3.10 (3), 4.1 (4) and 4.1 step by step (4). Nothing is
  optional any more.
- **Everything else stays:** the same `add`s, knowns, wants,
  eliminations and solves, in the same order, and the same `BOOK`
  values. `eq_flat` stays where a module writes its own equations, such
  as 3.6's speed, 3.7's launch and 3.10's links.
- **Symbols a module makes itself stay plain,** with their names (see
  "Not in this increment").
- **Comments and docstrings use the new names.** A comment that quotes
  a formula quotes it as the module prints it now. That includes 3.10's
  kept equations, 4.1 step by step's four equations left, and
  docstrings such as 3.6's "equation (4) is
  `0 = (-m_0_v_x + m_1_v_x)/dt_m_0_1`".
- **Docstrings that name the old code** say what the module uses now:
  4.1's (both) "written out with the physics code's `Point3`", 4.1's
  "Its local `make_force`, `polar_to_components` and
  `components_to_polar` stay here", and 4.4's and 4.5 two steps'
  "the physics code's `make_point` and `newtons_second_law`".
- **The first lines, "with the physics code", the "Ported from" lines
  and the run commands stay,** as in chapter 2.

### `Formula` takes an expression

In `examples/answers.py`:

- **`Formula(solution, symbol, expr)`,** with `expr: sp.Expr`. Its
  fields are `solution`, `symbol` and `expr`.
- **When made, it checks:**
  - the symbol is a want of the solution, as now;
  - `expr` is an `sp.Expr`, not a string or a relation. Otherwise
    `UsageError`;
  - every free symbol of `expr` is a symbol of the solution: of its
    equations, knowns, wants or formulas. Otherwise `UsageError`,
    naming it. The check is by identity, not by name, so a plain
    `sp.Symbol("p0.vel.mag")` is caught.
- **`mismatch()` doesn't change:** one root, every symbol of `expr` in
  the root's formula, and a difference that simplifies to 0. Its
  messages print `expr` with `str`.
- **The string parsing goes:** `_parse`, `_sympy_name`, and the imports
  only they need (`io`, `keyword`, `tokenize`, `parse_expr`,
  `AppliedUndef`). `_symbols_by_name` becomes the set of the solution's
  symbols.
- **The docstrings** use an expression in the new names:
  `Formula(sol_top, p1.pos.y, p0.vel.mag**2*sp.sin(p0.vel.angle)**2/(2*g))`.
- **3.8's `BOOK`:**

  ```python
  BOOK: list[Formula] = [  # University Physics, 15th ed.
      Formula(sol_top, p1.t, p0.vel.mag * sp.sin(p0.vel.angle) / g),
      Formula(sol_top, p1.pos.y, p0.vel.mag**2 * sp.sin(p0.vel.angle) ** 2 / (2 * g)),
      Formula(sol_range, p1.t, 2 * p0.vel.mag * sp.sin(p0.vel.angle) / g),
      Formula(sol_range, p1.pos.x, p0.vel.mag**2 * sp.sin(2 * p0.vel.angle) / g),
  ]
  ```

- **3.10's:** `Formula(sol_t, d1.t, D / (d0.vel.mag * sp.cos(d0.vel.angle)))`.

### If a formula moves

Every row of `tests/test_old_outputs.py`, renamed back, must come out
verbatim, and so must 3.10's show-that. The scratch checks found none
that moved. If one does, stop. Don't change the row, the module's
equations, or the order of anything to make it pass. Report the row,
what came out, and what you think moved it. The same holds for a
`BOOK` that stops matching.

### Tests

**`tests/old_names.py`:**

- **The lone-vector rule:** `F1.x` → `F1_x`, `F1.y` → `F1_y`,
  `F1.mag` → `F1_mag`, `F1.angle` → `F1_angle`. These are
  `make_point`'s names. 4.4's `a.x` is `a_x`.
- **A state's velocity in polar:** `m0.vel.mag` → `m_0_v_mag`,
  `m0.vel.angle` → `m_0_v_angle`. These are `make_states_model`'s.
- **Still raises:** a position's or an edge's polar parts, `angle_deg`,
  and any other `Var`. The old code had none of them. 003 adds the
  ones it needs.
- **No per-module map yet.** `m` stays plain. `meet.t` (004) and
  `b.mass` (006) bring the map.
- The module docstring says which rules there are.

**`tests/test_old_outputs.py`:**

- **The rows don't change,** not by one character: the 66 rows of
  `OLD`, `R_MAG_4_1`, `R_ANGLE_4_1`, `OLD_GIVENS`, `OLD_3_10` and the
  count.
- **3.10's show-that** compares the sides through `old_str`, and puts
  `Var("d", "1", "pos", "x")` where it had `sp.Symbol("d_1_x")`. Its
  assertions stay the same otherwise.
- **Tests of `old_name`:** each new rule. The test of a `Var` the rule
  doesn't know needs one that still has no rule, such as
  `Var("m", "0", "pos", "mag")` or `Var("b", "", "mass")`.

**`tests/test_physics.py`:**

- **Lone vectors:** `Vector("F1", XY)`'s `x` and `mag` are named
  `F1.x` and `F1.mag`; two made alike are equal. The names `"m.x"`,
  `""`, `"2F"` and `"F 1"` raise `UsageError`.
- **The polar parts' names:** `m0.vel.mag`, `m0.vel.angle`,
  `m0.vel.angle_deg`, `m0.pos.mag` and `F1.angle`.
- **The arithmetic,** as components: `F1 + F2`, `F1 - F2`, `-F1`,
  `2 * F1`, `F1 * m` and `m * F1`. A `Vector` and a `Vec` mix:
  `(F1 + F2) + F3` and `F3 + (F1 + F2)`. Each result is a `Vec`.
  `sum([F1, F2, F3]) == F1 + F2 + F3`.
- **`.eq`:** the two pairs of strings above.
- **Polar:** `d0.vel.from_polar()` and `d0.vel.to_polar()` as the four
  strings above.
- **Against the old copy,** renamed back, as strings:
  `*d0.vel.from_polar(), *d0.vel.to_polar()` is
  `magnitude_and_angle_equations`; `(F + n + w).eq(a * m)` is
  `newtons_second_law`; `R.eq(F1 + F2 + F3)` is
  `superposition_equations`. These use the old copy, so 007 deletes
  them with it.
- **Misuses raise `UsageError` at run time:** `.mag` of an `X` vector;
  `F1 + f`, `F1 - f` and `R.eq(f)` with `f` in `X`; `F1 + 1`; `1 + F1`;
  `F1 * F2`. Reach them through `getattr`, or with the operand cast to
  `Any`, so pyright doesn't see the misuse here.
- **`BookNotation`:** each new row through `text`, with and without the
  owner `P`. The test that other symbols print their names used
  `Var("F1", "", "x")` and `Var("m", "0", "pos", "mag")`, which now
  have rows. Use symbols that still don't, such as
  `Var("m", "01", "a", "mag")`.

**`tests/physics_misuse.py`:** add, each with its ignore:

```python
F1, R = Vector("F1", XY), Vector("R", XY)
f = Vector("f", X)
f.mag  # pyright: ignore[reportAttributeAccessIssue]
f.from_polar()  # pyright: ignore[reportAttributeAccessIssue]
_ = F1 + f  # pyright: ignore[reportOperatorIssue]
R.eq(f)  # pyright: ignore[reportArgumentType]
```

- **`F1 + f` is assigned to `_`.** A bare `F1 + f` also gets
  `reportUnusedExpression`, as a warning.
- **Check once that it bites.** Add an ignore to a correct line, such
  as `F1.mag`, and see `uv run pyright` fail. Then take it out.

**`tests/test_examples.py`:** the `Formula` tests take expressions.

- `Formula(double, x, 2 * sp.sin(a) * sp.cos(a))` matches verbatim, and
  `Formula(double, x, sp.sin(2 * a))` as an equivalent form.
- The tests of a different formula, several roots, no roots, and a
  symbol not in the formula keep their meaning, with expressions.
- **Misuses raise `UsageError`:** a known that isn't a want; a symbol
  that isn't the solution's (`b`); a string and a relation (`a > 0`),
  each cast to `Any` so pyright doesn't see them. The parse errors and
  "a SymPy function it doesn't know" cases go with the parsing.

**`tests/slow_examples.py`:** no change. 3.9 and 3.10 stay. Report
their import times.

## Docs

- **`src/equarium/physics/__init__.py`'s docstring,** as above.
- **`examples/answers.py`'s docstrings,** as above.
- **The package `README.md`** doesn't change: "Most of them run on
  equarium's physics layer" stays true.
- **The series [README](../README.md):** mark 002 done in its
  increments table, and update its status line and the "1 of 7 done".
  Leave the commit cell and this page's status line for the manager.
- **The [series map](../../README.md):** 004's status says 2 of 7
  increments are done.
- **Don't edit** `spec.md`, `charter.md` or this page. If something
  here is wrong, say so in the report.

## Check and commit

- **`uv run pytest`** passes: the 294 fast tests, plus yours. Report
  how long `tests/test_examples.py` takes.
- **`uv run pytest -m slow`** passes its 8 tests. 3.9's rows and 3.10's
  show-that now go through `old_name`. It takes several minutes, so run
  it in the background.
- **`uv run pyright`:** 0 errors and 0 warnings, over `src`, `tests`
  and `examples`, `tests/physics_misuse.py` included.
- **Every changed module** runs with
  `uv run python -m examples.up_15e.ch03.examples.n06.main` and so on.
- **No old names left:**
  `grep -rn "kinematics_states\|newtons_laws\|make_point\|Point3" examples`
  finds nothing, and neither does
  `grep -n "parse_expr\|tokenize" examples/answers.py`.
- **No files outside the repo.** Keep scratch output in your own
  scratch folder.
- **One commit on the branch `2026-11-08-physics-redesign`,** with the
  code, tests and docs, in the style of `git log`: a subject line, then
  a wrapped paragraph saying what and why. Don't push.

## Report

When done, say in a few lines:

- the commit, the number of tests, fast and slow, how long
  `tests/test_examples.py` takes, and 3.9's and 3.10's import times;
- that no formula moved, or, if one did, the row and what came out
  (you stopped there);
- any name you chose differently from this page, and why;
- what pyright needed beyond the `cast`s this page names;
- anything in the spec or this checkpoint that was wrong or unclear,
  and what you did instead.

Then stop. Increment 003, polar and degrees, is a separate checkpoint.
