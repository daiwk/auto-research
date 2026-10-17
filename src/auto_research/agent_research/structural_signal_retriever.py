"""SSR's deterministic structural IDF index (§III), independently implemented.

The paper does not enumerate its fixed stopword list.  This component therefore
publishes an explicit local list and allows a caller to freeze another list;
it does not claim bit-identical upstream benchmark preprocessing.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import math
import re
from typing import Iterable

DEFAULT_STOPWORDS = frozenset((
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in", "is", "it", "of", "on",
    "or", "that", "the", "this", "to", "was", "were", "with",
))
NORMALIZATION_REVISION = "ssr-local-explicit-stopwords-v1"


def structural_signals(text: str, *, stopwords: frozenset[str] = DEFAULT_STOPWORDS,
                       limit: int = 64) -> frozenset[str]:
    if not isinstance(text, str) or not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 64:
        raise ValueError("text and integer signal limit within [1,64] required")
    if any(not isinstance(word, str) for word in stopwords):
        raise ValueError("stopwords must be strings")
    tokens = [token for token in re.findall(r"[a-z0-9]+", text.lower())
              if len(token) >= 2 and token not in stopwords]
    frequency = Counter(tokens)
    # Frequencies only decide retention. Scoring always uses binary presence.
    unigrams = sorted(frequency, key=lambda token: (-frequency[token], token))
    bigrams = sorted({f"{left} {right}" for left, right in zip(tokens, tokens[1:])})
    return frozenset((unigrams + bigrams)[:limit])


@dataclass(frozen=True)
class AgentCard:
    identifier: str
    name: str = ""
    description: str = ""
    skills: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    examples: tuple[str, ...] = ()
    tools: tuple[str, ...] = ()

    def capability_text(self) -> str:
        if not isinstance(self.identifier, str) or not self.identifier:
            raise ValueError("nonempty string card identifier required")
        fields = (self.name, self.description, *self.skills, *self.tags, *self.examples, *self.tools)
        if any(not isinstance(value, str) for value in fields):
            raise ValueError("capability fields must contain text, not labels or opaque objects")
        return " ".join(fields)


@dataclass(frozen=True)
class RetrievalHit:
    identifier: str
    score: float
    matched_signals: tuple[str, ...]


class StructuralSignalIndex:
    """No model, gold answer, relevant-card target or hidden fallback is accepted."""

    def __init__(self, cards: Iterable[AgentCard], *, stopwords: frozenset[str] = DEFAULT_STOPWORDS,
                 limit: int = 64) -> None:
        self.stopwords, self.limit = frozenset(stopwords), limit
        # Validate the configuration even for an empty registry.
        structural_signals("", stopwords=self.stopwords, limit=limit)
        self.signals: dict[str, frozenset[str]] = {}
        postings: dict[str, set[str]] = defaultdict(set)
        for card in cards:
            text = card.capability_text()
            if card.identifier in self.signals:
                raise ValueError("duplicate Agent Card identifier")
            signals = structural_signals(text, stopwords=self.stopwords, limit=limit)
            self.signals[card.identifier] = signals
            for signal in signals:
                postings[signal].add(card.identifier)
        self.postings = {signal: frozenset(ids) for signal, ids in postings.items()}
        n = len(self.signals)
        self.idf = {signal: math.log((n + 1) / (len(ids) + 1)) + 1
                    for signal, ids in self.postings.items()}

    def query(self, query: str, *, top_k: int = 20) -> list[RetrievalHit]:
        if not isinstance(top_k, int) or isinstance(top_k, bool) or top_k < 1:
            raise ValueError("positive integer top_k required")
        signals = structural_signals(query, stopwords=self.stopwords, limit=self.limit)
        candidates: set[str] = set()
        for signal in signals:
            candidates.update(self.postings.get(signal, ()))
        hits = []
        for identifier in candidates:
            matched = tuple(sorted(signals & self.signals[identifier]))
            hits.append(RetrievalHit(identifier, math.fsum(self.idf[signal] for signal in matched), matched))
        hits.sort(key=lambda hit: (-hit.score, -len(hit.matched_signals), hit.identifier))
        return hits[:top_k]


@dataclass(frozen=True)
class SelectionOutcome:
    status: str
    selected_identifier: str | None = None


def validate_orchestrator_selection(pool: list[RetrievalHit], selected_index: object = None,
                                    *, api_failed: bool = False) -> SelectionOutcome:
    """Validate external one-based model output, preserving every failure status.

    This is an interface only, not an LLM simulator.  Empty pools must not make
    an API call; the caller can check them before calling its provider.
    """
    if not pool:
        return SelectionOutcome("empty_pool")
    if api_failed:
        return SelectionOutcome("api_failure")
    if (not isinstance(selected_index, int) or isinstance(selected_index, bool)
            or not 1 <= selected_index <= len(pool)):
        return SelectionOutcome("invalid_index")
    return SelectionOutcome("selected", pool[selected_index - 1].identifier)


def outcome_counts(outcomes: Iterable[SelectionOutcome]) -> dict[str, int]:
    counts = {key: 0 for key in ("selected", "empty_pool", "api_failure", "invalid_index")}
    for outcome in outcomes:
        if outcome.status not in counts:
            raise ValueError("unknown outcome must not be silently excluded")
        counts[outcome.status] += 1
    return {"total_attempts": sum(counts.values()), **counts}
