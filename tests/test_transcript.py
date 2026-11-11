"""Transcript mode, `equarium.transcript`: plain Python first, then
Example 2.4."""

import ast
import re
import subprocess
import sys
import time
from collections.abc import Callable
from pathlib import Path
from textwrap import dedent

import pytest

from equarium import transcript
from equarium.transcript import (
    Script,
    Transcript,
    in_place,
    render,
    run,
    run_module,
    run_path,
    changed_lines,
    strip_results,
    uncolored,
)

ANSI = re.compile(r"\x1b\[[0-9;]*m")
BASICS = Path("docs/experiments/transcripts/basics.py")
N04 = Path("examples/up_15e/ch02/examples/n04/main.py")


def transcribe(source: str, rule: transcript.Rule = "worksheet") -> str:
    return render(run(dedent(source), rule=rule))


def without_results(text: str) -> str:
    return "".join(
        line
        for line in text.splitlines(keepends=True)
        if not (line.rstrip("\n") == "#>" or line.startswith("#> "))
    )


# Plain Python


def test_the_worksheet_rule_shows_expressions_and_assignments() -> None:
    assert transcribe(
        """\
        x = 5
        x * 2
        print("x is", x)
        """
    ) == dedent(
        """\
        x = 5
        #> 5
        x * 2
        #> 10
        print("x is", x)
        #> x is 5
        """
    )


def test_the_repl_rule_shows_expressions_only() -> None:
    assert transcribe("x = 5\nx * 2\n", rule="repl") == "x = 5\nx * 2\n#> 10\n"


def test_comments_and_blank_lines_stay_where_they_are() -> None:
    assert transcribe(
        """\
        # The start.

        x = 5  # five

        # The end.
        """
    ) == dedent(
        """\
        # The start.

        x = 5  # five
        #> 5

        # The end.
        """
    )


def test_a_semicolon_ending_the_line_hides_the_value() -> None:
    assert transcribe("x = 5;\nx;  # hidden\nx\n") == "x = 5;\nx;  # hidden\nx\n#> 5\n"


def test_a_semicolon_between_statements_only_separates_them() -> None:
    assert transcribe("x = 5; y = 6\n") == "x = 5; y = 6\n#> 5\n#> 6\n"


def test_a_statement_over_several_lines_shows_after_its_last() -> None:
    assert transcribe("total = (\n    1\n    + 2\n)\n") == "total = (\n    1\n    + 2\n)\n#> 3\n"


def test_none_and_the_docstring_dont_show() -> None:
    assert transcribe('"""A docstring."""\nprint()\nNone\n"abc"\n') == (
        '"""A docstring."""\nprint()\n#>\nNone\n"abc"\n#> \'abc\'\n'
    )


def test_an_assignment_shows_what_its_target_holds() -> None:
    assert transcribe("a, b = 1, 2\nb += 10\nd = {}\nd['k'] = a\n") == dedent(
        """\
        a, b = 1, 2
        #> (1, 2)
        b += 10
        #> 12
        d = {}
        #> {}
        d['k'] = a
        #> 1
        """
    )


def test_an_annotation_alone_shows_nothing() -> None:
    assert transcribe("x: int\nx: int = 3\n") == "x: int\nx: int = 3\n#> 3\n"


def test_a_compound_statement_shows_what_it_printed() -> None:
    assert transcribe(
        """\
        for i in range(2):
            print(i)
        if __name__ == "__main__":
            print("main")
        """
    ) == dedent(
        """\
        for i in range(2):
            print(i)
        #> 0
        #> 1
        if __name__ == "__main__":
            print("main")
        #> main
        """
    )


def test_an_error_ends_the_transcript() -> None:
    result = run("x = 1\n1 / 0\ny = 2\n", filename="script.py")
    assert result.failed
    text = render(result)
    assert text.startswith("x = 1\n#> 1\n1 / 0\n#> Traceback (most recent call last):\n")
    assert text.endswith("#> ZeroDivisionError: division by zero\n")
    assert 'File "script.py", line 2' in text
    assert "transcript.py" not in text
    assert "y = 2" not in text


def test_a_value_prints_by_its_repr_pretty() -> None:
    class Pretty:
        def _repr_pretty_(self, p: transcript.TextPrinter, cycle: bool) -> None:
            p.text("pretty")

    assert transcript.show(Pretty()) == "pretty"
    assert transcript.show("text") == "'text'"


def test_a_container_shows_its_items_as_ipython_does() -> None:
    class Pretty:
        def _repr_pretty_(self, p: transcript.TextPrinter, cycle: bool) -> None:
            p.text("pretty")

    assert transcript.show([Pretty(), 1, "a"]) == "[pretty, 1, 'a']"
    assert transcript.show((Pretty(),)) == "(pretty,)"
    assert transcript.show({"k": Pretty()}) == "{'k': pretty}"
    assert transcript.show({Pretty()}) == "{pretty}"
    assert transcript.show(frozenset({1})) == "frozenset({1})"
    empty: list[object] = [[], (), {}, set(), frozenset()]
    assert transcript.show(empty) == "[[], (), {}, set(), frozenset()]"


def test_a_long_container_shows_one_item_to_a_line() -> None:
    words = ["a" * 30, "b" * 30, "c" * 30]
    assert transcript.show(words) == f"['{words[0]}',\n '{words[1]}',\n '{words[2]}']"
    assert transcript.show(("x\ny", 1)) == "('x\\ny', 1)"


def test_a_multiline_item_is_indented() -> None:
    class Lines:
        def _repr_pretty_(self, p: transcript.TextPrinter, cycle: bool) -> None:
            p.text("one\ntwo")

    assert transcript.show([Lines(), Lines()]) == "[one\n two,\n one\n two]"


def test_a_container_inside_itself_shows_as_repr_does() -> None:
    a: list[object] = [1]
    a.append(a)
    d: dict[str, object] = {}
    d["d"] = d
    assert (transcript.show(a), transcript.show(d)) == (repr(a), repr(d))


def test_a_subclass_of_a_container_shows_by_its_repr() -> None:
    from collections import namedtuple

    Point = namedtuple("Point", "x y")
    assert transcript.show(Point(1, 2)) == "Point(x=1, y=2)"


def test_without_its_results_a_transcript_is_the_script() -> None:
    source = strip_results(BASICS.read_text())  # basics.py has its results in it
    if not source.endswith("\n"):
        source += "\n"  # a transcript ends its last line
    assert without_results(render(run_path(str(BASICS)))) == source


def test_basics_has_its_current_results_in_it() -> None:
    assert render(run_path(str(BASICS)), color=False, unrun=True) == BASICS.read_text()


def test_the_transcript_module_imports_nothing_from_equarium() -> None:
    tree = ast.parse(Path(transcript.__file__).read_text())
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imported.add(node.module)
    assert not any(name.split(".")[0] == "equarium" for name in imported)


def test_the_command_line(capsys: pytest.CaptureFixture[str]) -> None:
    assert transcript.main([str(BASICS)]) == 0
    assert "x * 2\n#> 10\n" in capsys.readouterr().out


# Only what changed

# A value of one line per item, which `plus`, `swap` and `drop` remake.
LINES = """\
class Lines:
    def __init__(self, *items):
        self.items = items
    def plus(self, *items):
        return Lines(*self.items, *items)
    def swap(self, old, new):
        return Lines(*(new if item == old else item for item in self.items))
    def drop(self, gone):
        return Lines(*(item for item in self.items if item != gone))
    def _repr_pretty_(self, p, cycle):
        p.text("\\n".join(self.items))

"""


def results(source: str, display: transcript.Display = "changes") -> str:
    """The transcript of `LINES` and then `source`, from `source` on, in
    the changes display unless a test asks for another."""
    text = render(run(LINES + dedent(source), display=display))
    assert text.startswith(LINES)
    return text[len(LINES) :]


def test_a_value_made_from_a_seen_one_shows_what_changed() -> None:
    assert results(
        """\
        a = Lines("x = 1", "y = 2")
        a = a.plus("z = 3")
        a = a.swap("x = 1", "x = 5")
        b = a.plus("w = 4")
        """
    ) == dedent(
        """\
        a = Lines("x = 1", "y = 2")
        #> x = 1
        #> y = 2
        a = a.plus("z = 3")
        #> z = 3
        a = a.swap("x = 1", "x = 5")
        #> x = 5
        b = a.plus("w = 4")
        #> w = 4
        """
    )


def test_a_name_alone_shows_all_of_it() -> None:
    assert results('a = Lines("x = 1")\na = a.plus("y = 2")\na\n') == (
        'a = Lines("x = 1")\n#> x = 1\na = a.plus("y = 2")\n#> y = 2\na\n#> x = 1\n#> y = 2\n'
    )


def test_a_line_thats_gone_is_marked() -> None:
    assert results('a = Lines("x = 1", "y = 2")\na = a.drop("y = 2")\n').endswith(
        'a = a.drop("y = 2")\n#> - y = 2\n'
    )


def test_a_step_that_changes_nothing_says_so() -> None:
    assert results('a = Lines("x = 1", "y = 2")\na = a.plus()\n').endswith(
        "a = a.plus()\n#> (no change)\n"
    )


def test_another_type_and_one_line_show_whole() -> None:
    assert results(
        """\
        a = Lines("x = 1", "y = 2")
        t = a.items
        n = 5
        n = n + 1
        """
    ).endswith("t = a.items\n#> ('x = 1', 'y = 2')\nn = 5\n#> 5\nn = n + 1\n#> 6\n")


def test_the_changes_are_from_what_the_reader_last_saw() -> None:
    # The hidden step isn't seen, so the next one shows both changes.
    assert results('a = Lines("x = 1")\na = a.plus("y = 2");\na = a.plus("z = 3")\n').endswith(
        'a = a.plus("y = 2");\na = a.plus("z = 3")\n#> y = 2\n#> z = 3\n'
    )


def test_full_shows_every_value_whole() -> None:
    assert results('a = Lines("x = 1")\na = a.plus("y = 2")\n', display="full").endswith(
        'a = a.plus("y = 2")\n#> x = 1\n#> y = 2\n'
    )


def test_marked_shows_every_value_whole_with_its_changes_marked() -> None:
    assert results(
        """\
        a = Lines("x = 1", "y = 2", "z = 3")
        a = a.swap("y = 2", "y = 5")
        a = a.drop("z = 3")
        a = a.plus()
        """,
        display="marked",
    ) == dedent(
        """\
        a = Lines("x = 1", "y = 2", "z = 3")
        #> x = 1
        #> y = 2
        #> z = 3
        a = a.swap("y = 2", "y = 5")
        #>   x = 1
        #> * y = 5
        #>   z = 3
        a = a.drop("z = 3")
        #>   x = 1
        #>   y = 5
        #> - z = 3
        a = a.plus()
        #>   x = 1
        #>   y = 5
        """
    )


def test_marked_pairs_like_lines_as_changes_does() -> None:
    before = "(1)  dt = t1\n(2)  v = x/dt\n(3)  a = v/dt\nknowns: none"
    after = "(2)  v = x/t1\n(3)  a = v/t1\nknowns: none"
    assert transcript.marked_lines(before, after) == (
        "- (1)  dt = t1\n* (2)  v = x/t1\n* (3)  a = v/t1\n  knowns: none"
    )
    assert transcript.marked_lines("5", "6") == "6"


def test_the_display_flags_on_the_command_line(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "script.py"
    path.write_text(LINES + 'a = Lines("x = 1")\na = a.plus("y = 2")\n')
    assert transcript.main([str(path)]) == 0  # marked, the default
    assert capsys.readouterr().out.endswith('a = a.plus("y = 2")\n#>   x = 1\n#> * y = 2\n')
    assert transcript.main([str(path), "--changes"]) == 0
    assert capsys.readouterr().out.endswith('a = a.plus("y = 2")\n#> y = 2\n')
    assert transcript.main([str(path), "--full"]) == 0
    assert capsys.readouterr().out.endswith('a = a.plus("y = 2")\n#> x = 1\n#> y = 2\n')


def test_changes_are_judged_without_colors() -> None:
    green = "\x1b[32mx\x1b[0m = 1"
    assert changed_lines("x = 1\ny = 2", f"{green}\ny = 2") == "(no change)"
    assert changed_lines("x = 1\ny = 2", f"{green}\ny = 3") == "y = 3"


def test_a_shorter_run_pairs_like_lines() -> None:
    # Eliminating dt: (1) goes, and (2) and (3) change in place.
    before = "(1)  dt = t1\n(2)  v = x/dt\n(3)  a = v/dt\nknowns: none"
    after = "(2)  v = x/t1\n(3)  a = v/t1\nknowns: none"
    assert changed_lines(before, after) == "- (1)  dt = t1\n(2)  v = x/t1\n(3)  a = v/t1"


def test_a_system_built_step_by_step_shows_each_steps_effect() -> None:
    script = dedent(
        """\
        from sympy.physics.units import meter, second
        from equarium import System
        from equarium.physics import Particle, X
        m = Particle("m", 2, X);
        m0, m1 = m.states;
        m01 = m.edge(0, 1);
        s = System().add(*m.kinematics())
        s = s.add(*m01.constant_acceleration())
        s = s.known(m0.t, 0 * second)
        s = s.eliminate_zeros()
        a = s.want(m1.pos.x)
        """
    )
    text = render(run(script, display="changes"))
    after = uncolored(text.split("s = s.add(*m01.constant_acceleration())\n", 1)[1])
    *steps, connected = after.splitlines()
    assert steps == [
        "#> (4)  m01.v_av.x = m0.vel.x/2 + m1.vel.x/2",
        "s = s.known(m0.t, 0 * second)",
        "#> knowns: m0.t = 0",
        "s = s.eliminate_zeros()",
        "#> (1)  m01.dt = m1.t",
        "a = s.want(m1.pos.x)",
        "#> wants: m1.pos.x",
    ]
    # Only m0.t is known, so everything else in the four equations isn't.
    assert connected.startswith("#> connected: m0.pos.x, m0.vel.x, m01.a.x, m01.dt,")
    assert connected.endswith("(8 unknowns in 4 equations)")


# Results in the script


def test_stripping_drops_the_result_lines_only() -> None:
    source = 'x = 5\n#> 5\ns = """\n#> kept\n"""\nprint()\n#>\n    #> kept too\n'
    assert strip_results(source) == 'x = 5\ns = """\n#> kept\n"""\nprint()\n    #> kept too\n'


def test_stripping_a_script_that_doesnt_tokenize_is_a_syntax_error() -> None:
    with pytest.raises(SyntaxError):
        strip_results("x = (\n")


def test_a_transcript_drops_the_old_results(tmp_path: Path) -> None:
    path = tmp_path / "script.py"
    path.write_text("x = 5\n#> 999\n")
    assert render(run_path(str(path))) == "x = 5\n#> 5\n"


def script(tmp_path: Path, source: str) -> Script:
    path = tmp_path / "script.py"
    path.write_text(source)
    return Script.file(str(path))


def test_in_place_writes_the_results_into_the_script(tmp_path: Path) -> None:
    s = script(tmp_path, "x = 5\nx * 2\n")
    assert in_place(s) == (0, "script.py: ran, results written")
    assert s.read() == "x = 5\n#> 5\nx * 2\n#> 10\n"
    assert in_place(s) == (0, "script.py: ran, no change")


def test_in_place_replaces_the_old_results(tmp_path: Path) -> None:
    s = script(tmp_path, "x = 6\n#> 5\n")
    in_place(s)
    assert s.read() == "x = 6\n#> 6\n"


def test_in_place_keeps_the_lines_after_an_error(tmp_path: Path) -> None:
    s = script(tmp_path, "x = 1\n1 / 0\ny = 2\n")
    assert in_place(s) == (
        1,
        "script.py: stopped at an error, ZeroDivisionError: division by zero, results written",
    )
    written = s.read()
    assert written.endswith("#> ZeroDivisionError: division by zero\ny = 2\n")
    assert strip_results(written) == "x = 1\n1 / 0\ny = 2\n"


def test_a_traceback_gives_the_files_lines(tmp_path: Path) -> None:
    s = script(tmp_path, "x = 1\n#> 1\n#> 1\n1 / 0\n")
    in_place(s)
    written = s.read()
    assert 'script.py", line 2, in <module>\n#>     1 / 0\n' not in written
    assert written.startswith("x = 1\n#> 1\n1 / 0\n#> Traceback")
    # Run again, its results in it: the error is on the file's line 3.
    in_place(s)
    assert '#>   File "' + str(tmp_path / "script.py") + '", line 3, in <module>\n#>     1 / 0\n' in s.read()


def test_in_place_leaves_a_script_that_doesnt_parse(tmp_path: Path) -> None:
    for source in ("x = 5\n#> 5\nx = (\n", "x = 5\n#> 5\nx = = 6\n"):
        s = script(tmp_path, source)
        code, report = in_place(s)
        assert code == 2
        assert report.startswith("script.py: doesn't parse, left as it is: line 3")
        assert s.read() == source


def test_in_place_leaves_a_script_that_changed_while_it_ran(tmp_path: Path) -> None:
    source = 'with open(__file__, "a") as f:\n    f.write("# edited\\n")\n'
    s = script(tmp_path, source)
    assert in_place(s) == (0, "script.py: changed while it ran, left as it is")
    assert s.read() == source + "# edited\n"


def test_in_place_writes_no_colors(tmp_path: Path) -> None:
    s = script(
        tmp_path,
        dedent(
            """\
            class Green:
                def _repr_pretty_(self, p, cycle):
                    p.text("\\x1b[32mgreen\\x1b[0m")
            Green()
            """
        ),
    )
    in_place(s)
    assert s.read().endswith("Green()\n#> green\n")


def wait_for(condition: Callable[[], bool], timeout: float = 20.0) -> None:
    deadline = time.monotonic() + timeout
    while not condition():
        assert time.monotonic() < deadline, "timed out"
        time.sleep(0.05)


def test_watch_writes_the_results_on_every_save(tmp_path: Path) -> None:
    path = tmp_path / "script.py"
    path.write_text("x = 5\n")
    command = [sys.executable, "-m", "equarium.transcript", "--watch", str(path)]
    process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        wait_for(lambda: path.read_text() == "x = 5\n#> 5\n")
        path.write_text("x = 6\n#> 5\n")
        wait_for(lambda: path.read_text() == "x = 6\n#> 6\n")
    finally:
        process.terminate()
        process.wait(timeout=10)


# Example 2.4


@pytest.fixture(scope="module")
def n04() -> Transcript:
    return run_module("examples.up_15e.ch02.examples.n04.main")


def entry_value(result: Transcript, source_line: str) -> str:
    """The value of the statement whose source has the line."""
    for entry in result.entries:
        if source_line in entry.source.splitlines():
            assert entry.value is not None
            return ANSI.sub("", entry.value)
    raise AssertionError(f"no statement has the line {source_line!r}")


def test_2_4_runs(n04: Transcript) -> None:
    assert not n04.failed
    assert without_results(render(n04)) == N04.read_text()


def test_2_4_shows_its_systems(n04: Transcript) -> None:
    part_a = entry_value(
        n04, "part_a = motorcycle.known(m1.t, 2 * second).want(m1.pos.x, m1.vel.x)"
    )
    lines = part_a.splitlines()
    # It's made from `motorcycle`, which shows whole, so it shows whole
    # with what changed marked: the wants are new, and no equation is.
    assert "* wants: m1.pos.x, m1.vel.x" in lines
    assert all(line.startswith("  ") for line in lines if line.lstrip("* ").startswith("("))


def test_2_4_shows_its_solutions(n04: Transcript) -> None:
    assert entry_value(n04, "sol_a = part_a.solve()").splitlines() == [
        "m1.pos.x = m0.pos.x + m0.vel.x*m1.t + m01.a.x*m1.t**2/2",
        "m1.pos.x = 43.0*meter",
        "m1.vel.x = m0.vel.x + m01.a.x*m1.t",
        "m1.vel.x = 23.0*meter/second",
    ]


def test_2_4_shows_its_model_and_its_book(n04: Transcript) -> None:
    assert entry_value(n04, 'm = Particle("m", 2, X)  # the motorcyclist') == (
        "particle m (x): m0, m1"
    )
    assert entry_value(n04, "m0, m1 = m.states") == "(m0, m1)"
    book = entry_value(n04, "BOOK: list[Answer] = [  # University Physics, 15th ed.")
    assert book.splitlines() == [
        "[✓ m1.pos.x: book 43 meter, found 43.0*meter,",
        " ✓ m1.vel.x: book 23 meter/second, found 23.0*meter/second,",
        " ✓ m1.pos.x: book 55 meter, found 55.0*meter]",
    ]


def test_2_4_colors_knowns_and_wants(n04: Transcript) -> None:
    entry = next(e for e in n04.entries if "sol_a = part_a.solve()" in e.source)
    assert entry.value is not None
    assert "\x1b[32mm0.pos.x\x1b[0m" in entry.value  # a known, green
    assert "\x1b[31mm1.pos.x\x1b[0m" in entry.value  # a want, red
