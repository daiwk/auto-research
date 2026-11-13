"""Pure Eq.55--56 tests; no learned medical model or clinical evaluation."""
from dataclasses import asdict
import math

import pytest

from auto_research.multimodal.sensorwm_planning import (
    Actions, Candidate, diagnostic, personalized_effort, rank_candidates,
)


def test_sigma_floors_and_individual_variability_are_not_population_costs():
    base, target = Actions(1000, 400, 20), Actions(1500, 415, 30)
    assert personalized_effort(target, base, Actions(0, 0, 0)) == 3
    assert personalized_effort(target, base, Actions(1000, 30, 20)) == .75
    assert personalized_effort(base, base, Actions(0, 0, 0)) == 0


def test_future_against_future_anchor_and_exact_denominator():
    base, sigma = Actions(1000, 400, 20), Actions(500, 15, 10)
    candidate = Candidate("c", Actions(2000, 400, 20), projected_endpoint=19, feasible=True)
    row = rank_candidates([candidate], base, sigma, status_quo_endpoint=20)[0]
    assert asdict(row) == {"candidate_id": "c", "gain": 1., "effort": 4., "score": .2}
    assert "baseline_health_age" not in rank_candidates.__annotations__
    assert "targets" not in asdict(row)  # no recommendation emitted


def test_strict_threshold_external_feasibility_and_empty_result():
    base, sigma = Actions(0, 0, 0), Actions(0, 0, 0)
    equal = Candidate("equal", base, 0, True)
    assert rank_candidates([equal], base, sigma, .1) == []
    assert rank_candidates([equal], base, sigma, math.nextafter(.1, math.inf))
    rejected = Candidate("external", base, -1, False)
    assert rank_candidates([rejected], base, sigma, .1) == []
    assert rank_candidates([], base, sigma, .1) == []


def test_effort_can_reverse_raw_gain_order_and_ties_use_ids():
    base, sigma = Actions(1000, 400, 20), Actions(500, 15, 10)
    high_gain = Candidate("high-effort", Actions(6000, 400, 20), 8, True)
    lower_gain = Candidate("low-effort", Actions(1500, 400, 20), 9, True)
    assert [x.candidate_id for x in rank_candidates([high_gain, lower_gain], base, sigma, 10)] == [
        "low-effort", "high-effort"]
    ties = [Candidate("b", base, 9, True), Candidate("a", base, 9, True)]
    assert [x.candidate_id for x in rank_candidates(ties, base, sigma, 10)] == ["a", "b"]


@pytest.mark.parametrize("bad", [True, "2", None, float("nan"), float("inf"), -1])
def test_action_types_and_nonnegative_finite_values(bad):
    with pytest.raises(ValueError):
        Actions(bad, 0, 0)


@pytest.mark.parametrize("bad", [True, "2", None, float("nan"), float("inf")])
def test_endpoint_is_explicit_finite_external_scalar(bad):
    base = Actions(0, 0, 0)
    with pytest.raises(ValueError):
        Candidate("c", base, bad, True)
    with pytest.raises(ValueError):
        rank_candidates([], base, base, bad)


def test_missing_feasibility_duplicate_identity_and_untyped_inputs_rejected():
    base = Actions(0, 0, 0)
    for bad in (1, "safe", None):
        with pytest.raises(ValueError):
            Candidate("c", base, 1., bad)
    candidate = Candidate("c", base, 1., True)
    with pytest.raises(ValueError, match="unique"):
        rank_candidates([candidate, candidate], base, base, 2.)
    with pytest.raises(ValueError, match="typed"):
        rank_candidates([{"candidate_id": "c"}], base, base, 2.)
    with pytest.raises(ValueError, match="typed"):
        rank_candidates([], base, [0, 0, 0], 2.)


def test_overflowing_arithmetic_is_rejected_not_reported_as_finite_score():
    base = Actions(0, 0, 0)
    with pytest.raises(ValueError, match="finite arithmetic"):
        personalized_effort(Actions(1e308, 0, 0), base, base)
    with pytest.raises(ValueError, match="finite arithmetic"):
        rank_candidates([Candidate("c", base, -1e308, True)], base, base, 1e308)


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic_is_finite_l1_arithmetic_only(seed):
    result = diagnostic(seed)
    assert result["seed"] == seed and result["diagnostic_only"] is True
    assert result["evaluation_tier"] == "l1_mechanism"
    assert all(type(x) is bool and x for x in result["checks"].values())
    assert all(math.isfinite(x) for x in result["metrics"].values())
    with pytest.raises(ValueError, match="CPU"):
        diagnostic(seed, device="cuda")
