# physics 003: polar and degrees

**Status:** Done at `4d84e67` and reviewed (2026-11-09).

If you've been told to read this file, this is the whole assignment.
Build it, check it, commit it, report, and stop.

## Goal

The first reshape. The examples that still do polar or degrees by hand
move to the methods, and two-way polar becomes one way. That means:

- **`polar.py` gains `degrees`,** and `Vector` gains `degrees()`.
- **`notation.py` gains the rows for `angle_deg`:** `α0°`, `θ0°`, `θR°`.
- **One-way polar everywhere.** 3.6 and 3.7 move to `to_polar()`,
  `from_polar()` and `degrees()`. 3.8, 3.9 and 3.10 drop `to_polar()`.
  4.1 (both) moves to `R.degrees()`.
- **Two by-hand steps go,** as the user chose: 3.8's two
  `eliminate(…, using=…)`, and 3.9's `eliminating()`.
- **3.9 and 3.10 leave `SLOW_EXAMPLES`.** One way, 3.9 imports in
  1.7 s and 3.10 in 4.1 s.
- **The old formulas, still renamed back.** `tests/old_names.py` gains a
  per-module map for the names the old scripts made themselves, such as
  3.6's `dist`. All 66 rows and 3.10's show-that come out verbatim.

**No formula changes.** The equations change, and so do the names, but
every want's formula, renamed back, is the old one. The scratch run
checked all 66 rows. So no row needs a new formula, and none gets one.
The new text, in the new names, is listed below for the comments. The
test rule for a row whose formula changes is designed under "A row
whose formula changes". It isn't built here.

**Not in this increment:**

- `Event` (004). 3.10's `t` and `y` stay plain.
- The projectile setup (005). 3.6's `eliminate(m01.dt)` stays. So do
  the `a_y = -g`, `v0x = v1x` and `a_x = 0` lines of 3.6 to 3.10.
- `mass` and `newton` (006).
- **The by-hand steps the spec keeps.** 3.7's `eliminate(b1.vel.angle)`
  stays: without it, SymPy still leaves `b1.vel.angle_deg` undetermined
  (checked). 3.10's 19 eliminations stay, in the same order.
- **4.4 and 4.5** don't change. They have no polar.

## Read first

- **[The spec](../spec.md).** In "Decisions": "Polar and degrees",
  "Book notation", "The steps the helpers make unnecessary", "The
  examples" and "The tests". Then "### 003 polar and degrees", "How each
  increment lands" and "SymPy to watch".
- **[Checkpoint 002](002-chapters-3-and-4-renamed.md),** and what it
  built: `src/equarium/physics/vectors.py`, `polar.py` and
  `notation.py`. Also `tests/old_names.py`, `tests/test_old_outputs.py`,
  `tests/physics_misuse.py`, `tests/test_physics.py` and
  `tests/slow_examples.py`.
- **The seven modules,** listed in "The examples" below.
- **`tests/test_strategies.py`.** It has 3.9 and 4.1 written out with
  two-way polar, and the `eliminating()` lesson. It doesn't change.
- **The prototype,** outside the repo, in
  `~/.config/Claude/side-session-notes/local_9ac850c1-eb15-42fc-bbb0-61739b724d16/004-spec-prototype/`:
  `ch3.py` (3.8 and 3.9 all at once, one way), `sketches.py` (3.6 with
  `to_polar` and `degrees`, and 3.10's one-way dart) and `layer.py`'s
  `degrees`. It's data, not the source: the spec and this page win.
  Where it differs:
  - its 3.6, 3.8 and 3.9 use the projectile setup, which is 005. Here
    they keep their own lines, and 3.6 keeps `eliminate(m01.dt)`;
  - its `degrees` lives in `Vector`. Here it delegates to `polar.py`.

## Starting point

The branch `2026-11-08-physics-redesign`, at the commit that adds this
checkpoint, on top of `6b7b869` (the review of 002). Check it with
`git branch --show-current`. If you're on another branch, stop and ask.
Don't switch branches, stash or reset.

`uv run pytest` passes 315 tests and deselects 8 slow ones, in about
35 s. `uv run pytest -m slow` passes those 8. `uv run pyright` reports
0 errors and 0 warnings.

Checked in scratch while writing this page, on the repo at `6b7b869`:

- **Every reshaped module,** written as this page says, ran. All 66
  rows came out verbatim, renamed back through the map below, with
  their numbers. Every `BOOK` passed.
- **A scratch copy of `tests/test_old_outputs.py`,** with the map and
  `old_name(symbol, module)`, passed all 80 of its tests against the
  reshaped modules, in 19 s. 3.10's show-that ran unmarked.
- **3.10's show-that** is the same, sides swapped:
  `D*d0.vel.mag*sin(d0.vel.angle)/d1.pos.x = d0.vel.mag*sin(d0.vel.angle)`.
  It holds at `d1.pos.x = D`, `reached` has no equations, and `sol_t`
  is `D/(d0.vel.mag*cos(d0.vel.angle))`. Its shape didn't change, so it
  isn't pinned anew.
- **Pyright** flags `f.degrees()` on an `X` vector
  (`reportAttributeAccessIssue`), an unneeded ignore on `R.degrees()`
  fails the run, and the package with `degrees` is clean. So is
  `old_names.py` with the map.
- **The notation rows** print as the table below.
- **The times,** each module's import in a fresh process, after
  SymPy and equarium, three runs each:

  | Module | Now | One way |
  |---|---|---|
  | 3.6 | 0.43 s | 0.47 s |
  | 3.7 | 1.73 s | 1.72 s |
  | 3.8 | 1.35 s | 0.53 s |
  | 3.9 | 6.0 s | 1.7 s (the solve 1.6 s) |
  | 3.10 | 9.4 s | 4.1 s |
  | 4.1 | 1.33 s | 1.33 s |
  | 4.1 step by step | 3.8 s | 3.8 s (it imports `main.py`) |

  3.10's dart eliminations take 0.7 s, not 5.9 s. Its meeting's two
  eliminations, about 1.3 s each, don't change; 004 reshapes them.
- **The slow tests left,** the three in `tests/test_strategies.py`,
  take 5 min 14 s: 4.1's R_y 216 s, R_x 91 s, and 3.9's
  `eliminating()` 6 s.

## Build

### `polar.py`: `degrees`

- **A third plain function:**

  | Function | Equations |
  |---|---|
  | `degrees(v)` | `v.angle_deg = 180*v.angle/pi`, SymPy's `deg` |

  It takes a `Vector[XY]` and returns `list[sp.Eq]`, one equation, so
  every polar method reads the same: `.add(*R.degrees())`. Write the
  right side as `sp.deg(v.angle)`, and narrow with `cast`, as the other
  two do.
- **As a string:** `Eq(d0.vel.angle_deg, 180*d0.vel.angle/pi)`. That's
  the old `vel_angle*180/pi`, since SymPy orders the product.
- **The module docstring** says `degrees` gives the angle in degrees
  from the angle in radians.

### `vectors.py`: `Vector.degrees`

- **`degrees(self: Vector[XY]) -> list[sp.Eq]`,** a one-line call into
  `polar.degrees`, beside `from_polar` and `to_polar`.
- **At run time,** on an `X` or `Y` vector, it raises `UsageError`
  through `angle_deg`: `f is in X, so it has no angle_deg`.
- **The module docstring** names `degrees` with the other two.

### `notation.py`: the rows for `angle_deg`

- **This increment's rows** of the spec's table:

  | Symbol | Book | With owner `P` |
  |---|---|---|
  | `m0.vel.angle_deg` | `α0°` | `αP0°` |
  | `m0.pos.angle_deg` | `θ0°` | `θP0°` |
  | `R.angle_deg`, `F1.angle_deg` | `θR°`, `θF1°` | |

- **Each is its angle's row, then `°`.** The order stays the book's:
  letter, owner, state, then the degree sign.
- **Still printed as names:** an edge vector's polar parts, such as
  `m01.a.mag` and `m01.a.angle_deg`, and any other `Var` the table
  doesn't cover.
- **The class docstring** gains the `angle_deg` rows, and stops naming
  `m0.vel.angle_deg` as a symbol that prints its name.

### `__init__.py`

**The docstring** says that `from_polar()`, `to_polar()` and
`degrees()` write a vector's polar equations, one way each.

### The examples

| Module, under `examples/up_15e/` | What changes |
|---|---|
| `ch03/examples/n06/main.py` | `m1.pos.to_polar()`, `m1.vel.to_polar()`, `m1.vel.degrees()`. `dist`, `vel_mag`, `vel_angle` and `vel_angle_deg` go. `eliminate(m01.dt)` stays. |
| `ch03/examples/n07/main.py` | `b0.vel.from_polar()`, `b1.vel.to_polar()`, `b1.vel.degrees()`. Its five symbols go. `eliminate(b1.vel.angle)` stays. |
| `ch03/examples/n08/main.py` | `p0.vel.from_polar()` only. The two `eliminate(…, using=…)` go. |
| `ch03/examples/n09/main.py` | `b0.vel.from_polar()` only. `eliminating()` goes: all at once. |
| `ch03/examples/n10/main.py` | `d0.vel.from_polar()` only. The eliminations stay. |
| `ch04/examples/n01/main.py` | `R.degrees()`, twice. `R_angle_deg` goes. |
| `ch04/examples/n01/main_step_by_step.py` | `R.degrees()`. It no longer imports `R_angle_deg`. |

**In every module:**

- **The labels.** Each new `add` takes the place of the old one. 3.7
  and 4.1 keep their numbers. 3.6 gains (10), the position's angle, so
  its speed and direction move to (11) to (13). 3.8, 3.9 and 3.10 lose
  two-way polar's two equations, so 3.10's projectile lines become (10)
  and (11). Nothing picks these by label: 3.10's `equation("8")` and
  `("9")` stay the same.
- **Everything else stays:** the knowns, wants, solves and
  eliminations, in the same order. `eq_flat` stays where a module still
  writes its own equations. Remove an import a module no longer uses:
  3.6's `eq_flat`, 3.9's `eliminating`.
- **The `BOOK`s keep their answers.** Only the symbols are renamed:
  `dist` becomes `m1.pos.mag`, and so on.
- **Comments and docstrings use the new names.** A comment that quotes
  a formula quotes it as the module prints it now. The new lines are
  below.
- **A docstring says which step went and why,** where one went (3.8,
  3.9), as the spec asks.

#### 3.6

```python
ride = (
    cliff
    .add(*m1.pos.to_polar())  # (9), (10): the distance, and the position's angle
    .add(*m1.vel.to_polar())  # (11), (12): the speed and direction
    .add(*m1.vel.degrees())  # (13)
)

sol = ride.solve(
    m1.pos.x, m1.pos.y, m1.pos.mag, m1.vel.y, m1.vel.mag, m1.vel.angle, m1.vel.angle_deg
)
```

- **`cliff` doesn't change,** `eliminate(m01.dt)` included.
- **The equations added:**

  ```
  (9)   m1.pos.mag = sqrt(m1.pos.x**2 + m1.pos.y**2)
  (10)  m1.pos.angle = atan2(m1.pos.y, m1.pos.x)
  (11)  m1.vel.mag = sqrt(m1.vel.x**2 + m1.vel.y**2)
  (12)  m1.vel.angle = atan2(m1.vel.y, m1.vel.x)
  (13)  m1.vel.angle_deg = 180*m1.vel.angle/pi
  ```

  (10) is new: `to_polar()` gives the position's angle too. Nothing
  wants it, and it doesn't reach the formulas.
- **The comment lines:**

  ```
  # m1.pos.x = m1.t*(m0.vel.x + m1.vel.x)/2                                            4.5
  # m1.pos.y = m1.t*(-g*m1.t + 2*m0.vel.y)/2                                           -1.225
  # m1.pos.mag = sqrt(m1.t**2*((m0.vel.x + m1.vel.x)**2 + (g*m1.t - 2*m0.vel.y)**2))/2   4.66
  # m1.vel.y = -g*m1.t + m0.vel.y                                                      -4.9
  # m1.vel.mag = sqrt(m1.vel.x**2 + (g*m1.t - m0.vel.y)**2)                            10.25
  # m1.vel.angle = atan2(-g*m1.t + m0.vel.y, m1.vel.x)                                 -0.499
  # m1.vel.angle_deg = 180*atan2(-g*m1.t + m0.vel.y, m1.vel.x)/pi                      -28.6
  ```

- **`BOOK`:** `Answer(sol, m1.pos.mag, "4.7")`,
  `Answer(sol, m1.vel.mag, "10.2")`, `Answer(sol, m1.vel.angle_deg, "-29")`.
  The other three don't change.
- **The docstring.** "The distance, speed and angle are written by hand
  from the components, as in the old script" becomes: the distance is
  the position's magnitude, from `m1.pos.to_polar()`, and the speed and
  direction come from `m1.vel.to_polar()` and `m1.vel.degrees()`. The
  old script wrote them by hand. The paragraph on `eliminate(m01.dt)`
  stays, until 005.

#### 3.7

```python
launch = (
    ...
    .known(g, 9.80)  # m/s²
    .add(*b0.vel.from_polar())  # (10), (11): the launch
    .known(b0.vel.mag, 37.0)  # m/s
    .known(b0.vel.angle, sp.N(sp.rad(53.1)))  # degrees to radians
)

# The speed and direction: (12), (13).
speed = launch.add(*b1.vel.to_polar())
# The angle in degrees, (14), then the old script's by-hand step.
flight = speed.add(*b1.vel.degrees()).eliminate(b1.vel.angle)
```

- **The wants** rename: `b1_vel_mag` becomes `b1.vel.mag`,
  `b1_vel_angle` `b1.vel.angle`, `b1_vel_angle_deg` `b1.vel.angle_deg`.
- **The comment lines.** SymPy orders the new names differently, so
  some terms move. Renamed back, each is the old row.

  ```
  # (a)
  # b1.pos.x = b0.vel.mag*b1.t*cos(b0.vel.angle)                       44.4
  # b1.pos.y = b1.t*(-g*b1.t + 2*b0.vel.mag*sin(b0.vel.angle))/2       39.6
  # b1.vel.x = b0.vel.mag*cos(b0.vel.angle)                            22.2
  # b1.vel.y = -g*b1.t + b0.vel.mag*sin(b0.vel.angle)                  9.99
  # b1.vel.mag = sqrt(g**2*b1.t**2 - 2*g*b0.vel.mag*b1.t*sin(b0.vel.angle) + b0.vel.mag**2)
  #                                                                    24.36
  # b1.vel.angle_deg = 180*atan2(-g*b1.t + b0.vel.mag*sin(b0.vel.angle),
  #                              b0.vel.mag*cos(b0.vel.angle))/pi     24.2
  # sol_a_radians
  # b1.vel.angle = atan2(-g*b1.t + b0.vel.mag*sin(b0.vel.angle),
  #                      b0.vel.mag*cos(b0.vel.angle))                 0.4225
  # (b)
  # b1.t = b0.vel.mag*sin(b0.vel.angle)/g                              3.02
  # b1.pos.y = b0.vel.mag**2*sin(b0.vel.angle)**2/(2*g)                44.7
  # (c)
  # b1.t = 2*b0.vel.mag*sin(b0.vel.angle)/g                            6.04
  # b1.pos.x = b0.vel.mag**2*sin(2*b0.vel.angle)/g                     134
  # b1.vel.x = b0.vel.mag*cos(b0.vel.angle)                            22.2
  # b1.vel.y = -b0.vel.mag*sin(b0.vel.angle)                           -29.6
  # b1.vel.angle_deg = 180*atan2(-b0.vel.mag*sin(b0.vel.angle),
  #                              b0.vel.mag*cos(b0.vel.angle))/pi     -53.1
  ```

- **`BOOK`:** the same twelve answers, with `b1.vel.mag` and
  `b1.vel.angle_deg`.
- **The docstring.** "The launch is polar one way, in the script's own
  symbols, and the speed and angle at 2.00 s are written by hand"
  becomes: the launch is `b0.vel.from_polar()`, and the speed and
  direction at 2.00 s are `b1.vel.to_polar()` and `b1.vel.degrees()`.
  The old script wrote them in its own symbols. The paragraph on the
  by-hand step stays, in the new names: `b1.vel.angle`,
  `b1.vel.angle_deg`.

#### 3.8

```python
launch = (
    System()
    .add(*p.kinematics())  # (1) to (7)
    .add(*eq_flat(p01.a.y, -g, p0.vel.x, p1.vel.x))  # (8), (9): projectile motion
    .known({p0.pos.x: 0, p0.pos.y: 0, p01.a.x: 0, p0.t: 0})  # from the origin, at t = 0
    .eliminate_zeros()
    # Launched at speed v0 and angle α0, polar one way: (10), (11).
    .add(*p0.vel.from_polar())
    .known(g)
    .known(p0.vel.mag)  # v0
    .known(p0.vel.angle)  # α0
)

# (a) The highest point, where the vertical velocity is zero.
top = launch.known(p1.vel.y, 0).eliminate_zeros()
sol_top = top.solve(p1.t, p1.pos.y)

# (b) Back at the launch height.
back = launch.known(p1.pos.y, 0).eliminate_zeros()
sol_range = back.solve(p1.t, p1.pos.x)
```

- **The formulas don't change,** not even in the new names. The
  comments and `BOOK` stay.
- **`top` and `back` change.** They keep (10) and (11) as written,
  where the eliminations had put `p0.vel.mag*cos(p0.vel.angle)` into
  (4) to (9), and they have no (12) or (13).
- **The docstring.** "The launch is polar both ways, with
  `p0.vel.from_polar()` and `p0.vel.to_polar()`" becomes "polar one
  way, with `p0.vel.from_polar()`". The paragraph on the by-hand steps
  is replaced by one that says each part solves all at once. The old
  script eliminated `p0.vel.x` by hand, and with the launch polar both
  ways this port eliminated `p0.vel.x` and `p0.vel.y` through the polar
  equations, or the solve found no roots. One way, neither step is
  needed.

#### 3.9

```python
from equarium import System, eq_flat

window = (
    ...
    .known(b0.pos.y, 8.0)  # m
    .add(*b0.vel.from_polar())  # (10), (11)
    .known(b0.vel.mag, 10.0)  # m/s
    .known(b0.vel.angle, sp.N(sp.rad(-20.0)))  # degrees to radians
)

sol = window.solve(b1.pos.x, b1.t)  # about 1.6 s
```

- **The formulas don't change,** in the new names either, and nor do
  the roots: −15.7 and −1.67, 9.17 and 0.976. The comments stay.
- **`__main__`:** `sol.system.show_history()` and its `print()` go.
  They showed `eliminating()`'s steps.
- **The docstring.** "The launch is polar both ways, … and
  `eliminating()` solves it, as the old version 2 did" becomes: the
  launch is polar one way, `b0.vel.from_polar()`, so it solves all at
  once, in about 1.6 s. The old version 2 had it polar both ways, so
  `all_at_once` found no roots, and `eliminating()` solved it, in about
  6 s. `tests/test_strategies.py` keeps that lesson, written out. "The
  time is added as a want, solved with x in no more time than x alone"
  stays true: both take about 1.5 s.

#### 3.10

```python
dart_start = (
    System()
    .add(*d.kinematics())  # (1) to (7)
    .add(*d0.vel.from_polar())  # (8), (9)
    .add(*eq_flat(d01.a.y, -g, d0.vel.x, d1.vel.x))  # (10), (11): projectile motion
    ...
)
```

- **The eliminations follow:** the same 19, in the same order. The
  dart's eight leave (8) and (9), as before, and nothing else. Both
  ways, they also left (10) and (11), the equations back to polar,
  rewritten in `d1.pos` and `d1.t`.
- **The formulas and the show-that don't change.** The comments, the
  `BOOK` and `STAGES` stay.
- **The docstring.** "the dart's launch polar both ways" becomes "the
  dart's launch polar one way, where the old script had it both ways".
  Add that the dart's eliminations leave the same two equations.

#### 4.1

- **`main.py`:** `R_angle_deg = sp.Symbol("R_angle_deg")` goes. In
  `belt`, `.add(*R.degrees())  # (11)`. In `book_step`,
  `.add(*R.degrees())  # (3)`. The wants are `R.angle_deg`.
- **`main_step_by_step.py`:** it imports `F1, F2, F3, R, sol_book`.
  `degrees = ys.add(*R.degrees())  # (11)`, and
  `sol_deg = degrees.solve(R.angle_deg)`.
- **The comment lines.** After `sol`, in both modules:

  ```
  # R.angle_deg = 180*atan2(R.y's formula, R.x's)/pi   141.59
  ```

  After `sol_book`, in `main.py`:

  ```
  # R.angle_deg = 180*atan2(R.y, R.x)/pi   141.34
  ```

- **`BOOK`,** in both: `Answer(sol_book, R.angle_deg, "141")`.
- **The docstrings.** `main.py`'s says its degrees equation is
  `R.degrees()`, beside "the physics code's lone vectors, `from_polar()`
  and `to_polar()`".

### Tests

**`tests/old_names.py`: the per-module map.** 003 needs one. A symbol
that a script made itself becomes a `Var` here, and the rule can't
reach its old name:

- 3.6's `dist`, `vel_mag`, `vel_angle` and `vel_angle_deg` are
  `m1.pos.mag` and so on now. The rule has no position polar parts and
  no `angle_deg`.
- 3.7's `b0_vel_mag` is `b0.vel.mag`. The rule gives it `b_0_v_mag`,
  `make_states_model`'s name, which 3.9 needs. 3.7's old script named
  its launch itself. So the map is per module, and it wins over the
  rule.
- 4.1's `R_angle_deg` is `R.angle_deg`, in both modules.

```python
SCRIPT_NAMES: Mapping[str, Mapping[Var, str]] = {
    "ch03.examples.n06.main": {
        Var("m", "1", "pos", "mag"): "dist",
        Var("m", "1", "vel", "mag"): "vel_mag",
        Var("m", "1", "vel", "angle"): "vel_angle",
        Var("m", "1", "vel", "angle_deg"): "vel_angle_deg",
    },
    "ch03.examples.n07.main": {
        Var("b", "0", "vel", "mag"): "b0_vel_mag",
        Var("b", "0", "vel", "angle"): "b0_vel_angle",
        Var("b", "1", "vel", "mag"): "b1_vel_mag",
        Var("b", "1", "vel", "angle"): "b1_vel_angle",
        Var("b", "1", "vel", "angle_deg"): "b1_vel_angle_deg",
    },
    "ch04.examples.n01.main": {Var("R", "", "angle_deg"): "R_angle_deg"},
    "ch04.examples.n01.main_step_by_step": {Var("R", "", "angle_deg"): "R_angle_deg"},
}
```

- **The key is the module,** under `examples.up_15e`, as `OLD` names
  it. The map is keyed by the `Var`, since a name can print alike.
- **`old_name(symbol, module="")`** looks in the module's map first,
  then follows the rules. **`old_str(expr, module="")`** passes the
  module on. Without a module, nothing changes: the rules alone.
- **The rules don't change.** `angle_deg` and a position's polar parts
  still raise without a map.
- **The module docstring** says the map holds the names an old script
  made itself, which a reshape turned into `Var`s, and that it wins
  over the rules. 004 adds 2.5's `meet.t`, and 006 4.5's `b.mass`.
- Scratch used exactly this. Its diff to the current file is the map,
  the `Mapping` import, the two parameters, and three lines in
  `old_name`.

**`tests/test_old_outputs.py`:**

- **The rows don't change,** not by one character: the 66 rows of
  `OLD`, `R_MAG_4_1`, `R_ANGLE_4_1`, `OLD_GIVENS`, `OLD_3_10` and the
  count.
- **`test_old_output` passes the module** to all three lookups:
  `old_name(w, module) == want`, `old_str(root.formula(symbol), module)`
  and `old_name(sym, module) == name` for `OLD_GIVENS`.
- **`test_3_10_show_that` loses `@pytest.mark.slow`.** 3.10 imports in
  about 4 s. Its body doesn't change.
- **The module docstring** says the names a script made itself are
  renamed back through the module's map.
- **New tests of the map:**
  - in its module, a symbol gets its script's name: 3.6's
    `m1.pos.mag` is `dist` and `m1.vel.angle_deg` `vel_angle_deg`, and
    4.1's `R.angle_deg` is `R_angle_deg`;
  - it wins over the rule: 3.7's `b0.vel.mag` is `b0_vel_mag`, but
    `b_0_v_mag` without a module, and in 3.9;
  - it applies in its module only: `m1.pos.mag` in 3.8 raises;
  - every module in `SCRIPT_NAMES` has rows in `OLD`, so a typo in a
    key is loud.
- **`test_old_name_of_a_var_the_rule_doesnt_know`** stays as it is: no
  module, so its six symbols still raise.

**`tests/test_physics.py`:**

- **Polar:** `test_polar_one_way_each` also checks
  `d0.vel.degrees()` as `["Eq(d0.vel.angle_deg, 180*d0.vel.angle/pi)"]`.
- **Misuses at run time:** `.degrees()` of an `X` vector raises
  `UsageError`, reached through `getattr` as the others are.
- **`BookNotation`:** each row of the table above, with and without the
  owner `P`, and a lone vector's owner ignored, as for `θR`.
- **The test that other symbols print their names** used
  `Var("m", "0", "vel", "angle_deg")` and `Var("F1", "", "angle_deg")`,
  which now have rows. Use an edge's, such as
  `Var("m", "01", "a", "angle_deg")`, beside `m01.a.mag`.

**`tests/physics_misuse.py`:** add, with the other polar misuse:

```python
f.degrees()  # pyright: ignore[reportAttributeAccessIssue]
```

Check once that it bites: put the same ignore on `R.degrees()`, see
`uv run pyright` fail, and take it out.

**`tests/slow_examples.py`:** the set is empty. 3.9 and 3.10 leave it.

```python
SLOW_EXAMPLES: frozenset[str] = frozenset()
```

Keep the file and its use in the two test files, for the next slow
module. Its docstring says that 3.9 and 3.10 left the set in
increment 003 of the 004 series, once one-way polar made them fast.

**`tests/test_examples.py`** and **`tests/test_strategies.py`:** no
change.

### A row whose formula changes

**Not built here,** since no row needs it. The spec's rule, made
concrete for the first increment that has such a row. That's likely
005, where 3.6's v1x stops being a given.

- **The row stays as it is,** the old formula as the record.
- **A table beside `OLD`** holds the new formula, in the new names, as
  `str()` prints it:

  ```python
  # The rows a reshape changed: (module, solution, the old formula) to
  # the new formula, in the new names. The row keeps the old formula as
  # the record.
  RESHAPED: dict[tuple[str, str, str], str] = {...}
  ```

  The key has the old formula, since a module and solution can have
  two rows for one want (3.9's two roots).
- **`test_old_output` picks the formula to compare:**

  ```python
  new = RESHAPED.get((module, solution, formula))
  if new is None:  # renamed back, verbatim
      formulas = [old_str(root.formula(symbol), module) for root in sol.roots]
      expected = formula
  else:  # reshaped: the new formula, verbatim
      formulas = [str(root.formula(symbol)) for root in sol.roots]
      expected = new
  assert expected in formulas
  root = sol.roots[formulas.index(expected)]
  ```

  The want is still found by its old name, through the rules or the
  map. The number is compared with the old number as now, with
  `OLD_GIVENS`.
- **A guard test:** every key of `RESHAPED` is a row of `OLD`.
- **The checkpoint that builds it** lists each row it adds, with the
  new formula.

### If a formula moves

Every row of `tests/test_old_outputs.py`, renamed back through the
rules and the map, must come out verbatim, and so must 3.10's
show-that. The scratch run found none that moved. If one does, stop.
Don't change the row, the module's equations, or the order of anything
to make it pass, and don't add the reshape table. Report the row, what
came out, and what you think moved it. The same holds for a `BOOK` that
stops matching.

## Docs

- **The docstrings** of `physics/__init__.py`, `polar.py`,
  `vectors.py` and `notation.py`, as above.
- **The package `README.md`** doesn't change. `uv run pytest -m slow`
  is still "a few minutes in all": about 5 min.
- **The series [README](../README.md):** mark 003 done in its
  increments table, and update its status line and the "2 of 7 done".
  Leave the commit cell and this page's status line for the manager.
- **The [series map](../../README.md):** 004's status says 3 of 7
  increments are done.
- **Don't edit** `spec.md`, `charter.md` or this page. If something
  here is wrong, say so in the report.

## Check and commit

- **`uv run pytest`** passes: the 315 fast tests, the 5 that were slow
  (3.9's and 3.10's `test_book`, 3.9's two rows, 3.10's show-that), and
  yours. It takes a few seconds longer, since 3.9 and 3.10 now import
  in it. Report how long it and `tests/test_examples.py` take.
- **`uv run pytest -m slow`** passes the 3 left, in
  `tests/test_strategies.py`, in about 5 min. Run it in the background.
- **`uv run pyright`:** 0 errors and 0 warnings, over `src`, `tests`
  and `examples`, `tests/physics_misuse.py` included.
- **Every changed module** runs with
  `uv run python -m examples.up_15e.ch03.examples.n06.main` and so on.
- **The times.** Report each changed module's import time. If 3.10's
  is 5 s or more on your run, keep it in `SLOW_EXAMPLES` and its
  show-that marked slow, and say so.
- **No by-hand polar left.**
  `grep -rn "b0_vel\|b1_vel\|vel_mag\|vel_angle\|R_angle_deg\|using=\|strategy=" examples/up_15e/ch03 examples/up_15e/ch04`
  finds nothing. Today it finds the six modules that change. And
  `to_polar()` is called only in 3.6, 3.7 and 4.1.
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
- that no formula moved, or, if one did, the row and what came out
  (you stopped there);
- any name you chose differently from this page, such as
  `SCRIPT_NAMES`, and why;
- what pyright needed beyond the `cast`s this page names;
- anything in the spec or this checkpoint that was wrong or unclear,
  and what you did instead.

Then stop. Increment 004, events, is a separate checkpoint.
