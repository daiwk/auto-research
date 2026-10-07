"""Extracted unchanged from auto_research.agent_research.latest_20260914; stable mechanism boundary."""
from __future__ import annotations

from collections import Counter, defaultdict
from auto_research.agent_research.mechanisms.public_observation import ObservationAgent, PublicObservation, read_evidence
from auto_research.agent_research.method_families.base import _tokens

class EcdysisAgent(ObservationAgent):
    """Batch recurring-failure diagnosis before accepting a harness repair."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.failure_signatures = Counter()
        self.pending_signature = ""
        self.cross_instance_failures = self.fdcr_repairs = 0

    def solve_observation(self, observation, step):
        answer, plan = read_evidence(observation)
        self.pending_signature = ":".join(sorted(_tokens(observation.intent))[:2])
        if self.failure_signatures[self.pending_signature] >= 2:
            self.fdcr_repairs += 1
        self.actions += len(plan)
        self.cost += len(observation.context)
        return answer, plan, "cross-instance-failure-aggregation/fdcr-moderation"

    def observe(self, task, answer_ok, plan_ok, step):
        del task, step
        if not (answer_ok and plan_ok):
            self.failure_signatures[self.pending_signature] += 1
            self.cross_instance_failures += 1
