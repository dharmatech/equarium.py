# Transcript mode

Transcript mode runs a Python script and shows each statement's result
right under it, as a `#> ` comment, like a worksheet: every step, and
next to it what it gave.

```python
x = 5
#> 5
x * 2
#> 10

names = ["Ada", "Grace", "Barbara"]
#> ['Ada', 'Grace', 'Barbara']
[name.upper() for name in names]
#> ['ADA', 'GRACE', 'BARBARA']
```

It works with any Python script. Those lines are from
[`basics.py`](basics.py), beside this page, which has no equarium in it. equarium's systems, solutions
and book checks show up readably too.

## Run it

Print a script's transcript in the terminal, from a file or from a
module, as `python -m` runs one:

```bash
uv run python -m equarium.transcript docs/transcripts/basics.py
uv run python -m equarium.transcript -m examples.up_15e.ch02.examples.n04.main
```

Or write the results into the script itself, once, or every time you
save it:

```bash
uv run python -m equarium.transcript --in-place docs/transcripts/basics.py
uv run python -m equarium.transcript --watch docs/transcripts/basics.py
```

With `--watch` running in a terminal, edit the script in VS Code, save,
and the results appear under each line.

A transcript is still valid Python, since the results are comments. The
`#> ` lines belong to transcript mode: it drops them before every run
and writes them again. So don't start a comment of your own with `#> `.

## More

- [What shows](what-shows.md): which statements show a result, how to
  hide one, and how values print.
- [Step effects](step-effects.md): how a step that changes a value shows
  what it changed.
- [In place and on every save](in-place.md): `--in-place` and
  `--watch`, and what keeps your code safe.
- [Influences and related work](related-work.md): where the ideas came
  from, and similar tools.
- [The design record](../design/implementation/006-transcript-mode/README.md):
  why it works the way it does, and what's still open.
