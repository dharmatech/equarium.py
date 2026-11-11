# physics 007: the end

**Status:** Done at `bb0f492` and reviewed (2026-11-09).

If you've been told to read this file, this is the whole assignment.
Build it, check it, commit it, report, and stop.

## Goal

The last increment. It deletes the old physics code's copy, sets the
version to 0.2.0, and says in the docs that the series is done. No
equation, formula, example or `BOOK` changes. That means:

- **The old copy goes:** `src/equarium/physics/kinematics_states.py`
  and `newtons_laws.py`. Only `tests/test_physics.py` imports them.
- **`tests/test_physics.py` stops using it.** Four of its tests use the
  copy today. Two go. The other two become one, with the copy's output
  written out as strings. Its 60 tests become 57.
- **`physics/__init__.py`'s docstring loses its last paragraph,** which
  says the copy stays until 007.
- **The version is 0.2.0,** in `pyproject.toml`. `uv.lock` records the
  version too, so it changes with it.
- **The docs say the series is done:** the series README, the series
  map and 002's README.

**The record of the old results doesn't change.**
`tests/test_old_outputs.py` and `tests/old_names.py` stay as they are,
character for character: the 66 rows, `RESHAPED` and the rename map.
The next section says why they can. The user approved that section
(2026-11-09), which had to happen before this increment is built.

The fast suite goes from 347 tests to 344.

**Not in this increment:**

- **Merging into `master`, tagging `v0.2.0` and pushing.** They are the
  user's calls. The builder commits on the branch and stops.
- **Any example, any `BOOK`, the core, or the layer's other ten
  modules.** Only the docstring of `physics/__init__.py` changes.
- **The package `README.md`.** The spec asks 007 to update its mention
  of the old code. Increment 001 already did: its sentence reads "Most
  of them run on equarium's physics layer, `equarium.physics`". Nothing
  in it names the copy, so it doesn't change.
- **The docs that name the two files as history:** 002's charter, spec
  and checkpoint 007, the catalog, and this series' charter, spec and
  earlier checkpoints.
- **The comments that name the old code's functions as history:**
  `tests/old_names.py` (`make_states_model`'s and `make_point`'s
  names), `tests/test_strategies.py` and 4.1's docstring.
- **`tests/slow_examples.py`.** It stays, empty, for the next slow
  module.
- **The findings for a later series,** in the series README: labels for
  generated equations, `show(symbol=…)` and `clear_zero_denominators`.

## For the user to approve: the record

**Approved:** yes, by the user (2026-11-09), in the conversation that
wrote this page.

**The kinematics test:** kept, with the copy's side written out. The
user chose that on 2026-11-09, over "the other way" below.

The old scripts' output, compared with today's, is the proof that the
redesign kept every old result. After this increment, that proof is in
two files. Both stay exactly as they are:

- **`tests/test_old_outputs.py`,** 89 tests:
  - `OLD`, the 66 rows. Each is a formula an old script printed,
    verbatim, in the old names, with its number;
  - `RESHAPED`, the new formulas of the five rows of 3.6 that the
    projectile setup changed;
  - `OLD_GIVENS`, the old givens of 3.7, 3.9 and 4.7, and `OLD_3_10`,
    3.10's show-that;
  - the two guards, which pin the counts 66 and 5.
- **`tests/old_names.py`:** `old_name` and `old_str`, which rename a
  symbol back by the old rule, and `SCRIPT_NAMES`, the 18 names in 8
  modules that an old script made itself.

**Neither file uses the old copy.** Checked in scratch, on the repo's
files at `10f9d5f`:

- **The rows are text.** They were quoted from the catalog, which has
  the old scripts' output as the old repo printed it on 2026-11-08.
  Nothing computes them.
- **Neither file imports the copy.** Beside the standard library,
  `tests/test_old_outputs.py` imports SymPy, pytest, `Solution`,
  `System`, `Var`, `old_names` and `slow_examples`.
  `tests/old_names.py` imports SymPy and `Var`. `equarium.physics`
  imports neither old module.
- **With the copy still there,** `tests/test_old_outputs.py`, run
  alone, passes its 89 tests and loads neither old module. The whole
  fast suite without `tests/test_physics.py` passes 287 tests and
  loads neither.
- **With the copy deleted,** the same 89 tests pass, the 66 rows among
  them.

**What goes with the copy.** Four tests in `tests/test_physics.py` use
it, and nothing else does:

| Test today | After |
|---|---|
| `test_vector_equations_renamed_back_are_the_old_copys` | goes |
| `test_newton_renamed_back_is_the_old_copys` | goes |
| `test_kinematics_renamed_back_are_the_old_copys` | stays, with the copy's side written out |
| `test_the_same_equations_as_the_old_library` | its four strings move into the test above |

- **The two that go lose nothing but the comparison.** Each compared
  equations of the new layer, renamed back, with the copy's. The same
  equations stay pinned as strings, in the new names, by the tests
  beside them: `test_polar_one_way_each`,
  `test_eq_makes_one_equation_per_axis` and
  `test_newton_makes_one_equation_per_axis`.
- **The kinematics test stays, because nothing else pins what it
  pins.** It is the only test that has three states in `XY`, where the
  order of the equations is each edge, then x and y. No example has
  that shape. Checked by breaking it in scratch: with the kinematics
  loops swapped, each axis and then each edge, today's fast suite fails
  that test and passes the other 346. With all four tests deleted, the
  swapped loops pass all 343 tests. With the test kept as below, they
  fail it again.
- **So its old side is written out.** Today the copy computes it. The
  22 strings under "Build" are the copy's output, printed before the
  copy went. The first four are the old library's own, which the fourth
  test has today. The test then needs no copy.

**The other way,** as the spec says it, strictly: delete all four
tests. Then the fast suite has 343 tests, and no test pins the order of
the kinematics equations for several edges and several axes. Scratch
passed both ways. The user didn't choose it (2026-11-09).

**Where the old code still is:** the tag `v0.1.0`, every commit of this
branch before this increment's, and the old repo,
`~/src/combine-equations.py`.

## Read first

- **[The spec](../spec.md):** "### 007 the end", "### The tests" and
  "How each increment lands".
- **The series [README](../README.md),** its status and "What's next".
- **The code:** `tests/test_physics.py` (its imports, the four tests
  above and its last section), `src/equarium/physics/__init__.py`'s
  docstring, and `pyproject.toml`.
- **The docs to edit:** the series README, the
  [series map](../../README.md) and
  [002's README](../../002-core/README.md).

## Starting point

The branch `2026-11-08-physics-redesign`, at the commit that adds this
checkpoint, on top of `10f9d5f` (the review of 006). Check it with
`git branch --show-current`. If you're on another branch, stop and ask.
Don't switch branches, stash or reset.

**The line "Approved" above must say "yes".** If it says "not yet",
stop and ask.

`uv run pytest` passes 347 tests and deselects 3 slow ones, in about
48 s. `uv run pytest -m slow` passes those 3, in about 5 min.
`uv run pyright` reports 0 errors and 0 warnings.

Checked in scratch while writing this page, on the repo's files at
`10f9d5f`, with the increment built as this page says:

- **The fast suite** passes 344 tests and deselects 3, in 48.3 s.
  Before the change, its 347 took 47.9 s on the same machine.
  `tests/test_physics.py` has 57 tests, where it had 60, and no other
  file's count changes: `tests/test_old_outputs.py` keeps its 89.
- **The slow tests** pass, all 3, in 5 min 21 s, run beside other
  work. They are the three in `tests/test_strategies.py`, which doesn't
  import the physics layer.
- **Pyright** reports 0 errors and 0 warnings over `src`, `tests` and
  `examples`.
- **The 22 strings** of the kept test are the copy's output, line for
  line, in order. The command under "Build" printed them.
- **`uv run` rewrote `uv.lock`,** one line: the package's `version`.
  The installed version reads 0.2.0.
- **The diff** is six files: the two deleted, 484 lines, and
  `physics/__init__.py`, `tests/test_physics.py`, `pyproject.toml` and
  `uv.lock`. `tests/test_physics.py` goes from 629 lines to 604.
- **The greps** under "Check and commit" find nothing. Today they find
  6, 22 and 6 lines.
- **With all four tests deleted instead,** the fast suite passes 343
  tests in 48.0 s, the slow tests pass in 5 min 21 s, and pyright
  reports 0 errors.

## Build

### Before deleting: print the copy's strings

Run this once, while the copy is still there:

```bash
uv run python -c "
from equarium.physics.kinematics_states import kinematics_fundamental, make_states_model
for n, axes in ((2, ('x',)), (2, ('y',)), (3, ('x', 'y'))):
    for eq in kinematics_fundamental(make_states_model('m', n), axes=axes):
        print(eq)
"
```

It prints 22 lines. They must be the 22 strings of the test below, in
order. If one differs, stop and report it.

### Delete the old copy

`git rm src/equarium/physics/kinematics_states.py src/equarium/physics/newtons_laws.py`.
Eleven modules are left in `src/equarium/physics/`.

### `tests/test_physics.py`

**The imports.** These two go:

```python
from equarium.physics.kinematics_states import (
    kinematics_fundamental,
    magnitude_and_angle_equations,
    make_point,
    make_states_model,
)
from equarium.physics.newtons_laws import newtons_second_law, superposition_equations
```

`from old_names import old_str` stays: the kept test uses it.

**Two tests go,** whole: `test_vector_equations_renamed_back_are_the_old_copys`
and `test_newton_renamed_back_is_the_old_copys`.

**One test is rewritten.** `test_kinematics_renamed_back_are_the_old_copys`
becomes this, in the same place. Scratch used exactly this:

```python
def test_kinematics_renamed_back_are_the_old_codes() -> None:
    # The old physics code's output, written out: equarium's copy of that
    # code went in increment 007 of the 004 series. The first four strings
    # are the old library's own, from its venv in combine-equations.py
    # (2026-11-08). The rest are the copy's, printed before it went.
    assert [old_str(eq) for eq in m.kinematics()] == [
        "Eq(dt_m_0_1, -m_0_t + m_1_t)",
        "Eq(v_av_x_m_0_1, (-m_0_x + m_1_x)/dt_m_0_1)",
        "Eq(a_x_m_0_1, (-m_0_v_x + m_1_v_x)/dt_m_0_1)",
        "Eq(v_av_x_m_0_1, m_0_v_x/2 + m_1_v_x/2)",
    ]
    assert [old_str(eq) for eq in Particle("m", 2, Y).kinematics()] == [
        "Eq(dt_m_0_1, -m_0_t + m_1_t)",
        "Eq(v_av_y_m_0_1, (-m_0_y + m_1_y)/dt_m_0_1)",
        "Eq(a_y_m_0_1, (-m_0_v_y + m_1_v_y)/dt_m_0_1)",
        "Eq(v_av_y_m_0_1, m_0_v_y/2 + m_1_v_y/2)",
    ]
    # Three states in XY, which no example has: for each edge, x then y.
    assert [old_str(eq) for eq in Particle("m", 3, XY).kinematics()] == [
        "Eq(dt_m_0_1, -m_0_t + m_1_t)",
        "Eq(dt_m_1_2, -m_1_t + m_2_t)",
        "Eq(v_av_x_m_0_1, (-m_0_x + m_1_x)/dt_m_0_1)",
        "Eq(v_av_y_m_0_1, (-m_0_y + m_1_y)/dt_m_0_1)",
        "Eq(v_av_x_m_1_2, (-m_1_x + m_2_x)/dt_m_1_2)",
        "Eq(v_av_y_m_1_2, (-m_1_y + m_2_y)/dt_m_1_2)",
        "Eq(a_x_m_0_1, (-m_0_v_x + m_1_v_x)/dt_m_0_1)",
        "Eq(a_y_m_0_1, (-m_0_v_y + m_1_v_y)/dt_m_0_1)",
        "Eq(a_x_m_1_2, (-m_1_v_x + m_2_v_x)/dt_m_1_2)",
        "Eq(a_y_m_1_2, (-m_1_v_y + m_2_v_y)/dt_m_1_2)",
        "Eq(v_av_x_m_0_1, m_0_v_x/2 + m_1_v_x/2)",
        "Eq(v_av_y_m_0_1, m_0_v_y/2 + m_1_v_y/2)",
        "Eq(v_av_x_m_1_2, m_1_v_x/2 + m_2_v_x/2)",
        "Eq(v_av_y_m_1_2, m_1_v_y/2 + m_2_v_y/2)",
    ]
```

- **The first case is new here.** It is `m`, the module's `X` particle
  with two states, against the four strings that
  `test_the_same_equations_as_the_old_library` has today. That test
  checked the copy against them. This one checks the new layer, renamed
  back.
- **The other two cases are today's,** `Particle("m", 2, Y)` and
  `Particle("m", 3, XY)`, with the copy's side written out.

**The last section.** `test_the_same_equations_as_the_old_library`
goes, since its strings moved. The section's comment,
`# The old copy, and the layers`, becomes `# The layers`.
`test_the_core_doesnt_import_the_physics_code` stays, as the spec asks.

**The module docstring.** Its last sentence, "Also the old physics
code's copy, until increment 007 deletes it, and the layers." becomes:
"Also the kinematics equations against the old physics code's output,
and the layers."

**Everything else stays,** the other 56 tests among them.

**The other way, which the user didn't choose** (2026-11-09), for the
record. Don't build it. All four tests would go, and so would
`from old_names import old_str`, which nothing else in the file uses.
The docstring's last sentence would be "Also the layers: the core
doesn't import the physics layer." The fast suite would then have 343
tests, and `tests/test_physics.py` 56.

### `physics/__init__.py`

The docstring's last paragraph goes, with the blank line before it:

```
The old physics code from combine-equations.py, `kinematics_states` and
`newtons_laws`, stays here until increment 007 of the 004 series. No
example uses it any more: only `tests/test_physics.py` does, to compare.
```

The docstring then ends with the paragraph on Newton's second law.
Nothing else in the file changes: it never re-exported the copy.

### The version

- **`pyproject.toml`:** `version = "0.1.0"` becomes `version = "0.2.0"`.
- **`uv.lock`** has the package's version too, at its line 16. The next
  `uv run` rewrites that line, and nothing else in the file. The spec
  names only `pyproject.toml`. Commit both.
- **Nothing reads the version in code.** There is no `__version__`.

### If a test fails that this page doesn't list

Nothing else should fail. If a row of `tests/test_old_outputs.py`
fails, or a `BOOK`, or any test this page doesn't remove, stop. Don't
change a row, `RESHAPED`, `tests/old_names.py`, an example or a module
of the layer to make it pass. Report the test and what it printed.

## Docs

- **The series [README](../README.md):**
  - its status line says all seven increments are built, that 007 waits
    for review, that the old copy is deleted and the version is 0.2.0,
    and that merging, tagging and pushing are the user's calls;
  - "6 of 7 done" becomes "7 of 7 done", and row 007 says
    "Done (2026-11-09)";
  - the sentence before the prompt says the last checkpoint was 007 and
    the series is done, as 002's README says of its own;
  - "What's next" starts with what is left, the user's three calls, and
    then says what 007 did, in the past tense. Its paragraphs on the
    earlier increments, the reviews and the findings for a later series
    stay;
  - leave row 007's commit cell and this page's status line for the
    manager.
- **The [series map](../../README.md):**
  - row 004's status becomes "Done (2026-11-09): 7 of 7 increments
    done, on branch `2026-11-08-physics-redesign`, as version 0.2.0";
  - the paragraph on 004 gains: "Done: every example runs on the new
    layer, the old physics code's copy is deleted, and the version is
    0.2.0. The branch merges into `master` when the user chooses.";
  - in the paragraph on 002, "The physics redesign would be the next
    series." becomes "Series 004 then redesigned the physics layer and
    deleted that code."
- **[002's README](../../002-core/README.md)** gains a dated note at its
  end, after the two it has:

  ```
  *(2026-11-09: series 004 is done. The old physics code that this
  series copied over, `kinematics_states.py` and `newtons_laws.py`, is
  deleted: every example runs on the new physics layer, with the same
  book answers. Both findings above are settled for the examples. 3.6
  uses the projectile setup, so it needs neither
  `clear_zero_denominators` nor its by-hand step. Polar is one way, so
  3.9 and 3.10 aren't slow any more, and `tests/slow_examples.py` is
  empty.)*
  ```

- **The docstrings** of `physics/__init__.py` and
  `tests/test_physics.py`, as above.
- **Don't edit** `spec.md`, `charter.md`, this page, the earlier
  checkpoints or the package `README.md`. If something here is wrong,
  say so in the report.

## Check and commit

- **`uv run pytest`** passes 344 tests and deselects 3, in about 48 s.
- **`uv run pytest -m slow`** passes the 3 slow tests, in about 5 min.
  Run it in the background.
- **`uv run pyright`:** 0 errors and 0 warnings, over `src`, `tests`
  and `examples`.
- **Nothing imports the old copy.** Each of these finds nothing. They
  use `git grep`, which reads tracked files only, so a stale compiled
  cache can't match.

  ```bash
  git grep -n "kinematics_states\|newtons_laws" -- src tests examples README.md pyproject.toml
  ```

  ```bash
  git grep -n "make_states_model(\|kinematics_fundamental(\|make_point(\|Point3(\|magnitude_and_angle_equations(\|newtons_second_law(\|superposition_equations(" -- src tests examples
  ```

  ```bash
  git grep -n "old copy\|007 deletes\|until increment 007" -- src tests examples README.md
  ```

  Today they find 6, 22 and 6 lines.
- **The copy is gone at run time.**
  `uv run python -c "import equarium.physics.kinematics_states"` raises
  `ModuleNotFoundError`, and so does `newtons_laws`.
- **The version.**
  `uv run python -c "import importlib.metadata as m; print(m.version('equarium'))"`
  prints `0.2.0`. `git diff HEAD -- uv.lock` shows one line changed.
- **The record is untouched.**
  `git diff HEAD --stat -- tests/test_old_outputs.py tests/old_names.py examples README.md`
  prints nothing.
- **Nine paths, and no others,** in `git status --short`: the two
  deleted modules, `src/equarium/physics/__init__.py`,
  `tests/test_physics.py`, `pyproject.toml`, `uv.lock`, and the three
  docs.
- **No files outside the repo.** Keep scratch output in your own
  scratch folder.
- **One commit on the branch `2026-11-08-physics-redesign`,** with the
  code, tests and docs, staged by path, in the style of `git log`: a
  subject line, then a wrapped paragraph saying what and why.
- **Don't merge, tag or push.** Don't switch to `master`.

## Report

When done, say in a few lines:

- the commit, the number of tests, fast and slow, and how long the fast
  run takes;
- that the 22 strings were the copy's output before it went, or the
  line that differed (you stopped there);
- that the three greps find nothing, and that
  `tests/test_old_outputs.py`, `tests/old_names.py` and the examples
  are untouched;
- anything you named or worded differently from this page, and why;
- anything in the spec or this checkpoint that was wrong or unclear,
  and what you did instead.

Then stop. There is no next checkpoint.

## After the review: the user's calls

Not the builder's, and not part of this increment.

- **The merge.** `master` is at `v0.1.0` (`3370e5d`), and so is
  `origin/master` as this folder last saw it. `master` is an ancestor
  of this branch, so the merge can be a fast-forward.
- **The tag** `v0.2.0` goes on the merged commit.
- **The push:** `master`, the tag `v0.2.0`, and the tag `v0.1.0` if it
  is still local.
