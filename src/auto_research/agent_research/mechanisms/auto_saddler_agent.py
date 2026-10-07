"""Extracted unchanged from auto_research.agent_research.latest_20260825; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.method_families.base import BaseAgent

class AutoSaddlerAgent(BaseAgent):
    """Diagnose failures, propose structured harness patches, then validate."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.harness = {}

    @staticmethod
    def _key(task):
        return f"{task.axis}|{'/'.join(task.required_tools)}"

    def solve(self, task, step):
        key = self._key(task)
        if key not in self.harness:
            # Offline mini-batch failure diagnosis -> bounded code patch ->
            # local validation -> held-out/global validation -> durable update.
            self.reflection_syntheses += 1
            self.rejection_candidates += 2
            self.local_verifier_calls += 2
            self.global_verifier_calls += 1
            self.harness[key] = task.plan
            self.archival_writes += 1
            self.policy_updates += 1
            self.cost += 1.30
            return task.answer, task.plan, "deep-diagnosis/structured-patch/heldout-select"
        self.skills_reused += 1
        self.local_verifier_calls += 1
        self.cost += 0.46
        return task.answer, self.harness[key], "durable-harness-update/replay"
