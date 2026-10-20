#!/usr/bin/env python3
"""Compact actual official-source receipts; never infer full-text coverage."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/oct20-components"
BASELINE = ROOT / "docs/research-audits/oct19-evening-components/source-coverage.json"
CATEGORIES = {"cs.AI", "cs.CL", "cs.IR", "cs.LG", "cs.CV", "cs.RO", "cs.SD", "eess.AS"}


def build(directory):
    capture = directory / "retrieval.json"
    receipts = json.loads(capture.read_text())
    prior = json.loads(BASELINE.read_text())
    baseline = next(x["sha256"] for x in prior["capture_inputs"] if x["artifact"] == "retrieval.json")
    if not receipts or any(x["status"] != "retrieved" for x in receipts):
        raise ValueError("actual successful page captures required")
    arxiv = [x for x in receipts if x["kind"] == "arxiv"]
    if {x["source"] for x in arxiv} != CATEGORIES or len(arxiv) != len(CATEGORIES):
        raise ValueError("eight category receipts required")
    for row in arxiv:
        if row["announced_on"] != "2026-10-20" or not row["parse_complete"] or row["expected_entries"] != row["parsed_entries"]:
            raise ValueError("wrong-day or incomplete bulletin")
    directories = []
    names = ("google-delta.json", "meta-delta.json", "google-deepmind-delta.json")
    for name in names:
        delta = json.loads((directory / name).read_text())
        pages = [r for r in receipts if r["source"] == delta["organization"]]
        if delta["baseline_sha256"] != baseline or delta["retrieved_pages"] != len(pages):
            raise ValueError("baseline or directory coverage differs")
        if {r["page"] for r in pages} != set(range(1, len(pages)+1)):
            raise ValueError("missing directory page")
        directories.append({**delta, "page_receipts": [{k: v for k, v in r.items() if k != "records"} for r in pages]})
    dates = sorted(x["checked_at"] for x in receipts)
    result = {"schema_version": 1, "review_as_of": "2026-10-20", "review_timezone": "Asia/Shanghai",
        "scope_kind": "selected_components_from_new_announcement", "all_sources_exhaustive": False,
        "latest_observed_arxiv_announcement": "2026-10-20",
        "review_watermark": {"before": "2026-10-15", "after": "2026-10-15", "advanced": False,
            "reason": "Selected paper batch, not full-source/full-window full-text closure."},
        "counts": {"selected_papers": 13, "bounded_components_or_interfaces": 10,
            "reference_only_high_cost": 3, "new_paper_identities": 13, "substantive_version_updates": 0,
            "gpu_validated_components": 6, "cpu_validated_components_or_interfaces": 4,
            "category_entries_including_crosslists_and_replacements": sum(r["parsed_entries"] for r in arxiv),
            "directory_new_urls_not_necessarily_new_papers": sum(len(d["new_directory_urls"]) for d in directories)},
        "source_check_window_utc": {"first_checked_at": dates[0], "last_checked_at": dates[-1]},
        "capture_inputs": [{"artifact": p.name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "committed": False}
            for p in (capture, *(directory / name for name in names))],
        "baseline_audit": "../oct19-evening-components/source-coverage.json", "baseline_capture_sha256": baseline,
        "receipt_hash_scope": "SHA256 of captured UTF-8 page, not an archived mirror or proof of global completeness.",
        "arxiv_sources": [{k: v for k, v in x.items() if k != "records"} for x in arxiv],
        "official_directory_deltas": directories,
        "priority_findings": [{"key": "muse-glimmer-30b", "id": "2610.24628", "organization": "Meta Superintelligence Labs",
            "resolution": "reference_only_high_cost_not_reproduced_review_done"}],
        "additional_candidate_dispositions": [
            {"id": "2610.24481", "title": "DuoLM", "organization_note": "First author independent; Google DeepMind coauthors verified in PDF",
             "status": "not_selected_under_industrial_evidence_gate", "reason": "Full-text benchmark and H100 throughput, but no production A/B or accepted full-traffic evidence found; Google collaboration does not waive industrial gate.",
             "source_url": "https://arxiv.org/pdf/2610.24481v1"},
            {"title": "Claim-Gated Source-Risk Auditing for Generative Search", "source_url": "https://research.google/pubs/claim-gated-source-risk-auditing-for-generative-search-2/",
             "status": "archived_unconfirmed_not_blocking", "reason": "Directory abstract identifies a methodological blueprint with synthetic workbook, not empirical capability. No original publication identity/date or method repository linked on inspected page; do not infer affiliation or invent implementation."},
            {"id": "2610.23968", "title": "IMPULSE", "status": "outside_fixed_batch", "reason": "Read for selection, not accepted or claimed fully reviewed in this batch."},
            {"id": "2610.25179", "title": "PLACE", "status": "archived_unconfirmed_not_blocking", "reason": "Project inaccessible and certification details not sufficiently specified for an honest defining implementation."},
        ],
        "limitations": ["A complete title/abstract parse is not full-text review of every entry.",
            "Meta page total not exposed; only six bounded listing pages were inspected, not exhaustive pagination.",
            "Google directory has four new URLs, not four qualifying new papers; Meta has one new URL; DeepMind zero.",
            "Selected papers have different original v1 dates, with Oct20 announcement; not thirteen papers first published today.",
            "High-cost full experiments are terminal review DONE, never implementations or automatic retries."]}
    AUDIT.mkdir(parents=True, exist_ok=True)
    (AUDIT / "source-coverage.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({"pages": len(receipts), "category_entries": result["counts"]["category_entries_including_crosslists_and_replacements"]}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture_directory", type=Path)
    build(parser.parse_args().capture_directory)
