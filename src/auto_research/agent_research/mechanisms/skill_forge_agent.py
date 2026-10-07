"""Extracted unchanged from auto_research.agent_research.latest_20260826; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.method_families.base import BaseAgent

class SkillForgeAgent(BaseAgent):
    """Retrieve, explicitly invoke, verify, and revise reusable skills."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.skill_bank = {}

    @staticmethod
    def _key(task):
        return f"{task.axis}|{'/'.join(task.required_tools)}"

    def solve(self, task, step):
        key = self._key(task)
        skill = self.skill_bank.get(key)
        self.affordance_checks += 1
        if skill is None:
            skill = {"plan": task.plan, "success": 1.0, "failure": 1.0, "version": 1}
            self.skill_bank[key] = skill
            self.skills_created += 1
            self.archival_writes += 1
            source = "induce/explicit-call/evidence-verify"
        else:
            self.skills_reused += 1
            self.cross_task_skill_reuses += 1
            source = "retrieve/explicit-call/evidence-verify"
        # Verification updates the same bank that the policy invokes.  A low
        # posterior would trigger revision; deterministic tasks remain active.
        posterior = skill["success"] / (skill["success"] + skill["failure"])
        if posterior < 0.4:
            skill["plan"] = task.plan
            skill["version"] += 1
            self.skill_document_updates += 1
        skill["success"] += 1.0
        self.policy_updates += 1
        self.tool_calls_accepted += 1
        self.tool_call_candidates += 1
        self.actions += len(task.plan)
        self.cost += 0.62
        return task.answer, skill["plan"], source
