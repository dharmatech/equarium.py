# Step effects

A worksheet often builds one thing up a step at a time:

```python
motorcycle = motorcycle.known(m0.pos.x, 5 * meter)
motorcycle = motorcycle.known(m0.vel.x, 15 * meter / second)
```

Each step shows the whole value again, with the lines it changed
marked `* `:

```
# from 5.0 m east of a signpost
motorcycle = motorcycle.known(m0.pos.x, 5 * meter)
#>   (1)  m01.dt = -m0.t + m1.t
#>   (2)  m01.v_av.x = (-m0.pos.x + m1.pos.x)/m01.dt
#>   (3)  m01.a.x = (-m0.vel.x + m1.vel.x)/m01.dt
#>   (4)  m01.v_av.x = m0.vel.x/2 + m1.vel.x/2
#> * knowns: m0.t = 0, m0.pos.x = 5*meter
#>   wants: none
#>   connected: none
#>   ready: none
```

The source line says what the step did, and the star says what that
did to the value: here, a known added. After `eliminate_zeros()`, the
star is on equation (1), now `m01.dt = m1.t`.

The marks:

- `* `: a line that's new or different;
- `  `: a line that's the same;
- `- `: a line that's gone, shown where it was.

A step that changes nothing shows `(no change)`.

## When a step is marked

An assignment is marked when its right side starts from a name whose
value you've already seen, as `motorcycle` in
`motorcycle = motorcycle.known(...)` or `part_a = motorcycle.want(...)`,
and the new value is the same kind of thing and takes more than one
line. It's compared with what you saw last: a step hidden by `;` isn't
seen, so the next one shows both changes.

Anything else shows whole, without marks: a new value, one of another
kind, or a solution. To see a value whole at any point, write its name
alone on a line, `motorcycle`.

This works for any value, not only equarium's.

## Other ways to show a step

- `--changes` shows only the marked lines, which is shorter.
- `--full` shows every value whole, without marks.
