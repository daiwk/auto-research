"""Answer-blind sufficiency routing and governed repair interfaces for AskALCF.

Seven coarse dispositions are preserved, not the unpublished complete 28-rule
router, agent judge, RAG system, or production knowledge-authoring workflow.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from hashlib import sha256
import json

REQUIRES_GPU_VALIDATION = False


@dataclass(frozen=True)
class SufficiencyRequest:
    question: str
    passages: tuple[str, ...]
    scope: str


def two_scope_sufficiency(question: str, production: Sequence[str], corpus: Sequence[str],
                          evaluator: Callable[[SufficiencyRequest], bool | None]) -> tuple:
    """The evaluator receives no generated answer, answer quality or gold label."""
    if not isinstance(question, str) or not question:
        raise ValueError("nonempty question required")
    if isinstance(production, str) or isinstance(corpus, str):
        raise TypeError("passages must be sequences, not strings")
    if any(not isinstance(p, str) for p in (*production, *corpus)):
        raise TypeError("passages must be text")
    results = tuple(evaluator(SufficiencyRequest(question, tuple(chunks), scope))
                    for chunks, scope in ((production, "production"), (corpus, "corpus")))
    if any(v is not None and type(v) is not bool for v in results):
        raise TypeError("sufficiency judgments must be bool or unknown")
    return results


@dataclass(frozen=True)
class Evidence:
    production_sufficient: bool | None = None
    corpus_sufficient: bool | None = None
    tool_error: bool | None = None
    policy_failure: bool | None = None
    fabricated_citation: bool | None = None
    faithful: bool | None = None
    correct: bool | None = None
    conflicting_signals: bool = False

    def __post_init__(self) -> None:
        if any(v is not None and type(v) is not bool for v in vars(self).values()):
            raise TypeError("evidence is three-valued bool, not numeric confidence")


def route(evidence: Evidence) -> str:
    """First supported match; missing signals do not mean failure or success."""
    if evidence.tool_error is True:
        return "tools_mcp"
    if evidence.conflicting_signals:
        return "unknown"
    if evidence.policy_failure is True:
        return "prompt"
    if evidence.production_sufficient is False:
        if evidence.corpus_sufficient is False:
            return "knowledge"
        if evidence.corpus_sufficient is True:
            return "retrieval"
    if evidence.production_sufficient is True:
        if (evidence.fabricated_citation is True or evidence.faithful is False
                or evidence.correct is False):
            return "model"
        if evidence.faithful is True and evidence.correct is True:
            return "no_failure"
    return "unknown"


@dataclass(frozen=True)
class Revisions:
    model: str
    prompt: str
    corpus: str
    retrieval: str
    tools: str
    evaluator: str

    def __post_init__(self) -> None:
        if any(not isinstance(v, str) or not v.strip() for v in vars(self).values()):
            raise ValueError("all cache dependencies must have explicit revisions")


class ExpansionCache:
    """Content-addressed in-memory interface; persistence belongs to the harness."""

    def __init__(self) -> None:
        self._entries: dict[str, tuple[str, ...]] = {}

    def get(self, query: str, revisions: Revisions,
            expand: Callable[[str], Sequence[str]], *, bypass: bool = False) -> tuple[str, ...]:
        if not isinstance(query, str) or not query:
            raise ValueError("query required")
        key = sha256(json.dumps([query, vars(revisions)], sort_keys=True).encode()).hexdigest()
        if not bypass and key in self._entries:
            return self._entries[key]
        value = expand(query)
        if isinstance(value, str):
            raise TypeError("expansion must be a sequence of nonempty strings")
        frozen = tuple(value)
        if any(not isinstance(x, str) or not x for x in frozen):
            raise TypeError("expansion must be a sequence of nonempty strings")
        if not bypass:
            self._entries[key] = frozen
        return frozen


def repair_noise_report(before: Sequence[bool], after: Sequence[bool],
                        null: Sequence[bool]) -> dict:
    """Report paired after-vs-null effects, not selected-before improvement.

    The conservative local gate requires a net count larger than all null
    flips as well as a rate gain above null drift; it is not a significance test.
    The real human ship/revert decision remains a separate callback interface.
    """
    if not before or len(before) != len(after) or len(before) != len(null):
        raise ValueError("nonempty paired arms of equal length required")
    if any(type(x) is not bool for arm in (before, after, null) for x in arm):
        raise TypeError("arm outcomes must be bool")
    n = len(before)
    gain = (sum(after) - sum(null)) / n
    drift = (sum(null) - sum(before)) / n
    flips = sum(a != b for a, b in zip(before, null))
    return {"after_minus_null": gain, "null_rate_drift": drift,
            "null_flip_count": flips,
            "clears_local_noise_gate": gain > abs(drift) and sum(after) - sum(null) > flips}


def reviewed_action(decision: str, ship: Callable[[], object],
                    revert: Callable[[], object]) -> dict:
    if decision not in {"ship", "revert", "decline"}:
        raise ValueError("an explicit human decision is required")
    if decision == "decline":
        return {"decision": decision, "executed": False, "succeeded": False}
    try:
        result = (ship if decision == "ship" else revert)()
    except Exception as error:
        return {"decision": decision, "executed": True, "succeeded": False,
                "error_type": type(error).__name__}
    return {"decision": decision, "executed": True, "succeeded": result is True}


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("CPU protocol only")
    observed = []

    def judge(request: SufficiencyRequest) -> bool:
        observed.append(request)
        return "supported" in request.passages

    r, c = two_scope_sufficiency("public question", ("other",), ("supported",), judge)
    calls = []
    cache = ExpansionCache()
    revisions = Revisions("m1", "p1", "c1", "r1", "t1", "e1")

    def expand(query: str) -> list[str]:
        calls.append(query)
        return [query, f"probe-{seed}"]

    cache.get("q", revisions, expand)
    cache.get("q", revisions, expand)
    cache.get("q", Revisions("m1", "p1", "c2", "r1", "t1", "e1"), expand)
    cache.get("q", revisions, expand, bypass=True)
    actions = []

    def ship() -> bool:
        actions.append("ship")
        return True

    declined = reviewed_action("decline", ship, lambda: True)
    shipped = reviewed_action("ship", ship, lambda: True)
    noise = repair_noise_report((False, True), (True, True), (True, False))
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "checks": {"answer_blind_probe": all(not hasattr(x, "answer") for x in observed),
                       "retrieval_not_model": route(Evidence(r, c, correct=False)) == "retrieval",
                       "missing_not_healthy": route(Evidence()) == "unknown",
                       "revision_and_null_cache": len(calls) == 3,
                       "opposing_null_flips_preserved": noise["null_flip_count"] == 2
                       and not noise["clears_local_noise_gate"],
                       "human_action_real_callback": not declined["executed"]
                       and shipped["succeeded"] and actions == ["ship"]},
            "metrics": {"probe_calls": len(observed), "expansion_callbacks": len(calls),
                        "action_callbacks": len(actions), "null_flips": noise["null_flip_count"]}}
