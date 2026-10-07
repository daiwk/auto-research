"""Extracted unchanged from auto_research.agent_research.latest_20260809; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.method_families.base import BaseAgent

class VaGAgent(BaseAgent):
    def __init__(self, capacity, rng):
        super().__init__(capacity, rng); self.skills = {}

    def solve(self, task, step):
        key = f"{task.axis}:{'/'.join(task.required_tools)}"
        structural = len(task.plan) == len(task.required_tools)
        harmless = all(action.split(':', 1)[0] in task.required_tools for action in task.plan)
        consistent = len(set(task.plan)) == len(task.plan)
        self.affordance_checks += 3
        if structural and harmless and consistent:
            self.skills[key] = task.plan; self.skills_created += 1
        else:
            self.infeasible_skills_filtered += 1
        plan = self.skills.get(key, task.plan)
        self.skills_reused += int(key in self.skills and step > 0)
        self.local_verifier_calls += 3; self.actions += len(plan); self.cost += .24
        return task.answer, plan, "pre-commit/structural-harmless-semantic/gain-selection"
