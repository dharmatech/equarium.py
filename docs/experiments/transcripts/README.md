# Transcript mode (experiment)

**Status:** a prototype (2026-11-11): the terminal transcript, then the
results written into the script itself, on every save, then three ways
to show a step: only what it changed, the whole value, or the whole
value with its changes marked. This is an
experiment, not a series. It takes a series number only if it's
adopted.

On paper, a student's worksheet keeps each step next to its result, and
they can read it back later. A script keeps only the steps: its results
show up when it runs, apart from the code, or in comments typed by hand
that nothing checks. Transcript mode runs a script and prints its source
as written, with each statement's results under it. The aim is the
worksheet's readability without leaving a plain `.py` file and the
editor.

It should work for any Python script, not only equarium's. So the engine
knows nothing about equarium. A library takes part through IPython's
display methods, which many libraries already have.

**Where:** branch `2026-11-11-transcript-mode`, from
`2026-11-08-physics-redesign` at `0d0949a`, in its own worktree,
`equarium-transcript/`, so the physics branch's review wasn't disturbed.
It merged into the physics branch, and with it into `master`, on
2026-11-11.

## What there is

- **`src/equarium/transcript.py`.** It parses the script with `ast` and
  runs it one top-level statement at a time, as `__main__`, in one
  namespace. It prints every source line, comments and blank lines too,
  and after each statement's last line, its results, marked `#> `:
  - what it printed;
  - its value. Under the worksheet rule, the default, a bare expression
    shows its value and an assignment shows what its target holds, as in
    Mathematica. Under the REPL rule, `--repl`, only a bare expression
    does, as in Python's REPL and Jupyter. Either way a `;` ending the
    line hides it, as in Mathematica and IPython, and neither `None` nor
    the script's docstring shows;
  - an error's traceback, without the module's own frames. The terminal
    transcript ends there.

  A value prints as IPython prints it: by its class's `_repr_pretty_`,
  and otherwise by `repr`. A list, tuple, set or dict shows each item
  so, on one line when it fits in 79 characters, and otherwise one item
  to a line. The module imports nothing from equarium, and a test checks
  that, so it can move to a package of its own. It uses only the
  standard library.
- **In place, and on every save.** The `#> ` lines are comments, so a
  script with its results in it is still the script. `--in-place` runs
  it and writes its results into it. `--watch` does that now and again
  each time the file's code changes, until Ctrl-C: keep it running in a
  terminal, and edit and save the script in VS Code. Every mode first
  drops the `#> ` lines it finds (not ones inside a string), so old
  results never run or pile up, and line numbers in tracebacks and
  syntax errors are the file's.

  In place, the script is written only when it's safe:
  - not when it doesn't parse, as in the middle of an edit;
  - not when it changed while it ran, so a save made meanwhile isn't
    overwritten. The next save runs it again;
  - after an error, with the lines that didn't run kept as they are.

  The results have no colors in the file: color codes would show as
  `\x1b[32m`. Each run under `--watch` is a fresh Python, so changes to
  imported modules take effect too.
- **`System._repr_pretty_` and `Solution._repr_pretty_`.** They print
  what `show()` prints: knowns green, wants red. IPython uses the same
  method, so a system or a solution also prints readably there.
- **Short displays for the model and the book** (branch
  `2026-11-11-worksheet-displays`), by `_repr_pretty_` too, so `repr()`
  and test messages don't change:
  - `Particle` prints `particle m (x): m0, m1`, a `State` its name, `m0`,
    an `Edge` `m01: m0 → m1`, and an `Event` `event meet: m1, q1`;
  - an `Answer` prints its check, `✓ m1.pos.x: book 43 meter, found
    43.0*meter`, or `✗` and what `mismatch()` says. A `Formula` prints
    `✓ p1.t = …, as in the book` when it's found as the book prints it,
    and both forms when it's an equivalent one. So `BOOK` reads as the
    worksheet's answer check, one line to an answer.
- **Each step's effect** (branch `2026-11-11-transcript-changes`). An
  assignment that makes a value from one the reader has seen marks the
  lines that are new or different: after
  `motorcycle = motorcycle.known(m0.pos.x, 5 * meter)` the knowns line
  is starred, and after `part_a = motorcycle.want(m1.pos.x)` the wants
  and what they connect. The source line says what the step did; the
  marks say what that did to the value. The rule, in the engine and for
  any value:
  - the right side starts from a name whose value the reader has seen,
    `motorcycle` in `motorcycle.known(...)`, by calls, attributes and
    subscripts, and the new value is of the same type and takes more
    than one line;
  - lines are compared without their colors, so a symbol turning green
    isn't a change;
  - a line that's gone shows marked `- `. Where a run of lines is
    replaced by as many, each changed in place; where the counts differ,
    `difflib.ndiff` pairs like lines, so eliminating `dt` shows
    `- (1)  m01.dt = m1.t` and the new (2) and (3);
  - a step that changes nothing shows `(no change)`;
  - anything else shows whole: a new value, one of another type, or a
    `solve()`'s solution. So does a name alone on a line, `motorcycle`,
    which is how to see all of it at a point of your choosing;
  - the changes are from what the reader last saw: a step hidden by `;`
    isn't seen, so the next shows both.

  Three ways to show such a value:
  - **marked,** the default: the whole value, each line marked `* ` new
    or different, `- ` gone (in its place), or `  ` the same. The
    context stays next to every step, and what the step did stands out;
  - **`--changes`:** only the marked lines;
  - **`--full`:** the whole value, unmarked, as before.
- **`basics.py`**, beside these notes: a plain Python script with no
  equarium in it.
- **`tests/test_transcript.py`.** The rules on small scripts, in place,
  the watch, and 2.4. Without its `#> ` lines, a transcript is the script.

Run it on a file, or on a module as `python -m` does, and write the
results into it, once or on every save:

```bash
uv run python -m equarium.transcript docs/experiments/transcripts/basics.py
uv run python -m equarium.transcript -m examples.up_15e.ch02.examples.n04.main
uv run python -m equarium.transcript --in-place docs/experiments/transcripts/basics.py
uv run python -m equarium.transcript --watch docs/experiments/transcripts/basics.py
```

The `#> ` mark is the convention of R's `reprex`. It keeps a transcript
valid Python.

## Found so far

- **Plain Python works unchanged.** `basics.py` reads like a worksheet:
  `x * 2` then `#> 10`.
- **2.4's `main.py`, unchanged, under the worksheet rule:** each system
  and solution shows, in color, right under the line that made it. But:
  - `m`, `m0, m1` and `m01` print dataclass reprs, such as
    `Particle(name='m', count=2, axes=<class 'equarium.physics.axes.X'>)`;
  - `BOOK` prints one line of 2,967 characters: `Answer`'s dataclass
    repr includes its `Solution`'s, which includes its `System`'s;
  - the `__main__` block runs, since the script runs as `__main__`, and
    prints every result again. The transcript is 163 lines;
  - the result comments typed by hand, `# m1.pos.x = …   43.0*meter`,
    sit right under the real results, and add nothing.
- **A worksheet-style copy** (a `;` after `m`, `m0, m1`, `m01` and
  `BOOK`, no `__main__` block, no result comments) is 66 lines, each
  result once. It's a scratch copy, not in the repo.
- **With the short displays, 2.4's model and book read in a few lines:**

  ```
  m = Particle("m", 2, X)  # the motorcyclist
  #> particle m (x): m0, m1
  m0, m1 = m.states
  #> (m0, m1)
  m01 = m.edge(0, 1)  # the interval from state 0 to state 1
  #> m01: m0 → m1
  ...
  BOOK: list[Answer] = [  # University Physics, 15th ed.
      ...
  ]
  #> [✓ m1.pos.x: book 43 meter, found 43.0*meter,
  #>  ✓ m1.vel.x: book 23 meter/second, found 23.0*meter/second,
  #>  ✓ m1.pos.x: book 55 meter, found 55.0*meter]
  ```

  The `__main__` block and the result comments are still there.
- **The REPL rule on 2.4's `main.py` shows nothing from its
  statements.** All 53 result lines come from the `__main__` block's
  prints. Under that rule, an example would show a result with a bare
  name on its own line, `sol_a`, as in a notebook.
- **Side by side, the transcript lost the syntax highlighting** the
  editor gives the script. In place, it keeps it: the results are
  comments, colored as comments, and the code around them is code.
- **Rerunning on every save is cheap enough.** 2.4's whole transcript
  takes 0.64 s, 0.44 s of it importing SymPy and equarium. On a scratch
  copy of 2.4 under `--watch`, changing `m1.t` to 3 s rewrote the file
  on save with `68.0*meter` and `27.0*meter/second`.
- **A bare string other than the docstring shows,** as in the REPL:
  `"abc"` then `#> 'abc'`. At first no bare string showed.
- **Built up step by step, 2.4 halves.** The user's incremental 2.4,
  `motorcycle = motorcycle.add(...)`, then `.known(...)` one by one, then
  parts as `part_a1 = part_a.want(m1.pos.x)`, reprinted the whole system
  after every step: 145 lines, the four equations ten times. With only
  what changed it's 80, and each result is that step's effect: the
  knowns line growing, `eliminate_zeros()` rewriting (1), the known
  `m1.t` making (1) ready, the want connecting 4 unknowns in 4
  equations. With `--full` it's the 145 lines, character for character.
- **The user's verdict on only what changed: not sure.** The whole
  system next to each step is reassuring context, and a name alone to
  see it is one more thing to do. That led to `--marked`: the length of
  `--full`, with each step's effect starred, `* knowns: …` or
  `* (1)  m01.dt = m1.t`. The user liked it best, and made it the
  default (2026-11-11).

## Open questions

- **Which rule.** The worksheet rule shows 2.4's results with no change
  to the script. The REPL rule is what Python users know.
- **Other objects.** `BookNotation` and a projectile's `Setup` still
  print by `repr`. They get short displays when an example shows one.
- **The examples' `__main__` blocks and result comments.** Drop them
  once a transcript is how an example's results are read?
- **A committed transcript**, beside `main.py`, for reading on GitHub.
  Markdown, since GitHub renders it and shows an `.html` file as source.
  Colors could come from GitHub's math, `\color{green}{x_0}`, which would
  also give the book's subscripts. That still has to be checked. A test
  could check that each committed transcript is what the script gives
  today, as `tests/test_sketch.py` does for `sketch.svg`. Its name
  mustn't look like `main_<slug>.py`, which the tests take as a version.
- **The editor.** VS Code reloads a file changed on disk when it has no
  unsaved edits. Is that smooth enough, or does it want an extension that
  runs the script on save and edits the buffer itself? An extension
  could also color the results again, knowns green and wants red.
- **Results that go stale.** A script with results in it can be edited
  without being run, and then its results are old. `--watch` keeps them
  current while it runs. For committed scripts, a test could check that
  the results in them are what they give today.
- **Slow scripts.** Every save runs the whole script. Running only from
  the first statement that changed is where notebooks' complexity starts.
- **Notebooks, for comparison.** Jupyter, and VS Code's Interactive
  window, which runs `# %%` cells of a plain `.py` file. Both use
  `_repr_pretty_` already. A `_repr_html_` would color them.
- **Long values.** A value prints whole, on as many lines as it has.
  Shorten long ones, as `reprlib` does?
- **Where it ends up.** A package of its own, which equarium doesn't
  depend on: equarium only has the display methods.
