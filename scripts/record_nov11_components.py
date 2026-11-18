"""Record the fixed Nov 11 component cohort without advancing the review watermark."""
from __future__ import annotations

import argparse
from datetime import date, datetime
import hashlib
import json
from pathlib import Path
import re
from zoneinfo import ZoneInfo

from curate_nov04_components import aggregate_metrics, write_new
from curate_nov11_components import validate_raw
from run_nov11_components import AUDIT, BATCH, COMPONENTS, CUDA_KEYS, ROOT, SEEDS

DAY = "2026-11-11"
WATERMARK = ROOT / "docs/paper-discovery-watermark.json"
LEDGER = ROOT / "docs/paper-discovery-ledger.json"
REVIEW_FILES = ("priority-review.json", "post-training-review.json", "agent-review.json")
FOUNDATION_KEYS = {"adindex", "b3", "steprefine"}
REFERENCE = "alphaproof-code"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def specs() -> dict[str, dict]:
    result = {}
    for path in (ROOT / "src/auto_research/paper_specs/catalog").glob("*/*.json"):
        spec = load(path)
        if spec["key"] in {*COMPONENTS, REFERENCE}:
            if spec["key"] in result:
                raise ValueError("ambiguous selected catalog key")
            result[spec["key"]] = spec
    if set(result) != {*COMPONENTS, REFERENCE}:
        raise ValueError("expected sixteen components and one reference")
    return result


def primary_reviews() -> dict[str, dict]:
    """Normalize only evidence actually read by the bounded review owners."""
    result = {}
    priority = load(AUDIT / "priority-review.json")
    for row in priority["reviewed_papers"]:
        source = row.get("fixed_source", row.get("technical_report", {}))
        if not source:
            source = next(item for item in priority["source_receipts"]
                          if item.get("url") == row.get("paper_url"))
        result[row["key"]] = {
            "review_artifact": "research-audits/nov11-components/priority-review.json",
            "source_url": source["url"], "source_sha256": source["sha256"],
            "source_cache": source["capture"],
            "read_scope": row["source_review_scope"], "full_article_read": False,
        }
    for row in load(AUDIT / "post-training-review.json")["records"]:
        receipt = row["source_receipt"]
        result[row["key"].rsplit(":", 1)[-1]] = {
            "review_artifact": "research-audits/nov11-components/post-training-review.json",
            "source_url": row["original_url"], "source_sha256": receipt["sha256"],
            "source_cache": receipt["cache_path"], "read_scope": receipt["read_scope"],
            "full_article_read": False,
        }
    for row in load(AUDIT / "agent-review.json")["papers"]:
        if row.get("module_key") not in COMPONENTS:
            continue
        result[row["module_key"]] = {
            "review_artifact": "research-audits/nov11-components/agent-review.json",
            "source_url": row["source_url"], "source_sha256": row["source_sha256"],
            "source_cache": row["source_cache"], "read_scope": row["reviewed_sections"],
            "full_article_read": False,
        }
    for key in FOUNDATION_KEYS:
        path = ROOT / f".cache/nov11-components/foundation/{key}.html"
        spec = specs()[key]
        result[key] = {
            "review_artifact": spec["detail_path"],
            "source_url": spec["reviewed_version_url"], "source_sha256": digest(path),
            "source_cache": path.relative_to(ROOT).as_posix(),
            "read_scope": "original byline, defining method, equations and experimental configuration; "
                          "locations and cost limits are documented in the paper README and catalog spec",
            "full_article_read": False,
        }
    if set(result) != {*COMPONENTS, REFERENCE}:
        raise ValueError("selected papers lack original-source evidence")
    for row in result.values():
        if digest(ROOT / row["source_cache"]) != row["source_sha256"]:
            raise ValueError("original-source receipt changed")
    return result


def build_coverage() -> dict:
    state = load(WATERMARK)
    if state["review_watermark"] != "2026-11-09":
        raise ValueError("this bounded intake was authorized against the November 9 watermark")
    captures = []
    for path in sorted((ROOT / ".cache/nov11-components/ci").glob("*-paper-candidates/paper-*.json")):
        if "official-review" in path.name:
            continue
        row = load(path)
        transport = row["arxiv_transport"]
        captures.append({
            "artifact": path.relative_to(ROOT).as_posix(), "sha256": digest(path),
            "track": row["track"], "recall_mode": row["recall_mode"],
            "requested_window": row["requested_window"], "effective_window": row["window"],
            "candidate_count": len(row["candidates"]),
            **{key: transport[key] for key in (
                "coverage_complete", "transport_complete", "query_count", "capped_queries", "failed_queries",
            )},
            "incomplete_queries": [{key: query.get(key) for key in (
                "query", "categories", "date_from", "date_to", "identifier_months", "maximum_results",
                "next_offset", "state", "coverage_complete", "transport_complete", "error",
            )} for query in transport["queries"] if not query["coverage_complete"]],
            "all_returned_candidates_method_reviewed": False,
        })
    if len(captures) != 8 or {row["track"] for row in captures} != {
        "agent", "post-training", "foundation-model", "recommendation",
    }:
        raise ValueError("expected four tracks and two actual capture modes")
    priority = load(AUDIT / "priority-review.json")
    post = load(AUDIT / "post-training-review.json")
    agent = load(AUDIT / "agent-review.json")
    return {
        "schema_version": 1, "batch": BATCH, "checked_on": DAY,
        "scope_kind": "bounded-component-intake", "all_sources_exhaustive": False,
        "full_window_review_complete": False, "new_announcement_date_verified_for_all": False,
        "review_watermark_advanced": False,
        "review_watermark": {"before": state["review_watermark"], "after": state["review_watermark"]},
        "watermark_artifact": "paper-discovery-watermark.json", "watermark_sha256": digest(WATERMARK),
        "date_policy": "Use exact original published_at converted to Asia/Shanghai against November 9. "
                       "Discovery, announcement and identifier month are not first-publication dates. "
                       "AlphaProof Code has official day precision only and no fabricated arXiv identity.",
        "ci_capture_receipts": captures,
        "ci_transport_complete": all(row["transport_complete"] for row in captures),
        "ci_recall_coverage_complete": all(row["coverage_complete"] for row in captures),
        "capped_queries": sum(row["capped_queries"] for row in captures),
        "review_artifacts": [{"path": path, "sha256": digest(AUDIT / path)} for path in REVIEW_FILES],
        "official_coverage": priority["official_coverage"],
        "official_source_receipts": priority["source_receipts"],
        "supplemental_keyword_search": post["search_receipts"],
        "bounded_unreviewed_leads": post["unselected_additional_leads"],
        "other_recorded_dispositions": {
            "priority": priority["excluded_or_duplicate"],
            "agent": [row for row in agent["papers"] if row.get("module_key") not in COMPONENTS],
        },
        "limitations": [
            "Fixed seventeen-paper delivery, not a window-wide or historical method audit.",
            "The foundation late-index LLM query is capped at 2000; transport success does not prove recall exhaustion.",
            "The supplemental post-training Atom search returned the first 100 of 111 keyword results only.",
            "Google first/last pages and selected details were checked; count 462 versus 450 is not twelve new papers.",
            "Meta publication directory returned an unavailable-content response. An unchanged curated home page is not a census.",
            "Unreviewed leads are neither accepted implementation work nor high-cost DONE decisions.",
            "Sixteen L1 synthetic mechanism checks and four real A100 checks are not full-paper capability or Evolve evidence.",
        ],
    }


def validate_evidence(specifications: dict[str, dict]) -> dict:
    from auto_research.gpu_validation import load_gpu_receipt

    frozen = load(AUDIT / "frozen-sources.json")
    runs = {device: load(AUDIT / f"raw-{device}.json") for device in ("cpu", "cuda")}
    for device, raw in runs.items():
        validate_raw(raw, device, frozen)
    for key in COMPONENTS:
        spec = specifications[key]
        device = "cuda" if key in CUDA_KEYS else "cpu"
        metric_path = ROOT / "docs" / Path(spec["detail_path"]).parent / f"metrics/component-{device}-seeds42-44.json"
        metric = load(metric_path)
        raw = runs[device]
        expected_metrics = aggregate_metrics(raw["components"][key]["per_seed"])
        if (metric.get("method") != key or metric.get("metrics") != expected_metrics
                or metric.get("per_seed") != raw["components"][key]["per_seed"]
                or metric.get("seeds") != SEEDS or metric.get("diagnostic_only") is not True
                or metric.get("evaluation_tier") != "l1_mechanism"
                or metric.get("formal_comparison") is not False
                or metric.get("promotion_eligible") is not False or metric.get("evolve_integrated") is not False
                or metric["provenance"].get("commit") != frozen["commit"]
                or metric["provenance"].get("executed_source_sha256") != frozen["source_sha256"]
                or metric["provenance"].get("raw_runner_artifact_sha256") != digest(AUDIT / f"raw-{device}.json")
                or metric["provenance"].get("accelerator") != raw["accelerator"]):
            raise ValueError(f"{key}: final metric differs from frozen actual execution")
        if key in CUDA_KEYS:
            receipt = load_gpu_receipt(ROOT / spec["gpu_validation_artifact"])
            if (not spec["gpu_validation_passed"] or receipt["adapter_key"] != key
                    or receipt["seeds"] != SEEDS or receipt["metrics"] != expected_metrics
                    or receipt["provenance"]["commit"] != frozen["commit"]
                    or receipt["provenance"]["metric_artifact_path"] != metric_path.relative_to(ROOT).as_posix()):
                raise ValueError(f"{key}: GPU receipt is not the accepted execution")
        elif spec["requires_gpu_validation"] or spec.get("gpu_validation_artifact"):
            raise ValueError(f"{key}: CPU-only component must not claim a GPU receipt")
    alpha = specifications[REFERENCE]
    if (alpha["implementation_status"] != "deferred_high_cost" or alpha.get("local_operator")
            or alpha.get("adapter") is not None or alpha["requires_gpu_validation"]):
        raise ValueError("AlphaProof is a review-only reference, not a local verifier")
    return frozen


def selected_rows(specifications: dict[str, dict], reviews: dict[str, dict]) -> list[dict]:
    rows = []
    for key in (*COMPONENTS, REFERENCE):
        spec = specifications[key]
        if (not spec["review_done"] or not spec["full_experiment_review_done"]
                or spec["full_experiment_status"] != "not_reproduced_high_cost"
                or any(spec[flag] is not False for flag in (
                    "promotion_eligible", "evolve_integrated", "automatic_retry", "automatic_implementation_queue",
                ))):
            raise ValueError(f"{key}: selected paper lacks a closed cost/evidence boundary")
        is_component = key in COMPONENTS
        timestamp = spec.get("published_at")
        local_day = (datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                     .astimezone(ZoneInfo("Asia/Shanghai")).date() if timestamp else date.fromisoformat(spec["published"]))
        match = re.search(r"(\d{4}\.\d{4,5})(?:v\d+)?$", spec["paper_url"])
        identity = match.group(1) if match else "official:google-deepmind:alphaproof-code"
        row = {
            **{field: spec[field] for field in (
                "domain", "key", "title", "paper_url", "detail_path", "published", "first_author",
                "first_author_affiliation", "priority", "implementation_status", "cost_assessment",
                "requires_gpu_validation", "gpu_validation_passed", "full_experiment_status",
                "full_experiment_review_done", "promotion_eligible", "evolve_integrated", "automatic_retry",
                "automatic_implementation_queue", "review_done",
            )},
            "id": identity, "doc": spec["detail_path"], "catalog_key": key,
            "catalog_detail": spec["detail_path"], "published_at": timestamp,
            "publication_date_precision": "timestamp" if timestamp else "day",
            "first_publication_shanghai_day": local_day.isoformat(),
            "intake_class": "new_first_publication_since_watermark" if local_day > date(2026, 11, 9)
                            else "historical_or_overlap_backfill",
            "announced_on": spec.get("announced_on"),
            "announcement_date_not_inferred_from_identifier_or_discovery": True,
            "track": {"foundation-models": "foundation-model", "agent-research": "agent",
                      "multimodal-models": "multimodal"}.get(spec["domain"], spec["domain"]),
            "included_in_selected_scope": True, "status": "implemented" if is_component else "deferred",
            "resolution": "bounded_l1_component_accepted" if is_component else "not_reproduced_high_cost",
            "component_implemented": is_component, "component_accepted": is_component,
            "evaluation_tier": "l1_mechanism" if is_component else "reference_only",
            "diagnostic_only": is_component,
            "source_provenance": [reviews[key]],
        }
        if is_component:
            device = "cuda" if key in CUDA_KEYS else "cpu"
            row["component_evidence"] = (Path("docs") / Path(spec["detail_path"]).parent
                                         / f"metrics/component-{device}-seeds42-44.json").as_posix()
            if key in CUDA_KEYS:
                row["gpu_validation_artifact"] = spec["gpu_validation_artifact"]
        else:
            row["reason"] = spec["deferral_reason"]
            row["local_code"] = "无本地复现；仅成本审查文档 / no local reproduction; cost-review documentation only"
        rows.append(row)
    return rows


def record(check_only: bool = False) -> None:
    watermark_before = WATERMARK.read_bytes()
    specifications = specs()
    frozen = validate_evidence(specifications)
    reviews = primary_reviews()
    coverage = build_coverage()
    rows = selected_rows(specifications, reviews)
    excluded = next(row for row in load(AUDIT / "priority-review.json")["excluded_or_duplicate"]
                    if row.get("id") == "2611.13539")
    rejected = {
        "id": excluded["id"], "key": "feature-invariant-scaling-laws", "track": "recommendation",
        "title": excluded["title"], "priority": "P0", "status": "rejected",
        "resolution": excluded["decision"], "reason": excluded["reason"],
        "published_at": excluded["first_release_utc"], "included_in_selected_scope": False,
        "verified_priority_organizations": ["Meta"], "review_done": True,
        "component_implemented": False, "component_accepted": False,
        "automatic_retry": False, "automatic_implementation_queue": False,
        "source_provenance": [excluded["source"]],
        "source_review_scope": excluded["source_review_scope"],
    }
    common = {
        "schema_version": 1, "batch": BATCH, "date": DAY, "scope_kind": "bounded-component-intake",
        "all_sources_exhaustive": False, "full_window_review_complete": False,
        "review_watermark_advanced": False, "review_watermark": coverage["review_watermark"],
        "selected_scope_complete": True, "delivery_status": "bounded_scope_complete",
        "source_artifact": "research-audits/nov11-components/README.md",
        "counts": {
            "selected_papers": 17, "reviewed_candidates": 18, "component_implementations": 16,
            "cuda_validated_components": 4, "cpu_only_components": 12, "high_cost_reference_only": 1,
            "high_cost_full_experiments_not_reproduced": 17, "full_capability_reproductions": 0,
            "industrial_rejected_for_missing_online_evidence": 1,
            "first_publications_since_watermark": sum(row["intake_class"] == "new_first_publication_since_watermark"
                                                      for row in rows),
            "historical_or_overlap_backfills": sum(row["intake_class"] == "historical_or_overlap_backfill"
                                                  for row in rows),
        },
        "execution_commit": frozen["commit"],
        "execution_artifacts": {name: {"path": f"research-audits/nov11-components/{name}.json",
                                       "sha256": digest(AUDIT / f"{name}.json")}
                                for name in ("preflight", "frozen-sources", "raw-cpu", "raw-cuda")},
    }
    coverage_blob = json.dumps(coverage, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    common["source_coverage_sha256"] = hashlib.sha256(coverage_blob.encode()).hexdigest()
    ledger = load(LEDGER)
    batch = common | {"candidates": [*rows, rejected]}
    scope = common | {"papers": rows, "excluded_related_reviews": [rejected],
                      "bounded_unreviewed_leads": coverage["bounded_unreviewed_leads"]}
    matches = [item for item in ledger["batches"] if item["batch"] == BATCH]
    if check_only:
        if (matches != [batch] or load(AUDIT / "task-scope.json") != scope
                or (AUDIT / "source-coverage.json").read_text() != coverage_blob):
            raise ValueError("recorded bounded scope differs from source and execution evidence")
    else:
        if matches or any((AUDIT / filename).exists() for filename in ("task-scope.json", "source-coverage.json")):
            raise ValueError("batch already recorded; use --check, do not overwrite accepted evidence")
        for filename, payload in (("source-coverage.json", coverage), ("task-scope.json", scope)):
            write_new(AUDIT / filename, payload)
        ledger["batches"].append(batch)
        LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    if WATERMARK.read_bytes() != watermark_before:
        raise ValueError("bounded component delivery must not modify the review watermark")
    print("verified" if check_only else "recorded", "17 selected: 16 L1 components + 1 review-only; "
          "Meta offline-only paper rejected separately; review watermark remains 2026-11-09")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify the already-recorded immutable batch")
    record(parser.parse_args().check)
