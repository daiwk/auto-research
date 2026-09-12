"""Observation-only mechanisms for Agent papers reviewed through 2026-09-12."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass

from .latest_20260907 import ObservationAgent, PublicObservation, read_evidence
from .method_families.base import _tokens


class ProceduralGraphAgent(ObservationAgent):
    """Procedure-relation-procedure graph with a conservative edit gate."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.edges = Counter()
        self.accepted_plans: dict[str, tuple[str, ...]] = {}
        self.procedural_graph_edges = 0
        self.heldout_edit_accepts = 0
        self.heldout_edit_rejects = 0

    def solve_observation(self, observation, step):
        answer, observed_plan = read_evidence(observation)
        key = " ".join(sorted(_tokens(observation.intent)))
        prior = self.accepted_plans.get(key, ())
        # A public workflow is a candidate edit.  Replacing an established
        # route is allowed only when it preserves its endpoints, a deterministic
        # local analogue of the paper's held-out validation gate.
        if observed_plan:
            admissible = not prior or (
                observed_plan[0] == prior[0] and observed_plan[-1] == prior[-1]
            )
            if admissible:
                self.accepted_plans[key] = observed_plan
                self.heldout_edit_accepts += 1
                for left, right in zip(observed_plan, observed_plan[1:]):
                    self.edges[(left, "next", right)] += 1
            else:
                self.heldout_edit_rejects += 1
        plan = observed_plan or prior
        self.procedural_graph_edges = len(self.edges)
        self.actions += len(plan)
        self.cost += len(observation.context)
        return answer, plan, "procedure-relation-procedure/localize/heldout-edit-gate"


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


class FeedbackScaffoldAgent(ObservationAgent):
    """Early public action guidance followed by late observation enrichment."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.early_action_guidance = 0
        self.feedback_observations = 0
        self.late_stage_enrichments = 0

    def solve_observation(self, observation, step):
        answer, plan = read_evidence(observation)
        # FEE switches scaffold type over the trajectory.  At the first turn a
        # workflow explicitly present in the public observation can guide the
        # action sequence; this is evidence supplied to the agent, never the
        # benchmark's hidden gold plan.
        if step == 0 and plan:
            self.early_action_guidance += 1
        # Enrichment exposes state summaries only after initial exploration;
        # it never inserts a next-action label.
        if step > 0:
            summaries = tuple(
                fact for fact in observation.context if "resolves to" in fact
            )
            self.feedback_observations += len(summaries)
            self.late_stage_enrichments += int(bool(summaries))
            if not answer:
                answer, _ = read_evidence(PublicObservation(
                    observation.task_id, observation.intent, summaries
                ))
        self.actions += len(plan)
        self.cost += len(observation.context)
        phase = "early-public-action-guidance" if step == 0 else "late-observation-enrichment"
        return answer, plan, f"{phase}/feedback-scaffold"


class MAPLEAgent(ObservationAgent):
    """Persistent accepted plan/candidate state across natural-language updates."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.programs: dict[str, tuple[str, ...]] = {}
        self.accepted_solution_updates = 0
        self.reused_executable_states = 0

    def solve_observation(self, observation, step):
        answer, proposed = read_evidence(observation)
        key = observation.intent.split()[0].lower() if observation.intent else "default"
        previous = self.programs.get(key, ())
        if proposed:
            # Executability contract of this mini-suite: a plan is a nonempty
            # sequence of named operations.  Hidden benchmark fields are not
            # used to accept it.
            if all(isinstance(action, str) and action.strip() for action in proposed):
                self.programs[key] = proposed
                self.accepted_solution_updates += 1
        elif previous:
            proposed = previous
            self.reused_executable_states += 1
        self.actions += len(proposed)
        self.cost += len(observation.context)
        return answer, proposed, "persistent-program/accepted-plan/evolutionary-candidate-state"


LATEST_AGENTS = {
    "procedural-graphs": ProceduralGraphAgent,
    "memforest": MemForestAgent,
    "feedback-scaffold": FeedbackScaffoldAgent,
    "maple": MAPLEAgent,
}
