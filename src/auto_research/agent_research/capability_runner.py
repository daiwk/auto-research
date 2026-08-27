from __future__ import annotations

from dataclasses import dataclass
import json
import math
from pathlib import Path
from statistics import mean, stdev
from typing import Any

from .capability_benchmark import (
    CapabilityEnvironment,
    build_capability_tasks,
    capability_dataset_fingerprint,
    evaluate_episode,
)
from .capability_methods import CAPABILITY_METHODS, CapabilityPolicy


@dataclass(frozen=True)
class CapabilitySuiteConfig:
    methods: tuple[str, ...] = CAPABILITY_METHODS
    seeds: tuple[int, ...] = (42, 43, 44)
    episodes: int = 60
    output_dir: Path = Path("runs/agent-capability")

    def __post_init__(self) -> None:
        unknown = sorted(set(self.methods) - set(CAPABILITY_METHODS))
        if unknown:
            raise ValueError(f"unsupported capability methods: {', '.join(unknown)}")
        if not self.methods or not self.seeds or self.episodes < 12:
            raise ValueError("methods/seeds are required and episodes must be >= 12")


def _mean_metrics(rows: list[dict[str, float]]) -> dict[str, float]:
    return {
        key: mean(row[key] for row in rows)
        for key in rows[0]
    }


def _aggregate(rows: list[dict[str, float]]) -> dict[str, dict[str, float]]:
    result = {}
    for key in rows[0]:
        values = [row[key] for row in rows]
        deviation = stdev(values) if len(values) > 1 else 0.0
        result[key] = {
            "mean": mean(values),
            "std": deviation,
            "ci95_radius": 1.96 * deviation / math.sqrt(len(values)),
        }
    return result


def _run_seed(method: str, episodes: int, seed: int) -> dict[str, Any]:
    policy = CapabilityPolicy(method)
    episode_rows: list[dict[str, Any]] = []
    telemetry = {"retries": 0, "reflections": 0, "hints": 0, "skill_reuses": 0}
    trace = []
    for task in build_capability_tasks(episodes, seed):
        environment = CapabilityEnvironment(task)
        prediction = policy.solve(task.observation, environment.call)
        row = evaluate_episode(task, prediction.answer, environment)
        episode_rows.append(row)
        for key in telemetry:
            telemetry[key] += int(getattr(prediction, key))
        if len(trace) < 20:
            trace.append({
                **row,
                "source": prediction.source,
                "calls": environment.calls,
            })
    failure_rows = [row for row in episode_rows if row["has_failure"]]
    total_calls = sum(float(row["tool_calls"]) for row in episode_rows)
    metrics = {
        "answer_accuracy": mean(bool(row["answer_ok"]) for row in episode_rows),
        "plan_exact_match": mean(bool(row["plan_ok"]) for row in episode_rows),
        "plan_step_f1": mean(float(row["plan_step_f1"]) for row in episode_rows),
        "joint_success": mean(bool(row["joint_ok"]) for row in episode_rows),
        "recovery_success_rate": mean(
            bool(row["joint_ok"]) for row in failure_rows
        ) if failure_rows else 0.0,
        "invalid_tool_rate": (
            sum(float(row["invalid_calls"]) for row in episode_rows)
            / max(1.0, total_calls)
        ),
        "average_tool_calls": total_calls / len(episode_rows),
        "average_cost": mean(float(row["cost"]) for row in episode_rows),
    }
    axis_metrics = {
        axis: mean(
            bool(row["joint_ok"]) for row in episode_rows if row["axis"] == axis
        )
        for axis in ("clean", "transient", "ambiguous", "combined")
    }
    return {
        "seed": seed,
        "metrics": metrics,
        "axis_metrics": axis_metrics,
        "telemetry": telemetry,
        "trace": trace,
    }


def render_capability_report(payload: dict[str, Any]) -> str:
    metrics = payload["metrics"]
    rows = "\n".join(
        f"| {name} | {value:.4f} |"
        for name, value in metrics.items()
    )
    seed_rows = "\n".join(
        f"| {row['seed']} | {row['metrics']['joint_success']:.4f} | "
        f"{row['metrics']['plan_step_f1']:.4f} | {row['metrics']['average_cost']:.4f} |"
        for row in payload["seed_results"]
    )
    return f"""# Agent L2 capability report: {payload['method']}

> 该评测在接口层隔离 evaluator 的 oracle labels。Agent 只能看到 observation、工具描述和
> 调用后的反馈，不能读取 reference answer 或 plan。

## 三 seed 汇总

| 指标 | 均值 |
|---|---:|
{rows}

| Seed | Joint success | Plan step F1 | Average cost |
|---:|---:|---:|---:|
{seed_rows}

## 口径

- benchmark：`toolroute-l2-v1`
- episodes/seed：{payload['diagnostics']['episodes_per_seed']}
- oracle fields exposed：`false`
- formal comparison：`{str(payload['evaluation_protocol']['formal_comparison']).lower()}`
"""


def run_capability_suite(config: CapabilitySuiteConfig) -> dict[str, dict[str, Any]]:
    config.output_dir.mkdir(parents=True, exist_ok=True)
    fingerprint = capability_dataset_fingerprint(config.episodes, config.seeds)
    results = {}
    for method in config.methods:
        seed_results = [_run_seed(method, config.episodes, seed) for seed in config.seeds]
        metric_rows = [row["metrics"] for row in seed_results]
        aggregate = _aggregate(metric_rows)
        payload = {
            "schema_version": 2,
            "manifest_ref": f"agent-research:{method}:toolroute-l2-v1",
            "method": method,
            "benchmark": "toolroute-l2",
            "dataset": "toolroute-l2-v1",
            "seeds": list(config.seeds),
            "metrics": _mean_metrics(metric_rows),
            "aggregate_metrics": aggregate,
            "seed_results": seed_results,
            "diagnostics": {
                "episodes_per_seed": config.episodes,
                "total_episodes": config.episodes * len(config.seeds),
                "oracle_fields_exposed": False,
                "public_observation_type": "CapabilityObservation",
                "hidden_labels": ["answer", "reference_plan"],
                "fidelity": "shared no-oracle deterministic capability benchmark",
            },
            "evaluation_protocol": {
                "tier": "l2_capability",
                "seeds": list(config.seeds),
                "formal_comparison": len(config.seeds) >= 3,
                "claim_policy": (
                    "shared no-oracle benchmark; compare only within toolroute-l2-v1"
                ),
            },
            "provenance": {
                "dataset_fingerprint": fingerprint,
                "artifact_path": "runtime output; committed copies declare their docs path",
                "original_code_commit": "current working tree",
            },
        }
        run_dir = config.output_dir / f"{method}-toolroute-l2-seeds{'-'.join(map(str, config.seeds))}"
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "metrics.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (run_dir / "report.md").write_text(
            render_capability_report(payload), encoding="utf-8",
        )
        results[method] = payload
    summary = {
        "schema_version": 2,
        "manifest_ref": "experiments:agent-toolroute-l2-runtime",
        "benchmark": "toolroute-l2-v1",
        "methods": list(config.methods),
        "seeds": list(config.seeds),
        "episodes_per_seed": config.episodes,
        "results": {method: payload["metrics"] for method, payload in results.items()},
        "evaluation_protocol": {
            "tier": "l2_capability",
            "seeds": list(config.seeds),
            "formal_comparison": len(config.seeds) >= 3,
            "claim_policy": (
                "shared no-oracle benchmark; compare only within toolroute-l2-v1"
            ),
        },
        "provenance": {
            "dataset_fingerprint": fingerprint,
            "artifact_path": str(config.output_dir / "summary.json"),
            "original_code_commit": "current working tree",
        },
    }
    (config.output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    return results
