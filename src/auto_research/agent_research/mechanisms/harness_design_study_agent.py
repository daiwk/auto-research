"""Extracted unchanged from auto_research.agent_research.latest_20260919; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.mechanisms.public_observation import ObservationAgent, read_evidence

class HarnessDesignStudyAgent(ObservationAgent):
    """Ablate planning, action granularity and context compression explicitly."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.rule_elisions = self.context_summaries = self.action_granularity_choices = 0

    def solve_observation(self, observation, step):
        answer, plan = read_evidence(observation)
        context = tuple(dict.fromkeys(observation.context))[-self.capacity:]
        self.rule_elisions += max(0, len(observation.context) - len(context))
        self.context_summaries += int(len(observation.context) > self.capacity)
        self.action_granularity_choices += 1
        chosen = tuple(plan[: max(1, min(len(plan), 1 + step % 3))])
        self.actions += len(chosen); self.cost += len(context)
        return answer, chosen, "fixed-loop/harness-ablation"
