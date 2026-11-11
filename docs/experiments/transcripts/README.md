# Transcript mode (experiment)

**Status:** first prototype, the terminal transcript (2026-11-11). This is
an experiment, not a series. It takes a series number only if it's
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
`equarium-transcript/`, so the physics branch's review isn't disturbed.

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
    line hides it, as in Mathematica and IPython, and `None` and bare
    strings (docstrings) never show;
  - an error's traceback, without the module's own frames. The
    transcript ends there.

  A value prints as IPython prints it: by its class's `_repr_pretty_`,
  and otherwise by `repr`. The module imports nothing from equarium, and
  a test checks that, so it can move to a package of its own. It uses
  only the standard library.
- **`System._repr_pretty_` and `Solution._repr_pretty_`.** They print
  what `show()` prints: knowns green, wants red. IPython uses the same
  method, so a system or a solution also prints readably there.
- **`basics.py`**, beside these notes: a plain Python script with no
  equarium in it.
- **`tests/test_transcript.py`.** The rules on small scripts, and 2.4.
  Without its `#> ` lines, a transcript is the script.

Run it on a file, or on a module as `python -m` does:

```bash
uv run python -m equarium.transcript docs/experiments/transcripts/basics.py
uv run python -m equarium.transcript -m examples.up_15e.ch02.examples.n04.main
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
- **The REPL rule on 2.4's `main.py` shows nothing from its
  statements.** All 53 result lines come from the `__main__` block's
  prints. Under that rule, an example would show a result with a bare
  name on its own line, `sol_a`, as in a notebook.

## Open questions

- **Which rule.** The worksheet rule shows 2.4's results with no change
  to the script. The REPL rule is what Python users know.
- **Quiet objects.** A `;` after each, or short reprs for `Particle`,
  `State`, `Edge` and `Answer`, such as `Particle m: 2 states, on x`?
  Short reprs change the physics layer and `examples/answers.py`.
- **The examples' `__main__` blocks and result comments.** Drop them
  once a transcript is how an example's results are read?
- **A committed transcript**, beside `main.py`, for reading on GitHub.
  Markdown, since GitHub renders it and shows an `.html` file as source.
  Colors could come from GitHub's math, `\color{green}{x_0}`, which would
  also give the book's subscripts. That still has to be checked. A test
  could check that each committed transcript is what the script gives
  today, as `tests/test_sketch.py` does for `sketch.svg`. Its name
  mustn't look like `main_<slug>.py`, which the tests take as a version.
- **A live view.** A watch mode that rewrites the Markdown or HTML on
  every save, beside the editor in VS Code's preview, before any
  extension.
- **Notebooks, for comparison.** Jupyter, and VS Code's Interactive
  window, which runs `# %%` cells of a plain `.py` file. Both use
  `_repr_pretty_` already. A `_repr_html_` would color them.
- **Long values.** A value prints whole, on as many lines as it has.
  Shorten long ones, as `reprlib` does?
- **Where it ends up.** A package of its own, which equarium doesn't
  depend on: equarium only has the display methods.
