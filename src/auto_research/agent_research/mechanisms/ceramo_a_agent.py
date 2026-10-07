"""Extracted unchanged from auto_research.agent_research.latest_20260919; stable mechanism boundary."""
from __future__ import annotations

from collections import Counter
from auto_research.agent_research.mechanisms.public_observation import ObservationAgent, read_evidence
from auto_research.agent_research.method_families.base import _tokens

class CERAMoAAgent(ObservationAgent):
    """Route by observable familiarity and update only the selected specialist."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.specialists = Counter(); self.pending = "default"
        self.familiarity_routes = self.targeted_allocations = self.router_updates = 0

    def solve_observation(self, observation, step):
        del step
        answer, plan = read_evidence(observation)
        axes = sorted(_tokens(observation.intent))[:3] or ["default"]
        self.pending = max(axes, key=lambda key: self.specialists[key])
        self.familiarity_routes += 1
        self.actions += len(plan); self.cost += len(observation.context)
        return answer, plan, f"familiarity-route/{self.pending}"

    def observe(self, task, answer_ok, plan_ok, step):
        del task, step
        self.specialists[self.pending] += 1 if answer_ok and plan_ok else -1
        self.targeted_allocations += 1; self.router_updates += 1
