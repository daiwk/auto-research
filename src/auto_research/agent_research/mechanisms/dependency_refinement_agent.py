"""Extracted unchanged from auto_research.agent_research.latest_20260919; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.mechanisms.public_observation import ObservationAgent, read_evidence
from auto_research.agent_research.method_families.base import _tokens

class DependencyRefinementAgent(ObservationAgent):
    """Prune and merge observable plan rounds with a dependency DAG."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.dependency_edges = self.leaf_prunes = self.strict_merges = self.relaxed_merges = 0

    def solve_observation(self, observation, step):
        del step
        answer, plan = read_evidence(observation)
        refined = []
        seen = set()
        for action in plan:
            tokens = _tokens(action)
            self.dependency_edges += int(bool(refined))
            if not tokens:
                self.leaf_prunes += 1; continue
            if tokens <= seen:
                self.strict_merges += 1; continue
            if refined and len(tokens & seen) >= max(1, len(tokens) // 2):
                refined[-1] = f"{refined[-1]}；{action}"; self.relaxed_merges += 1
            else:
                refined.append(action)
            seen |= tokens
        self.actions += len(refined); self.cost += len(observation.context)
        return answer, tuple(refined) or tuple(plan), "dependency-dag-refinement"
