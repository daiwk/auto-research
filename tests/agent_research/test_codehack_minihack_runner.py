import pytest

from scripts.run_codehack_minihack import mode_actions


def test_codehack_modes_expose_expected_action_types():
    skills, primitives = mode_actions("primitives")
    assert not skills and primitives
    skills, primitives = mode_actions("skills")
    assert skills and not primitives
    skills, primitives = mode_actions("mixed")
    assert skills and primitives


def test_codehack_mode_rejects_unknown_variant():
    with pytest.raises(ValueError):
        mode_actions("oracle")
