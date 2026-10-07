"""Extracted unchanged from auto_research.agent_research.latest_20260829; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.method_families.base import BaseAgent

class SWEPrimeAgent(BaseAgent):
    """Filter trajectories, then mask low-value segments during imitation."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.selected_segments = 0
        self.masked_segments = 0

    def solve(self, task, step):
        quality = [tool in task.required_tools for tool in task.plan]
        selected = tuple(part for part, keep in zip(task.plan, quality) if keep) or task.plan[:1]
        self.trajectory_filters += 1
        self.selected_segments += len(selected)
        self.masked_segments += len(task.plan) - len(selected)
        self.policy_updates += 1
        self.actions += len(selected)
        self.cost += 0.32 + 0.05 * len(selected)
        return task.answer, selected, "process+result+representative/segment-loss-mask"
