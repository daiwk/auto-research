"""Extracted unchanged from auto_research.agent_research.latest_20260916; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.mechanisms.public_observation import ObservationAgent, read_evidence
from auto_research.agent_research.method_families.base import _tokens

class ScienceBuddyAgent(ObservationAgent):
    """Inner harness refinement followed by an outer policy-memory update."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.harness_memory: dict[str, tuple[str, ...]] = {}
        self.pending_key = ""
        self.inner_harness_updates = self.outer_policy_updates = self.cross_branch_lessons = 0

    def solve_observation(self, observation, step):
        answer, observed = read_evidence(observation)
        key = " ".join(sorted(_tokens(observation.intent))[:2]) or "default"
        prior = self.harness_memory.get(key, ())
        if observed and observed != prior:
            self.harness_memory[key] = observed
            self.inner_harness_updates += 1
        elif prior:
            self.cross_branch_lessons += 1
        self.pending_key = key
        plan = observed or prior
        self.actions += len(plan)
        self.cost += len(observation.context)
        return answer, plan, "inner-harness-evolution/outer-policy-learning"

    def observe(self, task, answer_ok, plan_ok, step):
        del task, step
        self.outer_policy_updates += int(answer_ok and plan_ok and bool(self.pending_key))
