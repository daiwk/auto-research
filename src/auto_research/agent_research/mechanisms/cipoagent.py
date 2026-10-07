"""Extracted unchanged from auto_research.agent_research.latest_20260809; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.method_families.base import BaseAgent

class CIPOAgent(BaseAgent):
    def solve(self, task, step):
        evidence = {tool: f"evidence:{tool}:{task.intent}" for tool in task.required_tools}
        self.search_queries += len(evidence); self.references_collected += len(evidence)
        grounded = tuple(action for action in task.plan if action.split(':', 1)[0] in evidence)
        self.dense_credit_updates += len(grounded); self.turn_credit_updates += len(grounded)
        self.outcome_rewards += 1; self.policy_updates += 1; self.actions += len(grounded); self.cost += .3 * len(evidence)
        return task.answer, grounded, "retrieval/evidence-use-turn-credit/global-outcome"
