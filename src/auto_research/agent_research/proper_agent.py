"""ProPerAgent graph/gate and strict timing protocol; no model or oracle policy."""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Callable, Sequence


@dataclass(frozen=True)
class MemoryFact:
    key: str
    subject: str
    relation: str
    object: str
    timestamp: float
    source_event: str
    passage: str
    kind: str = "episodic"
    open_loop: bool = False


@dataclass(frozen=True)
class Observation:
    timestamp: float
    description: str
    entities: tuple[str, ...]


@dataclass(frozen=True)
class GateEvidence:
    fact_keys: tuple[str, ...]
    text: str


@dataclass(frozen=True)
class DecisionView:
    observation: Observation
    evidence: GateEvidence | None
    already_spoken: tuple[tuple[float, str], ...]


@dataclass(frozen=True)
class Intervention:
    timestamp: float
    text: str


def _finite(value: float) -> bool:
    return type(value) in (int, float) and math.isfinite(value)


def _unit(values: Sequence[float]) -> tuple[float, ...]:
    if not values or any(not _finite(v) for v in values):
        raise ValueError("finite nonempty embedding required")
    norm = math.sqrt(sum(v*v for v in values))
    if norm == 0:
        raise ValueError("zero embedding")
    return tuple(v/norm for v in values)


class MemoryGraph:
    """Two-layer supplied facts with provenance and real personalized PageRank.

    Extraction/embeddings/gate are external trusted integrations, not substituted
    by gold facts. Hyperparameters below are explicit local choices: the paper
    does not publish all graph-ranking coefficients.
    """

    def __init__(self, facts: Sequence[MemoryFact], *, embed: Callable[[str], Sequence[float]],
                 synonym_threshold: float = .95):
        if not facts or len({f.key for f in facts}) != len(facts):
            raise ValueError("nonempty unique fact IDs required")
        if not _finite(synonym_threshold) or not -1 <= synonym_threshold <= 1:
            raise ValueError("invalid synonym threshold")
        for fact in facts:
            if (not all(isinstance(v, str) and v.strip() for v in (fact.key, fact.subject, fact.relation,
                         fact.object, fact.source_event, fact.passage)) or not _finite(fact.timestamp)
                    or type(fact.open_loop) is not bool
                    or fact.kind not in {"episodic", "semantic"}):
                raise ValueError("typed source-grounded fact required")
        self.facts = tuple(facts)
        self.embed = embed
        self.vectors = {name: _unit(embed(name)) for f in facts for name in (f.subject, f.object)}
        if len({len(v) for v in self.vectors.values()}) != 1:
            raise ValueError("embedding dimensions differ")
        self.synonym_threshold = synonym_threshold

    def retrieve(self, observation: Observation, *, limit: int = 8, restart: float = .15,
                 iterations: int = 80) -> tuple[MemoryFact, ...]:
        if (not _finite(observation.timestamp) or not observation.entities or type(limit) is not int
                or limit < 1 or not _finite(restart) or not 0 < restart <= 1
                or type(iterations) is not int or not 1 <= iterations <= 10_000
                or any(not isinstance(e, str) or not e.strip() for e in observation.entities)):
            raise ValueError("valid causal observation and PageRank parameters required")
        facts = [f for f in self.facts if f.timestamp <= observation.timestamp]
        if not facts:
            return ()
        names = sorted({name for f in facts for name in (f.subject, f.object)})
        edges = {name: set() for name in names}
        for f in facts:
            edges[f.subject].add(f.object)
            edges[f.object].add(f.subject)
        for i, a in enumerate(names):
            for b in names[i+1:]:
                if sum(x*y for x, y in zip(self.vectors[a], self.vectors[b])) >= self.synonym_threshold:
                    edges[a].add(b)
                    edges[b].add(a)
        seeds = {name: 0. for name in names}
        for entity in observation.entities:
            query = _unit(self.embed(entity))
            if len(query) != len(next(iter(self.vectors.values()))):
                raise ValueError("query embedding dimension differs")
            match = max(names, key=lambda n: sum(x*y for x, y in zip(query, self.vectors[n])))
            seeds[match] += 1/len(observation.entities)
        rank = dict(seeds)
        for _ in range(iterations):
            updated = {name: restart*seeds[name] for name in names}
            for name in names:
                neighbours = edges[name]
                if neighbours:
                    # Hub downweighting is a local configurable graph choice.
                    weights = {n: 1/math.sqrt(max(1, len(edges[n]))) for n in neighbours}
                    total = sum(weights.values())
                    for n, weight in weights.items():
                        updated[n] += (1-restart)*rank[name]*weight/total
                else:
                    for n in names:
                        updated[n] += (1-restart)*rank[name]*seeds[n]
            rank = updated
        def score(fact):
            return (rank[fact.subject]+rank[fact.object], fact.open_loop, fact.timestamp, fact.key)
        selected = sorted(facts, key=score, reverse=True)[:limit]
        # Narrative first, then semantic/episodic facts, preserving source IDs.
        return tuple(sorted(selected, key=lambda f: (f.kind != "semantic", -score(f)[0], f.key)))


def run_stream(graph: MemoryGraph, observations: Sequence[Observation], *,
               gate: Callable[[Observation, tuple[MemoryFact, ...]], GateEvidence | None],
               actor: Callable[[DecisionView], str | None]) -> tuple[Intervention, ...]:
    """Callbacks never receive reference windows, gold evidence or judge verdicts."""
    times = [o.timestamp for o in observations]
    if any(not _finite(t) for t in times) or any(a >= b for a, b in zip(times, times[1:])):
        raise ValueError("strictly increasing finite observation timestamps required")
    spoken: list[Intervention] = []
    for observation in observations:
        candidates = graph.retrieve(observation)
        evidence = gate(observation, candidates)
        if evidence is not None:
            allowed = {f.key for f in candidates}
            if (not isinstance(evidence.text, str) or not evidence.text.strip() or not evidence.fact_keys
                    or len(set(evidence.fact_keys)) != len(evidence.fact_keys)
                    or not set(evidence.fact_keys) <= allowed):
                raise ValueError("gate must cite actual retrieved provenance, or abstain")
        answer = actor(DecisionView(observation, evidence, tuple((s.timestamp, s.text) for s in spoken)))
        if answer is not None:
            if not isinstance(answer, str) or not answer.strip():
                raise ValueError("actor returns nonempty intervention or None")
            spoken.append(Intervention(observation.timestamp, answer))
    return tuple(spoken)


def score_clip(interventions: Sequence[Intervention], *, window: tuple[float, float] | None,
               judge: Callable[[Intervention], bool | None], tolerance: float = 2.) -> dict:
    """Private scorer only. None judge verdict stays unscored, not incorrect/dropped."""
    if (not _finite(tolerance) or tolerance < 0 or
            (window is not None and (len(window) != 2 or
             any(not _finite(t) for t in window) or window[0] > window[1]))):
        raise ValueError("valid private window/tolerance required")
    if any(not _finite(i.timestamp) or not i.text for i in interventions):
        raise ValueError("invalid intervention")
    verdicts = [judge(i) for i in interventions]
    if any(v is not None and type(v) is not bool for v in verdicts):
        raise ValueError("judge verdict must be bool or None")
    early = window is not None and any(i.timestamp < window[0] for i in interventions)
    late = window is not None and any(i.timestamp > window[1]+tolerance for i in interventions)
    hit = window is not None and any(window[0] <= i.timestamp <= window[1]+tolerance and v is True
                                     for i, v in zip(interventions, verdicts))
    scored = all(v is not None for v in verdicts)
    perfect = (not interventions if window is None else len(interventions) == 1 and hit)
    return {"fires": len(interventions), "scored": scored, "hit": hit, "early": early,
            "late": late, "over_trigger": len(interventions) > 1,
            "perfect": perfect if scored else None,
            "silent_clip_false_trigger": window is None and bool(interventions)}
