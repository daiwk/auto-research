from pathlib import Path

import numpy as np

from auto_research.agent_research.methods import build_agent
from auto_research.agent_research.models import AgentResearchConfig
from auto_research.agent_research.runner import AgentResearchRunner
from auto_research.post_training.models import PostTrainingConfig
from auto_research.post_training.runner import PostTrainingRunner


POST = (
    "r2-opd", "sr-opsd", "opd2", "causal-opd", "smopd", "rstg",
    "sa-mrpo", "rubric-dropout", "erils", "crpo", "serpo", "iso-rlvr",
)
AGENT = (
    "sapo", "spade", "rtpo", "planpo", "trca", "loongreflect",
    "hymem", "openloopevolve", "pmcoder", "toollift", "hyperagent", "manta",
)


def test_b08_b09_objectives_execute_and_report_unique_mechanisms(tmp_path: Path):
    mechanism_ids = set()
    for key in POST:
        result, _ = PostTrainingRunner(PostTrainingConfig(
            algorithm=key, steps=12, maximum_examples=64, seed=42,
            allow_network=False, output_dir=tmp_path,
        )).run()
        assert all(np.isfinite(list(result.final.values())))
        diagnostics = result.training["last_diagnostics"]
        mechanism_ids.add(diagnostics["mechanism_id"])
        assert result.training["rollout_policy_refreshes"] >= 0
    assert len(mechanism_ids) == len(POST)


def test_b10_b11_agents_execute_distinct_mechanism_paths(tmp_path: Path):
    sources = set()
    for key in AGENT:
        config = AgentResearchConfig(
            method=key, benchmark="planbench-mini", episodes=12,
            memory_size=8, seed=42, output_dir=tmp_path,
        )
        agent = build_agent(key, 8, np.random.default_rng(42))
        sources.add(agent.source)
        result, _ = AgentResearchRunner(config).run()
        assert result.metrics["joint_success"] == 1.0
        assert result.diagnostics["policy_updates"] > 0
    assert len(sources) == len(AGENT)

