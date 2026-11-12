# Transcript mode: influences and related work

Transcript mode runs a Python script and writes each statement's results
under it as `#> ` comments, once or on every save. The
[transcript notes](README.md) say how it works. Few of its ideas are
new, and this page credits where they came from and points to similar
tools.

## Influences

What we drew on knowingly while designing it, in November 2026:

- **[reprex](https://reprex.tidyverse.org/)**, for R, by Jennifer Bryan.
  It runs code and renders it with its output as `#>` comment lines, so
  the result can be pasted and run again. Our `#> ` mark is its
  convention.
- **Mathematica.** An input shows its output, an assignment's too,
  unless a `;` ends it: the
  [output is then not printed](https://reference.wolfram.com/language/ref/CompoundExpression.html).
  That's our worksheet rule.
- **[IPython](https://ipython.org/).** A `;` ending a line hides its
  value there too, and an object prints itself through
  [`_repr_pretty_`](https://ipython.readthedocs.io/en/stable/api/generated/IPython.lib.pretty.html).
  Transcript mode prints values the same way, so a library that looks
  good in IPython looks good in a transcript. equarium's systems and
  solutions take part that way.
- **[seeing_is_believing](https://github.com/JoshCheek/seeing_is_believing)**,
  for Ruby. It runs a program and
  [prints it back](https://github.com/JoshCheek/seeing_is_believing/wiki/Command-Line-Usage)
  with each line's result as a `# =>` comment at the end of the line.
  It doesn't write the file: its
  [editor integrations](https://github.com/JoshCheek/seeing_is_believing/wiki/Editor-Integration)
  replace the text being edited with that output, and `--clean` takes
  the comments out again. Results that live in the code itself come
  from there. `--in-place` and `--watch` go one step further and write
  them into the file.

## Related work

Found after transcript mode was built, in a search on 2026-11-11:

- **[reprexlite](https://jayqi.github.io/reprexlite/stable/)**, the
  closest. It runs Python code and shows its results as `#>` comments
  below the lines that made them, so the output can be pasted and run
  again: the same idea and the same format as ours, from the same
  parent, R's reprex. It's made for sharing a snippet on GitHub or Stack
  Overflow, so it takes code from your text editor, a string, or an
  IPython or Jupyter cell, and in its examples an assignment shows
  nothing, as in Python's REPL. To share a snippet, use reprexlite.

  We found it after building transcript mode. But transcript mode was
  designed together with an AI assistant, whose training data may well
  include reprexlite, so reprexlite may have shaped it too, indirectly.
- **[reprexpy](https://github.com/crew102/reprexpy)**, a Python port of
  reprex closer to the original's workflow: it runs the code in a
  Jupyter kernel and works through the clipboard.
- **[AREPL](https://github.com/Almenon/arepl-vscode)**, a VS Code
  extension that runs Python as you type and shows the variables in a
  side panel.
- **[live-py-plugin](https://github.com/donkirkby/live-py-plugin)** and
  its command-line tool, Space Tracer: each line's values in a column
  beside the code, in PyCharm, Emacs, Sublime Text or the browser.
- **[marimo](https://marimo.io/)**, reactive notebooks kept as `.py`
  files, with their results outside the file.
- **VS Code's Interactive window**, which runs the `# %%` cells of a
  plain `.py` file, Jupytext's
  [percent format](https://jupytext.readthedocs.io/en/stable/formats-scripts.html),
  with the results in a window of their own.
- **[inline-snapshot](https://github.com/15r10nk/inline-snapshot)**,
  which fills expected values into `snapshot()` calls in test code: the
  same idea of writing results into the source, for tests.
- **[doctest](https://docs.python.org/3/library/doctest.html)**, in
  Python's standard library: examples kept in docstrings with their
  output, and checked. The output is written by hand.

As far as we found, what transcript mode adds is the combination:
results kept in the plain script itself and current on every save, the
worksheet rule in Python, and each step's effect marked against the
value before it.
