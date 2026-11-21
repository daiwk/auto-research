import itertools
import math

import pytest

from auto_research.foundation_models.e_rwsc import ERWSC, diagnostic, rwsc_masses


def test_first_appearance_is_not_counted_as_a_predictable_bet_success():
    state = ERWSC(max_samples=20)
    assert state.observe("a", 1.) is None
    assert state.last_bets == {}
    assert state.evidence["a"].post_appearance_agreements == 0
    assert state.evidence["a"].log_wealth == 0.
    state.observe("b", 100.)
    assert "b" not in state.last_bets
    assert state.evidence["b"].log_wealth == 0.


def test_reward_normalization_softmax_and_equal_score_convention():
    a = rwsc_masses([("a", -1.), ("b", 1.), ("a", 3.)])
    b = rwsc_masses([("a", 10.), ("b", 20.), ("a", 30.)])
    assert a == pytest.approx(b)
    assert rwsc_masses([("a", 0.), ("b", 0.), ("a", 0.)]) == {"a": 2/3, "b": 1/3}
    assert math.fsum(rwsc_masses([("a", 1e308), ("b", -1e308)]).values()) == pytest.approx(1.)
    assert rwsc_masses([("a", -1.), ("b", 1.)], 1e-300) == {"a": 0., "b": 1.}


def test_next_observation_and_reward_cannot_influence_current_stakes():
    a, b = ERWSC(max_samples=40), ERWSC(max_samples=40)
    for answer, reward in (("a", 1.), ("a", 1.), ("b", 0.)):
        a.observe(answer, reward)
        b.observe(answer, reward)
    expected = a.predictable_bets()
    a.observe("a", 1e100)
    b.observe("c", -1e100)
    assert a.last_bets == b.last_bets == expected


def test_existing_capital_survives_a_reward_weighted_leader_change():
    s = ERWSC(alpha=1e-10, max_samples=32)
    for _ in range(3):
        s.observe("a", 0.)
    before = s.evidence["a"].log_wealth
    stake = s.predictable_bets()["a"]
    s.observe("b", 100.)
    assert rwsc_masses(s.observations)["b"] > rwsc_masses(s.observations)["a"]
    assert s.evidence["a"].log_wealth == pytest.approx(before+math.log1p(-.5*stake))
    assert s.evidence["a"].log_wealth != 0.


def test_certification_is_policy_majority_not_correctness_and_returns_best_response():
    s = ERWSC(alpha=.1, max_samples=32)
    for n in range(32):
        result = s.observe("wrong-but-certain", float(n))
        if result is not None:
            break
    assert result.certified and result.answer == "wrong-but-certain"
    assert result.response_index == result.samples-1
    assert result.log_weighted_wealth >= -math.log(.1)
    assert result.reason == "majority_certified_not_correctness"
    with pytest.raises(ValueError):
        s.observe("future", 1000.)


def test_budget_exhaustion_falls_back_to_uncertified_rwsc_not_current_majority():
    s = ERWSC(alpha=1e-12, max_samples=3)
    s.observe("a", 0.)
    s.observe("a", 0.)
    result = s.observe("b", 100.)
    assert not result.certified and result.answer == "b" and result.response_index == 2
    assert result.reason == "budget_exhausted_uncertified" and result.samples == 3


def test_first_appearance_rank_sets_summable_evidence_weights():
    s = ERWSC(alpha=1e-12, max_samples=4)
    s.observe("first", 0.)
    s.observe("second", 0.)
    assert s.evidence["first"].rank == 1 and s.evidence["second"].rank == 2
    assert s._weighted_wealth("second") == pytest.approx(-math.log(6.))


def test_small_exact_iid_null_enumeration_does_not_exceed_nominal_error():
    # Exact enumeration of all fair iid answer paths, not a claim about LLMs.
    horizon, alpha = 10, .2
    false_certifications = 0
    for path in itertools.product(("a", "b"), repeat=horizon):
        s = ERWSC(alpha=alpha, max_samples=horizon)
        for answer in path:
            result = s.observe(answer, 0.)
            if result is not None:
                false_certifications += result.certified
                break
    assert false_certifications / 2**horizon <= alpha


@pytest.mark.parametrize("kwargs", [{"alpha": 0.}, {"alpha": 1.}, {"threshold": .49},
    {"threshold": 1.}, {"clip": 1.}, {"clip": 0.}, {"prior_strength": 0.},
    {"temperature": -1.}, {"max_samples": True}, {"max_samples": 0}, {"alpha": math.nan}])
def test_invalid_parameters_fail_closed(kwargs):
    with pytest.raises(ValueError):
        ERWSC(**kwargs)


@pytest.mark.parametrize("answer,reward", [("", 0.), (None, 0.), ("a", True),
                                          ("a", math.nan), ("a", math.inf)])
def test_invalid_observation_rejected_before_state_mutation(answer, reward):
    s = ERWSC()
    with pytest.raises(ValueError):
        s.observe(answer, reward)
    assert s.observations == [] and s.evidence == {}


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_cpu_diagnostic_controls(seed):
    result = diagnostic(seed)
    assert result["device"] == "cpu" and result["checks"] == result["controls"]
    assert all(result["checks"].values())
    with pytest.raises(ValueError):
        diagnostic(seed, "cuda")
