# 001 example catalog: checkpoint

**Status:** Written and reviewed (2026-11-08). Not started.

If you've been told to read this file, this is the whole assignment.
Survey the old examples, write the catalog, check it, commit it,
report, and stop.

## Goal

Write `docs/design/implementation/001-example-catalog/catalog.md`: one
entry for every problem the old library's `examples/up/` solves, plus
`ch2/kinematic-equations/`. Each entry records the problem, the book's
printed answers, the techniques, every old script with its role and
what it prints, the styles worth keeping, and what equarium already
covers. The catalog ends with recommendations for
[002 core](../002-core/README.md)'s increment 007, which ports the old
physics code and the examples onto the new core and is written from
this catalog.

No code changes: not in equarium, and never in the old repo. Stop when
the catalog is written, checked and committed.

## Read first

- [This series' README](README.md), for what the catalog is for.
- [002's spec](../002-core/spec.md):
  - "Values or equations: `eliminate_zeros`", for how old zero
    equations and zero values map onto the core;
  - "Strategies", for how the old solving styles map onto the core;
  - "Examples in the repo", for the layout, the slugs and `BOOK`;
  - §007, which says what 007 needs from this catalog.
- [002's charter](../002-core/charter.md): "Where the old library is"
  (the library's modules, and the shim, extended below) and "What the
  old library taught".
- equarium's three example modules, as models of a port:
  `examples/up_15e/ch02/example_2_4_handwritten.py`,
  `example_2_5_handwritten.py` and
  `example_2_5_handwritten_step_by_step.py`, and `examples/answers.py`.

You don't need 002's checkpoints. What they found that matters here
is under "Starting point".

## Where things are

- **The old repo:** `~/src/combine-equations.py`, at `d9d15b3`, clean.
  Never edit it, its `uv.lock` included: run it with `uv run --frozen`.
  - The scripts: `examples/up/`, 50 `.py` files and 2 notebooks.
    `examples/eq-gui/` is out of scope.
  - The library: `src/combine_equations/`.
  - Its own tests pin three examples: `tests/test_up_example_3_6.py`,
    `test_up_example_3_7.py` and `test_up_example_3_9_v2.py`.
- **The textbook:** `~/journal/2026-11-06-equations/up-15e.pdf`,
  University Physics with Modern Physics, 15th edition, 1596 pages.
  Never read it whole. Pages here are the PDF's page numbers, not the
  printed ones.
  - `pdftotext -f P -l Q -raw up-15e.pdf -` extracts pages P to Q and
    keeps fractions readable. `-layout` garbles them.
  - The examples, by the page where each starts. An example can run
    onto the next page.

    | Pages | Examples |
    |---|---|
    | 78 | 2.4, 2.5 |
    | 80 to 82 | 2.6, 2.7, 2.8 |
    | 107 to 110 | 3.6, 3.7, 3.8 and 3.9, 3.10 |
    | 116 | 3.13 |
    | 133 | 4.1 |
    | 141 | 4.4, 4.5 |
    | 145 | 4.7 |

  - Chapter 2's exercises: 2.1, 2.3 and 2.5 on page 89, and 2.19, 2.21
    and 2.23 on page 90.
  - The answers to the odd-numbered exercises, for chapters 1 to 6, are
    on page 1563 (printed A-9). `-raw` mixes the columns there, so grep
    for the line, as in `grep -E '^2\.23 '`. All six exercises here are
    odd.
- **equarium:** `~/journal/2026-11-06-equations/equarium.py`, this repo.

## Starting point

`master` at the commit that adds this checkpoint, on top of `9ec5d88`
(002's increment 006). `uv run pytest` passes 160 tests in about 20 s,
with the 3 slow ones deselected. `uv run pyright` reports 0 errors and
0 warnings. Both venvs have SymPy 1.14.0.

### Running the old scripts

**Use this shim,** saved in your scratchpad, never in the old repo. It
extends the one in 002's charter:

```python
# run_with_shim.py: runs one old example script, from the old repo's root:
#   PYTHONUNBUFFERED=1 uv run --frozen python <this file> <example.py>
import runpy, sys, types
import sympy as sp
import combine_equations.display_equations as de
import combine_equations.solve_system as ss

# 1. solve_system_2 was commented out on 2026-01-09; 11 scripts import it.
def solve_system_2(equations, values, want):
    unknowns = list(ss.connected_unknowns(equations, values, want))
    result = sp.solve(equations, unknowns, dict=True)
    return sp.Eq(want, result[0][want])

ss.solve_system_2 = solve_system_2

# 2. The old venv's Python has no tkinter, so equation_gui can't import.
#    Exercises 2.21 and 2.23 import it; 2.21 opens the GUI.
def show_equation_gui(equations, values=None, want=None, description="Initial equations"):
    print(f"[shim: show_equation_gui({description!r}, want={want}) skipped]")

gui = types.ModuleType("combine_equations.equation_gui")
gui.show_equation_gui = show_equation_gui
sys.modules["combine_equations.equation_gui"] = gui

# 3. No colors: the old display colors a symbol by renaming it, which
#    changes SymPy's term order. Plain names print SymPy's own order,
#    the order equarium's display keeps.
de.red_text = de.green_text = lambda s: s

runpy.run_path(sys.argv[1], run_name="__main__")
```

- **What needs which part.** The 11 scripts that import
  `solve_system_2`: 2.4's three, 2.5's four, 2.6's two, 2.7 v1-000 and
  3.6 v1-000. The GUI stub: Exercise 2.21's two scripts and 2.23-000.
  Every script gets the plain names.
- **Why plain names matter.** With colors, 2.4 v4-001 prints
  `v_av_x_m_0_1 = (m_1_x - m_0_x)/dt_m_0_1`. With the shim, it prints
  `(-m_0_x + m_1_x)/dt_m_0_1`, SymPy's own order. The catalog records
  the plain output, which is what 007 compares with.
- **Run them all first,** in the background, four at a time, one log
  per script, with the exit code and the time of each. All but two
  finish within 20 s. Leave out kinematic-equations 004 (below), and
  the whole run takes about as long as 4.1 v1-003, about 9 minutes.
  Give each script a timeout of 15 minutes.

### What a survey run on 2026-11-08 found

The same shim, without part 3, on every script:

- **41 of the 50 run to the end,** in 2 to 18 s each, most of it
  start-up.
- **8 fail even with the shim,** each partway through, after printing
  some output:

  | Script | Error |
  |---|---|
  | kinematic-equations `000`, `001`, `002-dt` | `NameError: display_equation_` (never imported) |
  | `ch3/up-example-3.9-v1-000.py` | `ValueError: No solutions found.` from `solve_system_multiple_solutions` |
  | `ch3/up-example-3.10-v1-000.py` | `IndexError` from `sp.solve(...)[0]`, line 121 |
  | 4.1 `v1-003-4-force-equations` | `ValueError: No solutions found.` at `R_angle_deg`, after 9 min 15 s (see the 002 findings below) |
  | 4.1 `v1-004-4-force-equations-elim`, `v1-005` | `NameError: R_angle_deg`, at the last solve |

  For each, the catalog records how far it got, and whether a later
  version of the same problem replaced it.
- **1 doesn't finish:** kinematic-equations `004-every-possible-eq`.
  At line 151 it calls `derive_all_equations([eq_2_2, eq_2_7, eq_2_10],
  max_depth=3)`. Depth 1 finds 8 new equations and depth 2 finds 196
  within 150 s, but depth 3 hadn't finished after 20 minutes. So the
  derivations after it never print: the book's 2.14, 2.8, 2.13 and
  2.12, by hand with misc.py's both-sides helpers. Don't wait for it.
  Copy the script to your scratchpad, set `max_depth=2` on line 151,
  run the copy with the shim from the old repo's root, and say so in
  the catalog. The copy ran to the end in 114 s and printed the four
  equations, ending with `x_2 = a_x*dt**2/2 + dt*v_1x + x_1`.
- **The run printed about 2,100 lines,** most of them derivations.
  Don't read the logs whole: grep them for the solution lines.

### Findings from 002 the catalog must carry

- **Exercise 2.3:** the book's answer is 55 min, how much longer the
  slow trip takes. The old scripts compute the slow trip's 2.75 h.
  equarium's `tests/test_units.py` adds the step to 55 min.
- **Example 3.9:** the book prints 9.2 m. The old v2 prints 9.16
  (v1-000 fails, below).
- **Example 4.1 v1-003,** with the two-way polar equations, never gives
  |R| or the angle as numbers. It "solves" them as
  `sqrt(R_x**2 + R_y**2)` and `atan2(R_y, R_x)`, formulas in other
  unknowns, and its last step then raises "No solutions found". The
  128 N and 141.6° come from v1-006 and v1-007, with one-way
  equations. On equarium, R_x took 91 s and R_y 223 s with
  `eliminating()`; |R| didn't finish in 20 minutes.
- **Example 3.9 v2,** two-way: `all_at_once` finds no roots, and
  `eliminating()` finds 9.16 after seven eliminations, in about 6 s.
  One-way, `all_at_once` finds it in about 1 s.
- **Example 3.10's** "show that" ends with the stated condition, not
  an empty system. It reaches an empty system once `Eq(d1x, D)` is
  added.

### What equarium covers today

Written out by hand in tests or example modules, never through the old
physics code, which arrives in 007:

| Problem | Where | From the old script |
|---|---|---|
| 2.4 | `examples/up_15e/ch02/example_2_4_handwritten.py`; `tests/example_2_4.py`, `tests/test_solve.py` | v3-001 |
| 2.5 | `example_2_5_handwritten.py`, `example_2_5_handwritten_step_by_step.py`; `tests/test_rewrite.py` | v3-002, v3-001 |
| 2.7, 2.8 | `tests/test_roots.py` | 2.7 v1-000 |
| 3.9 | `tests/test_roots.py` (one-way), `tests/test_strategies.py` (two-way, slow) | v2 |
| 3.10 | `tests/test_rewrite.py` | v1-001 |
| 4.1 | `tests/test_rewrite.py` (by hand, one-way), `tests/test_strategies.py` (two-way, R_x and R_y, slow) | v1-006, v1-003 |
| Exercise 2.3 | `tests/test_units.py` | 000 two steps, 002 one step |
| Exercise 2.23 | `tests/test_units.py` | 000 |
| kinematic-equations | `tests/kinematics_005.py`, `tests/test_rewrite.py`: the first derivation only | 005 |

## Build

### How to work

- **Write the catalog as you go,** one problem at a time, in the order
  below. The file holds the work, not the conversation.
- **Read narrowly.** For a problem with several versions, read the
  latest whole, and the others through `diff` against the version next
  to them. For the logs, grep for the solution lines.
- **If the context grows large,** stop after a finished chapter. Put
  where you stopped in the catalog's status line, commit, and report.
  A new conversation continues from this page and the catalog. You
  may also hand one chapter's survey to a subagent, with this page's
  entry shape. Check its book answers against the PDF and its printed
  output against the logs before they go in.
- **The order:** chapter 2's examples, chapter 2's exercises,
  kinematic-equations, chapter 3, chapter 4, then the recommendations
  for 007.

### The catalog's shape

`catalog.md` has these sections, in this order.

**1. Header.** The title `# Example catalog`, a status line, and a
short paragraph: what it covers, the old repo's commit (`d9d15b3`),
the date of the runs, the SymPy version (the old repo's venv), and how
the runs were made (the shim above, plain names). Then one paragraph
on how to read an entry, and the technique vocabulary (below).

**2. Index.** One table, one row per problem, in the book's order:

| Problem | Title | Page | Old scripts | Book's answers | In equarium | Port in 007 as |
|---|---|---|---|---|---|---|

- *Problem*: `Example 2.4` or `Exercise 2.3`, linked to its entry.
- *Title*: the book's title, for examples. A few words of your own for
  exercises.
- *Page*: the PDF page.
- *Old scripts*: the count, and how many ran to the end.
- *Book's answers*: short, with units: `43 m; 23 m/s; 55 m`.
- *In equarium*: from the table above, updated as later series port
  examples.
- *Port in 007 as*: the module names, or "not ported" and a word on
  why.

**3. One entry per problem,** in the index's order: 21 in all.

- Examples 2.4 to 2.8; 3.6 to 3.10 and 3.13; 4.1, 4.4, 4.5 and 4.7.
- Exercises 2.1, 2.3, 2.5, 2.19, 2.21 and 2.23.

Example 2.8 is solved inside 2.7's script, but gets its own entry,
pointing at it. Each entry has this shape:

````markdown
## Example 2.4: Constant-acceleration calculations

PDF page 78. Old folder: `examples/up/ch2/up-example-2.4/`.

**Problem.** <Two to four sentences in your own words, with every given
number and unit, and the questions as (a), (b), …>

**Book's answers.**

| Part | Quantity | Printed |
|---|---|---|
| (a) | position at 2.0 s | 43 m |

**Old scripts.**

| Script | Style | Role | Runs | Time |
|---|---|---|---|---|
| `up-example-2.4-v4-001-ks-display-solution.py` | physics code, all at once, zero equations | latest | yes, shim | 2 s |

<Then, for each script that runs, a code block with what it prints for
each want: the formula and the number, verbatim from the plain run, as
in:>

```
m_1_x = a_x_m_0_1*m_1_t**2/2 + m_0_v_x*m_1_t + m_0_x
m_1_x = 43
```

<A script that fails: how far it got, and the error. A script that
prints a long derivation: the final equations and the solutions only,
and the number of lines it printed.>

**Techniques.** <From the vocabulary below.>

**Zeros.** <Per script to port: which zeros are equations and where
they're eliminated, which are values. 007 turns the first into
`known(sym, 0)` plus `eliminate_zeros()` at that point, and the second
into `known(sym, 0)` alone.>

**Physics code used.** <The functions from `kinematics_states.py` and
`newtons_laws.py` the scripts to port call, such as
`make_states_model`, `kinematics_fundamental`,
`magnitude_and_angle_equations`, `link_same_time`.>

**Styles worth keeping.** <Which scripts show a style worth keeping as
a contrast, and why, with the module name each becomes.>

**In equarium.** <What covers it now.>

**Notes.** <Differences between the book and the old output, edition
mismatches, bugs in the old scripts, anything 007 must know.>
````

- *Role* is one of: **latest** (the newest version of its style),
  **alternative** (a different style kept on purpose), **draft** (a
  later version replaced it: say which), **duplicate** (say of what),
  **other library** (it doesn't use combine_equations).
- *Runs* is: **yes**, **yes, shim** (it needed `solve_system_2` or the
  GUI stub), or **fails** (and the error).
- *Time* is the run's wall time, rounded to the second.
- **The problem in your own words.** The catalog is meant for a public
  repo, and some old scripts copy the book's text into their comments.
  Keep the numbers and the questions, not the wording.
- **The book's answers come from the book,** never from the old
  output. For an example, they're in the worked solution, usually
  under EXECUTE. For an exercise, they're on page 1563. Copy them as
  printed, with their significant figures (`9.2 m`, not `9.16 m`).
- **Check the edition.** The old scripts don't say which edition they
  follow. For each problem, confirm that the 15th edition's problem
  with that number is the one the script solves, with the same givens.
  A mismatch goes in Notes and in the report.

**4. kinematic-equations,** one entry for the folder, in the same
spirit:

- each script and the notebook: what it derives, by which technique,
  whether it runs, and which of the book's equations it reaches (2.8,
  2.12, 2.13, 2.14, from Table 2.5 on page 77);
- which of misc.py's helpers each uses (`add_both_sides`,
  `multiply_both_sides`, `divide_both_sides`, `expand_lhs`,
  `expand_rhs`, `isolate_variable`), and its own local helpers;
- 005: what the derive-all search does, how many equations it finds,
  how long it takes, and what its history printout looks like (a few
  lines, verbatim).

**5. Other files,** briefly: the 11 PNG images (figures from the book,
saved beside the scripts; never copied into equarium), the notebook's
`.ipynb_checkpoints` copy, and the old repo's three tests, with the
values they pin.

**6. Recommendations for 007.** The section 007's checkpoint is written
from. It decides, with a reason for each:

- **The port list.** One table: the module to create
  (`examples/up_15e/ch02/example_2_4.py`), the old script it comes
  from, its `BOOK` lines exactly as they'll be written, and the old
  formulas it must reproduce. Include the problems already covered by
  tests, since 007 ports their physics-code versions.
- **Where the old output isn't the book's answer,** as in Exercise 2.3,
  what the port adds to reach it, as `tests/test_units.py` does for
  2.3. The `BOOK` holds the book's answer, and the old formulas are
  still compared as they are.
- **The slugs.** A short list, each with its meaning. Start from the
  spec's `_handwritten`, `_step_by_step`, `_two_steps` and `_one_step`,
  and add as few as the kept styles need. The default to apply unless
  the scripts argue otherwise: the physics-code version solved all at
  once has no slug (`example_2_4.py`), and a slug marks each kept
  contrast. Note that the existing `example_2_5_handwritten_step_by_step.py`
  combines two slugs.
- **What isn't ported,** each with a reason: drafts, duplicates, the
  other-library script, GUI-only scripts, and scripts that never
  produced the answer. Say whether any of them still teaches something
  a test should keep.
- **misc.py's both-sides helpers:** whether they come over (as plain
  functions on `sp.Eq` in `equations.py`, per the spec), and which
  example needs them. Today only kinematic-equations 003, 004 and the
  notebook import them.
- **kinematic-equations 005's derive-all search:** whether it's ported,
  and if so where (an example module, a test, or the core) and what it
  checks. equarium's origin tree already records provenance.
- **The physics code:** the functions the port list needs from
  `kinematics_states.py` and `newtons_laws.py`, and anything a kept
  example needs that the old physics code doesn't have. That goes to
  the physics redesign, not 007.
- **007's size:** the number of modules, and whether 007 fits one
  checkpoint or should be split, such as chapter 2, then chapters 3 and
  4.
- **Questions for the user:** every choice above that the scripts
  don't settle, each with your recommendation.

### The technique vocabulary

Use these words, so an entry can be found by grep. Add a word only
when none fits, and define it in the header.

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
| polar two-way, polar one-way | `magnitude_and_angle_equations`, or components from polar only | equations |
| show that | eliminate until only the stated condition is left | `eliminate` |
| both sides | misc.py's `add_both_sides` and the rest | none yet |
| derive all | kinematic-equations 005's search | origins only |
| GUI | `show_equation_gui` | out of scope |

### Docs

- **This series' [README](README.md):** set the status line to
  "Catalog written (date), waiting for the user's review", and link
  `catalog.md` under Files.
- **The [series map](../README.md):** 001's status, the same words.
- **002's [README](../002-core/README.md):** leave it. Its manager
  writes 007's checkpoint from the catalog.

Don't edit this page or the spec. If something here turns out wrong,
say so in the catalog's Notes and in your report.

## Check and commit

- **Every file is accounted for.** Each of the 50 scripts and both
  notebooks is named in the catalog. This prints any that aren't, and
  should print nothing:

  ```bash
  cd ~/src/combine-equations.py/examples/up
  find . \( -name '*.py' -o -name '*.ipynb' \) -printf '%f\n' |
    while read -r f; do
      grep -qF "$f" ~/journal/2026-11-06-equations/equarium.py/docs/design/implementation/001-example-catalog/catalog.md || echo "missing: $f"
    done
  ```

- **Every book answer has its page,** and was read there.
- **Every number in a recommended `BOOK` line** matches the book's
  printed answer, to within `Answer`'s half unit in the last digit.
- **Every quoted output** comes from a run with the shim above, today,
  on `d9d15b3`.
- **The old repo is untouched:** `git -C ~/src/combine-equations.py
  status --short` prints nothing.
- **equarium still passes:** `uv run pytest` and `uv run pyright`,
  though no code changed.
- **One commit on `master`,** with `catalog.md` and the two README
  updates, in the style of `git log`: a subject line, then a wrapped
  paragraph saying what and why. Don't push.

## Report

When done, say in a few lines:

- the commit, the number of problems and scripts catalogued, and how
  many scripts ran to the end;
- the port list's size, and whether 007 should be split;
- the decisions on the both-sides helpers and the derive-all search;
- every difference found between the book and the old output, and any
  edition mismatch;
- the questions for the user;
- anything on this page that was wrong or unclear, and what you did
  instead.

Then stop. 002's manager writes 007's checkpoint once the user has
reviewed the catalog.
