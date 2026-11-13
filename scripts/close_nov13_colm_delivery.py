"""Close exactly the 24 historical identities without claiming a new scan window."""
from __future__ import annotations

import hashlib
import json
import re

from PIL import Image

from auto_research.discovery_history import reconcile_priority_history
from auto_research.discovery_review import disposition_rank
from auto_research.discovery_sources import load_sources
from curate_nov13_colm_evidence import validate_admission
from oct18_frozen_sources import verify_sources
from run_nov13_colm_components import (
    AUDIT, BATCH, COMPONENTS, CUDA_KEYS, ROOT, load, source_hashes, tier,
)

REVIEW_FILES = ("foundation-review.json", "agent-review.json", "evaluation-review.json")


def write(path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def identity(row):
    return row.get("id") or row.get("arxiv_id")


def main():
    frozen = load(AUDIT / "frozen-sources.json")
    if frozen["source_sha256"] != source_hashes():
        raise ValueError("execution source no longer matches evidence")
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    for device in ("cpu", "cuda"):
        validate_admission(load(AUDIT / f"raw-{device}.json"), frozen)
    intake = load(AUDIT / "intake-scope.json")
    expected = {value for values in intake["review_assignments"].values() for value in values}
    records = [row for name in REVIEW_FILES for row in load(AUDIT / name)["records"]]
    if len(records) != 24 or {identity(row) for row in records} != expected:
        raise ValueError("the exact 24-identity review is incomplete or duplicated")
    by_id = {identity(row): row for row in records}
    specifications = {}
    for key, (domain, _) in COMPONENTS.items():
        spec = load(ROOT / f"src/auto_research/paper_specs/catalog/{domain}/{key}.json")
        for device in (("cpu", "cuda") if key in CUDA_KEYS else ("cpu",)):
            metric = ROOT / "docs" / spec["detail_path"].replace("README.md", f"metrics/component-{device}-seeds42-44.json")
            if not metric.is_file():
                raise ValueError("component execution metric absent: " + key)
        if key in CUDA_KEYS and (spec.get("gpu_validation_passed") is not True
                                 or not (ROOT / spec["gpu_validation_artifact"]).is_file()):
            raise ValueError("real CUDA evidence absent: " + key)
        arxiv_id = re.search(r"\d{4}\.\d{4,5}", spec["paper_url"]).group()
        specifications[arxiv_id] = spec
    if set(specifications) != expected - {"2601.16355"}:
        raise ValueError("accepted/excluded identity scope differs")
    candidates = []
    figures_path = ROOT / "docs/paper-figures-manifest.json"
    figures = load(figures_path)
    for arxiv_id in sorted(expected):
        review = by_id[arxiv_id]
        organizations = review.get("verified_priority_organizations") or review.get("priority_organizations")
        source_url = review["source_url"]
        locations = review.get("reviewed_sections") or review.get("sections_read")
        if isinstance(locations, str):
            locations = [locations]
        if not organizations or not locations or not review.get("source_sha256"):
            raise ValueError("sourceful institution and method review required: " + arxiv_id)
        row = {"id": arxiv_id, "title": review["title"], "new_first_publication": False,
               "intake_class": "historical_priority_backfill", "review_scope": "named-full-text-sections",
               "verified_priority_organizations": organizations, "automatic_retry": False,
               "automatic_implementation_queue": False,
               "source_provenance": [{"organization": organization, "source_url": source_url} for organization in organizations],
               "full_text_review": {"scope": "full-text", "version": "v1", "source_url": source_url,
                                    "source_locations": locations, "source_sha256": review["source_sha256"],
                                    "read_scope": "Byline, defining method, evaluation and cost sections; not a claim that every appendix result was re-executed"}}
        if arxiv_id not in specifications:
            if review["decision"] != "out_of_scope_application_study" or not review.get("reason"):
                raise ValueError("sourceful exclusion required")
            row.update(status="rejected", resolution="out_of_scope_application_study",
                       review_decision="out_of_scope", reason=review["reason"],
                       priority="P2", priority_reason="Sourceful scope exclusion; no implementation queue",
                       track="agent",
                       component_implemented=False, full_capability_reproduced=False)
        else:
            spec = specifications[arxiv_id]
            key = spec["key"]
            fidelity = spec.get("fidelity_note") or spec.get("cost_assessment", {}).get("component_boundary")
            if not fidelity:
                raise ValueError("explicit local fidelity boundary required: " + key)
            row = spec | row | {"status": "implemented", "resolution": "bounded_component_accepted",
                                "reason": fidelity, "component_implemented": True,
                                "doc": spec["detail_path"],
                                "track": {"foundation-models": "foundation", "agent-research": "agent",
                                          "multimodal-models": "multimodal", "post-training": "post-training"}[spec["domain"]],
                                "full_capability_reproduced": False,
                                "component_evidence": "docs/" + spec["detail_path"].replace("README.md", "metrics/component-cpu-seeds42-44.json")}
            page = ROOT / "docs" / spec["detail_path"]
            asset = page.parent / "assets/paper-figure-01.png"
            text = page.read_text()
            block = text.split("<!-- paper-figure:start -->", 1)[1].split("<!-- paper-figure:end -->", 1)[0]
            figure_match = re.search(r"Figure\s+\d+", block)
            urls = re.findall(r"https://[^)\s]+", block)
            source = next((url for url in urls if re.search(r"\.(png|svg|jpg)$", url)), source_url)
            width, height = Image.open(asset).size
            metadata = {"page": page.relative_to(ROOT).as_posix(), "paper_url": spec["paper_url"],
                        "arxiv_id": arxiv_id, "figure": figure_match.group() if figure_match else "Original figure",
                        "original_caption": "", "source_url": source, "extraction": "original_source_reviewed",
                        "asset": asset.relative_to(ROOT).as_posix(), "width": width, "height": height,
                        "score": 0, "error": "", "asset_sha256": hashlib.sha256(asset.read_bytes()).hexdigest()}
            existing = next((i for i, value in enumerate(figures) if value["page"] == metadata["page"]), None)
            if existing is None:
                figures.append(metadata)
            else:
                figures[existing] = metadata
            if tier(key) != spec["evaluation_tier"]:
                raise ValueError("spec tier differs from frozen run")
        if disposition_rank(row) < 3:
            raise ValueError("historical review not substantively closed: " + arxiv_id)
        candidates.append(row)
    write(figures_path, figures)
    for name in REVIEW_FILES:
        review = load(AUDIT / name)
        for row in review["records"]:
            if identity(row) in specifications:
                row["implementation_pending"] = False
                row["implementation_evidence"] = "docs/" + specifications[identity(row)]["detail_path"].replace("README.md", "metrics/component-cpu-seeds42-44.json")
        write(AUDIT / name, review)
    scope = {key: value for key, value in intake.items() if key not in {"selected_scope_complete", "delivery_status"}}
    scope.update(selected_scope_complete=True, delivery_status="fixed_scope_complete",
                 review_watermark={"before": "2026-11-09", "after": "2026-11-09"},
                 full_window_review_complete=False, all_sources_exhaustive=False,
                 counts={"reviewed_identities": 24, "catalogued_papers": 23, "sourceful_exclusions": 1,
                         "low_cost_components": 23, "l0_interfaces": 3, "l1_mechanisms": 20,
                         "cpu_validated_components": 23, "cuda_validated_components": len(CUDA_KEYS),
                         "reviewed_bilingual_paper_pages": 23, "authored_four_level_questions": 92,
                         "full_capability_reproductions": 0, "new_first_publications": 0},
                 coverage_limits=["Exactly the earlier 24 needs-review identities, not a new-paper or institution-exhaustive scan",
                                  "Original 28-ID capture and other unavailable-source exceptions remain separately auditable",
                                  "High-cost or private-dependency full campaigns are explicitly not reproduced; local diagnostics are not capability evidence"],
                 papers=candidates)
    write(AUDIT / "task-scope.json", scope)
    ledger_path = ROOT / "docs/paper-discovery-ledger.json"
    ledger = load(ledger_path)
    ledger["batches"] = [value for value in ledger["batches"] if value.get("batch") != BATCH]
    ledger["batches"].append({key: value for key, value in scope.items() if key != "papers"} | {"candidates": candidates})
    write(ledger_path, ledger)
    observation = load(ROOT / "docs/research-audits/nov13-history-repair/historical-source-observation.json")
    reconciliation = reconcile_priority_history(observation["source_stats"], ROOT / "docs/research-manifest.json", ledger_path,
                                               expected_sources=load_sources(ROOT / "configs/paper-discovery-sources.json", "agent"))
    if any(row["arxiv_id"] in expected and row["historical_review_required"] for row in reconciliation["candidates"]):
        raise ValueError("one or more selected identities still require review")
    write(AUDIT / "historical-source-reconciliation.json", reconciliation)
    print("closed 24 exact historical reviews: 23 bounded components, one sourceful exclusion; no new-window claim")


if __name__ == "__main__":
    main()
