"""Extracted unchanged from auto_research.agent_research.latest_20260921; stable mechanism boundary."""
from __future__ import annotations

from collections import Counter
from auto_research.agent_research.mechanisms.public_observation import ObservationAgent, PublicObservation, read_evidence
from auto_research.agent_research.method_families.base import _tokens

class MACEAgent(ObservationAgent):
    """Maintain functional condition-action-output units with feedback weights."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.units: dict[str, tuple[str, ...]] = {}
        self.scores = Counter()
        self.pending = "default"
        self.functional_units = self.typed_relations = self.presentation_updates = 0

    def solve_observation(self, observation, step):
        del step
        answer, plan = read_evidence(observation)
        key = " ".join(sorted(_tokens(observation.intent))[:2]) or "default"
        if key in self.units:
            plan = self.units[key]; self.skills_reused += 1
        elif plan:
            self.units[key] = tuple(plan); self.functional_units += 1
            self.typed_relations += max(0, len(plan) - 1)
        self.pending = key
        self.cost += len(observation.context); self.actions += len(plan)
        return answer, plan, "memgog/support-repair/instruction"

    def observe(self, task, answer_ok, plan_ok, step):
        del task, step
        self.scores[self.pending] += 1 if answer_ok and plan_ok else -1
        self.presentation_updates += 1
