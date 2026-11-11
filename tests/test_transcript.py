"""Transcript mode, `equarium.transcript`: plain Python first, then
Example 2.4."""

import ast
import re
from pathlib import Path
from textwrap import dedent

import pytest

from equarium import transcript
from equarium.transcript import Transcript, render, run, run_module, run_path

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


def test_none_and_bare_strings_dont_show() -> None:
    assert transcribe('"""A docstring."""\nprint()\nNone\n') == '"""A docstring."""\nprint()\n#>\nNone\n'


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


def test_without_its_results_a_transcript_is_the_script() -> None:
    source = BASICS.read_text()
    assert without_results(render(run_path(str(BASICS)))) == source


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
    assert "wants: m1.pos.x, m1.vel.x" in part_a.splitlines()


def test_2_4_shows_its_solutions(n04: Transcript) -> None:
    assert entry_value(n04, "sol_a = part_a.solve()").splitlines() == [
        "m1.pos.x = m0.pos.x + m0.vel.x*m1.t + m01.a.x*m1.t**2/2",
        "m1.pos.x = 43.0*meter",
        "m1.vel.x = m0.vel.x + m01.a.x*m1.t",
        "m1.vel.x = 23.0*meter/second",
    ]


def test_2_4_colors_knowns_and_wants(n04: Transcript) -> None:
    entry = next(e for e in n04.entries if "sol_a = part_a.solve()" in e.source)
    assert entry.value is not None
    assert "\x1b[32mm0.pos.x\x1b[0m" in entry.value  # a known, green
    assert "\x1b[31mm1.pos.x\x1b[0m" in entry.value  # a want, red
