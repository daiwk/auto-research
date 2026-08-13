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


def build_lmms_eval_command(config: LMMSEvalConfig) -> list[str]:
    if not config.tasks:
        raise ValueError("lmms-eval requires at least one task")
    command = [
        sys.executable, "-m", "lmms_eval", "--model", config.model,
        "--model_args", config.model_args, "--tasks", ",".join(config.tasks),
        "--batch_size", config.batch_size,
        "--output_path", str(config.output_dir), "--log_samples",
    ]
    if config.limit is not None:
        if config.limit < 1:
            raise ValueError("lmms-eval limit must be positive")
        command += ["--limit", str(config.limit)]
    if config.device:
        command += ["--device", config.device]
    return command


def run_lmms_eval(
    config: LMMSEvalConfig,
    *, dry_run: bool = False,
    runner: Callable[..., subprocess.CompletedProcess] = subprocess.run,
) -> dict:
    command = build_lmms_eval_command(config)
    config.output_dir.mkdir(parents=True, exist_ok=True)
    request = {"schema_version": 1, "command": command, "tasks": list(config.tasks)}
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
    return {**request, "status": "completed", "stdout_tail": completed.stdout[-2000:]}
