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
            "fidelity": "mechanism reproduction on deterministic benchmark mini-suites",
        }
        result = AgentResearchResult(
            config.method, config.benchmark, metrics, axis_metrics, diagnostics, trace
        )
        run_dir = config.output_dir / f"{config.method}-{config.benchmark}-seed{config.seed}"
        run_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "method": result.method, "benchmark": result.benchmark,
            "metrics": result.metrics, "axis_metrics": result.axis_metrics,
            "diagnostics": result.diagnostics, "trace": result.trace,
        }
        (run_dir / "metrics.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
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
