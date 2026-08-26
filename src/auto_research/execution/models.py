from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ResourceBudget:
    timeout_seconds: int = 3600
    retries: int = 0
    gpu_memory_mb: int | None = None
    maximum_cost: float | None = None
    estimated_cost: float = 0.0
    estimated_gpu_memory_mb: int | None = None

    def validate(self) -> None:
        if self.timeout_seconds < 1 or self.retries < 0:
            raise ValueError("timeout_seconds must be positive and retries non-negative")
        if self.gpu_memory_mb is not None and self.gpu_memory_mb < 1:
            raise ValueError("gpu_memory_mb must be positive")
        if (self.gpu_memory_mb is not None and self.estimated_gpu_memory_mb is not None
                and self.estimated_gpu_memory_mb > self.gpu_memory_mb):
            raise ValueError(
                f"estimated GPU memory {self.estimated_gpu_memory_mb} MB exceeds "
                f"budget {self.gpu_memory_mb} MB"
            )
        if self.maximum_cost is not None and self.estimated_cost > self.maximum_cost:
            raise ValueError(
                f"estimated cost {self.estimated_cost:g} exceeds budget {self.maximum_cost:g}"
            )


@dataclass(frozen=True)
class ExecutionSpec:
    run_id: str
    command: tuple[str, ...]
    output_dir: Path
    backend: str = "local"
    working_directory: str | None = None
    environment: dict[str, str] = field(default_factory=dict)
    budget: ResourceBudget = field(default_factory=ResourceBudget)
    host: str | None = None
    partition: str | None = None
    submit_only: bool = False
    dry_run: bool = False
    resume: bool = False

    def validate(self) -> None:
        if not self.run_id or not self.command:
            raise ValueError("run_id and command are required")
        if self.backend not in {"local", "ssh", "slurm"}:
            raise ValueError("backend must be local, ssh or slurm")
        if self.backend == "ssh" and not self.host:
            raise ValueError("SSH execution requires host")
        self.budget.validate()


@dataclass(frozen=True)
class ExecutionResult:
    run_id: str
    backend: str
    status: str
    returncode: int | None
    attempts: int
    duration_seconds: float
    command: tuple[str, ...]
    stdout_path: str
    stderr_path: str
    state_path: str
    job_id: str | None = None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["command"] = list(self.command)
        return payload

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ExecutionResult":
        payload = dict(payload); payload["command"] = tuple(payload["command"])
        return cls(**payload)
