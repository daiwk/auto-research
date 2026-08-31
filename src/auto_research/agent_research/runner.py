from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from .benchmarks import build_benchmark
from .methods import build_agent
from .models import AgentResearchConfig, AgentResearchResult


class AgentResearchRunner:
    def __init__(self, config: AgentResearchConfig):
        self.config = config

    def run(self) -> tuple[AgentResearchResult, Path]:
        config = self.config
        if config.benchmark == "osreward-mini":
            return self._run_osreward()
        if config.benchmark == "swebench-local":
            return self._run_code_benchmark()
        tasks = build_benchmark(config.benchmark, config.episodes, config.seed)
        agent = build_agent(config.method, config.memory_size, np.random.default_rng(config.seed))
        axis_totals, axis_correct = {}, {}
        trace = []
        answer_correct = plan_correct = 0
        for step, task in enumerate(tasks):
            answer, plan, source = agent.solve(task, step)
            answer_ok = answer == task.answer
            plan_ok = tuple(plan) == task.plan
            answer_correct += answer_ok
            plan_correct += plan_ok
            axis_totals[task.axis] = axis_totals.get(task.axis, 0) + 1
            axis_correct[task.axis] = axis_correct.get(task.axis, 0) + int(answer_ok and plan_ok)
            agent.observe(task, answer_ok, plan_ok, step)
            if step < 20:
                trace.append(
                    {
                        "task_id": task.task_id, "axis": task.axis, "source": source,
                        "answer_correct": answer_ok, "plan_correct": plan_ok,
                    }
                )
        count = len(tasks)
        metrics = {
            "answer_accuracy": answer_correct / count,
            "plan_success": plan_correct / count,
            "joint_success": sum(axis_correct.values()) / count,
            "average_cost": agent.cost / count,
        }
        axis_metrics = {
            axis: axis_correct[axis] / total for axis, total in axis_totals.items()
        }
        diagnostics = {
            "episodes": count,
            "memory_size": config.memory_size,
            "tool_evictions": agent.tool_evictions,
            "reused_plans": agent.reused_plans,
            "reasoning_steps": agent.reasoning_steps,
            "actions": agent.actions,
            "reflections": agent.reflections,
            "skills_created": agent.skills_created,
            "skills_reused": agent.skills_reused,
            "verification_retries": agent.verification_retries,
            "tree_nodes_expanded": agent.tree_nodes_expanded,
            "search_rollouts": agent.search_rollouts,
            "backtracks": agent.backtracks,
            "tool_call_candidates": agent.tool_call_candidates,
            "tool_calls_accepted": agent.tool_calls_accepted,
            "refinements": agent.refinements,
            "plans_created": agent.plans_created,
            "worker_calls": agent.worker_calls,
            "agent_messages": agent.agent_messages,
            "critic_rounds": agent.critic_rounds,
            "plan_explorations": agent.plan_explorations,
            "policy_updates": agent.policy_updates,
            "router_calls": agent.router_calls,
            "symbolic_expert_calls": agent.symbolic_expert_calls,
            "model_matches": agent.model_matches,
            "dependency_edges": agent.dependency_edges,
            "memories_retrieved": agent.memories_retrieved,
            "reflection_syntheses": agent.reflection_syntheses,
            "archival_writes": agent.archival_writes,
            "page_ins": agent.page_ins,
            "interrupts": agent.interrupts,
            "browser_queries": agent.browser_queries,
            "references_collected": agent.references_collected,
            "rejection_candidates": agent.rejection_candidates,
            "affordance_checks": agent.affordance_checks,
            "infeasible_skills_filtered": agent.infeasible_skills_filtered,
            "programs_generated": agent.programs_generated,
            "interpreter_calls": agent.interpreter_calls,
            "task_examples_retrieved": agent.task_examples_retrieved,
            "generation_pauses": agent.generation_pauses,
            "task_library_updates": agent.task_library_updates,
            "hindsight_skills": agent.hindsight_skills,
            "dense_credit_updates": agent.dense_credit_updates,
            "solver_value_queries": agent.solver_value_queries,
            "turn_credit_updates": agent.turn_credit_updates,
            "rollout_turns_saved": agent.rollout_turns_saved,
            "skill_graph_nodes": agent.skill_graph_nodes,
            "skill_graph_edges": agent.skill_graph_edges,
            "atomic_ops_reused": agent.atomic_ops_reused,
            "episodic_routes": agent.episodic_routes,
            "parametric_routes": agent.parametric_routes,
            "memory_consolidations": agent.memory_consolidations,
            "search_queries": agent.search_queries,
            "retrieved_tokens_masked": agent.retrieved_tokens_masked,
            "outcome_rewards": agent.outcome_rewards,
            "trajectory_rollouts": agent.trajectory_rollouts,
            "trajectory_filters": agent.trajectory_filters,
            "critic_baseline_updates": agent.critic_baseline_updates,
            "gradient_clips": agent.gradient_clips,
            "echo_trap_events": agent.echo_trap_events,
            "reasoning_rewards": agent.reasoning_rewards,
            "off_policy_reuses": agent.off_policy_reuses,
            "leave_one_out_updates": agent.leave_one_out_updates,
            "per_token_clips": agent.per_token_clips,
            "context_compressions": agent.context_compressions,
            "parallel_trajectory_groups": agent.parallel_trajectory_groups,
            "multi_turn_group_updates": agent.multi_turn_group_updates,
            "simulated_user_turns": agent.simulated_user_turns,
            "intent_refinements": agent.intent_refinements,
            "real_tool_responses": agent.real_tool_responses,
            "task_completion_rewards": agent.task_completion_rewards,
            "tools_exposed": agent.tools_exposed,
            "tools_available": agent.tools_available,
            "tool_exposure_reduction": (
                1.0 - agent.tools_exposed / agent.tools_available
                if agent.tools_available else 0.0
            ),
            "cost_aware_stops": agent.cost_aware_stops,
            "regret_weighted_labels": agent.regret_weighted_labels,
            "skill_document_updates": agent.skill_document_updates,
            "cross_task_skill_reuses": agent.cross_task_skill_reuses,
            "downstream_credit_updates": agent.downstream_credit_updates,
            "step_value_queries": agent.step_value_queries,
            "step_gae_updates": agent.step_gae_updates,
            "step_sequence_ratios": agent.step_sequence_ratios,
            "intra_group_advantages": agent.intra_group_advantages,
            "inter_group_advantages": agent.inter_group_advantages,
            "transition_targets": agent.transition_targets,
            "transition_accuracy": (
                agent.transition_correct / agent.transition_targets
                if agent.transition_targets else 0.0
            ),
            "reflective_groups": agent.reflective_groups,
            "success_failure_contrasts": agent.success_failure_contrasts,
            "privileged_guidance_updates": agent.privileged_guidance_updates,
            "world_rehearsals": agent.world_rehearsals,
            "rolewise_advantage_updates": agent.rolewise_advantage_updates,
            "private_rehearsals": agent.private_rehearsals,
            "recursive_belief_updates": agent.recursive_belief_updates,
            "pivotal_turns": agent.pivotal_turns,
            "observation_calibrations": agent.observation_calibrations,
            "scaffold_ablations": agent.scaffold_ablations,
            "local_verifier_calls": agent.local_verifier_calls,
            "global_verifier_calls": agent.global_verifier_calls,
            "memory_operations": agent.memory_operations,
            "coevolution_alternations": agent.coevolution_alternations,
            "router_updates": agent.router_updates,
            "memory_bank_updates": agent.memory_bank_updates,
            "fidelity": "mechanism reproduction on deterministic benchmark mini-suites",
        }
        # Paper-specific counters are intentionally surfaced explicitly.  The
        # public dashboard uses them to distinguish a real mechanism path from
        # the common deterministic answer/plan contract of the mini-suite.
        for name in (
            "harness_generations", "harness_repairs", "archive_distillations",
            "reopened_approaches", "versioned_edits",
            "tool_necessity_filters", "redundant_calls_avoided",
            "reliability_reflections", "prefix_hits", "critical_path_updates",
            "aging_promotions", "counterfactual_probes", "bayesian_edge_updates",
            "progress_predictions", "meta_gate_decisions", "budget_downgrades",
            "deciding_tool_attributions", "validation_ratchet_accepts",
            "validation_ratchet_rejects", "accuracy_gates",
            "complexity_calibrations", "diversity_accepts", "diversity_rejections",
            "state_snapshots", "subplan_revisions", "runtime_feedback_repairs",
        ):
            diagnostics[name] = getattr(agent, name, 0)
        phase_counts = getattr(agent, "phase_counts", None)
        if phase_counts is not None:
            diagnostics["phase_counts"] = dict(phase_counts)
        result = AgentResearchResult(
            config.method, config.benchmark, metrics, axis_metrics, diagnostics, trace
        )
        run_dir = config.output_dir / f"{config.method}-{config.benchmark}-seed{config.seed}"
        run_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "method": result.method, "benchmark": result.benchmark,
            "metrics": result.metrics, "axis_metrics": result.axis_metrics,
            "diagnostics": result.diagnostics, "trace": result.trace,
            "evaluation_protocol": {
                "tier": "l1_mechanism",
                "seeds": [config.seed],
                "formal_comparison": False,
                "claim_policy": (
                    "single-seed deterministic mechanism result; "
                    "do not claim a stable capability improvement"
                ),
            },
        }
        (run_dir / "metrics.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        from .report import render_report
        (run_dir / "report.md").write_text(render_report(result), encoding="utf-8")
        return result, run_dir

    def _run_osreward(self):
        from .osreward import evaluate_osreward

        config = self.config
        if config.method != "os-shepherd":
            raise ValueError("osreward-mini requires method os-shepherd")
        metrics, diagnostics, trace = evaluate_osreward(
            config.episodes, config.seed
        )
        result = AgentResearchResult(
            config.method,
            config.benchmark,
            metrics,
            {
                "success": metrics["success_recall"],
                "failure": metrics["fail_recall"],
            },
            diagnostics,
            trace,
        )
        run_dir = (
            config.output_dir
            / f"{config.method}-{config.benchmark}-seed{config.seed}"
        )
        run_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "method": result.method,
            "benchmark": result.benchmark,
            "metrics": result.metrics,
            "axis_metrics": result.axis_metrics,
            "diagnostics": result.diagnostics,
            "trace": result.trace,
        }
        (run_dir / "metrics.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        from .report import render_report
        (run_dir / "report.md").write_text(render_report(result), encoding="utf-8")
        return result, run_dir

    def _run_code_benchmark(self):
        from .code_benchmark import run_code_method

        config = self.config
        if config.method not in {
            "metagpt", "critic", "agent-lightning", "swe-agent", "openhands",
        }:
            raise ValueError(
                "swebench-local requires metagpt, critic, agent-lightning, "
                "swe-agent or openhands"
            )
        metrics, diagnostics, trace = run_code_method(
            config.method, config.episodes, config.memory_size
        )
        result = AgentResearchResult(
            config.method, config.benchmark, metrics,
            {"code_execution": metrics["joint_success"]}, diagnostics, trace,
        )
        run_dir = (
            config.output_dir
            / f"{config.method}-{config.benchmark}-seed{config.seed}"
        )
        run_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "method": result.method, "benchmark": result.benchmark,
            "metrics": result.metrics, "axis_metrics": result.axis_metrics,
            "diagnostics": result.diagnostics, "trace": result.trace,
        }
        (run_dir / "metrics.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        from .report import render_report
        (run_dir / "report.md").write_text(render_report(result), encoding="utf-8")
        return result, run_dir
