from dataclasses import FrozenInstanceError
from typing import Any

import pytest
import sympy as sp

from equarium import Contradiction, System, UsageError, eq_flat
from equarium.analysis import Role
from equarium.equations import Derived, Given
from equarium.steps import AddStep, EliminateZerosStep

from example_2_4 import (
    a,
    base,
    eq_2_2,
    eq_2_7,
    eq_2_10,
    motorcycle,
    part_a,
    pre,
    t0,
    t1,
    v0,
    v1,
    v_av,
    x0,
    x1,
)

D, g, th = sp.symbols("D g th")


def labels(system: System) -> tuple[str, ...]:
    return tuple(e.label for e in system.equations)


# Labels


def test_given_labels() -> None:
    assert labels(base) == ("2.2", "2.7", "2.10")


def test_automatic_labels() -> None:
    assert labels(System().add(eq_2_2).add(eq_2_7)) == ("1", "2")


def test_label_with_two_equations() -> None:
    with pytest.raises(UsageError):
        System().add(eq_2_2, eq_2_7, label="2.2")


def test_duplicate_label() -> None:
    with pytest.raises(UsageError):
        base.add(eq_2_10, label="2.2")


def test_automatic_label_skips_one_in_use() -> None:
    assert labels(System().add(eq_2_2, label="1").add(eq_2_7)) == ("1", "2")


def test_add_true_adds_nothing() -> None:
    added = base.add(sp.Eq(x0, x0))
    assert added.equations == base.equations
    assert added.step == AddStep(())


def test_add_false_is_a_contradiction() -> None:
    with pytest.raises(Contradiction):
        base.add(sp.Eq(x0, x0 + 1))


def test_add_rejects_a_non_equation() -> None:
    with pytest.raises(UsageError):
        System().add(x0 + 1)


def test_old_style_zero_equation() -> None:
    zeroed = System().add(sp.Eq(t0, 0)).known(t0, 0).eliminate_zeros()
    assert zeroed.equations == ()
    assert isinstance(zeroed.step, EliminateZerosStep)
    assert zeroed.step.dropped == ("1",)
    # A label is never issued again after its equation is dropped.
    assert labels(zeroed.add(eq_2_2)) == ("2",)


# Zeros


def test_known_zero_leaves_the_equations_as_written() -> None:
    assert tuple(e.eq for e in pre.equations) == (eq_2_2, eq_2_7, eq_2_10)


def test_eliminate_zeros() -> None:
    assert all(t0 not in e.eq.free_symbols for e in base.equations)
    assert base.step == EliminateZerosStep((t0,), ("2.2", "2.7"), ())
    assert base.equation("2.2").origin == Derived(
        "eliminate zeros", t0, (pre.equation("2.2"),)
    )
    assert base.equation("2.7").origin == Derived(
        "eliminate zeros", t0, (pre.equation("2.7"),)
    )
    assert base.equation("2.10").origin == Given()
    assert base.fixed == {t0}


def test_float_zero_puts_no_float_in_the_equations() -> None:
    zeroed = motorcycle(t0_value=0.0).eliminate_zeros()
    assert zeroed.equations == base.equations
    assert all(t0 not in e.eq.free_symbols for e in zeroed.equations)
    assert not any(e.eq.atoms(sp.Float) for e in zeroed.equations)


def test_fixed_knowns() -> None:
    with pytest.raises(UsageError):
        base.forget(t0)
    with pytest.raises(UsageError):
        base.known(t0, 3)
    assert t0 not in pre.forget(t0).knowns
    assert pre.known(t0, 3).knowns[t0] == 3


def test_a_later_zero() -> None:
    later = base.known(x0, 0)
    assert x0 in later.equation("2.2").eq.free_symbols
    again = later.eliminate_zeros()
    assert all(x0 not in e.eq.free_symbols for e in again.equations)


def test_no_zeros_changes_nothing() -> None:
    system = System().add(eq_2_2)
    zeroed = system.eliminate_zeros()
    assert zeroed == system
    assert zeroed.step == EliminateZerosStep((), (), ())


def test_zero_contradiction() -> None:
    with pytest.raises(Contradiction):
        System().add(sp.Eq(t0, 3)).known(t0, 0).eliminate_zeros()


# Knowns


def test_known_leaves_the_equations_alone() -> None:
    known = System().add(eq_2_2).known(x0, 5)
    assert known.equations == System().add(eq_2_2).equations
    assert known.knowns[x0] == 5


def test_known_refuses_a_relationship() -> None:
    with pytest.raises(UsageError):
        System().known(x0, D * sp.tan(th))


def test_known_with_no_number() -> None:
    known = base.known(D)
    assert known.knowns[D] is None
    assert known.analyze().role(D) is Role.KNOWN


def test_known_dict_sets_several_in_one_step() -> None:
    known = System().known({t0: 0, x0: 5, D: None})
    assert dict(known.knowns) == {t0: 0, x0: 5, D: None}
    assert known.previous == System()


def test_replaced_known_keeps_its_place() -> None:
    assert list(base.known(x0, 7).knowns) == [t0, x0, v0, a]


def test_known_and_want_exclude_each_other() -> None:
    with pytest.raises(UsageError):
        part_a.known(x1, 3)
    with pytest.raises(UsageError):
        base.want(x0)
    with pytest.raises(UsageError):
        base.forget(t1)


def test_want_duplicate() -> None:
    with pytest.raises(UsageError):
        base.want(x1, x1)


def test_want_replaces_and_clears() -> None:
    assert part_a.want(v1).wants == (v1,)
    assert part_a.want().wants == ()


# Branches


def test_branches_dont_touch_their_base() -> None:
    assert t1 in part_a.knowns
    assert t1 not in base.knowns
    assert base.wants == ()


def test_branches_built_the_same_way_are_equal() -> None:
    assert base.known(t1, 2).want(x1, v1) == part_a
    assert base.known(t1, 2).want(x1, v1) == base.want(x1, v1).known(t1, 2)


def test_systems_are_immutable() -> None:
    knowns: Any = part_a.knowns
    with pytest.raises(TypeError):
        knowns[t1] = 3
    with pytest.raises(FrozenInstanceError):
        setattr(part_a, "wants", ())
    assert part_a.previous is not None
    assert part_a.previous.previous is base


# Analysis


def test_analysis_of_part_a() -> None:
    analysis = part_a.analyze()
    assert analysis.connected == {x1, v1, v_av}
    assert analysis.ready == ("2.7",)
    assert analysis.connected_labels == ("2.2", "2.7", "2.10")
    assert analysis.others == frozenset()
    assert analysis.role(x0) is Role.KNOWN
    assert analysis.role(x1) is Role.WANT
    assert analysis.role(v_av) is Role.UNKNOWN


def test_analysis_with_no_wants() -> None:
    analysis = base.analyze()
    assert analysis.connected == frozenset()
    assert analysis.others == {x1, v1, v_av, t1}
    assert analysis.ready == ()


# eq_flat


def test_eq_flat() -> None:
    p, q, r, s = sp.symbols("p q r s")
    assert eq_flat(p, q, r, s) == [sp.Eq(p, q), sp.Eq(r, s)]
    with pytest.raises(UsageError):
        eq_flat(p, q, r)


def test_eq_flat_into_add() -> None:
    assert labels(System().add(*eq_flat(v_av, v0, a, v1))) == ("1", "2")
