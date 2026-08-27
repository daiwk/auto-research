from __future__ import annotations

from dataclasses import dataclass
import json
import math
from pathlib import Path
from statistics import mean, stdev
from typing import Any

from .capability_benchmark import (
    AXES,
    CapabilityEnvironment,
    CapabilitySplit,
    build_capability_tasks,
    capability_dataset_fingerprint,
    evaluate_episode,
)
from .capability_methods import (
    CAPABILITY_ABLATIONS,
    CAPABILITY_METHODS,
    CapabilityPolicy,
)


@dataclass(frozen=True)
class CapabilitySuiteConfig:
    methods: tuple[str, ...] = CAPABILITY_METHODS
    seeds: tuple[int, ...] = (42, 43, 44)
    episodes: int = 60
    train_episodes: int = 36
    output_dir: Path = Path("runs/agent-capability")

    def __post_init__(self) -> None:
        supported = set(CAPABILITY_METHODS) | set(CAPABILITY_ABLATIONS)
        unknown = sorted(set(self.methods) - supported)
        if unknown:
            raise ValueError(f"unsupported capability methods: {', '.join(unknown)}")
        if not self.methods or not self.seeds or self.episodes < 12 or self.train_episodes < 12:
            raise ValueError("methods/seeds are required and split episodes must be >= 12")


def _mean_metrics(rows: list[dict[str, float]]) -> dict[str, float]:
    return {key: mean(row[key] for row in rows) for key in rows[0]}


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


def _metrics(rows: list[dict[str, Any]]) -> dict[str, float]:
    failure_rows = [row for row in rows if row["has_failure"]]
    total_calls = sum(float(row["tool_calls"]) for row in rows)
    return {
        "answer_accuracy": mean(bool(row["answer_ok"]) for row in rows),
        "plan_exact_match": mean(bool(row["plan_ok"]) for row in rows),
        "plan_step_f1": mean(float(row["plan_step_f1"]) for row in rows),
        "joint_success": mean(bool(row["joint_ok"]) for row in rows),
        "recovery_success_rate": (
            mean(bool(row["joint_ok"]) for row in failure_rows)
            if failure_rows else 0.0
        ),
        "invalid_tool_rate": (
            sum(float(row["invalid_calls"]) for row in rows) / max(1.0, total_calls)
        ),
        "irreversible_error_rate": mean(
            float(row["irreversible_errors"] > 0) for row in rows
        ),
        "average_tool_calls": total_calls / len(rows),
        "average_cost": mean(float(row["cost"]) for row in rows),
    }


def _run_split(
    policy: CapabilityPolicy,
    episodes: int,
    seed: int,
    split: CapabilitySplit,
    *,
    retain_trace: bool = True,
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    telemetry = {
        "retries": 0, "reflections": 0, "skill_reuses": 0,
        "verifications": 0, "compressions": 0, "memory_writes": 0,
    }
    trace = []
    for task in build_capability_tasks(episodes, seed, split):
        environment = CapabilityEnvironment(task)
        prediction = policy.solve(task.observation, environment.call)
        row = evaluate_episode(task, prediction.answer, environment)
        row["cost"] = float(row["cost"]) + prediction.decision_cost
        rows.append(row)
        for key in telemetry:
            telemetry[key] += int(getattr(prediction, key))
        if retain_trace and len(trace) < 12:
            trace.append({**row, "source": prediction.source, "calls": environment.calls})
    axis_metrics = {
        axis: mean(bool(row["joint_ok"]) for row in rows if row["axis"] == axis)
        for axis in AXES
    }
    return {
        "split": split,
        "metrics": _metrics(rows),
        "axis_metrics": axis_metrics,
        "telemetry": telemetry,
        "trace": trace,
    }


def _run_seed(method: str, episodes: int, train_episodes: int, seed: int) -> dict[str, Any]:
    training_policy = CapabilityPolicy(method)
    training = _run_split(
        training_policy, train_episodes, seed, "train", retain_trace=False,
    )
    validation_policy = CapabilityPolicy(method, skills=dict(training_policy.skills))
    test_policy = CapabilityPolicy(method, skills=dict(training_policy.skills))
    validation = _run_split(validation_policy, episodes, seed, "validation")
    test = _run_split(test_policy, episodes, seed, "test")
    return {
        "seed": seed,
        "training": training,
        "validation": validation,
        "test": test,
        "metrics": test["metrics"],
        "axis_metrics": test["axis_metrics"],
        "telemetry": test["telemetry"],
        "trace": test["trace"],
    }


def run_genome_capability(
    genome: Any,
    seed: int,
    episodes: int,
    split: CapabilitySplit,
) -> dict[str, float]:
    """Evaluate one Agent genome without exposing labels to the controller."""

    policy = CapabilityPolicy.from_genome(genome)
    _run_split(policy, max(12, episodes // 2), seed, "train", retain_trace=False)
    result = _run_split(policy, episodes, seed, split, retain_trace=False)
    metrics = dict(result["metrics"])
    telemetry = result["telemetry"]
    metrics.update({
        "reuse_rate": telemetry["skill_reuses"] / max(1, episodes),
        "recovery_rate": metrics["recovery_success_rate"],
        "verification_rate": telemetry["verifications"] / max(1, episodes),
        "compression_rate": telemetry["compressions"] / max(1, episodes),
    })
    return metrics


def render_capability_report(payload: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| {name} | {value:.4f} |"
        for name, value in payload["metrics"].items()
    )
    seed_rows = "\n".join(
        f"| {row['seed']} | {row['validation']['metrics']['joint_success']:.4f} | "
        f"{row['metrics']['joint_success']:.4f} | "
        f"{row['metrics']['plan_step_f1']:.4f} | {row['metrics']['average_cost']:.4f} |"
        for row in payload["seed_results"]
    )
    return f"""# Agent L2.1 capability report: {payload['method']}

> Policy 只能看到公开 observation、工具元数据和调用反馈。评测不存在 guide、answer、
> route 或 reference-plan 查询接口；train、validation、test 的任务族和路径深度隔离。

## 隔离 test 三 seed 汇总

| 指标 | 均值 |
|---|---:|
{rows}

| Seed | Validation joint | Test joint | Test plan F1 | Test cost |
|---:|---:|---:|---:|---:|
{seed_rows}

## 口径

- benchmark：`toolroute-l2.1-v1`
- train/validation/test episodes per seed：{payload['diagnostics']['split_episodes']}
- oracle fields exposed：`false`
- guide endpoint：`absent`
- formal comparison：`{str(payload['evaluation_protocol']['formal_comparison']).lower()}`
"""


def run_capability_suite(config: CapabilitySuiteConfig) -> dict[str, dict[str, Any]]:
    config.output_dir.mkdir(parents=True, exist_ok=True)
    fingerprint = capability_dataset_fingerprint(config.episodes, config.seeds)
    results = {}
    for method in config.methods:
        seed_results = [
            _run_seed(method, config.episodes, config.train_episodes, seed)
            for seed in config.seeds
        ]
        test_rows = [row["metrics"] for row in seed_results]
        validation_rows = [row["validation"]["metrics"] for row in seed_results]
        payload = {
            "schema_version": 2,
            "manifest_ref": f"agent-research:{method}:toolroute-l2.1-v1",
            "method": method,
            "benchmark": "toolroute-l2.1",
            "dataset": "toolroute-l2.1-v1",
            "seeds": list(config.seeds),
            "metrics": _mean_metrics(test_rows),
            "aggregate_metrics": _aggregate(test_rows),
            "validation_metrics": _mean_metrics(validation_rows),
            "validation_aggregate_metrics": _aggregate(validation_rows),
            "seed_results": seed_results,
            "diagnostics": {
                "split_episodes": {
                    "train": config.train_episodes,
                    "validation": config.episodes,
                    "test": config.episodes,
                },
                "total_episodes": (
                    config.train_episodes + 2 * config.episodes
                ) * len(config.seeds),
                "oracle_fields_exposed": False,
                "guide_endpoint": "absent",
                "split_family_overlap": False,
                "test_route_depths": [5, 6],
                "public_observation_type": "CapabilityObservation",
                "hidden_labels": ["answer", "allowed_steps", "canonical_route"],
                "fidelity": "shared no-oracle held-out capability benchmark",
            },
            "evaluation_protocol": {
                "tier": "l2_capability",
                "seeds": list(config.seeds),
                "formal_comparison": len(config.seeds) >= 3,
                "claim_policy": (
                    "held-out test, no guide/oracle; compare only within toolroute-l2.1-v1"
                ),
            },
            "provenance": {
                "dataset_fingerprint": fingerprint,
                "artifact_path": "runtime output; committed copies declare their docs path",
                "original_code_commit": "current working tree",
            },
        }
        seed_label = "-".join(map(str, config.seeds))
        run_dir = config.output_dir / f"{method}-toolroute-l21-seeds{seed_label}"
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "metrics.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
        )
        (run_dir / "report.md").write_text(render_capability_report(payload), encoding="utf-8")
        results[method] = payload
    summary = {
        "schema_version": 2,
        "manifest_ref": "experiments:agent-toolroute-l2.1-runtime",
        "benchmark": "toolroute-l2.1-v1",
        "methods": list(config.methods),
        "seeds": list(config.seeds),
        "split_episodes": {
            "train": config.train_episodes,
            "validation": config.episodes,
            "test": config.episodes,
        },
        "results": {method: payload["metrics"] for method, payload in results.items()},
        "evaluation_protocol": {
            "tier": "l2_capability",
            "seeds": list(config.seeds),
            "formal_comparison": len(config.seeds) >= 3,
            "claim_policy": "held-out no-guide test; compare only within toolroute-l2.1-v1",
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
