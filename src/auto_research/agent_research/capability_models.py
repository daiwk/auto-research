from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class ToolSpec:
    """Tool metadata visible to an Agent policy."""

    name: str
    tag: str
    description: str


@dataclass(frozen=True)
class CapabilityObservation:
    """Public task view; deliberately contains no answer or reference plan."""

    task_id: str
    family: str
    request: str
    start_tags: tuple[str, ...]
    tools: tuple[ToolSpec, ...]


@dataclass(frozen=True)
class ToolFeedback:
    status: str
    message: str
    next_tags: tuple[str, ...] = ()
    answer: str = ""


ToolCaller = Callable[[str], ToolFeedback]


@dataclass(frozen=True)
class CapabilityPrediction:
    answer: str
    source: str
    retries: int = 0
    reflections: int = 0
    hints: int = 0
    skill_reuses: int = 0

