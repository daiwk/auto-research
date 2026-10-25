"""FinanceGym PIT and Eq.2 aggregation protocol, not FinanceHarness intelligence.

No corpus download, network, live-web access, LLM judging, rubric generation or
financial advice. Prediction code receives question/cutoff only; private rubric
and post-cutoff evidence enter only the separate post-submission evaluator.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import math
import random
from typing import Mapping, Sequence


@dataclass(frozen=True)
class Document:
    document_id: str
    published_on: date | None
    text: str


class PointInTimeStore:
    """Filter retriever-ranked IDs AND independently guard subsequent reads.

    Retrieval ranking is external, not invented by this protocol. Missing dates
    fail closed. Direct document reads may not bypass the publication cutoff.
    """
    def __init__(self, documents: Sequence[Document], cutoff: date):
        if type(cutoff) is not date or not documents or not all(isinstance(d, Document) for d in documents):
            raise ValueError("documents and an exact publication-date cutoff required")
        if any(not d.document_id or not isinstance(d.text, str) or (d.published_on is not None and type(d.published_on) is not date) for d in documents):
            raise ValueError("document IDs, strings and dates must be valid")
        if len({d.document_id for d in documents}) != len(documents):
            raise ValueError("document IDs must be unique")
        self._documents = {d.document_id: d for d in documents}
        self._cutoff = cutoff
        self._read_ids: set[str] = set()
        self.invalidated = False

    def search(self, ranked_ids: Sequence[str]) -> tuple[str, ...]:
        """Preserve external rank but remove future/unknown-date documents."""
        if len(set(ranked_ids)) != len(ranked_ids) or any(i not in self._documents for i in ranked_ids):
            raise ValueError("distinct indexed document IDs required")
        return tuple(i for i in ranked_ids if self._documents[i].published_on is not None
                     and self._documents[i].published_on <= self._cutoff)

    def read(self, document_id: str) -> str:
        document = self._documents[document_id]
        if document.published_on is None or document.published_on > self._cutoff:
            self.invalidated = True
            raise ValueError("PIT violation: run invalid, not an ordinary scoring error")
        self._read_ids.add(document_id)
        return document.text

    def validate_submission(self, cited_ids: Sequence[str], *, live_web_used: bool = False) -> None:
        if type(live_web_used) is not bool:
            raise ValueError("explicit Boolean live-web audit required")
        if live_web_used or any(i not in self._read_ids for i in cited_ids):
            self.invalidated = True
        if self.invalidated:
            raise ValueError("PIT/grounding contract invalidated: no score may be reported")


@dataclass(frozen=True)
class PrivateCriterion:
    criterion_id: str
    kind: str  # pre_cutoff or post_cutoff; never exposed to the evaluated agent.


def outcome_score(rubrics: Mapping[str, Sequence[PrivateCriterion]],
                  submitted_scores: Mapping[str, Mapping[str, int]], *,
                  invalidated_runs: Sequence[str] = (), kind: str | None = None) -> float:
    """Eq.2: average per-question normalized rubric scores, not pooled items.

    Inputs are post-submission criterion grades from an external judge, not
    predictions. All expected question/criterion IDs must be present; a PIT
    violation invalidates the evaluation, never becomes a zero or omitted case.
    Type-disaggregated scores follow the same question-equal normalization.
    """
    if invalidated_runs:
        raise ValueError("PIT leakage invalidates runs; cannot aggregate a benchmark score")
    if not rubrics or set(rubrics) != set(submitted_scores) or kind not in (None, "pre_cutoff", "post_cutoff"):
        raise ValueError("complete aligned question sets and valid criterion kind required")
    questions = []
    for question, criteria in rubrics.items():
        if (not criteria or any(not isinstance(c, PrivateCriterion) or not c.criterion_id
                               or c.kind not in {"pre_cutoff", "post_cutoff"} for c in criteria)
                or len({c.criterion_id for c in criteria}) != len(criteria)):
            raise ValueError("nonempty unique typed private criteria required")
        grades = submitted_scores[question]
        if set(grades) != {c.criterion_id for c in criteria} or any(type(v) is not int or not 0 <= v <= 4 for v in grades.values()):
            raise ValueError("all criterion scores must be integers on the five-tier 0..4 scale")
        selected = [c for c in criteria if kind is None or c.kind == kind]
        if selected:
            questions.append(math.fsum(grades[c.criterion_id] for c in selected) / (4 * len(selected)))
    if not questions:
        raise ValueError("no questions contain the selected criterion type")
    return math.fsum(questions) / len(questions)


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("pure CPU protocol diagnostic requires integer seed and device='cpu'")
    documents = [Document("past", date(2026, 1, 1), "historical evidence"),
                 Document("cutoff", date(2026, 1, 2), "cutoff-day evidence"),
                 Document("future", date(2026, 1, 3), "withheld future outcome"),
                 Document("unknown", None, "unverified date")]
    random.Random(seed).shuffle(documents)
    store = PointInTimeStore(documents, date(2026, 1, 2))
    visible = store.search(["future", "past", "unknown", "cutoff"])
    store.read("past")
    store.validate_submission(["past"])
    rejected = False
    try:
        store.read("future")
    except ValueError:
        rejected = True
    live_store = PointInTimeStore(documents, date(2026, 1, 2))
    live_store.read("past")
    live_web_rejected = False
    try:
        live_store.validate_submission(["past"], live_web_used=True)
    except ValueError:
        live_web_rejected = live_store.invalidated
    rubrics = {"q1": [PrivateCriterion("a", "pre_cutoff")],
               "q2": [PrivateCriterion("a", "pre_cutoff"), PrivateCriterion("b", "post_cutoff"), PrivateCriterion("c", "post_cutoff")]}
    score = outcome_score(rubrics, {"q1": {"a": 4}, "q2": {"a": 0, "b": 0, "c": 0}})
    return {"seed": seed, "metrics": {"documents": len(documents), "visible_documents": len(visible),
        "question_equal_score": score, "pooled_item_negative_control": .25, "model_calls": 0},
        "checks": {"search_cutoff_inclusive_fail_closed": visible == ("past", "cutoff"),
                   "read_cannot_bypass_cutoff": rejected and store.invalidated,
                   "question_equal_not_item_equal": score == .5,
                   "live_web_audit_invalidates_submission": live_web_rejected}}
