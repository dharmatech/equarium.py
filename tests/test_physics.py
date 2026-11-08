"""The old physics code's copy, and the layers."""

import subprocess
import sys

from equarium.physics.kinematics_states import kinematics_fundamental, make_states_model


def test_the_same_equations_as_the_old_library() -> None:
    # The old library's own output, from its venv in combine-equations.py
    # (2026-11-08).
    assert [str(eq) for eq in kinematics_fundamental(make_states_model("m", 2), axes=("x",))] == [
        "Eq(dt_m_0_1, -m_0_t + m_1_t)",
        "Eq(v_av_x_m_0_1, (-m_0_x + m_1_x)/dt_m_0_1)",
        "Eq(a_x_m_0_1, (-m_0_v_x + m_1_v_x)/dt_m_0_1)",
        "Eq(v_av_x_m_0_1, m_0_v_x/2 + m_1_v_x/2)",
    ]


def test_the_core_doesnt_import_the_physics_code() -> None:
    # In a fresh interpreter, since other tests import the physics code.
    check = "import sys, equarium; print('equarium.physics' in sys.modules)"
    result = subprocess.run(
        [sys.executable, "-c", check], capture_output=True, text=True, check=True
    )
    assert result.stdout.strip() == "False"
