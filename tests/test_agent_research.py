from pathlib import Path

import pytest

from auto_research.agent_research import AgentResearchConfig, AgentResearchRunner


@pytest.mark.parametrize("method", ["long-context", "u-mem", "legomem", "memtool"])
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
