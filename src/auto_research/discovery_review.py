"""Fail-closed first-pass classification for high-recall discovery artifacts.

The classifier only removes obvious cross-domain query collisions.  A paper is
    kept for human review whenever it matches at least three independent query
    families or it was recalled by a Google/Meta sweep.  Lower-signal topical
    hits remain visible as P2/deferred candidates instead of disappearing.  The
result is deliberately conservative: downstream full-text review remains the
authority for implementation and industrial online-evidence decisions.
"""

from __future__ import annotations

from collections import Counter
import re
from typing import Iterable
from urllib.parse import urlparse


TRACK_ANCHORS: dict[str, tuple[str, ...]] = {
    "recommendation": (
        "recommend", "recommender", "ranking", "retrieval", "search", "advertis",
        "click-through", "conversion", "ctr", "user interest", "user behavior",
    ),
    "foundation-model": (
        "language model", "transformer", "attention", "long context", "inference",
        "pretrain", "vision-language", "multimodal", "mixture of experts", "token",
    ),
    "post-training": (
        "post-training", "preference optim", "reinforcement learning", "reward model",
        "policy optim", "policy distill", "rlhf", "grpo", "dpo", "verifier",
    ),
    "agent": (
        "agent", "tool use", "tool-use", "tool calling", "web navigation", "memory",
        "planning", "computer use", "software engineering", "multi-agent",
    ),
}

PRIORITY_QUERY_PREFIXES = ("priority-org-google", "priority-org-google-deepmind", "priority-org-meta")
METADATA_ONLY_REVIEW_SCOPES = frozenset({
    "historical_metadata_identity_date_scope_only", "identity_date_only", "metadata-only",
})
METADATA_ONLY_RESOLUTIONS = frozenset({"historical_first_publication", "historical_metadata_only"})
TERMINAL_EXCEPTION_RESOLUTIONS = frozenset({
    "not_reproduced_high_cost", "deferred_high_cost", "source_unavailable_archived",
    "source_exception_archived", "archived_unconfirmed_not_blocking",
    "not_reproduced_resource_unavailable", "not_reproduced_private_data",
})
ACCEPTED_UNIMPLEMENTED_RESOLUTIONS = frozenset({
    "affordable_candidate_not_implemented", "affordable_core_review_candidate",
    "accepted_core_not_implemented_this_run",
})
UNIMPLEMENTED_STATUSES = frozenset({
    "not_implemented", "pending", "not_implemented_by_review",
    "not_implemented_in_this_review",
})


def metadata_only_disposition(candidate: dict) -> bool:
    """An old publication date is bookkeeping, not a substantive rejection.

    Frozen historical snapshots keep their original labels. Consumers must not
    promote those labels to an algorithm/cost review merely because review_done
    was set. Explicit cost and unavailable-source decisions are not date-only.
    """
    if candidate.get("resolution") in TERMINAL_EXCEPTION_RESOLUTIONS:
        return False
    return (
        candidate.get("resolution") in METADATA_ONLY_RESOLUTIONS
        or candidate.get("review_scope") in METADATA_ONLY_REVIEW_SCOPES
        or candidate.get("review_level") == "historical_metadata_abstract_scope_triage"
    )


def pending_implementation_disposition(candidate: dict) -> bool:
    """Recognize review acceptance, never infer implementation authorization.

    Older registers encoded acceptance in ``resolution`` rather than
    ``review_decision``. Both structured forms remain visible. Free-text 'next
    batch'/'待实现' is not acceptance and cannot manufacture a delivery queue.
    """
    if candidate.get("resolution") in TERMINAL_EXCEPTION_RESOLUTIONS:
        return False
    return (
        candidate.get("resolution") in ACCEPTED_UNIMPLEMENTED_RESOLUTIONS
        or (candidate.get("review_decision") == "accepted"
            and candidate.get("implementation_status") in UNIMPLEMENTED_STATUSES)
    )


def disposition_status(candidate: dict) -> str:
    """Separate accepted opportunities from deferrals and terminal decisions."""
    if pending_implementation_disposition(candidate):
        return "accepted-unimplemented"
    if candidate.get("resolution") in TERMINAL_EXCEPTION_RESOLUTIONS:
        return "reviewed"
    if re.search(r"成本过高|not reproduced.{0,20}(?:cost|budget)|high[- ]cost",
                 str(candidate.get("reason", "")), re.I):
        return "reviewed"
    if candidate.get("status") == "deferred":
        return "review-deferred"
    return "reviewed"


def disposition_rank(candidate: dict) -> int:
    """Merge observations without allowing generic 'known' to close delivery.

    0: discovery/date observation; 1: legacy generic terminal label;
    2: accepted, delivery pending; 3: explicit substantive/cost/source closure.
    Catalog entries are assigned rank 4, without implying implementation. A legacy cost
    reason is retained, not silently reclassified into an expensive retry.
    """
    if candidate.get("status") not in {"implemented", "rejected", "deferred"}:
        return 0
    if candidate.get("resolution") in TERMINAL_EXCEPTION_RESOLUTIONS:
        return 3
    if metadata_only_disposition(candidate):
        return 0
    legacy_cost = bool(re.search(r"成本过高|not reproduced.{0,20}(?:cost|budget)|high[- ]cost",
                                 str(candidate.get("reason", "")), re.I))
    if legacy_cost:
        return 3
    if pending_implementation_disposition(candidate):
        return 2
    review = candidate.get("full_text_review", {})
    substantive_review = (isinstance(review, dict) and review.get("scope") == "full-text"
                          and bool(review.get("source_locations")))
    # Reading Methods is evidence of review, not a structured rejection. A
    # generic known row with reading locations must not outrank acceptance.
    explicit_decision = (
        candidate.get("review_decision") in {"rejected", "excluded", "out_of_scope"}
        or candidate.get("resolution") not in {None, "", "known", "already_known", "catalogued"}
    )
    if substantive_review and explicit_decision:
        return 3
    return 1


def priority_organizations(candidate: dict) -> tuple[str, ...]:
    """Recall priority from provenance, not abstract mentions or one query name.

    This is a review signal, never proof of authorship. Institution membership
    and paper eligibility still need primary-source review. Parse URL hosts and
    GitHub owners exactly, so lookalike domains cannot acquire priority.
    """
    found: set[str] = set()

    def organization(value):
        value = str(value or "")
        if re.search(r"\b(?:google|deepmind|youtube)\b", value, re.I):
            found.add("Google")
        if re.search(r"\b(?:meta|facebook|instagram)\b", value, re.I):
            found.add("Meta")

    for query in candidate.get("matched_queries", ()):
        for prefix in PRIORITY_QUERY_PREFIXES:
            if query == prefix or query.startswith(prefix + "-"):
                found.add("Meta" if prefix.endswith("meta") else "Google")
    for field in ("organization", "first_author_affiliation"):
        organization(candidate.get(field))
    for source in candidate.get("source_provenance", ()):
        organization(source.get("organization"))
        for field in ("source_url", "url", "repository_url"):
            parsed = urlparse(str(source.get(field, "")))
            host = (parsed.hostname or "").lower()
            if host in {"research.google", "deepmind.google", "research.google.com"}:
                found.add("Google")
            if host in {"ai.meta.com", "ai.facebook.com", "research.facebook.com", "research.meta.com"}:
                found.add("Meta")
            if host in {"github.com", "www.github.com"}:
                owner = parsed.path.strip("/").split("/", 1)[0].lower()
                if owner in {"google", "google-research", "google-deepmind", "deepmind"}:
                    found.add("Google")
                if owner in {"facebook", "facebookresearch", "meta-llama", "meta-recsys"}:
                    found.add("Meta")
    return tuple(sorted(found))


def priority_review_signal(candidate: dict) -> bool:
    return bool(candidate.get("priority_review_required") or priority_organizations(candidate))


INDUSTRIAL_EVIDENCE_ANCHORS = (
    "online a/b", "online ab", "a/b test", "production a/b", "deployed in production",
    "fully deployed", "global traffic", "live traffic", "online experiment",
    # Recall only: an abstract can report a launch without spelling out A/B;
    # the full-text gate below still decides whether quantitative evidence exists.
    "deployed as", "deployed across", "production launch", "consecutive launches",
    "served in production", "production evaluation",
)


def classify_candidate(track: str, candidate: dict) -> dict:
    """Return a conservative, auditable first-pass review decision."""
    if track not in TRACK_ANCHORS:
        raise ValueError(f"unsupported discovery track: {track}")
    matched_queries = tuple(candidate.get("matched_queries", ()))
    text = f"{candidate.get('title', '')}\n{candidate.get('abstract', '')}".lower()
    anchors = tuple(anchor for anchor in TRACK_ANCHORS[track] if anchor in text)
    industrial_evidence = tuple(anchor for anchor in INDUSTRIAL_EVIDENCE_ANCHORS if anchor in text)
    priority = priority_review_signal(candidate)
    if candidate.get("revision_review_required"):
        bucket = "revision-fulltext-review"
        reason = "known paper revision requires independent full-text review; not a new v1"
    elif candidate.get("repository_status") in {"implementation-pending", "accepted-unimplemented"}:
        bucket = "accepted-unimplemented"
        reason = "review accepted; no delivered implementation or automatic implementation authorization"
    elif candidate.get("repository_status") == "review-deferred":
        bucket = "review-deferred"
        reason = "retained deferral, not accepted implementation work; inspect recorded reason separately"
    elif candidate.get("historical_review_required"):
        bucket = "priority-fulltext-review" if priority else "historical-fulltext-review"
        reason = "historical identity/date triage is not a completed method or cost review"
    elif candidate.get("repository_status") != "new":
        bucket = "already-closed"
        reason = f"repository status is {candidate.get('repository_status')}"
    elif priority:
        bucket = "priority-fulltext-review"
        reason = "Google/Meta reverse-search hit; abstract is not used as the evidence gate"
    elif track == "recommendation" and anchors and industrial_evidence:
        bucket = "industrial-fulltext-review"
        reason = "recommendation topic plus possible production evidence; full text must verify quantified A/B"
    elif len(matched_queries) >= 3:
        bucket = "manual-review"
        reason = "at least three independent discovery query families matched"
    elif anchors or len(matched_queries) >= 2:
        bucket = "p2-deferred-review"
        reason = "topical hit retained for later P2 review; below the P0/P1 multi-query threshold"
    else:
        bucket = "query-collision"
        reason = "single broad query hit without a track anchor in title or abstract"
    return {
        **candidate,
        "review_bucket": bucket,
        "review_reason": reason,
        "matched_track_anchors": list(anchors),
        "matched_industrial_evidence_anchors": list(industrial_evidence),
        "full_text_review_required": bucket in {
            "priority-fulltext-review", "industrial-fulltext-review", "manual-review",
            "revision-fulltext-review", "historical-fulltext-review",
        },
    }


def classify_artifact(artifact: dict) -> dict:
    rows = [classify_candidate(artifact["track"], item) for item in artifact.get("candidates", [])]
    return {
        **artifact,
        "schema_version": max(int(artifact.get("schema_version", 1)), 3),
        "classification_policy": "review-delivery-separated-v2",
        "classification_counts": dict(sorted(Counter(row["review_bucket"] for row in rows).items())),
        "candidates": rows,
    }


def unresolved_candidates(artifacts: Iterable[dict]) -> list[dict]:
    return [
        row
        for artifact in artifacts
        for row in artifact.get("candidates", [])
        if row.get("full_text_review_required") and (
            row.get("repository_status") == "new" or row.get("revision_review_required")
            or row.get("historical_review_required")
        )
    ]
