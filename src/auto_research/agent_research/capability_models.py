from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class ToolSpec:
    """Tool metadata visible to an Agent policy."""

    name: str
    tag: str
    description: str
    reliability: float = 1.0
    reversible: bool = True
    cost: float = 1.0


@dataclass(frozen=True)
class CapabilityObservation:
    """Public task view; deliberately contains no answer or reference plan."""

    task_id: str
    split: str
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
    terminal: bool = False


ToolCaller = Callable[[str], ToolFeedback]


@dataclass(frozen=True)
class CapabilityPrediction:
    answer: str
    source: str
    retries: int = 0
    reflections: int = 0
    hints: int = 0
    skill_reuses: int = 0
    verifications: int = 0
    compressions: int = 0
    memory_writes: int = 0
    decision_cost: float = 0.0
