"""Extracted unchanged from auto_research.agent_research.latest_20260914; stable mechanism boundary."""
from __future__ import annotations

from collections import Counter, defaultdict
from auto_research.agent_research.mechanisms.public_observation import ObservationAgent, PublicObservation, read_evidence
from auto_research.agent_research.method_families.base import _tokens

class GroundedMemoryAgent(ObservationAgent):
    """Least-privilege curation that admits facts only after public re-probing."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.probes = Counter()
        self.curated: dict[str, str] = {}
        self.environment_probes = self.memory_admissions = self.stale_rejections = 0

    def solve_observation(self, observation, step):
        del step
        for fact in observation.context:
            key = " ".join(sorted(_tokens(fact))[:4])
            self.probes[(key, fact)] += 1
            self.environment_probes += 1
            prior = self.curated.get(key)
            if prior and prior != fact:
                self.stale_rejections += 1
                continue
            if self.probes[(key, fact)] >= 2 and prior is None:
                self.curated[key] = fact
                self.memory_admissions += 1
        evidence = tuple(observation.context) + tuple(self.curated.values())
        answer, plan = read_evidence(PublicObservation(
            observation.task_id, observation.intent, evidence
        ))
        self.actions += len(plan)
        self.cost += len(evidence)
        return answer, plan, "read-only-probe/scope-refresh/curation-gate"
