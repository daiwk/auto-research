from pathlib import Path

import pytest

from auto_research.agent_research import AgentResearchConfig, AgentResearchRunner


@pytest.mark.parametrize(
    "method",
    [
        "long-context", "react", "reflexion", "voyager",
        "tree-of-thoughts", "lats", "toolformer",
        "self-refine", "rewoo", "autogen", "pearl",
        "u-mem", "legomem", "memtool",
        "mrkl", "hugginggpt", "generative-agents", "memgpt",
        "webgpt", "saycan", "pal", "art",
    ],
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


@pytest.mark.parametrize(
    ("method", "benchmark"),
    [
        ("tree-of-thoughts", "planbench-mini"),
        ("lats", "planbench-mini"),
        ("toolformer", "scalemcp-mini"),
    ],
)
def test_classic_search_and_tool_agents_expose_their_mechanisms(
    tmp_path: Path, method: str, benchmark: str
):
    result, _ = AgentResearchRunner(
        AgentResearchConfig(
            method=method,
            benchmark=benchmark,
            episodes=24,
            memory_size=12,
            output_dir=tmp_path,
        )
    ).run()
    assert result.metrics["joint_success"] == 1
    if method == "toolformer":
        assert result.diagnostics["tool_calls_accepted"] > 0
        assert (
            result.diagnostics["tool_call_candidates"]
            > result.diagnostics["tool_calls_accepted"]
        )
    else:
        assert result.diagnostics["tree_nodes_expanded"] > 0
        assert result.diagnostics["backtracks"] > 0


@pytest.mark.parametrize(
    ("method", "diagnostic"),
    [
        ("self-refine", "refinements"),
        ("rewoo", "worker_calls"),
        ("autogen", "agent_messages"),
        ("pearl", "policy_updates"),
    ],
)
def test_refinement_multi_agent_and_adaptive_planning_mechanisms(
    tmp_path: Path, method: str, diagnostic: str
):
    result, _ = AgentResearchRunner(
        AgentResearchConfig(
            method=method,
            benchmark="planbench-mini",
            episodes=36,
            memory_size=16,
            output_dir=tmp_path,
        )
    ).run()
    assert result.metrics["joint_success"] == 1
    assert result.diagnostics[diagnostic] > 0
    if method == "pearl":
        assert result.diagnostics["plan_explorations"] > 0
        assert result.diagnostics["reused_plans"] > 0


@pytest.mark.parametrize(
    ("method", "diagnostic"),
    [
        ("metagpt", "role_messages"),
        ("critic", "critic_rounds"),
        ("agent-lightning", "credit_updates"),
        ("swe-agent", "actual_file_edits"),
        ("openhands", "actual_subprocess_commands"),
    ],
)
def test_code_agents_edit_real_files_and_execute_regression_tests(
    tmp_path: Path, method: str, diagnostic: str
):
    result, run_dir = AgentResearchRunner(
        AgentResearchConfig(
            method=method,
            benchmark="swebench-local",
            episodes=12,
            memory_size=6,
            output_dir=tmp_path,
        )
    ).run()
    assert result.diagnostics["baseline_failures"] == 12
    assert result.metrics["joint_success"] == 1
    assert result.diagnostics["actual_subprocess_commands"] >= 24
    assert result.diagnostics[diagnostic] > 0
    assert any(
        event["event"] == "command"
        for row in result.trace for event in row["events"]
    )
    assert (run_dir / "metrics.json").exists()


@pytest.mark.parametrize(
    ("method", "benchmark", "diagnostics"),
    [
        ("mrkl", "scalemcp-mini", ("router_calls", "symbolic_expert_calls")),
        ("hugginggpt", "planbench-mini", ("model_matches", "dependency_edges")),
        (
            "generative-agents",
            "evomem-mini",
            ("memories_retrieved", "reflection_syntheses"),
        ),
        ("memgpt", "evomem-mini", ("archival_writes", "page_ins", "interrupts")),
    ],
)
def test_missing_classic_agent_mechanisms_are_observable(
    tmp_path: Path,
    method: str,
    benchmark: str,
    diagnostics: tuple[str, ...],
):
    result, _ = AgentResearchRunner(
        AgentResearchConfig(
            method=method,
            benchmark=benchmark,
            episodes=36,
            memory_size=8,
            output_dir=tmp_path,
        )
    ).run()
    assert result.metrics["joint_success"] == 1
    for diagnostic in diagnostics:
        assert result.diagnostics[diagnostic] > 0


@pytest.mark.parametrize(
    ("method", "benchmark", "diagnostics"),
    [
        (
            "webgpt",
            "scalemcp-mini",
            ("references_collected", "rejection_candidates"),
        ),
        (
            "saycan",
            "planbench-mini",
            ("affordance_checks", "infeasible_skills_filtered"),
        ),
        ("pal", "scalemcp-mini", ("programs_generated", "interpreter_calls")),
        (
            "art",
            "planbench-mini",
            ("task_examples_retrieved", "generation_pauses", "task_library_updates"),
        ),
    ],
)
def test_p1_agent_candidate_mechanisms_are_observable(
    tmp_path: Path,
    method: str,
    benchmark: str,
    diagnostics: tuple[str, ...],
):
    result, _ = AgentResearchRunner(
        AgentResearchConfig(
            method=method,
            benchmark=benchmark,
            episodes=36,
            memory_size=12,
            output_dir=tmp_path,
        )
    ).run()
    assert result.metrics["joint_success"] == 1
    for diagnostic in diagnostics:
        assert result.diagnostics[diagnostic] > 0


@pytest.mark.parametrize(
    ("method", "benchmark", "diagnostics"),
    [
        ("seed", "planbench-mini", ("hindsight_skills", "dense_credit_updates")),
        ("cast", "planbench-mini", ("solver_value_queries", "turn_credit_updates")),
        ("turn-opd", "scalemcp-mini", ("rollout_turns_saved",)),
        (
            "hiskill",
            "planbench-mini",
            ("skill_graph_nodes", "skill_graph_edges", "atomic_ops_reused"),
        ),
        (
            "unimem",
            "evomem-mini",
            ("episodic_routes", "parametric_routes", "memory_consolidations"),
        ),
    ],
)
def test_20260729_agentic_rl_and_memory_mechanisms_are_observable(
    tmp_path: Path,
    method: str,
    benchmark: str,
    diagnostics: tuple[str, ...],
):
    result, _ = AgentResearchRunner(
        AgentResearchConfig(
            method=method,
            benchmark=benchmark,
            episodes=36,
            memory_size=12,
            output_dir=tmp_path,
        )
    ).run()
    for diagnostic in diagnostics:
        assert result.diagnostics[diagnostic] > 0


@pytest.mark.parametrize(
    ("method", "benchmark", "diagnostics"),
    [
        (
            "search-r1",
            "scalemcp-mini",
            ("search_queries", "retrieved_tokens_masked", "outcome_rewards"),
        ),
        (
            "ragen",
            "planbench-mini",
            (
                "trajectory_rollouts",
                "trajectory_filters",
                "critic_baseline_updates",
                "gradient_clips",
                "echo_trap_events",
                "reasoning_rewards",
            ),
        ),
    ],
)
def test_classic_agentic_rl_mechanisms_are_observable(
    tmp_path: Path,
    method: str,
    benchmark: str,
    diagnostics: tuple[str, ...],
):
    result, _ = AgentResearchRunner(
        AgentResearchConfig(
            method=method,
            benchmark=benchmark,
            episodes=36,
            memory_size=12,
            output_dir=tmp_path,
        )
    ).run()
    assert result.metrics["joint_success"] == 1
    for diagnostic in diagnostics:
        assert result.diagnostics[diagnostic] > 0
