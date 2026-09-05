from pathlib import Path

import numpy as np

from auto_research.agent_research.methods import build_agent
from auto_research.agent_research.models import AgentTask
from auto_research.evolution.compatibility import operator_registry
from auto_research.evolution.papers import AGENT_MUTATIONS, INSTALLED_MUTATIONS, POST_TRAINING_MUTATIONS
from auto_research.post_training.models import PostTrainingConfig
from auto_research.post_training.runner import PostTrainingRunner
from auto_research.reproductions.registry import get_adapter


def test_recent_recommendation_adapters_are_independent_and_cpu_only():
    expected = {"rest": "2609.01240", "tgr": "2609.00986", "camie": "2608.30255", "setmir": "2608.30251"}
    for key, paper_id in expected.items():
        adapter = get_adapter(key)
        assert adapter.paper.arxiv_id == paper_id
        assert adapter.device_capabilities == ("cpu",)
        assert adapter.paper.online_ab


def test_gapo_executes_adaptive_clip(tmp_path: Path):
    result, _ = PostTrainingRunner(PostTrainingConfig(
        algorithm="gapo", steps=4, maximum_examples=32,
        output_dir=tmp_path / "gapo", allow_network=False,
    )).run()
    diagnostics = result.training["last_diagnostics"]
    assert diagnostics["adaptive_upper_clip"] >= 0.20
    assert "scarce_correct_headroom" in diagnostics


def test_draco_executes_dynamic_rubric_credit():
    task = AgentTask(
        "t", "planning", "deploy safely", ("inspect", "verify"), "ok",
        ("inspect", "patch", "verify"), ("inspect", "patch", "verify"),
    )
    agent = build_agent("draco", 8, np.random.default_rng(42))
    _, _, source = agent.solve(task, 0)
    assert source == "dynamic-rubric/step-attribution/closed-form-credit"
    assert agent.dynamic_rubrics > 0
    assert agent.credit_redistributions == 1


def test_recent_papers_are_evolve_visible():
    assert INSTALLED_MUTATIONS["2609.01240"][0] == "context:rest-dual-gate"
    assert POST_TRAINING_MUTATIONS["2609.00444"][0] == "gapo"
    assert AGENT_MUTATIONS["2609.04094"][0] == "critic:draco"
    registry = operator_registry()
    for operator in (
        "context:rest-dual-gate", "head:tgr-generation-reasoning",
        "context:coengagement-embedding", "context:setmir-query-set",
        "gapo", "critic:draco",
    ):
        assert operator in registry
