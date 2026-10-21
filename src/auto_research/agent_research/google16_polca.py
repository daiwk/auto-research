"""POLCA priority/history/epsilon-net core; no implicit LLM or benchmark oracle.

Implements paper Algorithm 1 and farthest-first filter from the linked author
implementation. Summarizer, proposer, embedding and evaluator are real callback
interfaces; unit fixtures are not evidence of model optimization capability.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import math
import random
from typing import Callable, Sequence

PROTOCOL = "polca-empirical-queue-epsilon-net-component-v1"
UPSTREAM_COMMIT = "4ee52f12f0bb328dfee2f16b6c1801232c6ccf46"


@dataclass(frozen=True)
class Candidate:
    key: str
    parameter: str
    embedding: tuple[float, ...]

    def __post_init__(self):
        if not self.key or not self.parameter or not self.embedding:
            raise ValueError("candidate identity, parameter and embedding required")
        if any(not math.isfinite(x) for x in self.embedding):
            raise ValueError("finite embedding required")


@dataclass(frozen=True)
class EvaluationResult:
    score: float
    feedback: str
    output: object


@dataclass(frozen=True)
class Observation:
    candidate_key: str
    item_id: str
    input: object
    output: object
    score: float
    feedback: str
    round_index: int


@dataclass(frozen=True)
class History:
    candidate: Candidate
    observations: tuple[Observation, ...]

    @property
    def mean(self) -> float:
        return sum(x.score for x in self.observations) / len(self.observations)

    @property
    def sample_variance(self) -> float | None:
        n = len(self.observations)
        return None if n < 2 else sum((x.score - self.mean) ** 2 for x in self.observations) / (n - 1)


def epsilon_filter(proposals: Sequence[Candidate], memory: Sequence[Candidate], *,
                   epsilon: float) -> tuple[Candidate, ...]:
    """Greedy farthest-to-current-memory first, strict distance > epsilon.

    The epsilon=0 path follows the author's explicit no-filter ablation; duplicate
    identities still fail rather than corrupting the statistics dictionary.
    """
    if not math.isfinite(epsilon) or epsilon < 0:
        raise ValueError("nonnegative finite epsilon required")
    all_candidates = tuple(memory) + tuple(proposals)
    if len({p.key for p in all_candidates}) != len(all_candidates):
        raise ValueError("candidate identities must be unique")
    dimensions = {len(p.embedding) for p in all_candidates}
    if len(dimensions) > 1:
        raise ValueError("consistent embedding dimension required")
    if epsilon == 0:
        return tuple(proposals)
    remaining, accepted, existing = list(proposals), [], list(memory)
    while remaining:
        distances = [min((math.dist(p.embedding, q.embedding) for q in existing),
                         default=math.inf) for p in remaining]
        index = max(range(len(remaining)), key=lambda i: (distances[i], -i))
        if distances[index] <= epsilon:
            break
        candidate = remaining.pop(index)
        accepted.append(candidate)
        existing.append(candidate)
    return tuple(accepted)


@dataclass(frozen=True)
class RoundTrace:
    round_index: int
    minibatch_ids: tuple[str, ...]
    selected: tuple[str, ...]
    proposed: tuple[str, ...]
    admitted: tuple[str, ...]
    deferred_budget: tuple[str, ...]
    summary: str
    metric_calls: int


class Polca:
    """Small synchronous bounded controller; never receives a test split.

    Minibatches are sampled with replacement. Repeated evaluations of promising
    programs update their empirical means/variance instead of keeping best-of-N
    noisy observations. This is paper §3 priority, not the theoretical UCB variant.
    """
    def __init__(self, initial: Candidate, *, epsilon: float, seed: int = 42,
                 max_metric_calls: int = 64, max_memory: int = 16):
        if not math.isfinite(epsilon) or epsilon < 0:
            raise ValueError("finite nonnegative epsilon required")
        if not 1 <= max_metric_calls <= 1000 or not 1 <= max_memory <= 128:
            raise ValueError("bounded metric/memory budgets required")
        self.epsilon, self.rng = epsilon, random.Random(seed)
        self.max_metric_calls, self.max_memory = max_metric_calls, max_memory
        self.memory = {initial.key: History(initial, ())}
        self.calls, self.traces = 0, []

    def histories(self) -> tuple[History, ...]:
        return tuple(self.memory.values())

    def _record(self, candidate, batch, evaluator, round_index):
        old = self.memory.get(candidate.key, History(candidate, ()))
        for item_id, value in batch:
            # Count before invocation so failures never silently restore a spent call.
            self.calls += 1
            observed_input = deepcopy(value)
            result = evaluator(candidate, value)
            if (not isinstance(result, EvaluationResult) or not math.isfinite(result.score)
                    or not isinstance(result.feedback, str)):
                raise ValueError("EvaluationResult with finite score, feedback and actual output required")
            observation = Observation(candidate.key, item_id, observed_input,
                                      deepcopy(result.output), result.score, result.feedback, round_index)
            old = History(candidate, old.observations + (observation,))
            self.memory[candidate.key] = old

    def round(self, validation: Sequence[tuple[str, object]], *,
              evaluator: Callable[[Candidate, object], EvaluationResult],
              summarizer: Callable[[tuple[History, ...]], str],
              proposer: Callable[[tuple[History, ...], str], Sequence[Candidate]],
              batch_size: int = 2, select_count: int = 1,
              split: str = "validation") -> RoundTrace:
        if split != "validation" or not validation or not 1 <= batch_size <= 16:
            raise ValueError("nonempty validation-only dataset and bounded batch required")
        if len({key for key, _ in validation}) != len(validation):
            raise ValueError("unique validation item IDs required")
        if not 1 <= select_count <= len(self.memory):
            raise ValueError("valid exploration count required")
        if self.calls + batch_size * select_count > self.max_metric_calls:
            raise RuntimeError("insufficient metric budget for an exploration minibatch")
        round_index = len(self.traces)
        batch = tuple(self.rng.choice(validation) for _ in range(batch_size))
        selected = sorted(self.histories(), key=lambda h: (
            -(h.mean if h.observations else math.inf), h.candidate.key))[:select_count]
        for history in selected:
            self._record(history.candidate, batch, evaluator, round_index)
        history = self.histories()
        summary = summarizer(history)
        if not isinstance(summary, str) or len(summary) > 24000:
            raise ValueError("bounded real summarizer response required")
        selected_history = tuple(self.memory[h.candidate.key] for h in selected)
        raw = tuple(proposer(selected_history, summary))
        if len(raw) > 16:
            raise ValueError("proposal budget exceeded")
        admitted = epsilon_filter(raw, [h.candidate for h in history], epsilon=self.epsilon)
        accepted, deferred = [], []
        for candidate in admitted:
            if (len(self.memory) >= self.max_memory or
                    self.calls + batch_size > self.max_metric_calls):
                deferred.append(candidate.key)
                continue
            # Identical sampled batch for old and new candidates, not a lucky resample.
            self._record(candidate, batch, evaluator, round_index)
            accepted.append(candidate.key)
        trace = RoundTrace(round_index, tuple(key for key, _ in batch),
                           tuple(h.candidate.key for h in selected), tuple(c.key for c in raw),
                           tuple(accepted), tuple(deferred), summary, self.calls)
        self.traces.append(trace)
        return trace

    def best(self) -> History:
        evaluated = [h for h in self.histories() if h.observations]
        if not evaluated:
            raise RuntimeError("no observed candidate")
        return min(evaluated, key=lambda h: (-h.mean, h.candidate.key))
