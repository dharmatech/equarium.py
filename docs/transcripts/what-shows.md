# What shows

Transcript mode runs a script one top-level statement at a time. After
each statement's last line, it shows that statement's results, each
line marked `#> `.

## Which statements show a result

- **A bare expression** shows its value: `x * 2` then `#> 10`.
- **An assignment** shows the value it gave its target:
  `y = x**2 + 1` then `#> 26`. For `a, b = 1, 2`, it's `(1, 2)`.
- **Anything a statement prints** shows too, such as `print("y is", y)`
  then `#> y is 26`, including what a loop or an `if` prints.
- **A `;` ending the line hides the value:** `z = y - x;` shows nothing.
  The statement still runs.
- **`None` never shows,** and neither does the script's docstring.

That's the worksheet rule, the default. With `--repl`, an assignment
shows nothing, as in Python's REPL and Jupyter, and only bare
expressions and printed output show.

## How values print

A value prints as IPython would print it: by its class's
`_repr_pretty_` method if it has one, and otherwise by `repr`. A list,
tuple, set or dict shows on one line when it fits in 79 characters, and
otherwise one item to a line.

So a library can make its objects read well in a transcript by giving
them `_repr_pretty_`, the same method IPython uses. equarium does:

- **A `System`** prints what `show()` prints: its equations, knowns,
  wants, connected unknowns and ready equations.
- **A `Solution`** prints each want's formula, then its number:

  ```
  sol_a1 = part_a1.solve()
  #> m1.pos.x = m0.pos.x + m0.vel.x*m1.t + m01.a.x*m1.t**2/2
  #> m1.pos.x = 43.0*meter
  ```
- **The physics model** prints briefly: a particle as
  `particle m (x): m0, m1`, a state as its name, `m0`, an edge as
  `m01: m0 → m1`, and an event as `event meet: m1, q1`.
- **A book check,** an `Answer` or a `Formula`, prints `✓` or `✗` and
  what it compared, so a `BOOK` list reads as the worksheet's answers:

  ```
  #> [✓ m1.pos.x: book 43 meter, found 43.0*meter,
  #>  ✓ m1.vel.x: book 23 meter/second, found 23.0*meter/second]
  ```

In the terminal, knowns show in green and wants in red, as `show()`
prints them. Written into a file, the results have no colors.

## Errors

An error stops the script. Its traceback is the last result, under the
statement that raised it, and its line numbers are the file's. The
terminal transcript ends there. Written into the file, the lines after
it stay as they are, without results.
