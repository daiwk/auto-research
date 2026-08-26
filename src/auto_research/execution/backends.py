from __future__ import annotations

import json
import os
import shlex
import subprocess
import time
from pathlib import Path
from typing import Callable

from .models import ExecutionResult, ExecutionSpec

Runner = Callable[..., subprocess.CompletedProcess]


class BaseExecutor:
    backend = "base"

    def __init__(self, runner: Runner = subprocess.run):
        self.runner = runner

    def command(self, spec: ExecutionSpec, run_dir: Path) -> list[str]:
        raise NotImplementedError

    def execute(self, spec: ExecutionSpec) -> ExecutionResult:
        spec.validate()
        run_dir = spec.output_dir.resolve() / spec.run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        stdout_path, stderr_path = run_dir / "stdout.log", run_dir / "stderr.log"
        state_path = run_dir / "state.json"
        if spec.resume and state_path.exists():
            previous = json.loads(state_path.read_text(encoding="utf-8"))
            if previous.get("status") in {"completed", "submitted"}:
                return ExecutionResult.from_dict(previous)
        command = self.command(spec, run_dir)
        if spec.dry_run:
            return self._finish(spec, command, state_path, stdout_path, stderr_path,
                                "planned", None, 0, 0.0)
        started, last_error = time.monotonic(), None
        for attempt in range(1, spec.budget.retries + 2):
            self._write_state(state_path, spec, command, "running", attempt)
            try:
                env = os.environ.copy()
                env.update(spec.environment)
                completed = self.runner(
                    command, cwd=spec.working_directory if self.backend == "local" else None,
                    env=env, capture_output=True, text=True,
                    timeout=spec.budget.timeout_seconds, check=False,
                )
                stdout_path.write_text(completed.stdout or "", encoding="utf-8")
                stderr_path.write_text(completed.stderr or "", encoding="utf-8")
                if completed.returncode == 0:
                    job_id = _job_id(completed.stdout) if self.backend == "slurm" else None
                    status = "submitted" if self.backend == "slurm" or spec.submit_only else "completed"
                    return self._finish(spec, command, state_path, stdout_path, stderr_path,
                                        status, completed.returncode, attempt,
                                        time.monotonic() - started, job_id=job_id)
                last_error = f"process exited with {completed.returncode}"
            except subprocess.TimeoutExpired as exc:
                last_error = f"timeout after {spec.budget.timeout_seconds}s: {exc}"
                stderr_path.write_text(last_error + "\n", encoding="utf-8")
            except OSError as exc:
                last_error = f"{type(exc).__name__}: {exc}"
                stderr_path.write_text(last_error + "\n", encoding="utf-8")
        return self._finish(spec, command, state_path, stdout_path, stderr_path,
                            "failed", None, spec.budget.retries + 1,
                            time.monotonic() - started, error=last_error)

    @staticmethod
    def _write_state(path, spec, command, status, attempts, **extra):
        payload = {
            "schema_version": 1, "run_id": spec.run_id, "backend": spec.backend,
            "status": status, "attempts": attempts, "command": command, **extra,
        }
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def _finish(self, spec, command, state_path, stdout_path, stderr_path,
                status, returncode, attempts, duration, job_id=None, error=None):
        stdout_path.touch(exist_ok=True); stderr_path.touch(exist_ok=True)
        result = ExecutionResult(
            spec.run_id, spec.backend, status, returncode, attempts, duration,
            tuple(command), str(stdout_path), str(stderr_path), str(state_path), job_id, error,
        )
        state_path.write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2) + "\n",
                              encoding="utf-8")
        return result


class LocalExecutor(BaseExecutor):
    backend = "local"

    def command(self, spec, run_dir):
        return list(spec.command)


class SSHExecutor(BaseExecutor):
    backend = "ssh"

    def command(self, spec, run_dir):
        env = " ".join(f"{key}={shlex.quote(value)}" for key, value in sorted(spec.environment.items()))
        body = shlex.join(spec.command)
        if spec.working_directory:
            body = f"cd {shlex.quote(spec.working_directory)} && {body}"
        if env:
            body = f"env {env} {body}"
        return ["ssh", str(spec.host), body]


class SlurmExecutor(BaseExecutor):
    backend = "slurm"

    def command(self, spec, run_dir):
        script = run_dir / "job.sh"
        lines = ["#!/usr/bin/env bash", "set -euo pipefail"]
        if spec.partition:
            lines.append(f"#SBATCH --partition={spec.partition}")
        lines.extend([
            f"#SBATCH --time={max(1, spec.budget.timeout_seconds // 60)}",
            f"#SBATCH --output={run_dir / 'slurm-%j.out'}",
        ])
        if spec.budget.gpu_memory_mb:
            lines.append("#SBATCH --gres=gpu:1")
        if spec.working_directory:
            lines.append(f"cd {shlex.quote(spec.working_directory)}")
        for key, value in sorted(spec.environment.items()):
            lines.append(f"export {key}={shlex.quote(value)}")
        lines.append(shlex.join(spec.command))
        script.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return ["sbatch", "--parsable", str(script)]


def _job_id(stdout: str) -> str | None:
    value = (stdout or "").strip().split(";", 1)[0]
    return value or None


def create_executor(backend: str, runner: Runner = subprocess.run) -> BaseExecutor:
    executors = {"local": LocalExecutor, "ssh": SSHExecutor, "slurm": SlurmExecutor}
    try:
        return executors[backend](runner)
    except KeyError as exc:
        raise ValueError(f"unknown execution backend: {backend}") from exc


class ExecutionQueue:
    """Persistent FIFO coordinator; Slurm remains the cluster-level scheduler."""

    def __init__(self, path: Path):
        self.path = path

    def run(self, specs: list[ExecutionSpec]) -> list[ExecutionResult]:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        results = []
        for index, spec in enumerate(specs):
            self.path.write_text(json.dumps({
                "schema_version": 1, "status": "running", "next_index": index,
                "run_ids": [item.run_id for item in specs],
            }, indent=2) + "\n", encoding="utf-8")
            results.append(create_executor(spec.backend).execute(spec))
        self.path.write_text(json.dumps({
            "schema_version": 1, "status": "completed", "next_index": len(specs),
            "results": [item.to_dict() for item in results],
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return results
