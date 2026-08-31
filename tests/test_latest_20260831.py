from pathlib import Path

import numpy as np

from auto_research.agent_research.methods import build_agent
from auto_research.agent_research.models import AgentResearchConfig, AgentTask
from auto_research.agent_research.runner import AgentResearchRunner
from auto_research.evolution.compatibility import operator_registry
from auto_research.evolution.papers import AGENT_MUTATIONS, POST_TRAINING_MUTATIONS
from auto_research.foundation_methods import CritiqueExample, build_criticl_prompt, select_criticl_examples
from auto_research.post_training.models import PostTrainingConfig
from auto_research.post_training.runner import PostTrainingRunner


def test_late_august_post_training_mechanisms_execute(tmp_path: Path):
    expectations = {
        "rlvr-fusion": "task_vector_cosine_mean",
        "video-opsd": "evidence_token_weight_mean",
        "normalized-dpo": "centered_softplus_loss",
    }
    for algorithm, marker in expectations.items():
        result, _ = PostTrainingRunner(PostTrainingConfig(
            algorithm=algorithm, steps=4, maximum_examples=32,
            output_dir=tmp_path / algorithm, allow_network=False,
        )).run()
        assert marker in result.training["last_diagnostics"]
        assert result.training["rollout_policy_refreshes"] >= 0


def test_late_august_agent_mechanisms_execute(tmp_path: Path):
    task = AgentTask(
        "t0", "planning", "deploy safely", ("repo",), "ok",
        ("inspect", "patch", "verify"), ("inspect", "patch", "verify"),
    )
    expectations = {
        "redevoagent": ("validation-ratchet", "validation_ratchet_accepts"),
        "ace-data": ("diversity-support", "diversity_accepts"),
        "deeprepro": ("state-aware-subplan", "state_snapshots"),
    }
    for method, (source_marker, counter) in expectations.items():
        agent = build_agent(method, 8, np.random.default_rng(42))
        assert source_marker in agent.solve(task, 0)[2]
        assert getattr(agent, counter) > 0
        result, _ = AgentResearchRunner(AgentResearchConfig(
            method=method, episodes=12, output_dir=tmp_path / method,
        )).run()
        assert counter in result.diagnostics


def test_criticl_retrieves_failure_modes_without_oracle_answer():
    bank = (
        CritiqueExample("add two fractions", "added denominators", "fractions", "align denominators first"),
        CritiqueExample("add two lengths", "mixed centimeters and meters", "units", "normalize units"),
        CritiqueExample("subtract signed values", "dropped the sign", "sign", "verify the sign"),
    )
    static = select_criticl_examples("add two fractions", bank, mode="static", maximum_examples=2)
    dynamic = select_criticl_examples("convert units before adding values", bank, mode="dynamic", maximum_examples=1)
    assert static == bank[:2]
    assert dynamic == (bank[1],)
    prompt, diagnostics = build_criticl_prompt("convert units", bank, mode="dynamic", maximum_examples=1)
    assert "normalize units" in prompt
    assert diagnostics["critbank_size"] == 3
    assert diagnostics["retrieved_critiques"] == 1
    assert diagnostics["online_weak_model_calls"] == 0


def test_late_august_batch_is_evolve_visible_where_executable():
    registry = operator_registry()
    for paper_id, operator in {
        "2608.27409": "rlvr-fusion",
        "2608.27065": "video-opsd",
        "2608.27032": "normalized-dpo",
    }.items():
        assert POST_TRAINING_MUTATIONS[paper_id][0] == operator
        assert operator in registry
    for paper_id, operator in {
        "2608.27439": "policy:redevoagent",
        "2608.27260": "memory:ace-data",
        "2608.26557": "planner:deeprepro",
    }.items():
        assert AGENT_MUTATIONS[paper_id][0] == operator
        assert operator in registry
