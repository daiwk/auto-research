"""Extracted unchanged from auto_research.agent_research.latest_20261002; stable mechanism boundary."""
from __future__ import annotations

from dataclasses import dataclass, field



@dataclass
class CurriculumArm:
    name: str
    value: float = 0.0
    pulls: int = 0
    examples: tuple[str, ...] = ()
