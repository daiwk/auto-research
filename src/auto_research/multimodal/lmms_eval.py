"""Optional, auditable subprocess bridge to the upstream lmms-eval CLI."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import subprocess
import sys
from typing import Callable


@dataclass(frozen=True)
class LMMSEvalConfig:
    model: str
    model_args: str
    tasks: tuple[str, ...]
    output_dir: Path
    batch_size: str = "1"
    limit: int | None = None
    device: str | None = None
    public_model_id: str | None = None
    model_revision: str | None = None
    upstream_revision: str | None = None
    seed: int = 42
    gen_kwargs: str | None = None


def build_lmms_eval_command(config: LMMSEvalConfig) -> list[str]:
    if not config.tasks:
        raise ValueError("lmms-eval requires at least one task")
    if config.public_model_id and (
        config.model_revision is None or len(config.model_revision) != 40
    ):
        raise ValueError("public lmms-eval models require a 40-character revision")
    if config.upstream_revision is not None and len(config.upstream_revision) != 40:
        raise ValueError("lmms-eval upstream revision must contain 40 characters")
    command = [
        sys.executable, "-m", "lmms_eval", "--model", config.model,
        "--model_args", config.model_args, "--tasks", ",".join(config.tasks),
        "--batch_size", config.batch_size,
        "--output_path", str(config.output_dir), "--log_samples",
        "--seed", f"{config.seed},{config.seed},{config.seed},{config.seed}",
    ]
    if config.limit is not None:
        if config.limit < 1:
            raise ValueError("lmms-eval limit must be positive")
        command += ["--limit", str(config.limit)]
    if config.device:
        command += ["--device", config.device]
    if config.gen_kwargs:
        command += ["--gen_kwargs", config.gen_kwargs]
    return command


def _result_file(output_dir: Path) -> Path:
    candidates = [
        path for path in output_dir.rglob("*.json")
        if path.name not in {"request.json", "summary.json"}
        and "results" in path.stem
    ]
    if not candidates:
        raise RuntimeError(f"lmms-eval completed without a results JSON under {output_dir}")
    return max(candidates, key=lambda path: path.stat().st_mtime_ns)


def _scalar_metrics(values: object) -> dict[str, int | float | bool | str | None]:
    if not isinstance(values, dict):
        return {}
    metrics: dict[str, int | float | bool | str | None] = {}
    for raw_name, value in values.items():
        if isinstance(value, (str, int, float, bool)) or value is None:
            metrics[str(raw_name).split(",", 1)[0]] = value
    return metrics


def normalize_lmms_eval_results(
    payload: dict,
    config: LMMSEvalConfig,
    *,
    source_file: Path,
) -> dict:
    """Reduce upstream output to stable, path-free evidence for this repository."""
    raw_results = payload.get("results", {})
    sample_counts = payload.get("n-samples", payload.get("n_samples", {}))
    higher_is_better = payload.get("higher_is_better", {})
    raw_efficiency = payload.get("efficiency", {})
    tasks = []
    for task_name in config.tasks:
        counts = sample_counts.get(task_name, {}) if isinstance(sample_counts, dict) else {}
        tasks.append(
            {
                "task": task_name,
                "metrics": _scalar_metrics(
                    raw_results.get(task_name, {}) if isinstance(raw_results, dict) else {}
                ),
                "samples": {
                    key: value for key, value in counts.items()
                    if key in {"effective", "original"} and isinstance(value, int)
                } if isinstance(counts, dict) else {},
                "higher_is_better": _scalar_metrics(
                    higher_is_better.get(task_name, {})
                    if isinstance(higher_is_better, dict) else {}
                ),
            }
        )
    return {
        "schema_version": 2,
        "status": "completed",
        "backend": "lmms-eval",
        "model": {
            "adapter": config.model,
            "public_id": config.public_model_id,
            "revision": config.model_revision,
        },
        "protocol": {
            "batch_size": config.batch_size,
            "limit": config.limit,
            "seed": config.seed,
            "gen_kwargs": config.gen_kwargs,
        },
        "tasks": tasks,
        "efficiency": {
            "overall": _scalar_metrics(
                raw_efficiency.get("overall", {})
                if isinstance(raw_efficiency, dict) else {}
            ),
            "by_task": {
                task_name: _scalar_metrics(
                    raw_efficiency.get("by_task", {}).get(task_name, {})
                    if isinstance(raw_efficiency, dict)
                    and isinstance(raw_efficiency.get("by_task"), dict) else {}
                )
                for task_name in config.tasks
            },
        },
        "upstream": {
            "revision": config.upstream_revision,
            "versions": payload.get("versions", {}),
            "source_file": source_file.name,
        },
    }


def run_lmms_eval(
    config: LMMSEvalConfig,
    *, dry_run: bool = False,
    runner: Callable[..., subprocess.CompletedProcess] = subprocess.run,
) -> dict:
    command = build_lmms_eval_command(config)
    config.output_dir.mkdir(parents=True, exist_ok=True)
    request = {
        "schema_version": 2,
        "command": command,
        "tasks": list(config.tasks),
        "public_model_id": config.public_model_id,
        "model_revision": config.model_revision,
        "upstream_revision": config.upstream_revision,
        "seed": config.seed,
    }
    (config.output_dir / "request.json").write_text(
        json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if dry_run:
        return {**request, "status": "dry-run"}
    try:
        completed = runner(command, check=True, text=True, capture_output=True)
    except ModuleNotFoundError as exc:
        raise RuntimeError("lmms-eval is optional; install auto-research[lmms-eval]") from exc
    except subprocess.CalledProcessError as exc:
        tail = (exc.stderr or exc.stdout or "")[-2000:]
        raise RuntimeError(f"lmms-eval failed: {tail}") from exc
    result_file = _result_file(config.output_dir)
    try:
        payload = json.loads(result_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"cannot parse lmms-eval results: {result_file.name}") from exc
    summary = normalize_lmms_eval_results(payload, config, source_file=result_file)
    (config.output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return {**summary, "stdout_tail": completed.stdout[-2000:]}
