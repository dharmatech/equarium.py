"""Transcript mode: run a Python script one top-level statement at a time,
and print its source as written, with each statement's results under it.

    uv run python -m equarium.transcript path/to/script.py
    uv run python -m equarium.transcript -m package.module

An experiment: see `docs/experiments/transcripts/`. This module imports
nothing from equarium, so it works for any Python script, and can move to
a package of its own.

The script runs as `python` would run it, as `__main__`. Every source
line is printed, comments and blank lines too, and a statement's results
follow its last line, each line marked `#> `. So a transcript without
its `#> ` lines is the script. Its results are:

- what it printed;
- its value. Under the worksheet rule, the default, a bare expression
  shows its value and an assignment shows the value it bound, as in
  Mathematica. Under the REPL rule, `--repl`, only a bare expression
  does, as in Python's REPL. Either way, a `;` ending the line hides the
  value, `None` never shows, and neither does a bare string, which is a
  docstring or a comment.

A value prints as IPython would print it: through its class's
`_repr_pretty_`, when it has one, and otherwise `repr`.

An error stops the run. Its traceback is the statement's last result,
and the transcript ends there.
"""

import __future__
import argparse
import ast
import contextlib
import copy
import importlib.util
import io
import os
import sys
import traceback
import types
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Literal

type Rule = Literal["worksheet", "repl"]

MARK = "#> "


@dataclass(frozen=True)
class Entry:
    """One top-level statement: the source lines it adds, through its
    last line, and its results.

    `source` starts after the previous entry's last line, so it holds any
    comments and blank lines before the statement. It's empty for a
    statement that shares a line with the one before it.
    """

    source: str
    printed: str
    value: str | None
    error: str | None = None


@dataclass(frozen=True)
class Transcript:
    entries: tuple[Entry, ...]
    rest: str  # the lines after the last statement's
    failed: bool


def run(
    source: str,
    filename: str = "<script>",
    namespace: dict[str, object] | None = None,
    rule: Rule = "worksheet",
) -> Transcript:
    """Run `source`, statement by statement, in `namespace`, and record
    each statement's results."""
    if namespace is None:
        namespace = {"__name__": "__main__"}
    tree = ast.parse(source, filename)
    lines = source.splitlines(keepends=True)
    entries: list[Entry] = []
    echoed = 0  # how many lines are in entries so far
    flags = 0
    for node in tree.body:
        end = node.end_lineno or node.lineno
        text = "".join(lines[echoed:end])
        echoed = max(echoed, end)

        printed = io.StringIO()
        value: str | None = None
        try:
            with contextlib.redirect_stdout(printed):
                result = _execute(node, filename, namespace, flags)
                if rule == "worksheet" or isinstance(node, ast.Expr):
                    if result is not None and not _hidden(node, lines):
                        value = show(result)
        except Exception as e:  # the script's error, recorded, not raised
            # The lines after it didn't run, so they aren't shown.
            entries.append(Entry(text, printed.getvalue(), value, _traceback(e)))
            return Transcript(tuple(entries), "", failed=True)
        entries.append(Entry(text, printed.getvalue(), value))
        flags |= _future_flags(node)
    return Transcript(tuple(entries), "".join(lines[echoed:]), failed=False)


def _execute(node: ast.stmt, filename: str, namespace: dict[str, object], flags: int) -> object:
    """Run the statement, and return its value: a bare expression's, or
    for an assignment, the value it bound, read back from its target.
    Anything else is None."""
    if isinstance(node, ast.Expr):
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            exec(_compile(ast.Module([node], []), filename, "exec", flags), namespace)
            return None
        return eval(_compile(ast.Expression(node.value), filename, "eval", flags), namespace)
    exec(_compile(ast.Module([node], []), filename, "exec", flags), namespace)
    match node:
        case ast.Assign(targets=[target, *_]) | ast.AugAssign(target=target):
            pass
        case ast.AnnAssign(target=target, value=value) if value is not None:
            pass
        case _:
            return None
    load = ast.Expression(_as_load(target))
    return eval(_compile(load, filename, "eval", flags), namespace)


def _compile(tree: ast.Module | ast.Expression, filename: str, mode: str, flags: int) -> types.CodeType:
    return compile(tree, filename, mode, flags=flags, dont_inherit=True)


def _as_load(target: ast.expr) -> ast.expr:
    """The target, as an expression that reads it: `m0, m1` for
    `m0, m1 = m.states`."""
    target = copy.deepcopy(target)
    for node in ast.walk(target):
        if isinstance(node, ast.Name | ast.Attribute | ast.Subscript | ast.Starred | ast.Tuple | ast.List):
            node.ctx = ast.Load()
    return target


def _hidden(node: ast.stmt, lines: list[str]) -> bool:
    """Whether a `;` ends the statement's line: `x = 5;`, or `x = 5;  # a
    comment`. A `;` before another statement, as in `x = 5; y = 6`, only
    separates them."""
    if node.end_lineno is None or node.end_col_offset is None:
        return False
    line = lines[node.end_lineno - 1]
    # Column offsets count UTF-8 bytes.
    after = line.encode()[node.end_col_offset :].decode().strip()
    if not after.startswith(";"):
        return False
    after = after[1:].strip()
    return after == "" or after.startswith("#")


def _future_flags(node: ast.stmt) -> int:
    """The compiler flags of a `from __future__ import ...`, which apply to
    the statements after it."""
    if not (isinstance(node, ast.ImportFrom) and node.module == "__future__"):
        return 0
    flags = 0
    for alias in node.names:
        flags |= getattr(getattr(__future__, alias.name, None), "compiler_flag", 0)
    return flags


def _traceback(error: BaseException) -> str:
    """The traceback, without this module's frames."""
    exception = traceback.TracebackException.from_exception(error)
    here = os.path.abspath(__file__)
    exception.stack = traceback.StackSummary.from_list(
        [frame for frame in exception.stack if os.path.abspath(frame.filename) != here]
    )
    return "".join(exception.format()).rstrip("\n")


# Values as text


def show(value: object) -> str:
    """The value as IPython prints it: by its class's `_repr_pretty_`, when
    it has one, and otherwise by `repr`."""
    method = getattr(type(value), "_repr_pretty_", None)
    if method is None:
        return repr(value)
    printer = TextPrinter()
    method(value, printer, False)
    return printer.getvalue()


class TextPrinter:
    """The parts of IPython's pretty printer that a `_repr_pretty_` calls,
    printing on one line, without IPython."""

    def __init__(self) -> None:
        self._parts: list[str] = []

    def text(self, obj: str) -> None:
        self._parts.append(obj)

    def breakable(self, sep: str = " ") -> None:
        self._parts.append(sep)

    def pretty(self, obj: object) -> None:
        self._parts.append(show(obj))

    def begin_group(self, indent: int = 0, open: str = "") -> None:
        self._parts.append(open)

    def end_group(self, dedent: int = 0, close: str = "") -> None:
        self._parts.append(close)

    @contextlib.contextmanager
    def group(self, indent: int = 0, open: str = "", close: str = "") -> Iterator[None]:
        self.begin_group(indent, open)
        yield
        self.end_group(indent, close)

    @contextlib.contextmanager
    def indent(self, indent: int) -> Iterator[None]:
        yield

    def getvalue(self) -> str:
        return "".join(self._parts)


# Output


def render(transcript: Transcript) -> str:
    """The source as written, with each statement's results after its
    last line, marked `#> `."""
    out: list[str] = []
    for entry in transcript.entries:
        out.append(entry.source)
        if entry.source and not entry.source.endswith("\n"):
            out.append("\n")
        printed = entry.printed.removesuffix("\n") if entry.printed else None
        for result in (printed, entry.value, entry.error):
            if result is not None:
                out.extend(_marked(result))
    out.append(transcript.rest)
    return "".join(out)


def _marked(text: str) -> list[str]:
    return [f"{MARK}{line}".rstrip() + "\n" for line in text.split("\n")]


# Running a script or a module


def run_path(path: str, rule: Rule = "worksheet") -> Transcript:
    """Run a script file as `python path` would, with its folder first on
    the path."""
    path = os.path.abspath(path)
    with open(path, encoding="utf-8") as f:
        source = f.read()
    with _as_main(path, package=None, path_entry=os.path.dirname(path)) as namespace:
        return run(source, path, namespace, rule)


def run_module(name: str, rule: Rule = "worksheet") -> Transcript:
    """Run a module as `python -m name` would, with the current folder
    first on the path."""
    with _path_first(os.getcwd()):
        spec = importlib.util.find_spec(name)
    if spec is None or spec.origin is None or not spec.origin.endswith(".py"):
        raise SystemExit(f"transcript: no Python module named {name}")
    with open(spec.origin, encoding="utf-8") as f:
        source = f.read()
    package = name.rpartition(".")[0]
    with _as_main(spec.origin, package=package, path_entry=os.getcwd()) as namespace:
        return run(source, spec.origin, namespace, rule)


@contextlib.contextmanager
def _as_main(path: str, package: str | None, path_entry: str) -> Iterator[dict[str, object]]:
    """A fresh `__main__` module for the script, in `sys.modules` while it
    runs, as `runpy` does, so that pickling and dataclasses find it."""
    module = types.ModuleType("__main__")
    module.__file__ = path
    module.__package__ = package
    saved_main = sys.modules.get("__main__")
    saved_argv = sys.argv
    sys.modules["__main__"] = module
    sys.argv = [path]
    try:
        with _path_first(path_entry):
            yield module.__dict__
    finally:
        sys.argv = saved_argv
        if saved_main is not None:
            sys.modules["__main__"] = saved_main


@contextlib.contextmanager
def _path_first(entry: str) -> Iterator[None]:
    sys.path.insert(0, entry)
    try:
        yield
    finally:
        sys.path.remove(entry)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m equarium.transcript",
        description="Print a Python script's source with each statement's results under it.",
    )
    where = parser.add_mutually_exclusive_group(required=True)
    where.add_argument("path", nargs="?", help="a script to run")
    where.add_argument("-m", dest="module", help="a module to run, as python -m does")
    parser.add_argument(
        "--repl",
        action="store_true",
        help="show only bare expressions' values, as Python's REPL does",
    )
    args = parser.parse_args(argv)
    rule: Rule = "repl" if args.repl else "worksheet"
    if args.module is not None:
        transcript = run_module(args.module, rule)
    else:
        transcript = run_path(args.path, rule)
    sys.stdout.write(render(transcript))
    return 1 if transcript.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
