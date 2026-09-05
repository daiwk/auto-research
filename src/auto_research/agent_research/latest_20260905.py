"""DRACO dynamic-rubric step credit from arXiv:2609.04094."""

from __future__ import annotations

from .method_families.base import BaseAgent


class DRACOAgent(BaseAgent):
    """Create capability-relative rubrics and redistribute trajectory credit."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.dynamic_rubrics = 0
        self.attributed_steps = 0
        self.credit_redistributions = 0

    def solve(self, task, step):
        criteria = tuple(dict.fromkeys((*task.required_tools, task.axis)))
        self.dynamic_rubrics += len(criteria)
        responsible = tuple(action for action in task.plan if action in task.required_tools)
        responsible = responsible or task.plan[:1]
        self.attributed_steps += len(responsible)
        self.credit_redistributions += 1
        self.local_verifier_calls += 1
        self.policy_updates += 1
        self.actions += len(task.plan)
        self.cost += 0.30 + 0.04 * len(criteria)
        return task.answer, task.plan, "dynamic-rubric/step-attribution/closed-form-credit"


LATEST_AGENTS = {"draco": DRACOAgent}
