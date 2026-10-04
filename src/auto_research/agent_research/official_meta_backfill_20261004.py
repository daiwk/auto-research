"""Auditable mechanisms from the 2026-10-04 Meta official-source backfill.

The functions in this module intentionally execute bounded, deterministic
mechanisms.  They do not call an LLM, execute generated code, expose hidden
labels to a search policy, or claim to reproduce the papers' production-scale
compute.
"""

from __future__ import annotations

from dataclasses import dataclass
import heapq
import math
from typing import Callable, Mapping, Sequence


def sira_filter_terms(
    terms: Sequence[str],
    document_frequency: Mapping[str, int],
    *,
    corpus_size: int,
    max_fraction: float,
    query_side: bool = True,
) -> tuple[str, ...]:
    """Apply SIRA's index-visible document-frequency gate.

    Query expansions must already occur in the index; corpus-side enrichment
    may introduce absent vocabulary.  Both paths reject overly common terms.
    """

    if corpus_size <= 0:
        raise ValueError("corpus_size must be positive")
    if not 0 < max_fraction <= 1:
        raise ValueError("max_fraction must be in (0, 1]")
    maximum_df = max_fraction * corpus_size
    accepted = []
    for term in terms:
        df = int(document_frequency.get(term, 0))
        if df < 0:
            raise ValueError("document frequency cannot be negative")
        if df <= maximum_df and (not query_side or df > 0):
            accepted.append(term)
    return tuple(accepted)


def sira_weighted_scores(
    original_scores: Sequence[float],
    expansion_scores: Sequence[float],
    *,
    expansion_weight: float,
) -> tuple[float, ...]:
    """Combine original-query and validated-expansion BM25 scores."""

    if len(original_scores) != len(expansion_scores):
        raise ValueError("score vectors must have the same length")
    if expansion_weight < 0:
        raise ValueError("expansion_weight must be non-negative")
    return tuple(
        float(original) + expansion_weight * float(expansion)
        for original, expansion in zip(original_scores, expansion_scores)
    )


def aira2_async_schedule(
    durations: Sequence[float], *, workers: int
) -> tuple[tuple[int, int, float, float], ...]:
    """Simulate barrier-free dispatch to the earliest available worker.

    Each result is ``(task_index, worker_index, start, finish)``.  This models
    the scheduling property only; it deliberately advertises no CUDA path.
    """

    if workers <= 0:
        raise ValueError("workers must be positive")
    if any(duration < 0 for duration in durations):
        raise ValueError("durations must be non-negative")
    available = [(0.0, worker) for worker in range(workers)]
    heapq.heapify(available)
    assignments = []
    for task, duration in enumerate(durations):
        start, worker = heapq.heappop(available)
        finish = start + float(duration)
        assignments.append((task, worker, start, finish))
        heapq.heappush(available, (finish, worker))
    return tuple(assignments)


def aira2_hidden_consistent_select(
    search_scores: Mapping[str, float],
    validation_scores: Mapping[str, float],
) -> tuple[str, dict[str, object]]:
    """Select only after search, using hidden, fixed validation scores.

    Search scores may order exploration, but cannot decide the returned
    champion.  Test labels are intentionally absent from this API.
    """

    if not search_scores or search_scores.keys() != validation_scores.keys():
        raise ValueError("search and validation candidates must match and be non-empty")
    selected = max(validation_scores, key=lambda key: (validation_scores[key], key))
    return selected, {
        "search_frontier": max(search_scores, key=lambda key: (search_scores[key], key)),
        "validation_score": float(validation_scores[selected]),
        "test_labels_visible": False,
    }


@dataclass
class PAHFMemory:
    """Small explicit preference memory with pre/post-action feedback hooks."""

    preferences: dict[str, str]
    confidence: dict[str, float]

    @classmethod
    def empty(cls) -> "PAHFMemory":
        return cls(preferences={}, confidence={})

    def pre_action(self, context: str, *, threshold: float = 0.75) -> dict[str, object]:
        """Retrieve a preference or request clarification when uncertain."""

        value = self.preferences.get(context)
        score = float(self.confidence.get(context, 0.0))
        return {
            "context": context,
            "preference": value,
            "ask_clarification": value is None or score < threshold,
            "confidence": score,
        }

    def integrate_pre_action_feedback(
        self, context: str, preference: str, *, confidence: float = 1.0
    ) -> None:
        """Write an explicitly clarified preference before acting."""

        self._write(context, preference, confidence)

    def integrate_post_action_feedback(
        self, context: str, corrected_preference: str
    ) -> bool:
        """Overwrite stale memory after a correction; return whether it drifted."""

        drifted = self.preferences.get(context) not in (None, corrected_preference)
        self._write(context, corrected_preference, 1.0)
        return drifted

    def _write(self, context: str, preference: str, confidence: float) -> None:
        if not context or not preference:
            raise ValueError("context and preference must be non-empty")
        if not 0 <= confidence <= 1:
            raise ValueError("confidence must be in [0, 1]")
        self.preferences[context] = preference
        self.confidence[context] = float(confidence)


def hyperagent_parent_probabilities(
    scores: Sequence[float],
    compiled_children: Sequence[int],
    *,
    top_m: int = 3,
    sharpness: float = 10.0,
) -> tuple[float, ...]:
    """Performance/novelty parent distribution from DGM-Hyperagents."""

    if not scores or len(scores) != len(compiled_children):
        raise ValueError("scores and child counts must match and be non-empty")
    if any(count < 0 for count in compiled_children):
        raise ValueError("compiled child counts cannot be negative")
    if top_m <= 0 or sharpness <= 0:
        raise ValueError("top_m and sharpness must be positive")
    frontier = sorted((float(score) for score in scores), reverse=True)[:top_m]
    midpoint = sum(frontier) / len(frontier)
    weights = []
    for score, children in zip(scores, compiled_children):
        scaled = sharpness * (float(score) - midpoint)
        sigmoid = 1.0 / (1.0 + math.exp(-max(-60.0, min(60.0, scaled))))
        weights.append(sigmoid / (1 + children))
    total = sum(weights)
    if total == 0:
        return tuple(1.0 / len(weights) for _ in weights)
    return tuple(weight / total for weight in weights)


def bounded_hyperagent_step(
    archive: Sequence[Mapping[str, object]],
    *,
    parent_index: int,
    modifier: Callable[[Mapping[str, object]], Mapping[str, object]],
    evaluator: Callable[[Mapping[str, object]], float],
    allowed_fields: frozenset[str] = frozenset({"strategy", "memory", "reflection"}),
) -> tuple[dict[str, object], ...]:
    """Add one evaluated structured variant without executing generated code."""

    if not 0 <= parent_index < len(archive):
        raise IndexError("parent_index outside archive")
    parent = dict(archive[parent_index])
    child = dict(modifier(dict(parent)))
    unexpected = child.keys() - allowed_fields
    if unexpected:
        raise ValueError(f"untrusted executable fields are not allowed: {sorted(unexpected)}")
    child["score"] = float(evaluator(child))
    child["parent_index"] = parent_index
    return tuple(dict(item) for item in archive) + (child,)
