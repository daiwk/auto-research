"""Extracted unchanged from auto_research.agent_research.latest_20261001; stable mechanism boundary."""
from __future__ import annotations

from dataclasses import dataclass, field



@dataclass(frozen=True)
class ProposedAction:
    name: str
    expected_value: float
    cost: int
    context: tuple[str, ...] = ()
