# physics 005: the projectile setup

**Status:** Done at `f505be6` and reviewed (2026-11-09).

If you've been told to read this file, this is the whole assignment.
Build it, check it, commit it, report, and stop.

## Goal

The third reshape, and the first that changes a formula. Five examples
write projectile motion by hand, and a helper takes its place. That
means:

- **`projectile.py`, with `Setup` and the projectile setup.**
  `d01.projectile(g)`, on an `XY` edge, returns a `Setup`: the
  equations `d01.a.y = -g` and `d0.vel.x = d1.vel.x`, and the knowns
  `{d01.a.x: 0}`. The example adds both.
- **3.6 to 3.10 use it,** in place of their own `a_y = -g`, `v0x = v1x`
  and `a_x = 0` lines. 3.10 uses it twice, for the dart and the monkey.
- **3.6's v1x is derived, not given.** Its by-hand `eliminate(m01.dt)`
  goes, as the user chose, and the book's v_x = 9.0 m/s becomes an
  `Answer`.
- **3.10's monkey fits the setup, with one more elimination.** Its
  `m1.vel.x = 0` stops being a given, so `m1.vel.x` is eliminated by
  hand before the old script's five.
- **`tests/test_old_outputs.py` gains the `RESHAPED` table,** which
  [checkpoint 003](003-polar-and-degrees.md) designs under "A row whose
  formula changes".

**Five formulas change, all in 3.6, all for one reason.** They are
listed next, with the one new `Answer`. Everything else comes out as it
does today: the other 61 rows, renamed back, 3.10's show-that, and
every other `BOOK`. The scratch run compared every `System` and
`Solution` of the five modules, not only the rows.

**Not in this increment:**

- `mass` and `newton` (006).
- **The origin and the clock.** Each example still sets its own zero
  positions and times. 3.9 still starts at y0 = 8.0 and ends at y1 = 0.
- **The by-hand steps the spec keeps.** 3.7's `eliminate(b1.vel.angle)`
  stays. 3.10's 19 eliminations stay, in the same order, with one more
  before the monkey's five, `m1.vel.x` (see 3.10 below).
- **`clear_zero_denominators`.** The core doesn't change.
- **Options.** `projectile(g)` takes gravity and nothing else. y points
  up.
- **Book notation.** The setup has no symbols of its own, so
  `notation.py` doesn't change.
- **Labels for the setup's equations.** 3.10 still picks
  `dart.equation("8")` by number.
- **`tests/test_strategies.py`.** Its 3.9, written out, doesn't change.

## The formulas that change

Each formula here is as `str()` prints it. The scratch run made every
one, on a copy of the repo at `3e4bdc3`.

**Why they move.** 3.6's `m1.vel.x` isn't a given any more. The setup's
`m0.vel.x = m1.vel.x` gives it, from the given `m0.vel.x`. So a formula
that had `m1.vel.x` has `m0.vel.x` in its place. Checked with SymPy:
each new formula is the old one with `m0.vel.x` substituted for
`m1.vel.x`, character for character. The numbers don't change, since
both velocities were 9.0.

**It is the givens, not the solver.** Give `m1.vel.x` again, with the
old by-hand step, and all six old rows of 3.6 come back verbatim, from
the new module. A new test keeps that true.

### Five rows of `tests/test_old_outputs.py`

All five are rows of the module `ch03.examples.n06.main` and the
solution `sol`. Each row keeps its old formula, as the record.
`RESHAPED` pins the new one, in the new names. The number is still
compared with the row's old number.

**Row 1, the want `m_1_x`,** which is `m1.pos.x`. Number
4.50000000000000.

```
old  m_1_t*(m_0_v_x + m_1_v_x)/2      the row, in the old names
     m1.t*(m0.vel.x + m1.vel.x)/2     the same, as 3.6 prints it today
new  m0.vel.x*m1.t                    pinned in RESHAPED
     m_0_v_x*m_1_t                    the same, renamed back
```

x was t times the average of the two given velocities. With v1x = v0x,
the average is v0x. It is the book's x = v0x t.

**Row 2, the want `dist`,** which is `m1.pos.mag`. Number
4.66375653309647.

```
old  sqrt(m_1_t**2*((m_0_v_x + m_1_v_x)**2 + (g*m_1_t - 2*m_0_v_y)**2))/2
     sqrt(m1.t**2*((m0.vel.x + m1.vel.x)**2 + (g*m1.t - 2*m0.vel.y)**2))/2
new  sqrt(m1.t**2*(4*m0.vel.x**2 + (g*m1.t - 2*m0.vel.y)**2))/2
     sqrt(m_1_t**2*(4*m_0_v_x**2 + (g*m_1_t - 2*m_0_v_y)**2))/2
```

`(v0x + v1x)**2` is `(2*v0x)**2`, which SymPy prints as `4*v0x**2`.

**Row 3, the want `vel_mag`,** which is `m1.vel.mag`. Number
10.2474387043788.

```
old  sqrt(m_1_v_x**2 + (g*m_1_t - m_0_v_y)**2)
     sqrt(m1.vel.x**2 + (g*m1.t - m0.vel.y)**2)
new  sqrt(m0.vel.x**2 + (g*m1.t - m0.vel.y)**2)
     sqrt(m_0_v_x**2 + (g*m_1_t - m_0_v_y)**2)
```

The speed's x part was the given v1x. It is v0x now.

**Row 4, the want `vel_angle`,** which is `m1.vel.angle`. Number
-0.498567905638218.

```
old  atan2(-g*m_1_t + m_0_v_y, m_1_v_x)
     atan2(-g*m1.t + m0.vel.y, m1.vel.x)
new  atan2(-g*m1.t + m0.vel.y, m0.vel.x)
     atan2(-g*m_1_t + m_0_v_y, m_0_v_x)
```

**Row 5, the want `vel_angle_deg`,** which is `m1.vel.angle_deg`.
Number -28.5658367937466.

```
old  180*atan2(-g*m_1_t + m_0_v_y, m_1_v_x)/pi
     180*atan2(-g*m1.t + m0.vel.y, m1.vel.x)/pi
new  180*atan2(-g*m1.t + m0.vel.y, m0.vel.x)/pi
     180*atan2(-g*m_1_t + m_0_v_y, m_0_v_x)/pi
```

Rows 4 and 5 are row 3's change again: the angle's x part was v1x.

### The 61 rows that don't change

- **3.6's sixth row, `m_1_y`:** `m_1_t*(-g*m_1_t + 2*m_0_v_y)/2`,
  -1.22500000000000. It never had `m1.vel.x`.
- **3.7's twelve rows, 3.8's one and 3.9's two.** Their modules move to
  the setup, but their equations are the same, in the same order.
- **The other 45 rows,** of modules this increment doesn't touch.
- **3.10 has no row.** Its show-that, `OLD_3_10`, doesn't change.

### One new `Answer`, in 3.6's `BOOK`

```python
Answer(sol, m1.vel.x, "9.0"),  # m/s, a given in the old script
```

- **Module and solution:** `ch03.examples.n06.main`, `sol`.
- **The want, its formula and its number:** `m1.vel.x = m0.vel.x`,
  9.00000000000000. It's a new want, so it has no old row.
- **Why it's new:** the book's v_x = 9.0 m/s was a given,
  `.known(m1.vel.x, 9.0)`, and a given has no `Answer`. Now it's
  derived, so the book's number checks it.
- **Where:** after `m1.pos.mag`, before `m1.vel.y`, in the wants'
  order.

### The `BOOK`s that don't change

- **3.6's other six answers** keep their symbols and printed values,
  and still match: 4.5, -1.2, 4.7, -4.9, 10.2 and -29.
- **3.7's twelve answers, 3.8's four formulas, 3.9's two answers and
  3.10's one formula** don't change, not by one character.

## Read first

- **[The spec](../spec.md).** In "Decisions": "The projectile setup",
  "The steps the helpers make unnecessary", "The examples" and "The
  tests". The 3.10 sketch. Then "### 005 the projectile setup", "How
  each increment lands" and "SymPy to watch".
- **The series [README](../README.md),** its "What's next" and the
  reviews of 001 to 004.
- **[Checkpoint 003](003-polar-and-degrees.md),** the section "A row
  whose formula changes". This page builds that design. Where it adds
  to it is said under "Tests" below.
- **[Checkpoint 004](004-events.md),** for the form, and for 3.10 as it
  is now.
- **The code:** `src/equarium/physics/particles.py` (`Edge`),
  `kinematics.py` (a plain function the method calls, with its
  `TYPE_CHECKING` import), `polar.py` (the `cast`s) and `__init__.py`.
  Also `tests/test_old_outputs.py`, `tests/old_names.py`,
  `tests/test_physics.py` and `tests/physics_misuse.py`.
- **The five modules,** `examples/up_15e/ch03/examples/n06/main.py` to
  `n10/main.py`.
- **The prototype,** outside the repo, in
  `~/.config/Claude/side-session-notes/local_9ac850c1-eb15-42fc-bbb0-61739b724d16/004-spec-prototype/`:
  `layer.py`'s `Edge.projectile`, `ch3.py` (3.8 and 3.9 with the setup)
  and `sketches.py` (3.6 and 3.10's dart with it). It's data, not the
  source: the spec and this page win. Where it differs:
  - its `projectile` returns a plain tuple, and its examples unpack it,
    `eqs, knowns = c01.projectile(g)`. Here it returns a `Setup`, as
    the spec says, and the examples read `flight.equations` and
    `flight.knowns`;
  - its method builds the equations itself. Here it calls
    `projectile.py` in one line;
  - it has no run-time check: on an `X` edge it would make a `Var`
    named `m01.a.y`. Here that raises `UsageError`;
  - its 3.6 solves six wants, without `m1.vel.x` or `m1.vel.angle`, and
    never compared its formulas with the old rows. Here 3.6 keeps its
    seven wants and gains `m1.vel.x`;
  - it ported neither 3.7 nor 3.10's monkey to the setup, and compared
    no system before and after.

## Starting point

The branch `2026-11-08-physics-redesign`, at the commit that adds this
checkpoint, on top of `3e4bdc3` (the review of 004). Check it with
`git branch --show-current`. If you're on another branch, stop and ask.
Don't switch branches, stash or reset.

`uv run pytest` passes 332 tests and deselects 3 slow ones, in about
41 s. `uv run pytest -m slow` passes those 3, in about 5 min.
`uv run pyright` reports 0 errors and 0 warnings.

Checked in scratch while writing this page, on a copy of the repo at
`3e4bdc3`, with `projectile.py` built and the five modules ported as
this page says:

- **Every `System` and `Solution`** in the five modules, renamed back
  to the old names, was compared with the same at `3e4bdc3`: the
  equations with their labels, the knowns, the wants, and every root's
  formulas and numbers.
- **3.6:** five formulas move, the five above, and nothing else in
  `sol`. Every number is the same. `m1.vel.x` is a new want,
  `m1.vel.x = m0.vel.x`, 9.0. `cliff` and `ride` differ as this page
  designs:
  - (1), `m01.dt = m1.t`, stays, and (2) to (5) keep `m01.dt`, where
    the by-hand step had put `m1.t`;
  - (9) is new, `m0.vel.x = m1.vel.x`, so the polar equations are (10)
    to (14);
  - the known `m1.vel.x = 9.0` is gone.
- **3.7, 3.8 and 3.9:** every system and solution is the same: the
  equations, their labels, the wants, the formulas and the numbers.
  Only the knowns' order differs: `a.x`, the setup's, comes first.
- **3.10:** `dart_start` and `dart` are the same, but for that order.
  `meet`, `proved`, `reached`, `agree` and `sol_t` are the same. The
  monkey differs:
  - `monkey_start` has eleven equations, not nine. (4) stays, as
    `0 = m1.vel.x/m01.dt`. (6) is `m01.v_av.x = m1.vel.x/2`, where it
    was `m01.v_av.x = 0`. (11) is new, `0 = m1.vel.x`. The known
    `m1.vel.x = 0` is gone;
  - `monkey` has the same four equations, (2), (6), (8) and (9). Only
    that known is gone.
- **The monkey fits the setup, with one more elimination.** Three ways
  were tried:
  - *The setup, and the old five eliminations.* `monkey` is left with
    six equations, (4) and (11) among them, and `agree` finds no roots:
    `sp.solve left d1.t in terms of the unknown m1.vel.x`.
  - *The setup, with `m1.vel.x` eliminated first, then the old five.*
    This page's choice. After that first step, in 0.004 s,
    `monkey_start`'s equations are the nine it has today, exactly. Then
    everything is as it is today. Eliminating `m1.vel.x` last gives the
    same `monkey`.
  - *The setup, with `m1.vel.x` still a zero known.* Every system is
    the same as today's: (11) becomes `0 = 0` and is dropped. But the
    given is redundant, which is what the setup is there to spare.
- **3.6 with `m1.vel.x` given too** still finds no roots, as the spec
  says, in 1.8 s. With the old `eliminate(m01.dt)` as well, all six old
  rows come back verbatim, renamed back, with their numbers.
- **3.6's by-hand step, kept, wouldn't change a formula.** With v1x
  derived and `eliminate(m01.dt)` kept, the same eight formulas come
  out. So the givens move the formulas, not the step. The step only
  buys time: the solve takes 0.2 s with it and 1.6 to 1.8 s without.
- **The fast suite,** with `RESHAPED` and six draft tests, passed all
  338 tests in 45 s: the 66 rows, the show-that and every `BOOK`.
  Without the `RESHAPED` lookup, exactly the five rows fail.
  `tests/test_examples.py` takes 21.5 to 21.7 s, where it took 20.4 s.
- **Pyright** reported 0 errors over `src`, `tests` and `examples`. It
  flags `m01.projectile(g)` on an `X` edge and on a `Y` edge
  (`reportAttributeAccessIssue`: `Edge[X]` isn't `Edge[XY]`). An ignore
  on a correct call fails the run. It types the result as `Setup`, and
  `.known(flight.knowns)` needs no cast.
- **The times,** each module's import in a fresh process, after SymPy
  and equarium, three runs each:

  | Module | Now | With the setup |
  |---|---|---|
  | 3.6 | 0.47 to 0.49 s | 1.88 to 1.92 s (the solve 1.8 s, was 0.3 s) |
  | 3.7 | 1.73 to 1.75 s | 1.76 to 1.78 s |
  | 3.8 | 0.54 to 0.56 s | 0.55 s |
  | 3.9 | 1.72 to 1.73 s | 1.73 to 1.74 s |
  | 3.10 | 4.07 to 4.16 s | 4.11 to 4.22 s |

  None crosses 5 s, so `SLOW_EXAMPLES` stays empty. 3.10 is the
  closest. 3.6 is slower because `m01.dt` stays an unknown.
- **The slow tests** weren't run. They are the three in
  `tests/test_strategies.py`, which imports none of the five modules.

## Build

### `projectile.py`: `Setup` and the setup

A new module. Scratch used exactly this:

```python
class Setup(NamedTuple):
    """Equations and knowns that go into a system together:
    `.add(*flight.equations).known(flight.knowns)`."""

    equations: list[sp.Eq]
    knowns: Mapping[sp.Symbol, sp.Expr]


def projectile_setup(edge: Edge[XY], g: sp.Expr) -> Setup:
    """`d01.a.y = -g` and `d0.vel.x = d1.vel.x`, with `d01.a.x` known
    zero."""
    if edge.axes.names != XY.names:
        raise UsageError(
            f"{edge.owner}{edge.where} is in {edge.axes.__name__},"
            " so it has no projectile setup"
        )
    return Setup(
        equations=[
            cast(sp.Eq, sp.Eq(edge.a.y, -g)),
            cast(sp.Eq, sp.Eq(edge.start.vel.x, edge.end.vel.x)),
        ],
        knowns={edge.a.x: sp.S.Zero},
    )
```

- **`Setup` is a named tuple,** as the spec says. It unpacks,
  `equations, knowns = d01.projectile(g)`, and compares by value.
- **`equations` is a `list[sp.Eq]`,** as every other helper returns, in
  the ports' order: `a.y = -g`, then `v0x = v1x`.
- **`knowns` is a `Mapping[sp.Symbol, sp.Expr]`,** which `System.known`
  takes as it is. The zero is `sp.S.Zero`, as in the core.
- **`g` is the example's symbol.** Its value stays the example's known,
  `.known(g, 9.80)`.
- **At run time,** an edge that isn't in `XY` raises `UsageError`
  before any equation is made:
  `m01 is in X, so it has no projectile setup`. The message reads as
  `Vector`'s does.
- **As strings:**

  ```
  Particle("d", 2, XY).edge(0, 1).projectile(g)
    equations  Eq(d01.a.y, -g)
               Eq(d0.vel.x, d1.vel.x)
    knowns     {d01.a.x: 0}

  Particle("p", 3, XY).edge(1, 2).projectile(g)
    equations  Eq(p12.a.y, -g)
               Eq(p1.vel.x, p2.vel.x)
    knowns     {p12.a.x: 0}
  ```

- **Imports:** `Mapping`, `TYPE_CHECKING`, `NamedTuple` and `cast`,
  `UsageError`, `XY`, and `Edge` under `TYPE_CHECKING`, as
  `kinematics.py` imports `Particle`. `particles.py` imports this
  module, so there is no cycle.
- **The module docstring** says what the setup is: what projectile
  motion adds to an `XY` edge's kinematics, with y up. Gravity is the
  only acceleration, so `a.y = -g`, the horizontal velocity doesn't
  change, and `a.x` is zero. `d01.projectile(g)` returns a `Setup`, and
  the example adds both parts. The origin and the clock stay the
  example's.

### `particles.py`: `Edge.projectile`

```python
    def projectile(self: Edge[XY], g: sp.Expr) -> Setup:
        """The projectile setup: `a.y = -g` and `v0x = v1x`, with `a.x`
        known zero."""
        return projectile_setup(self, g)
```

- **A one-line call,** after `v_av`, as `Particle.kinematics` calls
  `kinematics_equations`.
- **`self: Edge[XY]`,** so pyright flags it on an `X` or a `Y` edge, as
  it flags `f.from_polar()`.
- **Imports:** `XY` beside `Axes`, and `Setup` and `projectile_setup`.
- **`Edge`'s docstring** gains a sentence: an `XY` edge also has the
  projectile setup, `m01.projectile(g)`.

### `__init__.py`

- **Re-export `Setup`,** in `__all__`, in order, after `Particle`.
- **The docstring** gains a paragraph: an `XY` edge has the projectile
  setup, `d01.projectile(g)`, a `Setup` of equations, `d01.a.y = -g`
  and `d0.vel.x = d1.vel.x`, and knowns, `d01.a.x` zero. The example
  adds both, `.add(*flight.equations).known(flight.knowns)`, and sets
  its own origin and clock.

### The examples

| Module, under `examples/up_15e/` | What changes |
|---|---|
| `ch03/examples/n06/main.py` | `flight = m01.projectile(g)` replaces `sp.Eq(m01.a.y, -g)` and the known `m01.a.x: 0`. `.eliminate(m01.dt)` and `.known(m1.vel.x, 9.0)` go. `m1.vel.x` is a want, and an `Answer`. |
| `ch03/examples/n07/main.py` | `motion = b01.projectile(g)` replaces the `eq_flat` line and the known `b01.a.x: 0`. |
| `ch03/examples/n08/main.py` | `flight = p01.projectile(g)`, likewise. |
| `ch03/examples/n09/main.py` | `flight = b01.projectile(g)`, likewise. |
| `ch03/examples/n10/main.py` | `flight = d01.projectile(g)` for the dart, `fall = m01.projectile(g)` for the monkey. The monkey's known `m1.vel.x: 0` goes, and `m1.vel.x` is eliminated first. |

**In every module:**

- **The setup's name.** `flight`, as in the spec's sketch. 3.7 already
  has a system named `flight`, so its setup is `motion`. The monkey's
  is `fall`.
- **The setup goes in where the old lines were:**
  `.add(*flight.equations)` in place of the old `add`, then
  `.known(flight.knowns)`, then the example's own zeros, without `a.x`.
- **The labels.** 3.7, 3.8, 3.9 and 3.10's dart keep theirs: the same
  two equations, in the same order. 3.6 gains (9), so its polar
  equations move to (10) to (14). 3.10's monkey gains (11). Nothing
  picks a label that moved: 3.10's `equation("8")`, `("9")`, `("2")`
  and `("6")` are the same equations.
- **The knowns' order.** `a.x` comes first now. `show()` prints the
  knowns in that order. No formula depends on it.
- **Everything else stays:** the other knowns, the wants, the solves
  and the eliminations, in the same order. Remove `eq_flat` from the
  imports of 3.7, 3.8 and 3.9. 3.10 still uses it.
- **Comments and docstrings use the new shape.** Each docstring says
  that projectile motion is the projectile setup, and what the old
  script wrote. The lines are below.

#### 3.6

```python
flight = m01.projectile(g)

cliff = (
    System()
    .add(*m.kinematics())  # (1) to (7)
    .add(*flight.equations)  # (8), (9): projectile motion
    .known(flight.knowns)  # m01.a.x = 0
    .known({m0.pos.x: 0, m0.pos.y: 0, m0.t: 0})  # from the edge, at t = 0
    .eliminate_zeros()
    .known(m0.vel.x, 9.0)  # m/s, horizontal
    .known(m0.vel.y, 0.0)  # m/s
    .known(g, 9.8)  # m/s²
    .known(m1.t, 0.50)  # s
)

ride = (
    cliff
    .add(*m1.pos.to_polar())  # (10), (11): the distance, and the position's angle
    .add(*m1.vel.to_polar())  # (12), (13): the speed and direction
    .add(*m1.vel.degrees())  # (14)
)

sol = ride.solve(  # about 1.8 s
    m1.pos.x,
    m1.pos.y,
    m1.pos.mag,
    m1.vel.x,
    m1.vel.y,
    m1.vel.mag,
    m1.vel.angle,
    m1.vel.angle_deg,
)
# m1.pos.x = m0.vel.x*m1.t                                                     4.5
# m1.pos.y = m1.t*(-g*m1.t + 2*m0.vel.y)/2                                     -1.225
# m1.pos.mag = sqrt(m1.t**2*(4*m0.vel.x**2 + (g*m1.t - 2*m0.vel.y)**2))/2      4.66
# m1.vel.x = m0.vel.x                                                          9.0
# m1.vel.y = -g*m1.t + m0.vel.y                                                -4.9
# m1.vel.mag = sqrt(m0.vel.x**2 + (g*m1.t - m0.vel.y)**2)                      10.25
# m1.vel.angle = atan2(-g*m1.t + m0.vel.y, m0.vel.x)                           -0.499
# m1.vel.angle_deg = 180*atan2(-g*m1.t + m0.vel.y, m0.vel.x)/pi                -28.6

BOOK: list[Answer] = [  # University Physics, 15th ed.
    Answer(sol, m1.pos.x, "4.5"),  # m
    Answer(sol, m1.pos.y, "-1.2"),  # m
    Answer(sol, m1.pos.mag, "4.7"),  # m
    Answer(sol, m1.vel.x, "9.0"),  # m/s, a given in the old script
    Answer(sol, m1.vel.y, "-4.9"),  # m/s, a new want
    Answer(sol, m1.vel.mag, "10.2"),  # m/s
    Answer(sol, m1.vel.angle_deg, "-29"),  # degrees
]
```

- **Three lines go:** `.eliminate(m01.dt)  # see the docstring`,
  `.known(m1.vel.x, 9.0)  # m/s`, and the comment "The book's
  v_x = 9.0 m/s is a given here, so it has no Answer."
- **`ride`, as `show()` prints it:**

  ```
  (1)  m01.dt = m1.t
  (2)  m01.v_av.x = m1.pos.x/m01.dt
  (3)  m01.v_av.y = m1.pos.y/m01.dt
  (4)  0 = (-m0.vel.x + m1.vel.x)/m01.dt
  (5)  m01.a.y = (-m0.vel.y + m1.vel.y)/m01.dt
  (6)  m01.v_av.x = m0.vel.x/2 + m1.vel.x/2
  (7)  m01.v_av.y = m0.vel.y/2 + m1.vel.y/2
  (8)  m01.a.y = -g
  (9)  m0.vel.x = m1.vel.x
  (10)  m1.pos.mag = sqrt(m1.pos.x**2 + m1.pos.y**2)
  (11)  m1.pos.angle = atan2(m1.pos.y, m1.pos.x)
  (12)  m1.vel.mag = sqrt(m1.vel.x**2 + m1.vel.y**2)
  (13)  m1.vel.angle = atan2(m1.vel.y, m1.vel.x)
  (14)  m1.vel.angle_deg = 180*m1.vel.angle/pi
  knowns: m01.a.x = 0, m0.pos.x = 0, m0.pos.y = 0, m0.t = 0, m0.vel.x = 9.0, m0.vel.y = 0.0, g = 9.8, m1.t = 0.5
  ```

- **The docstring's second paragraph.** "Its four zero equations, in
  its `eq_flat` with `m01.a.y = -g`, are zero knowns here" becomes:
  projectile motion is the projectile setup, `m01.projectile(g)`,
  which is `m01.a.y = -g` and `m0.vel.x = m1.vel.x`, with `m01.a.x`
  known zero. The old script wrote `m01.a.y = -g` itself, and gave
  both horizontal velocities. Its other three zero equations, the
  origin and the clock, are zero knowns here. "So is `m1.vel.x = 9.0`:
  the book's v_x is a given here" goes. "with the velocity's
  y-component added" becomes "with the velocity's components added".
- **The docstring's third paragraph,** on `eliminate(m01.dt)`, is
  replaced. The new one says:
  - the book's v_x = 9.0 m/s is an answer here, not a given. Only
    `m0.vel.x` is given, and the setup's `m0.vel.x = m1.vel.x` gives
    `m1.vel.x`;
  - so the formulas have `m0.vel.x` where the old script's had
    `m1.vel.x`;
  - with `m1.vel.x` given too, as in the old script, the solve finds
    no roots. Equation (4), `0 = (-m0.vel.x + m1.vel.x)/m01.dt`, then
    has `m01.dt` as its only unknown, and SymPy can't solve it for
    that;
  - the port had a step for that, `eliminate(m01.dt)`, where the old
    library's `clear_zero_denominators` did the work. It isn't needed
    any more.

#### 3.7

```python
from equarium import System

motion = b01.projectile(g)

launch = (
    System()
    .add(*b.kinematics())  # (1) to (7)
    .add(*motion.equations)  # (8), (9): projectile motion
    .known(motion.knowns)  # b01.a.x = 0
    .known({b0.pos.x: 0, b0.pos.y: 0, b0.t: 0})  # from the ground, at t = 0
    .eliminate_zeros()
    ...
)
```

- **Nothing else changes:** `speed`, `flight`, the four solves, their
  comments and the `BOOK`.
- **The docstring** gains a sentence, before "Its four zero equations":
  projectile motion is the projectile setup, `b01.projectile(g)`, which
  is the old script's `b01.a.y = -g` and `b0.vel.x = b1.vel.x`, with
  its zero `b01.a.x`.

#### 3.8

```python
from equarium import System

flight = p01.projectile(g)

launch = (
    System()
    .add(*p.kinematics())  # (1) to (7)
    .add(*flight.equations)  # (8), (9): projectile motion
    .known(flight.knowns)  # p01.a.x = 0
    .known({p0.pos.x: 0, p0.pos.y: 0, p0.t: 0})  # from the origin, at t = 0
    .eliminate_zeros()
    ...
)
```

- **Nothing else changes:** `top`, `back`, the two solves, their
  comments and the `BOOK`.
- **The docstring** gains the same sentence, with `p01` and `p0`,
  before "Its zero equations are zero knowns here".

#### 3.9

```python
from equarium import System

flight = b01.projectile(g)

window = (
    System()
    .add(*b.kinematics())  # (1) to (7)
    .add(*flight.equations)  # (8), (9): projectile motion
    .known(flight.knowns)  # b01.a.x = 0
    .known({b0.pos.x: 0, b0.t: 0, b1.pos.y: 0})  # b1.pos.y: it hits the ground
    .eliminate_zeros()
    ...
)
```

- **Nothing else changes:** the solve, both roots, their comments and
  the `BOOK`. The origin stays at the ground, with `b0.pos.y` 8.0 and
  `b1.pos.y` zero: the setup doesn't set them.
- **The docstring** gains the same sentence, before "Its four zero
  equations".

#### 3.10

```python
# The dart.
d = Particle("d", 2, XY)
d0, d1 = d.states
d01 = d.edge(0, 1)

flight = d01.projectile(g)

dart_start = (
    System()
    .add(*d.kinematics())  # (1) to (7)
    .add(*d0.vel.from_polar())  # (8), (9)
    .add(*flight.equations)  # (10), (11): projectile motion
    .known(flight.knowns)  # d01.a.x = 0
    .known({d0.pos.x: 0, d0.pos.y: 0, d0.t: 0})  # from the muzzle, at t = 0
    .known(g)
    .known(d0.vel.mag)  # v0
    .known(d0.vel.angle)  # α0
    .eliminate_zeros()
)

# The monkey.
m = Particle("m", 2, XY)
m0, m1 = m.states
m01 = m.edge(0, 1)

fall = m01.projectile(g)

monkey_start = (
    System()
    .add(*m.kinematics())  # (1) to (7)
    .add(*eq_flat(m0.pos.x, D, m0.pos.y, D * sp.tan(d0.vel.angle)))  # (8), (9)
    .add(*fall.equations)  # (10), (11): projectile motion
    .known(D)
    .known(g)
    .known(d0.vel.angle)
    .known(fall.knowns)  # m01.a.x = 0
    .known({m0.t: 0, m0.vel.x: 0, m0.vel.y: 0})  # it lets go at t = 0, from rest
    .eliminate_zeros()
)
# First `m1.vel.x`, which (4) and (11) make zero: the old script gave that
# zero. Then the old script's five.
monkey = monkey_start.eliminate(m1.vel.x, m0.pos.y, m01.dt, m01.v_av.y, m1.vel.y, m01.a.y)
```

- **The dart** changes only as 3.7 does. `dart` and its eight
  eliminations stay.
- **The monkey's own equations come first,** (8) and (9), so (10) is
  still `m01.a.y = -g`, and the equation the old script keeps is still
  (9).
- **`monkey_start`, as `show()` prints it:**

  ```
  (1)  m01.dt = m1.t
  (2)  m01.v_av.x = (-m0.pos.x + m1.pos.x)/m01.dt
  (3)  m01.v_av.y = (-m0.pos.y + m1.pos.y)/m01.dt
  (4)  0 = m1.vel.x/m01.dt
  (5)  m01.a.y = m1.vel.y/m01.dt
  (6)  m01.v_av.x = m1.vel.x/2
  (7)  m01.v_av.y = m1.vel.y/2
  (8)  m0.pos.x = D
  (9)  m0.pos.y = D*tan(d0.vel.angle)
  (10)  m01.a.y = -g
  (11)  0 = m1.vel.x
  knowns: D, g, d0.vel.angle, m01.a.x = 0, m0.t = 0, m0.vel.x = 0, m0.vel.y = 0
  ```

- **The twentieth elimination.** `m1.vel.x` was a zero known, so
  `eliminate_zeros()` substituted it. Now (4) and (11) both say it is
  zero, and it is eliminated by hand: the history reads
  `eliminate m1.vel.x using (4): into (6), dropped (11)`. A tie between
  (4) and (11) goes to the earlier equation. What is left is today's
  `monkey_start`, so the old script's five follow on the same system.
  This is the spec's rule: 3.10's list changes only where a helper
  changes the equations.
- **`monkey` and everything after it stay:** its comments, `hit`,
  `meet`, `proved`, `reached`, `agree`, `sol_t`, the `BOOK` and
  `STAGES`.
- **The docstring.** "and 19 eliminations by hand in its order"
  becomes: its 19 eliminations by hand, in its order, with one more
  before the monkey's. Add that each model's projectile motion is the
  projectile setup, `d01.projectile(g)` and `m01.projectile(g)`. The
  monkey starts at rest, so the setup's `m0.vel.x = m1.vel.x` makes
  `m1.vel.x` zero, where the old script gave that zero. Eliminating
  `m1.vel.x` first leaves the monkey's equations as the old script's
  were.
- **To leave the monkey as it is instead,** if the review prefers 19:
  keep its `eq_flat` line and its five zero knowns. Then
  `projectile(` is called five times, not six, and the grep under
  "Check and commit" finds two lines in 3.10.

### Tests

**`tests/test_old_outputs.py`: the `RESHAPED` table.** It is
checkpoint 003's design: the table, its key, the lookup in
`test_old_output` and the guard. Scratch used exactly this, after
`OLD`:

```python
# The rows a reshape changed: (module, solution, the old formula) to the
# new formula, in the new names. The row keeps the old formula as the
# record.
#
# Increment 005 of the 004 series, the projectile setup: 3.6's v1x isn't
# a given any more. The setup's `m0.vel.x = m1.vel.x` gives it, so each
# formula has `m0.vel.x` where the old one had `m1.vel.x`.
N06 = "ch03.examples.n06.main"
RESHAPED: dict[tuple[str, str, str], str] = {
    (N06, "sol", "m_1_t*(m_0_v_x + m_1_v_x)/2"): "m0.vel.x*m1.t",
    (
        N06,
        "sol",
        "sqrt(m_1_t**2*((m_0_v_x + m_1_v_x)**2 + (g*m_1_t - 2*m_0_v_y)**2))/2",
    ): "sqrt(m1.t**2*(4*m0.vel.x**2 + (g*m1.t - 2*m0.vel.y)**2))/2",
    (
        N06,
        "sol",
        "sqrt(m_1_v_x**2 + (g*m_1_t - m_0_v_y)**2)",
    ): "sqrt(m0.vel.x**2 + (g*m1.t - m0.vel.y)**2)",
    (
        N06,
        "sol",
        "atan2(-g*m_1_t + m_0_v_y, m_1_v_x)",
    ): "atan2(-g*m1.t + m0.vel.y, m0.vel.x)",
    (
        N06,
        "sol",
        "180*atan2(-g*m_1_t + m_0_v_y, m_1_v_x)/pi",
    ): "180*atan2(-g*m1.t + m0.vel.y, m0.vel.x)/pi",
}
```

- **The rows of `OLD` don't change,** not by one character, and the
  count stays 66. No two rows share a key: checked over all 66.
- **`test_old_output` picks the formula to compare,** as 003 wrote it:

  ```python
  # The formula, verbatim: renamed back, or, for a row a reshape
  # changed, the new one, in the new names. With several roots, SymPy's
  # order doesn't matter: the formula picks its root.
  new = RESHAPED.get((module, solution, formula))
  if new is None:
      formulas = [old_str(root.formula(symbol), module) for root in sol.roots]
      expected = formula
  else:
      formulas = [str(root.formula(symbol)) for root in sol.roots]
      expected = new
  assert expected in formulas
  root = sol.roots[formulas.index(expected)]
  ```

  The want is still found by its old name, and the number is still
  compared with the old number. Nothing else in the test changes.
- **The guard,** with the count pinned, as
  `test_every_quoted_formula_has_a_row` pins 66. The count is this
  page's addition to 003's design: a sixth entry should be as
  deliberate as a 67th row.

  ```python
  def test_every_reshaped_formula_is_a_row() -> None:
      assert set(RESHAPED) <= {(module, solution, formula) for module, solution, _, formula, _ in OLD}
      assert len(RESHAPED) == 5
  ```

- **One test 003's design doesn't have,** so the old formulas stay
  checked, not only recorded. It also keeps 3.6's old lesson, as
  `tests/test_strategies.py` keeps 3.9's. It takes 2.2 s, most of it
  the solve that finds no roots.

  ```python
  def test_3_6_given_v1x_again_is_the_old_output() -> None:
      # The reshaped rows moved because 3.6's givens changed. With
      # m1.vel.x given again, as in the old script, the solve needs the
      # port's old by-hand step, and then every old row comes back verbatim.
      module = importlib.import_module(f"examples.up_15e.{N06}")
      ride, sol = getattr(module, "ride"), getattr(module, "sol")
      assert isinstance(ride, System) and isinstance(sol, Solution)
      m1_vel_x, m01_dt = Var("m", "1", "vel", "x"), Var("m", "01", "dt")
      wants = [w for w in sol.system.wants if w != m1_vel_x]
      given = ride.known(m1_vel_x, 9.0)
      assert given.solve(*wants).roots == ()  # 0 = (-m0.vel.x + m1.vel.x)/m01.dt

      old = given.eliminate(m01_dt).solve(*wants)
      rows = [row for row in OLD if row[0] == N06]
      assert len(rows) == 6
      for _, _, want, formula, number in rows:
          (symbol,) = [w for w in wants if old_name(w, N06) == want]
          assert old_str(old.formula(symbol), N06) == formula
          assert number is not None
          assert math.isclose(float(old.number(symbol)), float(number), rel_tol=1e-9)
  ```

- **The module docstring's list** gains an item: 3.6's five rows that
  the projectile setup changed, in increment 005 of the 004 series. The
  port derives v1x, which the old script gave. `RESHAPED` has their new
  formulas, and the numbers are the old ones.
- **`test_3_10_show_that`** and the tests of `old_name` don't change.

**`tests/old_names.py`:** no change. `m1.vel.x` has a rule, `m_1_v_x`,
and no new symbol appears.

**`tests/test_physics.py`:** a section "# The projectile setup", after
the events and before `BookNotation`. Import `System` and `Setup`.
Scratch passed these:

- **`test_the_projectile_setup`:** `flight = d01.projectile(g)`, with
  `d01` the edge of `Particle("d", 2, XY)`. It is a `Setup`. Its
  equations are the two strings above, and its knowns equal
  `{d01.a.x: 0}`. It unpacks into the same two parts, and a second call
  equals it.
- **`test_the_projectile_setup_of_a_later_edge`:**
  `Particle("p", 3, XY).edge(1, 2)`, as the strings above.
- **`test_the_projectile_setup_goes_into_a_system`:**
  `System().add(*d.kinematics()).add(*flight.equations).known(flight.knowns)`.
  Its last two labels are `8` and `9`, its knowns are `{d01.a.x: 0}`,
  and after `eliminate_zeros()` equation (4) is
  `Eq(0, (-d0.vel.x + d1.vel.x)/d01.dt)`.
- **`test_the_projectile_setup_needs_xy`:** on the module's `X` edge,
  `m01`, and on a `Y` edge, `Particle("b", 2, Y).edge(0, 1)`, it raises
  `UsageError`: `m01 is in X, so it has no projectile setup` and
  `b01 is in Y, so it has no projectile setup`. Reached through
  `getattr`, as the other misuses are.
- **The module docstring** names the projectile setup.

**`tests/physics_misuse.py`:** add at the end, and `import sympy as sp`:

```python
# The projectile setup on an edge that isn't in XY.
g = sp.Symbol("g")
m01.projectile(g)  # pyright: ignore[reportAttributeAccessIssue]
b.edge(0, 1).projectile(g)  # pyright: ignore[reportAttributeAccessIssue]
```

The spec asks for the `X` edge. The `Y` edge is added because it's the
likely slip: 2.6 and 2.7 are free fall in `Y`. Check once that it
bites: put the same ignore on
`Particle("d", 2, XY).edge(0, 1).projectile(g)`, see `uv run pyright`
fail, and take it out.

**`tests/test_examples.py`, `tests/test_strategies.py` and
`tests/slow_examples.py`:** no change. 3.6's `test_book` checks seven
answers now.

### If a formula moves that this page doesn't list

Five rows move, to the five formulas pinned above. Every other row of
`tests/test_old_outputs.py`, renamed back, must come out verbatim, and
so must 3.10's show-that. If another row moves, or one of the five
comes out as anything but its pinned formula, stop. Don't change a
row, a pinned formula, a module's equations, or the order of anything
to make it pass. Report the row, what came out, and what you think
moved it. The same holds for a `BOOK` that stops matching, and for
3.10's `monkey` if its four equations aren't (2), (6), (8) and (9) as
they are today.

## Docs

- **The docstrings** of `physics/__init__.py`, `projectile.py`,
  `particles.py`, the five modules and the two test files, as above.
- **The package `README.md`** doesn't change.
- **The series [README](../README.md):** mark 005 done in its
  increments table, and update its status line and the "4 of 7 done".
  Leave the commit cell and this page's status line for the manager.
- **The [series map](../../README.md):** 004's status says 5 of 7
  increments are done.
- **Don't edit** `spec.md`, `charter.md` or this page. If something
  here is wrong, say so in the report.

## Check and commit

- **`uv run pytest`** passes: the 332 fast tests and yours. Scratch had
  338, in 45 s. Report how long it and `tests/test_examples.py` take.
- **`uv run pytest -m slow`** passes the 3 slow tests, in about 5 min.
  Run it in the background.
- **`uv run pyright`:** 0 errors and 0 warnings, over `src`, `tests`
  and `examples`, `tests/physics_misuse.py` included.
- **Every changed module** runs with
  `uv run python -m examples.up_15e.ch03.examples.n06.main`, and so on
  to `n10`.
- **The times.** Report each changed module's import time. If one is
  5 s or more on your run, put it in `SLOW_EXAMPLES` and say so. For
  3.10, also mark its show-that slow.
- **No projectile lines of their own left.**
  `grep -n 'a\.y, -g\|a\.x: 0\|known(m1\.vel\.x\|\.eliminate(m01\.dt)' examples/up_15e/ch03/examples/n0[6-9]/main.py examples/up_15e/ch03/examples/n10/main.py`
  finds nothing. Today it finds 14 lines. `projectile(` is called six
  times under `examples/`, in those five modules, docstrings aside. Of
  the five, only 3.10 imports `eq_flat`.
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
- that the five formulas listed are the only ones that moved, each to
  its pinned formula, or, if not, the row and what came out (you
  stopped there);
- that 3.10's `monkey` is as it is today, with the one more
  elimination;
- any name or message you chose differently from this page, and why;
- what pyright needed beyond the `cast`s this page names;
- anything in the spec or this checkpoint that was wrong or unclear,
  and what you did instead.

Then stop. Increment 006, Newton on the edge, is a separate checkpoint.
