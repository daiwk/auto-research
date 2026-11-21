"""AdaObs controls, not learned-agent or benchmark capability assertions."""
import math

import pytest

from auto_research.agent_research.sage_evolve import (
    Observation, PlateauMonitor, Proposal, diagnostic, first_feasible,
    hardest_informative, marginal_return, retain_increment, validate_update,
)


def test_explicit_retained_data_units():
    assert marginal_return(60, 61, 20_000) == .5
    assert marginal_return(61, 60, 5_000) == -2
    for count in (0, -1, True, 2.5):
        with pytest.raises(ValueError):
            marginal_return(60, 61, count)


def test_ema_strict_plateau_and_observation_reset():
    monitor = PlateauMonitor("v1")
    assert not monitor.observe(.1, phase_id="v1")
    assert not monitor.observe(.1, phase_id="v1")
    assert not monitor.observe(.1, phase_id="v1")  # Strict below, not <=.
    assert not monitor.observe(0, phase_id="v1")
    assert not monitor.observe(0, phase_id="v1")
    assert monitor.observe(0, phase_id="v1")
    assert monitor.history[-3:] == pytest.approx((.07, .049, .0343))
    with pytest.raises(ValueError):
        monitor.observe(0, phase_id="v2")
    monitor.start_phase("v2")
    assert monitor.history == () and not monitor.plateau
    assert not monitor.observe(.02, phase_id="v2")
    assert monitor.history == (.02,)


def test_increment_acceptance_has_fixed_anchor_barrier():
    assert retain_increment(50, 51, 60, 59.5)
    assert retain_increment(50, 49, 60, 61)
    assert not retain_increment(50, 51, 60, 59.499)
    assert not retain_increment(50, 50, 60, 60)
    with pytest.raises(ValueError):
        retain_increment(50, math.nan, 60, 60)


def test_concrete_failure_does_not_disable_lever_or_other_gap():
    current = Observation(("a",), ("easy",), "aggregate")
    one = Proposal("L1", "format", Observation(("a",), ("easy",), "format"))
    other = Proposal("L1", "length", Observation(("a",), ("easy",), "length"))
    two = Proposal("L2", "hard", Observation(("a",), ("easy", "hard"), "aggregate"))
    failure = frozenset({("gap", "L1", "format")})
    assert first_feasible(current, [two, one, other], gap="gap", failed=failure) == other
    assert first_feasible(current, [two, one], gap="other-gap", failed=failure) == one
    assert first_feasible(current, [two, one], gap="gap", failed=failure) == two
    assert first_feasible(current, [one], gap="gap", failed=failure) is None


def test_update_changes_exactly_one_axis_and_is_cumulative():
    current = Observation(("a",), ("easy",), "aggregate")
    validate_update(current, Proposal("L3", "b", Observation(("a", "b"), ("easy",), "aggregate")))
    for proposal in [Proposal("L1", "bad", Observation(("b",), ("easy",), "detail")),
                     Proposal("L2", "bad", Observation(("a",), ("hard",), "aggregate")),
                     Proposal("L2", "bad", Observation(("a",), ("easy", "hard", "hardest"), "aggregate")),
                     Proposal("L3", "bad", Observation(("b",), ("easy",), "aggregate"))]:
        with pytest.raises(ValueError):
            validate_update(current, proposal)


def test_hardest_tier_uses_inclusive_band_not_largest_pass_rate():
    assert hardest_informative([("a", .6), ("b", .35), ("c", .2), ("d", .1)]) == "c"
    assert hardest_informative([("a", .9), ("b", .1)]) is None
    with pytest.raises(ValueError):
        hardest_informative([("a", .3), ("a", .2)])
    with pytest.raises(ValueError):
        hardest_informative([("a", math.nan)])


@pytest.mark.parametrize("kwargs", [{"alpha": 0}, {"window": 0}, {"epsilon": -1}, {"alpha": math.inf}])
def test_bad_monitor_configuration(kwargs):
    with pytest.raises(ValueError):
        PlateauMonitor("phase", **kwargs)


def test_observation_axes_are_immutable_named_tuples():
    with pytest.raises(ValueError):
        Observation(["a"], ("easy",), "aggregate")


def test_diagnostic_is_bounded_cpu_mechanism_only():
    for seed in (42, 43, 44):
        result = diagnostic(seed)
        assert result["seed"] == seed and result["diagnostic_only"] is True
        assert result["evaluation_tier"] == "l1_mechanism"
        assert all(result["checks"].values())
    with pytest.raises(ValueError):
        diagnostic(42, "cuda")
