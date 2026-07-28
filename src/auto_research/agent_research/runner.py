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
