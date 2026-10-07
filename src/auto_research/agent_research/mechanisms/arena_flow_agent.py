"""Extracted unchanged from auto_research.agent_research.latest_20260921; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.mechanisms.public_observation import ObservationAgent, PublicObservation, read_evidence

class ArenaFlowAgent(ObservationAgent):
    """Expose tournament, pivotal-step and skill-credit accounting."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.tournament_comparisons = self.pivotal_step_updates = self.skill_utility_updates = 0

    def solve_observation(self, observation, step):
        del step
        answer, plan = read_evidence(observation)
        candidates = [tuple(plan), tuple(reversed(plan))] if plan else [()]
        winner = min(candidates, key=lambda candidate: sum(action not in observation.context for action in candidate))
        self.tournament_comparisons += max(0, len(candidates) - 1)
        self.pivotal_step_updates += len(winner)
        self.skill_utility_updates += int(bool(winner))
        self.cost += len(observation.context); self.actions += len(winner)
        return answer, winner, "tournament/hierarchical-credit/skill-prior"
