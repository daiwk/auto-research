from pathlib import Path

import numpy as np
import pytest

from auto_research.agent_research import AgentResearchConfig, AgentResearchRunner
from auto_research.foundation_latest_20260914 import (
    dequantize_blocks,
    frames_on_demand,
    modality_value_rotate,
    multi_expert_opd,
    repetition_regularization,
    sensenova_patch_targets,
    similarity_contracting_windows,
    soft_musec_update,
    windowed_key_quantize,
)
from auto_research.post_training import PostTrainingConfig, PostTrainingRunner
from auto_research.reproductions.sirf.experiment import reproduce
from auto_research.evolution.composable import AgentEvolutionEvaluator, PostTrainingEvolutionEvaluator
from auto_research.evolution.models import Genome
from auto_research.evolution.papers import AGENT_MUTATIONS, POST_TRAINING_MUTATIONS


@pytest.mark.parametrize("algorithm,diagnostic", [
    ("nsd", "reasoning_gate_mean"),
    ("adaptive-opd-gate", "gate_signals"),
    ("locus", "subspace_rank"),
    ("tasco", "local_stability_variance"),
])
def test_post_training_mechanisms_execute(tmp_path, algorithm, diagnostic):
    result, _ = PostTrainingRunner(PostTrainingConfig(
        algorithm=algorithm, allow_network=False, maximum_examples=64,
        steps=8, seed=42, output_dir=tmp_path,
    )).run()
    assert diagnostic in result.training["last_diagnostics"]
    assert result.training["diagnostic_only"] is True


@pytest.mark.parametrize("method,diagnostic", [
    ("cobra-skills", "bandit_allocations"),
    ("ecdysis", "cross_instance_failures"),
    ("grounded-memory", "environment_probes"),
    ("toolgrad", "answer_first_generations"),
    ("prompts", "profile_bottlenecks"),
    ("searchatlas", "evidence_graph_edges"),
    ("skill-retention", "anchor_penalties"),
    ("t1-terminal-rl", "tito_tokens"),
])
def test_agent_mechanisms_do_not_claim_capability(tmp_path, method, diagnostic):
    result, _ = AgentResearchRunner(AgentResearchConfig(
        method=method, episodes=24, seed=42, output_dir=tmp_path,
    )).run()
    assert diagnostic in result.diagnostics
    assert result.diagnostics["gold_fields_available_to_policy"] is False
    assert result.diagnostics["promotion_eligible"] is False


def test_omnikvquant_reference_round_trip_and_modal_rotation():
    rng = np.random.default_rng(42)
    keys = rng.normal(size=(19, 8))
    blocks = windowed_key_quantize(keys, bits=2, window=4)
    restored = dequantize_blocks(blocks)
    assert restored.shape == keys.shape
    assert np.mean((restored - keys) ** 2) < 0.2
    rotated, matrices = modality_value_rotate(keys, np.repeat([0, 1], [10, 9]))
    assert rotated.shape == keys.shape
    assert set(matrices) == {0, 1}


def test_multimodal_data_and_routing_kernels():
    patches = np.arange(24, dtype=float).reshape(2, 4, 3)
    mask = np.asarray([[False, True, False, True], [True, False, True, False]])
    reconstructed = sensenova_patch_targets(patches, mask)
    assert reconstructed.shape == patches.shape
    delta, weights = multi_expert_opd(np.ones((2, 3, 4)), np.zeros((2, 3)))
    assert delta.shape == (2, 4)
    assert np.allclose(weights.sum(-1), 1)
    chosen, audit = frames_on_demand(
        np.asarray([1.0, 0.0]), np.asarray([0.0, 1.0]),
        np.asarray([[0.0, 1.0], [1.0, 0.0]]), maximum_frames=1,
    )
    assert chosen.tolist() == [0]
    assert audit["visual_need"] == 1


def test_data_sparsity_musec_and_swrouter_kernels():
    sparse = repetition_regularization(64, sparse_model=True)
    dense = repetition_regularization(64, sparse_model=False)
    assert sparse["dropout"] > dense["dropout"]
    update, audit = soft_musec_update(np.diag([8.0, 0.5]), clip=1.0)
    assert np.linalg.norm(update, 2) <= 1.000001
    assert audit["spectral_norm_after"] <= 1.0
    windows = similarity_contracting_windows(
        ["a", "b", "c"], np.asarray([[1.0, 0.0], [0.9, 0.1], [0.0, 1.0]])
    )
    assert windows == [["a", "b"], ["c"]]


def test_sirf_runs_heldout_threshold_protocol():
    result = reproduce(Path("data"), 42)
    assert result["setup"]["heldout_split"] is True
    assert result["method"]["precision"] >= 0.95
    assert result["manifest_ref"] == "reproduction:sirf"


@pytest.mark.parametrize("paper_id,operator", [
    ("2609.11699", "nsd"),
    ("2609.11768", "adaptive-opd-gate"),
    ("2609.11739", "locus"),
    ("2609.11393", "tasco"),
])
def test_post_training_paper_operator_is_executed(paper_id, operator, tmp_path):
    assert POST_TRAINING_MUTATIONS[paper_id][0] == operator
    evaluator = PostTrainingEvolutionEvaluator(
        tmp_path, "arithmetic-smoke", 3, (42,), False, maximum_examples=32,
    )
    assert operator in evaluator.executable_operators
    values, diagnostics = evaluator._run(
        Genome(post_training=operator, post_steps=3), 42, test=False,
    )
    assert values["accuracy"] >= 0
    assert diagnostics["steps"] == 3


@pytest.mark.parametrize("paper_id,field,value,metric", [
    ("2609.11682", "agent_policy", "cobra-skills", "bandit_allocations"),
    ("2609.11677", "agent_critic", "ecdysis", "feedback_scaffold_updates"),
    ("2609.11060", "agent_memory", "grounded-memory", "environment_probes"),
    ("2508.04086", "agent_tool_policy", "toolgrad", "textual_gradient_edits"),
    ("mlsys2026-prompts", "agent_planner", "prompts", "profiled_proposals"),
    ("2609.10901", "agent_verifier", "searchatlas", "evidence_graph_edges"),
    ("2609.10750", "agent_memory", "skill-retention", "anchor_replays"),
    ("2609.11042", "agent_policy", "t1-terminal-rl", "exact_token_replays"),
])
def test_agent_paper_operator_changes_executed_diagnostic(
    paper_id, field, value, metric,
):
    assert AGENT_MUTATIONS[paper_id][0].endswith(value)
    evaluator = AgentEvolutionEvaluator("planbench-mini", (42,), episodes=12)
    result = evaluator._run(
        Genome(architecture="composable-agent", **{field: value}), 42,
    )
    assert metric in result
    assert result[metric] > 0
