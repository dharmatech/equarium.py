"""Transcript mode: run a Python script one top-level statement at a time,
and print its source as written, with each statement's results under it.

    uv run python -m equarium.transcript path/to/script.py
    uv run python -m equarium.transcript -m package.module
    uv run python -m equarium.transcript --in-place path/to/script.py
    uv run python -m equarium.transcript --watch path/to/script.py

`--in-place` writes the results into the script itself, as comments,
and `--watch` does that again every time the script is saved, so that
the script is its own transcript in the editor.

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
  value, and neither `None` nor the script's docstring shows.

A value prints as IPython would print it: through its class's
`_repr_pretty_`, when it has one, and otherwise `repr`.

An error stops the run. Its traceback is the statement's last result.
The terminal transcript ends there, and in place, the lines that didn't
run stay as they are.

The `#> ` lines are the results, and belong to transcript mode: before
it runs a script, it drops them, so a script with results in it runs as
it would without them.
"""

import __future__
import argparse
import ast
import contextlib
import copy
import importlib.util
import io
import os
import re
import subprocess
import sys
import time
import tokenize
import traceback
import types
from collections.abc import Iterator, Sequence
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
    rest: str  # the lines after the last entry's; after an error, the lines not run
    failed: bool


def run(
    source: str,
    filename: str = "<script>",
    namespace: dict[str, object] | None = None,
    rule: Rule = "worksheet",
    file_lines: Sequence[int] | None = None,
) -> Transcript:
    """Run `source`, statement by statement, in `namespace`, and record
    each statement's results.

    `file_lines` is the line in the file of each line of `source`, when
    they differ, as they do once its results are stripped. Tracebacks and
    syntax errors then give the file's lines.
    """
    if namespace is None:
        namespace = {"__name__": "__main__"}
    try:
        tree = ast.parse(source, filename)
    except SyntaxError as e:
        if file_lines is not None and e.lineno is not None:
            e.lineno = _file_line(file_lines, e.lineno)
            e.end_lineno = None
        raise
    lines = _lines(source)
    ends = [node.end_lineno or node.lineno for node in tree.body]
    hidden = [_hidden(node, lines) for node in tree.body]
    if file_lines is not None:
        _renumber(tree, file_lines)
    entries: list[Entry] = []
    echoed = 0  # how many lines are in entries so far
    flags = 0
    for number, (node, end) in enumerate(zip(tree.body, ends)):
        text = "".join(lines[echoed:end])
        echoed = max(echoed, end)

        printed = io.StringIO()
        value: str | None = None
        try:
            with contextlib.redirect_stdout(printed):
                result = _execute(node, filename, namespace, flags)
                shows = rule == "worksheet" or isinstance(node, ast.Expr)
                if shows and result is not None and not hidden[number]:
                    if not (number == 0 and _is_docstring(node)):
                        value = show(result)
        except Exception as e:  # the script's error, recorded, not raised
            entries.append(Entry(text, printed.getvalue(), value, _traceback(e)))
            return Transcript(tuple(entries), "".join(lines[echoed:]), failed=True)
        entries.append(Entry(text, printed.getvalue(), value))
        flags |= _future_flags(node)
    return Transcript(tuple(entries), "".join(lines[echoed:]), failed=False)


def _lines(source: str) -> list[str]:
    """The source's lines, ending as Python's tokenizer ends them, at
    `\\n`. (`str.splitlines` also ends one at a form feed.)"""
    return io.StringIO(source).readlines()


def strip_results(source: str) -> str:
    """The script without its results: each line that is a comment `#> …`
    or `#>`, from the start of the line. A `#> ` line inside a string
    stays. A `SyntaxError` when the source doesn't tokenize."""
    return _stripped(source)[0]


def _stripped(source: str) -> tuple[str, list[int]]:
    """The script without its results, and the line in `source` of each
    of its lines."""
    results: set[int] = set()
    try:
        for token in tokenize.generate_tokens(io.StringIO(source).readline):
            if (
                token.type == tokenize.COMMENT
                and token.start[1] == 0
                and (token.string == MARK.rstrip() or token.string.startswith(MARK))
            ):
                results.add(token.start[0])
    except tokenize.TokenError as e:
        message, (line, column) = e.args
        raise SyntaxError(message, ("<script>", line, column + 1, None)) from e
    kept = [(n, line) for n, line in enumerate(_lines(source), 1) if n not in results]
    return "".join(line for _, line in kept), [n for n, _ in kept]


def _file_line(file_lines: Sequence[int], line: int) -> int:
    """The file's line for a line of the stripped source. A line past the
    end, as a syntax error at the end can have, is past the file's."""
    if 1 <= line <= len(file_lines):
        return file_lines[line - 1]
    return (file_lines[-1] if file_lines else 0) + line - len(file_lines)


def _renumber(tree: ast.AST, file_lines: Sequence[int]) -> None:
    """Give every node its line in the file."""
    for node in ast.walk(tree):
        for attribute in ("lineno", "end_lineno"):
            line = getattr(node, attribute, None)
            if isinstance(line, int):
                setattr(node, attribute, _file_line(file_lines, line))


def _execute(node: ast.stmt, filename: str, namespace: dict[str, object], flags: int) -> object:
    """Run the statement, and return its value: a bare expression's, or
    for an assignment, the value it bound, read back from its target.
    Anything else is None."""
    if isinstance(node, ast.Expr):
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


def _is_docstring(node: ast.stmt) -> bool:
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    )


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


WIDTH = 79  # IPython's pretty printer's


def show(value: object) -> str:
    """The value as IPython prints it: by its class's `_repr_pretty_`, when
    it has one, and otherwise by `repr`. A list, tuple, set or dict
    shows each item so, on one line when it fits in 79 characters, and
    otherwise one item to a line."""
    return _show(value, frozenset())


def _show(value: object, seen: frozenset[int]) -> str:
    kind = type(value)
    if kind in (list, tuple, set, frozenset, dict):
        return _container(value, seen)
    method = getattr(kind, "_repr_pretty_", None)
    if method is None:
        return repr(value)
    printer = TextPrinter()
    method(value, printer, False)
    return printer.getvalue()


def _container(value: object, seen: frozenset[int]) -> str:
    """A builtin container, as IPython prints it. Only exact builtins:
    a subclass, such as a named tuple, prints by its own `repr`."""
    if id(value) in seen:  # a container inside itself, shown as repr shows it
        return "{...}" if isinstance(value, dict) else "[...]"
    seen = seen | {id(value)}
    if isinstance(value, dict):
        items = [f"{_show(k, seen)}: {_show(v, seen)}" for k, v in value.items()]
        return _items("{", items, "}", "{}")
    if isinstance(value, list):
        return _items("[", [_show(item, seen) for item in value], "]", "[]")
    if isinstance(value, tuple):
        items = [_show(item, seen) for item in value]
        if len(items) == 1:
            return f"({items[0]},)"
        return _items("(", items, ")", "()")
    assert isinstance(value, set | frozenset)
    items = [_show(item, seen) for item in value]
    if isinstance(value, frozenset):
        return "frozenset()" if not items else f"frozenset({_items('{', items, '}', '')})"
    return _items("{", items, "}", "set()")


def _items(open: str, items: list[str], close: str, empty: str) -> str:
    if not items:
        return empty
    line = f"{open}{', '.join(items)}{close}"
    if len(line) <= WIDTH and "\n" not in line:
        return line
    indent = " " * len(open)
    lines = [item.replace("\n", "\n" + indent) for item in items]
    return open + (",\n" + indent).join(lines) + close


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


def render(transcript: Transcript, color: bool = True, unrun: bool = False) -> str:
    """The source as written, with each statement's results after its
    last line, marked `#> `.

    Without `color`, the results have no ANSI color codes. With `unrun`,
    the lines after an error, which didn't run, follow it.
    """
    out: list[str] = []
    for entry in transcript.entries:
        out.append(entry.source)
        if entry.source and not entry.source.endswith("\n"):
            out.append("\n")
        printed = entry.printed.removesuffix("\n") if entry.printed else None
        for result in (printed, entry.value, entry.error):
            if result is not None:
                out.extend(_marked(result if color else uncolored(result)))
    if not transcript.failed or unrun:
        out.append(transcript.rest)
    return "".join(out)


ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def uncolored(text: str) -> str:
    """The text without ANSI escape codes, such as colors."""
    return ANSI.sub("", text)


def _marked(text: str) -> list[str]:
    return [f"{MARK}{line}".rstrip() + "\n" for line in text.split("\n")]


# Running a script or a module


@dataclass(frozen=True)
class Script:
    """A script to run: its file, its package when it runs as a module,
    and the folder first on the path while it runs."""

    path: str
    package: str | None
    path_entry: str

    @staticmethod
    def file(path: str) -> Script:
        """A script file, run as `python path` runs it, with its folder
        first on the path."""
        path = os.path.abspath(path)
        return Script(path, None, os.path.dirname(path))

    @staticmethod
    def module(name: str) -> Script:
        """A module, run as `python -m name` runs it, with the current
        folder first on the path."""
        with _path_first(os.getcwd()):
            spec = importlib.util.find_spec(name)
        if spec is None or spec.origin is None or not spec.origin.endswith(".py"):
            raise SystemExit(f"transcript: no Python module named {name}")
        return Script(spec.origin, name.rpartition(".")[0], os.getcwd())

    def read(self) -> str:
        with open(self.path, encoding="utf-8") as f:
            return f.read()

    def run(self, content: str, rule: Rule = "worksheet") -> Transcript:
        """Run `content`, the file's, as this script, without the results
        it has in it."""
        source, file_lines = _stripped(content)
        with _as_main(self.path, self.package, self.path_entry) as namespace:
            return run(source, self.path, namespace, rule, file_lines)


def run_path(path: str, rule: Rule = "worksheet") -> Transcript:
    """Run a script file."""
    script = Script.file(path)
    return script.run(script.read(), rule)


def run_module(name: str, rule: Rule = "worksheet") -> Transcript:
    """Run a module."""
    script = Script.module(name)
    return script.run(script.read(), rule)


# In place, and on every save


def in_place(script: Script, rule: Rule = "worksheet") -> tuple[int, str]:
    """Run the script and write its results into it, without colors.

    The file is left as it is when it doesn't parse, or when it changed
    while the script ran. Returns the exit code, 1 after an error in the
    script and 2 when it doesn't parse, and what happened.
    """
    name = os.path.basename(script.path)
    before = script.read()
    try:
        transcript = script.run(before, rule)
    except SyntaxError as e:
        where = f"line {e.lineno}: " if e.lineno else ""
        return 2, f"{name}: doesn't parse, left as it is: {where}{e.msg}"
    after = render(transcript, color=False, unrun=True)
    code = 1 if transcript.failed else 0
    ran = "ran"
    if transcript.failed:
        error = transcript.entries[-1].error or ""
        ran = f"stopped at an error, {uncolored(error).splitlines()[-1]}"
    if script.read() != before:
        return code, f"{name}: changed while it ran, left as it is"
    if after == before:
        return code, f"{name}: {ran}, no change"
    with open(script.path, "w", encoding="utf-8") as f:
        f.write(after)
    return code, f"{name}: {ran}, results written"


def watch(script: Script, target: list[str], rule: Rule = "worksheet", interval: float = 0.2) -> None:
    """Write the script's results into it now, and again each time its
    code changes, until interrupted.

    Each run is a fresh `python -m equarium.transcript --in-place`, so
    the modules it imports are loaded fresh. A change to the results
    alone, such as the run's own writing, doesn't start another run.
    """
    command = [sys.executable, "-m", "equarium.transcript", "--in-place", *target]
    if rule == "repl":
        command.append("--repl")
    shown = os.path.relpath(script.path)
    if shown.startswith(".."):
        shown = script.path
    print(f"watching {shown}, Ctrl-C to stop", flush=True)
    # The file is read every time: its timestamp can miss a save made
    # right after the run's own write.
    last_content: str | None = None
    last_code: str | None = None
    try:
        while True:
            try:
                content = script.read()
            except FileNotFoundError:
                content = None  # an editor's save can replace the file
            if content is not None and content != last_content:
                last_content = content
                try:
                    code = strip_results(content)
                except SyntaxError:
                    code = content
                if code != last_code:
                    last_code = code
                    result = subprocess.run(command, capture_output=True, text=True)
                    stamp = time.strftime("%H:%M:%S")
                    print(f"{stamp} {(result.stdout + result.stderr).strip()}", flush=True)
            time.sleep(interval)
    except KeyboardInterrupt:
        pass


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
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--in-place",
        action="store_true",
        help="write the results into the script, as #> comments",
    )
    mode.add_argument(
        "--watch",
        action="store_true",
        help="write the results into the script now, and on every save",
    )
    args = parser.parse_args(argv)
    rule: Rule = "repl" if args.repl else "worksheet"
    if args.module is not None:
        script = Script.module(args.module)
        target = ["-m", args.module]
    else:
        script = Script.file(args.path)
        target = [args.path]
    if args.watch:
        watch(script, target, rule)
        return 0
    if args.in_place:
        code, report = in_place(script, rule)
        print(report)
        return code
    transcript = script.run(script.read(), rule)
    sys.stdout.write(render(transcript))
    return 1 if transcript.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
