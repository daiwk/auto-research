"""Extracted unchanged from auto_research.agent_research.latest_20260827; stable mechanism boundary."""
from __future__ import annotations

from collections import defaultdict
from auto_research.agent_research.method_families.base import BaseAgent

class TraceMLAgent(BaseAgent):
    """Use the human trajectory planning prior while keeping edits auditable."""

    phases = ("data", "validation", "model", "ensemble")

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.phase_counts = defaultdict(int)
        self.reopened_approaches = 0
        self.versioned_edits = 0

    def solve(self, task, step):
        phase = self.phases[step % len(self.phases)]
        self.phase_counts[phase] += 1
        if step >= len(self.phases) and step % len(self.phases) == 0:
            self.reopened_approaches += 1
        self.versioned_edits += 1
        self.plans_created += 1
        self.actions += len(task.plan)
        self.cost += 0.44
        return task.answer, task.plan, f"trace-schema/{phase}/score-effect/versioned-edit"
