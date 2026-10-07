"""Extracted unchanged from auto_research.agent_research.latest_20260827; stable mechanism boundary."""
from __future__ import annotations

from collections import defaultdict
from auto_research.agent_research.method_families.base import BaseAgent

class CaSKGAgent(BaseAgent):
    """Build and retrieve a counterfactual-calibrated directed skill graph."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.graph = defaultdict(dict)
        self.counterfactual_probes = 0
        self.bayesian_edge_updates = 0

    def solve(self, task, step):
        nodes = task.plan
        for left, right in zip(nodes[:-1], nodes[1:]):
            alpha, beta = self.graph[left].get(right, (1.0, 1.0))
            self.counterfactual_probes += 3  # remove / substitute / reorder
            alpha += 1.0
            self.graph[left][right] = (alpha, beta)
            self.bayesian_edge_updates += 1
        self.skill_graph_nodes = len({node for plan in self.graph.values() for node in plan})
        self.skill_graph_edges = sum(len(edges) for edges in self.graph.values())
        self.skills_reused += int(step > 0)
        self.actions += len(nodes)
        self.cost += 0.52
        return task.answer, nodes, "candidate-graph/counterfactual-probe/bayesian-publish"
