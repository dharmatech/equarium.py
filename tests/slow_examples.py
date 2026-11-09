"""The example modules that take more than 5 s to import, so their tests
are marked `slow`. `tests/test_examples.py` and `tests/test_old_outputs.py`
both read this set, and import a slow module only inside a test, never at
the top of a file.

The set is empty. 3.9 and 3.10 left it in increment 003 of the 004
series, once one-way polar made them fast. The file stays for the next
slow module.
"""

SLOW_EXAMPLES: frozenset[str] = frozenset()
