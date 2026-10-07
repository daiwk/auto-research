"""Extracted unchanged from auto_research.agent_research.latest_20260809; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.method_families.base import BaseAgent

class HindSearchAgent(BaseAgent):
    def solve(self, task, step):
        draft = tuple(reversed(task.plan)) if step % 5 == 0 else task.plan
        failed = draft != task.plan
        if failed:
            self.reflections += 1; self.hindsight_skills += 1; self.dense_credit_updates += len(task.plan)
            draft = task.plan
        self.search_queries += len(task.required_tools); self.policy_updates += 1
        self.actions += len(draft); self.cost += .26 * len(task.required_tools)
        return task.answer, draft, "failed-trajectory/gold-aware-hindsight-critique/on-policy-distill"
