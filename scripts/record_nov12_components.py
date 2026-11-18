"""Record a bounded overlap cohort; portable checks do not reread web caches."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

from curate_nov04_components import aggregate_metrics, write_new
from curate_nov12_components import validate_raw
from run_nov12_components import AUDIT, BATCH, COMPONENTS, CUDA_KEYS, ROOT, SEEDS

LEDGER = ROOT / "docs/paper-discovery-ledger.json"
WATERMARK = ROOT / "docs/paper-discovery-watermark.json"
REVIEW_FILES = ("agent-review.json", "post-training-review.json", "foundation-review.json")
THEORY = "apmd-reference-reset"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def specifications():
    result = {}
    for path in (ROOT / "src/auto_research/paper_specs/catalog").glob("*/*.json"):
        spec = load(path)
        if spec["key"] in COMPONENTS:
            if spec["key"] in result:
                raise ValueError("ambiguous selected catalog key")
            result[spec["key"]] = spec
    if set(result) != set(COMPONENTS):
        raise ValueError("exactly eight fixed component specifications required")
    return result


def verify_captures(receipts):
    """Strict original-byte recheck, required for admission and opt-in thereafter."""
    for receipt in receipts:
        path = ROOT / receipt["capture"]
        if not path.is_file() or digest(path) != receipt["sha256"]:
            raise ValueError(f"original capture missing/changed: {receipt['capture']}; "
                             "a fresh clone can use --check without --recheck-source-captures")


def validate_sources(specs, *, reread_captures):
    coverage = load(AUDIT / "source-coverage.json")
    announcement = load(AUDIT / "announcement-index.json")
    primary = load(AUDIT / "primary-source-receipts.json")
    if (coverage["batch"] != BATCH or coverage["all_sources_exhaustive"] is not False
            or coverage["full_window_review_complete"] is not False
            or coverage["review_watermark_advanced"] is not False
            or coverage["review_watermark"] != {"before": "2026-11-09", "after": "2026-11-09"}
            or coverage["announcement_date"] != "2026-11-11"
            or announcement["announcement_date"] != "2026-11-11"
            or announcement["is_new_announcement_relative_to_prior_batch"] is not False
            or announcement["all_candidates_method_reviewed"] is not False
            or announcement["automatic_implementation_queue"] is not False
            or set(primary["papers"]) != set(COMPONENTS)):
        raise ValueError("bounded source scope was promoted or identities changed")
    all_captures = list(coverage["capture_receipts"])
    for key, row in primary["papers"].items():
        if (row["reviewed_version_url"] != specs[key]["reviewed_version_url"]
                or row["whole_paper_verified"] is not False
                or not row["reviewed_sections"] or len(row["captures"]) < 1):
            raise ValueError(f"defining-method primary review receipt differs: {key}")
        all_captures.extend(row["captures"])
    for row in all_captures:
        if (not isinstance(row.get("source_url"), str) or not row["source_url"].startswith("https://")
                or not re.fullmatch(r"[0-9a-f]{64}", row.get("sha256", ""))
                or not row["capture"].startswith(".cache/nov12-components/")):
            raise ValueError("identified source URL, exact byte hash and scoped capture required")
    if reread_captures:
        verify_captures(all_captures)
    return coverage


def validate_execution(specs):
    from auto_research.gpu_validation import load_gpu_receipt

    frozen = load(AUDIT / "frozen-sources.json")
    raw = {device: load(AUDIT / f"raw-{device}.json") for device in ("cpu", "cuda")}
    for device, result in raw.items():
        validate_raw(result, device, frozen)
    for key, spec in specs.items():
        device = "cuda" if key in CUDA_KEYS else "cpu"
        expected_status = "not_applicable_theory_only" if key == THEORY else "not_reproduced_high_cost"
        if (spec["domain"] != COMPONENTS[key][0] or spec["implementation_status"] != "component_only"
                or spec["requires_gpu_validation"] is not (device == "cuda")
                or spec["gpu_validation_passed"] is not (device == "cuda")
                or spec["full_experiment_status"] != expected_status
                or spec["full_experiment_review_done"] is not True or spec["review_done"] is not True
                or spec["promotion_eligible"] is not False or spec["evolve_integrated"] is not False
                or spec["automatic_retry"] is not False or spec["automatic_implementation_queue"] is not False):
            raise ValueError(f"implementation/cost/eligibility boundary differs: {key}")
        artifact = Path("docs") / Path(spec["detail_path"]).parent / f"metrics/component-{device}-seeds42-44.json"
        metric = load(ROOT / artifact)
        rows = raw[device]["components"][key]["per_seed"]
        if (metric["method"] != key or metric["per_seed"] != rows
                or metric["metrics"] != aggregate_metrics(rows) or metric["seeds"] != SEEDS
                or metric["provenance"]["commit"] != frozen["commit"]
                or metric["provenance"]["executed_source_sha256"] != frozen["source_sha256"]
                or metric["provenance"]["raw_runner_artifact_sha256"] != digest(AUDIT / f"raw-{device}.json")
                or metric["full_experiment_status"] != expected_status
                or metric["diagnostic_only"] is not True or metric["formal_comparison"] is not False
                or metric["promotion_eligible"] is not False or metric["evolve_integrated"] is not False):
            raise ValueError(f"accepted metric differs from actual frozen run: {key}")
        if device == "cuda":
            receipt = load_gpu_receipt(ROOT / spec["gpu_validation_artifact"])
            if (receipt["adapter_key"] != key or receipt["seeds"] != SEEDS
                    or receipt["metrics"] != metric["metrics"]
                    or receipt["provenance"]["commit"] != frozen["commit"]
                    or receipt["provenance"]["metric_artifact_path"] != artifact.as_posix()):
                raise ValueError(f"actual A100 receipt differs: {key}")
    return frozen


def record(*, check_only=False, recheck_source_captures=False):
    before = WATERMARK.read_bytes()
    if load(WATERMARK)["review_watermark"] != "2026-11-09":
        raise ValueError("this cohort does not advance the November 9 watermark")
    specs = specifications()
    validate_sources(specs, reread_captures=not check_only or recheck_source_captures)
    frozen = validate_execution(specs)
    papers = []
    for key in COMPONENTS:
        spec = specs[key]
        identity = re.search(r"\d{4}\.\d{4,5}", spec["paper_url"])[0]
        device = "cuda" if key in CUDA_KEYS else "cpu"
        artifact = Path("docs") / Path(spec["detail_path"]).parent / f"metrics/component-{device}-seeds42-44.json"
        papers.append({
            **{field: spec[field] for field in (
                "domain", "key", "title", "paper_url", "detail_path", "published", "published_at",
                "reviewed_version_url", "first_author", "first_author_affiliation", "priority",
                "implementation_status", "full_experiment_status", "full_experiment_review_done",
                "requires_gpu_validation", "gpu_validation_passed", "cost_assessment",
            )},
            "id": identity, "doc": spec["detail_path"], "catalog_key": key,
            "track": {"foundation-models": "foundation-model"}.get(spec["domain"], spec["domain"]),
            "status": "implemented", "resolution": "bounded_l1_component_accepted",
            "review_done": True, "component_implemented": True, "component_accepted": True,
            "component_evidence": artifact.as_posix(), "full_capability_reproduced": False,
            "promotion_eligible": False, "evolve_integrated": False,
            "automatic_retry": False, "automatic_implementation_queue": False,
            "intake_class": "official_source_historical_backfill" if key in {"bats", "agent-gym"}
            else "same_announcement_carryover", "new_first_publication_since_prior_delivery": False,
        })
    exception = load(AUDIT / "industrial-source-exception.json")
    if (exception["resolution"] != "archived_unconfirmed_not_blocking"
            or exception["accepted"] is not False or exception["implemented"] is not False
            or exception["blocks_watermark"] is not False):
        raise ValueError("unconfirmed industrial timeline cannot be promoted to accepted evidence")
    artifacts = ["source-coverage.json", "announcement-index.json", "primary-source-receipts.json",
                 "industrial-source-exception.json", "preflight.json", "frozen-sources.json",
                 "raw-cpu.json", "raw-cuda.json", *REVIEW_FILES]
    common = {
        "schema_version": 1, "batch": BATCH, "date": "2026-11-12",
        "scope_kind": "bounded-component-intake", "all_sources_exhaustive": False,
        "full_window_review_complete": False, "review_watermark_advanced": False,
        "review_watermark": {"before": "2026-11-09", "after": "2026-11-09"},
        "selected_scope_complete": True, "delivery_status": "bounded_scope_complete",
        "source_artifact": "research-audits/nov12-components/README.md",
        "execution_commit": frozen["commit"],
        "counts": {"selected_papers": 8, "reviewed_candidates": 9, "component_implementations": 8,
                   "cuda_validated_components": 3, "cpu_only_components": 5,
                   "full_capability_reproductions": 0, "new_first_publications_since_prior_delivery": 0,
                   "same_announcement_carryovers": 6, "official_source_historical_backfills": 2,
                   "high_cost_full_experiments_not_reproduced": 7, "theory_only_no_large_empirical_protocol": 1,
                   "archived_protocol_conflicts": 1},
        "artifacts": [{"path": "research-audits/nov12-components/" + name,
                       "sha256": digest(AUDIT / name)} for name in artifacts],
    }
    scope = common | {"papers": papers, "exceptions": [exception]}
    batch = common | {"candidates": [*papers, exception]}
    ledger = load(LEDGER)
    existing = [row for row in ledger["batches"] if row["batch"] == BATCH]
    if check_only:
        if existing != [batch] or load(AUDIT / "task-scope.json") != scope:
            raise ValueError("committed scope/ledger differs from source receipts and measured execution")
    else:
        if existing or (AUDIT / "task-scope.json").exists():
            raise ValueError("accepted batch is immutable; use --check")
        write_new(AUDIT / "task-scope.json", scope)
        ledger["batches"].append(batch)
        LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n")
    if WATERMARK.read_bytes() != before:
        raise ValueError("bounded intake must not mutate the global review watermark")
    print("verified eight L1 components, three actual A100 receipts; "
          + ("original captures rechecked" if not check_only or recheck_source_captures
             else "committed evidence checked; original source bytes not reread"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--recheck-source-captures", action="store_true")
    args = parser.parse_args()
    if args.recheck_source_captures and not args.check:
        parser.error("--recheck-source-captures is an opt-in extension of --check")
    record(check_only=args.check, recheck_source_captures=args.recheck_source_captures)
