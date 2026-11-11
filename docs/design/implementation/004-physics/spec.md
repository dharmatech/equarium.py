# 004 physics: spec

**Status:** Agreed with the user (2026-11-08). The decisions marked
*(user)* were settled with the user. The rest were proposed and left
standing. No increment has started.

What equarium's physics layer will be, in seven increments, one
checkpoint each. The [charter](charter.md) has the background, the
lessons from the old physics code and the references. This page is
what was decided.

## What the prototype showed

A scratch prototype of the whole layer, on the core unchanged
(2026-11-08). It is saved outside the repo, in
`~/.config/Claude/side-session-notes/local_9ac850c1-eb15-42fc-bbb0-61739b724d16/004-spec-prototype/`:
`layer.py` (the layer in one file), `sketches.py`, `ch3.py`,
`rename_all.py`, `typing_check.py` and `misuse.py`. It's data for the
checkpoints, not a design: this page wins where they differ.

- **The rename is safe.** `rename_all.py` makes the old physics code
  produce the new symbols, with the same equations, and runs every
  port unchanged. All 66 formulas of `tests/test_old_outputs.py`,
  renamed back to the old names, come back verbatim, and so does
  3.10's show-that. The new names sort in a new order, and
  `solve.py` sorts the unknowns by name, but no formula moved.
- **Name is enough for identity.** With the owner's name as its
  identity, 2.4 gives 43, 23 and 55, and 2.5 with an event gives 10, 30
  and 150 in one solve. 2.5 step by step still has its six links to
  eliminate.
- **Pyright sees the dimension.** With the axes as a type parameter,
  pyright flagged all seven misuses tried (`m0.pos.y` in an x-only
  model, `.mag` in 1D, `.x` in a y-only model, the projectile setup on
  an x-only edge, an xy force plus an x force, an xy force on an x
  edge, `.y` of an x-only event) and nothing else.
- **A file of misuses can stay in pyright's run.** Each misuse carries
  `# pyright: ignore[rule]`, and the file sets
  `reportUnnecessaryTypeIgnoreComment=true`. A misuse pyright stops
  flagging then fails `uv run pyright`.
- **One-way polar makes the workarounds unnecessary.** 3.8 solves all
  at once without its two by-hand eliminations (0.3 s), with the book's
  formulas. 3.9 solves all at once in 1.6 s, with the same two roots
  and formulas as its `eliminating()` run (5.9 s). 3.10's dart takes
  0.7 s and keeps the same two equations, (8) and (9).
- **The projectile setup spares 3.6 its by-hand step.** With the
  setup's `v0x = v1x` and only v0x given, 3.6 solves all at once
  (1.8 s): 4.5, −1.225, 4.66, −4.9, 10.25 and −28.6°. With v1x also
  given, it still finds no roots, as the charter says.
- **Newton on the edge keeps 4.5's formula.** `b01.newton(n, w, f)`
  gives the old `f_x` formula, with `b.mass` for `m` and no link
  equation, and −0.90.
- **The book's notation reads well.** The book writes `xP`, `vP0x`
  and `aPx` in 2.5, and `xdart`, `ymonkey` in 3.10. So the owner's
  subscript comes from the example, and the order is the book's:
  letter, owner, state, axis.

## Decisions

### The structured symbol: `Var`

- **`Var`, a subclass of `sp.Symbol`,** in `physics/symbols.py`. Its
  fields are three plain strings: `owner` (`"m"`), `where` (`""`, a
  state `"0"`, or an edge `"01"`) and `path` (`("pos", "x")`).
- **Its name is its access path:** `owner + where`, then the path,
  joined by dots. `m0.pos.x`, `m01.a.x`, `m1.t`, `F1.x`, `b.mass`,
  `meet.t`. That is the one naming rule.
- **Its identity is its structure.** `_hashable_content()` is
  `(name, owner, where, *path)`, all strings, in fixed positions,
  because SymPy compares them element by element to sort terms. It is
  built with `sp.Symbol.__xnew__`, which skips SymPy's name cache, and
  pickles through `__reduce_ex__`, as in the charter's excerpt. A plain
  `sp.Symbol("m0.pos.x")` is a different symbol.
- **No SymPy assumptions,** so every root stays, as 2.8 teaches.

### Owners are values *(user)*

- **An owner's name is its identity.** `Particle("m", 2, X)` made twice
  is the same particle, with the same symbols. Symbols that print
  alike are always equal. Two owners in one problem need two names.
  There is no hidden key, so the charter's `owner_key` goes.
- **Names.** A particle's or an event's name is a Python identifier
  that doesn't end in a digit, since `p2` with state 0 would print
  `p20.t`. A vector's name may end in one: `F1`. A bad name raises
  the core's `UsageError`.

### Particles, states and edges

- **One owner type, `Particle`,** for a particle that moves and for a
  body with forces. 4.5 needs both on one owner. `System` stays the
  core's, and `Quantity` stays `sympy.physics.units`'s.
- **`Particle(name, states, axes)`:** `Particle("m", 2, X)`. Two to ten
  states. Ten is the most that keeps `m01` unambiguous, and no example
  has more than three.
- **States:** `m0, m1 = m.states`. A `State` has `pos` and `vel`
  (vectors) and `t`.
- **Edges:** `m01 = m.edge(0, 1)`, and `m.edges` for all of them. Edges
  join consecutive states only, as before. An `Edge` has `dt`, `a`
  and `v_av` (vectors), and `start` and `end`.
- **The mass** is the particle's: `b.mass`, named `b.mass`. Only
  Newton's laws use it (increment 006).
- **Frozen dataclasses,** compared by value. States, edges and vectors
  are made on demand from the owner's name, so they hold no symbols.

### The dimension *(user)*

- **Set once, when the model is made, as a type:** `X`, `Y` or `XY`,
  in `physics/axes.py`. Each is a class with `names`, such as
  `("x", "y")`, and is passed as the class: `Particle("d", 2, XY)`.
  2.6 and 2.7 use `Y`. There is no `Z`, since no example needs it.
- **`Particle`, `State`, `Edge`, `Vector`, `Vec` and `Event` are
  generic in the axes.** The axis properties annotate `self`:
  `x` needs `Vector[X] | Vector[XY]`, `y` needs `Vector[Y] | Vector[XY]`,
  and the polar parts need `Vector[XY]`. So pyright flags `m0.pos.y`
  in an x-only model.
- **Run time agrees.** The same misuse raises `UsageError` when run,
  so a script that skips pyright fails the same way.
- **A misuse file,** `tests/physics_misuse.py`, in pyright's run, as in
  the prototype. Each increment adds the misuses its features can
  have.

### Kinematics

- **`m.kinematics()`** returns, for every edge and every axis of the
  model, the book's 2.2, 2.7 and 2.10, with Δt defined per edge. The
  order is the old one: every Δt, then 2.2 for each edge and axis, then
  2.7, then 2.10. So the automatic labels stay as they were.
- **The same equations as the old code,** in the new names:
  `Eq(m01.dt, -m0.t + m1.t)`,
  `Eq(m01.v_av.x, (-m0.pos.x + m1.pos.x)/m01.dt)`,
  `Eq(m01.a.x, (-m0.vel.x + m1.vel.x)/m01.dt)`,
  `Eq(m01.v_av.x, m0.vel.x/2 + m1.vel.x/2)`.
- **No options.** Every old call included v_av, Δt and all three
  equations, so the old flags go.

### Vectors and vector equations

- **A small vector type of our own,** in `physics/vectors.py`, not
  `sympy.physics.vector`, which needs reference frames, prints its own
  way, and doesn't hold our `Var`s.
- **`Vector[A]`** is a named vector whose components are `Var`s:
  `m0.pos`, `m01.a`, or a lone vector `Vector("F1", XY)`. It has `x`
  and `y` by its axes, and on `XY` the polar parts `mag`, `angle` and
  `angle_deg`. Every 2-axis vector has them, positions included, so
  3.6's distance is `m1.pos.mag`.
- **`Vec[A]`** is a vector expression: one SymPy expression per axis.
  `+`, `-`, unary `-` and `*` by a scalar work on both, and give a
  `Vec`. `sum()` works on vectors.
- **`.eq(other)`** returns one `sp.Eq` per axis, x first:
  `R.eq(F1 + F2 + F3)` is `R.x = F1.x + F2.x + F3.x`, then y. So laws
  are written once and expanded per axis. They still display one
  component per line.
- **Mixed dimensions are type errors:** `F1 + f` with `F1` in `XY` and
  `f` in `X`.

### Polar and degrees

Methods on a 2-axis vector, each returning equations, one way each:

| Method | Equations |
|---|---|
| `v.from_polar()` | `v.x = v.mag*cos(v.angle)`, `v.y = v.mag*sin(v.angle)` |
| `v.to_polar()` | `v.mag = sqrt(v.x**2 + v.y**2)`, `v.angle = atan2(v.y, v.x)` |
| `v.degrees()` | `v.angle_deg = 180*v.angle/pi` (SymPy's `deg`) |

- **One-way only.** Two-way polar is `from_polar()` and `to_polar()`
  added together, which the rename step uses for the old
  `magnitude_and_angle_equations`. After increment 003, no example
  uses both on one vector.
- **Givens in degrees stay by hand:** `.known(b0.vel.angle, sp.rad(53.1))`.
  The formulas keep the book's α0, not `pi/180` factors.

### Events

- **`Event(name, *states)`:** `Event("meet", m1, p1)`, two or more
  states with the same axes. It owns `meet.t` and `meet.pos`.
- **`event.equations(axes=None)`** writes the links as equations:
  each state's time equals the event's, then, for each axis, each
  state's position equals the event's. `m1.t = meet.t`,
  `p1.t = meet.t`, `m1.pos.x = meet.pos.x`, `p1.pos.x = meet.pos.x`.
  The time is always linked. `axes` picks the position axes, `Y` for
  3.10, and defaults to all of them.
- **Links stay equations,** as the charter decided, so 2.5 step by
  step still has links to eliminate.

### The projectile setup

- **`d01.projectile(g)`,** on an `XY` edge, returns a `Setup`: a
  named tuple of `equations` and `knowns`. The equations are
  `d01.a.y = -g` and `d0.vel.x = d1.vel.x`, in the ports' order. The
  knowns are `{d01.a.x: 0}`. The example adds both:
  `.add(*flight.equations).known(flight.knowns)`.
- **The origin and the clock stay the example's,** since 3.9 starts at
  y0 = 8.0 and ends at y1 = 0. The example sets its own zero positions
  and times.
- **No other equations for a zero-acceleration axis.** The setup's
  `v0x = v1x` already spares 3.6 its by-hand step, when v1x is derived
  rather than given.

### Newton's laws

- **`b01.newton(*forces)`** returns ΣF = m a over the edge's axes, one
  equation per axis: `f.x + n.x + w.x = b.mass*b01.a.x`. The
  acceleration is the edge's, so 4.5 needs no link equation. The
  forces must have the edge's axes.
- **Superposition is a vector equation,** `R.eq(F1 + F2 + F3)`, with no
  helper of its own.
- **4.4** gets a particle with two states, `Particle("box", 2, XY)`, so
  its acceleration is `box01.a`.

### Relative velocity and weight

No helpers. 3.13 (3.32 and 3.33) and 4.7 (`w = m*g`, `F = m*a`) are two
equations each, and the written-out form is their lesson. They stay as
they are.

### Labels

**The automatic numbers stay.** The core labels an equation only one
`add` at a time, and the core doesn't change in this series. So the
physics layer can't label its equations `(2.2 m01 x)`. 3.10 keeps
picking `dart.equation("8")` by number. Labels from the physics layer
go to "What's next".

### Book notation *(user)*

- **`BookNotation`,** in `physics/notation.py`: a frozen dataclass that
  is a display hook, `(symbol, role) -> str`. It prints the book's
  notation as plain text, **glued, as the book's text reads:** `x0`,
  `v0x`, `ax`, `vP0x`, with `Δt` and `α`. Knowns are green and wants
  red, with the core's `GREEN`, `RED` and `RESET`.
- **Fields:** `owners`, a map from an owner's name to the book's
  subscript (`{"m": "M", "p": "P"}` for 2.5, `{"d": "dart", "m": "monkey"}`
  for 3.10); an owner not in it gets none. `edge_index`, off by
  default, prints an edge's states (`Δt01`, `a01x`) for problems with
  several edges. `color`, on by default.
- **The table:**

  | Symbol | Book | With owner `P` |
  |---|---|---|
  | `m0.pos.x`, `m0.pos.y` | `x0`, `y0` | `xP0` |
  | `m0.pos.mag` | `r0` | `rP0` |
  | `m0.vel.x` | `v0x` | `vP0x` |
  | `m0.vel.mag` | `v0` | `vP0` |
  | `m0.vel.angle`, `angle_deg` | `α0`, `α0°` | `αP0` |
  | other angles (`m0.pos.angle`, `R.angle`) | `θ0`, `θR` | |
  | `m0.t` | `t0` | `tP0` |
  | `m01.dt` | `Δt` | `ΔtP` |
  | `m01.a.x` | `ax` | `aPx` |
  | `m01.v_av.x` | `vavx` | `vavPx` |
  | `b.mass` | `m` | `mP` |
  | `F1.x`, `F1.mag` | `F1x`, `F1` | |
  | `meet.t`, `meet.pos.x` | `t`, `x` | |
  | a plain symbol | its name | |

- **The debug form is the name,** with the core's default hook. Tests
  compare names. `System.show()` takes no hook, so an example prints
  the book form with `print(render(system, symbol=notation))`.
- **2.4 and 2.5** print the book form after the names in their
  `__main__`. The other examples print names only.

### The steps the helpers make unnecessary *(user)*

**Dropped.** Each `main.py` solves all at once, and its docstring says
which step went and why:

- **3.6:** `eliminate(m01.dt)`. The projectile setup's `v0x = v1x`
  gives v1x, which is no longer a given. The book's v_x = 9.0 m/s
  becomes an `Answer`.
- **3.8:** the two `eliminate(…, using=…)`, needed only with two-way
  polar.
- **3.9:** `eliminating()`. With one-way polar it solves all at once in
  about 1.6 s and leaves `SLOW_EXAMPLES`. `tests/test_strategies.py`
  keeps the `eliminating()` lesson, written out.

3.10 keeps its by-hand eliminations: that is its style. The list
changes only where the helpers change the equations.

### The examples

- **They change in place** (charter). Each `main.py` moves to the new
  layer, and git and the tag keep the old version. The written-out
  modules stay as they are.
- **The rename step renames what the old physics code made:** states,
  edges, `make_point` vectors, and 4.1's local copies of them. Symbols
  an example made itself (`m_v`, `dist`, `t_01`, `vel_mag`,
  `R_angle_deg`, `m`) stay plain until a reshape gives them a helper.
- **The `assert … is not None` narrowings go,** since nothing is
  optional any more.
- **`Formula` takes an expression,** not a string:
  `Formula(sol_t, d1.t, D/(d0.vel.mag*sp.cos(d0.vel.angle)))`. It is
  typed, and `parse_expr` can't read dotted names. Every free symbol
  must be a symbol of the solution. The string parsing in
  `examples/answers.py` goes.

### The tests

- **`tests/test_old_outputs.py` keeps the old formulas verbatim,** in
  the old names. A function in the tests, `old_name`, renames a `Var`
  back by the old rule (`m0.pos.x` → `m_0_x`, `m01.a.x` → `a_x_m_0_1`,
  `F1.x` → `F1_x`). A per-module map covers the symbols the rule can't
  reach, such as `meet.t` → `t_01` and `b.mass` → `m`. Plain symbols
  keep their names.
- **A reshape that changes a formula** keeps the row's old formula as
  the record and adds the new one, in the new names. The test then
  compares the new one verbatim, and the number with the old number,
  as before. The checkpoint lists every such row.
- **`tests/test_physics.py` is rewritten** for the new layer: identity,
  names, pickling, the kinematics equations as strings, vectors, polar,
  events, the projectile setup, Newton, and the notation. It keeps the
  check that the core doesn't import `equarium.physics`.
- **`tests/physics_misuse.py`,** checked by pyright (above).
- **The `BOOK`s never change,** except to add an answer a reshape
  makes available (3.6's v_x).

### The package

```
src/equarium/physics/
  __init__.py       re-exports: Var, X, Y, XY, Vector, Vec, Particle,
                    State, Edge, Event, Setup, BookNotation
  symbols.py        Var
  axes.py           Axes, X, Y, XY
  vectors.py        Vec, Vector
  polar.py          from_polar, to_polar, degrees
  particles.py      Particle, State, Edge
  kinematics.py     the kinematics equations
  events.py         Event
  projectile.py     Setup, the projectile setup
  newton.py         Newton's second law
  notation.py       BookNotation
  kinematics_states.py, newtons_laws.py
                    the old copy, until increment 007
```

- **Methods delegate.** As in the core, a method such as
  `m.kinematics()` or `v.from_polar()` is a one-line call into a small
  module of plain functions.
- **Layers.** The physics layer imports the core (`UsageError`, the
  display's colors and `Role`). The core imports nothing from physics.
- **The split can move** in a checkpoint, if a module turns out too
  small or makes an import cycle. Everything is typed, and pyright
  (standard mode) stays clean.

## Sketches

How four examples read at the end of the series. The checkpoints may
adjust names, but not the shape.

**2.4,** one particle:

```python
from equarium import System
from equarium.physics import Particle, X

m = Particle("m", 2, X)  # the motorcyclist
m0, m1 = m.states
m01 = m.edge(0, 1)

motorcycle = (
    System()
    .add(*m.kinematics())  # (1) to (4)
    .known(m0.t, 0)  # s
    .known(m01.a.x, 4)  # m/s²
    .known(m0.pos.x, 5)  # m
    .known(m0.vel.x, 15)  # m/s
    .eliminate_zeros()
)
sol_a = motorcycle.known(m1.t, 2).want(m1.pos.x, m1.vel.x).solve()
# m1.pos.x = m0.pos.x + m0.vel.x*m1.t + m01.a.x*m1.t**2/2   43
# book:  x1 = x0 + v0x*t1 + ax*t1**2/2
```

**2.5,** two particles and an event:

```python
m = Particle("m", 2, X)  # the motorist
p = Particle("p", 2, X)  # the police officer
m0, m1 = m.states
p0, p1 = p.states
p01 = p.edge(0, 1)
meet = Event("meet", m1, p1)  # the same time and place
m_v = sp.Symbol("m_v")

chase = (
    System()
    .add(*m.kinematics(), *p.kinematics())  # (1) to (8)
    .add(sp.Eq(m0.vel.x, m_v), sp.Eq(m1.vel.x, m_v))  # (9), (10)
    .add(*meet.equations())  # (11) to (14): m1.t = meet.t, …
    .known(m_v, 15)  # m/s
    .known({p0.vel.x: 0, p0.pos.x: 0, m0.pos.x: 0, m0.t: 0, p0.t: 0})
    .known(p01.a.x, 3)  # m/s²
    .want(meet.t, p1.vel.x, meet.pos.x)
    .eliminate_zeros()
)
sol = chase.solve()
# meet.t = 2*m_v/p01.a.x   10
# book, with BookNotation(owners={"m": "M", "p": "P"}):  t = 2*m_v/aPx
```

**3.10,** two particles, polar, the projectile setup and an event:

```python
D, g = sp.symbols("D g")
d = Particle("d", 2, XY)  # the dart
d0, d1 = d.states
d01 = d.edge(0, 1)
flight = d01.projectile(g)

dart = (
    System()
    .add(*d.kinematics())  # (1) to (7)
    .add(*d0.vel.from_polar())  # (8), (9)
    .add(*flight.equations)  # (10), (11)
    .known(flight.knowns)  # d01.a.x = 0
    .known({d0.pos.x: 0, d0.pos.y: 0, d0.t: 0})
    .known(g)
    .known(d0.vel.mag)  # v0
    .known(d0.vel.angle)  # α0
    .eliminate_zeros()
    .eliminate(d01.dt, d01.v_av.x, d0.vel.x, d1.vel.x, d0.vel.y, d01.v_av.y, d01.a.y, d1.vel.y)
)
# (8)  d1.pos.x/d1.t = d0.vel.mag*cos(d0.vel.angle)
# (9)  g*d1.t/2 + d1.pos.y/d1.t = d0.vel.mag*sin(d0.vel.angle)

# The monkey, m, likewise, from x0 = D and y0 = D*tan(α0), at rest.
hit = Event("hit", d1, m1)
meet = (
    System()
    .add(dart.equation("8").eq, dart.equation("9").eq, monkey.equation("9").eq)
    .add(*hit.equations(Y))  # the same time and height
    .known(D)
    .known(g)
    .known(d0.vel.mag)
    .known(d0.vel.angle)
)
proved = meet.eliminate(d1.t, m1.t, d1.pos.y, m1.pos.y, hit.pos.y, hit.t)
# D*d0.vel.mag*sin(d0.vel.angle)/d1.pos.x = d0.vel.mag*sin(d0.vel.angle)
```

**4.5,** kinematics and Newton on one particle:

```python
b = Particle("b", 2, X)  # the bottle
b0, b1 = b.states
b01 = b.edge(0, 1)
n, w, f = Vector("n", X), Vector("w", X), Vector("f", X)  # normal, weight, friction

counter = (
    System()
    .add(*b.kinematics())  # (1) to (4)
    .add(*b01.newton(n, w, f))  # (5): f.x + n.x + w.x = b.mass*b01.a.x
    .known({b0.t: 0, b0.pos.x: 0, b1.pos.x: 1.0, b0.vel.x: 2.0, b1.vel.x: 0.0})
    .known({n.x: 0, w.x: 0, b.mass: 0.45})  # N, N, kg
)
sol = counter.solve(f.x)
# f.x = (b.mass*b0.vel.x**2/2 - b.mass*b1.vel.x**2/2 - b0.pos.x*n.x - …)/(b0.pos.x - b1.pos.x)   -0.90
```

## Increments

| # | Increment | Adds | Moves |
|---|---|---|---|
| 001 | symbols and chapter 2 | `Var`, the axes, `Vector` (components), `Particle`, `State`, `Edge`, kinematics, `BookNotation` | chapter 2's 12 modules, renamed |
| 002 | chapters 3 and 4, renamed | vector arithmetic and `.eq`, lone vectors, the polar parts, `from_polar`, `to_polar`; `Formula` takes an expression | chapters 3 and 4's 10 modules, renamed |
| 003 | polar and degrees | `degrees`; one-way polar everywhere | 3.6, 3.7, 3.8, 3.9, 3.10, 4.1 (both) |
| 004 | events | `Event` | 2.5 (both), 3.10 |
| 005 | the projectile setup | `Setup`, `projectile` | 3.6 to 3.10 |
| 006 | Newton on the edge | `mass`, `newton` | 4.4, 4.5 (both) |
| 007 | the end | | the old copy deleted, version 0.2.0 |

**Rename before reshaping** (charter). 001 and 002 change names only:
every formula renamed back is the old one, and a formula that moves
stops the checkpoint, which reports it rather than adjusting anything.
003 to 006 change equations: each lists every formula it changes and
pins the new one. 3.10 is touched by 003, 004 and 005, in that order.

### 001 symbols and chapter 2

`symbols.py`, `axes.py`, `vectors.py` (`Vector` with its components
only), `particles.py`, `kinematics.py`, `notation.py`, and the
re-exports. The old copy stays.

- **Moves:** `ch02/examples/` `n04/main.py`, `n05/main.py`,
  `n05/main_step_by_step.py`, `n06/main.py`, `n07/main.py`;
  `ch02/exercises/` `n001`, `n003` (`main.py`, `main_two_steps.py`),
  `n005`, `n019`, `n021`, `n023`. 2.8 follows 2.7. Each uses
  `Particle(…)`, `m.states`, `m.edge(0, 1)` and `m.kinematics()`, with
  the same equations in the same order.
- **Checks:** all 66 rows of `tests/test_old_outputs.py`, chapter 2's
  renamed back with `old_name`, verbatim, with their numbers. Every
  `BOOK`. In the new `tests/test_physics.py`: `Var`'s identity (equal
  particles give equal symbols; `sp.Symbol("m0.pos.x")` differs;
  `Var("m0", "", "pos", "x")` differs though it prints alike; pickling
  round-trips); bad names and more than ten states raise `UsageError`;
  `Particle("m", 2, X).kinematics()` as the four strings above, and a
  three-state particle in the old order; `BookNotation` prints 2.4 (a)
  as `x1 = x0 + v0x*t1 + ax*t1**2/2`, and 2.5's `aPx` and `vP1x` with
  owners. In `tests/physics_misuse.py`: `.y` in an `X` model, `.x` in a
  `Y` model. 2.4 and 2.5 print the book form in `__main__`.

### 002 chapters 3 and 4, renamed

`vectors.py` gains `Vec`, the arithmetic, `.eq`, lone vectors and the
polar parts. `polar.py` has `from_polar` and `to_polar`.

- **Moves:** `ch03/examples/` `n06` to `n10`; `ch04/examples/` `n01`
  (`main.py`, `main_step_by_step.py`), `n04`, `n05` (`main.py`,
  `main_two_steps.py`). `magnitude_and_angle_equations(s)` becomes
  `*s.vel.from_polar(), *s.vel.to_polar()`. `make_point("n")` becomes
  `Vector("n", XY)`. `newtons_second_law([n, w, f], m, a)` becomes
  `(n + w + f).eq(a*m)`, and `superposition_equations(R, [F1, F2, F3])`
  becomes `R.eq(F1 + F2 + F3)`. 4.1's local `make_force`,
  `polar_to_components` and `components_to_polar` go. `m` stays a plain
  symbol.
- **`Formula`** takes an expression, in 3.8, 3.10 and
  `tests/test_examples.py`.
- **Checks:** all 66 rows verbatim, renamed back, and 3.10's
  show-that. Every `BOOK`. Tests for `+`, `-`, `*`, `sum()` and `.eq`,
  and the polar equations as strings. Misuses: `.mag` on an `X`
  vector, `XY + X`, `.eq` across dimensions.

### 003 polar and degrees

`polar.py` gains `degrees`, and the notation its symbols.

- **3.6:** `m1.pos.to_polar()` gives the distance (and the position's
  angle), `m1.vel.to_polar()` and `m1.vel.degrees()` the speed and
  direction. `dist`, `vel_mag`, `vel_angle` and `vel_angle_deg` go.
- **3.7:** `b0.vel.from_polar()` for the launch, `b1.vel.to_polar()`
  and `b1.vel.degrees()` for the speed and direction.
- **3.8:** `p0.vel.from_polar()` only, and its two by-hand
  eliminations go *(user)*.
- **3.9:** `b0.vel.from_polar()` only, all at once. `eliminating()`
  goes *(user)*, and 3.9 leaves `SLOW_EXAMPLES`.
- **3.10:** `d0.vel.from_polar()` only. Its eliminations follow, and
  3.10 leaves `SLOW_EXAMPLES` if it now imports in under 5 s.
- **4.1** (both): `R.degrees()` for `R_angle_deg`.
- **Checks:** every changed formula listed and pinned, every `BOOK`,
  3.10's show-that (pinned anew if its shape changes), and the times.

### 004 events

`events.py`, and the notation for events.

- **2.5** (both): `meet = Event("meet", m1, p1)`. `t_01` becomes
  `meet.t` and `dist` becomes `meet.pos.x`. Step by step still
  eliminates the six links (`m0.vel.x`, `m1.vel.x`, `m1.pos.x`,
  `p1.pos.x`, `m1.t`, `p1.t`).
- **3.10:** `hit = Event("hit", d1, m1)`, with `hit.equations(Y)` in
  the meeting and `hit.equations(X)` where the x's agree. `t` and `y`
  go.
- **Checks:** 2.5's formulas renamed back (`meet.t` → `t_01`,
  `meet.pos.x` → `dist`) verbatim, 10, 30 and 150. 3.10's show-that and
  its time. Tests of the equations, `axes=`, and an event of one state.
  Misuse: an event over states of different dimensions.

### 005 the projectile setup

`projectile.py`.

- **3.6:** the setup, with v1x derived. The by-hand
  `eliminate(m01.dt)` goes *(user)*, and v_x = 9.0 m/s becomes an
  `Answer`.
- **3.7, 3.8, 3.9:** the setup replaces their `a_y = -g`, `v0x = v1x`
  and `a_x = 0` lines.
- **3.10:** the setup for the dart, and for the monkey if it fits
  (its `m1.vel.x = 0` then comes from `v0x = v1x`).
- **Checks:** the formulas, listed and pinned, and every `BOOK`.
  Misuse: the setup on an `X` edge.

### 006 Newton on the edge

`newton.py`, and `Particle.mass`.

- **4.4:** `box = Particle("box", 2, XY)`, `box01.newton(F, n, w)`,
  `box01.a.y` known zero, and the want `box01.a.x`. `a` and `m` go.
- **4.5** (both): the bottle's forces in `X`. `b01.newton(n, w, f)`,
  and the link `a.x = b01.a.x` goes. In two steps, step 2 knows
  `b01.a.x` from step 1.
- **Checks:** 4.5's f_x is the old formula, renamed back with
  `b.mass` → `m`. The formulas, listed and pinned. Every `BOOK`.
  Misuse: an `XY` force on an `X` edge.

### 007 the end

- Delete `kinematics_states.py` and `newtons_laws.py`, and anything in
  the tests that only they needed. Update `physics/__init__.py`'s
  docstring and the package README's mention of the old code.
- Bump `pyproject.toml` to 0.2.0. The series README, the series map and
  002's README say the series is done.
- **Checks:** nothing imports the old copy; `uv run pytest`,
  `uv run pytest -m slow` and `uv run pyright` pass.
- **Merging** into `master` and tagging `v0.2.0` happen when the user
  chooses. Pushing is the user's call.

## How each increment lands

- **A checkpoint first,** `checkpoints/NNN-slug.md`, written from this
  page by the conversation that wrote it, once the previous increment
  has landed and the user has seen its review. A small increment can
  skip the full form. One that turns out too big is split.
- **One commit per increment,** on the branch
  `2026-11-08-physics-redesign`, with its code, tests and docs.
  `uv run pytest`, `uv run pytest -m slow` and `uv run pyright` pass.
  The series README records the commit and the status.
- **The `BOOK`s never change.** A changed answer means a bug.
- **The old repo stays as it is,** at `~/src/combine-equations.py`.

## SymPy to watch

- **Print order follows class, then name.** SymPy sorts by class name
  first, and `Var` isn't one of its own classes. So `Var`s and plain
  symbols sort apart, and the new names sort differently from the old.
  Renaming back restores the old order, and the prototype found no
  formula that moved.
- **`_hashable_content` holds strings only,** in fixed positions. A
  dataclass or a number there makes SymPy's sort raise `TypeError`.
- **`sp.Symbol.__xnew__`** skips the name cache. Never call
  `sp.Symbol(name)` for a `Var`.
- **`Float(43) == 43` is `False`** in SymPy 1.14. Compare numbers by
  value.
- **`sp.deg(x)` is `180*x/pi`,** the same expression as the old
  `x*180/pi`.

## What's next

Found while writing this spec, for a later series:

- **Labels for generated equations.** `System.add` could take labeled
  equations, so the physics layer could label `(2.2 m01 x)` and
  `eliminate(using=…)` could name them.
- **`show(symbol=…)`,** so an example can print the book form with
  `show()`.
- **`clear_zero_denominators`** has no example left that needs it,
  once 3.6 uses the projectile setup.

## Not in this spec

From the charter: changes to the core; 3.8's 90° and 45°; the GUIs,
LaTeX and Jupyter, and vector equations displayed as vectors; other
textbooks and new chapters; the derive-all search; SymPy assumptions.

Also out, because no example needs them: a z axis and 3D; edges
between states that aren't consecutive; more than ten states; two-way
polar as one helper; helpers for weight and relative velocity.
