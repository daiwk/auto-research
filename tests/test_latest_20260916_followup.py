from __future__ import annotations

import numpy as np

from auto_research.agent_research import AgentResearchConfig, AgentResearchRunner
from auto_research.foundation_latest_20260916_followup import (
    echo_candidates, echo_lossless_verify, persistent_recurrent_memory,
    register_chunk, reproducible_reduce, stacktok_select, videomm_select,
)
from auto_research.post_training import PostTrainingConfig, PostTrainingRunner
from auto_research.post_training.latest_20260916_followup import style_debiased_dpo, tiao_credit


def test_echo_candidates_and_lossless_correction():
    candidates, audit = echo_candidates([0, 2, 1], [2, 0, 1], [2], 1)
    assert 2 in candidates and len(candidates) == int(audit["candidate_count"])
    assert audit["early_bonus_mass"] > 0
    draft = np.asarray([[0.9, 0.1], [0.2, 0.8]])
    target = np.asarray([[0.1, 0.9], [0.8, 0.2]])
    accepted, correction, metrics = echo_lossless_verify(draft, target, [0.99, 0.0])
    assert accepted == 0 and correction is not None
    assert np.isclose(correction.sum(), 1.0)
    assert metrics["lossless_correction_used"] == 1


def test_multimodal_selectors_obey_budget():
    rng = np.random.default_rng(7)
    tokens, query = rng.normal(size=(24, 8)), rng.normal(size=8)
    micro, indices, video_audit = videomm_select(tokens, query, group_size=4, keep_groups=2)
    selected, stack_audit = stacktok_select(tokens, query, budget=6)
    assert len(micro) == len(indices) <= 12
    assert len(selected) == len(set(selected)) == 6
    assert 0 < video_audit["retained_fraction"] <= 0.5
    assert np.isclose(stack_audit["retained_fraction"], 0.25)


def test_memory_and_audit_kernels_preserve_contracts():
    rng = np.random.default_rng(9)
    hidden = rng.normal(size=(10, 6))
    output, state, audit = persistent_recurrent_memory(hidden, rng.normal(size=6), rng.normal(size=(6, 6)), rng.normal(size=(6, 6)), rng.normal(size=6))
    carried, carry_audit = register_chunk(rng.normal(size=(3, 6)), hidden, rng.normal(size=(6, 6)))
    left, first = reproducible_reduce([np.arange(8), np.arange(8) + 1])
    right, second = reproducible_reduce([np.arange(8), np.arange(8) + 1])
    assert output.shape == hidden.shape and state.shape == (6,)
    assert carried.shape == (3, 6) and carry_audit["cleared_text_tokens"] == 10
    assert audit["state_norm"] > 0
    assert np.array_equal(left, right) and first["state_hash"] == second["state_hash"]


def test_post_training_mechanisms_and_runner_dispatch():
    credit, tiao = tiao_credit([-1, -2, -3], [-2, -2, -1], 1.0)
    losses, sd = style_debiased_dpo([0.1, 0.9, 0.9], [1.0, 1.0, -1.0])
    assert np.count_nonzero(credit) >= 1 and tiao["trajectory_dependency"] > 0
    assert np.all(losses >= 0) and sd["inverted_pair_fraction"] > 0.5
    for method in ("tiao", "sd-dpo"):
        result, _ = PostTrainingRunner(PostTrainingConfig(algorithm=method, allow_network=False, maximum_examples=32, steps=2, seed=42)).run()
        assert result.training["steps"] == 2


def test_agent_followup_methods_are_observation_safe_diagnostics(tmp_path):
    for method in ("repoatlas", "interactive-memory"):
        result, _ = AgentResearchRunner(AgentResearchConfig(method=method, episodes=24, seed=42, output_dir=tmp_path)).run()
        assert result.diagnostics["gold_fields_available_to_policy"] is False
        assert result.diagnostics["policy_training_performed"] is False
        assert len(result.trace) >= 12


def test_agent_followup_methods_are_executable_evolve_mutations():
    from auto_research.evolution.papers import AGENT_MUTATIONS

    assert AGENT_MUTATIONS["2609.16936"][0] == "planner:repoatlas"
    assert AGENT_MUTATIONS["2609.17088"][0] == "memory:interactive-memory"
