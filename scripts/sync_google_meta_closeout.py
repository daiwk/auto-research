#!/usr/bin/env python3
"""Append the bounded Oct21 decisions; never rewrite frozen review snapshots."""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from auto_research.discovery import repository_paper_records  # noqa: E402
from auto_research.gpu_validation import load_gpu_receipt  # noqa: E402

AUDIT = ROOT / "docs/research-audits/google-meta-closeout-20261021"
PREVIOUS = ROOT / "docs/research-audits/historical-backlog-reconciliation-20261021"
LEDGER = ROOT / "docs/paper-discovery-ledger.json"
BATCH = "20261021-google-meta-review-and-two-components"
COMPONENTS = {"2610.09159": ("agent", "specguard"),
              "2610.06616": ("foundation-model", "video-encoder-selection")}


def read(path):
    return json.loads(path.read_text())


def normalized_review(review):
    return {**deepcopy(review), "scope": "full-text",
        "reading_extent": review.get("scope", "bounded_key_sections"),
        "source_locations": review.get("read_sections") or review.get("source_locations"),
        "browser_line_ranges": review.get("source_locations"),
        "full_article_read": False}


def build_batch(ledger):
    previous = read(PREVIOUS / "reconciliation.json")
    reviews = read(AUDIT / "google39-reviews.json")["records"]
    if len(reviews) != 39 or [r["id"] for r in reviews] != previous["current_2026_google_review_leads"]:
        raise ValueError("bounded Google39 identity inventory changed")
    rows = []
    for row in reviews:
        proof = AUDIT / row["source_retrieval_reference"]
        if hashlib.sha256(proof.read_bytes()).hexdigest() != row["source_sha256"]:
            raise ValueError(f"source receipt changed: {row['id']}")
        accepted = row["review_decision"] == "accepted"
        reason = row["cost_assessment"]["decision_zh"]
        rows.append({**deepcopy(row),
            "status": "rejected" if row["status"] == "rejected_scope" else "deferred",
            "priority": "P1" if accepted else "P2",
            "review_decision": "excluded" if row["review_decision"] == "rejected_scope" else row["review_decision"],
            "reason": reason, "review_artifact": str((AUDIT / "google39-reviews.json").relative_to(ROOT / "docs")),
            "full_text_review": normalized_review(row["full_text_review"]),
            "source_provenance": [{"source_url": url, "organization": "Google source recall; authorship checked separately"}
                                  for url in row["official_identity_sources"]],
            "industrial_reproduction_qualified": bool(
                row["industrial_online_evidence"]["strict_online_ab_confirmed"]
                or row["industrial_online_evidence"]["explicit_full_traffic_confirmed"]),
            "cost_assessment": {**deepcopy(row["cost_assessment"]), "source_url": row["source_url"],
                                "scale": row["cost_assessment"]["paper_configuration_and_scale"],
                                "cost_type": "reported_configuration_or_explicitly_labelled_estimate"},
        })

    # Structured repair of the 14 accepted Oct15 observations, not new acceptance
    # or implementation. The authoritative register itself remains untouched.
    register_path = ROOT / "docs/research-audits/oct15-review-closure/paper-register.json"
    accepted14 = [r for r in read(register_path)["papers"] if r["status"] == "accepted"]
    if len(accepted14) != 14:
        raise ValueError("frozen Oct15 accepted inventory changed")
    existing = {r["id"]: r for b in ledger["batches"] if b["batch"] != BATCH
                for r in b.get("candidates", []) if r.get("id")}
    for entry in accepted14:
        old = existing[entry["id"]]
        rows.append({**deepcopy(old), "status": "deferred", "review_decision": "accepted",
            "implementation_status": "not_implemented", "review_done": True,
            "automatic_implementation_queue": False, "automatic_retry": False,
            "classification_repair_only": True,
            "classification_source": str(register_path.relative_to(ROOT)),
            "reason": old["reason"] + "；本轮仅补齐接受/未实现字段，不新增实施授权。"})

    decisions = read(PREVIOUS / "data/this-audit-dispositions.json")["decisions"]
    if len(decisions) != 9:
        raise ValueError("confirmed priority-nine scope changed")
    for entry in decisions:
        old = existing[entry["id"]]
        # Private production resources are not an unread/unreachable paper.
        # Keep the prior report frozen, but normalize the new ledger decision.
        resolution = ("not_reproduced_resource_unavailable" if entry["resolution"] == "source_unavailable_archived"
                      else entry["resolution"])
        row = {"id": entry["id"], "title": old["title"], "track": old["track"],
            "priority": "P1", "status": "deferred", "review_decision": "not_reproduced",
            "implementation_status": "not_implemented", "resolution": resolution,
            "full_experiment_resolution": resolution, "review_done": True,
            "automatic_implementation_queue": False, "automatic_retry": False,
            "reason": entry["full_experiment"] + "；" + entry["basis"],
            "low_cost_component_scope": entry["component"],
            "cost_assessment": {"source_url": entry["source"], "basis": entry["basis"],
                "scale": entry["basis"], "available_resource": "one A100 or A30, or local Mac",
                "cost_type": "prior_primary_source_report_or_labelled_estimate_not_local_measurement"},
            "full_text_review": {"scope": "full-text", "source_url": entry["source"],
                "source_locations": [entry["location"]], "full_article_read": False,
                "review_evidence_reused": str((PREVIOUS / "priority-google-meta.md").relative_to(ROOT))},
            "review_artifact": str((PREVIOUS / "data/this-audit-dispositions.json").relative_to(ROOT / "docs"))}
        if entry["id"] in COMPONENTS:
            track, key = COMPONENTS[entry["id"]]
            artifact = f"docs/gpu-validations/{key}-a100-20261021.json"
            receipt = load_gpu_receipt(ROOT / artifact)
            if receipt["adapter_key"] != key or receipt.get("diagnostic_only") is not True:
                raise ValueError(f"component evidence scope differs: {key}")
            row.update(status="implemented", review_decision="component_implemented",
                track=track, implementation_status="component_only", component_key=key, key=key,
                doc=(f"agent-research/{entry['id']}-{key}/README.md" if track == "agent" else
                     f"foundation-models/{entry['id']}-{key}/README.md"),
                requires_gpu_validation=True, gpu_validation_artifact=artifact,
                diagnostic_only=True, promotion_eligible=False, evolve_integrated=False,
                low_cost_component_scope="本轮已实现并真实CUDA验证的L1组件；详见独立论文页；不代表完整实验或能力复现")
        rows.append(row)
    if len(rows) != 62 or len({r["id"] for r in rows}) != 62:
        raise ValueError("expected disjoint 39 +14 classification repairs +9 priority decisions")
    return {"batch": BATCH, "date": "2026-10-21", "scope_kind": "bounded-priority-review-and-component-closeout",
        "required_tracks": [], "review_watermark_advanced": False, "all_sources_exhaustive": False,
        "automatic_implementation_queue": False,
        "source_artifact": "research-audits/google-meta-closeout-20261021/README.md",
        "candidates": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    ledger = read(LEDGER)
    batch = build_batch(ledger)
    previous = [b for b in ledger["batches"] if b["batch"] == BATCH]
    if args.check:
        if previous != [batch]:
            raise SystemExit("stale or missing bounded closeout ledger batch")
    else:
        if previous and previous != [batch]:
            raise SystemExit("existing batch differs; do not overwrite appended review history")
        if not previous:
            ledger["batches"].append(batch)
            LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n")
    records = repository_paper_records(ROOT / "docs/research-manifest.json", LEDGER)
    identities = read(PREVIOUS / "reconciliation.json")["current_2026_google_review_leads"]
    counts = dict(sorted(Counter(records.get(identity, {}).get("repository_status", "new") for identity in identities).items()))
    summary = {"schema_version": 1, "date": "2026-10-21", "batch": BATCH,
        "google39_repository_statuses": counts,
        "classification_repairs": 14, "priority_full_experiment_decisions": 9,
        "component_keys": [key for _, key in COMPONENTS.values()],
        "repository_counts_not_delivery_commitments": dict(sorted(Counter(r["repository_status"] for r in records.values()).items())),
        "automatic_implementation_queue": False, "review_watermark_advanced": False,
        "all_sources_exhaustive": False, "frozen_review_snapshots_modified": False,
        "limitations": ["39 source leads only, not all Google/Meta papers or all 497 old accepted candidates",
            "Accepted core opportunities remain unimplemented unless separately commissioned",
            "Catalogued, L1 components, interfaces, and full capability reproduction are different states",
            "Industrial A/B qualification is separate from a general mechanism/assessment opportunity"]}
    output = AUDIT / "current-state.json"
    content = json.dumps(summary, ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if not output.is_file() or output.read_text() != content:
            raise SystemExit("stale current-state closeout")
    else:
        output.write_text(content)
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
