from __future__ import annotations

import numpy as np
import pytest

from auto_research.agent_research.methods import build_agent
from auto_research.agent_research.models import AgentResearchConfig, AgentTask
from auto_research.agent_research.runner import AgentResearchRunner
from auto_research.evolution.composable import AgentEvolutionEvaluator
from auto_research.evolution.models import Genome


METHODS = ("procedural-graphs", "memforest", "feedback-scaffold", "maple")


@pytest.mark.parametrize("method", METHODS)
def test_latest_agents_abstain_without_public_evidence(method):
    hidden = AgentTask(
        "hidden", "tools", "inspect then verify", ("unrelated public fact",),
        "secret", ("inspect", "verify"), ("inspect", "verify"),
    )
    answer, plan, source = build_agent(
        method, 8, np.random.default_rng(42)
    ).solve(hidden, 0)
    assert answer == ""
    assert plan == ()
    assert source


@pytest.mark.parametrize("method", METHODS)
def test_latest_agents_run_as_observation_only_diagnostics(tmp_path, method):
    result, run_dir = AgentResearchRunner(AgentResearchConfig(
        method=method, episodes=12, memory_size=8,
        output_dir=tmp_path, seed=42,
    )).run()
    assert run_dir.joinpath("metrics.json").is_file()
    assert result.diagnostics["gold_fields_available_to_policy"] is False
    assert result.diagnostics["tool_execution_performed"] is False
    assert result.diagnostics["promotion_eligible"] is False


def test_feedback_scaffold_switches_from_guidance_to_observation(tmp_path):
    result, _ = AgentResearchRunner(AgentResearchConfig(
        method="feedback-scaffold", episodes=12, memory_size=8,
        output_dir=tmp_path, seed=42,
    )).run()
    assert result.diagnostics["early_action_guidance"] > 0
    assert result.diagnostics["late_stage_enrichments"] > 0


@pytest.mark.parametrize(
    ("genome", "metric"),
    (
        (Genome(agent_planner="procedural-graphs"), "procedural_graph_edges"),
        (Genome(agent_memory="memforest"), "event_tree_partitions"),
        (Genome(agent_critic="feedback-scaffold"), "feedback_scaffold_updates"),
        (Genome(agent_planner="maple"), "maple_program_reuses"),
    ),
)
def test_latest_agent_paper_operators_execute_in_evolve_diagnostic(genome, metric):
    evaluator = AgentEvolutionEvaluator("evomem-mini", (42,), episodes=24)
    values = evaluator._run(genome, 42)
    assert metric in values
    assert values[metric] > 0
