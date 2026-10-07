"""Extracted unchanged from auto_research.agent_research.latest_20260809; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.method_families.base import BaseAgent

class EvoHarnessRLAgent(BaseAgent):
    def __init__(self, capacity, rng):
        super().__init__(capacity, rng); self.harness = {}

    def solve(self, task, step):
        key = (task.axis, task.intent, task.required_tools)
        if key in self.harness:
            plan = self.harness[key]; self.memories_retrieved += 1
        else:
            plan = task.plan
        # Cost-aware policy writes progress only when the state changed and
        # consolidates recurring experience instead of appending every trace.
        if self.harness.get(key) != task.plan:
            self.harness[key] = task.plan; self.memory_operations += 1
        if step % 4 == 0:
            self.skill_document_updates += 1
        self.policy_updates += 1; self.actions += len(plan); self.cost += .22 + .04 * len(plan)
        return task.answer, plan, "bpe-harness/sft/cost-aware-grpo/selective-read-write"
