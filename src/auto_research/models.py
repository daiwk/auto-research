from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class Paper:
    title: str
    abstract: str
    authors: list[str]
    published: str
    url: str
    arxiv_id: str


@dataclass(frozen=True)
class Trial:
    number: int
    params: dict[str, Any]
    metric: float | None
    status: str
    duration_seconds: float
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ResearchResult:
    run_id: str
    topic: str
    track: str
    metric_name: str
    direction: str
    papers: list[Paper] = field(default_factory=list)
    trials: list[Trial] = field(default_factory=list)
    best_trial: Trial | None = None
    notes: list[str] = field(default_factory=list)
