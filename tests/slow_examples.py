"""The example modules that take more than 5 s to import, so their tests
are marked `slow`. `tests/test_examples.py` and `tests/test_old_outputs.py`
both read this set, and import a slow module only inside a test, never at
the top of a file.
"""

SLOW_EXAMPLES = frozenset(
    {
        "examples.up_15e.ch03.examples.n09.main",  # eliminating() on two-way polar, about 6 s
        "examples.up_15e.ch03.examples.n10.main",  # the dart's eliminations, about 9 s
    }
)
