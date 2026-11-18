"""Materialize the accepted six-paper delivery, not historical exhaustiveness."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

from PIL import Image

from auto_research.discovery_history import reconcile_priority_history
from auto_research.discovery_sources import load_sources
from run_nov13_history_components import AUDIT, BATCH, COMPONENTS, ROOT, load, validate

KEYS = ["scientist-two", "ds-star", "era-flat-puct", "envharness", "mle-star", "alphaevolve"]


def write(path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def main():
    validate(load(AUDIT / "raw-cpu.json"), load(AUDIT / "frozen-sources.json"))
    records = load(AUDIT / "priority-inventory-review.json")["records"]
    by_id = {row["id"]: row for row in records}
    papers = []
    figures = load(ROOT / "docs/paper-figures-manifest.json")
    detailed = {row["page"]: row for row in load(AUDIT / "deep-dive-proposals-priority.json")["figure_metadata"]}
    for key in KEYS:
        spec = load(ROOT / f"src/auto_research/paper_specs/catalog/agent-research/{key}.json")
        identity = re.search(r"\d{4}\.\d{4,5}", spec["paper_url"]).group()
        component = key in COMPONENTS
        primary = by_id[identity]
        paper = spec | {
            "id": identity, "track": "agent", "doc": spec["detail_path"],
            "status": "implemented" if component else "deferred",
            "resolution": "bounded_l1_component_accepted" if component else "not_reproduced_high_cost",
            "reason": (spec["fidelity_note"] if component else spec["deferral_reason"]),
            "component_implemented": component, "full_capability_reproduced": False,
            "verified_priority_organizations": primary["verified_priority_organizations"],
            "new_first_publication": False, "intake_class": "historical_priority_backfill",
            "source_provenance": [{"organization": organization,
                "source_url": primary["source_receipts"][0]["url"]}
                for organization in primary["verified_priority_organizations"]],
            "full_text_review": {"scope": "full-text", "version": "v1",
                "source_url": f"https://arxiv.org/html/{identity}v1",
                "source_locations": primary["method_sections"],
                "read_scope": "Named defining-method and experimental-cost sections, byline and original publication history; not a claim to recheck every appendix result"},
        }
        if component:
            paper["component_evidence"] = "docs/" + spec["detail_path"].replace("README.md", "metrics/component-cpu-seeds42-44.json")
        papers.append(paper)
        path = ROOT / "docs" / spec["detail_path"]
        asset = path.parent / "assets/paper-figure-01.png"
        text = path.read_text()
        block = text.split("<!-- paper-figure:start -->", 1)[1].split("<!-- paper-figure:end -->", 1)[0]
        figure = re.search(r"Figure\s+\d+", block).group()
        meta = detailed.get(path.relative_to(ROOT).as_posix(), {})
        pngs = re.findall(r"https://[^)\s]+\.png", block)
        source_url = meta.get("source_url") or (pngs[0] if pngs else f"https://arxiv.org/html/{identity}v1/figure1.svg")
        width, height = Image.open(asset).size
        row = {"page": path.relative_to(ROOT).as_posix(), "paper_url": spec["paper_url"],
               "arxiv_id": identity, "figure": figure, "original_caption": "",
               "source_url": source_url, "extraction": "original_source_reviewed",
               "asset": asset.relative_to(ROOT).as_posix(), "width": width, "height": height,
               "score": 0, "error": "", "asset_sha256": hashlib.sha256(asset.read_bytes()).hexdigest()}
        figures = [old for old in figures if old["page"] != row["page"]] + [row]
    write(ROOT / "docs/paper-figures-manifest.json", figures)
    artifacts = ["preflight.json", "frozen-sources.json", "raw-cpu.json", "priority-inventory-review.json",
                 "scientist-two-review.json", "ds-star-review.json", "envharness-review.json",
                 "historical-source-observation.json", "fidelity-review.json"]
    scope = {"schema_version": 1, "batch": BATCH, "date": "2026-11-13",
             "scope_kind": "bounded-historical-priority-repair", "source_artifact": "research-audits/nov13-history-repair/README.md",
             "all_sources_exhaustive": False, "full_window_review_complete": False,
             "selected_scope_complete": True, "delivery_status": "bounded_scope_complete",
             "review_watermark_advanced": False,
             "review_watermark": {"before": "2026-11-09", "after": "2026-11-09"},
             "counts": {"selected_papers": 6, "component_implementations": 4, "cpu_validated_components": 4,
                        "cuda_validated_components": 0, "new_first_publications": 0, "historical_priority_backfills": 6,
                        "high_cost_full_experiments_not_reproduced": 5,
                        "commercial_dependency_full_experiments_not_run": 1, "review_only_papers": 2,
                        "full_capability_reproductions": 0, "authored_four_level_questions": 24},
             "artifacts": [{"path": (AUDIT / name).relative_to(ROOT / "docs").as_posix(),
                            "sha256": hashlib.sha256((AUDIT / name).read_bytes()).hexdigest()} for name in artifacts],
             "papers": papers,
             "unselected_leads": [{"id": "2604.15505", "title": "PolicyBank: Evolving Policy Understanding for LLM Agents",
                 "decision": "not_selected_current_focus_nonblocking_lead", "method_review_completed": False,
                 "implemented": False, "automatic_implementation_queue": False}],
             "coverage_limits": ["Only six explicitly selected related historical identities delivered; not all domains/institutions/history exhausted",
                 "COLM source identities are separate from accepted papers and implementation scope",
                 "Meta publication inventory is unavailable in the retained attempt; official related-work checks are bounded",
                 "DS-STAR development-task pricing is not inflated into large-GPU-training cost"],
             "automatic_implementation_queue": False, "automatic_retry": False}
    write(AUDIT / "task-scope.json", scope)
    ledger_path = ROOT / "docs/paper-discovery-ledger.json"
    ledger = load(ledger_path)
    ledger["batches"] = [row for row in ledger["batches"] if row.get("batch") != BATCH]
    ledger["batches"].append({key: value for key, value in scope.items() if key != "papers"} | {"candidates": papers})
    write(ledger_path, ledger)
    observed = load(AUDIT / "historical-source-observation.json")
    reconciliation = reconcile_priority_history(observed["source_stats"], ROOT / "docs/research-manifest.json", ledger_path,
                                               expected_sources=load_sources(ROOT / "configs/paper-discovery-sources.json", "agent"))
    write(AUDIT / "historical-source-reconciliation.json", reconciliation)
    print("six-paper bounded delivery recorded; history inventory remains independently unreviewed where applicable")


if __name__ == "__main__":
    main()
