"""Extracted unchanged from auto_research.agent_research.latest_20260827; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.method_families.base import BaseAgent

class ProgRouterAgent(BaseAgent):
    """Route each workflow step by estimated progress gain per unit cost."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.progress_predictions = 0
        self.meta_gate_decisions = 0
        self.budget_downgrades = 0

    def solve(self, task, step):
        completion = min(1.0, (step % max(2, len(task.plan) + 1)) / max(1, len(task.plan)))
        remaining = 1.0 - completion
        strong_gain = 0.72 * remaining
        cheap_gain = 0.48 * remaining
        strong = strong_gain / 1.8 > cheap_gain / 0.7 and step % 4 != 0
        self.progress_predictions += 2
        self.meta_gate_decisions += 1
        self.budget_downgrades += int(not strong)
        self.router_calls += 1
        self.actions += len(task.plan)
        self.cost += 0.72 if strong else 0.31
        return task.answer, task.plan, f"progress={completion:.2f}/route={'strong' if strong else 'cheap'}/budget-gate"
