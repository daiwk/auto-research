from pathlib import Path

import numpy as np

from auto_research.agent_research import AgentResearchConfig, AgentResearchRunner
from auto_research.foundation_latest_20260916 import agentkv_scores, loopspec_schedule, r4t_targets
from auto_research.post_training import PostTrainingConfig, PostTrainingRunner
from auto_research.post_training.latest_20260916 import (
    data_free_questions,
    depth_coupled_acceptance,
    discounted_credit,
    stride_prefix,
    turn_multiscale_weights,
    visual_preference_target,
)
from auto_research.reproductions.latest_20260916 import coarse_to_fine_tokens, gese_candidate_scores
from auto_research.reproductions.registry import get_adapter


def test_post_training_reference_kernels_preserve_invariants():
    assert np.allclose(discounted_credit([1, 0], gamma=.5), [1, 0])
    weights, turn_probs = turn_multiscale_weights([-.4, .2, .3, -.1])
    assert np.isclose(turn_probs.sum(), 1)
    assert np.all(weights >= 0)
    stop, restart = stride_prefix([-1., -1., -3.], threshold=-4.)
    assert (stop, restart) == (3, 2)
    questions = data_free_questions(np.zeros(5), np.random.default_rng(1), count=4)
    assert questions.shape == (4, 5)
    target = visual_preference_target([2., 0.], [0., 2.])
    assert np.isclose(target.sum(), 1) and target[0] > target[1]
    loss, mask = depth_coupled_acceptance([.8, .7, .6], 2)
    assert loss > 0 and np.count_nonzero(mask) == 2 and np.isclose(mask.sum(), 1)


def test_all_latest_post_training_methods_execute():
    for method in ("gamma-opd", "tlm-dre", "stride-opd", "df-opd", "opd-aha", "growmtp"):
        result, _ = PostTrainingRunner(PostTrainingConfig(
            algorithm=method, steps=3, maximum_examples=32, seed=42,
            allow_network=False, output_dir=Path("runs/tests"),
        )).run()
        assert result.training["last_diagnostics"]


def test_latest_agents_are_observation_safe_diagnostics():
    for method in ("fuse-evaluator", "harness-bandit", "sciencebuddy"):
        result, _ = AgentResearchRunner(AgentResearchConfig(
            method=method, episodes=24, seed=42, output_dir=Path("runs/tests"),
        )).run()
        assert result.diagnostics["diagnostic_only"] is True
        assert result.diagnostics["gold_fields_available_to_policy"] is False


def test_foundation_reference_kernels_are_bounded():
    rng = np.random.default_rng(4)
    targets, audit = r4t_targets(rng.normal(size=6), rng.normal(size=(12, 6)), count=4)
    assert targets.shape == (4, 6) and audit["vendi_score"] >= 1
    first, second, schedule = loopspec_schedule([.9, .8, .6, .4])
    assert 1 <= first <= 4 and 1 <= second <= 4 and schedule["expected_saved_depth"] >= 0
    scores, kv_audit = agentkv_scores(rng.normal(size=(10, 6)), {"plan": rng.normal(size=(3, 6))})
    assert scores.shape == (10,) and np.all((-1 <= scores) & (scores <= 1))
    assert kv_audit["phases"] == 1


def test_industrial_adapters_execute_without_fake_evolve_labels():
    for key in ("gese", "lazformer"):
        adapter = get_adapter(key)
        assert adapter.paper.has_online_ab
        assert adapter.evolve_operators == ()
        result = adapter.run(Path("data"), 42)
        assert result["manifest_ref"] == f"reproduction:{key}"
        assert result["setup"]["same_split_and_candidates"] is True

    data = __import__(
        "auto_research.reproductions.industrial_2026", fromlist=["load_industrial_data"]
    ).load_industrial_data(Path("data"))
    scores, selected = gese_candidate_scores(data, data.sequences.train[0])
    assert len(selected) == len(set(selected)) and np.isfinite(scores).all()
    tokens = coarse_to_fine_tokens(data.sequences.features, data.sequences.train[0])
    assert 1 < len(tokens) <= len(data.sequences.train[0])
