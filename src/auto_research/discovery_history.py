"""Bounded historical priority-source identities, separate from recent deltas.

This is source reconciliation, not institution attribution, method acceptance,
an implementation queue, or proof of exhaustive institutional history.
"""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import re
from typing import Iterable

from .discovery import repository_paper_records
from .discovery_review import (
    TERMINAL_EXCEPTION_RESOLUTIONS, disposition_rank, metadata_only_disposition,
    pending_implementation_disposition, priority_organizations,
)
from .discovery_sources import DiscoverySource
from .papers import canonical_arxiv_id

IDENTITY = re.compile(r"\d{4}\.\d{4,5}(?:v\d+)?")
SHA256 = re.compile(r"[0-9a-f]{64}")


def _fulltext(row: dict) -> bool:
    review = row.get("full_text_review")
    return (isinstance(review, dict) and review.get("scope") == "full-text"
            and bool(review.get("source_locations")))


def _review_state(rows: Iterable[dict]) -> tuple[str, dict | None]:
    """Reuse disposition semantics, but do not promote generic legacy labels."""
    relevant = [row for row in rows if not metadata_only_disposition(row)
                and row.get("review_scope") != "title-abstract-selection"
                and row.get("resolution") not in {"not_selected_this_window_p2", "not_selected_p2"}]
    substantive = [row for row in relevant if disposition_rank(row) >= 3]
    if substantive:
        row = substantive[-1]
        resolution = row.get("resolution", "")
        if resolution in TERMINAL_EXCEPTION_RESOLUTIONS and (
                "source" in resolution or resolution == "archived_unconfirmed_not_blocking"):
            return "archived-exception", row
        return "reviewed", row
    accepted = [row for row in relevant if pending_implementation_disposition(row) and _fulltext(row)]
    return ("accepted-unimplemented", accepted[-1]) if accepted else ("needs-review", None)


def reconcile_priority_history(
    source_stats: Iterable[dict], manifest_path: Path, ledger_path: Path, *,
    expected_sources: Iterable[DiscoverySource] = (),
) -> dict:
    """Reconcile exact captured IDs without date filters, title search, or network.

    Inventory rows must refer to a real decoded-text capture receipt in the same
    source observation. The original capture may be archived separately; no
    local web cache is read here. Caller-provided source affiliations signal
    priority review, never prove authorship or industrial online evidence.
    """
    repository = repository_paper_records(manifest_path, ledger_path)
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    decisions: dict[str, list[dict]] = {}
    for batch in ledger.get("batches", []):
        for row in batch.get("candidates", []):
            identity = str(row.get("id", ""))
            if IDENTITY.fullmatch(identity):
                decisions.setdefault(canonical_arxiv_id(identity), []).append(row)
    expected = {source.name: source for source in expected_sources if source.historical_inventory}
    observations = [row for row in source_stats
                    if row.get("historical_inventory") is True or row.get("source") in expected]
    exceptions, sources, candidates = [], [], {}
    observed_names = {row.get("source") for row in observations}
    for name, source in expected.items():
        if name not in observed_names:
            exceptions.append({
                "source": name, "source_url": source.url, "type": "inventory_not_captured",
                "reason": "configured historical source has no observation; no zero-delta inference",
                "attempted": False, "counts_as_accepted": False,
                "automatic_implementation_queue": False,
            })
    for stat in observations:
        reference = {"source": stat["source"], "source_url": stat["url"],
                     "source_kind": stat.get("kind"), "organization": stat.get("organization")}
        priority = priority_organizations({"source_provenance": [reference]})
        receipts = stat.get("capture_receipts", [])
        captures = {(row.get("source_url"), row.get("decoded_text_sha256")) for row in receipts
                    if row.get("capture_kind") == "decoded-text-utf8"
                    and SHA256.fullmatch(str(row.get("decoded_text_sha256", "")))
                    and row.get("captured_at") and type(row.get("decoded_text_bytes")) is int
                    and row["decoded_text_bytes"] > 0}
        source_row = reference | {
            "priority_source_matches": list(priority), "capture_receipts": receipts,
            "inventory_scope": stat.get("inventory_scope", "configured source pages only"),
            "source_identity_count": len({row.get("arxiv_id") for row in stat.get("inventory_records", [])}),
        }
        sources.append(source_row)
        errors = []
        if stat.get("status") == "error":
            errors.append(("source_unavailable", stat.get("error", "source transport failed")))
        if stat.get("page_failures"):
            errors.append(("pages_unavailable", stat["page_failures"]))
        if stat.get("pagination_capped"):
            errors.append(("pages_uncovered", "declared source pagination exceeds configured coverage"))
        if not captures:
            errors.append(("capture_unavailable", "no fixed successful text capture receipt"))
        if not stat.get("inventory_records") and stat.get("status") != "error":
            errors.append(("identity_unresolved", "captured source exposed no fixed arXiv identities"))
        for kind, reason in errors:
            exceptions.append(reference | {"type": kind, "reason": reason,
                "attempted": bool(captures or stat.get("attempted_at") or stat.get("error")),
                "counts_as_accepted": False, "automatic_implementation_queue": False})
        for row in stat.get("inventory_records", []):
            identity = str(row.get("arxiv_id", ""))
            witness = (row.get("source_url"), row.get("decoded_text_sha256"))
            version = row.get("observed_version") or ""
            if (not priority or not IDENTITY.fullmatch(identity) or witness not in captures
                    or canonical_arxiv_id(identity) != identity
                    or row.get("identity_url") != f"https://arxiv.org/abs/{identity}{version}"
                    or row.get("observed_version") is not None
                    and not re.fullmatch(r"v\d+", str(row["observed_version"]))):
                exceptions.append(reference | {"type": "invalid_inventory_identity",
                    "reason": "priority provenance, exact identity/version, or capture witness missing",
                    "record": row, "counts_as_accepted": False,
                    "automatic_implementation_queue": False})
                continue
            identity = canonical_arxiv_id(identity)
            entry = candidates.setdefault(identity, {
                "arxiv_id": identity, "source_provenance": [], "inventory_witnesses": [],
                "priority_source_matches": [], "automatic_implementation_queue": False,
                "automatic_retry": False,
            })
            if reference not in entry["source_provenance"]:
                entry["source_provenance"].append(reference)
            if row not in entry["inventory_witnesses"]:
                entry["inventory_witnesses"].append(row)
            entry["priority_source_matches"] = sorted(set(entry["priority_source_matches"]) | set(priority))
    for identity, entry in candidates.items():
        known = repository.get(identity, {})
        state, decision = _review_state(decisions.get(identity, []))
        if known.get("catalogued") is True:
            state = "catalogued"
        needs_review = state == "needs-review"
        entry.update({
            "repository_status": ("selection-reviewed" if known.get("selection_only")
                                  else "new" if needs_review else known.get("repository_status", "reviewed")),
            "reconciliation_status": state,
            "catalogued": known.get("catalogued") is True,
            "historical_review_required": needs_review,
            "priority_review_required": needs_review,
            "full_text_review_required": needs_review,
            "review_bucket": "priority-fulltext-review" if needs_review else "already-closed",
            "review_reason": (
                "exact priority-source identity lacks substantive method/cost closure; old dates and P2 selection do not close it"
                if needs_review else "exact canonical identity or substantive disposition retained; not a new implementation task"),
            "method_review_completed": bool(decision and _fulltext(decision)),
            "method_or_cost_review_closed": state in {"reviewed", "accepted-unimplemented"},
            "full_capability_reproduced": False,
        })
        if decision:
            entry["prior_disposition"] = {key: decision[key] for key in (
                "status", "resolution", "review_decision", "reason", "cost_assessment", "source_exception",
            ) if key in decision}
    rows = [candidates[key] for key in sorted(candidates)]
    return {
        "schema_version": 1, "scope_kind": "bounded-historical-priority-inventory",
        "all_institutional_history_exhaustive": False, "review_watermark_advanced": False,
        "automatic_implementation_queue": False, "automatic_retry": False,
        "identity_matching": "exact arXiv identity only; never title or URL-slug similarity",
        "source_priority_is_authorship_proof": False,
        "industrial_online_evidence_accepted": False,
        "source_identity_count": len(rows),
        "reconciliation_counts": dict(sorted(Counter(row["reconciliation_status"] for row in rows).items())),
        "needs_original_review_count": sum(row["full_text_review_required"] for row in rows),
        "sources": sources, "candidates": rows, "exceptions": exceptions,
        "coverage_note": "Only configured captured source identities were reconciled; missing pages/sources are explicit exceptions, not evidence of exhaustive history.",
    }
