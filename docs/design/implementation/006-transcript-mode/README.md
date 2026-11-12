# 006 transcript mode

**Status:** Done (2026-11-12): kept as a feature of equarium. It was
built on 2026-11-11 as an experiment, over several conversations, and
merged into `master`. On 2026-11-12 it was kept, and its docs were split
into a [user guide](../../../transcripts/README.md) and this record.

This is the design record: why, what was decided and why, what the work
found, and what's still open. How to use transcript mode is in the
guide. Where its ideas came from is in
[influences and related work](../../../transcripts/related-work.md).

## Why

On paper, a student's worksheet keeps each step next to its result, and
they can read it back later. A script keeps only the steps: its results
show up when it runs, apart from the code, or in comments typed by hand
that nothing checks. Transcript mode runs a script and shows its source
as written, with each statement's results under it: the worksheet's
readability, without leaving a plain `.py` file and the editor.

## Decisions *(user)*

- **Any Python script, not only equarium's,** built pragmatically, with
  no design for extension ahead of need. So the engine knows nothing
  about equarium, and a library takes part through IPython's display
  methods, which many libraries already have, not through a plugin
  system of ours.
- **One file.** Seen beside the script in VS Code, the terminal
  transcript lost the editor's syntax highlighting. So the results are
  written into the script itself, once or on every save.
- **The marked display is the default** for a step's effect: the whole
  value, with its changes starred. Of the three displays, the user liked
  it best.
- **Kept, not an experiment** (2026-11-12), with a user guide in
  `docs/transcripts/` and this record.

## Decisions made in the work

- **The `#> ` mark,** R's reprex convention. A transcript stays valid
  Python, and the results are comments.
- **Old results are dropped before each run:** every line that is a
  `#> ` comment from the start of the line, found by `tokenize`, so one
  inside a string stays. The script's statements are then renumbered to
  the file's lines, so tracebacks and syntax errors point at the lines
  the reader sees.
- **The worksheet rule by default:** a bare expression shows its value,
  and so does an assignment, read back from its target, as in
  Mathematica. `--repl` shows only bare expressions, as Python's REPL
  does. Either way a `;` ending the line hides the value, as in
  Mathematica and IPython, and neither `None` nor the script's docstring
  shows. Other bare strings show, as in the REPL.
- **A value prints as IPython prints it:** by its class's
  `_repr_pretty_`, and otherwise by `repr`. A list, tuple, set or dict
  shows each item so, on one line when it fits in 79 characters, and
  otherwise one item to a line.
- **equarium's objects print through `_repr_pretty_`,** so `repr()` and
  test messages don't change. A `System` and a `Solution` print what
  `show()` prints. The model and the book get short displays: a
  `Particle` `particle m (x): m0, m1`, a `State` its name, an `Edge`
  `m01: m0 → m1`, an `Event` `event meet: m1, q1`, and an `Answer` or a
  `Formula` its check against the book, `✓` or `✗`.
- **An error stops the run.** Its traceback, without the engine's own
  frames, is the statement's last result. The terminal transcript ends
  there, and in place, the lines that didn't run stay as they are.
- **In place, the file is written only when it's safe:** not when it
  doesn't parse, as in the middle of an edit, and not when it changed
  while it ran, so a save made meanwhile isn't overwritten. The results
  in the file have no colors.
- **`--watch` runs each save in a fresh Python,** so changes to imported
  modules take effect, and it compares the file's contents, not its
  timestamp, which can miss a save made right after its own write. A
  change to the results alone, such as its own writing, doesn't start
  another run.
- **A step's effect is marked against what the reader last saw.** An
  assignment whose right side starts from a name already shown, by
  calls, attributes and subscripts, and whose new value is of the same
  type and takes more than one line, shows each line marked `* ` new or
  different, `  ` the same, or `- ` gone, in its place. Lines are
  compared without their colors. Where a run of lines is replaced by as
  many, each changed in place; where the counts differ, `difflib.ndiff`
  pairs like lines. A step that changes nothing shows `(no change)`.
  Anything else shows whole, and so does a name alone on a line. A step
  hidden by `;` isn't seen, so the next shows both.
- **The engine imports nothing from equarium,** and a test checks that,
  so it can become a package of its own. It uses only the standard
  library.

## What there is

- `src/equarium/transcript.py`: the engine and its command line.
- `_repr_pretty_` on `System` and `Solution`, and on the physics model's
  and the book's objects.
- `tests/test_transcript.py`: the rules on small scripts, in place, the
  watch, the step effects, and 2.4. Without its `#> ` lines, a
  transcript is the script, and `docs/transcripts/basics.py` holds its
  current results.
- `docs/transcripts/`: the guide, `basics.py` and the related work.

## What the work found

- **Plain Python works unchanged.** `basics.py` reads like a worksheet:
  `x * 2` then `#> 10`.
- **2.4's `main.py`, before the short displays:** each system and
  solution showed, in color, right under the line that made it. But
  `m`, `m0, m1` and `m01` printed dataclass reprs, `BOOK` printed one
  line of 2,967 characters, the `__main__` block printed every result
  again, and the result comments typed by hand sat right under the real
  results. The transcript was 163 lines. A copy with a `;` after the
  model, no `__main__` block and no result comments was 66.
- **With the short displays,** 2.4's model and book read in a line each,
  and `BOOK` reads as the worksheet's answer check, one line to an
  answer.
- **The REPL rule on 2.4's `main.py` shows nothing from its
  statements.** All 53 result lines came from the `__main__` block's
  prints.
- **In place keeps the syntax highlighting:** the results are comments,
  colored as comments.
- **Rerunning on every save is cheap enough.** 2.4's whole transcript
  takes 0.64 s, 0.44 s of it importing SymPy and equarium. Under
  `--watch`, changing `m1.t` to 3 s rewrote the file on save with
  `68.0*meter` and `27.0*meter/second`.
- **Built up step by step, 2.4 halves.** The user's incremental 2.4
  reprinted the whole system after every step: 145 lines, the four
  equations ten times. With only what changed it's 80, and each result
  is that step's effect. The user wasn't sure about only what changed:
  the whole system next to each step is reassuring context. That led to
  the marked display, the length of the whole, with each step's effect
  starred.
- **VS Code reloads a file changed on disk only while its file watching
  works.** On Linux that needs inotify instances, 128 per user by
  default, and ~65 idle Claude Code sessions and an old VS Code had used
  them up. Restarting them freed them, and the user raised the limit to
  1024. The guide's [in-place page](../../../transcripts/in-place.md)
  says how.

## Open questions

- **Which rule.** The worksheet rule shows 2.4's results with no change
  to the script. The REPL rule is what Python users know.
- **Other objects.** `BookNotation` and a projectile's `Setup` still
  print by `repr`. They get short displays when an example shows one.
- **The examples' `__main__` blocks and result comments.** Drop them
  once a transcript is how an example's results are read?
- **A committed transcript** beside `main.py`, for reading on GitHub:
  Markdown, since GitHub renders it and shows an `.html` file as source.
  Colors could come from GitHub's math, `\color{green}{x_0}`, which would
  also give the book's subscripts. That still has to be checked. Its
  name mustn't look like `main_<slug>.py`, which the tests take as a
  version.
- **The editor.** Is VS Code's reload on change smooth enough, or does
  it want an extension that runs the script on save and edits the buffer
  itself? An extension could also color the results again.
- **Results that go stale.** A script with results in it can be edited
  without being run. A test could check that a committed script's
  results are what it gives today, as one does for `basics.py`.
- **Slow scripts.** Every save runs the whole script. Running only from
  the first statement that changed is where notebooks' complexity
  starts.
- **Notebooks, for comparison.** Jupyter, and VS Code's Interactive
  window, which runs `# %%` cells of a plain `.py` file. Both use
  `_repr_pretty_` already. A `_repr_html_` would color them.
- **Long values.** A value prints whole, on as many lines as it has.
  Shorten long ones, as `reprlib` does?
- **Where it ends up.** A package of its own, which equarium doesn't
  depend on: equarium only has the display methods.

## History

All on 2026-11-11 unless dated:

- The prototype, the terminal transcript, `891e8ee`. In place and on
  every save, `7d72e0d`. Merged into the physics branch in `a286c84`,
  and with it into `master` in `d25dd74`, tagged `v0.2.0`.
- The short displays for the model and the book, merged in `aef4385`.
- Each step's effect, `ba5c69c`, with the marked display made the
  default in `2b0c4c8`, merged in `8f5782e`.
- 2026-11-12: kept, with its docs moved from `docs/experiments/` to
  `docs/transcripts/` and the related work written, `3958237`; then
  split into the guide and this record.
