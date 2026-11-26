"""Independent formula, boundary and CPU-only checks for Nov26 post components."""

import copy
import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from auto_research.post_training import briar, feast


@pytest.mark.parametrize("seed", [3, 31, 97])
def test_briar_two_pass_matches_independent_dense_covariance(seed):
    rng = np.random.default_rng(seed)
    parents = np.array([-1, 0, 0, 1, 1, 2, 5, 5])
    rewards = [np.nan, np.nan, np.nan, 1., 0., np.nan, 0., 1.]
    lengths = np.r_[0., rng.uniform(160, 480, 7)]
    result = briar.smooth_tree(parents, rewards, lengths, root_mean=.3, root_variance=4.)
    mean, variance = briar.dense_reference(parents, rewards, lengths, result)
    np.testing.assert_allclose(result["means"], mean, atol=1e-12)
    np.testing.assert_allclose(result["variances"], variance, atol=1e-12)
    np.testing.assert_allclose(result["edge_advantages"][1:], mean[1:]-mean[parents[1:]], atol=1e-12)
    assert np.all(result["variances"] > 0)


def test_briar_jeffreys_frontier_and_boundary_scaling():
    out = briar.frontier_scores([0, 3, 6], [6, 6, 6])
    p = np.array([.5, 3.5, 6.5])/7
    np.testing.assert_allclose(out["probability"], p)
    np.testing.assert_allclose(out["priority"], p*(1-p)+.5*np.sqrt(p*(1-p)/8))
    np.testing.assert_array_equal(out["unresolved"], [False, True, False])
    result = briar.smooth_tree([-1, 0, 0], [np.nan, 0., 1.], [0, 200, 400], average_length=200)
    np.testing.assert_allclose(result["edge_variances"][1:], 2.2*.26*np.array([1.4, 1.8]))
    # Eq.5 is a modulation, not an exact hard martingale variance constraint.
    assert result["edge_variances"][1] > .25


def test_briar_minimal_absorption_and_clipped_recentered_lengths():
    parents = [-1, 0, 0, 1, 1]
    rewards, lengths = [np.nan, np.nan, 0, 1, 1], [0, 100, 200, 200, 600]
    # Explicit posterior values isolate frontier logic from the smoother.
    smooth = {"means": np.array([.7, .99, .1, .99, .99]), "variances": np.full(5, 1e-4)}
    rows = briar.absorbed_suffixes(parents, rewards, lengths, smooth)
    assert len(rows) == 1 and rows[0]["frontier"] == 1
    assert rows[0]["edge_paths"] == [[3], [4]]
    np.testing.assert_allclose(rows[0]["advantages"].sum(), 0, atol=1e-15)
    assert rows[0]["advantages"][0] > 0 > rows[0]["advantages"][1]
    assert briar.absorbed_suffixes(parents, rewards, lengths, smooth, min_spread=500) == []
    # One failed descendant prevents absorption regardless of posterior mean.
    assert briar.absorbed_suffixes(parents, [np.nan, np.nan, 0, 0, 1], lengths, smooth) == []


@pytest.mark.parametrize("parents,rewards,lengths", [
    ([-1, 2, 0], [np.nan, 1, 0], [0, 1, 1]),
    ([-1, 0], [0, 1], [0, 1]),
    ([-1, 0], [np.nan, .5], [0, 1]),
    ([-1, 0], [np.nan, 1], [0, 0]),
])
def test_briar_rejects_invalid_tree_contracts(parents, rewards, lengths):
    with pytest.raises(ValueError):
        briar.smooth_tree(parents, rewards, lengths)


def test_feast_exact_default_progressive_budget_and_stable_ties():
    plan = {0: list(range(32)), 1: list(range(32, 64)), 2: list(range(64, 96)), 3: list(range(96, 128))}
    out = feast.progressive_rollouts(plan, lambda prompt, n: np.zeros(n))
    assert out["total_rollouts"] == 1024
    assert set(out["spent_per_group"].values()) == {256}
    assert sorted(map(len, out["rewards"].values())) == [2]*64+[6]*32+[22]*32
    assert len(out["rewards"][0]) == 22 and len(out["rewards"][8]) == 6
    assert len(out["rewards"][16]) == 2
    assert out["signal_prompts"] == []


def test_feast_clusters_cannot_steal_each_others_reserved_budget():
    calls = []
    def sample(prompt, n):
        calls.append((prompt, n))
        return np.arange(n) % 2 if prompt < 4 else np.zeros(n)
    out = feast.progressive_rollouts({0: [0, 1, 2, 3], 1: [4, 5, 6, 7]}, sample)
    assert out["spent_per_group"] == {0: 32, 1: 32}
    assert sum(n for p, n in calls if p >= 4) == 32  # Entirely zero-signal cluster still served.


def test_feast_pilot_equal_feedback_and_signal_exposure_normalization():
    scheduler = feast.FeastScheduler(np.arange(12.).reshape(6, 2), atoms=2, seed=7)
    a = int(scheduler.assignment[0])
    same = np.flatnonzero(scheduler.assignment == a)
    p, q = map(int, same[:2])
    # Extra promoted successes must NOT bias the two-pilot attainment statistic.
    scheduler.observe({p: [0, 1]+[1]*20, q: [0, 0]}, total_budget=24)
    assert scheduler.m[a] == .25 and scheduler.u[a] == .5
    assert scheduler.trend[a] == 0
    scheduler.observe({p: [1, 1], q: [1, 0]}, total_budget=4)
    np.testing.assert_allclose(scheduler.m[a], .30)
    np.testing.assert_allclose(scheduler.trend[a], .05/(2/8))
    np.testing.assert_allclose(scheduler.slow_trend[a], .3*.2)
    other = 1-a
    assert scheduler.shortfall[other] == 14  # 12 + 2; zero service still accrues deficit.
    assert scheduler.m[other] == 0 and not scheduler.observed[other]


def test_feast_remaining_capacity_weights_and_prompt_cycle_exhaustion():
    x = np.arange(16., dtype=float).reshape(8, 2)
    scheduler = feast.FeastScheduler(x, atoms=2, seed=4)
    scheduler.groups[:] = 0
    one = scheduler.plan(selected_groups=1, prompts_per_group=4)[0]
    two = scheduler.plan(selected_groups=1, prompts_per_group=4)[0]
    assert len(set(one+two)) == 8 and not scheduler.unseen.any()
    _, weights = scheduler.group_weights(prompts_per_group=4)
    # Exposed weights are now stably rescaled, while the underlying exhausted
    # capacity score remains exactly the exploration floor.
    np.testing.assert_allclose(weights, 1.)
    _, log_scores = scheduler._group_log_scores(4)
    np.testing.assert_allclose(np.exp(log_scores), .05)
    three = scheduler.plan(selected_groups=1, prompts_per_group=4)[0]
    assert len(set(three)) == 4


def test_feast_failed_multicluster_plan_is_atomic_including_rng():
    vectors = [[0], [.01], [10], [10.01], [10.02], [20], [30], [31]]
    scheduler = feast.FeastScheduler(vectors, atoms=4, seed=0)
    scheduler.regroup(scheduler.vectors, seed=0, components=[2], semantic_dimensions=1)
    capacities = [int(np.isin(scheduler.assignment, np.flatnonzero(scheduler.groups == c)).sum())
                  for c in np.unique(scheduler.groups)]
    assert sorted(capacities) == [3, 5]
    unseen, cursor = scheduler.unseen.copy(), scheduler.cursor.copy()
    state = copy.deepcopy(scheduler.rng.bit_generator.state)
    with pytest.raises(ValueError, match="insufficient unique prompt capacity"):
        scheduler.plan(selected_groups=2, prompts_per_group=4)
    np.testing.assert_array_equal(scheduler.unseen, unseen)
    np.testing.assert_array_equal(scheduler.cursor, cursor)
    assert scheduler.rng.bit_generator.state == state
    # A smaller subsequent valid request must be identical to a fresh object;
    # the failed request neither consumes prompt exposure nor randomness.
    fresh = feast.FeastScheduler(vectors, atoms=4, seed=0)
    fresh.regroup(fresh.vectors, seed=0, components=[2], semantic_dimensions=1)
    assert scheduler.plan(selected_groups=2, prompts_per_group=2) == fresh.plan(
        selected_groups=2, prompts_per_group=2)


@pytest.mark.parametrize("temperature", [1e-4, 1e-320])
def test_feast_tiny_temperature_recomputes_remaining_cluster_masses(temperature):
    scheduler = feast.FeastScheduler(np.arange(24.).reshape(12, 2), atoms=3, seed=4)
    # Unequal priorities can underflow some *relative* masses; all three groups
    # still have to be drawable after higher-priority groups are removed.
    scheduler.u[:] = [0., .5, 1.]
    scheduler.m[:] = .5
    groups, weights = scheduler.group_weights(prompts_per_group=1, temperature=temperature)
    assert np.isfinite(weights).all() and weights.max() == 1 and weights.sum() > 0
    with np.errstate(all="raise"):
        plan = scheduler.plan(selected_groups=3, prompts_per_group=1, temperature=temperature)
    assert set(plan) == set(groups) and all(len(prompts) == 1 for prompts in plan.values())
    assert len(set(p for prompts in plan.values() for p in prompts)) == 3


@pytest.mark.parametrize("temperature", [0., -1., float("nan"), float("inf"), -float("inf"), True])
def test_feast_temperature_rejects_nonpositive_or_nonfinite_without_mutation(temperature):
    scheduler = feast.FeastScheduler(np.arange(16.).reshape(8, 2), atoms=2, seed=4)
    state = copy.deepcopy(scheduler.rng.bit_generator.state)
    for operation in [scheduler.group_weights, scheduler.plan]:
        with pytest.raises(ValueError, match="positive finite temperature"):
            operation(temperature=temperature)
    assert scheduler.unseen.all() and not scheduler.cursor.any()
    assert scheduler.rng.bit_generator.state == state


def test_feast_regrouping_uses_vectors_and_trend_preserving_atomic_history():
    rng = np.random.default_rng(7)
    scheduler = feast.FeastScheduler(rng.normal(size=(128, 10)), atoms=16, seed=7)
    scheduler.m[:] = np.linspace(0, 1, 16)
    scheduler.slow_trend[:] = np.linspace(-1, 1, 16)
    atomic, history = scheduler.assignment.copy(), scheduler.m.copy()
    out = scheduler.regroup(scheduler.vectors, seed=7, components=[4, 5, 6])
    assert out["features"].shape == (16, 9)
    np.testing.assert_allclose(out["features"][:, -1], scheduler.slow_trend)
    assert np.bincount(out["groups"]).min() >= 2
    np.testing.assert_array_equal(scheduler.assignment, atomic)
    np.testing.assert_array_equal(scheduler.m, history)
    assert np.isfinite(out["bic_before_repair"])


@pytest.mark.parametrize("module", [briar, feast])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostics_cpu_guard_boolean_checks_finite_scalars(module, seed):
    out = module.diagnostic(seed)
    assert out["evaluation_tier"] == "l1_mechanism" and out["diagnostic_only"]
    assert not out["training_executed"] and not module.REQUIRES_GPU_VALIDATION
    assert all(type(v) is bool and v for v in out["checks"].values()), out
    assert all(type(v) in (int, float) and np.isfinite(v) for v in out["metrics"].values())
    with pytest.raises(ValueError):
        module.diagnostic(seed, device="cuda")


@pytest.mark.parametrize("key,paper_id", [("briar", "2611.34746"), ("feast", "2611.33827"), ("care-opd", "2611.34756")])
def test_post_documents_metadata_translation_figure_provenance(key, paper_id):
    root = Path(__file__).resolve().parents[1]
    directory = root/f"docs/post-training/{paper_id}-{key}"
    source, english = (directory/"README.md").read_bytes(), (directory/"README-en.md").read_text()
    chinese = source.decode()
    assert f"<!-- source-sha256: {hashlib.sha256(source).hexdigest()} -->" in english
    assert "[简体中文](README.md)" in english
    for token in ("## 论文信息", "首次公开日期", "公司 / 作者机构", "原作者开源代码",
                  "本地adapter / 稳定键", "本地复现代码目录", "图片来自[原论文]", "版权归原作者所有",
                  "### 核心公式", "### 结果、负控与边界", "成本过高，不复现（审查 DONE）"):
        assert token in chinese
    provenance = json.loads((directory/"assets/provenance.json").read_text())
    assert hashlib.sha256((directory/"assets/paper-figure-01.png").read_bytes()).hexdigest() == provenance["asset_sha256"]
    assert provenance["visually_reviewed_on"] == "2026-11-26"
    if key == "care-opd":
        assert not (directory/"metrics").exists()
