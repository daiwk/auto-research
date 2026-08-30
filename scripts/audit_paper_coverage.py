#!/usr/bin/env python3
"""Fail closed when a paper-discovery batch is incomplete or undocumented."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs/paper-discovery-ledger.json"
TERMINAL = {"implemented", "deferred", "rejected"}
PRIORITIES = {"P0", "P1", "P2"}
TOP_PRIORITY_INSTITUTIONS = {"Google", "Meta"}
REQUIRED_RECOMMENDATION_QUERY_FAMILIES = {
    "recsys-general",
    "recommendation-ranking",
    "generative-recommendation",
    "llm-recommendation",
    "industrial-ranking",
    "production-evidence",
    "deployment-evidence",
    "search-ranking",
    "advertising-ranking",
}


def audit(strict: bool = False, pending_artifacts: tuple[Path, ...] = ()) -> list[str]:
    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    errors: list[str] = []
    seen: set[tuple[str, str]] = set()
    reviewed_ids = {
        str(entry.get("id"))
        for batch in data.get("batches", [])
        for entry in batch.get("candidates", [])
    }
    if strict:
        for artifact_path in pending_artifacts:
            artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
            pending = [
                item["arxiv_id"] for item in artifact.get("candidates", [])
                if item.get("repository_status") == "new"
                and item.get("arxiv_id") not in reviewed_ids
            ]
            if pending:
                errors.append(f"{artifact_path}: unreviewed P0/P1 candidates: {pending}")
    for batch in data.get("batches", []):
        required = set(batch.get("required_tracks", []))
        present = {entry.get("track") for entry in batch.get("candidates", [])}
        verified_empty = set(batch.get("empty_tracks_verified", []))
        if verified_empty - required:
            errors.append(
                f"{batch['batch']}: verified empty tracks were not required: "
                f"{sorted(verified_empty - required)}"
            )
        if verified_empty & present:
            errors.append(
                f"{batch['batch']}: tracks cannot be both present and verified empty: "
                f"{sorted(verified_empty & present)}"
            )
        if verified_empty and not batch.get("empty_review", {}).get("source_artifact"):
            errors.append(f"{batch['batch']}: verified empty batch lacks source artifact")
        missing = required - present - verified_empty
        if strict and missing:
            errors.append(f"{batch['batch']}: tracks without candidates: {sorted(missing)}")
        if batch.get("scope_kind") == "global":
            required_subtopics = {
                (entry["track"], entry["subtopic"])
                for entry in batch.get("required_subtopics", [])
            }
            present_subtopics = {
                (entry.get("track"), entry.get("subtopic"))
                for entry in batch.get("candidates", [])
            }
            if not required_subtopics:
                errors.append(f"{batch['batch']}: global audit lacks required_subtopics")
            if strict and required_subtopics - present_subtopics:
                errors.append(
                    f"{batch['batch']}: subtopics without a reviewed candidate: "
                    f"{sorted(required_subtopics - present_subtopics)}"
                )
        if batch.get("scope_kind") == "institution-priority":
            required_institutions = set(batch.get("priority_institutions", []))
            if required_institutions != TOP_PRIORITY_INSTITUTIONS:
                errors.append(
                    f"{batch['batch']}: institution-priority audit must cover "
                    f"{sorted(TOP_PRIORITY_INSTITUTIONS)}"
                )
            sweeps = batch.get("institution_sweeps", [])
            swept = {entry.get("organization") for entry in sweeps}
            if required_institutions - swept:
                errors.append(
                    f"{batch['batch']}: missing institution sweeps: "
                    f"{sorted(required_institutions - swept)}"
                )
            candidate_ids = {entry.get("id") for entry in batch.get("candidates", [])}
            for sweep in sweeps:
                if not sweep.get("queries"):
                    errors.append(
                        f"{batch['batch']}: {sweep.get('organization')} sweep lacks queries"
                    )
                missing = set(sweep.get("candidate_ids", [])) - candidate_ids
                if missing:
                    errors.append(
                        f"{batch['batch']}: swept candidates lack terminal records: "
                        f"{sorted(missing)}"
                    )
                if sweep.get("candidate_discovery_gate") != "affiliation-and-topic":
                    errors.append(
                        f"{batch['batch']}: {sweep.get('organization')} candidates "
                        "must be discovered by affiliation and topic before evidence review"
                    )
                if sweep.get("abstract_online_evidence_required") is not False:
                    errors.append(
                        f"{batch['batch']}: {sweep.get('organization')} sweep must not "
                        "require online evidence in the abstract"
                    )
                if sweep.get("full_text_review_required") is not True:
                    errors.append(
                        f"{batch['batch']}: {sweep.get('organization')} sweep must "
                        "require full-text evidence review"
                    )
        for entry in batch.get("candidates", []):
            identity = (batch["batch"], entry.get("id", ""))
            if identity in seen:
                errors.append(f"duplicate candidate: {identity}")
            seen.add(identity)
            status = entry.get("status")
            if batch.get("scope_kind") == "global" and not entry.get("subtopic"):
                errors.append(f"{identity}: global-audit entry lacks subtopic")
            if entry.get("priority") not in PRIORITIES:
                errors.append(f"{identity}: invalid priority {entry.get('priority')!r}")
            if status not in TERMINAL:
                errors.append(f"{identity}: non-terminal status {status!r}")
            if batch.get("scope_kind") == "automated-review-closure":
                if not entry.get("matched_queries") and not entry.get("source_provenance"):
                    errors.append(f"{identity}: closure record lacks discovery provenance")
            if batch.get("scope_kind") == "institution-priority":
                if not entry.get("organization"):
                    errors.append(f"{identity}: priority candidate lacks organization")
                if not entry.get("evidence_gate"):
                    errors.append(f"{identity}: priority candidate lacks evidence gate")
                if not entry.get("priority_reason"):
                    errors.append(f"{identity}: priority candidate lacks priority reason")
                if entry.get("priority") != "P0":
                    errors.append(f"{identity}: Google/Meta eligible candidate is not P0")
                evidence_review = entry.get("evidence_review", {})
                if evidence_review.get("scope") != "full-text":
                    errors.append(f"{identity}: evidence was not reviewed in full text")
                if evidence_review.get("abstract_used_as_gate") is not False:
                    errors.append(f"{identity}: abstract must not be used as evidence gate")
                if not evidence_review.get("locations"):
                    errors.append(f"{identity}: full-text evidence locations are missing")
                if not evidence_review.get("matched_terms"):
                    errors.append(f"{identity}: full-text matched evidence terms are missing")
            if batch.get("scope_kind") == "high-recall-correction":
                if entry.get("track") == "recommendation" and not entry.get("matched_queries"):
                    errors.append(f"{identity}: recommendation candidate lacks query provenance")
            if status in {"deferred", "rejected"} and not entry.get("reason"):
                errors.append(f"{identity}: {status} entry lacks reason")
            if status == "implemented":
                doc = ROOT / "docs" / entry.get("doc", "")
                if not doc.is_file():
                    errors.append(f"{identity}: missing doc {doc.relative_to(ROOT)}")
                    continue
                text = doc.read_text(encoding="utf-8")
                for marker in (entry["id"], f"`{entry['key']}`", "## 论文信息", "## 本地复现", "<!-- paper-figure:start -->"):
                    if marker not in text:
                        errors.append(f"{identity}: doc missing {marker}")
        if batch.get("scope_kind") == "high-recall-correction":
            matrix = set(batch.get("query_matrix", []))
            if REQUIRED_RECOMMENDATION_QUERY_FAMILIES - matrix:
                errors.append(
                    f"{batch['batch']}: incomplete recommendation query matrix: "
                    f"{sorted(REQUIRED_RECOMMENDATION_QUERY_FAMILIES - matrix)}"
                )
            pagination = batch.get("pagination", {})
            if pagination.get("page_size", 0) < 25:
                errors.append(f"{batch['batch']}: page_size is too small for high recall")
            if pagination.get("maximum_results_per_query", 0) < 100:
                errors.append(
                    f"{batch['batch']}: maximum_results_per_query is too small for high recall"
                )
            organizations = set(batch.get("priority_organization_terms", []))
            if not {"Google", "Meta", "Netflix"} <= organizations:
                errors.append(
                    f"{batch['batch']}: Google, Meta and Netflix must be reverse-searched"
                )
            organization_queries = set(batch.get("organization_query_matrix", []))
            expected_organization_queries = {
                f"priority-org-{organization.lower().replace(' ', '-')}"
                for organization in organizations
            }
            if expected_organization_queries - organization_queries:
                errors.append(
                    f"{batch['batch']}: priority organizations lack explicit query coverage: "
                    f"{sorted(expected_organization_queries - organization_queries)}"
                )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--pending-artifact", type=Path, action="append", default=[])
    args = parser.parse_args()
    errors = audit(args.strict, tuple(args.pending_artifact))
    if errors:
        raise SystemExit("\n".join(errors))
    print("paper coverage audit: closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
