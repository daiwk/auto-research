"""Extracted unchanged from auto_research.agent_research.latest_20260831; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.method_families.base import BaseAgent

class ACEDataAgent(BaseAgent):
    """Gate experience by Accuracy, learner-relative Complexity and Diversity."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.support = set()
        self.accuracy_gates = 0
        self.complexity_calibrations = 0
        self.diversity_accepts = 0
        self.diversity_rejections = 0

    def solve(self, task, step):
        grounded = set(task.required_tools).issubset(task.plan)
        self.accuracy_gates += 1
        difficulty = len(task.plan) / max(1, self.capacity)
        self.complexity_calibrations += 1
        signature = (task.axis, task.required_tools)
        if grounded and signature not in self.support and 0.0 < difficulty <= 1.5:
            self.support.add(signature)
            self.diversity_accepts += 1
            self.task_library_updates += 1
        else:
            self.diversity_rejections += 1
        self.local_verifier_calls += 1
        self.actions += len(task.plan)
        self.cost += 0.27 + 0.02 * len(task.context)
        return task.answer, task.plan, "accuracy-gate/learner-relative-complexity/diversity-support"
