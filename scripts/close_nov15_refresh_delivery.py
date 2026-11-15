"""Close the fixed Nov15 selection, never promote bulletin inventory to review."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

from PIL import Image

from auto_research.discovery_review import disposition_rank
from curate_nov15_refresh_evidence import validate_admission
from oct18_frozen_sources import verify_sources
from run_nov15_refresh_components import AUDIT, BATCH, COMPONENTS, CUDA_KEYS, ROOT, load, source_hashes


def write(path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def review_records():
    result = {}
    for name in ("foundation", "agent", "post", "root"):
        payload = load(AUDIT / f"{name}-review.json")
        for row in payload.get("records", payload.get("papers", payload.get("accepted", []))):
            key = row.get("key") or row.get("identity", ":").split(":", 1)[-1]
            if key:
                result[key] = row
    return result


def main():
    frozen, intake = load(AUDIT / "frozen-sources.json"), load(AUDIT / "intake-scope.json")
    if frozen["source_sha256"] != source_hashes():
        raise ValueError("execution source changed after actual run")
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    for device in ("cpu", "cuda"):
        validate_admission(load(AUDIT / f"raw-{device}.json"), frozen)
    reviews = review_records()
    figures = load(ROOT / "docs/paper-figures-manifest.json")
    candidates = []
    for identity in intake["accepted_papers"]:
        domain, key = identity.split(":", 1)
        spec = load(ROOT / f"src/auto_research/paper_specs/catalog/{domain}/{key}.json")
        review = reviews.get(key, {})
        source_hash = spec.get("method_source_sha256") or review.get("source_sha256")
        sections = (review.get("defining_sections") or review.get("reviewed_sections")
                    or review.get("sections_read") or review.get("source_locations") or spec.get("reviewed_sections"))
        if not source_hash or not sections:
            raise ValueError("primary source hash and explicit read locations missing: " + key)
        page = ROOT / "docs" / spec["detail_path"]
        if not page.is_file() or not page.with_name("README-en.md").is_file():
            raise ValueError("bilingual source pages missing: " + key)
        if not spec.get("review_done") or spec.get("automatic_implementation_queue") is not False:
            raise ValueError("cost/theory disposition is not explicit: " + key)
        is_component = key in COMPONENTS
        if is_component:
            for device in (("cpu", "cuda") if key in CUDA_KEYS else ("cpu",)):
                if not (page.parent / f"metrics/component-{device}-seeds42-44.json").is_file():
                    raise ValueError("executed evidence missing: " + key)
        elif list((page.parent / "metrics").glob("*.json")):
            raise ValueError("review-only article must not have fabricated metrics: " + key)
        if key in CUDA_KEYS and (spec.get("gpu_validation_passed") is not True
                                 or not (ROOT / spec["gpu_validation_artifact"]).is_file()):
            raise ValueError("real A100/A30 evidence missing: " + key)
        aid = re.search(r"\d{4}\.\d{4,5}", spec["paper_url"]).group()
        source_url = spec.get("reviewed_version_url") or spec["paper_url"]
        row = spec | {"id": aid, "status": "implemented" if is_component else "deferred",
                      "resolution": "bounded_component_accepted" if is_component else spec["review_resolution"],
                      "reason": spec.get("fidelity_note") or spec.get("experiment_scope") or spec["summary"],
                      "review_scope": "named-full-text-sections", "doc": spec["detail_path"],
                      "component_implemented": is_component, "full_capability_reproduced": False,
                      "track": {"recommendation": "recommendation", "foundation-models": "foundation-model",
                                "post-training": "post-training", "agent-research": "agent",
                                "multimodal-models": "multimodal"}[domain],
                      "new_first_publication": spec.get("published", "") >= "2026-11-10",
                      "full_text_review": {"scope": "full-text", "version": spec.get("reviewed_version", "v1"),
                                           "source_url": source_url, "source_sha256": source_hash,
                                           "source_locations": sections,
                                           "read_scope": "Byline, defining method, evaluation/cost sections; not an exhaustive-source or full-training claim"}}
        if disposition_rank(row) < 3:
            raise ValueError("not substantively closed: " + key)
        candidates.append(row)
        text = page.read_text()
        block = text.split("<!-- paper-figure:start -->", 1)[1].split("<!-- paper-figure:end -->", 1)[0]
        asset = page.parent / "assets/paper-figure-01.png"
        width, height = Image.open(asset).size
        match = re.search(r"Figure\s+\d+", block)
        figure = {"page": page.relative_to(ROOT).as_posix(), "paper_url": spec["paper_url"],
                  "arxiv_id": aid, "figure": match.group() if match else "Original figure",
                  "original_caption": "", "source_url": source_url,
                  "extraction": "original_source_reviewed", "asset": asset.relative_to(ROOT).as_posix(),
                  "width": width, "height": height, "score": 0, "error": "",
                  "asset_sha256": hashlib.sha256(asset.read_bytes()).hexdigest()}
        figures = [old for old in figures if old["page"] != figure["page"]] + [figure]
    exclusions = load(AUDIT / "source-coverage.json")["sourceful_exclusions"]
    for exclusion in exclusions:
        if exclusion.get("arxiv_id"):
            candidates.append(exclusion | {"id": exclusion["arxiv_id"], "status": "rejected",
                              "resolution": "out_of_scope_this_selection", "review_decision": "out_of_scope",
                              "priority": "P2", "track": exclusion["track"], "review_done": True,
                              "automatic_retry": False, "automatic_implementation_queue": False})
    scope = intake | {"selected_scope_complete": True, "delivery_status": "fixed_scope_complete",
                       "counts": {"catalogued_papers": len(intake["accepted_papers"]),
                                  "low_cost_components": len(COMPONENTS), "cuda_components": len(CUDA_KEYS),
                                  "review_only_papers": len(intake["accepted_papers"]) - len(COMPONENTS),
                                  "authored_four_level_questions": 4 * len(intake["accepted_papers"]),
                                  "full_capability_reproductions": 0}, "papers": candidates}
    write(AUDIT / "task-scope.json", scope)
    write(ROOT / "docs/paper-figures-manifest.json", figures)
    ledger_path = ROOT / "docs/paper-discovery-ledger.json"
    ledger = load(ledger_path)
    ledger["batches"] = [row for row in ledger["batches"] if row.get("batch") != BATCH]
    ledger["batches"].append({k: v for k, v in scope.items() if k != "papers"} | {"candidates": candidates})
    write(ledger_path, ledger)
    print(json.dumps(scope["counts"], sort_keys=True))


if __name__ == "__main__":
    main()
