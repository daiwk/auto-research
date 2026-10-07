"""Extracted unchanged from auto_research.agent_research.latest_20260914; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.mechanisms.public_observation import ObservationAgent, PublicObservation, read_evidence

class T1TerminalAgent(ObservationAgent):
    """Exact-token/route replay audit for long-horizon terminal RL traces."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.tito_tokens = self.routing_replays = self.turn_boundary_repairs = 0

    def solve_observation(self, observation, step):
        answer, plan = read_evidence(observation)
        token_ids = tuple(hash(token) & 0xFFFF for action in plan for token in action.split())
        self.tito_tokens += len(token_ids)
        self.routing_replays += len(plan)
        self.turn_boundary_repairs += sum(not action.strip() for action in plan)
        self.actions += len(plan)
        self.cost += len(observation.context)
        return answer, plan, "tito-exact-token/turn-boundary-repair/routing-replay"
