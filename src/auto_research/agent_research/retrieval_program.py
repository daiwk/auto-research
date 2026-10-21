"""A bounded typed subset of RPL's retrieval-program and mutation interface.

No Python source is evaluated. Dense/sparse retrieval and reranking are trusted
caller callbacks; they are not replaced with fabricated neural implementations.
This module does not implement GRPO, policy generation, SFT or a Python sandbox.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from typing import Callable

BREADTHS = (3, 5, 10, 20, 50)
RETENTIONS = (0, 3, 5, 10, 20)


@dataclass(frozen=True)
class Document:
    identifier: str
    text: str

    def __post_init__(self):
        if (not isinstance(self.identifier, str) or not self.identifier
                or not isinstance(self.text, str)):
            raise ValueError("public document identifier and text required")


@dataclass(frozen=True)
class RetrievalProgram:
    queries: tuple[str, ...]
    modality: str = "dense"
    breadth: int = 3
    retention: int = 0
    output_limit: int = 5

    def __post_init__(self):
        if (type(self.queries) is not tuple or not 1 <= len(self.queries) <= 4
                or any(not isinstance(query, str) or not query.strip() or len(query) > 2048
                       for query in self.queries) or len(set(self.queries)) != len(self.queries)
                or self.modality not in ("dense", "sparse", "fuse")
                or type(self.breadth) is not int or self.breadth not in BREADTHS
                or type(self.retention) is not int or self.retention not in RETENTIONS
                or type(self.output_limit) is not int or not 1 <= self.output_limit <= 20):
            raise ValueError("bounded query-preserving retrieval grammar required")


def dedup(documents: tuple[Document, ...]) -> tuple[Document, ...]:
    result, seen = [], set()
    for document in documents:
        if not isinstance(document, Document):
            raise ValueError("typed documents required")
        if document.identifier not in seen:
            result.append(document)
            seen.add(document.identifier)
    return tuple(result)


def reciprocal_rank_fusion(rankings: tuple[tuple[Document, ...], ...], *,
                           rank_constant: int = 60) -> tuple[Document, ...]:
    """Standard RRF; constant 60 is an explicit local convention, not fitted."""
    if type(rank_constant) is not int or rank_constant < 1:
        raise ValueError("positive rank constant required")
    scores, first, docs = {}, {}, {}
    for ranking in rankings:
        for rank, document in enumerate(dedup(ranking), 1):
            key = document.identifier
            if key in docs and docs[key] != document:
                raise ValueError("the same document identifier has conflicting content")
            docs[key] = document
            first.setdefault(key, len(first))
            scores[key] = scores.get(key, 0.) + 1. / (rank_constant + rank)
    return tuple(docs[key] for key in sorted(scores, key=lambda key: (-scores[key], first[key])))


Retriever = Callable[[str, int], tuple[Document, ...]]
Reranker = Callable[[str, tuple[Document, ...], int], tuple[Document, ...]]


@dataclass(frozen=True)
class RetrievalSDK:
    dense: Retriever
    sparse: Retriever
    rerank: Reranker


@dataclass(frozen=True)
class ExecutionResult:
    printed: tuple[Document, ...]
    retrieved_candidates: int
    unique_candidates: int
    primitive_calls: int


def execute(program: RetrievalProgram, sdk: RetrievalSDK) -> ExecutionResult:
    if not isinstance(program, RetrievalProgram) or not isinstance(sdk, RetrievalSDK):
        raise ValueError("typed retrieval program and SDK required")
    if any(not callable(callback) for callback in (sdk.dense, sdk.sparse, sdk.rerank)):
        raise ValueError("trusted retrieval callbacks required")
    rankings, calls = [], 0
    for query in program.queries:
        modes = ("dense", "sparse") if program.modality == "fuse" else (program.modality,)
        for mode in modes:
            ranking = getattr(sdk, mode)(query, program.breadth)
            if type(ranking) is not tuple or len(ranking) > program.breadth:
                raise ValueError("retriever exceeded its per-call document budget")
            dedup(ranking)  # Validate even when a single list is returned.
            rankings.append(ranking)
            calls += 1
    total = sum(map(len, rankings))
    documents = reciprocal_rank_fusion(tuple(rankings)) if len(rankings) > 1 else dedup(rankings[0])
    unique = len(documents)
    if program.retention:
        # The query is composed exclusively from the original policy queries.
        reranked = sdk.rerank("\n".join(program.queries), documents, program.retention)
        if type(reranked) is not tuple or len(reranked) > program.retention:
            raise ValueError("reranker exceeded retention budget")
        if len(dedup(reranked)) != len(reranked) or any(document not in documents for document in reranked):
            raise ValueError("reranking must select unique retrieved documents, not inject evidence")
        documents = reranked
        calls += 1
    return ExecutionResult(documents[:program.output_limit], total, unique, calls)


def structural_distance(candidate: RetrievalProgram, original: RetrievalProgram) -> tuple[int, ...]:
    return (int(candidate.modality != original.modality),
        int(bool(candidate.retention) != bool(original.retention)),
        int(candidate.queries != original.queries),
        abs(BREADTHS.index(candidate.breadth) - BREADTHS.index(original.breadth)),
        abs(RETENTIONS.index(candidate.retention) - RETENTIONS.index(original.retention)))


def mutations(original: RetrievalProgram) -> tuple[RetrievalProgram, ...]:
    """Appendix B grammar over subsets of existing queries; no invented query."""
    if not isinstance(original, RetrievalProgram):
        raise ValueError("typed original program required")
    variants = []
    for size in range(1, len(original.queries) + 1):
        for queries in combinations(original.queries, size):
            for modality, breadth, retention in product(("dense", "sparse", "fuse"), BREADTHS, RETENTIONS):
                candidate = RetrievalProgram(queries, modality, breadth, retention, original.output_limit)
                if candidate != original:
                    variants.append(candidate)
    return tuple(sorted(variants, key=lambda item: (structural_distance(item, original),
        item.queries, item.modality, item.breadth, item.retention)))


@dataclass(frozen=True)
class MutationTrial:
    program: RetrievalProgram
    execution: ExecutionResult
    retrieval_verified: bool


def verified_mutation(original: RetrievalProgram, sdk: RetrievalSDK, *,
                      verifier: Callable[[ExecutionResult], bool],
                      max_executions: int = 64) -> tuple[MutationTrial | None, tuple[MutationTrial, ...]]:
    """Verify nearest-distance variants, with an explicit bounded execution cap.

    A discovery-only verifier may close over training annotations. It is never
    passed to the program SDK or a continuation actor. Among equal-distance
    verified programs, actual returned candidate count and primitive calls break
    ties. A cap can stop search without a selected variant; it is not success.
    """
    if not callable(verifier) or type(max_executions) is not int or not 1 <= max_executions <= 256:
        raise ValueError("verifier and bounded execution count required")
    trials, verified, selected_distance = [], [], None
    for candidate in mutations(original):
        distance = structural_distance(candidate, original)
        if (selected_distance is not None and distance != selected_distance) or len(trials) >= max_executions:
            break
        execution = execute(candidate, sdk)
        passed = verifier(execution)
        if type(passed) is not bool:
            raise ValueError("retrieval verifier must return bool")
        trial = MutationTrial(candidate, execution, passed)
        trials.append(trial)
        if passed:
            selected_distance = distance
            verified.append(trial)
    selected = min(verified, key=lambda item: (item.execution.retrieved_candidates,
        item.execution.primitive_calls)) if verified else None
    return selected, tuple(trials)


@dataclass(frozen=True)
class ContinuationContext:
    question: str
    program: RetrievalProgram
    printed_evidence: tuple[Document, ...]


def continuation_context(question: str, trial: MutationTrial) -> ContinuationContext:
    if not isinstance(question, str) or not question.strip() or not trial.retrieval_verified:
        raise ValueError("public question and retrieval-verified mutation required")
    return ContinuationContext(question, trial.program, trial.execution.printed)


def supervision_spans(*, retrieval_verified: bool, answer_verified: bool) -> dict[str, bool]:
    """Span-level training contract, not token masks or an SFT implementation."""
    if type(retrieval_verified) is not bool or type(answer_verified) is not bool or not retrieval_verified:
        raise ValueError("only retrieval-verified trajectories enter distillation")
    return {"program": True, "environment_observation": False, "answer": answer_verified}
