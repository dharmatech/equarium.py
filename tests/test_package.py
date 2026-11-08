import equarium


def test_exports() -> None:
    for name in equarium.__all__:
        assert hasattr(equarium, name), name
