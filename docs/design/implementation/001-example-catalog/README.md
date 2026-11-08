# 001 example catalog

**Status:** Catalog written (2026-11-08), and its seven questions for
007 answered by the user, each as recommended.

Every example and exercise in the old library's `examples/up/`, in one
file: the problem, the book's printed answers, the techniques, the old
scripts and their versions, the styles worth keeping, and what each
old script prints. One conversation writes it, from the
[checkpoint](checkpoint.md).

To write the catalog, give a new conversation this:

> Read `docs/design/implementation/001-example-catalog/checkpoint.md`
> in `~/journal/2026-11-06-equations/equarium.py`. If you've been told
> to read that file, it is the whole assignment.

## Why

The old library ([combine-equations.py](https://github.com/dharmatech/combine-equations.py),
at `~/src/combine-equations.py`) grew one University Physics example at
a time. Its 50 scripts in `examples/up/` solve 21 problems from
chapters 2 to 4, plus the derivations in `ch2/kinematic-equations/`.
Many problems have several versions. Some versions are drafts that a
later one replaced, and some are alternative solving styles the user
wants kept as teaching contrasts. Nothing records which is which, what
each script prints, or what the book's answer is. Several scripts
don't run as they are, and a few never reached the book's answer.

## What the catalog is for

- **The input to [002 core](../002-core/README.md)'s increment 007,**
  which copies the old physics code onto the new core and ports the
  examples. 007's checkpoint is written from the catalog. It needs:
  which examples to port, under which module names and slugs; each
  one's `BOOK` answers; the old scripts' formulas and numbers to
  compare against; whether misc.py's both-sides helpers come over; and
  whether kinematic-equations 005's derive-all search is ported.
- **The test list:** every answer the book prints for these problems,
  as a ported example's `BOOK` will check it.
- **The to-do list for the rebuild:** each problem's status in
  equarium, from "covered by a test" to "not yet ported", updated as
  later series port examples.
- **A record of the old library,** so the old repo never has to be
  read again to know what an example did.

## Files

- [checkpoint.md](checkpoint.md): the assignment.
- [catalog.md](catalog.md): the catalog.
