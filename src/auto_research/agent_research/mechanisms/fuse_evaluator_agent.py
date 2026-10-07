"""Extracted unchanged from auto_research.agent_research.latest_20260916; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.mechanisms.public_observation import ObservationAgent, read_evidence
from auto_research.agent_research.method_families.base import _tokens

class FuseEvaluatorAgent(ObservationAgent):
    """Verifiable simulation audit without access to hidden benchmark gold."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.simulated_dialogues = self.framing_checks = self.verifiable_motives = 0

    def solve_observation(self, observation, step):
        del step
        answer, plan = read_evidence(observation)
        frames = [set(_tokens(fact)) for fact in observation.context]
        self.simulated_dialogues += 1
        self.framing_checks += sum(bool(left ^ right) for left, right in zip(frames, frames[1:]))
        self.verifiable_motives += int(bool(answer))
        self.actions += len(plan)
        self.cost += len(observation.context)
        return answer, plan, "multi-agent-simulation/user-mediation/verifiable-hidden-motive"
