# 002 core: spec

**Status:** Agreed with the user (2026-11-07). The decisions marked
*(user)* were settled with the user. The rest were proposed and left
standing. No increment has started.

What equarium's core will be, in seven increments, one checkpoint
each. The [charter](charter.md) has the background, the lessons from
the old library and the references. This page is what was decided.

## What the prototype showed

The design came from reading the old library and the reference
examples, from running 2.4 v4-001 with the charter's shim (43, 23, 55),
and from a scratch prototype in equarium's venv (SymPy 1.14) with
hand-written equations. The facts the increments rely on:

- **All at once works.** The knowns stay symbols, the unknowns linked
  to the wants go to one `sp.solve(..., dict=True)`, and the number
  comes from substituting the knowns at the end. With zeros substituted
  first: 2.4 gives 43, 23 and 55 with the book's formulas
  (`x1 = a*t1**2/2 + t1*v0 + x0`). 2.5's three wants (t, the officer's
  speed, dist) solve **together in one call**, with one root: 10, 30
  and 150. 2.7 gives 10.1 and 5.2, then ±11.27 and 11.48. For 2.8,
  solving t and v together keeps each root's t and v paired: 3.36 s
  with −17.97 m/s.
- **The old display reorders terms.** `dt = -m_0_t + m_1_t` prints as
  `m_1_t - m_0_t` once `m_1_t` is colored, because the color is put
  into the symbol's name and names decide SymPy's print order. A
  `StrPrinter` subclass that colors in `_print_Symbol` keeps the order.
- **Simplifying a whole `Eq` rewrites it.** In 2.5 the old elimination
  turned `v_av = v0/2 + v1/2` into `v0 = -v1 + 2*v_av`.
- **Units:** `convert_to(number, [m, s])` turns 2.23's
  `22.05*kilometer**2*second**2/(hour**2*meter)` into 1.70 m. With
  `[h, km]` the same call keeps 2.3's answer in hours. `0*m` is already
  `0`, and `3.36*second > 0` evaluates to `True`.
- **3.9:** with the two-way polar equations (`magnitude_and_angle_equations`),
  all at once gets **no roots**, and the old elimination attempts find
  9.16 m (and −15.7 m) in 9 s. With the one-way equations (polar to
  components only), all at once finds them in 1.2 s.
- **3.10's "show that"** ends with the stated condition, not an empty
  system. The old v1-001 script prints
  `d_0_v_mag*sin(d_0_v_angle) = d_0_v_mag*D*sin(d_0_v_angle)/d_1_x`,
  which holds exactly when the dart reaches x = D. In one combined
  system, the prototype gets the same equation, and gets an empty
  system once `d1x = D` is added. That only works if the monkey's x
  is eliminated first. Otherwise the automatic choice uses the
  monkey's x equation to eliminate t.

## Decisions

### The state: `System`

- **`System`, immutable.** A frozen dataclass with `equations`,
  `knowns` and `wants`, plus the step that made it and the system it
  was made from. Every method returns a new `System`, so a part of a
  problem is a branch from a shared base. The previous systems are
  the history: the GUI's "state after each step" and a step-by-step
  printout come from walking back.
- **Why `System`** *(user)*: it is a system of equations
  with its knowns and wants at every stage, from a base with no wants
  to what's left after six eliminations. The old library already used
  the word (`solve_system`). It avoids the book's own categories
  (Examples, Exercises, Problems) and the physics layer's `State` and
  `StatesModel`. The misuse error is `UsageError`, because Python
  already has a built-in `SystemError`. In chapters 4 and 5, "system"
  is also a physics term (what a free-body diagram is drawn for). The
  physics redesign will have to name around it.
- **Equality is content.** Two systems are equal when their
  equations (label and `Eq`), knowns and wants are. The history and
  the equations' origins don't take part, so two derivations of the
  same system compare equal. No field can change after construction.
  Mappings are read-only, and hashing isn't required.
- **Labeled equations, with an origin tree** *(user)*. An `Equation` is
  a label, a plain `sp.Eq` and an origin. The label is given
  (`"2.2"`) or automatic (`"1"`, `"2"`, … from a counter on the
  system, never reused after an equation is removed). A duplicate
  label is an error. An equation rewritten by an operation keeps its
  label, and its origin records how it was made, as a structured
  value: `Given`, or `Derived(op, symbol, parents)`, where the parents
  are the equations it came from, with their own origins. It renders
  as `(2.7) ← (2.7) + (2.2), eliminate dt`, and walking it gives
  kinematic-equations 005's ancestors.
- **Knowns** map a symbol to a value, or to nothing for a symbol that
  is known but has no number. That replaces 3.10's
  `values[d0.vel.mag] = d0.vel.mag`. A value is a number, possibly with
  units (`105*km/h`), and has no free symbols. A relationship between
  symbols is an equation, and `known` refuses one.
- **Several wants at once,** solved together. A symbol can't be a
  known and a want at the same time.
- **Steps are structured.** Each records its operation and arguments
  (adding equations, setting or forgetting knowns, setting wants,
  eliminating, isolating), plus what it changed: the replacement
  found, the labels it rewrote, and the labels its cleanup dropped.
  The description ("eliminate dt using (2.2): into (2.7)") is rendered
  from the step, never stored.

### Values or equations: `eliminate_zeros` *(user)*

**Numbers are knowns, and relationships are equations.** A zero is a
known like any other number, written `known(t0, 0)` and never
`Eq(t0, 0)`. A known stays a symbol in the formulas, and its value goes
in only for the number.

**`eliminate_zeros()` takes the zeros out, in one explicit step,** as
the old `eliminate_zero_eqs` did. It substitutes every known that is
zero at that moment into every equation, then cleans up. Zero means
SymPy's zero, so `0`, `0.0` and `0*m` all count. The step is recorded,
and each equation it rewrites gets an origin that says `t0 = 0`.

- **Layers.** `show()` before the step shows the full symbolic set,
  with the zeros listed among the knowns. After the step comes the
  simpler set the examples work from, as in the old 2.5, 2.7, 3.9 and
  3.10.
- **It's a step, not a standing rule.** A zero set afterwards stays a
  symbol until the number, and an equation added afterwards is left as
  written. Calling the step again substitutes whatever is zero by then.
  That brings back the old control. In 2.7, t0 and y0
  drop out of the base, while part (c) sets v1 = 0 afterwards and keeps
  it in `y1 = (v1**2 - v0**2)/(2*a)`. An example that never calls it,
  like 4.5, keeps the book's general formula
  `a = (v**2 - v0**2)/(2*(x - x0))`.
- **A substituted known is fixed.** Forgetting it, or giving it another
  value, raises `UsageError`, because the symbol is gone from the
  equations. Branch from before the step instead.
- **`subs` and cleanup only,** never `simplify`, so the equations keep
  their shape. An equation that becomes `0 = 0` is dropped. With no
  zero knowns, the step changes nothing.
- **Why only zeros.** Substituting a zero early loses nothing. It's
  usually a setup choice (the origin, the clock), and it removes terms.
  Substituting any other number early would put numbers into the
  formulas. No example needs a general substitution of knowns, so the
  core doesn't have one.
- **Why not automatic.** The core has no physics, so it can't tell a
  setup zero (t0) from a physical one (v1 = 0 at the top). The first
  draft of this spec substituted every zero automatically. That changed
  the formulas of every old example that kept a zero as a value (2.3,
  2.7 (c), 2.23, 4.5), and lost the book's general formula in 4.5. It
  also meant increment 007 could compare only numbers with the old
  scripts, not formulas.

### The operations

Methods on `System`, for dot syntax. The work lives in small modules
of plain functions, and each method is a one-line delegation.

| Method | Does |
|---|---|
| `add(*eqs, label=None)` | Adds equations. A label is allowed only with one equation. `True` is dropped, and `False` is a contradiction. |
| `known(sym, value)`, `known(sym)`, `known({sym: value, …})` | Adds or replaces knowns. |
| `eliminate_zeros()` | Substitutes the zero knowns into the equations (above). |
| `forget(*syms)` | Removes knowns. |
| `want(*syms)` | Replaces the wants. |
| `eliminate(*syms, using=None)` | Eliminates each symbol in turn (below). `using` names an equation, and is allowed only with one symbol. |
| `isolate(sym, label)` | Rewrites that equation as `sym = …`. |
| `analyze()` | Returns an `Analysis` (below). |
| `solve(*wants, strategy=all_at_once)` | Returns a `Solution`. Wants given here replace the system's wants first. |
| `show(origins=False)`, `show_history()` | Print through the display (below). |

**Eliminate,** the old "combine equations": solve one equation for the
symbol, substitute the result into every other equation, remove that
equation, then clean up.

- With `using`, that equation must give exactly one root for the
  symbol, and the root must not contain the symbol.
- Without `using`, the candidates are the equations that give exactly
  one such root. The simplest root by `count_ops` wins, as in the old
  `eliminate_variable_subst`, and ties go by label order. An equation
  that gives several roots is never used by itself, because the old
  silent choice of a sign is how a wrong answer would slip in.
- Eliminating a known or a want is an error.
- Each rewritten equation gets the origin
  `Derived("eliminate", sym, (itself, source))`.

**Isolate** requires exactly one root. Its origin is
`Derived("isolate", sym, (itself,))`.

**Cleanup** runs inside every rewrite, and its drops are recorded in
that step. It isn't a public method, because no example calls it
directly. It drops an equation that is `True`, or whose `lhs - rhs`
simplifies to 0. It raises `Contradiction` for `False`, or for a
difference that is a nonzero constant.

**Simplifying.** After eliminate and isolate, each side is simplified
separately with `safe_simplify`, never the `Eq` as a whole.
`eliminate_zeros` uses only `subs`. Display and solve never simplify.

**Failures are typed exceptions** *(user)*. `EliminationError`,
`IsolationError`, `Contradiction` and `UsageError` (misuse: a
duplicate or missing label, a known that is also a want, forgetting or
changing a known that `eliminate_zeros` substituted, solving with no
wants, asking one root of several) all share a base, `EquariumError`.
Each carries the symbol, the labels and the reason, so a GUI can show
it. Chains stay plain:
`p.eliminate(a).eliminate(b)`.

### Analysis

`Analysis` is a frozen value: the knowns, the wants, the **connected
unknowns** (the unknowns linked to the wants through the equations,
wants included, as in the old `connected_unknowns`), the other
unknowns, the labels of the equations **ready to solve** (exactly one
unknown), and the counts of connected unknowns and of the equations
that contain them. The display and `all_at_once` both use it. A
symbol's **role** is `KNOWN`, `WANT` or `UNKNOWN`.

### Solving

- **`Solution`** is a frozen value: the system it was solved from
  (with its history), the roots, the elapsed time in seconds, and the
  reason when SymPy found none.
- **`Root`** has a formula and a number for every want. The formula is
  SymPy's answer in terms of the knowns. The number is `sp.N` of the
  formula with the knowns' values substituted. Units stay as they
  come, and a known with no number stays a symbol.
- **Access:** `root.formula(x)`, `root.number(x)`, and on the solution
  `solution.formula(x)` and `solution.number(x)`, which need exactly
  one root and otherwise raise `UsageError` naming the count.
- **Filter:** `solution.where(t1 > 0)` keeps the roots for which a
  plain SymPy relation holds, once the root's numbers and the knowns
  are substituted. `&` and `|` combine relations. A relation that
  doesn't reduce to `True` or `False` is a `UsageError`.
- **Units:** `solution.in_units(m, s)` converts every number with
  `convert_to(number, [m, s])` and returns a new `Solution`.
- **No roots is a result.** If SymPy returns none, or raises
  `NotImplementedError`, the solution has no roots and keeps the
  reason. Strategies treat that as "try again". Any other exception
  propagates, since it means a bug.

### Strategies

A strategy is a function `System -> Solution`.

- **`all_at_once`,** the default: analyze, take the equations that
  contain a connected unknown, and run one `sp.solve` over the
  connected unknowns.
- **`eliminating(max_eliminations=10)`** returns a strategy, the old
  version 2. It runs `all_at_once`, and if that finds no roots it
  eliminates one connected unknown (not a want) and tries again. The
  old order picks the candidate: symbols outside the want's equations
  first, then fewer occurrences, then name. The eliminations are real
  steps, so `solution.system.show_history()` lists them. The elapsed
  time covers the whole run.
- **By hand** isn't a strategy object. It's the operations followed by
  `solve()`, as in 2.5 v4-002, 3.10 and 4.1 v1-006.
- **Two steps** (2.3 v000, 4.5 v000) is two systems. The second takes
  the first's answer as a known, through `solution.number(x)`.

All styles are the same `System` with a different strategy or
different steps, as the charter asks.

### The display

- **Rendering is separate from the value:** `render(system, symbol=…)
  -> str`, `render(solution, …)` and `render_history(system, …)` in
  `display.py`. `show()` and `show_history()` print what those return.
- **The hook** is a function `(symbol, role) -> str`, and the core
  never reads meaning into a symbol's name. The default, the terminal
  view, prints the name in green for a known, in red for a want, and
  plain otherwise, with ANSI codes. A plain hook (name only) is for
  tests. The GUI and the physics layer pass their own hooks later.
  It's implemented as a `StrPrinter` subclass whose `_print_Symbol`
  calls the hook, so the order of terms never changes.
- **A system** prints one equation per line, `(label)  lhs = rhs`,
  then the knowns with their values (`knowns: t0 = 0, x0 = 5, …`), so
  the zeros show before `eliminate_zeros`. Then comes a summary from the
  analysis: the wants, the connected unknowns
  against the equations, and the equations ready to solve.
  `show(origins=True)` adds each derived equation's origin under it.
- **A solution** prints each want's formula and number, numbered when
  there are several roots, and "no roots" with the reason when there
  are none. The time shows when it's at least 1 s.
- **The history** prints the numbered steps from the first.

### SymPy's rough edges

- **One `safe_simplify`,** in `sympy_compat.py`, the only place that
  mentions [SymPy issue 28926](https://github.com/sympy/sympy/issues/28926)
  and the only `try` around `simplify`. When the issue is fixed, it's
  the one place to change.
- **Slow solves are visible:** every solution records its time, and
  the display shows it from 1 s. There is no timeout, since SymPy
  can't be interrupted cleanly in-process.
- **Slow tests:** a test that takes more than 5 s gets
  `@pytest.mark.slow`, and `pyproject.toml` skips those by default
  (`addopts = "-m 'not slow'"`, with the marker registered). They run
  with `uv run pytest -m slow` when an increment adds one, and at each
  review.

### Examples in the repo *(user)*

- **Layout:** `examples/up_15e/ch02/example_2_4_handwritten.py`. The
  book and its edition come first, then the chapter (zero-padded, so
  the folders sort up to chapter 44), then `example_` or `exercise_`
  with the book's number. Another textbook gets its own folder beside
  `up_15e`.
- **Kept styles** get a slug after the number. In this series:
  `_handwritten` (equations written out, as in the old v3 scripts) and
  `_step_by_step` (eliminating by hand between displays). The catalog
  (001) names the rest, such as `_two_steps` and `_one_step` for
  Exercise 2.3.
- **Importable:** `examples/` and each folder under it are packages
  with an `__init__.py`. `pyproject.toml` adds `pythonpath = ["."]`
  for pytest, and `examples` to pyright's `include`.
- **Values at import, printing under `__main__`.** An example module
  builds its systems and solutions when imported, and prints only in
  `if __name__ == "__main__":`. It runs with
  `uv run python -m examples.up_15e.ch02.example_2_4_handwritten`.
- **The book's answers live in the example,** written once, as the
  book prints them:

  ```python
  BOOK = [                                  # University Physics, 15th ed.
      Answer(sol_a, x1, "43"),              # m
      Answer(sol_a, v1, "23"),              # m/s
      Answer(sol_b, x1, "55"),              # m
      Answer(sol_2_7_b, v1, "-11.3", "11.3"),
      Answer(sol_2_23, x1, "1.70", unit=meter),
  ]
  ```

  `Answer(solution, symbol, *printed, unit=None)` matches the
  solution's numbers for that symbol, sorted, one to one with the
  printed values, each to within half a unit in its last digit ("1.70"
  allows ±0.005). With `unit`, the number is divided by the unit first
  and must come out dimensionless. `Answer` lives in
  `examples/answers.py`, since it's about books, not the core.
- **One test,** `tests/test_examples.py`, finds every module under
  `examples/` whose name starts with `example_` or `exercise_`, imports
  it, and checks its `BOOK`. A module without a `BOOK` fails the test.

### The package

```
src/equarium/
  __init__.py       re-exports: System, Solution, Root, eq_flat,
                    all_at_once, eliminating, the errors
  system.py         System, Equation, Given, Derived, the steps
  analysis.py       Analysis, Role, analyze
  rewrite.py        eliminate_zeros, eliminate, isolate, cleanup
  solve.py          Solution, Root, all_at_once
  strategies.py     eliminating
  display.py        the printer, the hooks, render, render_history
  errors.py         EquariumError and its subclasses
  sympy_compat.py   safe_simplify
  equations.py      eq_flat
```

The exact split can move in a checkpoint if a module turns out too
small or creates a circular import. *(Since moved: checkpoint 001 put
`Equation`, the origins and `eq_flat` in `equations.py` and the steps
in `steps.py`, to avoid an import cycle, and 004 added `text.py` for
the text helpers.)* The layers can't move: the core
imports nothing from physics. Everything is typed, and pyright
(standard mode) stays clean.

## Sketches

How 2.4 and 2.5 read on this core. The checkpoints may adjust names,
but not the shape.

**2.4, equations written out** (the old v3, and increment 002's
example):

```python
import sympy as sp
from equarium import System
from examples.answers import Answer

x0, x1, v0, v1, t0, t1, v_av, a = sp.symbols("x0 x1 v0 v1 t0 t1 v_av a")

motorcycle = (
    System()
    .add(sp.Eq(v_av, (x1 - x0) / (t1 - t0)), label="2.2")
    .add(sp.Eq(a, (v1 - v0) / (t1 - t0)), label="2.7")
    .add(sp.Eq(v_av, (v0 + v1) / 2), label="2.10")
    .known(t0, 0)           # s
    .known(x0, 5)           # m
    .known(v0, 15)          # m/s
    .known(a, 4)            # m/s²
    .eliminate_zeros()      # t0 drops out; x0 = 5 stays a symbol
)

# (a) Position and velocity at t = 2.0 s.
part_a = motorcycle.known(t1, 2).want(x1, v1)
sol_a = part_a.solve()      # x1 = a*t1**2/2 + t1*v0 + x0   43
                            # v1 = a*t1 + v0                23
# (b) Where is he when his speed is 25 m/s?
sol_b = motorcycle.known(v1, 25).solve(x1)
                            # x1 = (2*a*x0 - v0**2 + v1**2)/(2*a)   55

BOOK = [Answer(sol_a, x1, "43"), Answer(sol_a, v1, "23"), Answer(sol_b, x1, "55")]

if __name__ == "__main__":
    part_a.show()           # (2.2)  v_av = (-x0 + x1)/t1  … x0, t1 green; x1 red
    sol_a.show()
    sol_b.show()
```

**2.5 after increment 007,** with the old physics code unchanged:

```python
m = make_states_model("m", 2)   # motorist
p = make_states_model("p", 2)   # police officer
m0, m1 = m.states
p0, p1 = p.states
p01 = p.edges[0]
m_v, dist, t = sp.symbols("m_v dist t")

setup = (
    System()
    .add(*kinematics_fundamental(m, axes=("x",)))     # (1)…(4)
    .add(*kinematics_fundamental(p, axes=("x",)))     # (5)…(8)
    .add(*eq_flat(
        m_v,  m0.vel.x,     # the motorist's speed is constant
        m_v,  m1.vel.x,
        dist, m1.pos.x,     # they meet: the same place
        dist, p1.pos.x,
        t,    m1.t,         # at the same time
        t,    p1.t,
    ))
    .known({m0.t: 0, p0.t: 0, m0.pos.x: 0, p0.pos.x: 0, p0.vel.x: 0})
    .known(m_v, 15)         # m/s
    .known(p01.a.x, 3)      # m/s²
    .want(t, p1.vel.x, dist)
)
setup.show()                    # the full set, the zeros among the knowns
chase = setup.eliminate_zeros() # as the old eliminate_zero_eqs(eqs)
chase.show()                    # the simpler set

all_at_once = chase.solve()     # t = 2*m_v/a_x_p_0_1   10
                                # p_1_v_x = 2*m_v       30
                                # dist = 2*m_v**2/a_x_p_0_1   150

by_hand = chase.eliminate(m0.vel.x, m1.vel.x, m1.pos.x, p1.pos.x, m1.t, p1.t)
by_hand.show()                  # the eight equations v4-002 printed
by_hand.solve().show()          # the same three answers
by_hand.show_history()          # … eliminate m_0_v_x using (9): into (3), (4) …
```

## Increments

| # | Increment | Adds |
|---|---|---|
| 001 | state and display | `System`, `Equation`, labels, `add`, `known`, `forget`, `want`, `eliminate_zeros`, `analyze`, the terminal display and its hook, the history of steps, `eq_flat` |
| 002 | all at once | `Solution`, `Root`, `solve`, `all_at_once`, several wants, the examples convention and its test |
| 003 | eliminate and isolate | `eliminate`, `isolate`, cleanup inside rewrites, their `Derived` origins, `show(origins=True)`, `show_history`, the errors |
| 004 | roots and filters | `where`, branching over replaced knowns, roots with several wants |
| 005 | units | numbers with units, `in_units`, `Answer(unit=…)` |
| 006 | elimination attempts | `eliminating`, the time on the display, the `slow` marker |
| 007 | the old physics code on the core | `kinematics_states.py` and `newtons_laws.py` copied over, and the examples ported |

The charter's "branching for parts" is spread across these increments.
The methods that branch come in 001, 2.4 (b) checks them in 002, and
2.7's four parts in 004. **Increments 001 to 006 use only equations
written out,** in tests or in the old v3-style examples. The physics
code comes in only in 007, so no answer can change while two layers
are new.

### 001 state and display

`system.py`, `analysis.py`, `rewrite.py` (`eliminate_zeros` and cleanup
only), `display.py`, `errors.py`, `equations.py`. Checks, in
`tests/test_system.py` and `tests/test_display.py`, on 2.4's
equations written out:

- Building the 2.4 base gives three equations labeled `2.2`, `2.7` and
  `2.10`. An unlabeled `add` gets `1`, then `2`, and a label is never
  reused after its equation is removed.
- `known(t0, 0)` alone leaves the equations as written, and `render`
  lists `t0 = 0` among the knowns. `eliminate_zeros()` then removes t0
  from every equation in one recorded step, and each rewritten
  equation's origin is `Derived("eliminate zeros", t0, (itself,))`. An
  old-style `Eq(t0, 0)` beside the known is dropped by that step.
  After the step, `forget(t0)` and `known(t0, 3)` raise `UsageError`,
  but before it they're allowed. A zero set after the step stays in
  the equations.
- `known(x0, 5)` leaves the equations alone. `known(x0, D*sp.tan(th))`
  raises, because it's a relationship. `known(D)` makes D known with
  no number.
- Branches don't touch their base: after `part_a = base.known(t1, 2)`,
  `base.knowns` has no t1, and two branches built the same way are
  equal.
- `part_a.analyze()`: the connected unknowns are `{x1, v1, v_av}`, and
  `(2.7)` is ready to solve.
- With the plain hook, `render(part_a)` (from the base after
  `eliminate_zeros`) prints `(2.2)  v_av = (-x0 + x1)/t1`
  and keeps SymPy's term order. With the terminal hook, x0 is wrapped
  in green codes and x1 in red, and only the symbols are wrapped.
- `render_history(part_a)` lists the steps: three adds, the knowns,
  `eliminate_zeros`, then t1 and the wants.
- `eq_flat(a, b, c, d)` is `[Eq(a, b), Eq(c, d)]`, and an odd count
  raises.

### 002 all at once

`solve.py`, `examples/`, `tests/test_examples.py`. Checks:

- **Examples:** `examples/up_15e/ch02/example_2_4_handwritten.py`,
  ported from the old `up-example-2.4-v3-001-step-by-step.py` (43, 23,
  55), and `example_2_5_handwritten.py`, from
  `up-example-2.5-v3-002-concise.py` (10, 30, 150), each with its
  `BOOK`. The old scripts' zero equations become zero knowns followed
  by `eliminate_zeros()`, which gives the old formulas.
- 2.4 (a) solves x1 and v1 together. The formulas are
  `a*t1**2/2 + t1*v0 + x0` and `a*t1 + v0`, with no t0 and no numbers
  in them.
- 2.5's three wants come from one solve, in one root, with
  `t = 2*m_v/p_a`.
- `solution.number(x1)` on a one-root solution is 43. A system with
  no wants raises `UsageError` on `solve()`.
- A system SymPy can't solve gives a solution with no roots and a
  reason, not an exception. The test can use any small system that
  `sp.solve` returns `[]` for.
- `render(sol_a)` shows `x1 = a*t1**2/2 + t1*v0 + x0`, then 43.
- The README gets a short usage section from the 2.4 example.

### 003 eliminate and isolate

`rewrite.py` gains `eliminate` and `isolate`. Checks:

- **kinematic-equations 005's first derivation:** on `(2.2)`, `(2.7)`
  and `(2.10)`, `eliminate(dt, using="2.7")` (with `dt` written as its
  own symbol, as in 005) leaves `(2.2)` equivalent to
  `v_av = a*(x2 - x1)/(v2 - v1)`. Its origin renders as
  `(2.2) ← (2.2) + (2.7), eliminate dt`, `(2.7)` is gone, and `(2.10)`
  is untouched.
- **Example:** `example_2_5_handwritten_step_by_step.py`, ported from
  `up-example-2.5-v3-001-step-by-step.py`. It eliminates the links by
  hand between displays and keeps the 2.5 answers. In a test, the
  2.5 system written out with the six links (m_v, dist, t) eliminated
  has none of those six symbols, still solves to 10, 30 and 150, and
  has six eliminate steps in its history.
- **3.10's proof,** written out in a test as one system: the dart and
  the monkey in 2D, `known(D)`, `known(v_mag)` and `known(angle)` with
  no numbers, `known(g)`, the zero knowns and `eliminate_zeros()`, and
  the links of the two
  objects' t and y. The test eliminates the monkey's x first (its
  v_av_x, x1 and x0), then follows the order of
  `up-example-3.10-v1-001.py`. Without that first step, the automatic
  choice uses the monkey's x equation to eliminate t. **Only the stated
  condition is left:** one equation, `D*v_mag*sin(angle)/d1x = v_mag*sin(angle)`,
  which holds exactly when the dart reaches x = D. The old script ends
  with the same equation. With `Eq(d1x, D)` added, and d1x eliminated
  last, **no equations are left.** Both results were confirmed in the
  spec's prototype.
- **4.1 v1-006,** written out (`R = F1 + F2 + F3` per axis, one-way
  polar for F1 to F3, components to polar for R, and
  `R_angle_deg = deg(R_angle)`). It eliminates F1 to F3's x and then y
  by hand, then solves: 128 N and 141.6°.
- **Errors:** `eliminate(x, using="2.10")` where (2.10) has no x
  raises `EliminationError`. An equation with two roots for the symbol
  is skipped without `using` and raises with it. Eliminating a known
  or a want raises. `isolate` with two roots raises `IsolationError`.
  A rewrite that yields `0 = 5` raises `Contradiction`.
- `isolate(v1, "2.7")` gives `(2.7) v1 = a*t1 + v0` with an isolate
  origin.
- Elimination never simplifies a whole `Eq`: after eliminating, an
  equation keeps its shape (`v_av = v0/2 + v1/2` stays with `v_av` on
  the left).

### 004 roots and filters

Checks, written out from `up-example-2.7-v1-000.py`:

- **2.7, four parts from one base** (`y0` and `t0` zero and
  eliminated, `v0 = 15.0`, `a = -9.8`): t1 = 1.0 gives 10.1 and 5.2.
  Replacing it with 4.0 gives −18.4 and −24.2. y1 = 5.0 gives two
  roots, ±11.3. v1 = 0.0, set after `eliminate_zeros`, gives 11.5 with
  the old script's formula `y1 = (v1**2 - v0**2)/(2*a)`. Part (d) is
  the known a, −9.8.
- **2.8:** y1 = −5.0 gives two roots, 3.36 and −0.303.
  `.where(t1 > 0)` keeps 3.36, and `.number(t1)` then works. Before the
  filter, `.number(t1)` raises `UsageError` naming 2 roots. Solving t1
  and v1 together keeps each root's pair.
- **3.9 with one-way polar,** written out from `up-example-3.9-v2.py`
  without the components-to-polar pair:
  `.where(b1x > 0)` keeps 9.16, and −15.7 is the other root.
- A relation that doesn't reduce (`.where(t1 > D)`, with D known and no
  number) raises `UsageError`.

### 005 units

Checks, written out from the old exercises:

- **2.23:** `a = -250*m/s**2`, `v0 = 105*km/h`, the rest zero and not
  eliminated, as in the old script. So the formula is the old one,
  `x1 = (2*a*x0 - v0**2 + v1**2)/(2*a)`. The raw number is
  `22.05*kilometer**2*second**2/(hour**2*meter)`, and `.in_units(m, s)`
  gives 1.70 m.
- **2.3, one step and two steps** (`up-exercise-2.3-002-one-step.py`
  and `-000-two-steps.py`): both give 2.75 h with `.in_units(h, km)`.
  The two-step test feeds the first solution's `number` into the
  second system as a known.
- `Answer(sol, x1, "1.70", unit=meter)` passes, and fails for a number
  in kilometers or for a wrong dimension.

### 006 elimination attempts

`strategies.py`. Checks:

- **3.9 v2 with the two-way polar equations:** `all_at_once` gives no
  roots. `solve(strategy=eliminating())` gives 9.16 (filtered), its
  system's history lists the eliminations, and the display shows the
  time. It's marked `slow` if it takes more than 5 s.
- **4.1 v1-003** (two-way polar for every force), `slow`: R_x −100.45,
  R_y 79.66, |R| 128.2 and 141.6°. The old run took 87 s, 224 s and
  103 s per answer. The checkpoint reports the new times. If it takes
  more than about 10 minutes, the test is reduced to |R| and the report
  says so.
- `eliminating(max_eliminations=0)` behaves like `all_at_once`.

### 007 the old physics code on the core

**Needs 001, the example catalog, to be done first.** `kinematics_states.py`
and `newtons_laws.py` are copied to `src/equarium/physics/` with no
design changes. Only their calls change: `eq_flat` comes from
`equarium`. The examples the catalog keeps are ported under
`examples/up_15e/`, with the catalog's slugs and a `BOOK` each. Their
calls become `System` methods, which is adapting, not redesigning:

- A zero the old script wrote as an equation (in `eq_flat` with
  `eliminate_zero_eqs`, or an `Eq(t0, 0)` that `sp.solve` removed)
  becomes `.known(sym, 0)` plus `.eliminate_zeros()`, at the point
  where the old script eliminated it.
- A zero the old script put in `values` becomes `.known(sym, 0)`
  alone.

Checks: every answer in the charter's table, through `BOOK`: 2.4, 2.5,
2.7, 2.8, 3.9, 4.1, 4.5, Exercises 2.3 and 2.23, and whatever else the
catalog lists. The formulas are compared with the old scripts'
output too. If a ported example's answer or formula differs from the
old script's, the checkpoint stops and reports it rather than adjusting
anything. The physics code doesn't get new features here. If it needs
one to port an example, that goes to the physics redesign.

Which of misc.py's equation helpers come over (`add_both_sides` and
the others, used only by kinematic-equations 003 and 004) is decided by
the catalog. If kept, they're plain functions on `sp.Eq` in
`equations.py`.

## How each increment lands

- **A checkpoint first.** `checkpoints/NNN-slug.md`, written from this
  page by the conversation that manages the checkpoints, once the
  previous increment has landed and the user has seen its review. An
  increment that turns out small can skip the full form, and one that
  turns out too big is split.
- **One commit per increment,** with its code, tests and docs.
  `uv run pytest` and `uv run pyright` pass, and so does
  `uv run pytest -m slow` when the increment has slow tests. The
  series README records the commit and the increment's status.
- **Checks pin the book's answers,** and formulas where the book prints
  them. A check that a later increment would change doesn't go into an
  earlier one.
- **The old repo stays as it is.** Old scripts run, when needed, with
  the charter's shim from outside the repo.
- **Docs:** the series README follows the code. The package README's
  usage section starts in 002 and stays one short example.

## SymPy to watch

- `sp.Eq` evaluates on construction and after `subs`: `Eq(x, x)` is
  `True`. `add` and every rewrite must accept `True` and `False`
  where an `Equality` was expected.
- `sp.solve(..., dict=True)` returns the roots in SymPy's own order.
  The display numbers them as they come, and tests never depend on the
  order (`Answer` sorts).
- Floats in the knowns (`15.0`, `-9.8`) never reach the formulas,
  because the knowns stay symbols. Only the numbers are floats.
- `105*km/h` stays exact (`175*meter/(6*second)` after conversion)
  until `sp.N`.
- SymPy's type hints are incomplete. Our code is fully typed, and where
  a SymPy call returns an unhelpful type, a `cast` or a narrow helper
  is better than a `# type: ignore`.

## Not in this spec

From the charter, each for a later series: the physics redesign,
structured symbols, vector equations, the GUIs, and other textbooks.

Also out, because no example needs them in the core: the derive-all
search of kinematic-equations 005 (the origin tree gives its
provenance, and porting the search is the catalog's call); the old
`eliminate_singleton_equations`, `check_knowns`, `matches_existing`
and `add_if_new`; `clear_zero_denominators` (added only if a check
fails without it); 2D and LaTeX rendering; Jupyter; timeouts for
`solve`; consistency checks for overdetermined systems.
