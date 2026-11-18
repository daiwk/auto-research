"""ERA v1 Algorithm 1 flat PUCT arithmetic over externally evaluated code.

This is not an empirical research agent. Code generation, sandboxing, research
ideas, task evaluation and validation/test isolation remain external duties.
Unlike recursive MCTS, every existing node competes for the next expansion.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import math
from numbers import Real
import random

REQUIRES_GPU_VALIDATION = False


def _finite(value, name):
    if isinstance(value, bool) or not isinstance(value, Real) or not math.isfinite(value):
        raise ValueError(f"finite {name} required")


@dataclass(frozen=True)
class Candidate:
    """Opaque code identity and external maximization-oriented validation score."""

    identity: str
    evidence_ref: str
    validation_score: float

    def __post_init__(self):
        if any(not isinstance(x, str) or not x.strip() for x in (self.identity, self.evidence_ref)):
            raise ValueError("explicit candidate identity and evaluation evidence reference required")
        _finite(self.validation_score, "external validation score")


@dataclass(frozen=True)
class Node:
    candidate: Candidate
    parent: str | None
    visits: int = 1


class FlatPUCT:
    """Literal v1 root/child visit=1; ancestors increment after expansion.

    Rank ties use average ranks and selection ties use identity order. The paper
    does not specify ties; these are explicit deterministic local conventions,
    not a claim of byte-identical upstream behavior. No rollout mean is used.
    """

    def __init__(self, root: Candidate, exploration_constant: float = 1.0):
        if not isinstance(root, Candidate):
            raise ValueError("externally evaluated root candidate required")
        _finite(exploration_constant, "exploration constant")
        if exploration_constant < 0:
            raise ValueError("exploration constant must be nonnegative")
        self._nodes = {root.identity: Node(root, None)}
        self.exploration_constant = exploration_constant

    @property
    def nodes(self) -> tuple[Node, ...]:
        return tuple(self._nodes.values())

    def rank_scores(self) -> dict[str, float]:
        """Ascending raw-score rank normalized by (rank-1)/(N-1)."""
        if len(self._nodes) == 1:
            return {next(iter(self._nodes)): 1.0}
        scores = [node.candidate.validation_score for node in self.nodes]
        return {key: (sum(score < node.candidate.validation_score for score in scores)
                      + (sum(score == node.candidate.validation_score for score in scores) - 1) / 2)
                     / (len(scores) - 1)
                for key, node in self._nodes.items()}

    def puct_scores(self) -> dict[str, float]:
        ranks = self.rank_scores()
        total = sum(node.visits for node in self.nodes)
        prior = 1 / len(self._nodes)
        return {key: ranks[key] + self.exploration_constant * prior * math.sqrt(total) / (1 + node.visits)
                for key, node in self._nodes.items()}

    def select(self) -> Candidate:
        scores = self.puct_scores()
        return self._nodes[min(scores, key=lambda key: (-scores[key], key))].candidate

    def expand(self, parent: str, candidate: Candidate) -> None:
        """Register a completed external evaluation, then update ancestors only."""
        if parent not in self._nodes or not isinstance(candidate, Candidate):
            raise ValueError("existing parent and externally evaluated candidate required")
        if candidate.identity in self._nodes:
            raise ValueError("candidate identity must be new")
        self._nodes[candidate.identity] = Node(candidate, parent)
        ancestor = parent
        while ancestor is not None:
            old = self._nodes[ancestor]
            self._nodes[ancestor] = Node(old.candidate, old.parent, old.visits + 1)
            ancestor = old.parent

    def best(self) -> Candidate:
        """Final choice uses external TaskScore, not exploration or test scores."""
        return min((node.candidate for node in self.nodes), key=lambda x: (-x.validation_score, x.identity))

    def run(self, generate_and_execute: Callable[[Candidate], Candidate], *, iterations: int) -> Candidate:
        if type(iterations) is not int or iterations < 0 or not callable(generate_and_execute):
            raise ValueError("nonnegative iteration budget and external callback required")
        for _ in range(iterations):
            parent = self.select()
            result = generate_and_execute(parent)
            self.expand(parent.identity, result)
        return self.best()


def diagnostic(seed: int, device: str = "cpu") -> dict:
    """Seeded score fixtures test control arithmetic, not research capability."""
    if device != "cpu":
        raise ValueError("CPU-only flat PUCT component; no CUDA model")
    if type(seed) is not int:
        raise ValueError("integer seed required")
    tree = FlatPUCT(Candidate("root", "fixture://root", 0.0), 0.8)
    singleton = tree.rank_scores()["root"] == 1 and tree.nodes[0].visits == 1
    tree.expand("root", Candidate("branch", "fixture://branch", .2))
    tree.expand("branch", Candidate("leaf", "fixture://leaf", .9))
    visits = {node.candidate.identity: node.visits for node in tree.nodes}
    flat = tree.select().identity == "leaf"
    values = [random.Random(seed).uniform(.3, .4), .7]
    callbacks = []

    def external(parent):
        index = len(callbacks)
        callbacks.append(parent.identity)
        return Candidate(f"new-{index}", f"fixture://new-{index}", values[index])

    winner = tree.run(external, iterations=2)
    ranks = tree.rank_scores()
    equal = FlatPUCT(Candidate("x", "fixture://x", 5), 0)
    equal.expand("x", Candidate("y", "fixture://y", 5))
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"nodes": len(tree.nodes), "external_evaluations": len(callbacks),
                        "total_visits": sum(node.visits for node in tree.nodes),
                        "fixture_best_validation_score": winner.validation_score,
                        "maximum_rank_score": max(ranks.values())},
            "checks": {"v1_singleton_rank_and_root_visits": singleton,
                       "ancestor_counts_not_rollout_means": visits == {"root": 3, "branch": 2, "leaf": 1},
                       "flat_selection_can_choose_deep_leaf": flat,
                       "bounded_external_evaluations": len(callbacks) == 2,
                       "best_uses_raw_validation_not_exploration": winner.identity == "leaf",
                       "rank_extrema": min(ranks.values()) == 0 and max(ranks.values()) == 1,
                       "explicit_average_rank_tie_convention": equal.rank_scores() == {"x": .5, "y": .5}}}
