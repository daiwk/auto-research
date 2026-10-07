"""Extracted unchanged from auto_research.agent_research.latest_20260829; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.method_families.base import BaseAgent

class SPTAgent(BaseAgent):
    """Use reference-aware skill packages as a pretraining prior."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.packages = {}
        self.reference_insertions = 0

    def solve(self, task, step):
        package = (task.axis, tuple(task.required_tools), task.plan)
        self.packages[task.axis] = package
        self.reference_insertions += len(task.required_tools)
        self.task_examples_retrieved += 1
        self.skills_created += int(step == 0)
        self.skills_reused += int(step > 0)
        self.actions += len(task.plan)
        self.cost += 0.30
        return task.answer, task.plan, "skill-package/reference-insert/mid-training-prior"
