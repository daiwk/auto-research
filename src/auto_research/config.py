from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ResearchConfig:
    topic: str
    track: str
    max_papers: int = 8
    max_trials: int = 8
    seed: int = 42
    output_dir: Path = Path("runs")
    dataset_dir: Path = Path("data")
    paper_query: str | None = None
    implementation_command: list[str] | None = None
    experiment_command: list[str] | None = None
    proposal_command: list[str] | None = None
    search_space: dict[str, list[Any]] = field(default_factory=dict)
    metric_name: str | None = None
    direction: str | None = None
    timeout_seconds: int = 1800
    implementation_timeout_seconds: int = 3600
    proposal_timeout_seconds: int = 300
    allow_network: bool = True
    cache_dir: Path = Path(".auto-research/cache")
    force_rerun: bool = False
    experiment_revision: str | None = None

    @classmethod
    def from_file(cls, path: str | Path) -> "ResearchConfig":
        path = Path(path)
        data = json.loads(path.read_text(encoding="utf-8"))
        if "output_dir" in data:
            data["output_dir"] = Path(data["output_dir"])
        if "dataset_dir" in data:
            data["dataset_dir"] = Path(data["dataset_dir"])
        if "cache_dir" in data:
            data["cache_dir"] = Path(data["cache_dir"])
        return cls(**data)

    def validate(self) -> None:
        if self.track not in {"llm", "recommendation"}:
            raise ValueError("track must be 'llm' or 'recommendation'")
        if not self.topic.strip():
            raise ValueError("topic must not be empty")
        if self.max_trials < 1 or self.max_papers < 0:
            raise ValueError("max_trials must be >= 1 and max_papers >= 0")
        if self.direction and self.direction not in {"minimize", "maximize"}:
            raise ValueError("direction must be minimize or maximize")
        if min(
            self.timeout_seconds,
            self.implementation_timeout_seconds,
            self.proposal_timeout_seconds,
        ) < 1:
            raise ValueError("all command timeouts must be >= 1 second")
