import numpy as np
import json

import pytest

from auto_research.agent_research import discernmem as dm, ruharness as rh


@pytest.mark.parametrize("module", [dm, rh])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_mechanism_diagnostics(module, seed):
    result = module.diagnostic(seed)
    assert result["checks"] and all(result["checks"].values())
    assert all(type(value) is bool for value in result["checks"].values())
    json.dumps(result, allow_nan=False)
    assert result["diagnostic_only"] and result["seed"] == seed
    with pytest.raises(ValueError):
        module.diagnostic(seed, "cuda")


def test_paired_replays_require_same_execution():
    with_memory = dm.ReplayScore("q", "m", 2, "planner", 42, "c", .6)
    assert dm.paired_effect(with_memory, dm.ReplayScore("q", None, None, None, 42, "c", .6)) == (0., "neutral")
    for baseline in [dm.ReplayScore("q", None, None, None, 43, "c", .6),
                     dm.ReplayScore("q2", None, None, None, 42, "c", .6),
                     dm.ReplayScore("q", None, None, None, 42, "other", .6)]:
        with pytest.raises(ValueError, match="same task"):
            dm.paired_effect(with_memory, baseline)


def test_scope_not_negative_score_alone():
    assert dm.attribution(-.4, use_match=False, avoid_match=False, supported_defect=True) == "scope"
    assert dm.attribution(-.4, use_match=True, avoid_match=False, supported_defect=False) == "none"
    assert dm.attribution(-.4, use_match=True, avoid_match=False, supported_defect=True) == "content"
    assert dm.attribution(.4, use_match=True, avoid_match=True, supported_defect=True) == "scope"
    assert dm.attribution(.4, use_match=True, avoid_match=False, supported_defect=True) == "none"


def test_repair_requires_both_baselines_and_complete_failure_guard():
    args = dict(trigger="q", body_changed=True, evidence_cited=True, expected_correction=True)
    assert not dm.repair_gate([dm.RepairComparison("q", .2, .8, .7)], **args)["accepted"]
    result = dm.repair_gate([dm.RepairComparison("q", .005, 0., 0.)], **args)
    assert result["pointwise_retention"] and not result["accepted"]
    assert not dm.repair_gate([dm.RepairComparison("q", .8, .8, .8)], **{**args, "evidence_cited": False})["accepted"]
    with pytest.raises(ValueError):
        dm.repair_gate([], **args)
    with pytest.raises(ValueError):
        dm.repair_gate([dm.RepairComparison("h", .8, .8, .8)], **args)


def test_version_does_not_inherit_old_effects_and_rejects_source_validation():
    parent = dm.MemoryVersion("m", "planner", 2, "old", "source", (("h", .2),), ("earlier fix",))
    result = dm.revised_version(parent, body="new", comparisons=[dm.RepairComparison("q", .2, .5, .7)],
                               trigger="q", related_tasks=(), correction="fixed stop", evidence_cited=True)
    assert result.version == 3 and result.effects == ()
    assert result.corrections == parent.corrections and parent.effects
    with pytest.raises(ValueError):
        dm.revised_version(parent, body="new", comparisons=[dm.RepairComparison("source", .2, .5, .7)],
                           trigger="source", related_tasks=(), correction="fix", evidence_cited=True)


def test_contingency_joint_rates_and_set_statistics():
    labels = np.array([[0, 1, 2, 0, 0, 1], [1, 1, 2, 0, 1, 1]])
    outcomes = np.array([True, True, True, False, False, False])
    counts = rh.contingency(labels, outcomes)
    np.testing.assert_array_equal(counts[0], [[1, 1, 1], [2, 1, 0]])
    d, c, p = rh.dcp(counts[0])
    np.testing.assert_allclose([d, c, p], [2 / 3 - 1 / 2, 2 / 3, 2 / 3 - 3 / 5])
    novelty, redundancy = rh.set_statistics(labels, outcomes)
    np.testing.assert_allclose(novelty, [1 / 3, 0])
    np.testing.assert_allclose(redundancy, [1 / 3, 1 / 3])


def test_posterior_is_joint_six_cells_not_independent_beta_rates():
    labels = np.array([[0, 1, 1, 0, 0, 1]])
    outcomes = np.array([True, True, True, False, False, False])
    counts = rh.contingency(labels, outcomes)[0]
    draws = np.random.default_rng(42).dirichlet(counts.ravel() + .5, size=2000).reshape(2000, 2, 3)
    d, c, p = rh.dcp(draws)
    novelty, redundancy = rh.set_statistics(labels, outcomes)
    expected = np.quantile(d + .5 * c + p + .5 * novelty[0] - .5 * redundancy[0], .2)
    result = rh.conservative_frontier(labels, outcomes, active=[True])
    assert result["scores"][0] == expected
    assert result["indices"].tolist() == [0]
    assert rh.conservative_frontier(labels, outcomes, active=[False])["indices"].size == 0


def test_bad_inputs_and_undefined_observed_rates_fail_closed():
    with pytest.raises(ValueError):
        rh.dcp(np.zeros((2, 3)))
    with pytest.raises(ValueError):
        rh.conservative_frontier([[0, 1]], [True, True], active=[True])
    with pytest.raises(ValueError):
        rh.contingency([[0., 1.]], np.array([True, False]))
    with pytest.raises(ValueError):
        rh.validation_update(.5, [float("nan")], verified=[True])
    assert rh.validation_update(.5, [.55], verified=[False]) is None
    assert rh.validation_update(.5, [.7, .7], verified=[True, True]) == 0
