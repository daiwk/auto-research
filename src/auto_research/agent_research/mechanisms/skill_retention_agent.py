"""Extracted unchanged from auto_research.agent_research.latest_20260914; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.mechanisms.public_observation import ObservationAgent, PublicObservation, read_evidence
from auto_research.agent_research.method_families.base import _tokens

class SkillRetentionAgent(ObservationAgent):
    """Replay-anchored skill router that retains observed real-task routes."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.anchors: dict[str, tuple[str, ...]] = {}
        self.anchor_penalties = self.replay_retrievals = 0

    def solve_observation(self, observation, step):
        answer, observed = read_evidence(observation)
        key = " ".join(sorted(_tokens(observation.intent))[:2])
        prior = self.anchors.get(key)
        if observed:
            if prior and prior != observed:
                self.anchor_penalties += 1
            self.anchors[key] = observed
        elif prior:
            self.replay_retrievals += 1
        plan = observed or prior or ()
        self.actions += len(plan)
        self.cost += len(observation.context)
        return answer, plan, "real-route-anchor/replay/forgetting-penalty"
