# physics 001: symbols and chapter 2

**Status:** Done at `6bf4296` and reviewed (2026-11-08).

If you've been told to read this file, this is the whole assignment.
Build it, check it, commit it, report, and stop.

## Goal

The first increment of the new physics layer, and chapter 2 moved onto
it. Only names change: every equation is the same, in the same order.
That means:

- **New modules** in `src/equarium/physics/`:
  - `symbols.py`, `Var`;
  - `axes.py`, `X`, `Y` and `XY`;
  - `vectors.py`, `Vector` with its components only;
  - `particles.py`, `Particle`, `State` and `Edge`;
  - `kinematics.py`, the kinematics equations;
  - `notation.py`, `BookNotation`;
  - and the re-exports in `__init__.py`.
- **Chapter 2's 12 modules** use the new layer, with the same
  equations in the same order. 2.8 follows 2.7.
- **The old formulas, renamed back.** `tests/test_old_outputs.py`
  renames the new symbols back to the old names, and all 66 rows come
  out verbatim, with their numbers.
- **`tests/test_physics.py`,** rewritten for the new layer.
- **`tests/physics_misuse.py`,** a file of misuses that pyright must
  flag.
- **2.4 and 2.5** print the book's notation in `__main__`, after the
  names.

The old copy, `kinematics_states.py` and `newtons_laws.py`, stays.
Chapters 3 and 4 still use it. Stop when the checks pass and the commit
is in.

**Not in this increment:** `Vec`, vector arithmetic, `.eq`, lone
vectors, the polar parts and `polar.py`, and `Formula` taking an
expression (002); degrees (003); `Event` (004); the projectile setup
(005); `mass` and Newton (006). `examples/answers.py` doesn't change.

## Read first

- **[The spec](../spec.md).** Read all of "Decisions", since the
  later increments' decisions shape this one's types. Then "### 001
  symbols and chapter 2", "How each increment lands" and "SymPy to
  watch".
- **[The charter](../charter.md):** "What the old physics code
  taught", "What the prototype showed" and "The user's preferences".
- **[002's checkpoint 007](../../002-core/checkpoints/007-physics-code-and-chapter-2.md),**
  for how chapter 2's ports were written, and which of their zeros are
  equations and which are values.
- **The core's display hook:** `src/equarium/display.py` (`SymbolHook`,
  `terminal`, `GREEN`, `RED`, `RESET`, `render`, `render_solution`),
  `Role` in `analysis.py`, and `UsageError` in `errors.py`.
  `display.py` also shows the `TYPE_CHECKING` import that breaks an
  import cycle.
- **The old copy,** `src/equarium/physics/kinematics_states.py`. Its
  `make_states_model` names and `kinematics_fundamental`'s order are
  what this increment must reproduce.
- **Chapter 2's modules,** under `examples/up_15e/ch02/` (listed in
  "The examples" below), and `tests/test_old_outputs.py`,
  `tests/test_physics.py` and `tests/slow_examples.py`.
- **The prototype,** outside the repo, in
  `~/.config/Claude/side-session-notes/local_9ac850c1-eb15-42fc-bbb0-61739b724d16/004-spec-prototype/`.
  `layer.py` is the whole layer in one file. `sketches.py` has an
  `old_name` and 2.4 and 2.5 on the layer. `rename_all.py` is the
  rename-back check over all 66 rows. `misuse.py` is the misuse-file
  trick. They're data to reuse, not the source: the spec and this page
  win. Where the prototype differs:
  - it raises `ValueError`, where the spec says `UsageError`;
  - its `Vector` takes `(owner, where, quantity, axes)`. This page
    orders the fields so that 002's `Vector("F1", XY)` works;
  - its `x` and `y` don't check the axes at run time;
  - its `Book` prints `v_av`, has a `unicode` flag, and calls
    `display.terminal` on a new symbol. The spec's `BookNotation`
    glues `vav`, always prints `Δt`, and has `owners`, `edge_index`
    and `color`;
  - it has `polar`, `Event`, `projectile`, `newton` and `mass`, which
    are later increments.

## Starting point

The branch `2026-11-08-physics-redesign`, at the commit that adds this
checkpoint, on top of `3b85912` (the charter and the spec). Check it
with `git branch --show-current`. If you're on another branch, stop and
ask. Don't switch branches, stash or reset.

`uv run pytest` passes 263 tests and deselects 8 slow ones, in about
33 s. `uv run pytest -m slow` passes those 8. `uv run pyright` reports
0 errors and 0 warnings.

What the prototype showed for this increment:

- **The rename is safe.** With the old physics code made to produce
  the new symbols, every port ran unchanged. All 66 rows, renamed
  back, came out verbatim. No formula moved.
- **The same equations.** Renamed back, the prototype's kinematics
  equations are the old copy's, as strings, for a two-state `Y`
  particle, a three-state `XY` particle and a four-state `X` particle
  (checked while writing this page).
- **2.4** gives 43, 23 and 55.
- **Pyright sees the dimension.** It flags `.y` in an `X` model and
  `.x` in a `Y` model, as `reportAttributeAccessIssue`. With
  `reportUnnecessaryTypeIgnoreComment` on, an ignore on a correct line
  fails the run (checked while writing this page).
- **The book's notation.** A scratch hook that follows the spec's
  table prints 2.4 (a) and 2.5 as shown under "2.4 and 2.5 in the
  book's notation" below.

## Build

### `symbols.py`: `Var`

The charter's excerpt, without `owner_key`:

```python
class Var(sp.Symbol):
    owner: str
    where: str
    path: tuple[str, ...]

    def __new__(cls, owner: str, where: str, *path: str) -> Self:
        obj = sp.Symbol.__xnew__(cls, ".".join((owner + where, *path)))  # no name cache
        obj.owner, obj.where, obj.path = owner, where, path
        return obj

    def _hashable_content(self) -> tuple[str, ...]:
        return (self.name, self.owner, self.where, *self.path)

    def __reduce_ex__(self, protocol: SupportsIndex) -> tuple[Any, ...]:
        return (type(self), (self.owner, self.where, *self.path))
```

- **The name is the access path:** `owner + where`, then the path,
  joined by dots. `Var("m", "0", "pos", "x")` is `m0.pos.x`, and
  `Var("m", "01", "a", "x")` is `m01.a.x`.
- **The identity is the structure.** `_hashable_content` holds strings
  only, in fixed positions, because SymPy compares it element by
  element to sort terms.
- **No SymPy assumptions.** Never build a `Var` through
  `sp.Symbol(name)`.
- **`Var` checks nothing.** The owners check their names.

### `axes.py`

```python
class Axes:
    names: ClassVar[tuple[str, ...]]

class X(Axes):
    names = ("x",)

class Y(Axes):
    names = ("y",)

class XY(Axes):
    names = ("x", "y")
```

An axes type is passed as the class: `Particle("m", 2, X)`. There is no
`Z`.

### `vectors.py`: `Vector`, components only

- **`Vector[A: Axes]`,** a frozen dataclass. Its fields, in this order:
  `owner: str`, `axes: type[A]`, `where: str = ""` and
  `quantity: tuple[str, ...] = ()`. A state's position is
  `Vector("m", X, "0", ("pos",))`. The order leaves room for 002's lone
  vector, `Vector("F1", XY)`, which isn't in this increment.
- **A component** is `Var(owner, where, *quantity, axis)`: `m0.pos.x`,
  `m01.a.x`.
- **`x` and `y`** are properties whose `self` is annotated. `x` takes
  `self: Vector[X] | Vector[XY]`, and `y` takes
  `self: Vector[Y] | Vector[XY]`. So pyright flags `m0.pos.y` in an `X`
  model.
- **At run time the same misuse raises `UsageError`,** naming the
  vector and its axes, so a script that skips pyright fails the same
  way.
- **`components`:** one `Var` per axis, in the axes' order. The
  kinematics iterates over it.

Nothing else: no arithmetic, no `.eq`, no polar parts.

### `particles.py`: `Particle`, `State`, `Edge`

All three are frozen dataclasses, generic in the axes, and equal by
value. They hold names, never symbols: states, edges, vectors and
symbols are made on demand.

- **`State[A]`:** fields `owner: str`, `index: int` and
  `axes: type[A]`. `pos` and `vel` are vectors, with `where` the index
  (`"0"`). `t` is `Var(owner, "0", "t")`.
- **`Edge[A]`:** fields `start: State[A]` and `end: State[A]`. Its
  `where` is the two indexes, `"01"`, and its `axes` are its states'.
  `dt` is `Var(owner, "01", "dt")`, and `a` and `v_av` are vectors.
- **`Particle[A]`:** `Particle(name, states, axes)`. Its `__init__` is
  its own (`init=False`, then `object.__setattr__`), as `Answer` does
  in `examples/answers.py`, since `states` is also the property. Its
  fields are `name`, `count` and `axes`.
  - **The name** is a Python identifier that doesn't end in a digit,
    since `p2` with state 0 would print `p20.t`. Otherwise
    `UsageError`.
  - **Two to ten states.** Otherwise `UsageError`.
  - **`states`:** a tuple of `State`, so `m0, m1 = m.states`.
  - **`edges`:** a tuple of `Edge`, one between each pair of
    consecutive states.
  - **`edge(i, j)`:** the edge from state `i` to state `j`. `j` must be
    `i + 1`, and both must be states of the particle. Otherwise
    `UsageError`.
  - **`kinematics()`:** one line, a call into `kinematics.py`.
- **Equal particles give equal symbols.** `Particle("m", 2, X)` made
  twice is the same particle, with the same states, edges and symbols.
- **No `mass`** yet (006).

### `kinematics.py`

- **A plain function** that `Particle.kinematics()` calls. It takes
  the particle, or its edges, as you prefer. Import `Particle` or
  `Edge` under `TYPE_CHECKING`, as `display.py` imports `Solution`, so
  the two modules don't import each other at run time.
- **The order is the old one:** every edge's Δt, then 2.2 for each
  edge and axis, then 2.7, then 2.10. That's the old
  `kinematics_fundamental` with every flag on. So the automatic labels
  stay as they were.
- **No options.** Every old call included v_av, Δt and all three
  equations.
- **Typing.** SymPy types `sp.Eq(...)` as a union, so narrow it as the
  old copy does, with `cast`.
- **`Particle("m", 2, X).kinematics()`,** as strings:

  ```
  Eq(m01.dt, -m0.t + m1.t)
  Eq(m01.v_av.x, (-m0.pos.x + m1.pos.x)/m01.dt)
  Eq(m01.a.x, (-m0.vel.x + m1.vel.x)/m01.dt)
  Eq(m01.v_av.x, m0.vel.x/2 + m1.vel.x/2)
  ```

- **`Particle("p", 3, X).kinematics()`,** in the old order:

  ```
  Eq(p01.dt, -p0.t + p1.t)
  Eq(p12.dt, -p1.t + p2.t)
  Eq(p01.v_av.x, (-p0.pos.x + p1.pos.x)/p01.dt)
  Eq(p12.v_av.x, (-p1.pos.x + p2.pos.x)/p12.dt)
  Eq(p01.a.x, (-p0.vel.x + p1.vel.x)/p01.dt)
  Eq(p12.a.x, (-p1.vel.x + p2.vel.x)/p12.dt)
  Eq(p01.v_av.x, p0.vel.x/2 + p1.vel.x/2)
  Eq(p12.v_av.x, p1.vel.x/2 + p2.vel.x/2)
  ```

### `notation.py`: `BookNotation`

- **A frozen dataclass that is a display hook,** `(symbol, role) -> str`.
  It prints the book's notation as plain text, glued, as the book's
  text reads.
- **Fields:**
  - `owners: Mapping[str, str]`, empty by default: an owner's name to
    the book's subscript, such as `{"m": "M", "p": "P"}`. An owner not
    in it gets none.
  - `edge_index: bool = False`: print an edge's states, for problems
    with several edges.
  - `color: bool = True`.
- **`text(symbol)`** is the book's form, without color.
  **`__call__(symbol, role)`** colors it as `display.terminal` does:
  knowns green, wants red, other unknowns plain, with the core's
  `GREEN`, `RED` and `RESET`. With `color=False`, it's `text` alone.
- **The order is the book's:** letter, owner, state, axis.
- **This increment's rows** of the spec's table:

  | Symbol | Book | With owner `P` | With `edge_index` |
  |---|---|---|---|
  | `m0.pos.x`, `m0.pos.y` | `x0`, `y0` | `xP0` | |
  | `m0.vel.x` | `v0x` | `vP0x` | |
  | `m0.t` | `t0` | `tP0` | |
  | `m01.dt` | `Δt` | `ΔtP` | `Δt01`, `ΔtP01` |
  | `m01.a.x` | `ax` | `aPx` | `a01x`, `aP01x` |
  | `m01.v_av.x` | `vavx` | `vavPx` | `vav01x`, `vavP01x` |
  | a plain symbol | its name | | |

- **Any other `Var` prints its name.** The spec's other rows come with
  their symbols in later increments: the polar parts, degrees, lone
  vectors, events and the mass.
- **The book's form is for reading.** It can be ambiguous: two owners
  without subscripts both print `x0`. Tests compare names, except the
  notation's own tests.

### `__init__.py`

- **Re-exports,** with `__all__`: `Var`, `X`, `Y`, `XY`, `Vector`,
  `Particle`, `State`, `Edge` and `BookNotation`.
- **The docstring** says what the layer is, and that the old copy,
  `kinematics_states` and `newtons_laws`, stays until increment 007
  for chapters 3 and 4.
- **Layers.** The new modules import the core (`UsageError`, the
  display's colors, `Role`), never the old copy. The core imports
  nothing from `equarium.physics`.

### The examples

The 12 modules, and 2.8:

| Module, under `examples/up_15e/ch02/` | Owners | Notes |
|---|---|---|
| `examples/n04/main.py` | `m`, `X` | `e01` becomes `m01`. Book form in `__main__`. |
| `examples/n05/main.py` | `m`, `p`, `X` | Book form in `__main__`, with owners `M` and `P`. |
| `examples/n05/main_step_by_step.py` | `m`, `p`, `X` | The six eliminations name the new symbols. Names only in `__main__`. |
| `examples/n06/main.py` | `c`, `Y` | |
| `examples/n07/main.py` | `b`, `Y` | |
| `examples/n08/main.py` | none | Imports `b1` and `ball` from 2.7. Only its comments change. |
| `exercises/n001/main.py` | `c`, `X` | Its assert goes. |
| `exercises/n003/main.py` | `ca`, `cb`, `X` | Its assert goes. |
| `exercises/n003/main_two_steps.py` | `ca`, `cb`, `X` | Its assert goes. |
| `exercises/n005/main.py` | `p`, 3 states, `X` | `p.edge(0, 1)` and `p.edge(1, 2)`. |
| `exercises/n019/main.py` | `o`, `X` | |
| `exercises/n021/main.py` | `b`, `X` | Its assert goes. |
| `exercises/n023/main.py` | `b`, `X` | |

**How each one changes:**

- `make_states_model("m", 2, …)` becomes `Particle("m", 2, X)`. The
  axes are the old `kinematics_fundamental` call's: `Y` for 2.6 and
  2.7, `X` for the rest.
- `m.edges[0]` becomes `m.edge(0, 1)`, and `m.edges[1]` becomes
  `m.edge(1, 2)`.
- `kinematics_fundamental(m, axes=…, …)` becomes `m.kinematics()`.
- **The four `assert … v_av is not None` go,** in 2.1, 2.3 (both) and
  2.21. Nothing is optional any more.
- **Everything else stays:** the same `add`s, knowns, wants,
  eliminations and solves, in the same order, and the same `BOOK`.
- **Symbols a module makes itself stay plain,** with their names:
  2.5's `m_v`, `dist` and `t_01` (events are 004), and Exercise 2.5's
  `dx_p_0_1`, `dx_p_1_2`, `avg_speed_02` and `avg_vel_02`.
- **Comments and docstrings use the new names.** A comment that quotes
  a formula quotes it as the module prints it now, such as 2.4's
  `# m1.pos.x = m0.pos.x + m0.vel.x*m1.t + m01.a.x*m1.t**2/2   43`.
  That includes 2.5 step by step's list of the eight equations left,
  as `linked.show()` prints them, and docstrings such as 2.1's "the
  formula keeps `c_0_t` and `c_0_x`".
- **The "Ported from" lines and the run commands stay.**

### 2.4 and 2.5 in the book's notation

- **After the displays they print now,** 2.4's and 2.5's `__main__`
  print the same displays again in the book's notation. `System.show()`
  and `Solution.show()` take no hook, so use
  `print(render(part_a, symbol=book))` and
  `print(render_solution(sol_a, symbol=book))`, from `equarium.display`.
  A short heading line before them is fine.
- **2.4** uses `BookNotation()`. **2.5's `main.py`** uses
  `BookNotation(owners={"m": "M", "p": "P"})`, the book's subscripts.
  2.5 step by step and the other modules print names only.
- **What the scratch hook printed,** without color. 2.4 (a):

  ```
  x1 = x0 + v0x*t1 + ax*t1**2/2
  x1 = 43.0
  v1x = v0x + ax*t1
  v1x = 23.0
  ```

  2.5:

  ```
  t_01 = 2*m_v/aPx
  t_01 = 10.0
  vP1x = 2*m_v
  vP1x = 30.0
  dist = 2*m_v**2/aPx
  dist = 150.0
  ```

### If a formula moves

Every chapter 2 row of `tests/test_old_outputs.py`, renamed back, must
come out verbatim. The prototype found none that moved. If one does,
stop. Don't change the row, the module's equations, or the order of
anything to make it pass. Report the row, what came out, and what you
think moved it. The same holds for a `BOOK` that stops matching.

### Tests

**`tests/old_names.py`, new.** A helper module, as `slow_examples.py`
is, so both test files below can use it.

- **`old_name(symbol) -> str`** renames a symbol back by the old rule:
  - a plain symbol keeps its name;
  - a state's `Var`: `m0.pos.x` → `m_0_x`, `m0.vel.x` → `m_0_v_x`,
    `m0.t` → `m_0_t`;
  - an edge's: `m01.dt` → `dt_m_0_1`, `m01.a.x` → `a_x_m_0_1`,
    `m01.v_av.x` → `v_av_x_m_0_1`;
  - any other `Var` raises, so a symbol the rule misses is loud.
- **A second function** gives `str()` of an expression with every `Var`
  replaced, through `xreplace`, by `sp.Symbol(old_name(var))`. With
  plain symbols, SymPy prints the old order again.
- **The spec's per-module map** (`meet.t` → `t_01`, `b.mass` → `m`) and
  the lone vectors' rule (`F1.x` → `F1_x`) come with the symbols that
  need them, in 002, 004 and 006. Chapter 2 has none.

**`tests/test_old_outputs.py`:**

- The want is found by its old name: `old_name(w) == want`.
- Each root's formula is compared renamed back.
- `OLD_GIVENS`' lookup goes through `old_name` too.
- **The rows don't change,** not by one character: the 66 rows of
  `OLD`, `R_MAG_4_1`, `R_ANGLE_4_1`, `OLD_3_10` and the count.
- The module docstring says, in a sentence, that the new symbols are
  renamed back.
- **Tests of `old_name`:** each of the six rules, a plain symbol, and a
  `Var` the rule doesn't know.

**`tests/test_physics.py`, rewritten:**

- **`Var`'s identity:**
  - `Particle("m", 2, X)` made twice gives equal particles, states,
    edges and symbols, with equal hashes;
  - `Var("m", "0", "pos", "x") == m0.pos.x`;
  - `sp.Symbol("m0.pos.x") != m0.pos.x`;
  - `Var("m0", "", "pos", "x")` prints `m0.pos.x`, but differs from
    `m0.pos.x`;
  - pickling round-trips a `Var`, still a `Var` with the same fields,
    and an equation of them.
- **Names:** `m0.pos.x`, `m0.vel.y`, `m1.t`, `m01.dt`, `m01.a.x`,
  `m01.v_av.x`, and a three-state particle's `p12.dt`.
- **Misuses raise `UsageError`:**
  - the names `"p2"`, `"m.x"`, `""` and `"2m"`;
  - 1 state and 11 states;
  - `edge(0, 2)`, and `edge(1, 2)` on two states;
  - at run time, `.y` of an `X` vector and `.x` of a `Y` vector.
    Reach them through `getattr`, so pyright doesn't see them here.
- **The kinematics:**
  - `Particle("m", 2, X).kinematics()` and `Particle("p", 3, X).kinematics()`
    as the strings above;
  - renamed back, a two-state `Y` particle's and a three-state `XY`
    particle's equations are the old copy's
    `kinematics_fundamental(make_states_model("m", n), axes=…)`, as
    strings. This test uses the old copy, so 007 deletes it with the
    copy.
- **`BookNotation`:**
  - each row of the table above, through `text`;
  - a plain symbol and an unknown `Var` print their names;
  - `__call__` colors by role, and `color=False` never colors;
  - 2.4 (a): `render_solution(sol_a, symbol=BookNotation(color=False))`,
    with 2.4's `sol_a`, starts with `x1 = x0 + v0x*t1 + ax*t1**2/2`;
  - 2.5: with owners `M` and `P`, `p01.a.x` prints `aPx` and
    `p1.vel.x` prints `vP1x`.
- **Keep** `test_the_core_doesnt_import_the_physics_code` as it is.
- **Keep** `test_the_same_equations_as_the_old_library`, the old
  copy's test, until 007.

**`tests/physics_misuse.py`, new.** pyright checks it. pytest doesn't
collect it, and nothing imports it.

- Its first line is `# pyright: reportUnnecessaryTypeIgnoreComment=true`.
- Its docstring says that each marked line is a misuse pyright must
  flag. The ignore comments keep the run clean, and an ignore that
  isn't needed fails `uv run pyright`. Later increments add their
  misuses.
- **This increment's misuses,** each with
  `# pyright: ignore[reportAttributeAccessIssue]`: `.y` of an `X`
  state's position and of an `X` edge's acceleration, and `.x` of a `Y`
  state's velocity.
- **Check once that it bites.** Add the same ignore to a correct line,
  such as `m0.pos.x`, and see `uv run pyright` fail. Then take it out.

**`tests/test_examples.py`:** no change. The module names and the
`BOOK`s are the same.

## Docs

- **`src/equarium/physics/__init__.py`'s docstring,** as above.
- **The package `README.md`.** Its sentence "Most of them run on the
  old physics code, which equarium carries as `equarium.physics`, such
  as Example 2.4's" is no longer true of 2.4. Make it say that most of
  them run on equarium's physics layer, `equarium.physics`. Keep 2.4's
  run command.
- **The series [README](../README.md):** mark 001 done in its
  increments table, and update its status line and the "0 of 7 done".
  Leave the commit cell and this page's status line for the manager.
- **The [series map](../../README.md):** 004's status says 1 of 7
  increments is done.
- **Don't edit** `spec.md`, `charter.md` or this page. If something
  here is wrong, say so in the report.

## Check and commit

- **`uv run pytest`** passes: the 263 fast tests, plus yours. Report
  how long `tests/test_examples.py` takes.
- **`uv run pytest -m slow`** passes its 8 tests. 3.9's rows now go
  through `old_name`. It takes several minutes, so run it in the
  background.
- **`uv run pyright`:** 0 errors and 0 warnings, over `src`, `tests`
  and `examples`, `tests/physics_misuse.py` included.
- **Every changed module** runs with
  `uv run python -m examples.up_15e.ch02.<…>`, and 2.4 and 2.5 print
  the book's form.
- **No old names left.** `grep -rn "make_states_model\|kinematics_fundamental" examples/up_15e/ch02`
  finds nothing.
- **No files outside the repo.** Keep scratch output in your own
  scratch folder.
- **One commit on the branch `2026-11-08-physics-redesign`,** with the
  code, tests and docs, in the style of `git log`: a subject line, then
  a wrapped paragraph saying what and why. Don't push.

## Report

When done, say in a few lines:

- the commit, the number of tests, fast and slow, and how long
  `tests/test_examples.py` takes;
- that no formula moved, or, if one did, the row and what came out
  (you stopped there);
- any name you chose differently from this page, such as `components`
  or `count`, and why;
- what pyright needed beyond the `cast`s this page names;
- anything in the spec or this checkpoint that was wrong or unclear,
  and what you did instead.

Then stop. Increment 002, chapters 3 and 4 renamed, is a separate
checkpoint.
