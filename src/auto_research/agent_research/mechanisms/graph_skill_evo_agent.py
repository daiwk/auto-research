"""Extracted unchanged from auto_research.agent_research.latest_20260921; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.mechanisms.public_observation import ObservationAgent, PublicObservation, read_evidence
from auto_research.agent_research.method_families.base import _tokens

class GraphSkillEvoAgent(ObservationAgent):
    """Represent observed procedures as graphs and mutate only explicit edges."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.graphs: dict[str, tuple[str, ...]] = {}
        self.graph_mutations = self.graph_crossovers = self.graph_prunes = 0

    def solve_observation(self, observation, step):
        answer, plan = read_evidence(observation)
        key = " ".join(sorted(_tokens(observation.intent))[:2]) or "default"
        prior = self.graphs.get(key)
        if prior and plan and prior != tuple(plan):
            cut = min(len(prior), len(plan), 1 + step % max(1, len(plan)))
            plan = prior[:cut] + tuple(plan[cut:]); self.graph_crossovers += 1
        if plan:
            compact = tuple(dict.fromkeys(plan))
            self.graph_prunes += len(plan) - len(compact)
            self.graph_mutations += int(self.graphs.get(key) != compact)
            self.graphs[key] = compact
            self.skill_graph_nodes += len(compact)
            self.skill_graph_edges += max(0, len(compact) - 1)
            plan = compact
        self.cost += len(observation.context); self.actions += len(plan)
        return answer, plan, "graph-skill/mutation/crossover"
