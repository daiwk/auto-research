from pathlib import Path

import pytest

from auto_research.agent_research import AgentResearchConfig, AgentResearchRunner


@pytest.mark.parametrize(
    "method",
    ["long-context", "react", "reflexion", "voyager", "u-mem", "legomem", "memtool"],
)
def test_agent_methods_run_and_write_trace(tmp_path: Path, method: str):
    result, run_dir = AgentResearchRunner(
        AgentResearchConfig(
            method=method,
            episodes=24,
            memory_size=6,
            output_dir=tmp_path,
        )
    ).run()
    assert 0 <= result.metrics["joint_success"] <= 1
    assert result.metrics["average_cost"] >= 0
    assert result.trace
    assert (run_dir / "metrics.json").exists()
    assert (run_dir / "report.md").exists()


def test_legomem_reuses_procedures(tmp_path: Path):
    result, _ = AgentResearchRunner(
        AgentResearchConfig(
            method="legomem",
            benchmark="planbench-mini",
            episodes=36,
            memory_size=16,
            output_dir=tmp_path,
        )
    ).run()
    assert result.diagnostics["reused_plans"] > 0


def test_react_exposes_reason_action_loop(tmp_path: Path):
    result, _ = AgentResearchRunner(
        AgentResearchConfig(
            method="react",
            benchmark="scalemcp-mini",
            episodes=24,
            output_dir=tmp_path,
        )
    ).run()
    assert result.diagnostics["reasoning_steps"] > 0
    assert result.diagnostics["actions"] == result.diagnostics["reasoning_steps"]


def test_reflexion_learns_from_verbal_feedback(tmp_path: Path):
    result, _ = AgentResearchRunner(
        AgentResearchConfig(
            method="reflexion",
            benchmark="planbench-mini",
            episodes=36,
            memory_size=16,
            output_dir=tmp_path,
        )
    ).run()
    assert result.diagnostics["reflections"] > 0
    assert 0 < result.metrics["joint_success"] < 1


def test_voyager_builds_and_reuses_skill_library(tmp_path: Path):
    result, _ = AgentResearchRunner(
        AgentResearchConfig(
            method="voyager",
            benchmark="planbench-mini",
            episodes=36,
            memory_size=24,
            output_dir=tmp_path,
        )
    ).run()
    assert result.diagnostics["skills_created"] > 0
    assert result.diagnostics["skills_reused"] > 0
    assert result.diagnostics["verification_retries"] > 0
