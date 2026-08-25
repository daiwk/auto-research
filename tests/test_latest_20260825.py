from pathlib import Path

import numpy as np

from auto_research.agent_research.methods import build_agent
from auto_research.agent_research.models import AgentResearchConfig, AgentTask
from auto_research.post_training.models import PostTrainingConfig
from auto_research.post_training.runner import PostTrainingRunner


def test_srpo_and_erpo_execute_distinct_objectives(tmp_path: Path):
    diagnostics = {}
    for algorithm, marker in (("srpo", "reflection_patches"), ("erpo", "query_kl")):
        config = PostTrainingConfig(
            algorithm=algorithm, steps=4, maximum_examples=32,
            output_dir=tmp_path / algorithm, allow_network=False,
        )
        result, _ = PostTrainingRunner(config).run()
        latest = result.training["last_diagnostics"]
        assert marker in latest
        diagnostics[algorithm] = latest
    assert diagnostics["erpo"]["response_policy_kl_coefficient"] == 0.0


def test_agent_g2_and_autosaddler_have_distinct_state_transitions():
    task = AgentTask(
        "t0", "planning", "deploy safely", (), "ok",
        ("inspect", "patch", "verify"), ("inspect", "patch", "verify"),
    )
    g2 = build_agent("agent-g2", 8, np.random.default_rng(42))
    assert "gaussian-guidance" in g2.solve(task, 0)[2]
    assert g2.trajectory_rollouts == 1

    saddler = build_agent("autosaddler", 8, np.random.default_rng(42))
    assert "structured-patch" in saddler.solve(task, 0)[2]
    assert "durable-harness" in saddler.solve(task, 1)[2]
    assert saddler.global_verifier_calls == 1
    assert AgentResearchConfig(method="autosaddler").method == "autosaddler"
