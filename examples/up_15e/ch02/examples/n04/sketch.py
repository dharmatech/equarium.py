"""Example 2.4's setup sketch, an experiment: `main.py`'s model, drawn by
`equarium.sketch`, one panel per part. It writes `sketch.svg` beside it:

    uv run python -m examples.up_15e.ch02.examples.n04.sketch
"""

from pathlib import Path

from equarium.sketch import sketch
from examples.up_15e.ch02.examples.n04.main import m, part_a, part_b

SVG = Path(__file__).with_name("sketch.svg")


def draw() -> str:
    return sketch(
        m,
        ("Example 2.4 (a): where is he, and how fast, at t = 2.0 s?", part_a),
        ("Example 2.4 (b): where is he when his speed is 25 m/s?", part_b),
    )


if __name__ == "__main__":
    SVG.write_text(draw())
    print(SVG)
