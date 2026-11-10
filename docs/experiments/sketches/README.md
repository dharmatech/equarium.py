# Setup sketches (experiment)

**Status:** first prototype, Example 2.4 (2026-11-09). Its sketch code
moved into the problem's folder, and the experiment merged into the
physics branch (2026-11-10). This is an experiment, not a series. It
takes a series number only if it's adopted.

The book's "set up" step is a sketch: axes, an origin, the points of
interest, and the knowns and unknowns labeled. Most of the book's
examples have a figure, but the exercises don't, and the publisher's
figures never go in this repo. So this experiment draws the sketch from
the model instead: the particle, its states and edges, and the system's
knowns, wants and other unknowns. A sketch drawn from the code always
agrees with the code.

**Where:** it began on its own branch, `2026-11-09-generated-sketches`,
from `2026-11-08-physics-redesign` at `107a670`, in its own worktree so
the physics branch's review wasn't disturbed. It merged into the
physics branch on 2026-11-10, and goes to master with it.

## What there is

- **`src/equarium/sketch.py`.** `sketch(particle, (title, system), ...)`
  returns an SVG document with one panel per part. Each panel has:
  - the x axis, with the origin, `O`
  - each state as a point, with its velocity as an arrow, dashed when
    the velocity's value isn't known
  - each edge as an arc from one state to the next
  - every symbol the system has, in the book's notation, with real
    subscripts: `x₀ = 5 m` (known, green), `x₁ = ?` (want, red), `t₁`
    (other unknown, gray)

  A known's value prints as the book prints it, `4 m/s²` or `15`. A
  symbol the system doesn't have isn't drawn. The sketch is a
  schematic, not to scale: the states are evenly spaced, in order, to
  the right of the origin. The module depends on the physics layer and
  the core, and neither imports it.
- **A problem's `sketch.py`, in its folder.** 2.4's is
  `examples/up_15e/ch02/examples/n04/sketch.py`. Its `draw()` returns
  the sketch of `main.py`'s `part_a` and `part_b`, and run, it writes
  `sketch.svg` beside it:

  ```bash
  uv run python -m examples.up_15e.ch02.examples.n04.sketch
  ```

- **`examples/up_15e/ch02/examples/n04/sketch.svg`.** What 2.4's
  `sketch.py` writes.
- **`tests/test_sketch.py`.** It tests the subscripts, the values and
  the labels' colors. It finds every problem's `sketch.py` and checks
  that the `sketch.svg` beside it is what it draws today.
- **Only `main.py` and `main_<slug>.py` are versions.** The tests check
  a problem's versions against the book, and those are the only modules
  they take as versions, as the repo's README names them. Any other
  module in a problem's folder, such as `sketch.py`, supports them and
  needs no `BOOK`. The change is in `tests/test_examples.py`'s
  `is_version`.

## Found so far

- **The model has nearly everything.** Which symbols go on which point
  or arc, and their roles and values, all come from the `System` and the
  `Particle`. Only the title is written by hand.
- **Units make it read like the book.** `main.py` has plain numbers, so
  its sketch says `aₓ = 4`. Drawn from the units version,
  `main_units.py` in the same folder, the same sketch says
  `aₓ = 4 m/s²` and `x₀ = 5 m`. A zero loses its
  unit: SymPy makes `0 * second` a plain `0`.
- **Not to scale is the safe default.** A wanted position has no value
  to place, so the states go in order. The origin is always on the
  left, which a negative known position would contradict.

## Open questions

- **Scale.** Place known positions to scale, and wanted ones in order
  between them?
- **The origin and the scenery.** 2.4's origin is a signpost. The model
  doesn't know that. Is a caption per sketch enough, such as
  `origin="signpost"`?
- **Which part.** One panel per part, or one sketch of the base system?
- **Several particles on one axis** (2.5, with an event), **projectiles**
  (3.6 to 3.10, with an `XY` plane and a trajectory) and **free-body
  diagrams** (4.4 and 4.5, from `newton`'s forces): one kind of drawing
  each, in that order.
- **Viewing.** VS Code needs an extension to preview SVG, but a browser
  and GitHub show it directly. A `--sketch` option on each `main.py`
  could write and open it.
- **Where it ends up.** A module of equarium's, or a package of its own
  that depends on equarium.
