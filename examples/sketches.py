"""The setup sketches, an experiment: each writes `sketch.svg` beside its
problem's `main.py`, drawn from that module's model by `equarium.sketch`.

    uv run python -m examples.sketches

The sketches live here, not in the problem's folder, since every module
there is an example with a `BOOK`.
"""

from collections.abc import Callable
from pathlib import Path

from equarium.sketch import sketch

HERE = Path(__file__).parent


def example_2_4() -> str:
    from examples.up_15e.ch02.examples.n04.main import m, part_a, part_b

    return sketch(
        m,
        ("Example 2.4 (a): where is he, and how fast, at t = 2.0 s?", part_a),
        ("Example 2.4 (b): where is he when his speed is 25 m/s?", part_b),
    )


SKETCHES: dict[str, Callable[[], str]] = {
    "up_15e/ch02/examples/n04": example_2_4,
}


if __name__ == "__main__":
    for folder, draw in SKETCHES.items():
        path = HERE / folder / "sketch.svg"
        path.write_text(draw())
        print(path.relative_to(HERE.parent))
