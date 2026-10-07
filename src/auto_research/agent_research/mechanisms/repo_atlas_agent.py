"""Extracted unchanged from auto_research.agent_research.latest_20260916_followup; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.mechanisms.public_observation import ObservationAgent, read_evidence
from auto_research.agent_research.method_families.base import _tokens

class RepoAtlasAgent(ObservationAgent):
    """Bounded select-project-refresh view built only from observable context."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.view: tuple[str, ...] = ()
        self.last_focus: frozenset[str] = frozenset()
        self.view_refreshes = self.selected_nodes = self.text_projections = 0

    def solve_observation(self, observation, step):
        del step
        answer, plan = read_evidence(observation)
        focus = frozenset(_tokens(observation.intent))
        nodes = []
        for position, fact in enumerate(observation.context):
            tokens = _tokens(fact)
            relevance = len(tokens & focus) + 1.0 / (position + 1)
            nodes.append((relevance, fact))
        selected = tuple(fact for _, fact in sorted(nodes, reverse=True)[: self.capacity])
        stale = not self.view or len(focus ^ self.last_focus) > max(1, len(focus) // 2)
        if stale:
            self.view = selected
            self.last_focus = focus
            self.view_refreshes += 1
        self.selected_nodes += len(self.view)
        self.text_projections += 1
        self.actions += len(plan)
        self.cost += len(self.view)
        return answer, plan, "select/project/refresh-text-index"
