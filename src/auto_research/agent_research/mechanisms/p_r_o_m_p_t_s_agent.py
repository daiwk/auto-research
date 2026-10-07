"""Extracted unchanged from auto_research.agent_research.latest_20260914; stable mechanism boundary."""
from __future__ import annotations

from collections import Counter, defaultdict
from auto_research.agent_research.mechanisms.public_observation import ObservationAgent, PublicObservation, read_evidence
from auto_research.agent_research.method_families.base import _tokens

class PROMPTSAgent(ObservationAgent):
    """Profiler bottleneck ranking and conservative configuration proposal."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.profile_bottlenecks = self.sharding_proposals = 0

    def solve_observation(self, observation, step):
        answer, plan = read_evidence(observation)
        costs = Counter(token for fact in observation.context for token in _tokens(fact))
        if costs:
            self.profile_bottlenecks += 1
            # Proposals are limited to an observed executable route; no invented
            # shell or distributed-runtime action is executed by this fixture.
            self.sharding_proposals += int(bool(plan))
        self.actions += len(plan)
        self.cost += len(observation.context)
        return answer, plan, "profile-evidence/bottleneck-rank/config-proposal"
