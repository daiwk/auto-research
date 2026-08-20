from __future__ import annotations

import json
from pathlib import Path
from statistics import mean, pstdev
from typing import Any

from .code_benchmark import run_code_method


DEFAULT_METHODS = ("direct", "critic", "agent-lightning", "swe-agent", "openhands")


def run_executor_matrix(
    output_dir: Path,
    methods: tuple[str, ...] = DEFAULT_METHODS,
    seeds: tuple[int, ...] = (42, 43, 44),
    episodes: int = 12,
    memory_size: int = 8,
) -> tuple[dict[str, Any], Path]:
    if episodes < 3 or not seeds or not methods:
        raise ValueError("matrix requires methods, seeds and at least three episodes")
    rows = []
    for seed in seeds:
        for method in methods:
            metrics, diagnostics, trace = run_code_method(
                method, episodes, memory_size,
            )
            if diagnostics["actual_subprocess_commands"] > 4 * episodes:
                raise RuntimeError(f"{method} exceeded the executor command budget")
            rows.append({
                "seed": seed,
                "method": method,
                "metrics": metrics,
                "diagnostics": diagnostics,
                "trace_digest": [
                    {"task_id": item["task_id"], "success": item["success"]}
                    for item in trace
                ],
            })
    summary = {}
    for method in methods:
        selected = [row for row in rows if row["method"] == method]
        summary[method] = {}
        for metric in ("joint_success", "average_cost", "reuse_rate"):
            values = [row["metrics"][metric] for row in selected]
            summary[method][f"{metric}_mean"] = mean(values)
            summary[method][f"{metric}_std"] = pstdev(values)
    payload = {
        "schema_version": 2,
        "task": "ag-002-real-executor-fair-matrix",
        "protocol": {
            "executor": "temporary repository + real python -m unittest subprocess",
            "same_foundation_policy": "fixed paper-method policy; no external LLM calls",
            "same_tasks": True,
            "episodes_per_run": episodes,
            "maximum_subprocess_commands_per_episode": 4,
            "seeds": list(seeds),
        },
        "summary": summary,
        "runs": rows,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "metrics.json"
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return payload, path
