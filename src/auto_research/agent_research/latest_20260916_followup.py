"""Observation-safe RepoAtlas and interactive-memory reference agents."""

from __future__ import annotations

from collections import Counter

import numpy as np

from .latest_20260907 import ObservationAgent, read_evidence
from .method_families.base import _tokens


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


class InteractiveMemoryAgent(ObservationAgent):
    """Planner/Trigger co-evolution using delayed observed success only."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.memory: dict[str, tuple[str, ...]] = {}
        self.value = Counter()
        self.pending_key = ""
        self.pending_plan: tuple[str, ...] = ()
        self.planner_updates = self.trigger_updates = self.delayed_rewards = 0

    def solve_observation(self, observation, step):
        answer, observed_plan = read_evidence(observation)
        key = " ".join(sorted(_tokens(observation.intent))[:2]) or "default"
        stored = self.memory.get(key, ())
        trigger = bool(stored) and self.value[key] >= 0
        plan = stored if trigger else observed_plan
        self.pending_key, self.pending_plan = key, tuple(observed_plan)
        self.trigger_updates += int(trigger)
        self.actions += len(plan)
        self.cost += len(observation.context) + int(trigger)
        return answer, plan, f"planner-trigger/{'retrieve' if trigger else 'observe'}"

    def observe(self, task, answer_ok, plan_ok, step):
        del task, step
        reward = 1 if answer_ok and plan_ok else -1
        self.value[self.pending_key] += reward
        self.delayed_rewards += 1
        if reward > 0 and self.pending_plan:
            if len(self.memory) >= self.capacity and self.pending_key not in self.memory:
                victim = min(self.memory, key=lambda key: self.value[key])
                self.memory.pop(victim)
            self.memory[self.pending_key] = self.pending_plan
            self.planner_updates += 1


LATEST_AGENTS = {"repoatlas": RepoAtlasAgent, "interactive-memory": InteractiveMemoryAgent}

