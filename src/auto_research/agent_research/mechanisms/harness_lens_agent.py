"""Extracted unchanged from auto_research.agent_research.latest_20260829; stable mechanism boundary."""
from __future__ import annotations

from collections import defaultdict
from auto_research.agent_research.method_families.base import BaseAgent

class HarnessLensAgent(BaseAgent):
    """Verify a harness mutation only on behavior-relevant tasks."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.behavior_tasks = defaultdict(int)
        self.attributable_evidence_gates = 0
        self.verification_budget_saved = 0

    def solve(self, task, step):
        relevant = tuple(dict.fromkeys((*task.required_tools, task.axis)))
        self.behavior_tasks[task.axis] += 1
        self.attributable_evidence_gates += 1
        self.verification_budget_saved += max(0, self.capacity - len(relevant))
        self.local_verifier_calls += len(relevant)
        self.policy_updates += 1
        self.actions += len(task.plan)
        self.cost += 0.28 + 0.07 * len(relevant)
        return task.answer, task.plan, "behavior-relevant/selective-verify/attribution-gate"
