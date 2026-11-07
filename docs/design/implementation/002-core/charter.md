# 002 core: charter

The handoff for designing equarium's core in a new conversation. It
says what equarium is for, what the old library taught, what is
already decided, and what the spec has to settle.

If you've been told to read this file, this is the whole assignment.
Read it, settle the open questions with the user, write `spec.md` in
this folder, and stop.

## The goal

equarium solves physics problems the way the old library
([combine-equations.py](https://github.com/dharmatech/combine-equations.py),
at `~/src/combine-equations.py`) did. It starts from a few core
equations, states what is known and what is wanted, and lets SymPy
derive the rest: the answer as a formula first, then its number.
Example 2.4 shows the idea. The examples give only the book's eqs.
2.2, 2.7 and 2.10, and the solver produces the book's 2.12, 2.8 and
2.13 itself, without anyone choosing them.

This series builds the **core**: the object that holds a problem, the
operations on it, and the display. The old physics code then runs on
the new core with **no design changes**, and the old examples become
tests. The
physics layer is redesigned later, in a series of its own.

## Scope

- **The same scope as the old library.** This is a consolidation and a
  redesign of what exists, lean and well factored. It adds no features
  for later chapters.
- **Every feature names an example.** The core grows only when an
  existing example or exercise needs it. Anything without one waits.
  The "Driven by" column below gives each lesson's example.
- **Keep the alternative styles.** Some examples are solved more than
  one way on purpose: one step or two, elimination by hand or
  automatic, all at once or step by step. The user wants those kept as
  teaching contrasts. In the new core they should be one problem with
  different strategies, not different code paths.

## The order of the work

1. **The core,** in this series.
2. **The old physics code as the core's first client, with no design
   changes.** `kinematics_states.py` and `newtons_laws.py` depend only
   on SymPy, `Point3` and `eq_flat`, so they can be copied over nearly
   as is. The examples then rerun on the new core and check its
   answers.
3. **The physics redesign,** in a later series.

**The old physics code doesn't shape the core.** Design the core as if
the physics code didn't exist. Where the right design differs from
what the physics code expects, the core does the right thing, and the
physics code is adapted when it's ported in step 2. The only point of
contact today is `eq_flat`, from `misc.py`, so little should need
adapting. Adapting its calls to the new core isn't a redesign: its
model, names and equations stay as they are until step 3.

**Never change two layers at once.** If an answer goes wrong while both
the core and the physics code are new, there's no telling which one
broke. In this order, a changed answer in step 3 can only come from the
physics redesign.

## Where the old library is

Everything is in `~/src/combine-equations.py`. It runs with
`uv run python <file>` from the repo root, on Python 3.14.

**Library, `src/combine_equations/`:**

| Module | What it does |
|---|---|
| `misc.py` | `isolate_variable`, `combine_equations_sp` (the original "combine": isolate a variable in one equation and substitute it into another), `eq_flat` (pairs into `Eq`s), both-sides helpers (`add_`, `multiply_`, `divide_both_sides`, `expand_lhs`, `expand_rhs`), `display_equation`. |
| `display_equations.py` | `display_equation_` and `display_equations_`: knowns in green, the want in red, through ANSI codes. It works by substituting symbols whose *names* contain the color codes. |
| `solve_system.py` | `connected_unknowns` (the unknowns linked to the want), `solve_system_multiple_solutions` (`sp.solve` over those, every root), `solve_with_elimination_attempts` (eliminate one variable at a time until `solve` works, and report the time), `clear_zero_denominators`, `filter_equations_for_unknowns`, `eliminate_singleton_equations`. `solve_system_2`, which took only the first root, is commented out. |
| `eliminate_variable_subst.py` | `eliminate_variable_subst` (solve each equation for the variable, take the simplest result by `count_ops`, substitute it everywhere, drop tautologies), `cleanup_equations`, `eliminate_zero_eqs`. It uses `_safe_simplify` to get around [SymPy issue 28926](https://github.com/sympy/sympy/issues/28926). |
| `solve_and_display.py` | `solve_and_display_`: solve with version 0, 1 or 2 of the solver, then print each root as a formula and as a number (`sp.N`). |
| `solve_for_target.py` | Commented out, and unused. |
| `kinematics_states.py` | The physics layer: `make_states_model`, `kinematics_fundamental` (the code's EQ2, EQ7 and EQ10, the book's eqs. 2.2, 2.7 and 2.10), `magnitude_and_angle_equations`, and link helpers. It contains no solver. |
| `newtons_laws.py` | `superposition_equations` and `newtons_second_law`, on `Point3`. |
| `equation_gui.py`, `equation_gui_jupyter.py` | tkinter and Jupyter GUIs. Click a symbol to highlight it everywhere, right-click to eliminate or isolate it, and see the history of steps. They recover symbols from the printed text with regular expressions. |

**The common shape.** Almost every function takes the same three
things: `(equations, values, want)`. The display, the solvers, the
eliminators and the GUI's history all carry that triple separately.
That's the main idea the core is built around.

**Examples,** under `examples/up/` (University Physics, 15th ed.):
chapter 2's Examples 2.4 to 2.8 and Exercises 2.1, 2.3, 2.5, 2.19,
2.21 and 2.23; Examples 3.6 to 3.10 and 3.13; Examples 4.1, 4.4, 4.5
and 4.7; and `ch2/kinematic-equations/`, which derives every equation
reachable from the core three. Several examples come in versions,
numbered in the file names, that show how the approach developed.

**11 scripts don't run as they are.** They import `solve_system_2`,
which was commented out on 2026-01-09. Don't edit the old repo unless
the user asks. To run them, restore the function from outside:

```python
# run_with_shim.py, from the old repo's root:
#   uv run python run_with_shim.py <example.py>
import runpy, sys
import sympy as sp
import combine_equations.solve_system as ss

def solve_system_2(equations, values, want):
    unknowns = list(ss.connected_unknowns(equations, values, want))
    result = sp.solve(equations, unknowns, dict=True)
    return sp.Eq(want, result[0][want])

ss.solve_system_2 = solve_system_2
runpy.run_path(sys.argv[1], run_name="__main__")
```

With this, the three Example 2.4 scripts print 43 m, 23 m/s and 55 m,
the book's answers.

## What the old library taught

| Lesson | Driven by |
|---|---|
| Solve every unknown linked to the want at once (`connected_unknowns`, then `sp.solve`). | 2.4 |
| Keep every root. A quadratic gives two, and the physical one is the user's call or a filter's: t = 3.36 s, not −0.30 s. | 2.7, 2.8, 3.9 |
| Eliminating trivial equations first (`x₀ = 0`, `t₀ = 0`) keeps the printout readable and helps `solve`. | 2.5, 2.7, 3.9, 3.10 |
| Elimination by hand, one variable at a time, has to stay possible. Some examples need it, and the GUI does it with clicks. | 3.10, 4.1 v1-006 |
| A "show that" can be proved by elimination. Eliminate until no condition is left, or only the stated one. | 3.10 |
| When `solve` struggles, eliminate a variable and try again, and say how long it took. With the full two-way polar equations, 4.1 v1-003 took 87 s, 224 s and 103 s per answer. One-way conversions fixed it. That fix belongs to the physics layer, but the core must make such slowness visible. | 3.9 v2, 4.1 |
| Values carry units (`105*km/h`), and the answer needs converting at the end. 2.23 prints `22.05*kilometer**2*second**2/(hour**2*meter)`, which is 1.70 m. | 2.3, 2.21, 2.23, 4.7 |
| The parts of one problem change the knowns. 2.4 (b) copies (a)'s values, removes t and adds v. 2.7 rebuilds them for every part. | 2.4, 2.7 |
| Knowns in green, the want in red, everything else plain. That shows at a glance what is ready to solve. | All |
| Record where each equation came from: "eq_2.2 + eq_2.7 (eliminate dt)". | kinematic-equations 005, the GUI's history |
| Symbol names carry meaning only as a string convention, and that is fragile. The display recolors by renaming symbols, and the GUI parses names with regular expressions. | The display, the GUI |
| Some examples give t₀ = 0 as an equation and others as a value. There was never one rule. | 2.4 vs 2.3, 2.21 |

**Answers the old scripts print,** a start on the test list. 001,
the example catalog, will complete it:

| Example | Answers |
|---|---|
| 2.4 | x = 43 m and v = 23 m/s at 2 s; x = 55 m when v = 25 m/s |
| 2.5 | t = 10 s, the officer at 30 m/s, 150 m each |
| 2.7 | at 1 s: 10.1 m and 5.2 m/s; at 4 s: −18.4 m and −24.2 m/s; ±11.3 m/s at 5 m; 11.5 m highest (g = 9.8) |
| 2.8 | t = 3.36 s (the other root, −0.30 s, is rejected) |
| 3.9 | 9.16 m (the other root, −15.7 m, is rejected) |
| 4.1 | net force 128 N at 141.6° |
| 4.5 | friction −0.90 N |
| Exercise 2.3 | 2.75 h for the slow trip |
| Exercise 2.23 | 1.70 m |

## What is decided

From the discussion that led to this charter (2026-11-06 and 07):

- **A problem state, immutable.** One object holds the equations, the
  knowns, the wants, and the steps that produced it. Every operation
  returns a new state that records the step, such as "eliminated dt
  using eq 2.2". The GUI's history, the provenance from kinematic
  equations 005, and a step-by-step derivation printout all come from
  that record.
- **Cheap branching.** A multi-part problem is a shared base with a few
  knowns changed per part, as in 2.4 and 2.7.
- **A small set of operations:**
  - substitute the knowns
  - eliminate a variable, optionally naming the equation to use. The
    original "combine equations" lives on here.
  - isolate a variable
  - clean up: drop tautologies and catch contradictions
  - solve: every root, with an optional filter such as t ≥ 0
  - analyze: the unknowns connected to the want, the equations ready
    to solve (one unknown), and the count of unknowns against
    equations
- **Solving styles are strategies** over those operations: all at
  once, step by step, eliminate until `solve` works, or guided by
  hand.
- **The display is a view** over the analysis: green, red and plain.
  It shows a symbol through a function the caller can supply, and
  never relies on the symbol's name meaning anything. The core has no
  physics in it. The physics layer supplies better rendering later.
- **Plain SymPy objects.** Equations and symbols stay `sp.Eq` and SymPy
  expressions, so the user can always drop down to SymPy. No wrapper
  language on top.
- **The project:** uv for everything, Python 3.14, `src/equarium/`,
  `uv run pytest` and `uv run pyright` (standard mode). Each ported
  example gets a test of the textbook's answers.

## The user's preferences

- **Dot syntax and objects,** as in `m0.pos.x`: methods on objects,
  not generic functions that lose the dots.
- **Static typing.** Typed code, frozen dataclasses, pyright clean.
- **Small, focused modules,** in layers: the core knows nothing of
  physics.
- **Think as if in Haskell or Scala.** Prefer structured values with
  structural equality to side tables. Rendering is a function separate
  from the value. Don't lean on a Python-only trick when a general
  design exists.

## Design questions for the spec

1. **The state's shape.** Are equations a list, or labeled ("eq 2.2")
   so that steps can name them? Are knowns a dict? Can there be several
   wants at once, or one per solve? How is a step recorded: a
   description, the operation and its arguments, or both?
2. **Branching.** How a part of a problem is written. Possibly
   `with_known` and `without_known`, or another shape that reads well
   in 2.4 (b).
3. **Values or equations.** One rule for t₀ = 0. For example: numbers
   are knowns, relationships are equations, and zeros are substituted
   automatically, which would make `eliminate_zero_eqs` disappear.
4. **The operations' API.** Methods on the state (the user's dot-syntax
   preference) or functions over it. What each one returns, and how a
   failure comes back: no candidate to eliminate with, a
   contradiction, no solution.
5. **The solve result.** The formula and the number for every root;
   which filter syntax picks the physical root; how a target unit is
   requested (2.23).
6. **Strategies.** What a strategy is (a function, an object, a name),
   and which ones the examples need. The old library's versions 0, 1
   and 2, and elimination by hand.
7. **The display.** The terminal form (ANSI colors) and the hook for
   showing a symbol, so the GUIs can sit on the same core later. How
   the history prints.
8. **The examples in the repo.** Where ported examples live and how
   they're named, and how their tests check answers without each
   example being written twice. One uniform convention, kept as the
   examples grow:
   - **The book first,** as in the old `up` for University Physics.
     Other textbooks may come later (see "Not in this series"), so the
     layout must leave room for them. Exercise numbers can change
     between editions, so the edition (15th) should be recorded
     somewhere, in the name or in a note.
   - **Then the chapter, then examples or exercises,** as the old repo
     intended. It drifted: chapter 2 and 4 examples sit in a folder
     each, chapter 3's are mostly loose files, and the exercises are
     under `ch2/exercises/2.3/`.
   - **Versions,** for the alternative styles that are kept on
     purpose.
   - **Importable names,** if tests import examples. Python can't
     import a file named `up-example-2.4-v4-001.py`. The old tests
     would have had to run each file as a script.
9. **SymPy's rough edges.** `_safe_simplify` and issue 28926; when to
   simplify; how to report a slow `solve`.

The spec doesn't have to answer the physics questions under "Not in
this series".

## Candidate increments

For the spec to choose from, reorder or merge. Each one lands with
tests.

1. **The state and the display.** Build a state from hand-written
   equations (the book's 2.2, 2.7 and 2.10, with symbols written out as
   in 2.4's v3 script) and print it green and red.
2. **Solve all at once.** Connected unknowns, every root, formula and
   number. Check 2.4: 43, 23, 55.
3. **Eliminate, isolate, clean up, with the history.** Checks from 2.5's
   simplification and 3.10's proof.
4. **Branching for parts.** 2.4 (b), and 2.7's four parts.
5. **Roots and filters.** 2.7, 2.8, 3.9.
6. **Units.** Values with units, and the answer in a target unit: 2.3
   and 2.23.
7. **Elimination attempts.** 3.9 v2 and 4.1, with the time reported.
8. **The old physics code on the new core.** Copy `kinematics_states.py`
   and `newtons_laws.py` over with no design changes, adapting only
   their calls to the core, and port the examples as tests. This one
   needs 001, the catalog, to be done.

## How to work

- **Design with code first.** Before settling the API, sketch how two
  or three examples would read on it, starting with 2.4 (one object,
  parts) and 2.5 (two objects meeting). Pick the design that makes
  them read best. The sketches can go in the spec.
- **Then increments, as checkpoints,** in the shape of mpl-niva's
  `008-simplifier` (see References): `spec.md` lists
  the agreed increments, and `checkpoints/NNN-slug.md` hands them out
  one at a time. Each lands as its own commit, with `uv run pytest` and
  `uv run pyright` passing, and the series README records it. The
  conversation that writes the spec manages the checkpoints and
  reviews each commit, and the user sees each review before the next
  one starts.
- **Scale to the work.** An increment that turns out small can skip
  the full checkpoint form. One that turns out too big gets split.
- **Docs:** this series' README for status and commits, and the
  [series map](../README.md).
- **The old repo stays as it is,** unless the user asks.

## Not in this series

Kept here so they aren't lost. Each belongs to a later series:

- **The physics redesign.** Keep `m0.pos.x`, the split between a state
  (an instant: position, velocity, time) and an edge (an interval: Δt,
  acceleration, average velocity), and generating equations from the
  model. Rethink:
  - the dimension, set when the model is created instead of at each
    equation call
  - one naming rule; today states put the object first (`m_0_v_x`)
    and edges last (`a_x_m_0_1`), and two models with the same prefix
    collide silently
  - polar form as a separate add-on, with one-way conversions (4.1)
  - events that link objects and generate the equalities (2.5, 3.10)
- **Structured symbols.** A symbol that knows its owner, state or
  edge, quantity and component. Either a SymPy class whose identity is
  that structure (SymPy's own objects are a constructor plus
  arguments, like an algebraic data type, and `Indexed` is a precedent)
  or a table from symbol to meaning. The user prefers the first, if
  SymPy handles it well. Rendering stays a separate function, a custom
  printer: `m0.pos.x` for debugging, the book's notation in Jupyter.
  Whether `solve`, `simplify` and `subs` treat such symbols correctly
  can be tested with a short prototype on 2.4.
- **Vector equations.** Write a law once as a vector equation and
  expand it into one equation per axis of the model. Solve with the
  components, display with the vectors.
- **The GUIs,** rebuilt on the core once it has settled.
- **Other textbooks,** once the library handles a good part of
  University Physics. For example Halliday & Resnick, or someday the
  Feynman Lectures. Their notation and naming will differ, which will
  test whether equarium's conventions hold up beyond one book. Until
  then University Physics is the one concrete target.

## References

- The old library and examples: `~/src/combine-equations.py`.
  Good starting files:
  - `examples/up/ch2/up-example-2.4/up-example-2.4-v4-001-ks-display-solution.py`:
    the cleanest small example.
  - `examples/up/ch2/up-example-2.4/up-example-2.4-v3-001-step-by-step.py`:
    the same with equations written by hand, a model for increment 1.
  - `examples/up/ch2/up-example-2.5/up-example-2.5-v4-002-ks-eq-flat.py`:
    two objects, linking symbols, elimination before solving.
  - `examples/up/ch2/up-example-2.7/up-example-2.7-v1-000.py`: four
    parts and two roots, with Example 2.8.
  - `examples/up/ch3/up-example-3.9-v2.py` and
    `examples/up/ch3/up-example-3.10-v1-001.py`: 2D, polar velocity,
    and the proof by elimination.
  - `examples/up/ch4/up-example-4.1/`: eight versions; compare `v1-003`
    (slow) with `v1-007-ok`.
  - `examples/up/ch2/exercises/2.23/up-exercise-2.23-000.py`: units.
  - `examples/up/ch2/kinematic-equations/kinematics-equations-005-eq-history.py`:
    every derivable equation, with provenance.
- The textbook: `~/journal/2026-11-06-equations/up-15e.pdf`, University
  Physics with Modern Physics, 15th ed., 1596 pages; don't read it
  whole. `mutool show up-15e.pdf outline` gives the chapters' pages
  (chapter 2 is PDF pages 64–95), and `pdftotext -f A -l B -raw` keeps
  fractions readable. Chapter 2 numbers 18 equations. 2.2 and 2.4 are
  definitions, 2.7 states that the average acceleration is the constant
  one, and 2.10 holds only for constant acceleration. Table 2.5 lists
  the derived 2.8, 2.12, 2.13 and 2.14 with the variables each one
  contains.
- The docs convention: `~/journal/2026-10-20-niva/mpl-niva/docs/design/implementation/`
  (`008-simplifier` has a charter, a spec and checkpoints), and the
  roles in `~/journal/2026-09-02-aloe-racket/docs/workflow.md`.

## First steps in the new conversation

1. Read this charter, then the old library's modules in the table
   above, and the reference examples.
2. Run Example 2.4 v4-001 with the shim above, to see what the old
   output looks like.
3. Sketch 2.4 and 2.5 on a proposed core, and go through the design
   questions with the user.
4. Write `spec.md`: the decisions, the increments with their checks,
   and how each increment lands. Then stop. The first checkpoint is
   written once the user has agreed the spec.
