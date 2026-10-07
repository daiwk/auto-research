"""Extracted unchanged from auto_research.agent_research.latest_20260914; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.mechanisms.public_observation import ObservationAgent, PublicObservation, read_evidence

class ToolGradAgent(ObservationAgent):
    """Answer-first tool-plan construction followed by textual-gradient edits."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.answer_first_generations = self.textual_gradient_edits = 0

    def solve_observation(self, observation, step):
        answer, plan = read_evidence(observation)
        self.answer_first_generations += 1
        # The desired answer is decoded from public evidence first.  A textual
        # gradient then removes duplicate operations from the observed route;
        # it never receives the benchmark's hidden plan.
        refined = tuple(dict.fromkeys(plan))
        self.textual_gradient_edits += int(refined != plan)
        self.actions += len(refined)
        self.cost += len(observation.context)
        return answer, refined, "answer-first/textual-gradient/tool-trajectory"
