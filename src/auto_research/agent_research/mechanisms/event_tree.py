"""Extracted unchanged from auto_research.agent_research.latest_20260912; stable mechanism boundary."""
from __future__ import annotations

from dataclasses import dataclass

from auto_research.agent_research.mechanisms.public_observation import ObservationAgent, PublicObservation, read_evidence
from auto_research.agent_research.method_families.base import _tokens

@dataclass
class EventTree:
    anchor_tokens: set[str]
    events: list[str]

class MemForestAgent(ObservationAgent):
    """Event-centric partitioning, progressive merge and anchor retrieval."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.forest: list[EventTree] = []
        self.event_tree_partitions = 0
        self.progressive_merges = 0
        self.anchor_propagations = 0

    @staticmethod
    def _overlap(tokens, tree):
        return len(tokens & tree.anchor_tokens) / max(1, len(tokens | tree.anchor_tokens))

    def _insert(self, event):
        tokens = _tokens(event)
        scores = [self._overlap(tokens, tree) for tree in self.forest]
        if scores and max(scores) > 0:
            tree = self.forest[max(range(len(scores)), key=scores.__getitem__)]
            tree.events.append(event)
            tree.anchor_tokens |= tokens
        else:
            self.forest.append(EventTree(set(tokens), [event]))
            self.event_tree_partitions += 1
        while sum(len(tree.events) for tree in self.forest) > self.capacity:
            candidates = [tree for tree in self.forest if len(tree.events) > 1]
            if not candidates:
                self.forest.pop(0)
                continue
            tree = max(candidates, key=lambda item: len(item.events))
            # The compact summary is an actual stored node; retrieval never
            # consults the task's hidden answer or plan.
            merged = " ; ".join(tree.events[:2])
            tree.events[:2] = [merged]
            self.progressive_merges += 1

    def solve_observation(self, observation, step):
        for fact in observation.context:
            self._insert(fact)
        query = _tokens(observation.intent)
        ranked = sorted(
            self.forest, key=lambda tree: self._overlap(query, tree), reverse=True
        )
        neighborhood = tuple(
            event for tree in ranked[:2] for event in tree.events[-2:]
        )
        self.anchor_propagations += len(neighborhood)
        answer, plan = read_evidence(observation)
        if not answer or not plan:
            recovered = read_evidence(PublicObservation(
                observation.task_id, observation.intent, neighborhood
            ))
            answer, plan = answer or recovered[0], plan or recovered[1]
        self.actions += len(plan)
        self.cost += len(observation.context) + len(neighborhood)
        return answer, plan, "event-partition/event-tree/progressive-merge/anchor-propagation"
