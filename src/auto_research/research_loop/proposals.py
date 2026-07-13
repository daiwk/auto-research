from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

from ..models import Trial


class CommandProposer:
    """Provider-neutral adaptive proposer backed by an explicit local command."""

    def __init__(
        self,
        command: list[str],
        manifest: dict[str, Any],
        max_trials: int,
        timeout_seconds: int,
        workdir: Path,
    ):
        if not command:
            raise ValueError("proposal_command must not be empty")
        self.command = command
        self.manifest = manifest
        self.max_trials = max_trials
        self.timeout_seconds = timeout_seconds
        self.workdir = workdir

    def propose(self, history: tuple[Trial, ...]) -> dict[str, Any] | None:
        if len(history) >= self.max_trials:
            return None
        env = os.environ.copy()
        env["AUTO_RESEARCH_MANIFEST"] = json.dumps(self.manifest, ensure_ascii=False)
        env["AUTO_RESEARCH_HISTORY"] = json.dumps(
            [trial.to_dict() for trial in history], ensure_ascii=False
        )
        completed = subprocess.run(
            self.command,
            cwd=self.workdir,
            env=env,
            capture_output=True,
            text=True,
            timeout=self.timeout_seconds,
            check=False,
        )
        if completed.returncode:
            raise RuntimeError(
                completed.stderr[-3000:]
                or f"proposal command exited with {completed.returncode}"
            )
        last_line = next(
            (line for line in reversed(completed.stdout.splitlines()) if line.strip()), ""
        )
        try:
            payload = json.loads(last_line)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "proposal command must print a JSON object on its last line"
            ) from exc
        if not isinstance(payload, dict):
            raise RuntimeError("proposal command output must be a JSON object")
        if payload.get("stop") is True:
            return None
        params = payload.get("params", payload)
        if not isinstance(params, dict) or not params:
            raise RuntimeError("proposal command must return non-empty params or {\"stop\": true}")
        return params
