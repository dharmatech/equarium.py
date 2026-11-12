# 004 physics

**Status:** Charter and spec agreed with the user (2026-11-08). All
seven increments are done and reviewed: 001, symbols and chapter 2,
002, chapters 3 and 4 renamed, 003, polar and degrees, 004, events,
005, the projectile setup, 006, Newton on the edge, and 007, the end.
The rename is complete, polar is one way everywhere, 2.5 and 3.10 link
through events, 3.6 to 3.10 use the projectile setup, and 4.4 and 4.5
use Newton on the edge. The old physics code's copy is deleted, and the
version is 0.2.0. The branch merged into `master` on 2026-11-11.
It's tagged `v0.2.0`, on the merge commit. Pushing is the user's call.

The physics layer's redesign: structured symbols that keep their
meaning, one naming rule, the dimension set once, and helpers for
polar form, events, the projectile setup and Newton's laws. The core
doesn't change. It runs as a charter, a spec and checkpoints.

- [charter.md](charter.md): the handoff. What the old physics code
  taught, what the prototype showed, what is decided, the design
  questions, candidate increments, and how to work.
- [spec.md](spec.md): what was decided, the sketches of 2.4, 2.5, 3.10
  and 4.5, and the seven increments with their checks.
- `checkpoints/`: one per increment, written when the one before has
  landed and been reviewed.

**Where:** branch `2026-11-08-physics-redesign`, from tag `v0.1.0`
(`3370e5d`), which is the core with the old physics code. Every commit
of this series goes on the branch. It merged into `master` on
2026-11-11, as version 0.2.0.

The spec was designed from the charter in its own conversation. To
implement a checkpoint, give a new conversation this, with the
checkpoint's file name (the last one was 007, and the series is done):

> Read `docs/design/implementation/004-physics/checkpoints/007-the-end.md`
> in `~/journal/2026-11-06-equations/equarium.py`, on the branch
> `2026-11-08-physics-redesign`. If you've been told to read that
> file, it is the whole assignment.

## Increments

From the [spec](spec.md#increments). 7 of 7 done. 001 and 002 rename
only; 003 to 006 change equations; 007 removes the old copy.

| # | Increment | Checkpoint | Status | Commit |
|---|---|---|---|---|
| 001 | symbols and chapter 2 | [001](checkpoints/001-symbols-and-chapter-2.md) | Done, reviewed (2026-11-08) | `6bf4296` |
| 002 | chapters 3 and 4, renamed | [002](checkpoints/002-chapters-3-and-4-renamed.md) | Done, reviewed (2026-11-08) | `a5f848d` |
| 003 | polar and degrees | [003](checkpoints/003-polar-and-degrees.md) | Done, reviewed (2026-11-09) | `4d84e67` |
| 004 | events | [004](checkpoints/004-events.md) | Done, reviewed (2026-11-09) | `e0c0b68` |
| 005 | the projectile setup | [005](checkpoints/005-projectile-setup.md) | Done, reviewed (2026-11-09) | `f505be6` |
| 006 | Newton on the edge | [006](checkpoints/006-newton-on-the-edge.md) | Done, reviewed (2026-11-09) | `2572faf` |
| 007 | the end | [007](checkpoints/007-the-end.md) | Done, reviewed (2026-11-09) | `bb0f492` |

## Decisions

The spec has them all. The ones the user settled (2026-11-08):

- **An owner's name is its identity.** Two `Particle("m", …)` are the
  same particle, with the same symbols. No hidden key.
- **The dimension is a type:** `X`, `Y` or `XY`, so pyright flags
  `m0.pos.y` in an x-only model.
- **The steps the helpers make unnecessary are dropped:** 3.6's
  `eliminate(m01.dt)`, 3.8's two by-hand eliminations, and 3.9's
  `eliminating()`.
- **Book notation is glued, as the book's text reads:** `x0`, `v0x`,
  `ax`, `vP0x`, with `Δt` and `α`.

## What's next

All seven increments are done and reviewed, so no checkpoint comes
next. The branch merged into `master` on 2026-11-11, with `--no-ff`,
after the user's hands-on review. Two experiments merged into the
branch before that: setup sketches, with its notes in
`docs/experiments/sketches/`, and transcript mode, kept as a feature
since, with its docs in `docs/transcripts/`. The merge commit is tagged `v0.2.0`
(2026-11-11). What is left is the user's call:

- **The push:** `master`, the tag `v0.2.0`, and the tag `v0.1.0` if it
  is still local.

Increment 007, the end, is done and reviewed, after its
[checkpoint](checkpoints/007-the-end.md). The user approved the
checkpoint's section on the record (2026-11-09) before it was built. No
equation, formula, example or `BOOK` changed. What changed:

- **The old copy is deleted:** `kinematics_states.py` and
  `newtons_laws.py`. Only `tests/test_physics.py` imported them. The
  old code is still in the tag `v0.1.0`, in every commit of the branch
  before this increment's, and in the old repo.
- **The record stayed as it was,** character for character: the 66 rows
  and `RESHAPED` in `tests/test_old_outputs.py`, and the map in
  `tests/old_names.py`. Neither file used the copy. With the copy
  deleted, `tests/test_old_outputs.py` passes the same 89 tests.
- **Of the four tests that used the copy, two went and two became
  one.** The comparisons of the vector equations and of Newton's second
  law went: the tests beside them pin the same equations as strings.
  The kinematics comparison stayed, as
  `test_kinematics_renamed_back_are_the_old_codes`, with the copy's
  output written out as 22 strings, the old library's own four among
  them. The copy printed the same 22, in order, just before it went.
  It is the only test that pins the order of the equations for three
  states in `XY`: with the loops swapped in the checkpoint's scratch,
  it alone failed. The spec has all four deleted. The user chose to
  keep this one (2026-11-09).
- **The fast suite has 344 tests,** where it had 347, and
  `tests/test_physics.py` has 57, where it had 60.
- **`physics/__init__.py`'s docstring** lost its paragraph on the
  copy.
- **The version is 0.2.0,** in `pyproject.toml` and in `uv.lock`, which
  records it too.
- **The package README didn't change.** Increment 001 already rewrote
  its sentence on the old physics code.
- **This README, the series map and 002's README** say the series is
  done.

Increment 006, Newton on the edge, is done and reviewed:
`Particle.mass` and `Edge.newton(*forces)`, in `newton.py`, for 4.4 and
4.5 (both), after its
[checkpoint](checkpoints/006-newton-on-the-edge.md). It is the last
reshape. No row's formula changed: all 66 come out verbatim, renamed
back, with their numbers. So `RESHAPED` keeps its five entries, and its
guard's count stays 5. What changed:

- **Three names in `SCRIPT_NAMES`,** which two rows need: 4.4's
  `box.mass` → `m` and `box01.a.x` → `a_x`, and 4.5's `b.mass` → `m`.
  With them, 4.5's f_x is the old formula, verbatim, and -0.9. Without
  them, exactly those two rows fail.
- **4.4's box is a particle,** `Particle("box", 2, XY)`, with
  `box01.newton(F, n, w)` and `box01.a.y` known zero. Its own `a` and
  `m` went. Its two equations and its formula are the same, renamed
  back. Its system is named `push`, since the particle takes the name
  `box`.
- **4.5 has five equations, where it had seven.** Its forces moved to
  `X`, with `b01.newton(n, w, f)`. The y equation and the link
  `a.x = b01.a.x` went, with its own `a` and `m`.
- **One formula that isn't a row changed its names:** step 2 of 4.5 in
  two steps is `f.x = b.mass*b01.a.x - n.x - w.x`, where it was
  `f.x = m*a.x - n.x - w.x`. Step 2 knows `b01.a.x`, the symbol step 1
  solves for. A new test pins it.
- **No `BOOK` value changed.** 4.4's `Answer` names `box01.a.x`, where
  it named `a.x`.
- **`vectors.py`'s `_describe` became `describe`,** a rename, since
  `newton.py` uses it for its messages. The checkpoint says how to
  leave `vectors.py` as it was instead.
- **The import times didn't change:** 0.02 s, 0.21 to 0.23 s and
  0.14 s.

Increment 005, the projectile setup, is done and reviewed: `Setup` and
`Edge.projectile(g)`, for 3.6 to 3.10, after its
[checkpoint](checkpoints/005-projectile-setup.md). It is the first
increment whose formulas change, renamed back. Five moved, the five the
checkpoint lists under "The formulas that change", all rows of 3.6, all
for one reason: `m1.vel.x` isn't a given any more, the setup's
`m0.vel.x = m1.vel.x` gives it, and each formula has `m0.vel.x` in its
place. The numbers don't change. The `RESHAPED` table that
[checkpoint 003](checkpoints/003-polar-and-degrees.md) designs is built,
in `tests/test_old_outputs.py`, and pins them. What else changed:

- **3.6's `BOOK` gained one `Answer`,** the book's v_x = 9.0 m/s, which
  was a given. No other `BOOK` changed.
- **3.6's by-hand `eliminate(m01.dt)` went,** so it imports in 1.9 s,
  where it took 0.5 s. No module crosses 5 s.
- **3.7, 3.8 and 3.9 keep the same equations,** so the other 61 rows
  and 3.10's show-that come out as before.
- **3.10's monkey uses the setup, with one more by-hand elimination,**
  `m1.vel.x`, which was a zero known. That makes 20, where the old
  script had 19. The checkpoint says how to leave the monkey as it was
  instead.
- **A new test gives `m1.vel.x` again,** with the old by-hand step, and
  gets all six old rows of 3.6 back verbatim. So the old formulas stay
  checked, and the test shows that the givens moved them, not the
  solver.

Increment 004, events, is done and reviewed: `Event`, for 2.5 (both)
and 3.10, after its [checkpoint](checkpoints/004-events.md). No formula
changed once renamed back: 2.5's links come time first, with the state
on the left, and 3.10's `agree` gains one link, but every solution,
all 66 old formulas and 3.10's show-that come back verbatim, with
`SCRIPT_NAMES` renaming 2.5's `meet.t` and `meet.pos.x` back to `t_01`
and `dist`. So `RESHAPED` is still not needed. The event's symbols are
the first with an empty `where` that aren't a lone vector's:
`BookNotation` matches them before a lone vector's and prints `t` and
`x`, and `old_name` reaches them only through the map, which it reads
before its rules. The import times don't change.

Increment 003, polar and degrees, the first increment that changes
equations, is done and reviewed. No formula changed once renamed back:
the equations and the names change, but all 66 old formulas and 3.10's
show-that come back verbatim, through a per-module map in
`tests/old_names.py` for the names an old script made itself, such as
3.6's `dist`. The test rule for a row whose formula does change is
designed in the [checkpoint](checkpoints/003-polar-and-degrees.md), and
built by the first increment that needs it, likely 005. 3.9 and 3.10
left `SLOW_EXAMPLES`, which is now empty.

The review of 001 (2026-11-08) found nothing to fix. 294 fast tests and
8 slow ones pass, pyright reports 0 errors, and all 66 old formulas
come back verbatim. One note for later: `BookNotation`'s `owners` is a
dict, so a `BookNotation` can't be hashed. Nothing hashes one yet.

The review of 002 (2026-11-08) found nothing to fix. 315 fast tests and
8 slow ones pass, pyright reports 0 errors, and all 66 old formulas and
3.10's show-that come back verbatim. No example imports the old copy
any more. Two notes for later:

- Pyright types `m * F1` as a SymPy `Expr`, from SymPy's own
  `Expr.__mul__`, though at run time it is a `Vec`. So `.eq(m * a)`
  would be a type error. Examples write `a * m`, and 006's `newton`
  builds the product itself.
- `BookNotation` treats a `Var` with an empty `where` as a lone
  vector's. Events (`meet.t`, 004) and the mass (`b.mass`, 006) have an
  empty `where` too, so their rows go before that branch.

The review of 003 (2026-11-09) found nothing to fix. 325 fast tests
pass in 41 s and the 3 slow ones in 5 min 14 s, pyright reports 0
errors, and all 66 old formulas and 3.10's show-that come back
verbatim, renamed back through `SCRIPT_NAMES`. The examples follow the checkpoint's sketches: only
3.6, 3.7 and 4.1 call `to_polar()`, and the steps the spec keeps stay,
3.6's `eliminate(m01.dt)`, 3.7's `eliminate(b1.vel.angle)` and 3.10's
19 eliminations. One note for later: 3.6's `m1.pos.to_polar()` adds
the position's angle, an equation and an unknown no want needs. It is
harmless: no formula moved, and 3.6 still imports in 0.47 s.

The review of 004 (2026-11-09) found nothing to fix. 332 fast tests
pass in 41 s and the 3 slow ones in 5 min 15 s, pyright reports 0
errors, and all 66 old formulas and 3.10's show-that come back
verbatim, with 2.5's `meet.t` and `meet.pos.x` renamed back through
`SCRIPT_NAMES`. `Event`, its messages, its book notation and the three
modules follow the checkpoint's sketches line for line. The event's
rows in `BookNotation` come before the lone vector's, as the review of
002 asked. 2.5 step by step still eliminates the same six links and
leaves (11) and (12). 3.10's 19 eliminations stay in order, with
`hit.pos.y` and `hit.t` for `y` and `t`.

The review of 005 (2026-11-09) found nothing to fix. 338 fast tests
pass in 44 s and the 3 slow ones in 5 min 13 s, and pyright reports 0
errors. `projectile.py`, `Edge.projectile`, the five modules and the
tests follow the checkpoint's code line for line. With `RESHAPED`, all
66 rows pass. Without it, exactly its five rows fail, the five of 3.6
the checkpoint lists, and each new formula's number is the old row's.
The new test gives `m1.vel.x` again and gets all six old rows of 3.6
back verbatim. 3.10's show-that and every `BOOK` pass, and the only
`BOOK` line that changed is 3.6's `Answer(sol, m1.vel.x, "9.0")`.
3.10's monkey has one more elimination, first: its history reads
`eliminate m1.vel.x using (4): into (6), dropped (11)`, the old
script's five follow, and the monkey keeps (2), (6), (8) and (9). The
grep for projectile lines of their own finds nothing, and `projectile(`
is called six times.

The review of 006 (2026-11-09) found nothing to fix. 347 fast tests
pass in 45 s and the 3 slow ones in 5 min 14 s, and pyright reports 0
errors. The code and the three modules are the checkpoint's scratch
build, line for line. The tests differ from it in one test only, which
binds `b0, b1` earlier and adds a comment. All 66 rows pass. Without
the three new names in `SCRIPT_NAMES`, exactly 4.4's and 4.5's rows
fail, and `RESHAPED` still has five. 4.5's f_x is its row, verbatim,
and -0.9. 4.5 has five equations, its (5)
`f.x + n.x + w.x = b.mass*b01.a.x`. The new test pins step 2's
`b.mass*b01.a.x - n.x - w.x`, with step 2 knowing step 1's `b01.a.x`.
The only `BOOK` line that changed is 4.4's `Answer`, whose symbol is
`box01.a.x`, with the same value. All five misuses raise `UsageError`
with the checkpoint's messages.

The review of 007 (2026-11-09) found nothing to fix. 344 fast tests
pass in 45 s and the 3 slow ones in 5 min 11 s, and pyright reports 0
errors. `tests/test_physics.py`, now 57 tests, `physics/__init__.py`,
`pyproject.toml` and `uv.lock` are byte for byte the build the review
made from the checkpoint before committing it. In that build, the copy
printed the kept test's 22 strings, in order, and with the kinematics
loops swapped only that test failed. `tests/test_old_outputs.py` and
`tests/old_names.py` are the same files as at `3f7af33`, so the 66
rows, `RESHAPED` and `SCRIPT_NAMES` are unchanged, and so are the
examples, the misuse file and the package README. The three greps find
nothing, importing either old module raises `ModuleNotFoundError`, the
installed version reads 0.2.0, and `uv.lock` changed only its version
line. `src/equarium/physics/` has `__init__.py` and the spec's ten
modules. The series map and 002's README say the series is done.

Found while writing the spec, for a later series (the core doesn't
change in this one): labels for generated equations, `show(symbol=…)`,
and `clear_zero_denominators`, which no example needs once 3.6 uses the
projectile setup.
