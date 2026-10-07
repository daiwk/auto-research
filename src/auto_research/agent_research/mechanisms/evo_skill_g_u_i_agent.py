"""Extracted unchanged from auto_research.agent_research.latest_20260919; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.mechanisms.public_observation import ObservationAgent, read_evidence
from auto_research.agent_research.method_families.base import _tokens

class EvoSkillGUIAgent(ObservationAgent):
    """Reflect-revise-reuse a bounded skill package from observed outcomes."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.skills = {}
        self.pending = None
        self.skill_revisions = self.skill_reuses = self.critic_reviews = 0

    def solve_observation(self, observation, step):
        del step
        answer, observed_plan = read_evidence(observation)
        key = " ".join(sorted(_tokens(observation.intent))[:2]) or "default"
        plan = self.skills.get(key, tuple(observed_plan))
        self.skill_reuses += int(key in self.skills)
        self.pending = (key, tuple(observed_plan))
        self.actions += len(plan); self.cost += len(observation.context)
        return answer, plan, "reflect/revise/reuse"

    def observe(self, task, answer_ok, plan_ok, step):
        del task, step
        self.critic_reviews += 1
        if answer_ok and plan_ok and self.pending:
            key, plan = self.pending
            if len(self.skills) >= self.capacity and key not in self.skills:
                self.skills.pop(next(iter(self.skills)))
            self.skills[key] = plan; self.skill_revisions += 1
