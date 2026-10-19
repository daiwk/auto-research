#!/usr/bin/env python3
"""Reduce actual capture receipts to a compact audit, without committing abstracts."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from curate_oct18_component_evidence import require, write_json  # noqa: E402


def build(directory: Path):
    capture = directory / "retrieval.json"
    receipts = json.loads(capture.read_text())
    require(len(receipts) == 51 and all(r["status"] == "retrieved" for r in receipts), "51 successful captured pages required")
    previous = json.loads((ROOT / "docs/research-audits/oct19-components/source-coverage.json").read_text())
    baseline = next(r["sha256"] for r in previous["capture_inputs"] if r["artifact"] == "retrieval.json")
    categories, directories = [], []
    for row in receipts:
        if row["kind"] != "arxiv":
            continue
        require(row["announced_on"] == "2026-10-19" and row["expected_entries"] == row["parsed_entries"], "bulletin incomplete or wrong day")
        categories.append({k: v for k, v in row.items() if k != "records"})
    for source, filename, pages in (("Google", "google-delta.json", 28), ("Meta", "meta-delta.json", 6), ("Google DeepMind", "google-deepmind-delta.json", 9)):
        delta = json.loads((directory / filename).read_text())
        require(delta["baseline_sha256"] == baseline and delta["retrieved_pages"] == pages, "baseline/pagination differs")
        selected = [r for r in receipts if r["source"] == source]
        require(len(selected) == pages and {r["page"] for r in selected} == set(range(1, pages + 1)), "official page coverage differs")
        directories.append({**delta, "page_receipts": [{k: v for k, v in r.items() if k not in {"records", "page_counts"}} for r in selected]})
    dates = sorted(r["checked_at"] for r in receipts)
    result = {"schema_version": 1, "review_as_of": "2026-10-19", "review_timezone": "Asia/Shanghai",
        "scope_kind": "selected_components_from_new_announcement_and_substantive_replacement",
        "all_sources_exhaustive": False, "latest_observed_arxiv_announcement": "2026-10-19",
        "review_watermark": {"before": "2026-10-15", "after": "2026-10-15", "advanced": False,
            "reason": "Selected implementation batch, not full-source/full-window review closure."},
        "counts": {"selected_papers": 14, "bounded_components_or_interfaces": 11, "reference_only_high_cost": 3,
            "new_paper_identities": 13, "substantive_version_updates": 1, "gpu_validated_components": 7,
            "cpu_validated_components_or_interfaces": 4, "official_directory_new_urls": 0},
        "source_check_window_utc": {"first_checked_at": dates[0], "last_checked_at": dates[-1]},
        "capture_inputs": [{"artifact": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "committed": False}
            for path in (capture, directory / "google-delta.json", directory / "meta-delta.json", directory / "google-deepmind-delta.json")],
        "baseline_audit": "../oct19-components/source-coverage.json", "baseline_capture_sha256": baseline,
        "receipt_hash_scope": "SHA256 of captured UTF-8 page; receipt is not an archived mirror or evidence of global source completeness.",
        "arxiv_sources": categories, "official_directory_deltas": directories,
        "priority_findings": [{"id": "2610.22671", "key": "proper-agent", "collaboration": "MSU / Meta"},
            {"id": "2610.22681", "key": "ego-p2c", "collaboration": "ASU / Meta"}],
        "classification_note": "Directory delta zero does not imply no Meta arXiv publications; affiliation was checked in full text. UniRec v3 is a replacement, not a new identity.",
        "limitations": ["Full parsed bulletin is not a claim that every entry has been full-text reviewed.",
            "Other institution pages, author repositories and model releases were not exhausted.",
            "High-cost full reproductions are terminal review DONE, not implementations or retry work."]}
    write_json(ROOT / "docs/research-audits/oct19-evening-components/source-coverage.json", result)
    print(json.dumps({"receipts": len(receipts), "arxiv_categories": len(categories), "directory_pages": sum(len(d["page_receipts"]) for d in directories)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture_directory", type=Path)
    build(parser.parse_args().capture_directory)
