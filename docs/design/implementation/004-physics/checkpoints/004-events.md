# physics 004: events

**Status:** Checkpoint written (2026-11-09).

If you've been told to read this file, this is the whole assignment.
Build it, check it, commit it, report, and stop.

## Goal

The second reshape. Two examples link states through symbols of their
own, and an event takes their place. That means:

- **`events.py`, with `Event`:** two or more states, in the same axes,
  at the same time and place. `Event("meet", m1, p1)` owns `meet.t` and
  `meet.pos`, and `meet.equations(axes=None)` writes its links.
- **`notation.py` gains the rows for events:** `meet.t` prints `t`, and
  `meet.pos.x` prints `x`.
- **2.5 (both):** `meet = Event("meet", m1, p1)`. `t_01` becomes
  `meet.t` and `dist` becomes `meet.pos.x`. Step by step still
  eliminates the same six links.
- **3.10:** `hit = Event("hit", d1, m1)`, with `hit.equations(Y)` in the
  meeting and `hit.equations(X)` where the x's agree. `t` and `y` go.
- **The old formulas, still renamed back.** `SCRIPT_NAMES` gains 2.5's
  two modules: `meet.t` → `t_01`, `meet.pos.x` → `dist`. All 66 rows and
  3.10's show-that come out verbatim.

**No formula changes.** The links change order and sides, and 3.10's
`agree` gains one link, but every want's formula, renamed back, is the
old one. The scratch run compared every system and solution of the
three modules, not only the rows. So no row needs a new formula, and
the `RESHAPED` table that checkpoint 003 designs under "A row whose
formula changes" isn't built here. 005 is still the likely first
increment to need it.

**Not in this increment:**

- The projectile setup (005). 3.10's `a_y = -g` and `v0x = v1x` lines
  stay, and so do the monkey's.
- `mass` and `newton` (006).
- **3.10's 19 eliminations** stay, in the same order. Two of them are
  renamed: `y` and `t` become `hit.pos.y` and `hit.t`.
- **2.5's `m_v`** stays a plain symbol, as in the spec's sketch.
- **The written-out 2.5 modules,** `main_handwritten.py` and
  `main_handwritten_step_by_step.py`, don't change. They keep their own
  `t_01` and `dist`.
- **Labels for the event's equations.** 3.10 still picks
  `dart.equation("8")` by number.
- **Pyright doesn't check `axes=`** against the event's axes.
  `meet.equations(Y)` on an `X` event raises at run time only. Typing it
  would take an overload per axes, and no example needs it.

## Read first

- **[The spec](../spec.md).** In "Decisions": "Owners are values",
  "Events", "Book notation", "The examples" and "The tests". The 2.5
  and 3.10 sketches. Then "### 004 events", "How each increment lands"
  and "SymPy to watch".
- **The series [README](../README.md),** the review of 002:
  `BookNotation` treats a `Var` with an empty `where` as a lone
  vector's. An event's symbols have an empty `where` too, so their rows
  go first.
- **[Checkpoint 003](003-polar-and-degrees.md),** and what it built:
  `tests/old_names.py`'s `SCRIPT_NAMES` and `tests/test_old_outputs.py`.
  Also `src/equarium/physics/particles.py` (`State`, and `Particle`'s
  name check and `__init__`), `vectors.py`, `notation.py` and
  `__init__.py`, and `tests/test_physics.py` and
  `tests/physics_misuse.py`.
- **The three modules,** `examples/up_15e/ch02/examples/n05/main.py`,
  `main_step_by_step.py` and `examples/up_15e/ch03/examples/n10/main.py`.
- **The prototype,** outside the repo, in
  `~/.config/Claude/side-session-notes/local_9ac850c1-eb15-42fc-bbb0-61739b724d16/004-spec-prototype/`:
  `layer.py`'s `Event` and `sketches.py`'s 2.5. It's data, not the
  source: the spec and this page win. Where it differs:
  - its `Event` takes the axes when it's made,
    `Event("meet", mo1, po1, axes=X)`, and always links those. Here the
    event's axes are its states', and `equations(axes=None)` picks the
    position axes, as the spec says, so one event serves both of 3.10's
    systems;
  - its states can be in any axes, `State[Any]`, and a mix raises
    `ValueError`. Here they share `A`, so pyright flags a mix, and the
    run time raises `UsageError`;
  - it ported neither 2.5 step by step nor 3.10.

## Starting point

The branch `2026-11-08-physics-redesign`, at the commit that adds this
checkpoint, on top of `cf39254` (the review of 003). Check it with
`git branch --show-current`. If you're on another branch, stop and ask.
Don't switch branches, stash or reset.

`uv run pytest` passes 325 tests and deselects 3 slow ones, in about
41 s. `uv run pytest -m slow` passes those 3, in about 5 min.
`uv run pyright` reports 0 errors and 0 warnings.

Checked in scratch while writing this page, on a copy of the repo at
`cf39254`, with `Event` built as this page says:

- **The three modules,** ported as this page says, ran. Every `System`
  and `Solution` in them, renamed back to the old names, was compared
  with the same at `cf39254`. The event's symbols were renamed back to
  the old scripts' `t_01`, `dist`, `t` and `y`. Every solution's
  formulas and numbers are the same: 10, 30 and 150 in both 2.5
  modules, and 3.10's `sol_t`. So are the knowns and the wants. Only
  this differs:
  - **2.5 (both):** the links, (11) to (14), are time first, with the
    state on the left: `m1.t = meet.t`, `p1.t = meet.t`,
    `m1.pos.x = meet.pos.x`, `p1.pos.x = meet.pos.x`. The old links were
    `dist = m1.pos.x`, `dist = p1.pos.x`, `t_01 = m1.t`, `t_01 = p1.t`.
  - **2.5 step by step:** after the six eliminations, the links left are
    (11) and (12), `m01.dt = meet.t` and `p01.dt = meet.t`. They were
    (13) and (14), `t_01 = m01.dt` and `t_01 = p01.dt`. The other six
    equations are the same.
  - **3.10:** `dart_start`, `dart`, `monkey_start`, `monkey`, `meet`,
    `proved` and `reached` are the same, renamed back. `agree` has eight
    equations, not seven: its old `d1.pos.x = m1.pos.x` is two links now,
    `d1.pos.x = hit.pos.x` and `m1.pos.x = hit.pos.x`. `sol_t` is the
    same.
- **The fast suite,** with the map and five draft tests of `Event`,
  passed all 330 tests in 44 s: the 66 rows, the show-that and every
  `BOOK`.
- **2.5 step by step's history** shows the six eliminations as this
  page explains them below: `m1.pos.x` using (13), `p1.pos.x` using
  (14), `m1.t` using (1) and `p1.t` using (5).
- **Pyright** reported 0 errors over `src`, `tests` and `examples`. It
  flags `Event("hit", m1, d1)` with `m1` in `X` and `d1` in `XY`
  (`reportArgumentType`: `State[XY]` isn't `State[X]`, since `State` is
  invariant in `A`). It flags `meet.pos.y` on an `X` event
  (`reportAttributeAccessIssue`). An ignore on a correct event fails the
  run.
- **The book form** of 2.5 prints the links as `(11) tM1 = t` to
  `(14) xP1 = x`, and the solution as `t = 2*m_v/aPx`, `vP1x = 2*m_v`
  and `x = 2*m_v**2/aPx`.
- **The times,** each module's import in a fresh process, after SymPy
  and equarium, three runs each:

  | Module | Now | With events |
  |---|---|---|
  | 2.5 | 0.28 to 0.30 s | 0.29 s |
  | 2.5 step by step | 0.29 to 0.30 s | 0.29 to 0.30 s |
  | 3.10 | 4.07 to 4.09 s | 4.06 to 4.19 s |

  In 3.10, `proved`'s eliminations take 1.27 s before and 1.31 s after,
  `reached`'s 1.27 s and 1.30 s, and `agree`'s solve 0.09 s and 0.10 s.
  Nothing changes.

## Build

### `events.py`: `Event`

A new module. Scratch used exactly this:

```python
@dataclass(frozen=True, init=False)
class Event[A: Axes]:
    name: str
    states: tuple[State[A], ...]

    def __init__(self, name: str, *states: State[A]) -> None:
        ...  # the checks below
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "states", states)

    @property
    def axes(self) -> type[A]:
        return self.states[0].axes

    @property
    def t(self) -> Var:
        return Var(self.name, "", "t")

    @property
    def pos(self) -> Vector[A]:
        return Vector(self.name, self.axes, "", ("pos",))

    def equations(self, axes: type[Axes] | None = None) -> list[sp.Eq]:
        return event_equations(self, axes)
```

- **A frozen dataclass, equal by value,** with its own `__init__`, as
  `Particle` has. It holds states, never symbols: `meet.t` and
  `meet.pos` are made on demand from the name. So two events with one
  name have the same symbols, as the spec says of owners.
- **The checks,** each a `UsageError`, in this order:

  | Misuse | Message |
  |---|---|
  | `Event("e2", m1, p1)` | `an event's name is a Python identifier that doesn't end in a digit, not 'e2'` |
  | `Event("meet", m1)` | `meet needs two or more states, not 1` |
  | `Event("hit", m1, d1)` | `hit: m1 is in X, but d1 is in XY` |
  | `Event("meet", m1, p1, m1)` | `meet has a state twice` |

  The name rule is `Particle`'s. The axes check compares each state's
  `axes` with the first's by `is`. A state reads as `owner + where`,
  `m1`. A state twice isn't in the spec. It's checked because it would
  write the same link twice.
- **`event_equations(event, axes=None)`,** a plain function in the same
  module, which the method calls in one line:
  - each state's time equals the event's, in the states' order;
  - then, for each axis of `axes`, in `axes.names` order, each state's
    position equals the event's. `axes` defaults to the event's.
  - An axis the event doesn't have raises before any equation is made:
    `meet is in X, so it has no y`, as `Vector`'s message reads.
  - Each equation is `cast(sp.Eq, sp.Eq(...))`, as in `polar.py`.
- **As strings:**

  ```
  Event("meet", m1, p1).equations()
    Eq(m1.t, meet.t)
    Eq(p1.t, meet.t)
    Eq(m1.pos.x, meet.pos.x)
    Eq(p1.pos.x, meet.pos.x)

  Event("hit", d1, m1).equations(Y)     # d and m in XY, as in 3.10
    Eq(d1.t, hit.t)
    Eq(m1.t, hit.t)
    Eq(d1.pos.y, hit.pos.y)
    Eq(m1.pos.y, hit.pos.y)
  ```

  On an `XY` event, `equations()` is the time, then x, then y, and
  `equations(XY)` is the same.
- **The sides are the spec's,** the state on the left. They are 3.10's
  old sides, `d1.t = t`. 2.5's old script had the other sides, and
  positions first. That changes 2.5's links, but no formula.
- **Imports:** `State` from `particles.py`, `Vector` from `vectors.py`,
  `Var`, `Axes` and `UsageError`. There is no cycle: nothing imports
  `events.py` but `__init__.py`.
- **The module docstring** says what an event is, that it owns a time
  and a position, and that its links stay equations, so an example can
  eliminate them by hand.

### `notation.py`: the rows for events

- **This increment's rows** of the spec's table:

  | Symbol | Book |
  |---|---|
  | `meet.t` | `t` |
  | `meet.pos.x`, `meet.pos.y` | `x`, `y` |

- **In `text`,** the branch for an empty `where` gains two cases, first,
  before the lone vector's: `("t",)` prints `t`, and `("pos", axis)`
  prints the axis. The paths can't clash, since a lone vector's path is
  one part and never `t`. First, as the review of 002 asked, so the
  branch reads "an event's, then a lone vector's".
- **`owners` doesn't apply to an event,** as it doesn't to a lone
  vector. The book writes the meeting's time as `t`.
- **Still printed as names:** an event's polar parts, such as
  `hit.pos.mag`.
- **The class docstring** gains the event rows, and the comment on the
  branch says it is an event's or a lone vector's.

### `__init__.py`

- **Re-export `Event`,** in `__all__`, in order.
- **The docstring** gains a paragraph: an `Event` is two or more states
  at the same time and place, `Event("meet", m1, p1)`, with its own
  time and position, `meet.t` and `meet.pos`. `meet.equations()` writes
  the links, and `hit.equations(Y)` links the positions on y only.

### The examples

| Module, under `examples/up_15e/` | What changes |
|---|---|
| `ch02/examples/n05/main.py` | `meet = Event("meet", m1, p1)`. `.add(*meet.equations())` replaces the two `add`s of links. `t_01` and `dist` go. |
| `ch02/examples/n05/main_step_by_step.py` | The same event. `.add(*meet.equations())` replaces the `eq_flat` of links. The six eliminations stay. |
| `ch03/examples/n10/main.py` | `hit = Event("hit", d1, m1)`. `hit.equations(Y)` in `meet`, `hit.equations(X)` in `agree`. `t` and `y` go. |

**In every module:**

- **The labels.** The links keep their numbers: 2.5's (11) to (14),
  3.10's `meet` (4) to (7). 3.10's `agree` gains (8).
- **Everything else stays:** the knowns, wants, solves and
  eliminations, in the same order, with the event's symbols for the
  old ones. `eq_flat` stays where a module still writes its own
  equations: 2.5 step by step's (9) and (10), and 3.10's.
- **The `BOOK`s keep their answers.** Only the symbols change:
  `meet.t` for `t_01`, `meet.pos.x` for `dist`.
- **Comments and docstrings use the new names.** A comment that quotes
  a formula quotes it as the module prints it now. The new lines are
  below.

#### 2.5

```python
from equarium.physics import BookNotation, Event, Particle, X

m = Particle("m", 2, X)  # the motorist
p = Particle("p", 2, X)  # the police officer
m0, m1 = m.states
p0, p1 = p.states
m01 = m.edge(0, 1)
p01 = p.edge(0, 1)
meet = Event("meet", m1, p1)  # the same time and place

m_v = sp.Symbol("m_v")

setup = (
    ...
    .known(p01.a.x, 3)  # m/s²
    # They meet at the same time and place: (11) to (14).
    .add(*meet.equations())
    .want(meet.t, p1.vel.x, meet.pos.x)
)

chase = setup.eliminate_zeros()
sol = chase.solve()
# meet.t = 2*m_v/p01.a.x          10
# p1.vel.x = 2*m_v                 30
# meet.pos.x = 2*m_v**2/p01.a.x    150
```

- **The links,** (11) to (14): `m1.t = meet.t`, `p1.t = meet.t`,
  `m1.pos.x = meet.pos.x`, `p1.pos.x = meet.pos.x`.
- **`BOOK`:** `Answer(sol, meet.t, "10")`, `Answer(sol, p1.vel.x, "30")`,
  `Answer(sol, meet.pos.x, "150")`.
- **`__main__`** doesn't change. Its book form prints the event as `t`
  and `x`: `(11) tM1 = t` and `t = 2*m_v/aPx`.
- **The docstring.** "with its links as it writes them" becomes: the
  meeting is an event, `Event("meet", m1, p1)`, whose four links are
  (11) to (14), each state's time, then its position, equal to the
  event's. The old script wrote them itself, through `t_01` and `dist`,
  positions first.

#### 2.5 step by step

```python
from equarium.physics import Event, Particle, X

...
meet = Event("meet", m1, p1)  # the same time and place

m_v = sp.Symbol("m_v")

links = (
    # The motorist's speed is constant: (9) and (10).
    start.add(*eq_flat(m_v, m0.vel.x, m_v, m1.vel.x))
    # The officer starts from rest, both at the sign, both at t = 0.
    .known({p0.vel.x: 0, m0.pos.x: 0, p0.pos.x: 0, m0.t: 0, p0.t: 0})
    # They meet at the same time and place: (11) to (14).
    .add(*meet.equations())
    .known(m_v, 15)  # m/s
    .known(p01.a.x, 3)  # m/s²
)

zeros = links.eliminate_zeros()  # as the old eliminate_zero_eqs

linked = zeros.eliminate(m0.vel.x, m1.vel.x, m1.pos.x, p1.pos.x, m1.t, p1.t)
# The eight equations the old script solves, each in the shape its
# eliminations leave here:
# (2)  m01.v_av.x = meet.pos.x/m01.dt
# (3)  m01.a.x = 0
# (4)  m01.v_av.x = m_v
# (6)  p01.v_av.x = meet.pos.x/p01.dt
# (7)  p01.a.x = p1.vel.x/p01.dt
# (8)  p01.v_av.x = p1.vel.x/2
# (11) m01.dt = meet.t
# (12) p01.dt = meet.t

sol = linked.want(meet.t, p1.vel.x, meet.pos.x).solve()
# meet.t = 2*m_v/p01.a.x          10
# p1.vel.x = 2*m_v                 30
# meet.pos.x = 2*m_v**2/p01.a.x    150
```

- **Why (11) and (12) are left,** not (13) and (14): `m1.pos.x` and
  `p1.pos.x` go through (13) and (14), their simplest roots. `m1.t` ties
  between (1), `m01.dt = m1.t`, and (11), `m1.t = meet.t`, and a tie
  goes to the earlier equation, so (1) goes and (11) keeps `meet.t`.
  Likewise `p1.t`, (5) and (12). The old links ended the same way, as
  (13) and (14).
- **`BOOK`:** as 2.5's.
- **The docstring.** Add that the links are the event `meet`'s
  equations, where the old script wrote them through `t_01` and `dist`,
  and that the same six eliminations remove them.

#### 3.10

```python
from equarium import System, eq_flat
from equarium.physics import XY, Event, Particle, X, Y
from examples.answers import Formula

D, g = sp.symbols("D g")  # the horizontal distance to the monkey, and gravity

# The dart. ... (no change)

# The monkey. ... (no change)

# The dart hits the monkey: the same time and place.
hit = Event("hit", d1, m1)

# They meet: the same time and height.
meet = (
    System()
    .add(dart.equation("8").eq, dart.equation("9").eq, monkey.equation("9").eq)  # (1) to (3)
    .add(*hit.equations(Y))  # (4) to (7)
    .known(D)
    .known(g)
    .known(d0.vel.mag)
    .known(d0.vel.angle)
)
proved = meet.eliminate(d1.t, m1.t, d1.pos.y, m1.pos.y, hit.pos.y, hit.t)
# (2)  D*d0.vel.mag*sin(d0.vel.angle)/d1.pos.x = d0.vel.mag*sin(d0.vel.angle)
# which holds exactly when the dart reaches x = D:
reached = meet.add(sp.Eq(d1.pos.x, D)).eliminate(
    d1.t, m1.t, d1.pos.y, m1.pos.y, hit.pos.y, hit.t, d1.pos.x
)
# no equations left

# The time when the x's agree.
agree = (
    System()
    .add(dart.equation("8").eq)  # (1)
    .add(monkey.equation("2").eq, monkey.equation("6").eq, monkey.equation("8").eq)  # (2) to (4)
    .add(*hit.equations(X))  # (5) to (8)
    .known(D)
    .known(d0.vel.mag)
    .known(d0.vel.angle)
)
sol_t = agree.solve(d1.t)
# d1.t = D/(d0.vel.mag*cos(d0.vel.angle))
```

- **`meet` keeps its name:** it's the system. The event is `hit`, as in
  the spec's sketch.
- **`meet`'s links,** (4) to (7): `d1.t = hit.t`, `m1.t = hit.t`,
  `d1.pos.y = hit.pos.y`, `m1.pos.y = hit.pos.y`. They're the old (4)
  to (7), with `hit.t` for `t` and `hit.pos.y` for `y`.
- **`agree`'s links,** (5) to (8): `d1.t = hit.t`, `m1.t = hit.t`,
  `d1.pos.x = hit.pos.x`, `m1.pos.x = hit.pos.x`. The old (7),
  `d1.pos.x = m1.pos.x`, is two links now, through `hit.pos.x`: one more
  equation and one more unknown, and the same time.
- **The comments, the `BOOK` and `STAGES`** stay.
- **The docstring.** "links them through new symbols `t` and `y`; here
  they're picked by label" becomes: they're picked by label here, and
  linked by the event `hit`, `Event("hit", d1, m1)`, on y:
  `hit.equations(Y)`, the same time and height. "the links through `t`
  and the x's" becomes "the event's links on x, `hit.equations(X)`".

### Tests

**`tests/old_names.py`: the map gains 2.5.** Scratch used exactly this,
first in `SCRIPT_NAMES`:

```python
    "ch02.examples.n05.main": {
        Var("meet", "", "t"): "t_01",
        Var("meet", "", "pos", "x"): "dist",
    },
    "ch02.examples.n05.main_step_by_step": {
        Var("meet", "", "t"): "t_01",
        Var("meet", "", "pos", "x"): "dist",
    },
```

- **The rules don't change.** An event has no rule: the old code never
  made one, and each old script named its own, 2.5's `t_01` and 3.10's
  `t`. `old_name` looks in the map before the rules, so before their
  lone-vector branch, as the review of 002 asked. Without a module, an
  event's symbol still raises.
- **3.10 isn't in the map.** `hit`'s symbols are eliminated before
  anything is compared, and the show-that test passes no module.
  `test_every_mapped_module_has_rows` would fail for a module with no
  rows.
- **The module docstring.** "Increment 004 adds 2.5's `meet.t`, and 006
  4.5's `b.mass`" becomes: 2.5's `meet.t` and `meet.pos.x` are its
  `t_01` and `dist`. Increment 006 adds 4.5's `b.mass`.

**`tests/test_old_outputs.py`:**

- **The rows don't change,** not by one character, and nor do
  `test_old_output` and `test_3_10_show_that`.
- **`test_old_name_of_a_var_the_rule_doesnt_know`** gains
  `Var("meet", "", "t")` and `Var("meet", "", "pos", "x")`: an event's,
  without a module.
- **`test_old_name_in_its_module_is_the_scripts`** gains 2.5: in both
  modules, `meet.t` is `t_01` and `meet.pos.x` is `dist`.
- **The module docstring:** "such as 3.6's `dist`" becomes "such as
  3.6's `dist` and 2.5's `t_01`".

**`tests/test_physics.py`:** a section "# Events", after the vectors and
before `BookNotation`. Scratch passed these:

- **`test_an_events_symbols`:** `meet = Event("meet", m1, p1)`, with
  `p1` an `X` state of `Particle("p", 2, X)`. Its names are `meet.t`
  and `meet.pos.x`. `meet.t == Var("meet", "", "t")`,
  `meet.pos == Vector("meet", X, "", ("pos",))`, and `meet.axes is X`.
  An event made twice is equal and hashes alike.
- **`test_an_events_equations`:** `meet.equations()` as the four
  strings above.
- **`test_an_events_equations_on_the_axes_chosen`:** 3.10's dart and
  monkey, both `XY`. `hit.equations(Y)` as the four strings above;
  `hit.equations(X)`'s last two, `Eq(d1.pos.x, hit.pos.x)` and
  `Eq(m1.pos.x, hit.pos.x)`; `hit.equations()` is time, x, then y, and
  equals `hit.equations(XY)`.
- **`test_event_misuses_raise`:** each row of the table above, and
  `meet.equations(Y)` on the `X` event. The mixed axes go through
  `cast(Any, …)`, so pyright doesn't see the misuse here. Bad names:
  `"e2"`, `"m.x"`, `""`.
- **`test_the_book_notation_of_an_event`,** with the other notation
  tests: `meet.t`, `meet.pos.x` and `hit.pos.y` print `t`, `x` and `y`;
  with `owners={"meet": "P"}` they print the same; `hit.pos.mag` prints
  its name.
- **`test_the_book_notation_of_2_5_with_owners`** gains the solution:
  `render_solution` of 2.5's `sol` with
  `BookNotation(owners={"m": "M", "p": "P"}, color=False)` starts with
  `"t = 2*m_v/aPx\n"`.
- **The module docstring** names events.

**`tests/physics_misuse.py`:** add, after the vectors' misuses, and
import `Event`:

```python
# An event over states of different dimensions, and an axis it doesn't have.
p1 = Particle("p", 2, X).states[1]
d1 = Particle("d", 2, XY).states[1]
meet = Event("meet", m1, p1)
meet.pos.y  # pyright: ignore[reportAttributeAccessIssue]
Event("hit", m1, d1)  # pyright: ignore[reportArgumentType]
```

Check once that it bites: put the same ignore on `Event("both", p1, m1)`,
see `uv run pyright` fail, and take it out.

**`tests/test_examples.py`, `tests/test_strategies.py` and
`tests/slow_examples.py`:** no change.

### If a formula moves

Every row of `tests/test_old_outputs.py`, renamed back through the
rules and the map, must come out verbatim, and so must 3.10's
show-that. The scratch run found none that moved. If one does, stop.
Don't change the row, the module's equations, or the order of anything
to make it pass, and don't add the `RESHAPED` table. Report the row,
what came out, and what you think moved it. The same holds for a `BOOK`
that stops matching, and for 2.5 step by step's links left, (11) and
(12), if they aren't as listed above.

## Docs

- **The docstrings** of `physics/__init__.py`, `events.py`,
  `notation.py`, the three modules and the three test files, as above.
- **The package `README.md`** doesn't change.
- **The series [README](../README.md):** mark 004 done in its increments
  table, and update its status line and the "3 of 7 done". Leave the
  commit cell and this page's status line for the manager.
- **The [series map](../../README.md):** 004's status says 4 of 7
  increments are done.
- **Don't edit** `spec.md`, `charter.md` or this page. If something
  here is wrong, say so in the report.

## Check and commit

- **`uv run pytest`** passes: the 325 fast tests and yours. Report how
  long it and `tests/test_examples.py` take.
- **`uv run pytest -m slow`** passes the 3 slow tests, in about 5 min.
  Run it in the background.
- **`uv run pyright`:** 0 errors and 0 warnings, over `src`, `tests`
  and `examples`, `tests/physics_misuse.py` included.
- **Every changed module** runs with
  `uv run python -m examples.up_15e.ch02.examples.n05.main`,
  `...n05.main_step_by_step` and `examples.up_15e.ch03.examples.n10.main`.
- **The times.** Report each changed module's import time. If 3.10's is
  5 s or more on your run, put it back in `SLOW_EXAMPLES`, mark its
  show-that slow, and say so.
- **No links of their own left.**
  `grep -n 'sp.symbols("m_v dist t_01")\|sp.symbols("t y")\|eq_flat(d1.t\|eq_flat(dist' examples/up_15e/ch02/examples/n05/main.py examples/up_15e/ch02/examples/n05/main_step_by_step.py examples/up_15e/ch03/examples/n10/main.py`
  finds nothing. Today it finds six lines. And `Event(` is called under
  `examples/` only in those three modules.
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
- any name or message you chose differently from this page, and why;
- what pyright needed beyond the `cast`s this page names;
- anything in the spec or this checkpoint that was wrong or unclear,
  and what you did instead.

Then stop. Increment 005, the projectile setup, is a separate
checkpoint.
