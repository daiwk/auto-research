from auto_research.agent_research import AgentResearchConfig, AgentResearchRunner
from auto_research.agent_research.models import DIAGNOSTIC_ONLY_METHODS


def test_latest_agent_kernels_are_observation_safe_and_executable(tmp_path):
    methods = ("autoviewmem", "mace", "arenaflow", "graphskillevo")
    for method in methods:
        result, _ = AgentResearchRunner(AgentResearchConfig(
            method=method, episodes=24, seed=42, output_dir=tmp_path,
        )).run()
        assert result.diagnostics["gold_fields_available_to_policy"] is False
        assert result.diagnostics["policy_training_performed"] is False
        assert result.metrics["joint_success"] >= 0.0


def test_latest_agent_diagnostics_are_not_misregistered_as_evolve_operators():
    assert DIAGNOSTIC_ONLY_METHODS == {
        "autoviewmem", "mace", "arenaflow", "graphskillevo",
    }
