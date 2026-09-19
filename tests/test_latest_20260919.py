from __future__ import annotations

import numpy as np
import pytest

from auto_research.agent_research import AgentResearchConfig, AgentResearchRunner
from auto_research.foundation_latest_20260919 import aspire_schedule, dqwen35_hybrid, fit_recall_head, on_demand_attention
from auto_research.post_training import PostTrainingConfig, PostTrainingRunner
from auto_research.post_training.latest_20260919 import adaptive_retirement, comparison_oracle_direction, trajectory_learnability_weights
from auto_research.reproductions.latest_20260919 import make_adapter
from auto_research.reproductions.latest_20260919 import dynamic_constrained_beam, hierarchical_identifiers


def test_post_training_mechanisms_and_dispatch(tmp_path):
    active, retired = adaptive_retirement([.2,.95,.96],[1,1,1],[.5,.2,.2])
    direction, compo = comparison_oracle_direction([2,0],[1,1], threshold=.1)
    weights, learn = trajectory_learnability_weights([[-2,-2],[-.1,-.1]],[[-1,-1],[-.2,-.2]])
    assert active.tolist() == [True, True, False]
    assert retired["retired_fraction"] > 0 and direction.tolist() == [1,-1]
    assert np.isclose(weights.sum(), 1) and learn["max_trajectory_weight"] > .5
    for method in ("retire-opd","compo","trajectory-learnability"):
        result, _ = PostTrainingRunner(PostTrainingConfig(algorithm=method, allow_network=False, maximum_examples=32, steps=2, seed=42, output_dir=tmp_path)).run()
        assert result.training["steps"] == 2


def test_agent_methods_are_observation_safe(tmp_path):
    for method in ("evoskill-gui","dependency-refinement","harness-design-study","cera-moa"):
        result, _ = AgentResearchRunner(AgentResearchConfig(method=method, episodes=24, seed=42, output_dir=tmp_path)).run()
        assert result.diagnostics["gold_fields_available_to_policy"] is False
        assert result.diagnostics["policy_training_performed"] is False


def test_foundation_reference_kernels():
    rng = np.random.default_rng(42)
    x = rng.normal(size=(12,8)); head = fit_recall_head(x, rng.normal(size=12))
    output, audit = on_demand_attention(rng.normal(size=8), x, x, rng.normal(size=(32,8)), rng.normal(size=(32,8)), head)
    hybrid, dq = dqwen35_hybrid(rng.normal(size=(10,8)), rng.normal(size=(8,8))/8, rng.normal(size=(8,8))/8)
    lengths, refresh, aspire = aspire_schedule([.2,.9], .1, 1, [1,8])
    assert output.shape == (8,) and audit["kv_retained"] == 32
    assert hybrid.shape == (10,8) and dq["bidirectional_passes"] == 2
    assert np.all(lengths >= 1) and refresh[0] and aspire["mean_draft_length"] >= 1


def test_cuda_kernels_reject_cpu():
    torch = pytest.importorskip("torch")
    from auto_research.foundation_latest_20260919 import aspire_cuda_kernel, dqwen35_cuda_kernel, oda_cuda_kernel
    x = torch.randn(4,4)
    with pytest.raises(ValueError): oda_cuda_kernel(x[0], x, x, x, x, x[0])
    with pytest.raises(ValueError): dqwen35_cuda_kernel(x, x, x)
    with pytest.raises(ValueError): aspire_cuda_kernel(torch.rand(4), .1, 1., torch.ones(4))


def test_angle_is_l2_and_has_online_evidence(tmp_path):
    adapter = make_adapter()
    features = np.eye(12)
    identifiers = hierarchical_identifiers(features)
    selected, audit = dynamic_constrained_beam(np.arange(12), identifiers, identifiers[:4], 3)
    assert adapter.paper.has_online_ab
    assert adapter.evaluation_tier.value == "l2_public_dataset"
    assert len(selected) <= 3 and audit["invalid_pruned"] > 0


def test_evolve_mappings_are_executable():
    from auto_research.evolution.papers import AGENT_MUTATIONS, POST_TRAINING_MUTATIONS
    for paper in ("2609.17653","2609.18417","2609.20804","2609.18779"):
        assert AGENT_MUTATIONS[paper][0].split(":",1)[1] in ("evoskill-gui","dependency-refinement","harness-design-study","cera-moa")
    for paper, method in (("2609.20784","retire-opd"),("2609.19144","compo"),("2609.18321","trajectory-learnability")):
        assert POST_TRAINING_MUTATIONS[paper][0] == method
