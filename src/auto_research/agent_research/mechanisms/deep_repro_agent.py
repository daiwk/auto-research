"""Extracted unchanged from auto_research.agent_research.latest_20260831; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.method_families.base import BaseAgent

class DeepReproAgent(BaseAgent):
    """Revise fine-grained subplans against the current repository state."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.repository_state = {}
        self.state_snapshots = 0
        self.subplan_revisions = 0
        self.runtime_feedback_repairs = 0

    def solve(self, task, step):
        previous = self.repository_state.get(task.axis)
        self.state_snapshots += 1
        if previous != task.plan:
            self.subplan_revisions += 1
            self.repository_state[task.axis] = task.plan
        else:
            self.skills_reused += 1
        if previous is not None and previous != task.plan:
            self.runtime_feedback_repairs += 1
            self.verification_retries += 1
        self.plans_created += 1
        self.worker_calls += len(task.required_tools)
        self.actions += len(task.plan)
        self.cost += 0.31 + 0.04 * len(task.required_tools)
        return task.answer, task.plan, "repository-snapshot/state-aware-subplan/runtime-feedback-repair"
