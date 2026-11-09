# Example catalog

**Status:** Written (2026-11-08). The user answered its seven questions
for 007 the same day, each as recommended.

Every problem the old library's `examples/up/` solves, University
Physics 15th edition chapters 2 to 4, plus the derivations in
`ch2/kinematic-equations/`: 21 problems, 50 scripts and 2 notebooks.
The old repo is [combine-equations.py](https://github.com/dharmatech/combine-equations.py),
at `~/src/combine-equations.py`, commit `d9d15b3`. Every script was run
on 2026-11-08 in that repo's own venv (Python 3.14, SymPy 1.14.0),
from the repo's root, through the shim in the
[checkpoint](checkpoint.md) ("Running the old scripts"). The shim
restores `solve_system_2` (one `sp.solve` over the connected unknowns,
the first root only), stubs the tkinter GUI, and turns the colors off,
so symbols print under their plain names, in SymPy's own term order.
Times are wall times, four scripts at a time, and include about 2 s of
start-up. 41 of the 50 scripts ran to the end. Eight fail partway, and
kinematic-equations 004 doesn't finish, so a copy of it ran at a
smaller search depth. The notebook's code cells ran in order, and its
checkpoint copy, identical, didn't run.

**How to read an entry.** Each entry gives the problem in our own
words, the book's printed answers with their page, then every old
script: its style, its role, whether it runs, and what it prints for
each want, verbatim. "Zeros" says, for each script to port, which
zeros the old script wrote as equations and which as values, which is
how [002](../002-core/spec.md)'s increment 007 ports them. "Styles
worth keeping" names the module each kept script becomes, under
`examples/up_15e/`. The last section,
[Recommendations for 007](#recommendations-for-007), collects the
decisions 007 is written from.

**Roles.** **latest**: the newest version of its style. **alternative**:
a different style, kept on purpose. **draft**: a later version replaced
it. **duplicate**: a copy of another script. **other library**: it
doesn't use combine_equations. **Runs**: **yes**, **yes, shim** (it
needed the shim's `solve_system_2` or GUI stub), or **fails**.

**The technique vocabulary.** Entries use these words, so a technique
can be found by grep.

| Technique | In the old scripts | In equarium |
|---|---|---|
| written out | equations and symbols by hand (v3, kinematic-equations) | `System.add` |
| physics code | `kinematics_states`, `newtons_laws` | 007 |
| zero equations | `Eq(x0, 0)`, `eliminate_zero_eqs` | `known(x0, 0)`, `eliminate_zeros()` |
| zero values | `0` in `values` | `known(x0, 0)` |
| all at once | `solve_system_2`, `solve_system_multiple_solutions` and its `_000`, `solve_and_display_` versions 0 and 1 | `solve()` |
| eliminating | `solve_with_elimination_attempts`, `solve_and_display_` version 2 | `eliminating()` |
| by hand | `eliminate_variable_subst` between displays | `eliminate` |
| isolate | `isolate_variable` | `isolate` |
| parts | one base, knowns changed per part | branching |
| several roots, filter | several solutions, the physical one chosen | `where` |
| units | values with units, converted at the end | `in_units`, `Answer(unit=)` |
| two steps | the first answer fed into a second system | two systems |
| links | equalities between objects' symbols (`eq_flat`, `link_same_time`) | equations |
| polar two-way, polar one-way | `magnitude_and_angle_equations`, or one direction only: components from polar (the forces in 4.1, the launch in 3.7), or polar from components (the net force in 4.1, the velocities in 3.6 and 3.7) | equations |
| show that | eliminate until only the stated condition is left | `eliminate` |
| both sides | misc.py's `add_both_sides` and the rest | none yet |
| derive all | kinematic-equations 005's search | origins only |
| GUI | `show_equation_gui` | out of scope |
| first root | `solve_system_2` keeps only `sp.solve`'s first root, so a second root is never printed | `solve()` keeps every root |

"first root" is the one word added to the checkpoint's vocabulary, and
"polar one-way" is widened to both directions. Chapter 3's entries
say "the other way round" for polar from components.

## Index

| Problem | Title | Page | Old scripts | Book's answers | In equarium | Port in 007 as |
|---|---|---|---|---|---|---|
| [Example 2.4](#example-24-constant-acceleration-calculations) | Constant-acceleration calculations | 78 | 3, all ran | 43 m; 23 m/s; 55 m | `ch02/examples/n04/`: `main.py`, `main_handwritten.py`; tests | `example_2_4.py` |
| [Example 2.5](#example-25-two-objects-with-different-accelerations) | Two objects with different accelerations | 78 | 4, all ran | 10 s; 30 m/s; 150 m | `ch02/examples/n05/`: `main.py`, `main_step_by_step.py`, `main_handwritten.py`, `main_handwritten_step_by_step.py`; tests | `example_2_5.py`, `example_2_5_step_by_step.py` |
| [Example 2.6](#example-26-a-freely-falling-coin) | A freely falling coin | 80 | 2, all ran | -4.9 m, -9.8 m/s; -20 m, -20 m/s; -44 m, -29 m/s | `ch02/examples/n06/`: `main.py` | `example_2_6.py` |
| [Example 2.7](#example-27-up-and-down-motion-in-free-fall) | Up-and-down motion in free fall | 81 | 1, ran | +10.1 m, +5.2 m/s; -18.4 m, -24.2 m/s; ±11.3 m/s; +11.5 m; -9.80 m/s² | `ch02/examples/n07/`: `main.py`; tests (written out) | `example_2_7.py` |
| [Example 2.8](#example-28-two-solutions-or-one) | Two solutions or one? | 82 | in 2.7's script | +3.36 s | `ch02/examples/n08/`: `main.py`; tests (written out) | `example_2_8.py` |
| [Exercise 2.1](#exercise-21-a-cars-distance-from-its-average-velocity) | A car's distance from its average velocity | 89 | 1, ran | 25.0 m | `ch02/exercises/n001/`: `main.py` | `exercise_2_1.py` |
| [Exercise 2.3](#exercise-23-the-slow-trip-home) | The slow trip home | 89 | 3, all ran | 55 min | `ch02/exercises/n003/`: `main.py`, `main_two_steps.py`; tests (written out) | `exercise_2_3.py`, `exercise_2_3_two_steps.py` |
| [Exercise 2.5](#exercise-25-average-velocity-and-speed-of-a-walk) | Average velocity and speed of a walk | 89 | 2, all ran | 0.313 m/s; 1.56 m/s | `ch02/exercises/n005/`: `main.py` | `exercise_2_5.py` |
| [Exercise 2.19](#exercise-219-an-antelopes-speed-and-acceleration) | An antelope's speed and acceleration | 90 | 1, ran | 8.33 m/s; 1.11 m/s² | `ch02/exercises/n019/`: `main.py` | `exercise_2_19.py` |
| [Exercise 2.21](#exercise-221-a-fast-pitch) | A fast pitch | 90 | 2, all ran | 675 m/s²; 0.0667 s | `ch02/exercises/n021/`: `main.py` | `exercise_2_21.py` |
| [Exercise 2.23](#exercise-223-stopping-distance-of-an-airbag) | Stopping distance of an airbag | 90 | 1, ran | 1.70 m | `ch02/exercises/n023/`: `main.py`; tests (written out) | `exercise_2_23.py` |
| [Example 3.6](#example-36-an-object-projected-horizontally) | An object projected horizontally | 107 | 1, ran | 4.5 m, -1.2 m; 4.7 m; 9.0 m/s, -4.9 m/s; 10.2 m/s at -29° | `ch03/examples/n06/`: `main.py` | `example_3_6.py` |
| [Example 3.7](#example-37-height-and-range-of-a-projectile-i-a-batted-baseball) | Height and range of a projectile I: A batted baseball | 108 | 1, ran | 44.4 m, 39.6 m; 22.2 m/s, 10.0 m/s; 24.4 m/s at 24.2°; 3.02 s, 44.7 m; 6.04 s, 134 m; -29.6 m/s at -53.1° | `ch03/examples/n07/`: `main.py` | `example_3_7.py` |
| [Example 3.8](#example-38-height-and-range-of-a-projectile-ii-maximum-height-maximum-range) | Height and range of a projectile II: Maximum height, maximum range | 109 | 1, ran | formulas for t1, h, t2 and R; 90°; 45° | `ch03/examples/n08/`: `main.py` | `example_3_8.py` |
| [Example 3.9](#example-39-different-initial-and-final-heights) | Different initial and final heights | 109 | 2, 1 ran | -1.7 s or 0.98 s; 9.2 m | `ch03/examples/n09/`: `main.py`; tests (written out) | `example_3_9.py` |
| [Example 3.10](#example-310-the-zookeeper-and-the-monkey) | The zookeeper and the monkey | 110 | 2, 1 ran | a "show that": the dart hits | `ch03/examples/n10/`: `main.py`; tests (written out) | `example_3_10.py` |
| [Example 3.13](#example-313-relative-velocity-on-a-straight-road) | Relative velocity on a straight road | 116 | 4, all ran | -192 km/h; +192 km/h; no change | `ch03/examples/n13/`: `main.py` | `example_3_13.py` |
| [Example 4.1](#example-41-superposition-of-forces-finding-the-net-force) | Superposition of forces: Finding the net force | 133 | 8, 5 ran | -100 N, 80 N; 128 N at 141° | `ch04/examples/n01/`: `main.py`, `main_step_by_step.py`; tests (written out) | `example_4_1.py`, `example_4_1_step_by_step.py` |
| [Example 4.4](#example-44-newtons-second-law-i-determining-acceleration-from-force) | Newton's second law I: Determining acceleration from force | 141 | 1, ran | 0.50 m/s² | `ch04/examples/n04/`: `main.py` | `example_4_4.py` |
| [Example 4.5](#example-45-newtons-second-law-ii-determining-force-from-acceleration) | Newton's second law II: Determining force from acceleration | 141 | 3, all ran | -2.0 m/s²; ΣF_x = -0.90 N, f = 0.90 N | `ch04/examples/n05/`: `main.py`, `main_two_steps.py` | `example_4_5.py`, `example_4_5_two_steps.py` |
| [Example 4.7](#example-47-mass-and-weight) | Mass and weight | 145 | 1, ran | 2540 kg; -7.20 m/s² | `ch04/examples/n07/`: `main.py` | `example_4_7.py` |

## Example 2.4: Constant-acceleration calculations

PDF page 78. Old folder: `examples/up/ch2/up-example-2.4/`.

**Problem.** A motorcyclist moving east accelerates at a constant
4.0 m/s². At t = 0 he is 5.0 m east of a signpost, moving east at
15 m/s. (a) What are his position and velocity at t = 2.0 s? (b) Where
is he when his speed is 25 m/s?

**Book's answers.** Page 78.

| Part | Quantity | Printed |
|---|---|---|
| (a) | position at 2.0 s | 43 m |
| (a) | velocity at 2.0 s | 23 m/s |
| (b) | position when the speed is 25 m/s | 55 m |

**Old scripts.**

| Script | Style | Role | Runs | Time |
|---|---|---|---|---|
| `up-example-2.4-v3-001-step-by-step.py` | written out, all at once, zero equations | latest (written out) | yes, shim | 2 s |
| `up-example-2.4-v4-000-ks.py` | physics code, all at once, zero equations | draft (of v4-001) | yes, shim | 2 s |
| `up-example-2.4-v4-001-ks-display-solution.py` | physics code, all at once, zero equations | latest | yes, shim | 2 s |

v3-001 (14 lines printed):

```
m_1_x = m_0_v*m_1_t + m_0_x + m_1_t**2*m_a/2
m_1_x = 43
m_1_v = m_0_v + m_1_t*m_a
m_1_v = 23
m_1_x = (-m_0_v**2 + 2*m_0_x*m_a + m_1_v**2)/(2*m_a)
m_1_x = 55
```

v4-001 (20 lines printed; v4-000 prints the same 20 lines):

```
m_1_x = a_x_m_0_1*m_1_t**2/2 + m_0_v_x*m_1_t + m_0_x
m_1_x = 43
m_1_v_x = a_x_m_0_1*m_1_t + m_0_v_x
m_1_v_x = 23
m_1_x = (2*a_x_m_0_1*m_0_x - m_0_v_x**2 + m_1_v_x**2)/(2*a_x_m_0_1)
m_1_x = 55
```

**Techniques.** physics code (v4), written out (v3), all at once,
first root, zero equations, parts: (b) copies (a)'s values, removes
`m_1_t` and adds `m_1_v_x = 25`.

**Zeros.** v4-001: `Eq(m0.t, 0)` is an equation, appended after the
first display. Nothing eliminates it before the solve: `sp.solve` takes
it with the other connected unknowns, so no formula has `m_0_t`. The
port writes `known(m0.t, 0)` and `eliminate_zeros()` in the base,
before the parts branch, as `example_2_4_handwritten.py` does for v3.
No zero values.

**Physics code used.** `make_states_model("m", 2, include_v_av=True)`,
`kinematics_fundamental(m, axes=("x",), include_dt_defs=True,
include_eq2=True, include_eq7=True, include_eq10=True)`.

**Styles worth keeping.** v4-001 becomes `example_2_4.py`, the
physics-code version. v3-001 is already `example_2_4_handwritten.py`.

**In equarium.** `examples/up_15e/ch02/example_2_4_handwritten.py`
(v3-001), `tests/example_2_4.py` and `tests/test_solve.py`.

**Notes.** The book and the 15th edition agree with the scripts'
givens. v4-001 differs from v4-000 only in passing `want` to the
display (the want in red) and in a local `solve_and_display` helper, so
the plain output is the same. v3-001's name says "step-by-step", but
it eliminates nothing by hand: it imports `eliminate_variable_subst`
and never calls it.

## Example 2.5: Two objects with different accelerations

PDF page 78 (the solution runs onto page 79). Old folder:
`examples/up/ch2/up-example-2.5/`.

**Problem.** A motorist moving at a constant 15 m/s passes a school
crossing. At that moment a police officer on a motorcycle, at rest at
the crossing, starts after him with a constant 3.0 m/s². (a) How long
until the officer passes the motorist? At that time, (b) how fast is
the officer going, and (c) how far has each traveled?

**Book's answers.** Page 79.

| Part | Quantity | Printed |
|---|---|---|
| (a) | time until the officer passes | 10 s |
| (b) | the officer's speed then | 30 m/s |
| (c) | distance each has traveled | 150 m |

**Old scripts.**

| Script | Style | Role | Runs | Time |
|---|---|---|---|---|
| `up-example-2.5-v3-001-step-by-step.py` | written out, by hand, zero equations, links | latest (written out, by hand) | yes, shim | 7 s |
| `up-example-2.5-v3-002-concise.py` | written out, all at once, zero equations, links | latest (written out, all at once) | yes, shim | 3 s |
| `up-example-2.5-v4-000-ks.py` | physics code, all at once, zero equations, links | alternative (all at once) | yes, shim | 3 s |
| `up-example-2.5-v4-002-ks-eq-flat.py` | physics code, by hand, zero equations, links | latest | yes, shim | 6 s |

v3-001 (62 lines printed; it displays the system after each of its
eight elimination stages):

```
t_01 = 2*m_v/p_a
t_01 = 10
p_1_v = 2*m_v
p_1_v = 30
dist = 2*m_v**2/p_a
dist = 150
```

v3-002 (57 lines) prints the same six lines.

v4-002 (145 lines; the pprint of both models takes about 30):

```
t_01 = 2*m_v/a_x_p_0_1
t_01 = 10
p_1_v_x = 2*m_v
p_1_v_x = 30
dist = 2*m_v**2/a_x_p_0_1
dist = 150
```

v4-000 (144 lines) prints the same six lines.

The system v4-002 solves, after the zeros and its six eliminations:

```
v_av_x_m_0_1 = dist/dt_m_0_1
a_x_m_0_1 = 0
m_v = v_av_x_m_0_1
v_av_x_p_0_1 = dist/dt_p_0_1
a_x_p_0_1 = p_1_v_x/dt_p_0_1
p_1_v_x = 2*v_av_x_p_0_1
dt_m_0_1 = t_01
dt_p_0_1 = t_01
```

**Techniques.** physics code (v4), written out (v3), links (`m_v`,
`dist` and `t_01` tie the two objects' symbols together; v4-002 writes
them with a local `eq_flat`), zero equations, by hand (v3-001,
v4-002), all at once (v3-002, v4-000), first root.

**Zeros.** v4-002: five zero equations in its `eq_flat` (`p0.vel.x`,
`m0.pos.x`, `p0.pos.x`, `m0.t`, `p0.t`), eliminated by a local
`eliminate_zero_eqs` right after the links are added, before the six
link eliminations. The port writes five `known(sym, 0)` and
`eliminate_zeros()` at that point, then `eliminate` for `m0.vel.x`,
`m1.vel.x`, `m1.pos.x`, `p1.pos.x`, `m1.t`, `p1.t`. v4-000: the same
five, appended as equations and never eliminated: `sp.solve` takes
them. Its port writes the five knowns and `eliminate_zeros()` before
the first solve. No zero values in either.

**Physics code used.** `make_states_model("m", 2, include_v_av=True)`
and `("p", 2, ...)`, `kinematics_fundamental(..., axes=("x",),
include_dt_defs=True)`. v4-002 defines its own `eq_flat` and
`eliminate_zero_eqs`, which the library later gained (`misc.eq_flat`,
`eliminate_variable_subst.eliminate_zero_eqs`).

**Styles worth keeping.** v4-000 becomes `example_2_5.py`, the
physics code solved all at once. v4-002 becomes
`example_2_5_step_by_step.py`, the same model with its links
eliminated by hand between displays. v3-002 and v3-001 are already
`example_2_5_handwritten.py` and
`example_2_5_handwritten_step_by_step.py`. So 2.5 shows both
contrasts, written out against physics code and all at once against
by hand.

**In equarium.** `example_2_5_handwritten.py` (v3-002),
`example_2_5_handwritten_step_by_step.py` (v3-001), and
`tests/test_rewrite.py` (the six links of 2.5).

**Notes.** The book and the 15th edition agree with the scripts'
givens. The book finds two times, t = 0 and t = 10 s, and answers
with the second. The scripts print only 10, since `solve_system_2`
keeps the first root. Keeping every root doesn't bring t = 0 back:
`example_2_5_handwritten.py`, on equarium's `solve()`, has one root,
since t = 0 would make a denominator zero (`dist/t_01`). The motorist's acceleration
is never given: `a_x_m_0_1 = 0` comes out of the eliminations, from
the motorist's equal start and end speeds.

## Example 2.6: A freely falling coin

PDF page 80 (the solution is on page 81). Old folder:
`examples/up/ch2/up-example-2.6/`.

**Problem.** A coin is dropped from rest from a tower and falls
freely, ignoring air resistance. What are its position and velocity
after 1.0 s, 2.0 s and 3.0 s? The book takes upward as positive, so
a = -9.8 m/s².

**Book's answers.** Page 81.

| Part | Quantity | Printed |
|---|---|---|
| 1.0 s | position | -4.9 m |
| 1.0 s | velocity | -9.8 m/s |
| 2.0 s | position | -20 m |
| 2.0 s | velocity | -20 m/s |
| 3.0 s | position | -44 m |
| 3.0 s | velocity | -29 m/s |

**Old scripts.**

| Script | Style | Role | Runs | Time |
|---|---|---|---|---|
| `up-example-2.6-v1-000.py` | written out, all at once, zero equations, downward positive | draft (of v2-000) | yes, shim | 2 s |
| `up-example-2.6-v2-000.ks.py` | physics code, all at once, zero equations | latest | yes, shim | 3 s |

v1-000 (11 lines):

```
c_1_x = c_1_t**2*c_a/2
c_1_x = 4.90000000000000
c_1_v = c_1_t*c_a
c_1_v = 9.80000000000000
c_1_x = c_1_t**2*c_a/2
c_1_x = 19.6000000000000
c_1_x = c_1_t**2*c_a/2
c_1_x = 44.1000000000000
```

v2-000 (23 lines):

```
c_1_y = a_y_c_0_1*c_1_t**2/2
c_1_y = -4.90000000000000
c_1_v_y = a_y_c_0_1*c_1_t
c_1_v_y = -9.80000000000000
c_1_y = a_y_c_0_1*c_1_t**2/2
c_1_y = -19.6000000000000
c_1_y = a_y_c_0_1*c_1_t**2/2
c_1_y = -44.1000000000000
```

**Techniques.** physics code (v2), written out (v1), zero equations,
all at once, first root, parts (one base, `c_1_t` changed per part).

**Zeros.** v2-000: three zero equations in a local `eq_flat`
(`c0.t`, `c0.vel.y`, `c0.pos.y`), eliminated by a local
`eliminate_zero_eqs` right after, before any values. The port writes
three `known(sym, 0)` and `eliminate_zeros()` in the base. No zero
values.

**Physics code used.** `make_states_model("c", 2, include_v_av=True)`,
`kinematics_fundamental(c, axes=("y",))`.

**Styles worth keeping.** v2-000 becomes `example_2_6.py`. v1-000
isn't ported: v2-000 replaced it, and its written-out style is kept by
2.4 and 2.5.

**In equarium.** Nothing.

**Notes.** Neither script solves for the velocity at 2.0 s or 3.0 s,
so the book's -20 m/s and -29 m/s are never printed. The port adds
`c1.vel.y` as a want at those times (the formula is the 1.0 s one,
`a_y_c_0_1*c_1_t`, giving -19.6 and -29.4). v1-000 takes downward as
positive (a = +9.8), so its numbers are the book's with the sign
flipped. The book rounds -19.6 m to -20 m and -44.1 m to -44 m, both
within `Answer`'s half unit.

## Example 2.7: Up-and-down motion in free fall

PDF page 81 (the solution runs onto page 82). Old folder:
`examples/up/ch2/up-example-2.7/`.

**Problem.** A ball is thrown straight up at 15.0 m/s from level with
a roof railing, then falls freely (a = -9.80 m/s², upward positive,
origin at the railing). (a) Where is it, and how fast is it moving,
1.00 s and 4.00 s later? (b) What is its velocity when it is 5.00 m
above the railing? (c) How high does it go? (d) What is its
acceleration at the top?

**Book's answers.** Pages 81 and 82.

| Part | Quantity | Printed |
|---|---|---|
| (a) | position at 1.00 s | +10.1 m |
| (a) | velocity at 1.00 s | +5.2 m/s |
| (a) | position at 4.00 s | -18.4 m |
| (a) | velocity at 4.00 s | -24.2 m/s |
| (b) | velocity at 5.00 m | ±11.3 m/s |
| (c) | maximum height | +11.5 m |
| (d) | acceleration at the top | -9.80 m/s² |

**Old scripts.**

| Script | Style | Role | Runs | Time |
|---|---|---|---|---|
| `up-example-2.7-v1-000.py` | physics code, all at once, zero equations, zero values, several roots | latest | yes, shim | 3 s |

v1-000 (87 lines; (a)'s position at 1.00 s prints twice, once through
`solve_system_2` and once through every root):

```
b_1_y = b_1_t*(a_y_b_0_1*b_1_t + 2*b_0_v_y)/2
b_1_y = 10.1000000000000
b_1_v_y = a_y_b_0_1*b_1_t + b_0_v_y
b_1_v_y = 5.20000000000000
b_1_y = b_1_t*(a_y_b_0_1*b_1_t + 2*b_0_v_y)/2
b_1_y = -18.4000000000000
b_1_v_y = a_y_b_0_1*b_1_t + b_0_v_y
b_1_v_y = -24.2000000000000
Solution 1:
b_1_v_y = -sqrt(2*a_y_b_0_1*b_1_y + b_0_v_y**2)
b_1_v_y = -11.2694276695846
Solution 2:
b_1_v_y = sqrt(2*a_y_b_0_1*b_1_y + b_0_v_y**2)
b_1_v_y = 11.2694276695846
b_1_y = (-b_0_v_y**2 + b_1_v_y**2)/(2*a_y_b_0_1)
b_1_y = 11.4795918367347
```

The script ends with Example 2.8, in its entry below.

**Techniques.** physics code, zero equations, zero values ((c)'s
`b_1_v_y = 0.0`), all at once, first root ((a), through a local
`solve_and_display`), several roots ((b), through a local
`solve_and_display_` over `solve_system_multiple_solutions`), parts
(the values are rebuilt for each part).

**Zeros.** Two zero equations in a local `eq_flat` (`b0.t`,
`b0.pos.y`), eliminated by a local `eliminate_zero_eqs` right after,
before any values: `known(sym, 0)` and `eliminate_zeros()` in the
base. (c)'s `b1.vel.y = 0.0` is a value, set after that step:
`known(b1.vel.y, 0.0)` alone, so the formula keeps `b_1_v_y`, as the
old one does. It is a Float zero, which equarium counts as zero.

**Physics code used.** `make_states_model("b", 2)`,
`kinematics_fundamental(b, axes=["y"])`.

**Styles worth keeping.** v1-000 becomes `example_2_7.py`.

**In equarium.** `tests/test_roots.py`, written out with the
equations of 2.4 rather than the physics code, from v1-000: the four
parts, with (b)'s two roots and (c)'s formula keeping `v1`.

**Notes.** The book and the 15th edition agree with the script's
givens. The script uses -9.8 where the book writes -9.80: the same
number. (d) is answered only in a comment ("Acceleration is constant,
so a = -g"): the acceleration is a known, which `Answer` can't check,
since it checks wants. The port keeps it as a comment, or as an
assertion on the known, as `tests/test_roots.py` does. The book's
11.5 m is 11.4796 rounded.

## Example 2.8: Two solutions or one?

PDF page 82. Solved in 2.7's script,
`examples/up/ch2/up-example-2.7/up-example-2.7-v1-000.py`.

**Problem.** For the ball of Example 2.7, at what time after release
is it 5.00 m below the railing?

**Book's answers.** Page 82.

| Part | Quantity | Printed |
|---|---|---|
| | time at y = -5.00 m | +3.36 s (the other root, -0.30 s, is rejected) |

**Old scripts.** `up-example-2.7-v1-000.py`, the last part of its
run (see Example 2.7):

```
Solution 1:
b_1_t = (-b_0_v_y - sqrt(2*a_y_b_0_1*b_1_y + b_0_v_y**2))/a_y_b_0_1
b_1_t = 3.36451028118484
Solution 2:
b_1_t = (-b_0_v_y + sqrt(2*a_y_b_0_1*b_1_y + b_0_v_y**2))/a_y_b_0_1
b_1_t = -0.303285791388921
```

**Techniques.** physics code, zero equations, all at once, several
roots, filter (the book's, by hand: the script prints both and
chooses neither).

**Zeros.** As in 2.7: the base's two zero equations.

**Physics code used.** As in 2.7.

**Styles worth keeping.** Becomes `example_2_8.py`, which imports
2.7's base system from `example_2_7.py` and adds `b1.pos.y = -5.0`.

**In equarium.** `tests/test_roots.py`: both roots, and `where(t1 > 0)`
keeping 3.36.

**Notes.** The book's two roots are +3.36 s and -0.30 s. The book also
mentions y = +5.00 m (t = +0.38 s and +2.68 s) as a follow-up. No
script computes that.

## Exercise 2.1: A car's distance from its average velocity

PDF page 89. Old folder: `examples/up/ch2/exercises/2.1/`.

**Problem.** A car moves in the +x direction on a straight, level
road. Over its first 4.00 s its average velocity is 6.25 m/s. How far
does it travel in those 4.00 s?

**Book's answers.** Page 1563 (printed A-9).

| Part | Quantity | Printed |
|---|---|---|
| | distance in 4.00 s | 25.0 m |

**Old scripts.**

| Script | Style | Role | Runs | Time |
|---|---|---|---|---|
| `up-exercise-2.1-000.py` | physics code, all at once, zero values, units | latest | yes | 2 s |

000 (7 lines):

```
c_1_x = -c_0_t*v_av_x_c_0_1 + c_0_x + c_1_t*v_av_x_c_0_1
c_1_x = 25.0*meter
```

**Techniques.** physics code, all at once (`solve_and_display_`
version 1, every root), zero values, units.

**Zeros.** `c0.pos.x = 0*m` and `c0.t = 0*s` are values:
`known(sym, 0)` alone, so the formula keeps `c_0_t` and `c_0_x`.

**Physics code used.** `make_states_model("c", 2)`,
`kinematics_fundamental(c, axes=["x"])`.

**Styles worth keeping.** 000 becomes `exercise_2_1.py`.

**In equarium.** Nothing.

**Notes.** The 15th edition's 2.1 is this problem, with these givens.
`solve_system_multiple_solutions` prints a `Solving for unknowns: [...]`
line before each solution, in set order, which changes from run to
run. This and the other entries leave those lines out. `0*m` is plain
`0` in SymPy, so the zero values carry no units.

## Exercise 2.3: The slow trip home

PDF page 89. Old folder: `examples/up/ch2/exercises/2.3/`.

**Problem.** The usual drive home averages 105 km/h and takes 1 h
50 min. One day traffic holds the average to 70 km/h over the same
distance. How much longer does the trip take?

**Book's answers.** Page 1563 (printed A-9).

| Part | Quantity | Printed |
|---|---|---|
| | how much longer the slow trip takes | 55 min |

**Old scripts.**

| Script | Style | Role | Runs | Time |
|---|---|---|---|---|
| `up-exercise-2.3-000-two-steps.py` | physics code, two steps, all at once, zero values, units | latest (two steps) | yes | 3 s |
| `up-exercise-2.3-001-one-step.py` | physics code, one system, all at once, zero values, links, units | draft (of 002) | yes | 4 s |
| `up-exercise-2.3-002-one-step.py` | physics code, one system, all at once, zero values, links, units | latest (one step) | yes | 4 s |

000 (21 lines; the first trip is solved twice, the second time to keep
its number):

```
ca_1_x = -ca_0_t*v_av_x_ca_0_1 + ca_0_x + ca_1_t*v_av_x_ca_0_1
ca_1_x = 192.5*kilometer
cb_1_t = (cb_0_t*v_av_x_cb_0_1 - cb_0_x + cb_1_x)/v_av_x_cb_0_1
cb_1_t = 2.75*hour
```

002 (12 lines):

```
cb_1_t = (-ca_0_t*v_av_x_ca_0_1 + ca_0_x + ca_1_t*v_av_x_ca_0_1 + cb_0_t*v_av_x_cb_0_1 - cb_0_x)/v_av_x_cb_0_1
cb_1_t = 2.75*hour
```

001 (23 lines) prints 000's first two lines, then 002's two.

**Techniques.** physics code, units, zero values, two steps (000: the
first trip's distance, `tmp[0][1].rhs` from `return_solutions=True`,
becomes the second system's `cb_1_x`), links (001, 002:
`eq_flat(ca1.pos.x, cb1.pos.x)`), all at once.

**Zeros.** All values, in both scripts to port: `ca0.t = 0*h`,
`ca0.pos.x = 0*km`, `cb0.t = 0*h`, `cb0.pos.x = 0*km`. `known(sym, 0)`
alone, so the formulas keep them, as above.

**Physics code used.** `make_states_model("ca", 2)` and `("cb", 2)`,
`kinematics_fundamental(..., axes=["x"])`, `misc.eq_flat`.

**Styles worth keeping.** 000 becomes `exercise_2_3_two_steps.py`, and
002 becomes `exercise_2_3.py`: the spec's own example of the two-steps
contrast. The spec suggests `exercise_2_3_one_step.py` for 002, but
one step is the default (question 6). 001 isn't ported: it is 002 with
the first trip solved and displayed first.

**In equarium.** `tests/test_units.py`: two steps from 000, one step
from 002, each with the old formulas, and the one-step system adds
`longer = cb1t - ca1t` to reach 55 min.

**Notes.** The book's answer is how much longer the slow trip takes,
55 min. The old scripts stop at the slow trip's 2.75 h. The
difference, 2.75 h - 1 h 50 min = 0.9167 h, is 55 min. The ports add
the step, as `tests/test_units.py` does: `Eq(longer, cb1.t - ca1.t)`
in the one-step system, and in the second system of the two steps
(with `ca1.t` a known there). The old scripts write 1 h 50 min as
`1 * h + 50/60 * h`, a Float: the test writes `sp.Rational(50, 60)`.
The 15th edition's 2.3 ("Trip Home") is this problem, with these
givens.

## Exercise 2.5: Average velocity and speed of a walk

PDF page 89. Old folder: `examples/up/ch2/exercises/2.5/`.

**Problem.** You walk 60.0 m east from a door to a windmill in 28.0 s,
then 40.0 m west to a bench in 36.0 s. For the whole trip, what are
(a) your average velocity and (b) your average speed?

**Book's answers.** Page 1563 (printed A-9).

| Part | Quantity | Printed |
|---|---|---|
| (a) | average velocity | 0.313 m/s |
| (b) | average speed | 1.56 m/s |

**Old scripts.**

| Script | Style | Role | Runs | Time |
|---|---|---|---|---|
| `up-exercise-2.5-000.py` | physics code, all at once, by hand (displayed only), zero values, links, units | draft (of 001) | yes | 8 s |
| `up-exercise-2.5-001.py` | physics code, all at once, zero values, links, units | latest | yes | 5 s |

001 (18 lines):

```
avg_vel_02 = (dx_p_0_1 + dx_p_1_2)/(dt_p_0_1 + dt_p_1_2)
avg_vel_02 = 0.3125*meter/second
avg_speed_02 = (Abs(dx_p_0_1) + Abs(dx_p_1_2))/(dt_p_0_1 + dt_p_1_2)
avg_speed_02 = 1.5625*meter/second
```

000 (48 lines) prints the same four lines, between displays of its
eliminations.

**Techniques.** physics code (three states, two intervals), links
(`eq_flat` defines `dx_p_0_1`, `dx_p_1_2`, `avg_vel_02` and
`avg_speed_02`, the last with `sp.Abs`), all at once, zero values,
units. 000 eliminates `p_2_x`, `p_1_x`, `p_2_t`, `p_1_t` by hand and
displays the result, but then solves the original equations, so its
eliminations change nothing in the answer.

**Zeros.** 001: `p0.t = 0*s` and `p0.pos.x = 0*m` are values:
`known(sym, 0)` alone.

**Physics code used.** `make_states_model("p", 3)`,
`kinematics_fundamental(p, axes=["x"])`, `misc.eq_flat`.

**Styles worth keeping.** 001 becomes `exercise_2_5.py`. 000 isn't
ported: its by-hand eliminations are only displayed.

**In equarium.** Nothing.

**Notes.** The 15th edition's 2.5 is this problem, with these givens.
0.3125 m/s against the book's 0.313 m/s is exactly half a unit in the
last digit, 0.0005. `Answer` accepts it, since its check fails only on
a difference greater than the half unit, but it is the one book answer
here that sits on the boundary. The average speed's formula keeps
`Abs` of the two knowns, which SymPy evaluates once the numbers go in.

## Exercise 2.19: An antelope's speed and acceleration

PDF page 90. Old folder: `examples/up/ch2/exercises/2.19/`.

**Problem.** An antelope with constant acceleration covers the 70.0 m
between two points in 6.00 s, passing the second at 15.0 m/s. What
are (a) its speed at the first point and (b) its acceleration?

**Book's answers.** Page 1563 (printed A-9).

| Part | Quantity | Printed |
|---|---|---|
| (a) | speed at the first point | 8.33 m/s |
| (b) | acceleration | 1.11 m/s² |

**Old scripts.**

| Script | Style | Role | Runs | Time |
|---|---|---|---|---|
| `up-exercise-2.19-000.py` | physics code, all at once, zero values, units | latest | yes | 2 s |

000 (16 lines):

```
o_0_v_x = (-dt_o_0_1*o_1_v_x - 2*o_0_x + 2*o_1_x)/dt_o_0_1
o_0_v_x = 8.33333333333333*meter/second
a_x_o_0_1 = (2*dt_o_0_1*o_1_v_x + 2*o_0_x - 2*o_1_x)/dt_o_0_1**2
a_x_o_0_1 = 1.11111111111111*meter/second**2
```

**Techniques.** physics code, all at once, zero values, units.

**Zeros.** `o0.pos.x = 0*m` is a value: `known(o0.pos.x, 0)` alone.

**Physics code used.** `make_states_model("o", 2)`,
`kinematics_fundamental(o, axes=["x"])`.

**Styles worth keeping.** 000 becomes `exercise_2_19.py`.

**In equarium.** Nothing.

**Notes.** The 15th edition's 2.19 is this problem, with these givens.
The script gives the interval's `dt_o_0_1` rather than the two times.

## Exercise 2.21: A fast pitch

PDF page 90. Old folder: `examples/up/ch2/exercises/2.21/`.

**Problem.** A pitched ball leaves the hand at 45.0 m/s after being
accelerated uniformly from rest over 1.50 m. (a) What was its
acceleration? (b) How long did the pitch take?

**Book's answers.** Page 1563 (printed A-9).

| Part | Quantity | Printed |
|---|---|---|
| (a) | acceleration | 675 m/s² |
| (b) | time | 0.0667 s |

**Old scripts.**

| Script | Style | Role | Runs | Time |
|---|---|---|---|---|
| `up-exercise-2.21-000.py` | physics code, all at once, zero values, units, GUI | latest | yes, shim | 3 s |
| `up-exercise-2.21-001-gui.py` | physics code, GUI only | alternative (GUI) | yes, shim | 2 s |

000 (19 lines):

```
a_x_b_0_1 = (b_0_v_x - b_1_v_x)*(b_0_v_x + b_1_v_x)/(2*(b_0_x - b_1_x))
a_x_b_0_1 = 675.0*meter/second**2
dt_b_0_1 = 2*(-b_0_x + b_1_x)/(b_0_v_x + b_1_v_x)
dt_b_0_1 = 0.0666666666666667*second
```

Then it eliminates `v_av_x_b_0_1` by hand, displays the result, and
opens the GUI twice:

```
[shim: show_equation_gui('Fast Pitch Problem', want=a_x_b_0_1) skipped]
[shim: show_equation_gui('Fast Pitch Problem', want=dt_b_0_1) skipped]
```

001 (1 line) only opens the GUI:

```
[shim: show_equation_gui('Fast Pitch Problem - Find acceleration', want=a_x_b_0_1) skipped]
```

**Techniques.** physics code, all at once, zero values, units, by hand
(one elimination, displayed only), GUI.

**Zeros.** 000: `b0.pos.x = 0*m`, `b0.vel.x = 0*m/s` and `b0.t = 0*s`
are values: `known(sym, 0)` alone, so the formulas keep `b_0_x` and
`b_0_v_x`.

**Physics code used.** `make_states_model("b", 2)`,
`kinematics_fundamental(b, axes=["x"])`.

**Styles worth keeping.** 000's solves become `exercise_2_21.py`,
without the GUI calls. 001 isn't ported: the GUI is out of scope.

**In equarium.** Nothing.

**Notes.** The 15th edition's 2.21 is this problem, with these givens.
000 and 001 are the same setup; 001 drops the solves. The old venv's
Python has no tkinter, so both need the shim's GUI stub to import.

## Exercise 2.23: Stopping distance of an airbag

PDF page 90. Old folder: `examples/up/ch2/exercises/2.23/`.

**Problem.** A body survives a sudden stop if the deceleration stays
under 250 m/s². In a crash at 105 km/h, an airbag stops you. Over
what minimum distance must it stop you?

**Book's answers.** Page 1563 (printed A-9).

| Part | Quantity | Printed |
|---|---|---|
| | minimum stopping distance | 1.70 m |

**Old scripts.**

| Script | Style | Role | Runs | Time |
|---|---|---|---|---|
| `up-exercise-2.23-000.py` | physics code, all at once, zero values, units | latest | yes, shim | 2 s |

000 (7 lines):

```
b_1_x = (2*a_x_b_0_1*b_0_x - b_0_v_x**2 + b_1_v_x**2)/(2*a_x_b_0_1)
b_1_x = 22.05*kilometer**2*second**2/(hour**2*meter)
```

**Techniques.** physics code, all at once, zero values, units.

**Zeros.** `b1.vel.x = 0*m/s`, `b0.t = 0*s` and `b0.pos.x = 0*m` are
values: `known(sym, 0)` alone, so the formula keeps `b_0_x` and
`b_1_v_x`.

**Physics code used.** `make_states_model("b", 2)`,
`kinematics_fundamental(b, axes=["x"])`.

**Styles worth keeping.** 000 becomes `exercise_2_23.py`.

**In equarium.** `tests/test_units.py`, written out, from 000: the
formula, `in_units(meter, second)` to 1.70 m, and `Answer`'s unit
checks.

**Notes.** The 15th edition's 2.23 is this problem, with these givens.
The old script ends at the unconverted number, under a
`# unit conversion` comment with nothing after it: 22.05 km² s²/(h² m)
is 1.70 m. The port converts with `in_units(meter, second)`, as the
test does. It imports `show_equation_gui` without calling it, so it
needs the shim's GUI stub only to import.

## Example 3.6: An object projected horizontally

PDF page 107. Old folder: `examples/up/ch3/` (one script).

**Problem.** A motorcycle rider leaves the edge of a cliff moving
horizontally at 9.0 m/s, with the edge as the origin and no air
resistance. At 0.50 s after he leaves the edge, find (a) his position,
(b) his distance from the edge, and (c) his velocity, as components and
as magnitude and direction. (The book doesn't letter the parts; the
letters here are ours.)

**Book's answers.** Page 107.

| Part | Quantity | Printed |
|---|---|---|
| (a) | x at 0.50 s | 4.5 m |
| (a) | y at 0.50 s | -1.2 m |
| (b) | distance from the origin, r | 4.7 m |
| (c) | v_x | 9.0 m/s |
| (c) | v_y | -4.9 m/s |
| (c) | speed v | 10.2 m/s |
| (c) | angle α | -29° |

**Old scripts.**

| Script | Style | Role | Runs | Time |
|---|---|---|---|---|
| `up-example-3.6-v1-000.py` | physics code, all at once, zero equations, zero values | latest | yes, shim | 5 s |

It prints 101 lines. Each want is solved on its own, as the equations
grow (`dist`, then `vel_mag` and `vel_angle`, then `vel_angle_deg`):

```
m_1_x = m_1_t*(m_0_v_x + m_1_v_x)/2
m_1_x = 4.50000000000000
m_1_y = m_1_t*(-g*m_1_t + 2*m_0_v_y)/2
m_1_y = -1.22500000000000
dist = sqrt(m_1_t**2*((m_0_v_x + m_1_v_x)**2 + (g*m_1_t - 2*m_0_v_y)**2))/2
dist = 4.66375653309647
vel_mag = sqrt(m_1_v_x**2 + (g*m_1_t - m_0_v_y)**2)
vel_mag = 10.2474387043788
vel_angle = atan2(-g*m_1_t + m_0_v_y, m_1_v_x)
vel_angle = -0.498567905638218
vel_angle_deg = 180*atan2(-g*m_1_t + m_0_v_y, m_1_v_x)/pi
vel_angle_deg = -28.5658367937466
```

**Techniques.** physics code; zero equations; zero values; all at once
(`solve_system_multiple_solutions`, through a local `solve_and_display_`);
polar one-way, the other way round: the distance, speed and angle are
written by hand from the components (`dist = sqrt(x**2 + y**2)`,
`vel_mag = sqrt(...)`, `vel_angle = atan2(...)`), plus a degrees
equation `vel_angle_deg = vel_angle*180/pi`.

**Zeros.** Equations: `m_0_x`, `m_0_y`, `a_x_m_0_1` and `m_0_t`,
eliminated right after the base (local `eliminate_zero_eqs`, line 89).
Value: `m_0_v_y = 0.0`, set after that step, so it stays in the
formulas (`2*m_0_v_y` in `m_1_y`). `a_y_m_0_1 = -g` stays an equation.

**Physics code used.** `make_states_model`, `kinematics_fundamental`.

**Styles worth keeping.** One script, one style: `example_3_6.py`.

**In equarium.** Nothing.

**Notes.**
- **The shim is needed only for the import.** Line 9 imports
  `solve_system_2`, and a local `solve_and_display` calls it, but the
  script never calls that function. Every solve goes through
  `solve_system_multiple_solutions`.
- **`m_1_v_x = 9.0` is a value, not derived,** although
  `(-m_0_v_x + m_1_v_x)/dt_m_0_1 = 0` is in the system. So the book's
  v_x = 9.0 m/s is a given here, and `m_1_v_x` shows up in the formulas
  for `m_1_x` and `dist`. **v_y is never solved:** `m_1_v_y` is only
  solved inside `vel_mag` and `vel_angle`.
- `values[sp.pi] = sp.N(sp.pi)` (line 188) puts π in as a "value" to
  get a number for `vel_angle_deg`.
- g = 9.8 m/s², the book's 9.80. The old output matches the book at the
  book's precision: 4.5, -1.2 (-1.225), 4.7 (4.664), 10.2 (10.247),
  -29 (-28.57).
- The script's comments show the same formulas and numbers as the
  plain run.
- **The old repo's test** `tests/test_up_example_3_6.py` builds the same
  system (g 9.8, `m_1_v_x` 9.0 as a value) and pins, to 9 places, with
  exactly one solution each: x 4.5, y -1.225, dist 4.66375653309647,
  vel_mag 10.2474387043788, vel_angle -0.498567905638218 (rad),
  vel_angle_deg -28.5658367937466. Its degree solve has no
  `values[sp.pi]`.
- Edition: the 15th edition's 3.6 has the same givens (9.0 m/s,
  0.50 s).

## Example 3.7: Height and range of a projectile I: A batted baseball

PDF page 108. Old folder: `examples/up/ch3/` (one script).

**Problem.** A baseball leaves the bat at 37.0 m/s, 53.1° above the
horizontal, from ground level (y0 = 0), with no air resistance. (a) Find
its position and its velocity (magnitude and direction) at t = 2.00 s.
(b) When does it reach its highest point, and how high is it then?
(c) Find the horizontal range R, where it returns to ground level, and
its velocity just before it lands.

**Book's answers.** Page 108.

| Part | Quantity | Printed |
|---|---|---|
| (a) | x at 2.00 s | 44.4 m |
| (a) | y at 2.00 s | 39.6 m |
| (a) | v_x | 22.2 m/s |
| (a) | v_y | 10.0 m/s |
| (a) | speed v | 24.4 m/s |
| (a) | angle α | 24.2° |
| (b) | time t1 at the top | 3.02 s |
| (b) | height h | 44.7 m |
| (c) | time t2 at ground level | 6.04 s (and t2 = 0) |
| (c) | range R | 134 m |
| (c) | v_y at landing | -29.6 m/s |
| (c) | angle at landing | -53.1° |

(The book also prints v0x = 22.2 m/s and v0y = 29.6 m/s on the way,
and in (c) says v_x is unchanged.)

**Old scripts.**

| Script | Style | Role | Runs | Time |
|---|---|---|---|---|
| `up-example-3.7-v1-000.py` | physics code, all at once, zero equations, parts | latest | yes | 10 s |

It prints 239 lines. The solutions:

```
b_1_x = b0_vel_mag*b_1_t*cos(b0_vel_angle)
b_1_x = 44.4310966741154
b_1_y = b_1_t*(2*b0_vel_mag*sin(b0_vel_angle) - b_1_t*g)/2
b_1_y = 39.5566647280447
b_1_v_x = b0_vel_mag*cos(b0_vel_angle)
b_1_v_x = 22.2155483370577
b_1_v_y = b0_vel_mag*sin(b0_vel_angle) - b_1_t*g
b_1_v_y = 9.96833236402236
b1_vel_mag = sqrt(b0_vel_mag**2 - 2*b0_vel_mag*b_1_t*g*sin(b0_vel_angle) + b_1_t**2*g**2)
b1_vel_mag = 24.3495018026193
b1_vel_angle = atan2(b0_vel_mag*sin(b0_vel_angle) - b_1_t*g, b0_vel_mag*cos(b0_vel_angle))
b1_vel_angle = 0.421780406158419
b1_vel_angle_deg = 180*atan2(b0_vel_mag*sin(b0_vel_angle) - b_1_t*g, b0_vel_mag*cos(b0_vel_angle))/pi
b1_vel_angle_deg = 24.1662371541911
```

(b), with `Eq(b_1_v_y, 0)` added:

```
b_1_t = b0_vel_mag*sin(b0_vel_angle)/g
b_1_t = 3.01613989439575
b_1_y = b0_vel_mag**2*sin(b0_vel_angle)**2/(2*g)
b_1_y = 44.6212748258844
```

(c), with `Eq(b_1_y, 0)` added:

```
b_1_x = b0_vel_mag**2*sin(2*b0_vel_angle)/g
b_1_x = 134.010403230554
b_1_v_x = b0_vel_mag*cos(b0_vel_angle)
b_1_v_x = 22.2155483370577
b_1_v_y = -b0_vel_mag*sin(b0_vel_angle)
b_1_v_y = -29.5883323640224
```

**Techniques.** physics code; zero equations; all at once; parts
(`values_a` with t = 2.00 s, `eqs_b` and `eqs_c` copies with one
equation added each); polar one-way for the launch (components from
`b0_vel_mag` and `b0_vel_angle`, its own symbols, not the State's
`vel.mag` and `vel.angle`); polar one-way the other way round for the
velocity at 2.00 s (`sqrt`, `atan2`, by hand); by hand
(`eliminate_variable_subst(eqs, b1_vel_angle)` before the degree solve).

**Zeros.** Equations: `b_0_x`, `b_0_y`, `a_x_b_0_1` and `b_0_t`,
eliminated right after the base (line 86). Then (b)'s `Eq(b_1_v_y, 0)`
and (c)'s `Eq(b_1_y, 0)` are equations added to a copy and never passed
to `eliminate_zero_eqs`; the all-at-once solve takes them as unknowns,
so their zero goes into the formulas (`b_1_t = b0_vel_mag*sin(b0_vel_angle)/g`
has no `b_1_v_y`). To keep those formulas, the port needs
`known(b1vy, 0)` then `eliminate_zeros()` in (b)'s branch, and
`known(b1y, 0)` then `eliminate_zeros()` in (c)'s. No zero values.
`b_0_v_x = b_1_v_x` is added as an equation (redundant with a_x = 0).

**Physics code used.** `make_states_model`, `kinematics_fundamental`.

**Styles worth keeping.** One script: `example_3_7.py`.

**In equarium.** Nothing.

**Notes.**
- **g = 9.81 m/s², the book's is 9.80.** At the book's precision, two
  old numbers then miss the book: the speed at 2.00 s, 24.3495 (book
  24.4; `Answer` allows ±0.05, it's off by 0.0505), and the height h,
  44.621 (book 44.7). With g = 9.80 the same formulas give 24.358 and
  44.667, and every printed value matches, t2 = 6.038 included. The
  other old numbers match the book as they are.
- **Not solved by the old script:** (c)'s time t2 = 6.04 s and landing
  angle -53.1°. The t2 = 0 root never appears: `dt_b_0_1` is in
  denominators, so SymPy drops it, and (c) prints one solution each.
- **The by-hand elimination of `b1_vel_angle` is needed** (the script's
  comment says "for some reason"). A scratch check with the old
  library, without it, got `KeyError: b1_vel_angle_deg` after 12.3 s:
  `sp.solve`'s solutions didn't include the degree symbol. 3.6 solves
  the same kind of degree equation without the step; it also has
  `values[sp.pi]`.
- The comment after the 2.00 s v_y says `9.96833236402235`; the plain run
  prints `9.96833236402236`. Every other comment matches the log.
- **The old repo's test** `tests/test_up_example_3_7.py` (g 9.81, the
  angle as `math.radians(53.1)`) pins, to 9 places: (a) x
  44.4310966741154, y 39.5566647280447, v_x 22.2155483370577, v_y
  9.96833236402235, speed 24.3495018026193, angle 0.421780406158419 rad
  and 24.1662371541911° (after the same by-hand elimination); (b) t
  3.01613989439575, height 44.6212748258844; (c) x 134.010403230554,
  v_x 22.2155483370577, v_y -29.5883323640224.
- Edition: the same givens (37.0 m/s, 53.1°, 2.00 s).

## Example 3.8: Height and range of a projectile II: Maximum height, maximum range

PDF page 109 (it shares the page with 3.9, which starts above it in the
extracted text). Old folder: `examples/up/ch3/` (one script).

**Problem.** A projectile is launched at speed v0 and angle α0 between 0
and 90°, from and back to the same height, with no air resistance. As
formulas in v0, α0 and g, find (a) its maximum height h and (b) its
horizontal range R. For a given v0, (c) which α0 gives the greatest h,
and (d) which gives the greatest R?

**Book's answers.** Page 109.

| Part | Quantity | Printed |
|---|---|---|
| (a) | time t1 at the top | t1 = v0 sin α0 / g |
| (a) | maximum height | h = v0² sin² α0 / (2g) |
| (b) | time t2 back at launch height | t2 = 2 v0 sin α0 / g |
| (b) | range | R = v0² sin 2α0 / g |
| (c) | α0 for the greatest h | 90° |
| (d) | α0 for the greatest R | 45° |

**Old scripts.**

| Script | Style | Role | Runs | Time |
|---|---|---|---|---|
| `up-example-3.8-v1-000.py` | physics code, polar two-way, by hand, all at once, parts | latest | yes | 7 s |

It prints 83 lines, formulas only (no numbers):

```
p_1_y = p_0_v_mag**2*sin(p_0_v_angle)**2/(2*g)
p_1_x = p_0_v_mag**2*sin(2*p_0_v_angle)/(2*g)
```

The second is half the book's R: see Notes.

**Techniques.** physics code; zero equations; polar two-way (the four
equations of `magnitude_and_angle_equations`, written by hand on
`p0.vel.mag` and `p0.vel.angle`); by hand
(`eliminate_variable_subst(tmp, p0.vel.x)` before the solve); all at
once; parts (`eqs_a` for the top, `eqs_b` for the range).

**Zeros.** Equations, all eliminated with the local
`eliminate_zero_eqs`: `p_0_x`, `p_0_y`, `a_x_p_0_1` and `p_0_t` after
the base (line 81); (a)'s `p_1_v_y` in `eqs_a` (line 110); (b)'s `p_1_y`
in `eqs_b` (line 140). No zero values. `p_0_v_x = p_1_v_x` is added as
an equation.

**Physics code used.** `make_states_model`, `kinematics_fundamental`
(and the State's `vel.mag`, `vel.angle` symbols).

**Styles worth keeping.** One script: `example_3_8.py`.

**In equarium.** Nothing.

**Notes.**
- **Bug: the range is solved from the wrong system.** Line 145 solves
  `tmp`, the top-of-flight system (`p_1_v_y = 0`, `p_0_v_x` eliminated),
  for `p_1_x`, instead of `eqs_b`. So it prints x at the top, half the
  range: `.../(2*g)`. A scratch check with the old library: `eqs_b` with
  the same by-hand elimination of `p_0_v_x` gives the book's
  `p_1_x = p_0_v_mag**2*sin(2*p_0_v_angle)/g` in 0.3 s, and its `p_1_t`
  is `2*p_0_v_mag*sin(p_0_v_angle)/g`; the top system's `p_1_t` is
  `p_0_v_mag*sin(p_0_v_angle)/g`. Both match the book.
- **The by-hand step is needed:** without eliminating `p_0_v_x`, both
  `eqs_a` (for `p_1_y`) and `eqs_b` (for `p_1_x`) raise
  `ValueError: No solutions found.` in the old library, the same
  two-way-polar failure as 3.9.
- **(c) and (d) aren't answered:** nothing maximizes over α0.
- `values` maps `p0.vel.mag` to a Symbol `v0` and `p0.vel.angle` to
  `a0`, and g to 9.81, but nothing prints the substituted form, so the
  formulas keep `p_0_v_mag` and `p_0_v_angle`, and 9.81 is never used.
  `v0` and `a0` then show up in the "Solving for unknowns" lists.
- No old test.
- Edition: the same problem (symbolic).

## Example 3.9: Different initial and final heights

PDF pages 109 to 110 (the answer is on 110). Old folder:
`examples/up/ch3/` (two scripts).

**Problem.** A ball is thrown from a window 8.0 m above the ground at
10.0 m/s, 20.0° below the horizontal, with no air resistance. (a) How
far from the window, horizontally, does it land?

**Book's answers.** Page 110.

| Part | Quantity | Printed |
|---|---|---|
| (a) | time to reach the ground, both roots | -1.7 s or 0.98 s (the negative one discarded) |
| (a) | horizontal distance x | 9.2 m |

**Old scripts.**

| Script | Style | Role | Runs | Time |
|---|---|---|---|---|
| `up-example-3.9-v2.py` | physics code, polar two-way, eliminating, zero equations | latest | yes | 14 s |
| `up-example-3.9-v1-000.py` | physics code, polar two-way, all at once, then by hand | draft (replaced by v2) | fails: `ValueError: No solutions found.` | 5 s |

v2 prints 44 lines. `solve_with_elimination_attempts` tries the solve
eight times (seven eliminations) and prints
`Elimination attempts elapsed: 10.173s`, then:

```
Solution 1:
b_1_x = b_0_v_mag*(b_0_v_mag*sin(b_0_v_angle) - sqrt(b_0_v_mag**2*sin(b_0_v_angle)**2 + 2*b_0_y*g))*cos(b_0_v_angle)/g
b_1_x = -15.7161745661753
Solution 2:
b_1_x = b_0_v_mag*(b_0_v_mag*sin(b_0_v_angle) + sqrt(b_0_v_mag**2*sin(b_0_v_angle)**2 + 2*b_0_y*g))*cos(b_0_v_angle)/g
b_1_x = 9.16380341748480
```

v1-000 prints the base and the system (45 lines with the traceback),
then fails at line 142, its first solve, all at once:
`ValueError: No solutions found.` from `solve_system_multiple_solutions`
(`solve_system.py` line 236). Its own comment there predicts the
error. Everything after it never runs: nine `eliminate_variable_subst`
calls by hand (`dt`, `v_av.x`, `v_av.y`, `a.y`, `b0.vel.x`, `b0.vel.y`,
`b1.vel.x`, `b1.vel.y`, `b1.t`), then a solve of the first remaining
equation alone, whose comments record the same two roots as v2; then
two more experiments (the three-equation leftover, commented
`IndexError: Index out of range: a[1]`, and `eliminate_singleton_equations`).

**Techniques.** v2: physics code; zero equations; polar two-way
(`magnitude_and_angle_equations`); eliminating (`solve_and_display_`
with `version=2`); several roots, printed both, no filter. v1-000: all
at once (fails); by hand (unreached).

**Zeros.** v2: equations `b_0_x`, `a_x_b_0_1`, `b_0_t` and `b_1_y` (it
hits the ground), eliminated right after the base (library
`eliminate_zero_eqs`, line 59). No zero values. `b_0_y = 8.0` is a value,
and `b_0_v_x = b_1_v_x` an equation.

**Physics code used.** `make_states_model`, `kinematics_fundamental`,
`magnitude_and_angle_equations`.

**Styles worth keeping.** v2 as `example_3_9.py`. v1-000's by-hand
sequence is what `eliminating()` automates; see the recommendations.

**In equarium.** `tests/test_roots.py`: one-way polar, written out, all
at once, from v2: the two roots (`"-15.7", "9.2"`), `where(b1x > 0)`,
and with the time, `b1t` 0.98. `tests/test_strategies.py`: two-way, as
v2: `all_at_once` finds no roots; `eliminating()` finds them after seven
eliminations, about 6 s (slow).

**Notes.**
- **The book prints 9.2 m; the old v2 prints 9.16** (9.16380341748480),
  which matches at the book's precision.
- g = 9.81 m/s², the book's 9.80; with 9.80 the root is 9.167. No
  difference at 2 significant figures.
- **The origin differs from the book's:** v2 puts y = 0 at the ground
  (`b_1_y = 0`, `b_0_y = 8.0`); the book puts it at the hand and lands at
  y = -8.0 m. Same answer.
- The old scripts never solve for the time; the book's -1.7 s and
  0.98 s are its roots. The negative x root (-15.7 m) is the book's
  t = -1.7 s.
- v2's comments show the same output as the plain run.
- **The old repo's test** `tests/test_up_example_3_9_v2.py` (g 9.81,
  `b0.pos.y` 8.0, speed 10.0, angle `math.radians(-20.0)`, its own copy
  of `magnitude_and_angle_equations`) solves with
  `solve_with_elimination_attempts` and pins exactly two solutions,
  sorted, to 9 places: -15.7161745661753 and 9.16380341748480.
- Edition: the same givens (8.0 m, 10.0 m/s, 20.0° below).

## Example 3.10: The zookeeper and the monkey

PDF pages 110 to 111 (the conclusion is on 111). Old folder:
`examples/up/ch3/` (two scripts).

**Problem.** A monkey hangs in a tree at horizontal distance d from a
dart gun, which is aimed straight at it at angle α0 with muzzle speed
v0, so the monkey starts at height d tan α0 above the muzzle. The monkey
lets go just as the dart is fired; no air resistance. (a) Show that the
dart always hits the monkey, provided it gets there before the monkey
reaches the ground. All givens are symbols.

**Book's answers.** Pages 110 and 111.

| Part | Quantity | Printed |
|---|---|---|
| (a) | time when the x's agree | t = d / (v0 cos α0) |
| (a) | monkey's height | y_monkey = d tan α0 - ½ g t² |
| (a) | dart's height | y_dart = (v0 sin α0) t - ½ g t² |
| (a) | the condition for a hit | d tan α0 = (v0 sin α0) t, which holds at t = d / (v0 cos α0) |

**Old scripts.**

| Script | Style | Role | Runs | Time |
|---|---|---|---|---|
| `up-example-3.10-v1-001.py` | physics code, two models, by hand, links, show that | latest | yes | 21 s |
| `up-example-3.10-v1-000.py` | physics code, by hand | draft (replaced by v1-001) | fails: `IndexError` at line 121 | 17 s |

v1-001 prints 90 lines. The dart's two equations it keeps (`tmp[0]`,
`tmp[1]`, after eight eliminations by hand), the monkey's (`tmp[2]`,
after five), and what is left after linking them and eliminating
`d_1_t`, `m_1_t`, `d_1_y`, `m_1_y`, `y` and `t`:

```
d_0_v_mag*cos(d_0_v_angle) = d_1_x/d_1_t
d_0_v_mag*sin(d_0_v_angle) = d_1_t*g/2 + d_1_y/d_1_t
D*tan(d_0_v_angle) = g*m_1_t**2/2 + m_1_y
...
d_0_v_mag*sin(d_0_v_angle) = D*d_0_v_mag*sin(d_0_v_angle)/d_1_x
```

The last line is the stated condition: it holds exactly when the dart
reaches x = D. It also prints, during the dart's eliminations (both
versions): `Warning: No solutions found when solving for variable.` /
`Equation: Eq((-d_0_v_x + d_1_v_x)/dt_d_0_1, 0), Variable: dt_d_0_1`.

v1-000 has `Eq(d1.pos.x, D)` in the dart's system and eliminates
`d1.pos.x`, so its dart equation reads `d_0_v_mag*cos(d_0_v_angle) = D/d_1_t`.
It gets as far as the dart's height,
`d_1_y = d_0_v_mag*d_1_t*sin(d_0_v_angle) - d_1_t**2*g/2` (log line 54),
then fails at line 121, `sp.expand(sp.solve(tmp[0], d1.pos.y)[0])`:
`tmp[0]` has no `d_1_y`, so `sp.solve` returns `[]`, and
`IndexError: list index out of range`. It never reaches the monkey.

**Techniques.** v1-001: physics code (two `make_states_model`s); zero
equations; polar two-way for the dart (`magnitude_and_angle_equations(d0)`);
by hand (`eliminate_variable_subst`, 19 calls in a fixed order, and
equations picked by index); links (by hand: `d1.t = t`, `m1.t = t`,
`d1.y = y`, `m1.y = y`, through new symbols `t` and `y`); show that.

**Zeros.** v1-001, all equations, each model's eliminated in its own
list before they're combined: the dart's `d_0_x`, `d_0_y`, `a_x_d_0_1`,
`d_0_t` (line 76); the monkey's `a_x_m_0_1`, `m_0_t`, `m_0_v_x`,
`m_0_v_y`, `m_1_v_x` (line 138). No zero values. `m_0_x = D`,
`m_0_y = D*tan(d_0_v_angle)`, `a_y = -g` (both) and `d_0_v_x = d_1_v_x`
stay equations.

**Physics code used.** `make_states_model` (twice),
`kinematics_fundamental`, `magnitude_and_angle_equations`. (`link_same_time`
isn't used; the links are written by hand.)

**Styles worth keeping.** v1-001 as `example_3_10.py`: the only
version, a show-that by hand.

**In equarium.** `tests/test_rewrite.py`, from v1-001, written out, with
one-way polar for the dart (v1-001 has two-way): 24 equations; with
`ORDER_3_10` (the monkey's x first) one equation is left,
`D*v_mag*sin(angle)/d1x = v_mag*sin(angle)`, true at `d1x = D`; with
`Eq(d1x, D)` added and `d1x` eliminated too, none.

**Notes.**
- **"Show that" ends with the stated condition, not an empty system.**
  It reaches an empty system once `Eq(d1x, D)` is added.
- **Stale comments in v1-001:** line 188 says `# empty list of
  equations`, and line 161 says `= D/d_1_t`. Both date from v1-000's
  `Eq(d1.pos.x, D)`, now commented out (line 66). The plain run prints
  the condition above.
- v1-001 keeps only `tmp[0]`, `tmp[1]` (the dart) and `tmp[2]` (the
  monkey) and drops the rest, including the monkey's x equations
  (`D = m_0_x`, `v_av_x_m_0_1 = 0`) and the dart's polar ones.
- `values` maps `d0.vel.mag` and `d0.vel.angle` to themselves ("test
  value") and g to 9.81; they only make the displays treat them as
  known. The book's d is the script's `D`.
- `misc.isolate_variable` is imported in v1-001 (line 103) but used
  only in v1-000.
- No old test.
- Edition: the same problem (symbolic).

## Example 3.13: Relative velocity on a straight road

PDF page 116. Old folder: `examples/up/ch3/up-example-3.13/` (four
scripts).

**Problem.** You drive north at a constant 88 km/h on a straight road; a
truck in the other lane comes toward you at a constant 104 km/h. Treat
it in one dimension, north positive. Find (a) the truck's velocity
relative to you, (b) your velocity relative to the truck, and (c) how
these change once you've passed each other.

**Book's answers.** Page 116.

| Part | Quantity | Printed |
|---|---|---|
| (a) | v_T/Y-x | -192 km/h |
| (b) | v_Y/T-x | +192 km/h |
| (c) | after passing | they don't change |

**Old scripts.**

| Script | Style | Role | Runs | Time |
|---|---|---|---|---|
| `up-example-3.13-001-eq.py` | written out, units, all at once | latest | yes | 2 s |
| `up-example-3.13-001-eq copy.py` | the same | duplicate of `-001-eq.py` (byte for byte, `cmp`) | yes | 2 s |
| `up-example-3.13-000.py` | plain SymPy, `subs`, no combine_equations | draft (replaced by 001-eq) | yes, prints nothing | 3 s |
| `up-example-3.13-002-reference-frames.py` | `sympy.physics.vector` frames and points | other library | yes | 2 s |

001-eq prints 8 lines (the copy's log is identical):

```
v_TY = v_TE - v_YE
v_TY = -192.0*kilometer/hour
v_YT = -v_TE + v_YE
v_YT = 192.0*kilometer/hour
```

000 computes `v_TY.subs(values)` and `v_YT.subs(values)` without
printing them: its log is empty. Its comments give
`-192*kilometer/hour` and `192*kilometer/hour`.

002 prints 60 lines of prose and vectors, among them
`v_T/Y = - 192*E.x`, `v_Y/T = 192*E.x` and `Magnitude: 192 km/h`, and
answers (c) in printed text ("The relative velocities do NOT change!").

**Techniques.** 001-eq: written out (`v_TE = v_TY + v_YE`,
`v_YT = -v_TY`, the book's 3.32 and 3.33); units
(`sympy.physics.units` km and h in the values); all at once
(`solve_and_display_`, version 1).

**Zeros.** None.

**Physics code used.** None (001-eq star-imports `kinematics_states`
and `newtons_laws` but uses neither).

**Styles worth keeping.** 001-eq as `example_3_13.py`. It is written
out, but there is no physics-code version to contrast it with, so it
takes no slug.

**In equarium.** Nothing.

**Notes.**
- **`up-example-3.13-001-eq copy.py` is a byte-for-byte duplicate** of
  `up-example-3.13-001-eq.py` (`cmp` exits 0), and their logs are
  identical.
- The old output matches the book. It prints `-192.0`, a Float, from
  `sp.N`.
- (c) is prose in the book; only 002 says it, as printed text.
- No old test.
- Edition: the same givens (88 km/h, 104 km/h).

## Example 4.1: Superposition of forces: Finding the net force

PDF page 133, answers included. Old folder:
`examples/up/ch4/up-example-4.1/`.

**Problem.** Three wrestlers pull horizontally on a belt, seen from
above: F1 = 50 N along +x, F2 = 120 N along -y, and F3 = 250 N at 53°
above the -x axis (127° from +x). The directions come from the book's
figure; the scripts give them as angles 0°, 270° and 180° - 53°.
(a) Find the x- and y-components of the net force R on the belt.
(b) Find its magnitude and direction.

**Book's answers.** Page 133.

| Part | Quantity | Printed |
|---|---|---|
| (a) | R_x | -100 N |
| (a) | R_y | 80 N |
| (b) | magnitude R | 128 N |
| (b) | direction, from +x | 141° |

**Old scripts.**

| Script | Style | Role | Runs | Time |
|---|---|---|---|---|
| `up-example-4.1-v1-000.py` | written out, polar one-way for F1 to F3 and two-way for R, by hand then all at once | draft (of v1-001) | yes | 16 s |
| `up-example-4.1-v1-001.py` | the same equations plus degrees, all at once | draft (v1-002 refactors it: same equations, same output) | yes | 17 s |
| `up-example-4.1-v1-002.py` | written out with a local `force_equations` helper, polar one-way for F1 to F3 and two-way for R, all at once | alternative (the two-way style that works) | yes | 17 s |
| `up-example-4.1-v1-003-4-force-equations.py` | written out, polar two-way for every force and R, eliminating | alternative (two-way, eliminating; never reaches \|R\|) | fails: `ValueError: No solutions found.` at `R_angle_deg` | 559 s |
| `up-example-4.1-v1-004-4-force-equations-elim.py` | written out, polar one-way, by hand then all at once, then eliminating | draft (of v1-005 and v1-006) | fails: `NameError: R_angle_deg` | 10 s |
| `up-example-4.1-v1-005.py` | written out, polar one-way, by hand (exploring R_x), then eliminating | draft (of v1-006) | fails: `NameError: R_angle_deg` | 13 s |
| `up-example-4.1-v1-006-ok-manual-elim.py` | written out, polar one-way, by hand then all at once | alternative (by hand) | yes | 9 s |
| `up-example-4.1-v1-007-ok.py` | written out, polar one-way, all at once | latest | yes | 7 s |

How each differs from the one before (all eight were added in one
commit, `322a4a0`, so the numbers are the only order):

- **v1-000:** one `eq_flat` with the superposition (2), the forces'
  components from polar (6), and R both ways (4: `R_x = R_mag*cos(R_angle)`,
  `R_y = ...`, `R_mag = sqrt(...)`, `R_angle = atan2(...)`). Eliminates
  F1_x, F1_y, F2_x, F2_y, F3_x, F3_y by hand, then solves all at once
  for R_x, R_y, R_mag, R_angle (radians only).
- **v1-001 vs v1-000:** drops the by-hand eliminations (solves the full
  system), adds `R_angle_deg = deg(R_angle)` and a fifth want, and
  deletes v1-000's commented-out `Point3` experiments.
- **v1-002 vs v1-001:** moves the components-from-polar equations into
  a local `force_equations(force)` (two equations, one-way), applied to
  F1, F2, F3 and R, plus R's mag and angle equations. The same 13
  equations in the same order; the log is identical but for the order
  of the "Solving for unknowns" lists.
- **v1-003 vs v1-002:** `force_equations` grows to four equations, both
  ways (the same four the library's `magnitude_and_angle_equations`
  writes for a State's velocity), for every force and R: 19 equations
  with the degrees. R_x, R_y, R_mag and R_angle switch to
  `solve_and_display_(..., version=2)`, eliminating; R_angle_deg stays
  all at once.
- **v1-004 vs v1-003:** the system becomes one-way: local
  `polar_to_components` for F1 to F3, `components_to_polar` for R, and
  a local `superposition_equations`; the `force_equations` calls and
  the R_angle_deg symbol and equation are commented out. Adds a by-hand
  section: eliminate F1_x, F2_x, F3_x and solve all at once for R_x;
  eliminate F1_y, F2_y, F3_y and solve for R_y. Its comments (five
  identical solutions for R_x, "takes a very long time" for R_y,
  listings with `F1_mag = sqrt(...)`) describe the two-way system, so
  they come from a two-way run, not from this one. It keeps v1-003's
  eliminating calls on the full system, which now take about 1 s each,
  and fails at the last solve, whose symbol is commented out.
- **v1-005 vs v1-004:** drops the per-component solves, keeps the six
  eliminations, and adds an exploration: eliminating R_x by hand picks
  `R_mag = sqrt(R_x**2 + R_y**2)` rather than the linear (1), giving
  `sqrt((R_mag - R_y)*(R_mag + R_y))` and `R_mag = sqrt(R_mag**2)`;
  eliminating R_y next brings back `R_mag*sin(R_angle)`. Then the same
  eliminating calls and the same NameError.
- **v1-006 vs v1-005:** drops the exploration and the eliminating
  calls. After the six by-hand eliminations, solves the four remaining
  equations all at once for R_mag and R_angle, then defines
  R_angle_deg again, adds its equation, and solves for it.
- **v1-007 vs v1-006:** drops the six by-hand eliminations and solves
  the full one-way system all at once. It never asks for R_x or R_y.

v1-007 (40 lines printed), all at once, one-way:

```
R_mag = sqrt(F1_mag**2 + 2*F1_mag*F2_mag*cos(F1_angle - F2_angle) + 2*F1_mag*F3_mag*cos(F1_angle - F3_angle) + F2_mag**2 + 2*F2_mag*F3_mag*cos(F2_angle - F3_angle) + F3_mag**2)
R_mag = 128.204889993952
R_angle = atan2(F1_mag*sin(F1_angle) + F2_mag*sin(F2_angle) + F3_mag*sin(F3_angle), F1_mag*cos(F1_angle) + F2_mag*cos(F2_angle) + F3_mag*cos(F3_angle))
R_angle = 2.47114041353915
R_angle_deg = 180*atan2(F1_mag*sin(F1_angle) + F2_mag*sin(F2_angle) + F3_mag*sin(F3_angle), F1_mag*cos(F1_angle) + F2_mag*cos(F2_angle) + F3_mag*cos(F3_angle))/pi
R_angle_deg = 141.585916280006
```

v1-006 (45 lines): the same three wants, formulas and numbers, after
the six by-hand eliminations leave:

```
F1_mag*cos(F1_angle) = -F2_mag*cos(F2_angle) - F3_mag*cos(F3_angle) + R_x
F1_mag*sin(F1_angle) = -F2_mag*sin(F2_angle) - F3_mag*sin(F3_angle) + R_y
R_mag = sqrt(R_x**2 + R_y**2)
R_angle = atan2(R_y, R_x)
```

v1-002 (41 lines), all at once, R two-way. v1-001 prints the same;
v1-000 the first four, by hand first:

```
R_x = F1_mag*cos(F1_angle) + F2_mag*cos(F2_angle) + F3_mag*cos(F3_angle)
R_x = -100.453755788012
R_y = F1_mag*sin(F1_angle) + F2_mag*sin(F2_angle) + F3_mag*sin(F3_angle)
R_y = 79.6588775118232
R_mag = sqrt(F1_mag**2 + 2*F1_mag*F2_mag*cos(F1_angle - F2_angle) + 2*F1_mag*F3_mag*cos(F1_angle - F3_angle) + F2_mag**2 + 2*F2_mag*F3_mag*cos(F2_angle - F3_angle) + F3_mag**2)
R_mag = 128.204889993952
R_angle = atan2(F1_mag*sin(F1_angle) + F2_mag*sin(F2_angle) + F3_mag*sin(F3_angle), F1_mag*cos(F1_angle) + F2_mag*cos(F2_angle) + F3_mag*cos(F3_angle))
R_angle = 2.47114041353915
R_angle_deg = 180*atan2(F1_mag*sin(F1_angle) + F2_mag*sin(F2_angle) + F3_mag*sin(F3_angle), F1_mag*cos(F1_angle) + F2_mag*cos(F2_angle) + F3_mag*cos(F3_angle))/pi
R_angle_deg = 141.585916280006
```

v1-003 (84 lines) fails after 9 min 19 s. Eliminating gives R_x and
R_y, then "solves" |R| and the angle as formulas in other unknowns, and
the all-at-once solve for R_angle_deg raises:

```
Elimination attempts elapsed: 1m 45.61s
R_x = F1_mag*cos(F1_angle) + F2_mag*cos(F2_angle) + F3_mag*cos(F3_angle)
R_x = -100.453755788012
Elimination attempts elapsed: 3m 50.60s
R_y = F1_mag*sin(F1_angle) + F2_mag*sin(F2_angle) + F3_mag*sin(F3_angle)
R_y = 79.6588775118232
Elimination attempts elapsed: 1m 51.00s
R_mag = sqrt(R_x**2 + R_y**2)
R_mag = (R_x**2 + R_y**2)**0.5
Elimination attempts elapsed: 1m 34.65s
R_angle = atan2(R_y, R_x)
R_angle = atan2(R_y, R_x)
ValueError: No solutions found.
```

The error comes from line 117, `solve_and_display_(eqs, values, R_angle_deg)`.

(The script's own comments say 87 s, 224 s and 1 min 43 s, run
alone.)

v1-004 (64 lines) prints R_x and R_y by hand, then R_x, R_y, R_mag and
R_angle by eliminating (`Elimination attempts elapsed:` 1.022 s,
0.957 s, 0.965 s, 0.899 s), all with v1-002's formulas and numbers, then
`NameError: name 'R_angle_deg' is not defined` at line 265. v1-005
(66 lines) prints the same four by eliminating (0.996 s, 0.916 s,
0.898 s, 0.940 s) and fails the same way at line 195. Both got every
answer but the degrees; they fail on a script bug, not the solver.

**Techniques.** written out (local `make_force`, `force_equations`,
`polar_to_components`, `components_to_polar`, `superposition_equations`
on the library's `Point3` and `eq_flat`); polar one-way (v1-004 to
v1-007); polar two-way (R only in v1-000 to v1-002, every force in
v1-003); all at once; eliminating (v1-003, v1-004, v1-005); by hand
(v1-000, v1-004, v1-005, v1-006).

**Zeros.** One zero, `F1_angle = sp.rad(0)`, a value in every version;
no zero equations. Port it as `known(F1_angle, 0)` alone, with no
`eliminate_zeros()`: the old formulas keep `cos(F1_angle)` and
`sin(F1_angle)`. (`F2_angle = sp.rad(270)` is `3*pi/2`.)

**Physics code used.** None from `kinematics_states.py` or
`newtons_laws.py` but `Point3` (with `mag` and `angle`). Every version
defines its helpers locally; the local `superposition_equations` is
identical to `newtons_laws.superposition_equations`. The library's
`magnitude_and_angle_equations` writes the same four two-way equations
as v1-003's `force_equations`, but takes a `State` and writes them for
its velocity, so it can't be applied to a force. The library has no
one-way polar helpers.

**Styles worth keeping.**

- v1-007, one-way, all at once: the plain version, as `example_4_1.py`,
  with R_x and R_y added as wants (as v1-001 and v1-002 have them).
- v1-006, one-way, by hand: eliminating the six components between
  displays, as `example_4_1_step_by_step.py`. Already a test.
- v1-002, two-way for R only, all at once, isn't kept: it prints
  v1-007's formulas and numbers, so it shows no contrast. Two-way for
  every force (v1-003) is the contrast that matters, the one that
  fails, and the slow tests keep it.
- Eliminating vs by hand: eliminating on the one-way system (v1-004,
  v1-005) gives the same formulas in about 1 s, so it isn't a contrast
  worth a module; the contrast that matters is v1-003's two-way
  eliminating, which never reaches |R|.

**In equarium.** `tests/test_rewrite.py::test_4_1`: written out by
hand from v1-006, one-way, the six components eliminated, then R_mag
and R_angle_deg, checked against `"128"` and `"141.6"`.
`tests/test_strategies.py::test_4_1_R_x` and `test_4_1_R_y` (slow):
two-way, from v1-003, with `eliminating()`, against the old numbers
`"-100.45"` and `"79.66"`.

**Notes.**

- **The book's angle is 141°; the old scripts print 141.586°,** which
  rounds to 142°. The book rounds first: F3's components to -150 N and
  200 N, so R = (-100 N, 80 N), arctan(-0.80) = -39°, then
  -39° + 180° = 141°. With unrounded components the angle is 141.59°.
  An `Answer(sol, R_angle_deg, "141")` fails (±0.5).
  `tests/test_rewrite.py` checks `"141.6"`, the old number, not the
  book's. The other three match the book within half a unit: -100.45
  against -100, 79.66 against 80, 128.20 against 128.
- **v1-003's two-way failure** is as recorded in 002: R_x and R_y come
  out by eliminating, |R| and the angle only as `sqrt(R_x**2 + R_y**2)`
  and `atan2(R_y, R_x)`, and the degrees raise. On equarium, two-way
  with `eliminating()`: R_x 91 s, R_y 223 s, |R| not finished in 20
  minutes.
- **The 128 N and 141.6° come not only from v1-006 and v1-007** but
  also from v1-000 to v1-002, where R alone is two-way and the forces
  one-way. Two-way polar is slow or fails only when every force has
  both directions (v1-003).
- **Only v1-000 to v1-005 solve for R_x and R_y;** the two `-ok`
  versions don't.
- **v1-004's and v1-005's comments** (timings of 87 s and 224 s, five
  solutions for R_x) were copied from the two-way runs; their own
  one-way runs take about 1 s per want with one solution.
- **A scratch try on equarium** (2026-11-08, nothing in equarium
  changed): the default `solve()` gives all four wants with the old
  formulas exactly, in 1.2 s for v1-007's one-way system and 2.5 s for
  v1-002's (R two-way). `eliminating()` on the one-way system takes
  1.2 s too.
- **Edition:** the 15th edition's Example 4.1 has the same givens
  (50 N, 120 N, 250 N, 53°).

## Example 4.4: Newton's second law I: Determining acceleration from force

PDF page 141. Old folder: `examples/up/ch4/up-example-4.4/`.

**Problem.** A worker pushes a 40 kg box horizontally with a constant
20 N force across a level floor with negligible friction. What is the
box's acceleration?

**Book's answers.** Page 141.

| Part | Quantity | Printed |
|---|---|---|
| — | a_x | 0.50 m/s² |

**Old scripts.**

| Script | Style | Role | Runs | Time |
|---|---|---|---|---|
| `up-example-4.4-000.py` | written out (local copy of `newtons_second_law`), zero values, all at once | latest | yes | 3 s |

`up-example-4.4-000.py` (9 lines printed):

```
a_x = (F_x + n_x + w_x)/m
a_x = 0.500000000000000
```

**Techniques.** written out (local `make_force`, `make_point` and
`newtons_second_law`, a copy of the library's); zero values; all at
once.

**Zeros.** F_y, a_y, n_x and w_x are values, set to 0. No zero
equations. The script calls `eliminate_zero_eqs(eqs)`, but that only
looks for equations `Eq(x, 0)`, so it changes nothing: the displays
before and after are identical, and the formula keeps n_x and w_x. Port
them as `known(sym, 0)` alone. Don't translate the
`eliminate_zero_eqs` call into `eliminate_zeros()`, which would
substitute the zero knowns and give `F_x/m` instead of the old formula.

**Physics code used.** None from the library but `Point3` and `eq_flat`.
The local `newtons_second_law` is identical to
`newtons_laws.newtons_second_law`; the local `force_equations`,
`polar_to_components`, `components_to_polar` and
`superposition_equations` are defined but unused.

**Styles worth keeping.** One script, one style: `example_4_4.py`.

**In equarium.** Nothing.

**Notes.**

- `newtons_second_law` writes `F_x + n_x + w_x = a_x*m`, the sum on the
  left.
- The script was in 4.1's folder until commit `6ec681d` moved it.
- A scratch try on equarium: the default `solve()` gives
  `(F_x + n_x + w_x)/m` = 0.5.
- **Edition:** same givens (20 N, 40 kg) in the 15th edition.

## Example 4.5: Newton's second law II: Determining force from acceleration

PDF page 141, continuing onto 142, where the answers are. Old folder:
`examples/up/ch4/up-example-4.5/`.

**Problem.** A 0.45 kg ketchup bottle is pushed along a level counter.
It leaves the hand at 2.0 m/s and slides 1.0 m before stopping, slowed
by a constant horizontal friction force. What are the friction force's
magnitude and direction?

**Book's answers.** Page 142.

| Part | Quantity | Printed |
|---|---|---|
| — | a_x (intermediate) | -2.0 m/s² |
| — | ΣF_x = -f | -0.90 N |
| — | f, the friction's magnitude | 0.90 N, opposite the velocity (toward -x) |

**Old scripts.**

| Script | Style | Role | Runs | Time |
|---|---|---|---|---|
| `up-example-4.5-000-two-steps.py` | physics code, zero values, all at once, two steps (the second never solved) | alternative (two steps) | yes, but stops before step 2's solve | 3 s |
| `up-example-4.5-001-one-step.py` | physics code, links, zero values, all at once, one step | latest | yes | 3 s |
| `up-example-4.5-002-peter-mechanics.py` | `sympy.physics.mechanics`, Kane's method | other library | yes, no number | 3 s |

How they differ: **001 vs 000** imports `newtons_laws` instead of
000's local copies, adds the Newton equations and the link
`a_x = a_x_b_0_1` to the kinematics system, and solves that one system
for f_x; it drops 000's separate solve for `a_x_b_0_1` and its
commented-out by-hand eliminations (dt, b1.t, v_av). **002** shares
only the comment header.

000 (9 lines printed). Step 1:

```
a_x_b_0_1 = (b_0_v_x - b_1_v_x)*(b_0_v_x + b_1_v_x)/(2*(b_0_x - b_1_x))
a_x_b_0_1 = -2.00000000000000
```

Step 2 builds `newtons_second_law([n, w, f], m, a)`, sets n_x = 0,
w_x = 0 and m = 0.45, displays the two equations and ends. It never
feeds a_x in and never solves for f_x:

```
f_x + n_x + w_x = a_x*m
f_y + n_y + w_y = a_y*m
```

001 (14 lines printed):

```
f_x = (b_0_v_x**2*m/2 - b_0_x*n_x - b_0_x*w_x - b_1_v_x**2*m/2 + b_1_x*n_x + b_1_x*w_x)/(b_0_x - b_1_x)
f_x = -0.900000000000000
```

002 (6 lines printed) models the friction as `-mu*m*g` along N.x and
prints, pretty-printed, the mass matrix `[[1, 0], [0, m]]` and the
forcing vector `[ux(t), -g*m*mu]`. No values, no answer. A trailing
comment holds a hand-derived `f_x = -b_0_v_x**2*m/(2*b_1_x)`.

**Techniques.** physics code; links (001: `a_x = a_x_b_0_1`); zero
values; all at once; two steps (000, unfinished) and one step (001).

**Zeros.** b_0_t = 0, b_0_x = 0, b_1_v_x = 0.0, n_x = 0 and w_x = 0,
all values; no zero equations (000 has a commented-out `eq_flat(b0.t,
0, b0.pos.x, 0)`). Port them as `known(sym, 0)` alone and never call
`eliminate_zeros()`: that keeps the book's general formula
`a = (v**2 - v0**2)/(2*(x - x0))`, as the spec says. (b_1_v_x is the
float `0.0`, which `eliminate_zeros()` would also count as zero.)

**Physics code used.** 001: `make_states_model('b', 2)`,
`kinematics_fundamental(b, axes=['x'])` and `make_point` from
`kinematics_states`, and `newtons_laws.newtons_second_law`. 000: the
same kinematics functions, with local copies of `make_point` and
`newtons_second_law` (and an unused `superposition_equations`); it
imports `magnitude_and_angle_equations` and `State` but doesn't use
them. The link `a_x = a_x_b_0_1` is written by hand with `eq_flat`.

**Styles worth keeping.** Both, as the two-steps/one-step contrast:
001 as `example_4_5.py` (physics code, one system, all at once), and
000 as `example_4_5_two_steps.py`, finished: step 2 takes step 1's
a_x as a known and solves for f_x. 002 isn't ported (other library).

**In equarium.** Nothing.

**Notes.**

- **The script's want is f_x, the friction's x-component,** -0.90 N:
  the book's ΣF_x = -f. The book's f = 0.90 N is the magnitude, which
  the script leaves to the reader (the sign gives the direction). The
  old charter's "friction -0.90 N" is this component.
- **000's "two steps" never does its second step.** Its second system
  doesn't receive a_x, and the script ends at a display.
- `newtons_laws.py` uses `sp.Symbol` in an annotation without importing
  sympy. It imports only because the old venv is Python 3.14, which
  evaluates annotations lazily.
- A scratch try on equarium: one system gives 001's f_x formula
  exactly, -0.9, in 0.2 s. Step 1 gives 000's a_x formula, -2.0, and
  step 2 with a_x known gives `f_x = a_x*m - n_x - w_x` = -0.9.
- **Edition:** same givens (0.45 kg, 2.0 m/s, 1.0 m) in the 15th
  edition.

## Example 4.7: Mass and weight

PDF page 145. Old folder: `examples/up/ch4/up-example-4.7/`.

**Problem.** A truck weighing 2.45 × 10⁴ N, moving in the +x
direction, brakes hard; the x-component of the net external force on
it is -1.83 × 10⁴ N. What is its acceleration? (The book first finds
the mass from the weight.)

**Book's answers.** Page 145.

| Part | Quantity | Printed |
|---|---|---|
| — | m (intermediate) | 2540 kg |
| — | a_x | -7.20 m/s² |

**Old scripts.**

| Script | Style | Role | Runs | Time |
|---|---|---|---|---|
| `up-example-4.7-000.py` | written out, units, all at once | latest | yes | 2 s |

`up-example-4.7-000.py` (5 lines printed):

```
a_x = F_x*g/w
a_x = -7.3274693877551*meter/second**2
```

**Techniques.** written out (`w = m*g`, `F_x = m*a_x`); units
(`sympy.physics.units`: newton, meter, second); all at once.

**Zeros.** None.

**Physics code used.** None. It imports `kinematics_states`,
`solve_system` and `newtons_laws` with `*` but uses only `eq_flat`;
`meters` is imported and unused.

**Styles worth keeping.** One script: `example_4_7.py`.

**In equarium.** Nothing.

**Notes.**

- **The book contradicts itself.** The statement gives
  2.45 × 10⁴ N, the SET UP calls the weight 2.49 × 10⁴ N, and the
  EXECUTE writes (2.45 × 10⁴ N)/(9.80 m/s²) = 2540 kg, which is
  2.49 × 10⁴ N's mass; 2.45 × 10⁴ N gives 2500 kg. The printed 2540 kg
  and -7.20 m/s² follow from 2.49 × 10⁴ N. Checked on the rendered
  page, not only in the text extraction.
- **The old output, -7.33 m/s², isn't the book's -7.20 m/s²:** the
  script uses the statement's 2.45 × 10⁴ N (giving -7.32) and
  g = 9.81 m/s² instead of the book's 9.80 (giving -7.327).
- The script never solves for the mass.
- A scratch try on equarium, with units, `a_x = F_x*g/w` and
  `m = w/g`: -7.3275 m/s² and 2497.5 kg with the old g = 9.81 m/s²;
  -7.32 m/s² and 2500 kg with the book's g = 9.80 m/s²; -7.2024 m/s²
  and 2540.8 kg with w = 2.49 × 10⁴ N and g = 9.80 m/s².
- **Edition:** the script's givens match the 15th edition's statement;
  the mismatch is inside the book (above). Whether an earlier edition
  had 2.49 × 10⁴ N in the statement wasn't checked.

## kinematic-equations

Old folder: `examples/up/ch2/kinematic-equations/`, six scripts and a
notebook. They derive the book's constant-acceleration equations from
three the code calls `eq_2_2`, `eq_2_7` and `eq_2_10`: the definitions
of average velocity (the book's 2.2) and average acceleration (2.7,
here over an interval `dt`), and average velocity as the mean of the
end velocities (2.10, true for constant acceleration). In 003, 004
and 005:

```python
eq_2_2 = sp.Eq(v_av_x, (x_2 - x_1) / dt)
eq_2_7 = sp.Eq(a_x, (v_2x - v_1x) / dt)
eq_2_10 = sp.Eq(v_av_x, (v_1x + v_2x) / 2)
```

000, 001 and 002-dt write `t_2 - t_1` where the later ones write `dt`.

**The book's equations,** Table 2.5 on PDF page 77, and the form the
scripts reach them in:

| Book | Equation | As derived (003, the notebook, 004's tail) |
|---|---|---|
| 2.8 | vx = v0x + ax·t | `v_2x = a_x*dt + v_1x` |
| 2.12 | x = x0 + v0x·t + ½·ax·t² | `x_2 = a_x*dt**2/2 + dt*v_1x + x_1` |
| 2.13 | vx² = v0x² + 2·ax·(x - x0) | `2*a_x*(-x_1 + x_2) + v_1x**2 = v_2x**2` |
| 2.14 | x - x0 = ½·(v0x + vx)·t | `-x_1 + x_2 = dt*(v_1x + v_2x)/2` |

**The scripts.**

| Script | What it derives | Techniques | Role | Runs | Time |
|---|---|---|---|---|---|
| `kinematics-equations-000.py` | A REPL session pasted into a file: substitutions between pairs of the three, `t_2 - t_1` as one unit. Its comments record 2.13 solved for `a_x`. | written out, by hand (a local `solve_subs`) | draft (of 001) | fails: `NameError: display_equation_` at line 91, before printing anything (the import is at line 113) | 2 s |
| `kinematics-equations-001.py` | Five substitutions, then 2.12 isolated, in `t_1` and `t_2`: `x_2 = a_x*t_1**2/2 - a_x*t_1*t_2 + a_x*t_2**2/2 - t_1*v_1x + t_2*v_1x + x_1`, per its comments. | written out, by hand, isolate (local) | draft (of 002-dt) | fails: the same `NameError` at line 60, before printing anything | 2 s |
| `kinematics-equations-002-dt.py` | 001 with `dt` for `t_2 - t_1`. Reaches 2.12 as `x_2 = a_x*dt**2/2 + dt*v_1x + x_1`, per its comments. | written out, by hand, isolate (local) | draft (of 003) | fails: the same `NameError` at line 69, before printing anything | 2 s |
| `kinematics-equations-003-book-equations.py` | The four book equations, each by a short chain of substitutions and both-sides steps. | written out, by hand, both sides, isolate (local) | latest (by hand) | yes | 2 s |
| `kinematics-equations-004-every-possible-eq.py` | A blind search over every pair and every shared symbol, to depth 3, then 003's four derivations. | derive all, both sides, isolate (local) | draft (of 005, for the search; its derivations are 003's) | doesn't finish at depth 3 (see below); a copy at depth 2 runs | 128 s at depth 2 |
| `kinematics-equations-005-eq-history.py` | The search again, with each equation's history, pruned by it: 14 equations in all. | derive all | latest (derive all) | yes | 16 s |
| `kinematics-equations-book-equations.ipynb` | 003's four derivations, one per cell, each with a comment naming the book's equation. | written out, by hand, both sides, isolate (local) | duplicate (of 003, as a notebook) | yes (its cells, run in order through the shim) | 2 s |
| `.ipynb_checkpoints/kinematics-equations-book-equations-checkpoint.ipynb` | Jupyter's autosave of the notebook. | | duplicate (byte for byte, of the notebook) | not run | |

**000, 001 and 002-dt** are interactive sessions saved as files: the
statements are in the order they were typed, and `display_equation_`
is used before the line that imports it. They print nothing but the
traceback (11 lines each). What they reached is in their comments,
which hold the session's output. Nothing in them is lost: 003 reaches
the same equations.

**003** (5 lines, all of it):

```
v_av_x = a_x*(-x_1 + x_2)/(-v_1x + v_2x)
-x_1 + x_2 = dt*(v_1x + v_2x)/2
v_2x = a_x*dt + v_1x
2*a_x*(-x_1 + x_2) + v_1x**2 = v_2x**2
x_2 = a_x*dt**2/2 + dt*v_1x + x_1
```

The first line is `eq_2_2` with `dt` eliminated through `eq_2_7`, the
derivation equarium already has. The other four are 2.14, 2.8, 2.13
and 2.12. How each is reached:

- 2.14: `eq_2_10` substituted into `eq_2_2` for `v_av_x`, both sides
  times `dt`, simplified, both sides times -1.
- 2.8: `eq_2_7` isolated for `v_2x`.
- 2.13: `eq_2_7` into `eq_2_2` for `dt`, then `eq_2_10` for `v_av_x`,
  both sides times `(-v_1x + v_2x)` and times 2, simplified, then
  `v_1x**2` added to both sides.
- 2.12: `eq_2_10` into `eq_2_2` for `v_av_x`, then `eq_2_7` for `v_2x`,
  then isolated for `x_2`.

**The notebook** prints, cell by cell (each cell's last value):

```
[cell 5] Eq(v_av-x, a_x*(-x_1 + x_2)/(-v_1x + v_2x))
[cell 6] Eq(-x_1 + x_2, dt*(v_1x + v_2x)/2)
[cell 7] Eq(v_2x, a_x*dt + v_1x)
[cell 8] Eq(2*a_x*(-x_1 + x_2) + v_1x**2, v_2x**2)
[cell 9] Eq(x_2, a_x*dt**2/2 + dt*v_1x + x_1)
```

The same five as 003, and the same as the outputs saved in the
notebook. Its comments name them: "eq 2.14", "equation 2.8", "eq
2.13", "eq 2.12". Its average-velocity symbol is `v_av-x`, with a
hyphen. A notebook can't be run with `runpy`, so a scratch runner ran
its code cells in order, through the shim, printing each cell's last
expression as Jupyter does.

**004** first runs the search, `derive_all_equations([eq_2_2, eq_2_7,
eq_2_10], max_depth=3)` at line 151. For every ordered pair of
equations and every symbol they share, it solves one for the symbol,
substitutes into the other, simplifies, and keeps the result unless it
is equivalent (`sp.simplify` of the difference is 0) to one already
found. It doesn't prune by where an equation came from, so the pairs
grow with the square of the set. The survey earlier on 2026-11-08
found 8 new equations at depth 1 and 196 at depth 2 within 150 s, and
depth 3 unfinished after 20 minutes, so the four derivations after
the search never print. Following the checkpoint, a copy in the
scratchpad set `max_depth=2` on line 151 and ran through the shim from
the old repo's root: 128 s, 15 lines.

```
Solving for dt
Solving for v_1x
Solving for v_av_x
Solving for v_2x
v_av_x = a_x*(-x_1 + x_2)/(-v_1x + v_2x)
v_av_x = a_x*(-x_1 + x_2)/(2*v_2x - 2*v_av_x)
v_1x/2 + v_2x/2 = a_x*(-x_1 + x_2)/(-v_1x + v_2x)
v_av_x = a_x*(-x_1 + x_2)/(-2*v_1x + 2*v_av_x)
Depth 1: Found 8 new equations
Depth 2: Found 196 new equations
```

then 003's five lines, ending with `x_2 = a_x*dt**2/2 + dt*v_1x + x_1`.
The "Solving for" lines come in set order, which can change between
runs. The search returns its equations without printing them. Its
counts are of the round's list, which isn't checked against itself, so
196 may count one equation more than once.

**005** gives each equation a history, `EquationWithHistory`: its
parents, the symbol eliminated, and every ancestor. Two equations are
combined only if neither is an ancestor of the other, they aren't
siblings, and they share no ancestor. That pruning ends the search: 4
equations at depth 1, 10 at depth 2, none at depth 3, 17 in all with
the three it starts from, in 16 s (150 lines). Each derived equation
prints with its history as it is found:

```
Starting with 3 fundamental equations

  Derived: eq_2.2 + eq_2.7 (eliminate dt)
v_av_x = a_x*(x_1 - x_2)/(v_1x - v_2x)

  Derived: eq_2.2 + eq_2.10 (eliminate v_av_x)
v_1x/2 + v_2x/2 = (-x_1 + x_2)/dt
```

```
  Derived: eq_2.2 + [eq_2.7 + eq_2.10 (eliminate v_2x)] (eliminate v_av_x)
a_x*dt/2 + v_1x = (-x_1 + x_2)/dt
```

```
Depth 1: Tried 4 combinations, skipped 0, found 4 new equations
Depth 2: Tried 14 combinations, skipped 14, found 10 new equations
Depth 3: Tried 14 combinations, skipped 129, found 0 new equations
No new equations found. Stopping.
Total equations: 17 (3 fundamental + 14 derived)
```

Then every equation with its one-line history, and the full tree:

```
#11 = eq_2.2 + #6 (eliminate v_av_x)
  #6 = eq_2.7 + eq_2.10 (eliminate v_2x)
```

Of the book's equations, 005 reaches 2.14 (`v_1x/2 + v_2x/2 =
(-x_1 + x_2)/dt`), 2.12 twice (`a_x*dt/2 + v_1x = (-x_1 + x_2)/dt`, and
`a_x = 2*(-dt*v_1x - x_1 + x_2)/dt**2`) and 2.13 (`a_x = (v_1x -
v_2x)*(v_1x + v_2x)/(2*(x_1 - x_2))`), each in a form it doesn't
rearrange. 2.8 is `eq_2_7` itself, rearranged. Some of the 14 are
degenerate: the three from `eq_2.10 + #3` put a symbol on both sides
(`v_1x = a_x*x_1/v_av_x - a_x*x_2/v_av_x - v_1x + 2*v_av_x`). Its
`EquationWithHistory` simplifies every equation it stores, so even the
fundamental `eq_2.10` prints as `v_1x = -v_2x + 2*v_av_x`.

**misc.py's helpers.** misc's own `isolate_variable` isn't used here:
001, 002-dt, 003, 004 and the notebook define a local one that refuses
more than one root (misc's takes the first). The both-sides helpers:

| Script | Imports from misc | Uses |
|---|---|---|
| 003 | `multiply_both_sides`, `add_both_sides` | both |
| 004 | `multiply_both_sides`, `divide_both_sides`, `expand_lhs`, `expand_rhs`, `add_both_sides` | `multiply_both_sides`, `add_both_sides` |
| the notebook | the same five as 004 | `multiply_both_sides`, `add_both_sides` |
| 000, 001, 002-dt, 005 | none | |

So `divide_both_sides`, `expand_lhs` and `expand_rhs` are imported but
never called anywhere in `examples/up/`. The scripts' own helpers:
`solve_subs(eq_a, eq_b, var)` (solve `eq_b` for `var`, one root only,
substitute into `eq_a`) and `symbols_in_common` in every script;
`isolate_variable` from 001 on; `derive_all_equations` and
`is_equivalent_to_any` in 004; `EquationWithHistory`,
`is_algebraically_equivalent`, `is_duplicate` and its own
`derive_all_equations` in 005.

**In equarium.** `tests/kinematics_005.py` and `tests/test_rewrite.py`:
005's first derivation only, `eq_2.2 + eq_2.7 (eliminate dt)`, through
`eliminate` and the origin tree.

**Notes.** The book's 2.9 is 2.2 with the interval starting at
t = 0, and page 77 gets 2.14 by setting 2.9 equal to 2.10. The scripts
keep the interval general (`dt`, and `x_1`, `v_1x` for the start).
The checkpoint says the eight scripts that fail print some output
first: these three print none.

## Other files

- **The 11 PNG images,** figures from the book saved beside the
  scripts, 0.5 to 1 MB each: `up-example-2.6.png`, `up-example-2.7.png`,
  `up-example-3.6.png`, `up-example-3.7.png`, `up-example-3.8.png`,
  `up-example-3.9.png`, `up-example-3.10.png`, `up-example-4.1.png`,
  `up-example-4.4.png`, `up-example-4.5.png` and `up-example-4.7.png`.
  They are the publisher's figures, so they are never copied into
  equarium. An example module names the figure in its docstring
  instead.
- **The notebook's `.ipynb_checkpoints` copy** is Jupyter's autosave,
  byte for byte the notebook (see kinematic-equations).
- **`examples/eq-gui/`** is out of scope, with the GUI.
- **The old repo's three tests,** `unittest` classes that rebuild the
  example's system with their own copies of `eq_flat` (and, for 3.6,
  `eliminate_zero_eqs`). Run on 2026-11-08 with
  `uv run --frozen python -m unittest discover -s tests`: 7 tests, OK,
  in 22 s. Each pins numbers to 9 places:
  - `test_up_example_3_6.py` (3 tests, g = 9.8): x 4.5, y -1.225;
    `dist` 4.66375653309647; `vel_mag` 10.2474387043788, `vel_angle`
    -0.498567905638218, `vel_angle_deg` -28.5658367937466.
  - `test_up_example_3_7.py` (3 tests, g = 9.81): at 2.00 s, x
    44.4310966741154, y 39.5566647280447, v_x 22.2155483370577, v_y
    9.96833236402235, speed 24.3495018026193, angle 0.421780406158419
    and 24.1662371541911°; at the top, t 3.01613989439575 and height
    44.6212748258844; at landing, x 134.010403230554, v_x
    22.2155483370577, v_y -29.5883323640224.
  - `test_up_example_3_9_v2.py` (1 test, g = 9.81): exactly two roots
    for x, through `solve_with_elimination_attempts`, -15.7161745661753
    and 9.16380341748480.

  The 3.7 and 3.9 numbers are at g = 9.81. Ports that use the book's
  9.80 (question 1) keep the formulas these tests imply, not their
  numbers.

## Recommendations for 007

### The port list

29 modules under `examples/up_15e/`: the three that exist and 26 new
ones, `table_2_5.py` among them. Symbols are written as the old scripts write them, through
the physics code's objects (`m1.pos.x` prints as `m_1_x`). Each
module's formulas must be the ones its entry quotes for the old script,
verbatim, except where the next section says otherwise.

**Chapter 2, `ch02/`:**

| Module | From | `BOOK` |
|---|---|---|
| `example_2_4.py` | 2.4 v4-001 | `Answer(sol_a, m1.pos.x, "43"),  # m`<br>`Answer(sol_a, m1.vel.x, "23"),  # m/s`<br>`Answer(sol_b, m1.pos.x, "55"),  # m` |
| `example_2_4_handwritten.py` | exists (v3-001) | |
| `example_2_5.py` | 2.5 v4-000 | `Answer(sol, t_01, "10"),  # s`<br>`Answer(sol, p1.vel.x, "30"),  # m/s`<br>`Answer(sol, dist, "150"),  # m` |
| `example_2_5_step_by_step.py` | 2.5 v4-002 | the same three |
| `example_2_5_handwritten.py`, `example_2_5_handwritten_step_by_step.py` | exist (v3-002, v3-001) | |
| `example_2_6.py` | 2.6 v2-000 | `Answer(sol_1, c1.pos.y, "-4.9"),  # m`<br>`Answer(sol_1, c1.vel.y, "-9.8"),  # m/s`<br>`Answer(sol_2, c1.pos.y, "-20"),  # m`<br>`Answer(sol_2, c1.vel.y, "-20"),  # m/s`<br>`Answer(sol_3, c1.pos.y, "-44"),  # m`<br>`Answer(sol_3, c1.vel.y, "-29"),  # m/s` |
| `example_2_7.py` | 2.7 v1-000 | `Answer(sol_a1, b1.pos.y, "10.1"),  # m`<br>`Answer(sol_a1, b1.vel.y, "5.2"),  # m/s`<br>`Answer(sol_a4, b1.pos.y, "-18.4"),  # m`<br>`Answer(sol_a4, b1.vel.y, "-24.2"),  # m/s`<br>`Answer(sol_b, b1.vel.y, "-11.3", "11.3"),  # m/s`<br>`Answer(sol_c, b1.pos.y, "11.5"),  # m` |
| `example_2_8.py` | 2.7 v1-000's last part, importing 2.7's base | `Answer(sol, b1.t, "-0.30", "3.36"),  # s, both roots`<br>`Answer(sol.where(b1.t > 0), b1.t, "3.36"),  # s` |
| `exercise_2_1.py` | 2.1 000 | `Answer(sol, c1.pos.x, "25.0", unit=meter),` |
| `exercise_2_3.py` | 2.3 002 | `Answer(sol.in_units(minute), longer, "55", unit=minute),` |
| `exercise_2_3_two_steps.py` | 2.3 000 | `Answer(slow.in_units(minute), longer, "55", unit=minute),` |
| `exercise_2_5.py` | 2.5 001 | `Answer(sol, avg_vel_02, "0.313", unit=meter/second),`<br>`Answer(sol, avg_speed_02, "1.56", unit=meter/second),` |
| `exercise_2_19.py` | 2.19 000 | `Answer(sol_a, o0.vel.x, "8.33", unit=meter/second),`<br>`Answer(sol_b, o01.a.x, "1.11", unit=meter/second**2),` |
| `exercise_2_21.py` | 2.21 000, without the GUI | `Answer(sol_a, b01.a.x, "675", unit=meter/second**2),`<br>`Answer(sol_b, b01.dt, "0.0667", unit=second),` |
| `exercise_2_23.py` | 2.23 000 | `Answer(sol.in_units(meter, second), b1.pos.x, "1.70", unit=meter),` |
| `table_2_5.py` (question 5) | kinematic-equations 003 | none: not an example or exercise, so `tests/test_examples.py` doesn't collect it. A test compares its five equations with 003's output. |

**Chapter 3, `ch03/`,** with g = 9.80 (question 1):

| Module | From | `BOOK` |
|---|---|---|
| `example_3_6.py` | 3.6 v1-000 | `Answer(sol, m1.pos.x, "4.5"),  # m`<br>`Answer(sol, m1.pos.y, "-1.2"),  # m`<br>`Answer(sol, dist, "4.7"),  # m`<br>`Answer(sol, m1.vel.y, "-4.9"),  # m/s, a new want`<br>`Answer(sol, vel_mag, "10.2"),  # m/s`<br>`Answer(sol, vel_angle_deg, "-29"),  # degrees` |
| `example_3_7.py` | 3.7 v1-000 | `Answer(sol_a, b1.pos.x, "44.4"),  # m`<br>`Answer(sol_a, b1.pos.y, "39.6"),  # m`<br>`Answer(sol_a, b1.vel.x, "22.2"),  # m/s`<br>`Answer(sol_a, b1.vel.y, "10.0"),  # m/s`<br>`Answer(sol_a, b1_vel_mag, "24.4"),  # m/s`<br>`Answer(sol_a, b1_vel_angle_deg, "24.2"),  # degrees`<br>`Answer(sol_b, b1.t, "3.02"),  # s`<br>`Answer(sol_b, b1.pos.y, "44.7"),  # m`<br>`Answer(sol_c, b1.t, "6.04"),  # s, a new want`<br>`Answer(sol_c, b1.pos.x, "134"),  # m`<br>`Answer(sol_c, b1.vel.y, "-29.6"),  # m/s`<br>`Answer(sol_c, b1_vel_angle_deg, "-53.1"),  # degrees, a new want` |
| `example_3_8.py` | 3.8 v1-000, its bug fixed | `Formula`s (question 2): t1, h, t2 and R as the book prints them, in the script's symbols:<br>`Formula(sol_top, p1.t, "p_0_v_mag*sin(p_0_v_angle)/g"),`<br>`Formula(sol_top, p1.pos.y, "p_0_v_mag**2*sin(p_0_v_angle)**2/(2*g)"),`<br>`Formula(sol_range, p1.t, "2*p_0_v_mag*sin(p_0_v_angle)/g"),`<br>`Formula(sol_range, p1.pos.x, "p_0_v_mag**2*sin(2*p_0_v_angle)/g"),` |
| `example_3_9.py` | 3.9 v2 | `Answer(sol.where(b1.pos.x > 0), b1.pos.x, "9.2"),  # m`<br>`Answer(sol_t, b1.t, "-1.7", "0.98"),  # s, a new want` |
| `example_3_10.py` | 3.10 v1-001 | a `Formula` (question 2) for the book's time, a new want:<br>`Formula(sol_t, d1.t, "D/(d_0_v_mag*cos(d_0_v_angle))"),`<br>The show-that itself stays a check of what is left, as in `tests/test_rewrite.py`. |
| `example_3_13.py` | 3.13 001-eq | `Answer(sol, v_TY, "-192", unit=kilometer/hour),`<br>`Answer(sol, v_YT, "192", unit=kilometer/hour),` |

**Chapter 4, `ch04/`:**

| Module | From | `BOOK` |
|---|---|---|
| `example_4_1.py` | 4.1 v1-007 | `Answer(sol, R_x, "-100"),  # N, a new want`<br>`Answer(sol, R_y, "80"),  # N, a new want`<br>`Answer(sol, R_mag, "128"),  # N`<br>`Answer(sol_book, R_angle_deg, "141"),  # degrees (question 3)` |
| `example_4_1_step_by_step.py` | 4.1 v1-006 | the same four |
| `example_4_4.py` | 4.4 000 | `Answer(sol, a_x, "0.50"),  # m/s²` |
| `example_4_5.py` | 4.5 001 | `Answer(sol, f_x, "-0.90"),  # N, the book's ΣF_x = -f` |
| `example_4_5_two_steps.py` | 4.5 000, its second step finished | `Answer(sol_1, b01.a.x, "-2.0"),  # m/s²`<br>`Answer(sol_2, f_x, "-0.90"),  # N` |
| `example_4_7.py` | 4.7 000 (question 4) | `Answer(sol.in_units(meter, second), a_x, "-7.20", unit=meter/second**2),`<br>`Answer(sol.in_units(kilogram), m, "2.54e3", unit=kilogram),  # the book's 2540 kg` |

Every number in these lines was checked against the old output, or the
port's stated change, within `Answer`'s half unit. The tight ones:
Exercise 2.5's 0.3125 against "0.313" sits exactly on the boundary,
which `Answer` includes (`tests/test_examples.py` tests that the
boundary is inclusive); 2.8's 3.3645 against "3.36" is 0.0045 off;
4.1's R_x, -100.45 against "-100", is 0.45 off.

### Where the port differs from the old script

The `BOOK` holds the book's answer, and the old formulas are still
compared as they are. Where a port adds a step, a want or a given,
007's checkpoint should list it as an expected difference, so the
comparison with the old script doesn't stop on it.

- **Exercise 2.3,** both modules: `Eq(longer, cb1.t - ca1.t)` added, to
  reach 55 min, as `tests/test_units.py` does.
- **Exercise 2.23:** `in_units(meter, second)` at the end, as the test
  does.
- **Example 2.6:** `c1.vel.y` added as a want at 2.0 s and 3.0 s.
- **Example 2.7 (d):** the acceleration is a known, so it stays a
  comment.
- **Example 2.8:** `where(b1.t > 0)` added, the book's choice of root.
- **Example 3.6:** `m1.vel.y` added as a want. The book's v_x = 9.0 m/s
  is a given in the script, so it has no `Answer`.
- **Example 3.7:** g = 9.80, not 9.81 (with 9.81 the speed and h miss).
  (c)'s time and landing angle added as wants.
- **Example 3.8:** the range solved from the range system, fixing line
  145, so its formula is the book's `.../g`, not the old `.../(2*g)`.
  The 90° and 45° need a maximization the old code never had: a
  comment, not a port.
- **Example 3.9:** g = 9.80 (9.81 also matches 9.2), the filter
  `x > 0`, and the time added as a want, if `eliminating()` finds it in
  about the same time as x. If it doesn't, the time line goes.
- **Example 4.1:** R_x and R_y added as wants (v1-007 and v1-006 don't
  have them), and the angle per question 3.
- **Example 4.4:** the old `eliminate_zero_eqs` call is a no-op (the
  zeros are values), so it becomes nothing, not `eliminate_zeros()`.
- **Example 4.5, two steps:** step 2 takes step 1's `a_x` as a known
  and solves for `f_x`, which 000 never did. It has no old formula;
  equarium gives `f_x = a_x*m - n_x - w_x`.
- **Example 4.7:** the weight and g per question 4, and the mass added
  as a want.

### The slugs

- `_handwritten`: the equations written out, where a physics-code
  version of the same problem exists (2.4, 2.5).
- `_step_by_step`: eliminating by hand between displays (2.5 v4-002,
  4.1 v1-006; 2.5 v3-001 combines it with `_handwritten`).
- `_two_steps`: the first answer fed into a second system (Exercise 2.3
  000, Example 4.5 000).

No other slug. The default applies everywhere: the main version, solved
all at once in one system, has none. So the one-step Exercise 2.3 is
`exercise_2_3.py`, not the spec's suggested `exercise_2_3_one_step.py`
(question 6). Problems with one kept version have no slug, even when
it is written out (3.13, 4.4, 4.7) or by hand (3.10): there is nothing
to contrast it with. A `_two_way` slug for 4.1 v1-002 was considered
and not recommended (below).

### What isn't ported

| Script | Why |
|---|---|
| 2.4 v4-000 | draft of v4-001, the same output |
| 2.6 v1-000 | draft of v2-000, downward positive, so the book's signs flip |
| Exercise 2.3 001 | draft of 002 |
| Exercise 2.5 000 | draft of 001: its eliminations are only displayed |
| Exercise 2.21 001-gui | GUI only |
| kinematic-equations 000, 001, 002-dt | REPL drafts that fail before printing; 003 reaches the same equations |
| kinematic-equations 004 | draft of 005 for the search, of 003 for the derivations |
| kinematic-equations 005 | the derive-all search (below) |
| the notebook and its checkpoint copy | duplicates of 003 |
| 3.9 v1-000 | draft; fails at its first solve, and v2 replaced it. Its lesson, that all at once finds nothing on two-way polar, is `tests/test_strategies.py`'s. |
| 3.10 v1-000 | draft; fails at line 121 |
| 3.13 000 | draft in plain SymPy, prints nothing |
| 3.13 `001-eq copy.py` | duplicate |
| 3.13 002 | other library (`sympy.physics.vector`) |
| 4.1 v1-000, v1-001 | drafts of v1-002 |
| 4.1 v1-002 | R two-way, the forces one-way: the same formulas and numbers as v1-007, all at once in 2.5 s on equarium. The two-way lesson is v1-003's, not this one's. |
| 4.1 v1-003 | never reaches \|R\| or the angle, and takes 9 minutes; its lesson is kept by the slow `tests/test_strategies.py` (R_x, R_y) |
| 4.1 v1-004, v1-005 | drafts that fail on a script bug (`R_angle_deg` commented out); eliminating on one-way is about 1 s, which `example_4_1.py`'s all-at-once solve already shows |
| 4.5 002 | other library (`sympy.physics.mechanics`), no number |

None of them teaches something a new test should keep: the two lessons
that matter (all at once fails on two-way polar; eliminating is slow on
it) are already in `tests/test_strategies.py`.

### misc.py's both-sides helpers

Bring over the two that are used, `add_both_sides` and
`multiply_both_sides`, as plain functions on `sp.Eq` in
`equations.py`, as the spec says, for kinematic-equations 003's port,
`table_2_5.py` (question 5: yes). Leave `divide_both_sides`,
`expand_lhs` and `expand_rhs`: nothing in `examples/up/` calls them.

Why: a scratch try on equarium (2026-11-08) shows `eliminate` and
`isolate` reach 2.8 and 2.12 exactly as 003 prints them
(`v_2x = a_x*dt + v_1x`, `x_2 = a_x*dt**2/2 + dt*v_1x + x_1`), but 2.13
and 2.14 only solved for a symbol (`x_2 = (2*a_x*x_1 - v_1x**2 +
v_2x**2)/(2*a_x)`, `x_2 = dt*v_1x/2 + dt*v_2x/2 + x_1`). Isolating
`v_2x` for 2.13 refuses, with two roots. The book's own shapes,
`2*a_x*(-x_1 + x_2) + v_1x**2 = v_2x**2` and
`-x_1 + x_2 = dt*(v_1x + v_2x)/2`, need the both-sides steps. 003 and
the notebook exist to reach those shapes: the notebook names each
"eq 2.14 from the book". So the module derives on a `System` where
`eliminate` and `isolate` reach, and uses the two helpers for the last
steps of 2.13 and 2.14, as 003 does.

### kinematic-equations 005's derive-all search

Not ported in 007. The search is a tool for exploring, not an example:
it has no answer to check, its pruning rules are its own design
(ancestors, siblings, shared ancestors), and three of its 14 equations
are degenerate. What it taught, recording where each equation came
from, is equarium's origin tree, and `tests/kinematics_005.py` already
pins its first derivation and that origin. If the user wants the
search, it belongs to a later series, on top of `System`'s origins
(question 7: left out).

### The physics code

The port list needs, from `kinematics_states.py`: `make_states_model`,
`kinematics_fundamental` (every kinematics port), `make_point` (4.4,
4.5), `Point3` (4.1, 4.4, 4.5) and `magnitude_and_angle_equations`
(3.9, 3.10). From `newtons_laws.py`: `newtons_second_law` (4.4, 4.5)
and `superposition_equations` (4.1; v1-007's local copy is the same
function). `eq_flat` comes from equarium. No kept script calls
`link_same_time`, `link_same_position`, `axis_zero_constraints`,
`axis_zero_substitution_map` or `constant_velocity_constraints`.

`newtons_laws.py` uses `sp.Symbol` in an annotation without importing
SymPy. It imports on Python 3.14 only because annotations are lazy.
The copy needs `import sympy as sp`, which pyright would ask for
anyway.

What the kept examples need that the old physics code doesn't have,
for the physics redesign, not 007:

- **One-way polar helpers for any vector,** in both directions: 4.1's
  local `polar_to_components` and `components_to_polar`, 3.7's launch,
  and 3.6's and 3.7's speed and angle written by hand. The port keeps
  4.1's local helpers in its module, as the old script does.
- **A two-way helper for any `Point3`:** `magnitude_and_angle_equations`
  takes a `State` and writes its velocity's.
- **A position magnitude:** 3.6's distance from the origin. `pos` has
  no `mag` or `angle`.
- **Degrees:** 3.6, 3.7 and 4.1 write `angle*180/pi` or `deg(angle)`.
- **A projectile setup:** 3.7 to 3.10 repeat the same block (zero x0,
  y0, t0 and a_x, `a_y = -g`, `v0x = v1x`).
- **Links through a shared symbol:** 3.10 writes `d1.t = t`,
  `m1.t = t`, `d1.y = y`, `m1.y = y` by hand. `link_same_time` covers
  the first two and was never used; nothing covers the positions.
- **Newton's acceleration as a kinematics edge's:** 4.5 writes
  `Eq(a.x, b01.a.x)` by hand.
- **Weight:** 4.7 writes `w = m*g` by hand.
- **Relative velocity:** 3.13's equations 3.32 and 3.33.
- **Maximizing over a parameter:** 3.8's 90° and 45°.

### 007's size

26 new modules, `table_2_5.py` among them, the physics code's copy,
the two helpers, and a `Formula` in `examples/answers.py`. Too much
for one checkpoint, and most of the questions' changes are in chapters
3 and 4. Split it:

- **007, chapter 2:** copy the physics code, port chapter 2's 13 new
  modules and `table_2_5.py`, and bring over the two helpers
  (questions 5 and 6).
- **008, chapters 3 and 4:** 12 new modules, and `Formula`
  (questions 1 to 4).

Two costs to plan for: `example_3_9.py` runs `eliminating()` on
two-way polar at import, about 6 s, and `tests/test_examples.py`
imports every example, so it either takes the 6 s or marks that module
slow. Every other port should take a second or two.

### Questions for the user

The user answered all seven on 2026-11-08, each as recommended. The
questions stay as they were asked, for the record.

1. **The book's givens over the old scripts'.** 3.7, 3.9 and 4.7 use
   g = 9.81; the book uses 9.80, and 3.7's speed and height miss the
   book's answers with 9.81. Port with the book's 9.80? *Recommended and chosen:
   yes.* The formulas are still compared with the old ones; only the
   numbers change.
2. **Answers that are formulas.** 3.8's answers are formulas (t1, h,
   t2, R), and 3.10's is a "show that". `tests/test_examples.py`
   fails a module whose `BOOK` is empty. Add a `Formula(solution,
   symbol, "printed")` to `examples/answers.py`, matching when the
   difference simplifies to 0, so both can be example modules?
   *Recommended and chosen: yes.* The alternative leaves 3.8 unported and 3.10 a
   test only, as it is in `tests/test_rewrite.py`.
3. **4.1's angle.** The book prints 141°, from its rounded components
   (-100 N, 80 N); unrounded, the angle is 141.59°, which `Answer`
   reads as 142. Add the book's step, the angle from the rounded R_x
   and R_y (141.34°), as a second system? Or leave the angle out of
   `BOOK`? *Recommended and chosen: the book's step,* as Exercise 2.3's port adds
   its step. Note that `tests/test_rewrite.py` checks "141.6", the old
   number, not the book's.
4. **4.7's weight.** The book's statement says 2.45 × 10⁴ N, but its
   solution prints 2540 kg and -7.20 m/s², which follow from
   2.49 × 10⁴ N (its SET UP's number). The old script uses 2.45 × 10⁴ N
   and g = 9.81, and prints -7.33 m/s². Port with 2.49 × 10⁴ N and
   g = 9.80, with a comment on the book's inconsistency, and the mass
   written "2.54e3", the book's three significant figures (±5 kg)?
   *Recommended and chosen: yes.*
5. **Table 2.5.** Port kinematic-equations 003 as
   `examples/up_15e/ch02/table_2_5.py`, with `add_both_sides` and
   `multiply_both_sides` in `equations.py`? *Recommended and chosen: yes.* Without
   it, no helper comes over.
6. **Exercise 2.3's names.** `exercise_2_3.py` and
   `exercise_2_3_two_steps.py` (the default rule), rather than the
   spec's `exercise_2_3_one_step.py` and `exercise_2_3_two_steps.py`?
   *Recommended and chosen: the default rule,* the same as 4.5's pair.
7. **The derive-all search.** Leave 005's search out of 007, for a
   later series if wanted? *Recommended and chosen: yes.*

### Corrections to the checkpoint

- It says the eight failing scripts each fail "after printing some
  output". kinematic-equations 000, 001 and 002-dt print nothing but
  the traceback.
- It says 4.1's 128 N and 141.6° come from v1-006 and v1-007. v1-000
  to v1-002 (only R two-way) print them too, and 141.6° is the old
  number: the book prints 141°.
- 3.6 v1-000 needs the shim only for its import: it never calls
  `solve_system_2`.
- 004 at depth 2 took 128 s today, four scripts at a time, against the
  survey's 114 s.
