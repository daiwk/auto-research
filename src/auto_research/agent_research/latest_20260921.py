"""Observation-safe kernels for the 2026-09-21 incremental paper batch."""

from __future__ import annotations

from collections import Counter

from .latest_20260907 import ObservationAgent, PublicObservation, read_evidence
from .method_families.base import _tokens


class AutoViewMemAgent(ObservationAgent):
    """Discover low-overlap write-time views before ordinary top-k retrieval."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.views: dict[str, list[str]] = {}
        self.view_discoveries = self.orthogonal_writes = self.view_consolidations = 0

    def solve_observation(self, observation, step):
        del step
        answer, plan = read_evidence(observation)
        for fact in observation.context:
            tokens = _tokens(fact)
            view = min(tokens, key=len) if tokens else "misc"
            bucket = self.views.setdefault(view, [])
            self.view_discoveries += int(not bucket)
            if fact not in bucket:
                bucket.append(fact); self.orthogonal_writes += 1
            if len(bucket) > self.capacity:
                del bucket[:-self.capacity]; self.view_consolidations += 1
        focused = [fact for key, facts in self.views.items() if key in _tokens(observation.intent) for fact in facts]
        if focused and (not answer or not plan):
            recovered = read_evidence(PublicObservation(observation.task_id, observation.intent, tuple(focused)))
            answer, plan = answer or recovered[0], plan or recovered[1]
        self.cost += len(observation.context); self.actions += len(plan)
        return answer, plan, "write-time-orthogonal-views/top-k"


class MACEAgent(ObservationAgent):
    """Maintain functional condition-action-output units with feedback weights."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.units: dict[str, tuple[str, ...]] = {}
        self.scores = Counter()
        self.pending = "default"
        self.functional_units = self.typed_relations = self.presentation_updates = 0

    def solve_observation(self, observation, step):
        del step
        answer, plan = read_evidence(observation)
        key = " ".join(sorted(_tokens(observation.intent))[:2]) or "default"
        if key in self.units:
            plan = self.units[key]; self.skills_reused += 1
        elif plan:
            self.units[key] = tuple(plan); self.functional_units += 1
            self.typed_relations += max(0, len(plan) - 1)
        self.pending = key
        self.cost += len(observation.context); self.actions += len(plan)
        return answer, plan, "memgog/support-repair/instruction"

    def observe(self, task, answer_ok, plan_ok, step):
        del task, step
        self.scores[self.pending] += 1 if answer_ok and plan_ok else -1
        self.presentation_updates += 1


class ArenaFlowAgent(ObservationAgent):
    """Expose tournament, pivotal-step and skill-credit accounting."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.tournament_comparisons = self.pivotal_step_updates = self.skill_utility_updates = 0

    def solve_observation(self, observation, step):
        del step
        answer, plan = read_evidence(observation)
        candidates = [tuple(plan), tuple(reversed(plan))] if plan else [()]
        winner = min(candidates, key=lambda candidate: sum(action not in observation.context for action in candidate))
        self.tournament_comparisons += max(0, len(candidates) - 1)
        self.pivotal_step_updates += len(winner)
        self.skill_utility_updates += int(bool(winner))
        self.cost += len(observation.context); self.actions += len(winner)
        return answer, winner, "tournament/hierarchical-credit/skill-prior"


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


LATEST_AGENTS = {
    "autoviewmem": AutoViewMemAgent,
    "mace": MACEAgent,
    "arenaflow": ArenaFlowAgent,
    "graphskillevo": GraphSkillEvoAgent,
}
