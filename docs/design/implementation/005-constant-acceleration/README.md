# 005 constant acceleration

**Status:** Checkpoint 001 written (2026-11-11), not built.

The physics layer's kinematics equations assume constant acceleration
on every edge, without saying so. This series makes the assumption a
step of its own, one edge at a time, as the book does.

## Why

Building Example 2.4 from scratch under transcript mode's `--watch`
(2026-11-11), the user saw `m.kinematics()` print four equations for
the edge `m01`:

```
(1)  m01.dt = -m0.t + m1.t
(2)  m01.v_av.x = (-m0.pos.x + m1.pos.x)/m01.dt
(3)  m01.a.x = (-m0.vel.x + m1.vel.x)/m01.dt
(4)  m01.v_av.x = m0.vel.x/2 + m1.vel.x/2
```

and asked whether (3) assumes constant acceleration before the problem
says so. It doesn't, but (4) does:

- **(3) is the book's 2.4,** the definition of the average
  acceleration over an interval, and holds for any motion. `m01.a`
  belongs to an edge, an interval, so it has one value there: its
  average acceleration. The instantaneous acceleration, the book's 2.5,
  would belong to an instant, a state, and the model has none. The
  book's 2.7 has the same right side; it's "the" acceleration only
  because, when the acceleration is constant, the average and the
  instantaneous are the same. The code called (3) "2.7", which blurred
  that.
- **(4) is the book's 2.10, "constant x-acceleration only".** For other
  motion the average velocity isn't the mean of the two ends'
  velocities. And it's what 2.4's answer needs. With (1) to (3) alone,
  part (a) is 4 unknowns in 3 equations. `m1.vel.x` still comes out,
  `23.0*meter/second`, since the average acceleration is enough for it,
  but `m1.pos.x` doesn't.

So every system built on `m.kinematics()` assumes constant acceleration
on every edge, whether its problem has it or not.

## Decisions *(user, 2026-11-11)*

1. **`m.kinematics()` gives only what holds for any motion:** for each
   edge, Δt, then for each edge and axis the book's 2.2, the average
   velocity, and 2.4, the average acceleration. The order is today's,
   with 2.10 gone.
2. **`m01.constant_acceleration()` states the assumption, for one
   edge:** the book's 2.10, one equation per axis, in the axes' order.
   It's called once for each edge that has constant acceleration. So
   constant acceleration on 0→1 and a different one on 1→2 is
   `m01.constant_acceleration()` and `m12.constant_acceleration()`, each
   edge with its own `a`. An edge without the call has only its
   averages, which lets the model take problems whose acceleration
   isn't constant.

   2.4 then reads as the book's IDENTIFY and SET UP:

   ```python
   motorcycle = (
       System()
       .add(*m.kinematics())               # Δt, 2.2, 2.4: any motion
       .add(*m01.constant_acceleration())  # "a constant 4.0 m/s²": 2.10
       ...
   ```

3. **`m01.a` stays one symbol:** the edge's average acceleration, by
   2.4. On an edge with constant acceleration, it's also the
   acceleration at every instant of the edge. The book's notation keeps
   printing it `ax`.
4. **The projectile setup doesn't include 2.10.** A projectile edge
   calls `constant_acceleration()` like any other, right after the
   kinematics, and `m01.projectile(g)` stays `a.y = -g` and
   `v0x = v1x`, with `a.x` known zero. This changes what was first
   proposed, that `projectile(g)` would include 2.10, since projectile
   motion is constant acceleration by definition. The reason is the
   order of the equations. Example 3.10's dart adds `d0.vel.from_polar()`
   between its kinematics and its projectile setup, so 2.10 inside the
   setup would move, the labels after it would change, and `sp.solve`
   can return a different form of a formula for equations in a
   different order, which the record of the old formulas checks
   verbatim. Including it can be reconsidered later, on its own.
5. **Two steps, as in "never change two layers at once":**
   - **001, the API and a port that changes no result.** Every example
     that calls `kinematics()` gets a `constant_acceleration()` for each
     edge, right after it. Every system then holds the equations it
     holds today, in the same order, with the same labels, so every
     answer, formula and record row stays as it is.
   - **002, the audit.** For each problem, the book says whether the
     acceleration is constant. Where it isn't, the line goes. If a
     problem then can't be solved, that's a finding for the user, not
     something to patch.
6. **Later, and separate: the equations' labels from the book,** (2.2),
   (2.4) and (2.10) in place of (1) to (4), so that a reader sees which
   one holds for constant acceleration only.
7. **Form:** a README and checkpoints, the lightest form that carries
   it, since the design was settled in the conversation. Each
   checkpoint is built in a fresh conversation and reviewed by the user
   before the next is written.

## Not in this series

- **The written-out versions and the core's tests**, such as
  `main_handwritten.py`, `tests/example_2_4.py` and
  `examples/up_15e/ch02/tables/n05/`. They write their equations out
  and label the acceleration's "2.7". Those are constant-acceleration
  problems, where 2.7 is the right name, and the core's tests don't
  use the physics layer.
- **The user's scratch copies** of 2.4 in the review folder,
  `equarium.py`, which are untracked: `main_000_check.py`,
  `main_incremental.py`, `main_watch_000.py` and `main_watch_001.py`.
  Once this merges, their part (a) shows 4 unknowns in 3 equations
  until they add `m01.constant_acceleration()`.

## Where

Branch `2026-11-11-constant-acceleration`, from `master` at `836cad3`
(`v0.2.0` and its notes), in its own worktree,
`~/journal/2026-11-06-equations/equarium-acceleration`, so the review
folder `equarium.py` stays on `master`. The branch
`2026-11-11-worksheet-displays` (transcript mode's short displays) is
separate, and not merged yet.

## Checkpoints

| # | Checkpoint | Status |
|---|---|---|
| 001 | [explicit constant acceleration](checkpoints/001-explicit-constant-acceleration.md) | Written (2026-11-11) |
| 002 | the audit | Written after 001 is reviewed |

The 19 modules that call `kinematics()` today, which 002 audits, are
listed in checkpoint 001.
