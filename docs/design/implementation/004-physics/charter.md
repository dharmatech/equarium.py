# 004 physics: charter

The handoff for redesigning equarium's physics layer in a new
conversation. It says what the old physics code does, what the examples
need, what is already decided, and what the spec has to settle.

If you've been told to read this file, this is the whole assignment.
Read it, settle the open questions with the user, write `spec.md` in
this folder, and stop.

## The goal

equarium's core is done (series 002). The old physics code from
[combine-equations.py](https://github.com/dharmatech/combine-equations.py)
runs on it, copied with typing-only fixes, and every ported University
Physics example checks the book's answers. This series redesigns that
physics layer: the objects an example builds its equations from. The
core doesn't change.

What the redesign is for:

- a symbol that knows what it means: its owner, state or edge, quantity
  and component;
- one naming rule;
- the dimension set once, when the model is made;
- polar form, events, the projectile setup and Newton's laws as small
  helpers, instead of code repeated in each example;
- laws written once, as vector equations.

At the end, every example that used the old physics code uses the new
one, with the same book answers, and the old copy is gone.

## Where the work happens

- **Tag `v0.1.0`,** annotated, on `3370e5d` (2026-11-08): the core and
  the old physics code, before this series. `pyproject.toml` already
  says `version = "0.1.0"`. The tag is local until the user pushes it.
- **Branch `2026-11-08-physics-redesign`,** from the tag. Every commit
  of this series goes there: this charter, the spec, each checkpoint
  and each increment. `master` stays at the tag until the series
  merges, so `git diff v0.1.0` shows the whole redesign. The branch
  name follows the user's convention: a date stamp, then the subject.
- **The series ends** by bumping `pyproject.toml` to 0.2.0, merging
  into `master`, and tagging `v0.2.0`, when the user chooses. Pushing
  is always the user's call.

## Scope

- **Every feature names an example,** as in 002. The physics layer
  grows only when a ported example needs it. The "Driven by" column
  below gives each lesson's examples.
- **The examples that use the old physics code.** 22 modules import
  it, and 2.8 imports 2.7's base:

  | Chapter | Modules, under `examples/up_15e/` |
  |---|---|
  | 2 | `ch02/examples/`: `n04/main.py`, `n05/main.py`, `n05/main_step_by_step.py`, `n06/main.py`, `n07/main.py`; `ch02/exercises/`: `n001`, `n003` (`main.py`, `main_two_steps.py`), `n005`, `n019`, `n021`, `n023` |
  | 3 | `ch03/examples/`: `n06`, `n07`, `n08`, `n09`, `n10` |
  | 4 | `ch04/examples/`: `n01` (`main.py`, `main_step_by_step.py`), `n04`, `n05` (`main.py`, `main_two_steps.py`) |

  The written-out modules don't use it, and stay as they are:
  `main_handwritten.py` for 2.4 and 2.5, 2.5's
  `main_handwritten_step_by_step.py`, Table 2.5, 3.13 and 4.7. 3.13
  and 4.7 move onto the new layer only if the spec gives them helpers
  (relative velocity, weight).
- **Keep the alternative styles.** Each version keeps its style: all at
  once, step by step, two steps, eliminating. A helper can make a
  version's step unnecessary. Then the spec settles with the user
  whether the version keeps its step or changes style.
- **No new chapters.** University Physics chapters 2 to 4, the examples
  already ported.

## The order of the work

"Never change two layers at once" held between the core and the
physics code. Inside this series it becomes **rename before
reshaping**:

1. **Rename.** The new symbols and the new model come in, and the
   examples move to them with the **same equations**. Each formula in
   `tests/test_old_outputs.py`, with the new symbols renamed back to
   the old names, must come back exactly as before. A formula that
   moves stops the checkpoint, which reports it rather than adjusting
   anything. One known risk is the core's `eliminating()` order, which
   breaks ties by name (`strategies.py`). The prototype's 3.9 came back
   verbatim, though.
2. **Reshape.** The helpers that change which equations an example
   adds: polar, events, the projectile setup, Newton's acceleration as
   the edge's, vector equations. Each checkpoint lists every formula it
   changes and pins the new one, as 007 listed its expected
   differences.
3. **Remove** the old copy, `src/equarium/physics/kinematics_states.py`
   and `newtons_laws.py`. The tag and the old repo keep it.

The `BOOK`s never change. A changed answer means a bug.

## Where things are

**The core,** `src/equarium/`. It takes any `sp.Symbol`. Its display
calls a hook for every symbol, `(symbol, role) -> str`, which
`render`, `render_solution` and `render_history` in `display.py` take
as `symbol=`. The default prints the name, colored by role. Its spec,
[002-core/spec.md](../002-core/spec.md), has the decisions.

**The old physics code,** `src/equarium/physics/`:

| Module | What it has |
|---|---|
| `kinematics_states.py` | `Point3` (x, y, z, and optional `mag` and `angle`), `make_point`, `State` (pos, vel, t), `EdgeVars` (dt, a, optional v_av), `StatesModel`, `make_states_model(prefix, n_states)`, `kinematics_fundamental(model, axes=...)` (Δt and the book's 2.2, 2.7 and 2.10, per edge and axis), `magnitude_and_angle_equations(state)` (the velocity's two-way polar), and helpers no kept example calls: `axis_zero_constraints`, `axis_zero_substitution_map`, `constant_velocity_constraints`, `link_same_time`, `link_same_position` |
| `newtons_laws.py` | `superposition_equations(R, forces)` and `newtons_second_law(forces, mass, acceleration)`, both for x and y only |

What the examples call: `make_states_model` and
`kinematics_fundamental` 24 times each, `make_point` 12,
`newtons_second_law` 3, `superposition_equations` 2,
`magnitude_and_angle_equations` 2, and `Point3` once, in 4.1's local
`make_force`.

**The examples and their checks:**

- `examples/answers.py`: `Answer` (a number the book prints) and
  `Formula` (a formula it prints, as a string read with `parse_expr`).
  These aren't the core, so they may change.
- `tests/test_examples.py`: every example's `BOOK`.
- `tests/test_old_outputs.py`: the old scripts' formulas, verbatim, in
  the old names, and `OLD_GIVENS` for the three ports that use the
  book's givens.
- `tests/test_physics.py`: the old code's equations as strings, and a
  check that the core doesn't import `equarium.physics`.
- `tests/slow_examples.py`: 3.9 (about 6 s) and 3.10 (about 9 s), both
  slow because of two-way polar.
- The core's own tests use the written-out examples, so this series
  doesn't touch them.

The layout is one folder per problem, from series 003
([003-example-layout](../003-example-layout/README.md)).

**The starting point:** 263 tests pass, with 8 slow ones deselected.
`uv run pytest -m slow` passes all 8, and `uv run pyright` reports 0
errors.

## What the old physics code taught

| Lesson | Driven by |
|---|---|
| The split between a state (an instant: position, velocity, time) and an edge (an interval: Δt, acceleration, average velocity) works. Generating 2.2, 2.7 and 2.10 from the model and solving all at once gives the book's derived equations. Keep it. | 2.4, every kinematics example |
| The dimension is chosen at each call (`axes=("x",)`, `["x", "y"]`), and every model has x, y and z. A 1D example can still reach `m0.pos.y`. | every `kinematics_fundamental` call |
| Two naming orders. States put the owner first (`m_0_v_x`), and edges put it last (`a_x_m_0_1`, `dt_m_0_1`). Two models with the same prefix collide silently. | `make_states_model` |
| `mag` and `angle` are optional fields of `Point3`. `make_states_model` sets them for velocities only and `make_point` for any vector, so the ports narrow them with asserts. A position has no magnitude. | 3.6, 3.9, 3.10, 4.1 |
| Two-way polar (`magnitude_and_angle_equations`) makes all at once fail and elimination slow. One-way conversions fix it. 4.1 writes its own one-way helpers, and 3.6 and 3.7 write the speed and angle by hand. | 3.6, 3.7, 3.9, 3.10, 4.1 |
| Degrees by hand: `angle*180/pi`, `deg(angle)`, and `sp.rad(53.1)` for a given. | 3.6, 3.7, 3.9, 4.1 |
| The projectile setup is repeated, with small differences: zero x0, y0, t0 and a_x, `a_y = -g`, `v0x = v1x`. 3.6 gives both velocities instead of `v0x = v1x`, and 3.9 starts at y0 = 8.0 m and ends at y1 = 0. | 3.6 to 3.10 |
| Links are written by hand through new symbols: 2.5's `dist = m1.x`, `dist = p1.x`, `t = m1.t`, `t = p1.t`; 3.10's `d1.t = t`, `m1.t = t`, `d1.y = y`, `m1.y = y`. `link_same_time` was never used, and nothing covers positions. | 2.5, 3.10 |
| Newton's acceleration is a separate `make_point("a")`, linked to the kinematics edge's by hand: `Eq(a.x, b01.a.x)`. | 4.5 |
| Newton's laws cover x and y only, whatever the model's dimension. | 4.1, 4.4, 4.5 |
| Weight is written by hand, `w = m*g`, and relative velocity is the book's 3.32 and 3.33 written out. | 4.7, 3.13 |
| 3.6 finds no roots from `0 = (-m_0_v_x + m_1_v_x)/dt_m_0_1` with both velocities known. Its port eliminates `m01.dt` by hand, since the core leaves out `clear_zero_denominators`. | 3.6 |
| Meaning lives only in names. The old display recolored by renaming symbols, and the old GUI parsed names with regular expressions. | the display, the GUIs |

The catalog's "Recommendations for 007" → "The physics code"
([catalog.md](../001-example-catalog/catalog.md#the-physics-code)) has
the same list, with 3.8's maximizing, which this series leaves out.

## What the prototype showed

A scratch prototype on the core, unchanged (2026-11-08):

- **A structured symbol can be a subclass of `sp.Symbol`.** Its
  identity is its structure, and its name is the access path:
  `m0.pos.x`. This version passes pyright and pickles:

  ```python
  from typing import Any, Self, SupportsIndex

  import sympy as sp

  class Q(sp.Symbol):
      owner: str
      owner_key: str       # tells two owners with the same name apart
      where: str           # a state, "0", or an edge, "01"
      path: tuple[str, ...]  # the rest of the access path: ("pos", "x")

      def __new__(cls, owner: str, owner_key: str, where: str, *path: str) -> Self:
          obj = sp.Symbol.__xnew__(cls, ".".join((owner + where, *path)))  # no name cache
          obj.owner, obj.owner_key, obj.where, obj.path = owner, owner_key, where, path
          return obj

      def _hashable_content(self) -> tuple[str, ...]:
          return (self.name, self.owner_key, self.where, *self.path)

      def __reduce_ex__(self, protocol: SupportsIndex) -> tuple[Any, ...]:
          return (type(self), (self.owner, self.owner_key, self.where, *self.path))
  ```

- **The core takes it with no change.** 2.4 gives 43, 23 and 55.
  `eliminate`, `isolate`, `simplify`, `subs`, `sp.solve`'s roots and
  pickling all keep the subclass. A plain `Symbol("m0.pos.x")` is a
  different symbol, and so is another owner's `m0.pos.x`, though both
  print the same.
- **The identity must be plain strings or numbers in fixed
  positions.** SymPy sorts terms by comparing `_hashable_content`
  element by element. A dataclass there raises `TypeError`. The
  stubs type it `tuple[str, ...]`, and pyright flags anything else. It
  also flags overriding `__getnewargs_ex__`, which `__reduce_ex__`
  avoids.
- **Book notation needs only a hook.** Through the core's display hook,
  2.4 (a) prints `x1 = x0 + v0x*t1 + ax*t1**2/2`. Without the hook, it
  prints `m1.pos.x = m0.pos.x + m0.vel.x*m1.t + m01.a.x*m1.t**2/2`.
- **Renamed back, the old formulas come back verbatim.** That holds for
  2.4's three, and for 3.9's two roots through two-way polar and
  `eliminating()`. SymPy prints terms in the order of the names, so the
  new names print in a new order, and renaming back restores the old
  one.
- **The same speed.** 3.9 takes 1.6 s all at once with one-way polar,
  and 6.4 s with two-way and `eliminating()`. Before, those were 1.2 s
  and about 6 s.
- **SymPy 1.14:** `Float(43) == 43` is `False`. Compare numbers by
  value.

## What is decided

From the discussion with the user, 2026-11-08:

1. **Structured symbols are a `sp.Symbol` subclass,** whose identity is
   its structure. There is no side table. **A symbol's name is its
   access path:** `m0.pos.x`, `m01.a.x`, `m01.dt`, `m1.t`. That is the
   one naming rule. The symbols carry no SymPy assumptions, such as
   t > 0, so every root stays, as 2.8 teaches.
2. **The core doesn't change in this series.** Anything found goes to
   "What's next" in this series' README, as 002 did. That includes
   `clear_zero_denominators`, so 3.6 keeps its by-hand step. A helper
   that gives knowns as well as equations returns them separately, and
   the example adds both: `.add(*eqs).known(knowns)`.
3. **Rename before reshaping,** as in "The order of the work".
4. **The ports change in place.** Each `main.py` moves to the new
   physics code, and git and the tag keep the old version. The old
   physics code isn't a solving style, so no version keeps it. The old
   copy is deleted at the end of the series. The written-out versions
   don't use it, and stay as they are.
5. **Events own their symbols and write the links as equations:**
   `meet.t`, with `m1.t = meet.t` and `p1.t = meet.t`. 2.5's step by
   step then still has links to eliminate. Sharing one symbol between
   the states would leave nothing to eliminate.
6. **Book notation is plain text,** through the core's display hook.
   The debug form is the name itself and needs no hook. LaTeX and
   Jupyter wait for the GUIs.
7. **Laws are written as vector equations:** ΣF = m a and
   R = F1 + F2 + F3, written once and expanded per axis of the model.
   They still display one component per line, because grouping
   equations by vector would change the core's display.
8. **From the first design discussion,** kept in 002's charter: keep
   the `m0.pos.x` access, the split between states and edges, and
   generating equations from the model. Set the dimension when the
   model is made. Polar is an add-on, with one-way conversions.
9. **The tag, the branch and the version,** as in "Where the work
   happens".

## The user's preferences

- **Dot syntax and objects,** as in `m0.pos.x`: methods on objects,
  not generic functions that lose the dots.
- **Static typing.** Typed code, frozen dataclasses, pyright clean
  (standard mode).
- **Small, focused modules,** in layers. The core knows nothing of
  physics.
- **Think as if in Haskell or Scala.** Prefer structured values with
  structural equality to side tables. Rendering is a function separate
  from the value.
- **Plain, short sentences** in the docs.
- **The publisher's figures never go into the repo.** A module names
  its figure in its docstring.

## A sketch: 2.5

From the discussion. The names are placeholders for the spec.

```python
m = Particle("m", states=2, axes="x")   # the motorist
p = Particle("p", states=2, axes="x")   # the officer
m0, m1 = m.states
p0, p1 = p.states
p01 = p.edge(0, 1)
meet = Event("meet", m1, p1)            # the same time and place

setup = (
    System()
    .add(*m.kinematics(), *p.kinematics())    # Δt, 2.2, 2.7, 2.10 per edge, x only
    .add(sp.Eq(m0.vel.x, m_v), sp.Eq(m1.vel.x, m_v))
    .add(*meet.equations())                   # m1.t = meet.t, p1.t = meet.t, m1.pos.x = meet.pos.x, …
    .known({m0.t: 0, p0.t: 0, m0.pos.x: 0, p0.pos.x: 0, p0.vel.x: 0})
    .known(m_v, 15).known(p01.a.x, 3)
    .want(meet.t, p1.vel.x, meet.pos.x)
)
# meet.t = 2*m_v/p01.a.x   10
```

## Design questions for the spec

1. **The types and their names.** What an owner is: one type for a
   moving particle and for a body with forces (4.5 needs both), or two.
   `Particle`, `Body` or another name. Avoid `System`, which is the
   core's, and `Quantity`, which is `sympy.physics.units`'s. How states
   and edges are reached: `m0, m1 = m.states`, and `m.edge(0, 1)` or
   `m.edges[0]`. The edge's name, `m01`, gets ambiguous past ten
   states.
2. **The structured symbol.** Its fields and their types, starting from
   the prototype's. Whether a lone vector (a force, `F1.x`) and a
   scalar the example names (`m`, `g`, `D`, `m_v`) are structured
   symbols too, or plain ones.
3. **The dimension.** Set when the model is made (`axes="x"`, `"xy"`).
   What `m0.pos.z` does in a 1D model, and whether pyright can see it.
4. **The naming rule's details.** Edge quantities (`m01.a.x`, `m01.dt`,
   `m01.v_av.x`), polar parts (`m0.vel.mag`, `m0.vel.angle`), an
   event's symbols (`meet.t`, `meet.pos.x`). What happens with two
   owners of the same name in one problem: they're different symbols
   that print alike.
5. **Equation labels.** Whether the physics layer labels its equations
   with the book's numbers, such as `(2.2 m01 x)`, so that
   `eliminate(using=...)` and the origins can name them. Today they are
   numbered `(1)`, `(2)`, …, and 3.10 picks `dart.equation("8")` by
   number.
6. **The polar add-on.** One-way in each direction, two-way, degrees,
   and a position's magnitude (3.6's distance). Which examples keep
   two-way: 3.9 and 3.10 use it today. With one-way, 3.9 would solve
   all at once, and 3.10 would import faster than its 9 s. Whether 3.9
   keeps `eliminating()` as its style, since `tests/test_strategies.py`
   already keeps that lesson, written out.
7. **Events.** What an event is: two states at the same time, the same
   place, or both, on chosen axes. 3.10 links t and y, but not x. Which
   symbols it owns, and its equations.
8. **The projectile setup.** Its equations and its knowns: zero a_x,
   `a_y = -g`, and which of the zero positions and times. Whether it
   gives `v0x = v1x`, as the ports do. Whether an axis with zero
   acceleration should get other equations, which would spare 3.6 its
   by-hand step.
9. **Newton's laws.** ΣF = m a over the model's axes, not x and y only.
   The body's acceleration over an edge as Newton's, with no link
   equation (4.5). Superposition (4.1). Weight (4.7).
10. **Vector equations.** A small vector type, with +, −, scalar ×, and
    one equation per axis, or `sympy.physics.vector` (which 3.13's
    unported v002 used). How a vector equation's components are
    labeled.
11. **Relative velocity.** A helper for 3.32 and 3.33, or 3.13 stays
    written out.
12. **The book-notation hook.** Which notation: the book's x, v_x, a_x,
    x_0, v_0x, Δt, with subscripts for several bodies, like 2.5's x_M
    and x_P. ASCII or Unicode. How a hook tells owners apart.
13. **The tests.** How `tests/test_old_outputs.py` renames back: a map
    in the tests from each new symbol to its old name, so the strings
    stay verbatim. What replaces `tests/test_physics.py`'s check of the
    old equations. `Formula`'s strings (3.8, 3.10), which `parse_expr`
    can't read with dotted names: an expression instead of a string, or
    a parse with the solution's symbols.
14. **The package.** Small modules in layers under
    `src/equarium/physics/` (for example symbols, vectors, the model,
    kinematics, polar, events, Newton, notation), and where the old
    copy sits until it's deleted.

## Candidate increments

For the spec to choose from, reorder, merge or split. Each one lands
with tests.

1. **The symbols and the model, chapter 2.** The structured symbol,
   states and edges, kinematics with the dimension set once, the naming
   rule, and the book-notation hook. Chapter 2's 12 modules move over,
   with the same equations.
2. **Chapters 3 and 4, renamed.** The 10 modules of chapters 3 and 4.
   `make_point`, `Point3`, `magnitude_and_angle_equations` and 4.1's
   local helpers become the new vectors, with the same equations.
3. **Polar and degrees.** 3.6, 3.7, 3.9, 3.10 and 4.1.
4. **Events.** 2.5 (both versions) and 3.10.
5. **The projectile setup.** 3.6 to 3.10.
6. **Vector equations and Newton.** 4.1, 4.4 and 4.5, and weight in 4.7.
   Relative velocity for 3.13, if the spec keeps it.
7. **The end.** Delete the old copy, bump the version to 0.2.0, update
   the docs, and merge into `master` when the user chooses.

## How to work

- **Design with code first.** Before settling names, sketch how 2.4,
  2.5, 3.10 and 4.5 read on the new layer. 3.10 has two owners and an
  event, and 4.5 has kinematics and Newton on one body. The sketches
  can go in the spec.
- **Prototype first,** as 002's spec did. Rebuild the symbol from the
  excerpt above, and extend it to 3.10 and 4.5.
- **Then increments, as checkpoints,** as in 002. `spec.md` lists the
  agreed increments, and `checkpoints/NNN-slug.md` hands them out one
  at a time. Each lands as its own commit on the branch, with
  `uv run pytest`, `uv run pytest -m slow` and `uv run pyright`
  passing, and the series README records it. The conversation that
  writes the spec manages the checkpoints and reviews each commit, and
  the user sees each review before the next one starts.
- **Scale to the work.** An increment that turns out small can skip the
  full checkpoint form. One that turns out too big gets split.
- **Docs:** this series' [README](README.md) for status and commits,
  and the [series map](../README.md).
- **The old repo stays as it is,** at `~/src/combine-equations.py`.

## Not in this series

- **Changes to the core,** `clear_zero_denominators` among them.
- **3.8's 90° and 45°,** which need maximizing over a parameter.
- **The GUIs,** LaTeX and Jupyter rendering, and displaying vector
  equations as vectors.
- **Other textbooks** and new chapters.
- **The derive-all search** of the old kinematic-equations 005.
- **SymPy assumptions** on the structured symbols.

## References

- [002's charter](../002-core/charter.md), [spec](../002-core/spec.md)
  and [README](../002-core/README.md), and its "What's next".
- [The example catalog](../001-example-catalog/catalog.md): each
  problem, the book's answers, the old scripts' formulas, and
  "Recommendations for 007".
- [003's README](../003-example-layout/README.md): the layout, and the
  old module names against the new.
- The old library: `~/src/combine-equations.py`,
  `src/combine_equations/kinematics_states.py` and `newtons_laws.py`.
- The textbook: `~/journal/2026-11-06-equations/up-15e.pdf`, University
  Physics with Modern Physics, 15th ed., 1596 pages. Don't read it
  whole. `mutool show up-15e.pdf outline` gives the chapters' pages
  (chapter 2 is PDF pages 64–95, chapter 3 starts at 96, chapter 4 at
  130), and `pdftotext -f A -l B -raw` keeps fractions readable. The
  book's notation for the hook comes from its own pages.
- The docs convention: `~/journal/2026-10-20-niva/mpl-niva/docs/design/implementation/`
  (`008-simplifier`), and the roles in
  `~/journal/2026-09-02-aloe-racket/docs/workflow.md`.

## First steps in the new conversation

1. Check that the folder is on the branch:
   `git switch 2026-11-08-physics-redesign`.
2. Read this charter, the "Decisions" of 002's spec, the catalog's "The
   physics code", then `src/equarium/physics/` and the examples in
   "Scope".
3. Run `uv run pytest` and `uv run pyright` to see the starting point.
4. Rebuild the prototype and extend it to 3.10 and 4.5. Sketch 2.4,
   2.5, 3.10 and 4.5 on a proposed layer, and go through the design
   questions with the user.
5. Write `spec.md`: the decisions, the increments with their checks,
   and how each increment lands. Then stop. The first checkpoint is
   written once the user has agreed the spec.
