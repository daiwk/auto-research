"""Literal formulas, leakage controls and negative cases for the root intake."""

import itertools
import math
import pytest
import torch
from auto_research.reproductions import mle_agents_components as mle
from auto_research.reproductions import xsplit_argus_components as argus
from auto_research.reproductions import mars_fapo_components as mars
from auto_research.agent_research import searchinject_components as si
from auto_research.agent_research import execjudges_components as ej


@pytest.mark.parametrize("module", [mle, argus, mars, si, ej])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostics(module, seed):
    result = module.diagnostic(seed)
    assert result["seed"] == seed and result["diagnostic_only"]
    assert result["checks"] and all(result["checks"].values())
    assert all(math.isfinite(x) for x in result["metrics"].values())


def test_mle_probe_not_stale_incumbent():
    # Candidate beats a stale .8 incumbent, but not this iteration's .6 probe.
    row = mle.assess_candidate((0.7, 0.7), (0.6, 0.6), completion_signals=(True, True))
    assert not row["offline_search_accept"] and not row["online_launch_authorized"]
    with pytest.raises(ValueError):
        mle.assess_candidate(
            (0.7, 0.7), (0.6, 0.6), completion_signals=(True, True), coherent_changes=2
        )
    with pytest.raises(ValueError):
        mle.weighted_ne(float("nan"), 0.1)


def test_argus_dual_head_l1_teacher_not_bce_or_kl():
    gt = torch.tensor([[0.2, -0.3]], dtype=torch.double, requires_grad=True)
    kd = torch.tensor([[1.0, -2.0]], dtype=torch.double, requires_grad=True)
    teacher = torch.tensor([[2.0, 1.0]], dtype=torch.double, requires_grad=True)
    labels = torch.tensor([[0.0, 1.0]], dtype=torch.double)
    expected = torch.nn.functional.binary_cross_entropy_with_logits(
        gt, torch.tensor([[0.01, 1.0]], dtype=torch.double)
    ) + 0.15 * torch.tensor(2.0, dtype=torch.double)
    loss = argus.joint_loss(gt, kd, labels, teacher)
    assert torch.allclose(loss, expected)
    loss.backward()
    assert teacher.grad is None and torch.allclose(
        kd.grad, torch.tensor([[-0.075, -0.075]], dtype=torch.double)
    )


def test_argus_causal_prefix_and_cached_overlap_are_distinct():
    torch.manual_seed(4)
    model = argus.XSplitMemory().eval()
    e = torch.randn(1, 9, 8)
    q = torch.randn(1, 1, 8)
    # b can overlap the recent branch, but must remain strictly before target.
    overlap = model.training_target(e, q, target=6, compressed=2, recent=2, cached_cutoff=5)[0]
    adjacent = model.training_target(e, q, target=6, compressed=2, recent=2, cached_cutoff=4)[0]
    assert not torch.allclose(overlap, adjacent)
    with pytest.raises(ValueError):
        model.training_target(e, q, target=6, compressed=2, recent=2, cached_cutoff=7)
    full = model._encode(e, runtime=True)[:, 4:6]
    truncated = model._encode(e[:, 4:6], runtime=True)
    assert not torch.allclose(full, truncated)  # train/serve receptive fields are not identical


def test_mars_literal_odds_and_weight_only_preference():
    c = torch.log(torch.tensor([[0.2, 0.7, 0.4]], dtype=torch.double))
    r = torch.log(torch.tensor([[0.9, 0.3, 0.5]], dtype=torch.double))
    cm = torch.tensor([[False, True, False]])
    rm = torch.tensor([[False, True, True]])
    gc, gr = c[cm].mean(), r[rm].mean()
    expected = -c.mean() - 0.5 * 2 * torch.nn.functional.logsigmoid(
        (gc - torch.log1p(-gc.exp())) - (gr - torch.log1p(-gr.exp()))
    )
    assert torch.allclose(
        mars.fapo_loss(c, r, cm, rm, weights=torch.tensor([2.0], dtype=torch.double)), expected
    )
    assert mars.posterior_weight(0.01, 0.3, 0.1) == 0.2
    assert mars.posterior_weight(0.5, 0.1, 0.1) == 3.0
    assert mars.orient_weak_pair(weak=True, chosen=0.1, rejected=0.2, scenario_mean=0.1, kappa=0.05)
    assert not mars.orient_weak_pair(
        weak=True, chosen=None, rejected=0.2, scenario_mean=0.1, kappa=0.05
    )
    with pytest.raises(ValueError):
        mars.fapo_loss(c, r, torch.zeros_like(cm), rm)
    with pytest.raises(ValueError):
        mars.posterior_weight(0.1, 0.2, 1.1)
    with pytest.raises(ValueError):
        mars.fapo_loss(c, r, cm, rm, generation_mask=[[True] * 3])
    with pytest.raises(ValueError):
        mars.fapo_loss(c, r, cm, rm, weights=[1.0])


def test_searchinject_feature_order_and_strict_threshold():
    x = si.risk_score(0.2, 0.4, 0.7, [1.0, 2.0, 3.0, 4.0, 5.0], -0.1)
    literal = 1 / (1 + math.exp(-(-0.1 + 0.2 + 0.8 + 2.1 + 4 * 0.08 + 5 * 0.14)))
    assert x == pytest.approx(literal)
    assert si.admit(["a", "b", "c"], [0.5, 0.6, 0.4], 0.5, context_size=2) == ("a", "c")
    result = si.calibrate_threshold([0.1, 0.2, 0.3, 0.3], [0.3, 0.4, 0.5], ceiling=0)
    assert result["threshold"] == 0.3 and result["calibration_recall"] == pytest.approx(2 / 3)
    assert not result["out_of_sample_guarantee"]
    with pytest.raises(ValueError):
        si.risk_score(0.1, 0.2, float("nan"), [1] * 5)
    with pytest.raises(ValueError):
        si.admit(["a", "a"], [0.1, 0.2], 0.3)


def test_searchinject_refill_can_increase_target_exposure():
    ranking = list(range(12))
    scores = [0.9, 0.9] + [0.1] * 10
    admitted = si.admit(ranking, scores, 0.8)
    assert 10 not in ranking[:10] and 10 in admitted
    # Fewer rejected carriers does not imply monotonic exposure after refill.
    assert admitted == tuple(range(2, 12))


def test_execjudges_all_boolean_combinations_and_floor():
    for subject, some, exact, dedicated in itertools.product([False, True], repeat=4):
        expected = 0 if not subject else 1 if not some else 3 if exact and dedicated else 2
        assert (
            ej.grade_dl(
                on_subject=subject, some_answer=some, exact_answer=exact, dedicated=dedicated
            )
            == expected
        )
    assert ej.consensus([3, 2, 3]) == 2
    assert ej.consensus([1, 0, 1]) == 0
    with pytest.raises(ValueError):
        ej.consensus([True, 1])
    with pytest.raises(ValueError):
        ej.grade_dl(on_subject=1, some_answer=True, exact_answer=True, dedicated=True)


@pytest.mark.parametrize("module", [mle, argus, mars, si, ej])
def test_bool_seed_rejected(module):
    with pytest.raises(ValueError):
        module.diagnostic(True)


def test_new_runner_does_not_mutate_previous_audit_namespace():
    import run_nov18_latest_components as previous
    import run_nov19_latest_components as current

    assert previous.AUDIT.name == 'nov18-latest'
    assert previous.BATCH == '2026-11-18-latest-components'
    assert current.AUDIT.name == 'nov19-latest'
    assert len(current.config()['components']) == 17
    assert sum(x['cuda'] for x in current.config()['components'].values()) == 7
    paths = current.execution_files()
    assert len(paths) == len(set(paths))
    assert 'scripts/run_nov18_latest_components.py' in paths
    assert 'scripts/run_nov19_latest_components.py' in paths
