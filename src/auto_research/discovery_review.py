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
from typing import Iterable


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
INDUSTRIAL_EVIDENCE_ANCHORS = (
    "online a/b", "online ab", "a/b test", "production a/b", "deployed in production",
    "fully deployed", "global traffic", "live traffic", "online experiment",
)


def classify_candidate(track: str, candidate: dict) -> dict:
    """Return a conservative, auditable first-pass review decision."""
    if track not in TRACK_ANCHORS:
        raise ValueError(f"unsupported discovery track: {track}")
    matched_queries = tuple(candidate.get("matched_queries", ()))
    text = f"{candidate.get('title', '')}\n{candidate.get('abstract', '')}".lower()
    anchors = tuple(anchor for anchor in TRACK_ANCHORS[track] if anchor in text)
    industrial_evidence = tuple(anchor for anchor in INDUSTRIAL_EVIDENCE_ANCHORS if anchor in text)
    priority = any(
        query == prefix or query.startswith(prefix + "-")
        for query in matched_queries
        for prefix in PRIORITY_QUERY_PREFIXES
    )
    if candidate.get("repository_status") != "new":
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
            "priority-fulltext-review", "industrial-fulltext-review", "manual-review"
        },
    }


def classify_artifact(artifact: dict) -> dict:
    rows = [classify_candidate(artifact["track"], item) for item in artifact.get("candidates", [])]
    return {
        **artifact,
        "schema_version": max(int(artifact.get("schema_version", 1)), 3),
        "classification_policy": "fail-closed-v1",
        "classification_counts": dict(sorted(Counter(row["review_bucket"] for row in rows).items())),
        "candidates": rows,
    }


def unresolved_candidates(artifacts: Iterable[dict]) -> list[dict]:
    return [
        row
        for artifact in artifacts
        for row in artifact.get("candidates", [])
        if row.get("full_text_review_required") and row.get("repository_status") == "new"
    ]
