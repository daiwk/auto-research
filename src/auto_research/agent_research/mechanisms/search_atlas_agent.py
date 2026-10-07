"""Extracted unchanged from auto_research.agent_research.latest_20260914; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.mechanisms.public_observation import ObservationAgent, PublicObservation, read_evidence

class SearchAtlasAgent(ObservationAgent):
    """Evidential query graph from public queries, observations and answer."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.evidence_graph_edges = self.unsupported_answer_flags = 0

    def solve_observation(self, observation, step):
        answer, plan = read_evidence(observation)
        evidence = [fact for fact in observation.context if "resolves to" in fact]
        self.evidence_graph_edges += len(plan) + len(evidence)
        self.unsupported_answer_flags += int(bool(answer) and not evidence)
        self.actions += len(plan)
        self.cost += len(observation.context)
        return answer, plan, "query-evidence-answer-graph/process-audit"
