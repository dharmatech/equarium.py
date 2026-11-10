# physics 006: Newton on the edge

**Status:** Done at `2572faf` and reviewed (2026-11-09).

If you've been told to read this file, this is the whole assignment.
Build it, check it, commit it, report, and stop.

## Goal

The fourth reshape, and the last. Three modules write Newton's second
law by hand, with a mass and an acceleration of their own, and a helper
takes its place. That means:

- **`newton.py`, with Newton's second law on an edge.**
  `b01.newton(n, w, f)` returns ΣF = m a, one equation per axis of the
  edge: `f.x + n.x + w.x = b.mass*b01.a.x`. The acceleration is the
  edge's, the one the kinematics equations have.
- **`Particle.mass`:** `b.mass`, a `Var` with an empty `where`.
- **4.4 uses it.** The box is a particle, `Particle("box", 2, XY)`, with
  `box01.newton(F, n, w)`. Its own `m` and `a` go.
- **4.5 uses it, in both versions.** The forces move to `X`, as the
  bottle is, with `b01.newton(n, w, f)`. Its own `m` and `a` go, and so
  do the y equation and the link `a.x = b01.a.x`. In two steps, step 2
  knows `b01.a.x` from step 1.
- **`notation.py` gains the row for the mass:** `b.mass` prints `m`.
- **The old formulas, still renamed back.** `SCRIPT_NAMES` gains three
  names: 4.4's `box.mass` → `m` and `box01.a.x` → `a_x`, and 4.5's
  `b.mass` → `m`.

**No row's formula changes.** All 66 rows of
`tests/test_old_outputs.py` come out verbatim, renamed back, with their
numbers. Two of them need the three new names. So `RESHAPED` keeps its
five entries, and its guard's count stays 5. One formula that isn't a
row changes its names, step 2 of 4.5 in two steps, and a new test pins
it. All of it is listed next. The scratch run compared every `System`
and `Solution` of the three modules, not only the rows.

**Not in this increment:**

- **Deleting the old copy** (007). `tests/test_physics.py` still imports
  it, to compare.
- **4.1.** Its superposition stays `R.eq(F1 + F2 + F3)`, with no helper
  of its own, as the spec says.
- **4.7 and 3.13.** They stay written out. There are no helpers for
  weight and relative velocity.
- **Kinematics for 4.4.** The old script had none. The box has two
  states only so that it has an edge.
- **A mass on a state or an edge.** The mass is the particle's.
- **Options.** `newton(*forces)` takes forces and nothing else.
- **The book form in 4.4's and 4.5's `__main__`.** Only 2.4 and 2.5
  print it.
- **Labels for the helper's equations.**
- **A `SCRIPT_NAMES` entry for 4.5 in two steps.** Its one row is step
  1's, which has no mass.
- **`RESHAPED` and its guard.** They don't change.
- **Pyright doesn't flag `b01.newton()`,** with no forces. It raises at
  run time only.

## The formulas that change

Each formula here is as `str()` prints it. The scratch run made every
one, on a copy of the repo at `b4585f5`.

**No row's formula changes, only names.** The old scripts made a mass,
`m`, and an acceleration, `a`, of their own. Now the mass is the
particle's and the acceleration is the edge's. So each formula below is
today's with `b.mass` in place of `m`, or `box.mass` in 4.4, and, in
4.5's step 2, the edge's acceleration in place of the lone `a.x`.
Checked with SymPy for all four solutions of the three modules:
`old.xreplace(...)` of those names equals the new formula, and prints
the same, character for character. Every number is the same.

### Two rows that come back through new names

Both rows stay as they are, formula and number. They pass through
three new names in `SCRIPT_NAMES`, and need nothing else.

**4.4's row.** Module `ch04.examples.n04.main`, solution `sol`, want
`a_x`. Number 0.500000000000000.

```
row    (F_x + n_x + w_x)/m           in the old names
today  (F.x + n.x + w.x)/m           the want is a.x, a lone vector's
new    (F.x + n.x + w.x)/box.mass    the want is box01.a.x, the edge's
       (F_x + n_x + w_x)/m           the same, renamed back: the row
```

- **`box.mass` → `m`.** The old script made `m` itself.
- **`box01.a.x` → `a_x`.** The old script made its own `a`, whose x was
  `a_x`. The edge's rule would say `a_x_box_0_1`, and the row's want is
  `a_x`. So the map names it, and wins over the rule, as it does for
  3.7's `b0.vel.mag`.

**4.5's row.** Module `ch04.examples.n05.main`, solution `sol`, want
`f_x`, which is `f.x`. Number -0.900000000000000.

```
row    (b_0_v_x**2*m/2 - b_0_x*n_x - b_0_x*w_x - b_1_v_x**2*m/2 + b_1_x*n_x + b_1_x*w_x)/(b_0_x - b_1_x)
today  (m*b0.vel.x**2/2 - m*b1.vel.x**2/2 - b0.pos.x*n.x - b0.pos.x*w.x + b1.pos.x*n.x + b1.pos.x*w.x)/(b0.pos.x - b1.pos.x)
new    (b.mass*b0.vel.x**2/2 - b.mass*b1.vel.x**2/2 - b0.pos.x*n.x - b0.pos.x*w.x + b1.pos.x*n.x + b1.pos.x*w.x)/(b0.pos.x - b1.pos.x)
       renamed back with b.mass → m: the row, verbatim
```

This is the spec's check: 4.5's f_x is the old formula, renamed back
with `b.mass` → `m`. The link equation and the y equation are gone, and
the formula doesn't notice.

**Without the three names, exactly these two rows fail,** and the other
64 pass. 4.4's fails because no want is named `a_x`. 4.5's fails with
`no old name for b.mass`.

### One formula that isn't a row: step 2 of 4.5 in two steps

Module `ch04.examples.n05.main_two_steps`, solution `sol_2`, want
`f.x`. Number -0.900000000000000.

```
today  m*a.x - n.x - w.x              a.x is step 2's own, a lone vector's
new    b.mass*b01.a.x - n.x - w.x     b01.a.x is the edge's, step 1's want
```

- **It has no row.** The old script never solved its step 2: it ends at
  a display. The catalog's scratch try gave `f_x = a_x*m - n_x - w_x`,
  which is today's formula.
- **It's the same formula, with the edge's acceleration.** Renamed with
  `b.mass` → `m` and `b01.a.x` → `a_x`, it prints `a_x*m - n_x - w_x`.
- **A map can't do that renaming for the module.** In it, `b01.a.x` is
  also step 1's want, whose row names it `a_x_b_0_1`. One symbol in both
  steps is the point of the reshape.
- **A new test pins it,**
  `test_4_5_step_2_has_the_edges_acceleration`, under "Tests" below.
  The `BOOK` already checks its number.

### The 64 other rows

- **4.5 in two steps' one row, step 1's:** want `a_x_b_0_1`,
  `(b_0_v_x - b_1_v_x)*(b_0_v_x + b_1_v_x)/(2*(b_0_x - b_1_x))`,
  -2.00000000000000. Step 1 is kinematics only, and doesn't change.
- **The other 63 rows,** of modules this increment doesn't touch.
- **3.10's show-that,** `OLD_3_10`, doesn't change.

### The equations that change

The systems, as `show()` prints them, renamed back in the same way.

- **4.4:** (1) and (2) are the same two equations, with
  `box.mass*box01.a.x` and `box.mass*box01.a.y` where they had `m*a.x`
  and `m*a.y`. The known `a.y = 0` is `box01.a.y = 0`. The system is
  named `push`, since the particle takes the name `box`.
- **4.5:** five equations, where it had seven.
  - (1) to (4), the kinematics, are the same.
  - (5) is `f.x + n.x + w.x = b.mass*b01.a.x`. It was
    `f.x + n.x + w.x = m*a.x`.
  - (6), `f.y + n.y + w.y = m*a.y`, is gone: the forces are in `X`. No
    want needed it: `f.y`, `n.y`, `w.y` and `a.y` were unknown, and in
    no other equation.
  - (7), `a.x = b01.a.x`, is gone: there is one acceleration.
- **4.5 in two steps:** `slide` and `sol_1` are the same. `push` has one
  equation, (1), `f.x + n.x + w.x = b.mass*b01.a.x`, where it had two.
  Its known `a.x = -2.0` is `b01.a.x = -2.0`.
- **The knowns keep their order and their values** in all three
  modules.

### The `BOOK`s

- **4.4:** `Answer(sol, a.x, "0.50")` becomes
  `Answer(sol, box01.a.x, "0.50")`. The symbol is renamed, and the
  printed value isn't touched.
- **4.5, both versions:** not one character changes. `f.x` and
  `b01.a.x` are the same symbols as today.
- **Every other `BOOK`** is in a module this increment doesn't touch.

## Read first

- **[The spec](../spec.md).** In "Decisions": "Particles, states and
  edges" (the mass), "Newton's laws", "Book notation" (the table's
  `b.mass` row), "The examples" and "The tests". The 4.5 sketch. Then
  "### 006 Newton on the edge", "How each increment lands" and "SymPy
  to watch".
- **The series [README](../README.md),** its "What's next" and the two
  notes in the review of 002: pyright types `m * F1` as an `Expr`, so
  `newton` builds the product itself, and the mass has an empty
  `where`, so its row in `BookNotation` goes before the lone vector's.
- **[Checkpoint 005](005-projectile-setup.md),** for the form, and for
  `Edge.projectile`, which this page follows: a method that calls a
  plain function in a module of its own. Also
  [checkpoint 004](004-events.md), for the first symbols with an empty
  `where` that aren't a lone vector's, and for `SCRIPT_NAMES`.
- **The code:** `src/equarium/physics/particles.py` (`Edge` and
  `Particle`), `projectile.py` (its `TYPE_CHECKING` import and its
  run-time check), `vectors.py` (the arithmetic, `_operand` and
  `_describe`), `notation.py` (the branch for an empty `where`) and
  `__init__.py`. Also `tests/old_names.py`, `tests/test_old_outputs.py`,
  `tests/test_physics.py` and `tests/physics_misuse.py`.
- **The three modules,** `examples/up_15e/ch04/examples/n04/main.py`,
  `n05/main.py` and `n05/main_two_steps.py`.
- **[The catalog](../../001-example-catalog/catalog.md),** "Example 4.4"
  and "Example 4.5": the old scripts' output, and step 2's scratch try.
- **The prototype,** outside the repo, in
  `~/.config/Claude/side-session-notes/local_9ac850c1-eb15-42fc-bbb0-61739b724d16/004-spec-prototype/`:
  `layer.py`'s `Edge.newton` and `Particle.mass`, `sketches.py`'s 4.5
  and `typing_check.py`'s `bad6`. It's data, not the source: the spec
  and this page win. Where it differs:
  - its `newton` builds the equations in the method. Here the method
    calls `newton.py` in one line;
  - it writes the mass's symbol twice, in `newton` and in
    `Particle.mass`. Here `mass_of` is the one place;
  - it has no run-time check. Here a force in other axes, a force that
    isn't a vector, and no forces at all raise `UsageError`;
  - it printed 4.5's formula with Newton on the edge, and never compared
    it with the old row. Here the row checks it, verbatim;
  - it ported neither 4.4 nor 4.5 in two steps.

## Starting point

The branch `2026-11-08-physics-redesign`, at the commit that adds this
checkpoint, on top of `b4585f5` (the review of 005). Check it with
`git branch --show-current`. If you're on another branch, stop and ask.
Don't switch branches, stash or reset.

`uv run pytest` passes 338 tests and deselects 3 slow ones, in about
44 s. `uv run pytest -m slow` passes those 3, in about 5 min.
`uv run pyright` reports 0 errors and 0 warnings.

Checked in scratch while writing this page, on a copy of the repo at
`b4585f5`, with `newton.py` built and the three modules ported as this
page says:

- **Every `System` and `Solution`** in the three modules, renamed back
  to the old names, was compared with the same at `b4585f5`: the
  equations with their labels, the knowns, the wants, and every
  solution's formulas and numbers. `box.mass` and `b.mass` were renamed
  back to `m`, and 4.4's `box01.a.x` and `box01.a.y` to `a_x` and
  `a_y`.
- **4.4:** nothing differs but the system's name. The two equations, the
  six knowns, the formula and 0.5 are the same.
- **4.5:** `sol` is the same: the formula, verbatim, and -0.9. `counter`
  differs as "The equations that change" says: (5) has the edge's
  acceleration, and (6) and (7) are gone. The eight knowns are the same.
- **4.5 in two steps:** `slide` and `sol_1` are the same. `push` has one
  equation, and its known acceleration is `b01.a.x`. `sol_2`'s formula
  has the edge's acceleration where it had the lone `a.x`, and is
  otherwise the same, with -0.9.
- **The fast suite,** with the three names and nine draft tests, passed
  all 347 tests in 48 s: the 66 rows, the show-that and every `BOOK`.
  The copy's 338 took 48 s before, on the same machine. Without the
  three names, exactly the two rows above fail.
  `tests/test_examples.py` takes 23.3 s, where it took 23.4 s.
- **The slow tests** passed, all 3, in 5 min 25 s. They are the three
  in `tests/test_strategies.py`, which imports none of the three
  modules.
- **Pyright** reported 0 errors over `src`, `tests` and `examples`, with
  no `cast` in `newton.py`. It flags `m01.newton(F1)`, an `XY` force on
  an `X` edge, and an `X` force on an `XY` edge (`reportArgumentType`:
  `Vector[XY]` isn't `Vector[X] | Vec[X]`, since `Vector` is invariant
  in `A`). An ignore on a correct call fails the run.
- **The book form** of 4.5's (5) prints `fx + nx + wx = m*ax`.
- **The times,** each module's import in a fresh process, after SymPy
  and equarium, three runs each:

  | Module | Now | With `newton` |
  |---|---|---|
  | 4.4 | 0.02 s | 0.02 s |
  | 4.5 | 0.23 to 0.24 s | 0.21 s |
  | 4.5 in two steps | 0.14 to 0.15 s | 0.14 s |

  None is near 5 s, so `SLOW_EXAMPLES` stays empty.

## Build

### `newton.py`: Newton's second law on an edge

A new module. Scratch used exactly this:

```python
def mass_of(owner: str) -> Var:
    """The mass of the particle named `owner`, `b.mass`."""
    return Var(owner, "", "mass")


def newton_equations[A: Axes](edge: Edge[A], forces: Sequence[Vector[A] | Vec[A]]) -> list[sp.Eq]:
    """`f.x + n.x + w.x = b.mass*b01.a.x`, for each axis of the edge: the
    forces' sum equals the particle's mass times the edge's acceleration."""
    name = edge.owner + edge.where
    call = f"{name}.newton({', '.join(describe(force) for force in forces)})"
    if not forces:
        raise UsageError(f"{call} needs one or more forces")
    for force in forces:
        if not isinstance(force, Vector | Vec):
            raise UsageError(f"{call}: {describe(force)} isn't a vector")
        if force.axes is not edge.axes:
            raise UsageError(
                f"{call}: {name} is in {edge.axes.__name__},"
                f" but {describe(force)} is in {force.axes.__name__}"
            )
    total = sum(forces[1:], start=forces[0])
    return total.eq(edge.a * mass_of(edge.owner))
```

- **The law is written once, as a vector equation,** ΣF = m a, and
  `.eq` expands it per axis, x first. So it covers the edge's axes,
  whatever they are, where the old code wrote x and y.
- **The product is built here,** `edge.a * mass`, with the vector first.
  Pyright types `mass * edge.a` as SymPy's `Expr`, as the review of 002
  notes. SymPy prints the product as `b.mass*b01.a.x` either way.
- **`mass_of` is the one place that makes the mass's symbol.** An edge
  holds its owner's name, not its particle, so `newton_equations` and
  `Particle.mass` both call it. The mass is the owner's, whatever its
  states and axes: `Particle("b", 2, X)` and `Particle("b", 3, XY)` have
  the same `b.mass`.
- **A force is a `Vector` or a `Vec`,** as `+` and `.eq` take both. The
  examples pass lone vectors. A vector expression, such as `-n`, works
  the same way, and costs nothing: the sum is the vectors' own `+`.
- **The sum starts from the first force,**
  `sum(forces[1:], start=forces[0])`, which pyright types as
  `Vec[A] | Vector[A]`. It types plain `sum(forces)` as
  `Vector[A] | Vec[A] | Literal[0]`, which has no `.eq`. SymPy sorts
  the terms, so the forces' order doesn't matter:
  `b01.newton(n, w, f) == b01.newton(f, w, n)`.
- **At run time,** each misuse raises `UsageError` before any equation
  is made. The messages read as `.eq`'s do, with the call first:

  | Misuse | Message |
  |---|---|
  | `m01.newton(f, F1)`, with `m01` in `X` and `F1` in `XY` | `m01.newton(f, F1): m01 is in X, but F1 is in XY` |
  | `d01.newton(f)`, with `d01` in `XY` and `f` in `X` | `d01.newton(f): d01 is in XY, but f is in X` |
  | `m01.newton(-F1)`, a `Vec` in `XY` | `m01.newton((-F1.x, -F1.y)): m01 is in X, but (-F1.x, -F1.y) is in XY` |
  | `m01.newton(f, f.x)`, a component | `m01.newton(f, f.x): f.x isn't a vector` |
  | `m01.newton()` | `m01.newton() needs one or more forces` |

- **No forces is a misuse,** not Newton's first law. `0 = b.mass*b01.a.x`
  would hold for a zero mass too, and no example needs it. An example
  with no net force says `.known(b01.a.x, 0)`.
- **As strings:**

  ```
  Particle("b", 2, X).edge(0, 1).newton(n, w, f)        n, w, f in X
    Eq(f.x + n.x + w.x, b.mass*b01.a.x)

  Particle("box", 2, XY).edge(0, 1).newton(F, n, w)     F, n, w in XY
    Eq(F.x + n.x + w.x, box.mass*box01.a.x)
    Eq(F.y + n.y + w.y, box.mass*box01.a.y)

  Particle("c", 2, Y).edge(0, 1).newton(w)              w in Y
    Eq(w.y, c.mass*c01.a.y)

  Particle("p", 3, X).edge(1, 2).newton(f)
    Eq(f.x, p.mass*p12.a.x)

  Particle("p", 3, X).edge(0, 1).newton(f, -n)
    Eq(f.x - n.x, p.mass*p01.a.x)
  ```

- **Imports:** `Sequence`, `TYPE_CHECKING`, `sympy`, `UsageError`,
  `Axes`, `Var`, and `Vec`, `Vector` and `describe` from `vectors.py`.
  `Edge` comes under `TYPE_CHECKING`, as `projectile.py` imports it.
  `particles.py` imports this module, and `vectors.py` doesn't, so
  there is no cycle. No `cast` is needed.
- **The module docstring** says what it is: Newton's second law on an
  edge, ΣF = m a, one equation per axis, with the particle's mass,
  `b.mass`, and the edge's acceleration, `b01.a`. The acceleration is
  the one the kinematics equations have, so a system with both, such as
  Example 4.5's, needs no equation to link them.
  `b01.newton(n, w, f)` calls this.

### `vectors.py`: `_describe` becomes `describe`

A rename, and nothing else: the definition and its thirteen uses, on
eight lines. `newton.py` needs it for its messages, so that a force
reads as it does in `.eq`'s: a vector's name, a `Vec`'s components, or
anything else's repr. A helper that a second module calls shouldn't
carry the underscore. It isn't re-exported from `equarium.physics`.

To leave `vectors.py` as it is instead, if the review prefers:
`newton.py` imports `_describe` under its private name. Pyright in
standard mode allows that. No other module imports a private name.

### `particles.py`: `Edge.newton` and `Particle.mass`

```python
    def newton(self, *forces: Vector[A] | Vec[A]) -> list[sp.Eq]:
        """Newton's second law, ΣF = m a: for each axis, the forces' sum
        equals the particle's mass times this edge's acceleration."""
        return newton_equations(self, forces)
```

```python
    @property
    def mass(self) -> Var:
        """The particle's mass, `m.mass`."""
        return mass_of(self.name)
```

- **`newton` is a one-line call,** after `projectile`, as `projectile`
  calls `projectile_setup`.
- **The forces share the edge's `A`,** so pyright flags a force in other
  axes. `self` needs no annotation: every edge has the law.
- **`mass` is a property,** after `edges` and before `edge`.
- **Imports:** `mass_of` and `newton_equations`, and `Vec` beside
  `Vector`.
- **The docstrings.** `Edge`'s gains a sentence: Newton's second law on
  an edge is `m01.newton(n, w, f)`. `Particle`'s gains one: its mass is
  `m.mass`, which Newton's second law uses.

### `notation.py`: the row for the mass

In `BookNotation.text`, in the branch for an empty `where`, after the
event's two cases and before the lone vector's:

```python
                case ("mass",):  # a particle's mass
                    return f"m{self.owners.get(symbol.owner, '')}"
```

- **`b.mass` prints `m`,** and `mB` with `owners={"b": "B"}`, as the
  spec's table says: `m`, and `mP` with the owner `P`. A particle's
  subscript applies to its mass, where it doesn't to an event or a lone
  vector.
- **The branch's comment** becomes: an event's, a particle's mass, then
  a lone vector's.
- **The docstrings.** The module's list of book forms gains "and a
  particle's mass, `m`". `BookNotation`'s gains a paragraph, after the
  event's: a particle's mass is the book's `m`: `b.mass` prints `m`, and
  `mP` with the owner's subscript.
- **4.5's (5) prints** `fx + nx + wx = m*ax`.

### `__init__.py`

- **No new re-export.** `newton` and `mass` are a method and a property.
- **The docstring** gains a paragraph, after the projectile setup's: an
  edge has Newton's second law, `b01.newton(n, w, f)`: ΣF = m a, one
  equation per axis, `f.x + n.x + w.x = b.mass*b01.a.x`. The mass is
  the particle's, `b.mass`, and the acceleration is the edge's, the one
  the kinematics equations have, so a system with both needs no
  equation to link them.
- **Its vectors paragraph** loses `(F + n + w).eq(a * m)`, which no
  example writes any more. `R.eq(F1 + F2 + F3)` stays as the example.

### The examples

| Module, under `examples/up_15e/` | What changes |
|---|---|
| `ch04/examples/n04/main.py` | `box = Particle("box", 2, XY)` and `box01`. `box01.newton(F, n, w)` replaces `(F + n + w).eq(a * m)`. `m` and `a` go: `box.mass`, `box01.a.y` and the want `box01.a.x` take their places. The system is `push`. |
| `ch04/examples/n05/main.py` | The forces are in `X`. `b01.newton(n, w, f)` replaces `(n + w + f).eq(a * m)` and the link. `m` and `a` go: `b.mass` takes `m`'s place. |
| `ch04/examples/n05/main_two_steps.py` | The forces are in `X`. `b01.newton(n, w, f)` replaces `(n + w + f).eq(a * m)`. `m` and `a` go: step 2 knows `b.mass`, and `b01.a.x` from step 1. |

**In every module:**

- **Everything else stays:** the other knowns, one per line, with their
  comments, in the same order, the solves and the `__main__`. The spec's
  sketch of 4.5 gives its knowns as two dicts. That is the shape, not
  the lines: the modules keep theirs.
- **`import sympy as sp` goes,** since nothing uses it any more. 4.5's
  two modules import `Particle`, `Vector` and `X`, without `XY`. 4.4
  imports `XY`, `Particle` and `Vector`.
- **Comments and docstrings use the new shape.** Each docstring says
  where Newton's second law comes from, and what the old script wrote.
  The lines are below.

#### 4.4

```python
from equarium import System
from equarium.physics import XY, Particle, Vector
from examples.answers import Answer

box = Particle("box", 2, XY)  # the box
box01 = box.edge(0, 1)

F = Vector("F", XY)  # the worker's force
n = Vector("n", XY)  # the normal force
w = Vector("w", XY)  # the weight

push = (
    System()
    .add(*box01.newton(F, n, w))  # (1), (2)
    .known(F.x, 20)  # N
    .known(F.y, 0)  # N
    .known(box01.a.y, 0)  # m/s²
    .known(n.x, 0)  # N
    .known(w.x, 0)  # N
    .known(box.mass, 40)  # kg
)

sol = push.solve(box01.a.x)
# box01.a.x = (F.x + n.x + w.x)/box.mass   0.5

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol, box01.a.x, "0.50"),  # m/s²
]
```

- **The system is `push`,** the worker's push, since `box` is the
  particle now, as the spec names it. `__main__` shows `push`.
- **The box's states aren't named.** Nothing uses them: there are no
  kinematics here.
- **`push`, as `show()` prints it:**

  ```
  (1)  F.x + n.x + w.x = box.mass*box01.a.x
  (2)  F.y + n.y + w.y = box.mass*box01.a.y
  knowns: F.x = 20, F.y = 0, box01.a.y = 0, n.x = 0, w.x = 0, box.mass = 40
  ```

- **The docstring's second paragraph.** "with the physics code's lone
  vectors and `.eq` where it had local helpers for the forces and
  Newton's second law" becomes: with the physics code's lone vectors
  and Newton's second law on the box's edge, `box01.newton(F, n, w)`,
  where it had local helpers for the forces and the law. Then, new: the
  box is a particle, so its mass is `box.mass` and its acceleration is
  the edge's, `box01.a`, where the old script made its own `m` and `a`.
  There are no kinematics here: the box has two states only so that it
  has an edge. The rest stays, from "Its zeros are values".

#### 4.5

```python
from equarium import System
from equarium.physics import Particle, Vector, X
from examples.answers import Answer

b = Particle("b", 2, X)  # the bottle
b0, b1 = b.states
b01 = b.edge(0, 1)

n = Vector("n", X)  # the normal force
w = Vector("w", X)  # the weight
f = Vector("f", X)  # the friction force

counter = (
    System()
    .add(*b.kinematics())  # (1) to (4)
    .known(b0.t, 0)  # s
    .known(b0.pos.x, 0)  # m
    .known(b1.pos.x, 1.0)  # m
    .known(b0.vel.x, 2.0)  # m/s
    .known(b1.vel.x, 0.0)  # m/s
    .add(*b01.newton(n, w, f))  # (5): Newton's acceleration is the kinematics'
    .known(n.x, 0)  # N
    .known(w.x, 0)  # N
    .known(b.mass, 0.45)  # kg
)

sol = counter.solve(f.x)
# f.x = (b.mass*b0.vel.x**2/2 - b.mass*b1.vel.x**2/2 - b0.pos.x*n.x - b0.pos.x*w.x
#        + b1.pos.x*n.x + b1.pos.x*w.x)/(b0.pos.x - b1.pos.x)   -0.9
```

- **The `BOOK` and `__main__` don't change.**
- **The normal force and the weight stay,** in `X`, with their zero x
  components. The old script gave those zeros, and the formula keeps
  `n.x` and `w.x`, as the row has them.
- **`counter`, as `show()` prints it:**

  ```
  (1)  b01.dt = -b0.t + b1.t
  (2)  b01.v_av.x = (-b0.pos.x + b1.pos.x)/b01.dt
  (3)  b01.a.x = (-b0.vel.x + b1.vel.x)/b01.dt
  (4)  b01.v_av.x = b0.vel.x/2 + b1.vel.x/2
  (5)  f.x + n.x + w.x = b.mass*b01.a.x
  knowns: b0.t = 0, b0.pos.x = 0, b1.pos.x = 1.0, b0.vel.x = 2.0, b1.vel.x = 0.0, n.x = 0, w.x = 0, b.mass = 0.45
  ```

- **The docstring's second paragraph.** "the kinematics and Newton's
  second law in one system, linked through the acceleration, solved all
  at once" becomes: the kinematics and Newton's second law in one
  system, solved all at once. Then, new:
  - Newton's second law is on the bottle's edge, `b01.newton(n, w, f)`,
    so its acceleration is the kinematics', `b01.a.x`, and its mass is
    the bottle's, `b.mass`;
  - the old script made its own `a` and `m`, and linked the two
    accelerations with an equation, `a.x = b01.a.x`;
  - the forces are in x only, as the bottle is, so the old script's y
    equation, which no want needs, has no counterpart here.

  The rest stays, from "Its zeros are values".

#### 4.5 in two steps

Step 1 doesn't change. Step 2:

```python
# Step 2: the friction force, from Newton's second law.
n = Vector("n", X)  # the normal force
w = Vector("w", X)  # the weight
f = Vector("f", X)  # the friction force

push = (
    System()
    .add(*b01.newton(n, w, f))  # (1)
    .known(n.x, 0)  # N
    .known(w.x, 0)  # N
    .known(b.mass, 0.45)  # kg
    .known(b01.a.x, sol_1.number(b01.a.x))  # m/s², from step 1
)
sol_2 = push.solve(f.x)
# f.x = b.mass*b01.a.x - n.x - w.x   -0.9
```

- **The `BOOK` and `__main__` don't change.**
- **`push`, as `show()` prints it:**

  ```
  (1)  f.x + n.x + w.x = b.mass*b01.a.x
  knowns: n.x = 0, w.x = 0, b.mass = 0.45, b01.a.x = -2.0
  ```

- **The docstring's second paragraph.** "with the physics code's lone
  vectors and `.eq` where it had local helpers for the forces and
  Newton's second law" becomes: with the physics code's lone vectors
  and Newton's second law on the bottle's edge, `b01.newton(n, w, f)`,
  where it had local helpers for the forces and the law. At its end,
  new: the acceleration is one symbol in both steps, `b01.a.x`, where
  the old script's step 2 had its own `a`, and the mass is the
  bottle's, `b.mass`. The forces are in x only, as the bottle is, so
  step 2 is one equation, where the old script displayed two.

### Tests

**`tests/old_names.py`: three names in `SCRIPT_NAMES`,** after 4.1's:

```python
    "ch04.examples.n04.main": {
        Var("box", "", "mass"): "m",
        Var("box", "01", "a", "x"): "a_x",
    },
    "ch04.examples.n05.main": {Var("b", "", "mass"): "m"},
```

- **No rule for the mass.** `m` is a name the old scripts made
  themselves, which is what the map is for. `old_name(b.mass)` without
  a module still raises, and the test that says so stays.
- **`box01.a.y` has no entry.** It is a known and in (2), but in no
  formula.
- **The module docstring.** "Increment 006 adds 4.5's `b.mass`" becomes:
  4.4's `box.mass` and 4.5's `b.mass` are their `m`, and 4.4's
  `box01.a.x` is its `a_x`, where the rule says `a_x_box_0_1`. The list
  of what the rules don't cover gains a particle's mass.

**`tests/test_old_outputs.py`:**

- **`OLD`, `RESHAPED` and both guards don't change,** not by one
  character. The counts stay 66 and 5.
- **`test_old_name_in_its_module_is_the_scripts`** gains:

  ```python
  box = (Var("box", "", "mass"), Var("box", "01", "a", "x"))
  assert [old_name(v, "ch04.examples.n04.main") for v in box] == ["m", "a_x"]
  assert old_name(Var("b", "", "mass"), "ch04.examples.n05.main") == "m"
  ```

- **`test_old_name_the_map_wins_over_the_rule`** gains:

  ```python
  box01_a_x = Var("box", "01", "a", "x")  # 4.4's acceleration, the old script's own
  assert old_name(box01_a_x, "ch04.examples.n04.main") == "a_x"
  assert old_name(box01_a_x) == "a_x_box_0_1"
  ```

- **One new test,** after `test_3_6_given_v1x_again_is_the_old_output`.
  It pins the one formula that changes and has no row:

  ```python
  def test_4_5_step_2_has_the_edges_acceleration() -> None:
      # Not a row: the old script never solved its step 2. The catalog's
      # scratch try gave `f_x = a_x*m - n_x - w_x`, with step 2's own `a_x`.
      # Since increment 006 of the 004 series, the acceleration is the
      # edge's, the one symbol step 1 solves for and step 2 knows.
      module = importlib.import_module("examples.up_15e.ch04.examples.n05.main_two_steps")
      sol_1, sol_2 = getattr(module, "sol_1"), getattr(module, "sol_2")
      assert isinstance(sol_1, Solution) and isinstance(sol_2, Solution)
      f_x, b_mass, b01_a_x = Var("f", "", "x"), Var("b", "", "mass"), Var("b", "01", "a", "x")
      formula = sol_2.formula(f_x)
      assert str(formula) == "b.mass*b01.a.x - n.x - w.x"
      old_names = {b_mass: sp.Symbol("m"), b01_a_x: sp.Symbol("a_x")}
      assert old_str(formula.xreplace(old_names)) == "a_x*m - n_x - w_x"
      assert b01_a_x in sol_1.system.wants
      assert sol_2.system.knowns[b01_a_x] == sol_1.number(b01_a_x)
  ```

- **A comment.** In `test_old_name_of_a_lone_vector`, the comment on
  the last assert, `# 4.4's acceleration`, becomes
  `# as the old 4.4's acceleration was`. The assert stays: it tests the
  rule.
- **The module docstring.** "such as 3.6's `dist` and 2.5's `t_01`"
  becomes "such as 3.6's `dist`, 2.5's `t_01` and 4.5's `m`".

**`tests/test_physics.py`:** a section "# Newton's second law, and the
mass", after the projectile setup and before `BookNotation`. Import
`render` beside `render_solution`. Scratch passed these eight:

- **`test_a_particles_mass`:** `b.mass` of `Particle("b", 2, X)` is
  named `b.mass` and equals `Var("b", "", "mass")`. A plain
  `sp.Symbol("b.mass")` differs. `Particle("b", 3, XY).mass` equals it,
  and `Particle("box", 2, XY).mass` doesn't.
- **`test_newton_on_an_edge`:** `b01.newton(n, w, f)`, in `X`, is one
  equation, the first string above. Its right side equals
  `b.mass * b01.a.x`. The forces in another order give the same
  equations.
- **`test_newton_makes_one_equation_per_axis`:** the box's two strings
  above, and the `Y` edge's one.
- **`test_newton_of_a_later_edge_and_of_a_vector_expression`:** the two
  strings of `Particle("p", 3, X)` above.
- **`test_newton_with_the_kinematics_needs_no_link`:** 4.5's shape.
  `System().add(*b.kinematics()).add(*b01.newton(f))` has the labels 1
  to 5. (3) is `Eq(b01.a.x, (-b0.vel.x + b1.vel.x)/b01.dt)` and (5) is
  `Eq(f.x, b.mass*b01.a.x)`. With
  `{b.mass: 2, b0.vel.x: 0, b1.vel.x: 6, b0.t: 0, b1.t: 3}` known,
  `solve(f.x)` gives `b.mass*(b0.vel.x - b1.vel.x)/(b0.t - b1.t)`, and
  4.0 as a float, since `Float(4) == 4` is false.
- **`test_newton_misuses_raise`:** the five messages of the table
  above, each matched with `re.escape`. The misplaced force is cast to
  `Any`, so pyright doesn't see the misuse there. `m01` is the module's
  `X` edge and `F1` its `XY` vector.
- **`test_newton_renamed_back_is_the_old_copys`:** it uses the old
  copy, so 007 deletes it with the copy, and says so in a comment.

  ```python
  box = Particle("box", 2, XY)
  box01 = box.edge(0, 1)
  F, n, w = Vector("F", XY), Vector("n", XY), Vector("w", XY)
  k, a = sp.Symbol("m"), make_point("a")
  names = {box.mass: k, box01.a.x: a.x, box01.a.y: a.y}
  new = [old_str(eq.xreplace(names)) for eq in box01.newton(F, n, w)]
  forces = [make_point("F"), make_point("n"), make_point("w")]
  old = [str(eq) for eq in newtons_second_law(forces, k, a)]
  assert new == old
  ```

- **`test_the_book_notation_of_a_mass`,** with the other notation
  tests: `m`, and `mB` with `owners={"b": "B"}`. Then
  `render(System().add(*b01.newton(n, w, f)), symbol=BookNotation(color=False))`
  starts with `(1)  fx + nx + wx = m*ax\n`.
- **The module docstring** names Newton's second law and the mass.

**`tests/physics_misuse.py`:** add at the end:

```python
# Newton's second law with a force that isn't in the edge's axes.
m01.newton(F1)  # pyright: ignore[reportArgumentType]
Particle("d", 2, XY).edge(0, 1).newton(f)  # pyright: ignore[reportArgumentType]
```

The spec asks for the `XY` force on an `X` edge. The `X` force on an
`XY` edge is added because it's the likely slip now: 4.5's forces are
in `X` and 4.4's in `XY`. Check once that it bites: put the same ignore
on `m01.newton(f)`, see `uv run pyright` fail, and take it out.

**`tests/test_examples.py`, `tests/test_strategies.py` and
`tests/slow_examples.py`:** no change.

### If a formula moves that this page doesn't list

No row moves. Every row of `tests/test_old_outputs.py`, renamed back
through the rules and the map with its three new names, must come out
verbatim, and so must 3.10's show-that. If one moves, or 4.5's f_x
comes out as anything but its row, stop. Don't change a row, add to
`RESHAPED`, add a name beyond the three, or change a module's
equations or the order of anything to make it pass. Report the row,
what came out, and what you think moved it. The same holds for a
`BOOK` that stops matching, and for `sol_2` of 4.5 in two steps if its
formula isn't `b.mass*b01.a.x - n.x - w.x`.

## Docs

- **The docstrings** of `physics/__init__.py`, `newton.py`,
  `particles.py`, `notation.py`, the three modules and the three test
  files, as above.
- **The package `README.md`** doesn't change.
- **The series [README](../README.md):** mark 006 done in its
  increments table, and update its status line and the "5 of 7 done".
  Leave the commit cell and this page's status line for the manager.
- **The [series map](../../README.md):** 004's status says 6 of 7
  increments are done.
- **Don't edit** `spec.md`, `charter.md` or this page. If something
  here is wrong, say so in the report.

## Check and commit

- **`uv run pytest`** passes: the 338 fast tests and yours. Scratch had
  347, in as long as its 338 took before. Report how long it and
  `tests/test_examples.py` take.
- **`uv run pytest -m slow`** passes the 3 slow tests, in about 5 min.
  Run it in the background.
- **`uv run pyright`:** 0 errors and 0 warnings, over `src`, `tests`
  and `examples`, `tests/physics_misuse.py` included.
- **Every changed module** runs with
  `uv run python -m examples.up_15e.ch04.examples.n04.main`, and
  likewise `n05.main` and `n05.main_two_steps`.
- **The times.** Report each changed module's import time. None should
  be near 5 s.
- **No mass, acceleration or link of their own left.** With `F` for
  the three files, `examples/up_15e/ch04/examples/n04/main.py`,
  `n05/main.py` and `n05/main_two_steps.py`:
  `grep -n 'sp\.Symbol("m")\|Vector("a"\|\.eq(a \* m)\|Eq(a\.x\|known(a\.\|known(m,\|import sympy' $F`
  finds nothing. Today it finds 18 lines.
  `grep -n 'XY' examples/up_15e/ch04/examples/n05/*.py` finds nothing,
  where today it finds 10 lines.
  `grep -rn '\.add(\*.*\.newton(' examples` finds three lines, one in
  each module.
- **No private name crosses a module.**
  `grep -rn '_describe' src tests examples` finds nothing.
- **No files outside the repo.** Keep scratch output in your own
  scratch folder.
- **One commit on the branch `2026-11-08-physics-redesign`,** with the
  code, tests and docs, in the style of `git log`: a subject line, then
  a wrapped paragraph saying what and why. Don't push.

## Report

When done, say in a few lines:

- the commit, the number of tests, fast and slow, how long the fast run
  and `tests/test_examples.py` take, and each changed module's import
  time;
- that no row moved, that the two rows pass through the three new
  names, and that 4.5's f_x is its row, verbatim, or, if not, the row
  and what came out (you stopped there);
- that `sol_2`'s formula is the one pinned;
- any name or message you chose differently from this page, and why;
- what pyright needed beyond what this page names;
- anything in the spec or this checkpoint that was wrong or unclear,
  and what you did instead.

Then stop. Increment 007, the end, is a separate checkpoint.
