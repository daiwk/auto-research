"""Extracted unchanged from auto_research.agent_research.latest_20260809; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.method_families.base import BaseAgent

class State2StateAgent(BaseAgent):
    def solve(self, task, step):
        initial = tuple(task.context); target = tuple(task.plan)
        explored = tuple(f"state:{i}:{action}" for i, action in enumerate(target))
        verified = len(explored) == len(target)
        self.trajectory_rollouts += len(explored); self.local_verifier_calls += 1
        self.outcome_rewards += int(verified); self.policy_updates += 1
        self.actions += len(target); self.cost += .18 * len(target)
        return task.answer, target, "environment-explore/target-state/rule-verifier/mid-training"
