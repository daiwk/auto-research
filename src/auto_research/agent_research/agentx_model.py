"""AgentX-Model proposal and outcome-blind historical-replay mechanisms.

The two roles here are deterministic and auditable, not a replacement for the
paper's private LLM agents or its 473-node production graph.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Iterable


class Action(StrEnum):
    REPRODUCE = "reproduce"
    FOLLOW_UP = "follow-up"
    COMPOSITION = "composition"
    DIAGNOSE = "diagnose"


@dataclass(frozen=True)
class Context:
    dataset: str
    split: str
    prediction: str
    metric: str
    baseline_version: str


@dataclass(frozen=True)
class Round:
    implementation: str
    auc: float | None
    pcoc: float | None = None
    status: str = "completed"


@dataclass(frozen=True)
class Experiment:
    key: str
    action: Action
    parents: tuple[str, ...]
    change: str
    context: Context
    rounds: tuple[Round, ...]
    question: str = ""

    @property
    def best(self) -> Round | None:
        valid = [r for r in self.rounds if r.status == "completed" and r.auc is not None]
        return max(valid, key=lambda r: r.auc) if valid else None


@dataclass(frozen=True)
class Candidate:
    key: str
    action: Action
    parents: tuple[str, ...]
    change: str
    context: Context


@dataclass(frozen=True)
class Proposal:
    key: str
    action: Action
    question: str
    starting_implementation: str
    modification: str
    evaluation: Context
    reference_auc: float


class Replay:
    """Candidate metadata is visible; its outcome is revealed only on selection."""

    def __init__(self, experiments: Iterable[Experiment], baseline_auc: float):
        records = tuple(experiments)
        self._records = {x.key: x for x in records}
        if not records or len(records) != len(self._records):
            raise ValueError("replay requires distinct experiment IDs")
        if not 0 <= baseline_auc <= 1:
            raise ValueError("invalid baseline AUC")
        self.baseline_auc = baseline_auc
        self.context = records[0].context
        self._seen: dict[str, Experiment] = {}
        for x in records:
            if x.context != self.context:
                raise ValueError("mixed evaluation contexts")
            if x.key in x.parents or any(p not in self._records for p in x.parents):
                raise ValueError("invalid dependency")
            if x.action == Action.COMPOSITION and len(x.parents) < 2:
                raise ValueError("composition requires two sources")
            if x.action in (Action.FOLLOW_UP, Action.DIAGNOSE) and not x.parents:
                raise ValueError("continuation requires a source")
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(key: str) -> None:
            if key in visiting:
                raise ValueError("cyclic graph")
            if key in visited:
                return
            visiting.add(key)
            for parent in self._records[key].parents:
                visit(parent)
            visiting.remove(key)
            visited.add(key)

        for key in self._records:
            visit(key)

    @property
    def seen(self) -> dict[str, Experiment]:
        return dict(self._seen)

    def available(self) -> tuple[Candidate, ...]:
        chosen = set(self._seen)
        return tuple(
            Candidate(x.key, x.action, x.parents, x.change, x.context)
            for x in self._records.values()
            if x.key not in chosen and set(x.parents) <= chosen
        )

    def select(self, key: str) -> Experiment:
        if key not in {x.key for x in self.available()}:
            raise ValueError("candidate not yet available")
        outcome = self._records[key]
        self._seen[key] = outcome
        return outcome

    def ancestors(self, key: str) -> tuple[Experiment, ...]:
        found: dict[str, Experiment] = {}

        def visit(current: str) -> None:
            for parent in self._records[current].parents:
                if parent not in self._seen:
                    raise ValueError("ancestor not revealed")
                if parent not in found:
                    found[parent] = self._seen[parent]
                    visit(parent)

        visit(key)
        return tuple(found.values())


class ResearchAgent:
    """Deterministic proposal assembler and independent proposal audit."""

    def propose(self, candidate: Candidate, revealed: dict[str, Experiment], baseline_auc: float) -> Proposal:
        if any(p not in revealed for p in candidate.parents):
            raise ValueError("unrevealed source")
        measured = [revealed[p].best for p in candidate.parents]
        measured = [r for r in measured if r is not None]
        start = max(measured, key=lambda r: r.auc).implementation if measured else "business-baseline"
        reference = max((r.auc for r in measured), default=baseline_auc)
        proposal = Proposal(candidate.key, candidate.action, candidate.change, start,
                            candidate.change, candidate.context, reference)
        self.audit(proposal, candidate, revealed, baseline_auc)
        return proposal

    @staticmethod
    def audit(proposal: Proposal, candidate: Candidate, revealed: dict[str, Experiment], baseline_auc: float) -> None:
        if proposal.key != candidate.key or proposal.action != candidate.action or proposal.evaluation != candidate.context:
            raise ValueError("proposal changes candidate or evaluation")
        if not proposal.modification.strip() or not proposal.starting_implementation:
            raise ValueError("incomplete proposal")
        if proposal.modification != candidate.change:
            raise ValueError("proposal changes approved modification")
        if any(revealed[p].context != proposal.evaluation for p in candidate.parents):
            raise ValueError("incomparable reference")
        rounds = [revealed[p].best for p in candidate.parents]
        measured = [r for r in rounds if r is not None]
        expected_start = max(measured, key=lambda r: r.auc).implementation if measured else "business-baseline"
        expected_reference = max((r.auc for r in measured), default=baseline_auc)
        if proposal.starting_implementation != expected_start or proposal.reference_auc != expected_reference:
            raise ValueError("proposal changes starting code or comparison reference")


class ModelAgent:
    """Execute an approved candidate and return its per-round measured outcomes."""

    def investigate(self, proposal: Proposal, replay: Replay) -> Experiment:
        candidate = {x.key: x for x in replay.available()}.get(proposal.key)
        if candidate is None:
            raise ValueError("proposal not executable")
        ResearchAgent.audit(proposal, candidate, replay.seen, replay.baseline_auc)
        return replay.select(proposal.key)


@dataclass
class ReplayResult:
    selections: list[dict[str, object]] = field(default_factory=list)
    best_auc: float = 0.0
    best_implementation: str = "business-baseline"
    target_at: int | None = None


def run_replay(replay: Replay, *, policy: str = "fixed", budget: int = 20, seed: int = 42) -> ReplayResult:
    """Fixed, random or revealed-parent-greedy routing; no hidden-outcome access.

    Diagnose is included in the four-action workflow but not in AUC-only
    allocation: its value of information is not measured by immediate AUC.
    """
    if policy not in {"fixed", "random", "parent-greedy"} or budget < 1:
        raise ValueError("unsupported policy or budget")
    rng = random.Random(seed)
    researcher, modeler = ResearchAgent(), ModelAgent()
    result = ReplayResult(best_auc=replay.baseline_auc)
    cycle = (Action.COMPOSITION, Action.FOLLOW_UP, Action.FOLLOW_UP, Action.REPRODUCE)
    for step in range(budget):
        available = [x for x in replay.available() if x.action != Action.DIAGNOSE]
        if not available:
            break
        if policy == "fixed":
            pool = []
            for offset in range(len(cycle)):
                pool = [x for x in available if x.action == cycle[(step + offset) % len(cycle)]]
                if pool:
                    break
            candidate = sorted(pool, key=lambda x: x.key)[0]
        elif policy == "random":
            candidate = rng.choice(available)
        else:
            def parent_auc(x: Candidate) -> float:
                rounds = [replay.seen[p].best for p in x.parents]
                return max((r.auc for r in rounds if r is not None), default=replay.baseline_auc)

            top = max(parent_auc(x) for x in available)
            candidate = rng.choice([x for x in available if parent_auc(x) == top])
        proposal = researcher.propose(candidate, replay.seen, replay.baseline_auc)
        observed = modeler.investigate(proposal, replay)
        best = observed.best
        if best and best.auc > result.best_auc:
            result.best_auc = best.auc
            result.best_implementation = best.implementation
        if result.target_at is None and result.best_auc > replay.baseline_auc + 0.001:
            result.target_at = step + 1
        ancestors = replay.ancestors(candidate.key)
        ancestor_auc = [x.best.auc for x in ancestors if x.best]
        result.selections.append({
            "id": candidate.key,
            "action": candidate.action.value,
            "parents": list(candidate.parents),
            "starting_implementation": proposal.starting_implementation,
            "reference_auc": proposal.reference_auc,
            "best_round": best.implementation if best else None,
            "validation_auc": best.auc if best else None,
            "delta_parent": best.auc - proposal.reference_auc if best and candidate.parents else None,
            "delta_path": best.auc - max(ancestor_auc) if best and ancestor_auc else None,
        })
    return result
