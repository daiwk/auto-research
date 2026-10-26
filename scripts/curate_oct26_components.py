"""Bind Oct26 bounded source review to exact frozen CPU/A100 component evidence.

This closes only the fixed selected scope, never a whole announcement window.
High-cost reference entries have no operator or fabricated experiment metrics.
"""
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
sys.path.insert(0, str(ROOT / "scripts"))
from auto_research.gpu_validation import load_gpu_receipt  # noqa: E402
from auto_research.paper_specs.catalog import catalog_records  # noqa: E402
from build_oct23_source_audit import CATEGORIES, directory_deltas, identity, timestamp  # noqa: E402
from curate_oct21_component_evidence import aggregate, digest, require, write  # noqa: E402
from oct18_frozen_sources import capture_sources, verify_sources  # noqa: E402
from run_google_emnlp25_components import validate_row  # noqa: E402
from run_oct26_components import execution_spec, sources, SEEDS, RUNNER  # noqa: E402

BATCH = "2026-10-26-priority-components"
AUDIT_REL = Path("docs/research-audits/oct26-components")
AUDIT = ROOT / AUDIT_REL
COMPONENT_KEYS = {"hge", "detector-scope", "opst", "frontier-opd", "mart-grpo", "dt-jepa", "editjev", "uniaction"}
REFERENCE_KEYS = {"watch-and-learn", "paperorchestra", "lazyflash", "pathjev", "flexglue", "image-rsi", "rsi-opt", "harnessmm"}


def catalogue():
    return {r["key"]: r for r in catalog_records()}


def validate_capture(rows):
    pages = [r for r in rows if r["kind"] == "arxiv"]
    require(len(pages) == 8 and {p["source"] for p in pages} == CATEGORIES, "eight distinct categories")
    for page in pages:
        require(page.get("status") == "retrieved" and page.get("announced_on") == "2026-10-26"
                and page.get("parse_complete") is True, "complete actual Oct26 bulletin required")
        records = page["records"]
        require(page["expected_entries"] == page["parsed_entries"] == len(records), "entry totals")
        require(len({r["id"] for r in records}) == len(records), "duplicate version in category")
        sections = page["sections"]
        require(len(sections) == 3 and {s["kind"] for s in sections} == {"new", "cross-list", "replacement"}, "three sections")
        counts = Counter(r["entry_kind"] for r in records)
        require(all(s["shown"] == s["expected"] == counts[s["kind"]] for s in sections), "section accounting")
        timestamp(page["checked_at"])
        require(len(page["sha256"]) == 64, "source digest")
        for row in records:
            identity(row["id"])
    return pages


def validate_catalog(catalog, specs):
    require(set(specs) == COMPONENT_KEYS, "fixed eight component set")
    for key in COMPONENT_KEYS | REFERENCE_KEYS:
        item = catalog[key]
        require(item.get("adapter") is None and item.get("full_experiment_status") == "not_reproduced_high_cost"
                and item.get("full_experiment_review_done") is True and item.get("review_done") is True
                and item.get("automatic_retry") is False and item.get("automatic_implementation_queue") is False
                and item.get("promotion_eligible") is False and item.get("evolve_integrated") is False
                and item.get("cost_assessment") and item.get("priority") in {"P0", "P1"}, f"{key}: cost/claim boundary")
        page = Path(item["detail_path"])
        require(not page.is_absolute() and ".." not in page.parts and page.name == "README.md", "safe document path")
        if key in COMPONENT_KEYS:
            expected_module = specs[key]["source"].removeprefix("src/").removesuffix(".py").replace("/", ".")
            require(item.get("implementation_status") == "component_only" and item.get("diagnostic_only") is True
                    and item.get("evaluation_tier") == "l1_mechanism" and item.get("requires_gpu_validation") is True
                    and item.get("gpu_validation_passed") is True
                    and item.get("gpu_validation_artifact") == f"docs/gpu-validations/{key}-a100-20261026.json"
                    and item.get("local_operator", "").startswith(expected_module + ".")
                    and item.get("local_command") == f"PYTHONPATH=src python -c 'from {expected_module} import diagnostic; print(diagnostic(42))'",
                    f"{key}: executed operator and diagnostic boundary")
        else:
            require(item.get("implementation_status") == "deferred_high_cost" and item.get("requires_gpu_validation") is False
                    and item.get("gpu_validation_passed") is False and not item.get("local_operator")
                    and not item.get("local_command") and not item.get("gpu_validation_artifact"), f"{key}: reference-only boundary")


def metric_path(key, catalog):
    return Path("docs") / Path(catalog[key]["detail_path"]).parent / "metrics/component-cuda-seeds42-44.json"


def validate_raw(raw, spec):
    require(set(raw) == {"cpu", "cuda"}, "both CPU and CUDA actual runs required")
    expected = {r["key"]: r for r in spec["components"]}
    for device, result in raw.items():
        require(result.get("schema_version") == 2 and result.get("device") == device and result.get("seeds") == SEEDS
                and set(result.get("components", {})) == COMPONENT_KEYS
                and result.get("evaluation_tier") == "l1_mechanism" and result.get("diagnostic_only") is True
                and result.get("formal_comparison") is False and result.get("promotion_eligible") is False
                and result.get("evolve_integrated") is False and result.get("pretrained_model_calls") == 0
                and result.get("full_experiments_executed") is False, "raw execution/claim schema")
        require(result["accelerator"] == "CPU" if device == "cpu"
                else any(n in result["accelerator"] for n in ("A100", "A30")), "actual accelerator")
        require(set(result["source_sha256"]) == set(sources(spec)), "complete frozen source scope")
        for key, entry in result["components"].items():
            rows = entry["per_seed"]
            require([r["seed"] for r in rows] == SEEDS, "exact three seeds")
            for seed, row in zip(SEEDS, rows):
                require(row.get("execution_device") == device and row.get("execution_accelerator") == result["accelerator"],
                        "per-seed execution device binding")
                validate_row(row, expected[key], seed)
            aggregate(rows)
    require(raw["cpu"]["code_commit"] == raw["cuda"]["code_commit"]
            and raw["cpu"]["source_sha256"] == raw["cuda"]["source_sha256"], "CPU/CUDA frozen identity")


def result_for(key, raw, raw_bytes, catalog):
    source = raw["cuda"]
    dataset = {"id": f"synthetic:oct26-{key}-v1", "revision": "sha256:" + digest(source["source_sha256"]),
               "recipe": "fixed-seeded-component-contracts", "capability_benchmark": False}
    return {"schema_version": 2, "method": key, "manifest_ref": catalog[key]["domain"] + ":" + key,
            "dataset": dataset, "seeds": SEEDS, "per_seed": source["components"][key]["per_seed"],
            "metrics": aggregate(source["components"][key]["per_seed"]), "evaluation_tier": "l1_mechanism",
            "evaluation_protocol": {"tier": "l1_mechanism", "seeds": SEEDS, "formal_comparison": False,
                                    "claim_policy": "L1 mechanism contracts, not pretrained capability or full paper reproduction"},
            "diagnostic_only": True, "fixture_demo": True, "formal_comparison": False, "promotion_eligible": False,
            "evolve_integrated": False, "pretrained_model_calls": 0, "full_experiment_status": "not_reproduced_high_cost",
            "full_experiment_review_done": True, "provenance": {"commit": source["code_commit"],
                "artifact_path": metric_path(key, catalog).as_posix(), "accelerator": source["accelerator"],
                "executed_source_sha256": source["source_sha256"],
                "raw_runner_artifact_sha256": hashlib.sha256(raw_bytes["cuda"]).hexdigest(),
                "dataset_fingerprint": "sha256:" + digest({"dataset": dataset, "seeds": SEEDS, "source": source["source_sha256"]})}}


def receipt_for(key, result, catalog):
    p = result["provenance"]
    return {"schema_version": 1, "adapter_key": key, "validated_at": "2026-10-26",
            "accelerator": {"vendor": "NVIDIA", "model": p["accelerator"], "count": 1},
            "command": ["python3", RUNNER, "--device", "cuda", "--source-commit", p["commit"],
                        "--frozen-proof", "oct26-frozen-proof.json", "--output", "results/components-cuda.json"],
            "dataset": result["dataset"], "checkpoint": {"public_id": "none-seeded-component-initialization",
                "revision": p["commit"], "pretrained": False}, "seeds": SEEDS, "result": "passed",
            "metrics": result["metrics"], "executed_source_sha256": p["executed_source_sha256"],
            "provenance": {**p, "artifact_path": catalog[key]["gpu_validation_artifact"],
                           "metric_artifact_path": metric_path(key, catalog).as_posix()},
            "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
            "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True}


def ingest(cpu, cuda):
    catalog, spec = catalogue(), execution_spec()
    validate_catalog(catalog, {r["key"]: r for r in spec["components"]})
    raw_bytes = {"cpu": cpu.read_bytes(), "cuda": cuda.read_bytes()}
    raw = {d: json.loads(b) for d, b in raw_bytes.items()}
    validate_raw(raw, spec)
    proof = capture_sources(ROOT, raw["cpu"]["code_commit"], sources(spec))
    verify_sources(ROOT, raw["cpu"]["code_commit"], raw["cpu"]["source_sha256"], proof)
    for key in COMPONENT_KEYS:
        result = result_for(key, raw, raw_bytes, catalog)
        write(ROOT / metric_path(key, catalog), result)
        write(ROOT / catalog[key]["gpu_validation_artifact"], receipt_for(key, result, catalog))
    write(AUDIT / "frozen-sources.json", {"schema_version": 1, "commit": raw["cpu"]["code_commit"], "proof": proof})
    for device, blob in raw_bytes.items():
        (AUDIT / f"raw-{device}.json").write_bytes(blob)


def build_review(directory, *, extend_refs=False):
    ledger_path = ROOT / "docs/paper-discovery-ledger.json"
    ledger = json.loads(ledger_path.read_text())
    existing = [b for b in ledger["batches"] if b["batch"] == BATCH]
    if extend_refs:
        require(len(existing) == 1, "one existing bounded batch required for explicit reference-only expansion")
        prior_scope = json.loads((AUDIT / "task-scope.json").read_text())
        prior_coverage = json.loads((AUDIT / "source-coverage.json").read_text())
        require(prior_scope["selected_scope_complete"] is True and prior_scope["fixed_component_keys"] == sorted(COMPONENT_KEYS)
                and set(prior_scope["reference_only_keys"]) == REFERENCE_KEYS - {"image-rsi", "rsi-opt", "harnessmm"},
                "only three newly accepted high-cost references may extend the scope")
    else:
        require(not existing, "batch already exists; refuse accepted-state overwrite")
    raw_bytes = (directory / "retrieval.json").read_bytes()
    receipts = json.loads(raw_bytes)
    if extend_refs:
        require(prior_coverage["raw_capture_sha256"] == hashlib.sha256(raw_bytes).hexdigest(), "reference expansion cannot replace source capture")
    pages = validate_capture(receipts)
    baseline = json.loads((ROOT / "docs/research-audits/oct25-priority-components/source-coverage.json").read_text())
    supplied = [json.loads((directory / f"{name}-delta.json").read_text()) for name in ("google", "meta", "google-deepmind")]
    deltas = directory_deltas(receipts, supplied)
    catalogue_rows = catalogue()
    observed = {}
    for page in pages:
        for entry in page["records"]:
            item = observed.setdefault(identity(entry["id"]), {"versions": set(), "categories": set(), "kinds": set()})
            item["versions"].add(entry["id"])
            item["categories"].add(page["source"])
            item["kinds"].add(entry["entry_kind"])
    previous = max(r["checked_at"] for r in baseline["retrieval_receipts"])
    reviewed = []
    for key in sorted(COMPONENT_KEYS | REFERENCE_KEYS):
        item = catalogue_rows[key]
        paper_id = item["paper_url"].split("/")[-1].split("v")[0]
        seen = observed.get(paper_id, {"versions": [], "categories": [], "kinds": []})
        component = key in COMPONENT_KEYS
        decision = "component_only" if component else "not_reproduced_high_cost"
        reviewed.append({"id": paper_id, "key": key, "domain": item["domain"], "title": item["title"],
            "priority": item["priority"], "paper_url": item["paper_url"], "detail_path": item["detail_path"],
            "first_author": item["first_author"], "first_author_affiliation": item["first_author_affiliation"],
            "original_published_at": item["published_at"], "decision": decision,
            "intake_class": "historical-directory-backfill" if key in {"watch-and-learn", "paperorchestra"}
                else "recent-source-release-backfill" if key == "detector-scope" else "new-announcement-selected",
            "first_publication_after_baseline_capture": timestamp(item["published_at"]) > timestamp(previous),
            "observed_versions": sorted(seen["versions"]), "bulletin_categories": sorted(seen["categories"]),
            "bulletin_entry_kinds": sorted(seen["kinds"]), "status": "implemented" if component else "deferred",
            "implementation_status": item["implementation_status"], "component_implemented": component,
            "component_accepted": component, "review_done": True, "full_experiment_review_done": True,
            "full_experiment_status": "not_reproduced_high_cost", "cost_assessment": item["cost_assessment"],
            "requires_gpu_validation": component, "gpu_validation_passed": component,
            "automatic_retry": False, "automatic_implementation_queue": False, "promotion_eligible": False,
            "evolve_integrated": False, "resolution": "bounded_l1_component_accepted" if component else "not_reproduced_high_cost",
            "component_evidence": metric_path(key, catalogue_rows).as_posix() if component else None,
            "reason": "限定组件三种子CPU/真实A100已验收；完整高成本实验不复现、审查DONE，不声称能力或全窗口穷尽。"
                if component else "完整实验成本过高，不复现（审查 DONE）；仅参考资料，无执行入口或自动重试。"})
    # Review is written only AFTER the exact actual runs are accepted.
    check_evidence()
    if extend_refs:
        current = {r["key"]: r for r in reviewed}
        require(all(current[r["key"]] == r for r in prior_scope["papers"]), "existing accepted review entries must remain byte-equivalent in meaning")
    prior_ids = {identity(v) for values in baseline["bulletin_ids_by_category"].values() for v in values}
    new_versions = {e["id"] for p in pages for e in p["records"]}
    old_versions = {v for values in baseline["bulletin_ids_by_category"].values() for v in values}
    counts = {"selected_papers": len(reviewed), "components_accepted": len(COMPONENT_KEYS),
              "components_pending_verification": 0, "gpu_validated_components": len(COMPONENT_KEYS),
              "reference_only_high_cost_done": len(REFERENCE_KEYS), "capability_reproductions_claimed": 0,
              "category_entries_including_crosslists_and_replacements": sum(len(p["records"]) for p in pages),
              "unique_bulletin_identities": len(observed),
              "snapshot_added_base_identities_not_new_paper_count": len(set(observed) - prior_ids),
              "snapshot_added_version_strings_not_revision_count": len(new_versions - old_versions),
              "section_entry_counts": dict(Counter(e["entry_kind"] for p in pages for e in p["records"])),
              "selected_first_publications_after_previous_capture": sum(r["first_publication_after_baseline_capture"] for r in reviewed)}
    common = {"schema_version": 1, "batch": BATCH, "delivery_status": "bounded_scope_complete",
              "selected_scope_complete": True, "all_sources_exhaustive": False, "review_watermark_advanced": False,
              "review_watermark": {"before": "2026-10-15", "after": "2026-10-15"}, "counts": counts}
    coverage = {**common, "checked_on": "2026-10-26", "scope_kind": "bounded-announcement-and-priority-source-components",
                "actual_announced_on": "2026-10-26", "new_announcement_batch_available": True,
                "raw_capture_sha256": hashlib.sha256(raw_bytes).hexdigest(),
                "baseline": "../oct25-priority-components/source-coverage.json", "baseline_last_checked_at": previous,
                "all_eight_bulletins_complete": True, "full_bulletin_full_text_review_complete": False,
                "bulletin_ids_by_category": {p["source"]: [r["id"] for r in p["records"]] for p in pages},
                "retrieval_receipts": [{k: v for k, v in p.items() if k != "records"} for p in receipts],
                "official_directory_deltas": deltas,
                "limitations": ["Oct26 announcement identities include weekend submissions and old replacements; snapshot additions are not a new-paper count.",
                    "Google/Meta/DeepMind directory comparisons are bounded, not an institutional full-web exhaustiveness guarantee.",
                    "Selected components are L1 diagnostics only; full high-cost experiments are not reproduced and do not enter automatic retries.",
                    "The fixed selected delivery does not claim every one of the835 bulletin identities was read in full text; global watermark remainsOct15."]}
    scope = {**common, "fixed_component_keys": sorted(COMPONENT_KEYS), "reference_only_keys": sorted(REFERENCE_KEYS), "papers": reviewed}
    batch = {**common, "date": "2026-10-26", "scope_kind": coverage["scope_kind"],
             "source_artifact": (AUDIT_REL / "README.md").relative_to("docs").as_posix(),
             "candidates": [{**r, "doc": r["detail_path"], "catalog_key": r["key"], "catalog_detail": r["detail_path"],
                 "track": "foundation-model" if r["domain"] == "foundation-models" else r["domain"],
                 "source_provenance": [{"source_url": r["paper_url"], "source_kind": "primary-method-resource-affiliation-review"}]}
                for r in reviewed]}
    updated = deepcopy(ledger)
    if extend_refs:
        expansion = {"added_reference_only_keys": ["harnessmm", "image-rsi", "rsi-opt"],
                     "component_scope_unchanged": True, "existing_acceptance_preserved": True}
        for value in (coverage, scope, batch):
            value["reference_scope_expansion"] = expansion
        updated["batches"] = [batch if b["batch"] == BATCH else b for b in updated["batches"]]
    else:
        updated["batches"].append(batch)
    for path, value in ((AUDIT / "source-coverage.json", coverage), (AUDIT / "task-scope.json", scope), (ledger_path, updated)):
        write(path, value)
    return counts


def check_evidence():
    catalog, spec = catalogue(), execution_spec()
    validate_catalog(catalog, {r["key"]: r for r in spec["components"]})
    blobs = {d: (AUDIT / f"raw-{d}.json").read_bytes() for d in ("cpu", "cuda")}
    raw = {d: json.loads(b) for d, b in blobs.items()}
    validate_raw(raw, spec)
    frozen = json.loads((AUDIT / "frozen-sources.json").read_text())
    require(frozen["commit"] == raw["cpu"]["code_commit"], "frozen commit binding")
    verify_sources(ROOT, frozen["commit"], raw["cpu"]["source_sha256"], frozen["proof"])
    for key in COMPONENT_KEYS:
        expected = result_for(key, raw, blobs, catalog)
        require(json.loads((ROOT / metric_path(key, catalog)).read_text()) == expected, f"{key}: raw/metric binding")
        require(load_gpu_receipt(ROOT / catalog[key]["gpu_validation_artifact"]) == receipt_for(key, expected, catalog), f"{key}: receipt binding")


def check():
    check_evidence()
    scope = json.loads((AUDIT / "task-scope.json").read_text())
    batches = [b for b in json.loads((ROOT / "docs/paper-discovery-ledger.json").read_text())["batches"] if b["batch"] == BATCH]
    require(len(batches) == 1, "exactly one ledger batch")
    validate_scope(scope, batches[0], catalogue())


def sync_figures():
    from PIL import Image

    catalog = catalogue()
    path = ROOT / "docs/paper-figures-manifest.json"
    rows = json.loads(path.read_text())
    for key in sorted(COMPONENT_KEYS | REFERENCE_KEYS):
        record = catalog[key]
        page = Path("docs") / record["detail_path"]
        assets = page.parent / "assets"
        proof = json.loads((ROOT / assets / "provenance.json").read_text())
        require(proof.get("visually_verified") is True or proof.get("visually_inspected") is True,
                f"{key}: original figure must have been visually verified")
        image = assets / proof.get("image", proof.get("local_path", "paper-figure-01.png"))
        blob = (ROOT / image).read_bytes()
        with Image.open(ROOT / image) as img:
            width, height = img.size
        expected = proof.get("image_sha256", proof.get("sha256"))
        if expected:
            require(expected == hashlib.sha256(blob).hexdigest(), "figure provenance hash")
        row = {"page": page.as_posix(), "paper_url": record["paper_url"],
               "arxiv_id": record["paper_url"].split("/")[-1].split("v")[0],
               "figure": str(proof.get("figure", "Figure 1")), "original_caption": proof.get("original_caption", ""),
               "source_url": proof.get("source_url", proof.get("source_image_url", record["paper_url"])),
               "extraction": "original-reviewed-paper-figure", "asset": image.as_posix(), "width": width,
               "height": height, "score": 0, "error": "", "sha256": hashlib.sha256(blob).hexdigest(),
               "visually_inspected": True}
        matches = [i for i, r in enumerate(rows) if r["page"] == row["page"]]
        require(len(matches) <= 1, "duplicate figure page")
        if matches:
            rows[matches[0]] = row
        else:
            rows.append(row)
    write(path, rows)


def validate_scope(scope, batch, catalog):
    candidates = batch["candidates"]
    require(scope.get("batch") == batch.get("batch") == BATCH
            and set(scope["fixed_component_keys"]) == COMPONENT_KEYS
            and len(scope["fixed_component_keys"]) == len(COMPONENT_KEYS)
            and set(scope["reference_only_keys"]) == REFERENCE_KEYS
            and len(scope["reference_only_keys"]) == len(REFERENCE_KEYS), "fixed batch scope")
    require({r["key"] for r in scope["papers"]} == COMPONENT_KEYS | REFERENCE_KEYS
            and len(scope["papers"]) == len(candidates) == len(COMPONENT_KEYS | REFERENCE_KEYS), "complete nonduplicated scope")
    for row, candidate in zip(scope["papers"], candidates):
        require(all(candidate[k] == v for k, v in row.items()), "scope/ledger exact binding")
        record = catalog[row["key"]]
        require(all(row[k] == record[k] for k in ("priority", "domain", "title", "paper_url", "detail_path", "first_author", "first_author_affiliation", "cost_assessment"))
                and row["original_published_at"] == record["published_at"], "canonical metadata binding")
        component = row["key"] in COMPONENT_KEYS
        require(row["id"] == record["paper_url"].split("/")[-1].split("v")[0]
                and row["decision"] == ("component_only" if component else "not_reproduced_high_cost")
                and row["resolution"] == ("bounded_l1_component_accepted" if component else "not_reproduced_high_cost")
                and row["component_evidence"] == (metric_path(row["key"], catalog).as_posix() if component else None),
                "canonical identity/decision/evidence binding")
        require(row["component_implemented"] is component and row["component_accepted"] is component
                and row["requires_gpu_validation"] is component and row["gpu_validation_passed"] is component
                and row["review_done"] is True and row["full_experiment_review_done"] is True
                and row["full_experiment_status"] == "not_reproduced_high_cost"
                and row["status"] == ("implemented" if component else "deferred")
                and row["implementation_status"] == record["implementation_status"]
                and row["automatic_retry"] is False and row["automatic_implementation_queue"] is False
                and row["promotion_eligible"] is False and row["evolve_integrated"] is False,
                "scope acceptance/claim boundary")
        require(candidate["doc"] == candidate["catalog_detail"] == record["detail_path"]
                and candidate["catalog_key"] == row["key"], "canonical aliases")
    require(scope["counts"] == batch["counts"] and scope["counts"]["selected_papers"] == len(COMPONENT_KEYS | REFERENCE_KEYS)
            and scope["counts"]["components_accepted"] == len(COMPONENT_KEYS)
            and scope["counts"]["gpu_validated_components"] == len(COMPONENT_KEYS)
            and scope["counts"]["components_pending_verification"] == 0
            and scope["counts"]["reference_only_high_cost_done"] == len(REFERENCE_KEYS)
            and scope["counts"]["capability_reproductions_claimed"] == 0, "exact completion counts")
    for value in (scope, batch):
        require(value["selected_scope_complete"] is True and value["delivery_status"] == "bounded_scope_complete"
                and value["review_watermark"] == {"before": "2026-10-15", "after": "2026-10-15"}
                and value["review_watermark_advanced"] is False and value["all_sources_exhaustive"] is False,
                "bounded closure is not global watermark")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cpu", type=Path)
    parser.add_argument("--cuda", type=Path)
    parser.add_argument("--build-review", type=Path)
    parser.add_argument("--extend-references", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--sync-figures", action="store_true")
    args = parser.parse_args()
    if args.cpu and args.cuda:
        ingest(args.cpu, args.cuda)
    if args.build_review:
        print(json.dumps(build_review(args.build_review, extend_refs=args.extend_references), ensure_ascii=False))
    if args.sync_figures:
        sync_figures()
    if args.check:
        check()
