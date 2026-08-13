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
        "tapo", "grsd", "envace",
        "agent-opsd", "ocsd", "vermem", "coevo-mem",
        "deepresearcher", "retool", "toolrl", "sage", "memskill",
        "memento-skills", "searl", "agent0",
        "agent-r1", "camel", "toolbench", "gaia",
        "evoharness-rl", "vag", "gse", "cipo", "state2state",
        "harnessopt-bench", "codegrep", "memorycpt", "hindsearch",
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


@pytest.mark.parametrize(
    ("method", "diagnostics"),
    [
        ("tapo", ("transition_targets", "transition_accuracy")),
        (
            "grsd",
            ("reflective_groups", "success_failure_contrasts", "privileged_guidance_updates"),
        ),
        (
            "envace",
            ("world_rehearsals", "rolewise_advantage_updates", "private_rehearsals"),
        ),
    ],
)
def test_latest_agentic_rl_mechanisms_are_observable(
    tmp_path: Path, method: str, diagnostics: tuple[str, ...]
):
    result, _ = AgentResearchRunner(
        AgentResearchConfig(
            method=method,
            benchmark="planbench-mini",
            episodes=24,
            output_dir=tmp_path,
        )
    ).run()
    assert result.metrics["joint_success"] == 1
    for diagnostic in diagnostics:
        assert result.diagnostics[diagnostic] > 0


@pytest.mark.parametrize(
    ("method", "diagnostics"),
    [
        ("agent-opsd", ("recursive_belief_updates", "pivotal_turns")),
        ("ocsd", ("observation_calibrations", "scaffold_ablations")),
        ("vermem", ("local_verifier_calls", "global_verifier_calls", "memory_operations")),
        ("coevo-mem", ("coevolution_alternations", "router_updates", "memory_bank_updates")),
    ],
)
def test_closed_audit_agent_mechanisms_are_observable(
    tmp_path: Path, method: str, diagnostics: tuple[str, ...]
):
    result, _ = AgentResearchRunner(AgentResearchConfig(
        method=method, benchmark="planbench-mini", episodes=36, output_dir=tmp_path,
    )).run()
    assert result.metrics["joint_success"] == 1.0
    for diagnostic in diagnostics:
        assert result.diagnostics[diagnostic] > 0


@pytest.mark.parametrize(
    ("method", "diagnostics"),
    [
        ("deepresearcher", ("search_queries", "references_collected")),
        ("retool", ("real_tool_responses", "verification_retries")),
        ("toolrl", ("tool_call_candidates", "dense_credit_updates")),
        ("sage", ("skills_created", "cross_task_skill_reuses")),
        ("memskill", ("memory_operations", "skill_document_updates")),
        ("memento-skills", ("memory_operations", "skills_reused")),
        ("searl", ("skill_graph_nodes", "memory_bank_updates")),
        ("agent0", ("trajectory_rollouts", "simulated_user_turns")),
    ],
)
def test_global_p0_agent_mechanisms_are_observable(
    tmp_path: Path, method: str, diagnostics: tuple[str, ...]
):
    result, _ = AgentResearchRunner(AgentResearchConfig(
        method=method, benchmark="planbench-mini", episodes=36, output_dir=tmp_path,
    )).run()
    for diagnostic in diagnostics:
        assert result.diagnostics[diagnostic] > 0


@pytest.mark.parametrize(
    ("method", "benchmark", "diagnostics"),
    [
        ("agent-r1", "planbench-mini", ("transition_targets", "step_value_queries", "step_gae_updates")),
        ("camel", "planbench-mini", ("agent_messages", "reasoning_steps")),
        ("toolbench", "scalemcp-mini", ("task_library_updates", "tools_exposed", "interpreter_calls")),
        ("gaia", "gaia-mini", ("tool_calls_accepted", "local_verifier_calls")),
    ],
)
def test_global_p1_agent_mechanisms_are_observable(
    tmp_path: Path, method: str, benchmark: str, diagnostics: tuple[str, ...]
):
    result, _ = AgentResearchRunner(AgentResearchConfig(
        method=method, benchmark=benchmark, episodes=24, output_dir=tmp_path,
    )).run()
    assert result.metrics["joint_success"] == 1.0
    for diagnostic in diagnostics:
        assert result.diagnostics[diagnostic] > 0


@pytest.mark.parametrize(
    ("method", "benchmark", "diagnostics"),
    [
        ("evoharness-rl", "planbench-mini", ("policy_updates", "skill_document_updates")),
        ("vag", "planbench-mini", ("affordance_checks", "local_verifier_calls", "skills_created")),
        ("gse", "planbench-mini", ("skill_graph_nodes", "skill_graph_edges", "skills_reused")),
        ("cipo", "scalemcp-mini", ("search_queries", "dense_credit_updates", "outcome_rewards")),
        ("state2state", "planbench-mini", ("trajectory_rollouts", "local_verifier_calls", "outcome_rewards")),
        ("harnessopt-bench", "planbench-mini", ("trajectory_rollouts", "local_verifier_calls", "policy_updates")),
        ("codegrep", "scalemcp-mini", ("tool_call_candidates", "tool_calls_accepted", "dense_credit_updates")),
        ("memorycpt", "planbench-mini", ("memory_operations", "memories_retrieved", "context_compressions")),
        ("hindsearch", "planbench-mini", ("reflections", "hindsight_skills", "dense_credit_updates")),
    ],
)
def test_20260809_agent_mechanisms_are_observable(
    tmp_path: Path, method: str, benchmark: str, diagnostics: tuple[str, ...]
):
    result, _ = AgentResearchRunner(AgentResearchConfig(
        method=method, benchmark=benchmark, episodes=36, memory_size=12, output_dir=tmp_path,
    )).run()
    for diagnostic in diagnostics:
        assert result.diagnostics[diagnostic] > 0


def test_sinkflex_rl_preserves_sink_and_compresses_long_context(tmp_path: Path):
    from auto_research.agent_research.latest_20260813 import sink_window_indices

    assert sink_window_indices(8, 3, 1) == (0, 5, 6, 7)
    result, _ = AgentResearchRunner(AgentResearchConfig(
        method="sinkflex-rl", benchmark="scalemcp-mini", episodes=24,
        memory_size=12, output_dir=tmp_path,
    )).run()
    assert result.metrics["joint_success"] == 1.0
    assert result.diagnostics["policy_updates"] > 0
    assert result.diagnostics["context_compressions"] > 0
    assert result.diagnostics["outcome_rewards"] > 0


def test_osreward_reports_both_class_recalls_and_leniency(tmp_path: Path):
    result, _ = AgentResearchRunner(
        AgentResearchConfig(
            method="os-shepherd",
            benchmark="osreward-mini",
            episodes=24,
            output_dir=tmp_path,
        )
    ).run()
    assert result.metrics["balanced_accuracy"] == 1.0
    assert result.metrics["success_recall"] == 1.0
    assert result.metrics["fail_recall"] == 1.0
    assert result.metrics["leniency_rate"] == 0.0


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


@pytest.mark.parametrize(
    ("method", "benchmark", "diagnostics"),
    [
        (
            "loop",
            "planbench-mini",
            ("off_policy_reuses", "leave_one_out_updates", "per_token_clips"),
        ),
        (
            "webagent-r1",
            "scalemcp-mini",
            (
                "context_compressions",
                "parallel_trajectory_groups",
                "multi_turn_group_updates",
            ),
        ),
        (
            "mua-rl",
            "scalemcp-mini",
            (
                "simulated_user_turns",
                "intent_refinements",
                "real_tool_responses",
                "task_completion_rewards",
            ),
        ),
    ],
)
def test_omitted_agentic_rl_mechanisms_are_observable(
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
    ("method", "diagnostics"),
    [
        ("gigpo", ("intra_group_advantages", "inter_group_advantages")),
        ("steppo", ("step_value_queries", "step_gae_updates", "step_sequence_ratios")),
    ],
)
def test_step_and_group_agentic_rl_are_observable(
    tmp_path: Path, method: str, diagnostics: tuple[str, ...]
):
    result, _ = AgentResearchRunner(
        AgentResearchConfig(
            method=method,
            benchmark="planbench-mini",
            episodes=24,
            memory_size=12,
            output_dir=tmp_path,
        )
    ).run()
    assert result.metrics["joint_success"] == 1
    for diagnostic in diagnostics:
        assert result.diagnostics[diagnostic] > 0
