"""Bind the fixed Oct29 low-cost scope to actual frozen CPU/A100 evidence."""
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
from curate_oct21_component_evidence import aggregate, digest, require, write  # noqa: E402
from oct18_frozen_sources import capture_sources, verify_sources  # noqa: E402
from run_google_emnlp25_components import validate_row  # noqa: E402
from run_oct29_components import COMPONENTS, ROOT as RUN_ROOT, RUNNER, SEEDS, execution_spec, sources  # noqa: E402

AUDIT = ROOT / "docs/research-audits/oct29-components"
BATCH = "2026-10-29-priority-components"
REFERENCES = {"pailitao-mmsearch2"}


def catalogue():
    return {r["key"]: r for r in catalog_records()}


def metric_path(key, catalog):
    device = COMPONENTS[key][1]
    return Path("docs") / Path(catalog[key]["detail_path"]).parent / f"metrics/component-{device}-seeds42-44.json"


def validate_raw(raw, spec):
    require(set(raw) == {"cpu", "cuda"}, "actual CPU and CUDA runs required")
    require(raw["cpu"]["code_commit"] == raw["cuda"]["code_commit"]
            and raw["cpu"]["source_sha256"] == raw["cuda"]["source_sha256"], "one frozen execution snapshot")
    for device, result in raw.items():
        expected = {r["key"]: r for r in spec["components"] if device == "cpu" or r["device"] == "cuda"}
        require(result.get("schema_version") == 2 and result.get("device") == device
                and result.get("seeds") == SEEDS and set(result.get("components", {})) == set(expected)
                and result.get("diagnostic_only") is True and result.get("formal_comparison") is False
                and result.get("promotion_eligible") is False and result.get("evolve_integrated") is False
                and result.get("pretrained_model_calls") == 0 and result.get("full_experiments_executed") is False,
                "fixed component/device/claim boundary")
        require(result["accelerator"] == "CPU" if device == "cpu" else
                result["accelerator"] in {"NVIDIA A100-SXM4-80GB", "NVIDIA A100-PCIE-40GB", "NVIDIA A30"},
                "real allowed accelerator required")
        require(set(result["source_sha256"]) == set(sources(spec)), "complete executed source map")
        for key, contract in expected.items():
            rows = result["components"][key]["per_seed"]
            require([r["seed"] for r in rows] == SEEDS, "three actual seeds required")
            for row, seed in zip(rows, SEEDS):
                validate_row(row, contract, seed)
                require(row["execution_device"] == device and row["execution_accelerator"] == result["accelerator"],
                        "per-seed device stamp")


def result_for(key, raw, catalog):
    device = COMPONENTS[key][1]
    source = raw[device]
    dataset = {"id": f"synthetic:oct29-{key}-v1", "revision": "sha256:" + source["source_sha256"]["src/auto_research/" + COMPONENTS[key][0]],
               "recipe": "fixed seeded mechanism contracts, no public capability dataset", "capability_benchmark": False}
    return {"schema_version": 2, "method": key, "manifest_ref": catalog[key]["domain"] + ":" + key,
            "paper": {"key": key, "title": catalog[key]["title"]}, "dataset": dataset,
            "seed": SEEDS, "seeds": SEEDS, "per_seed": source["components"][key]["per_seed"],
            "metrics": aggregate(source["components"][key]["per_seed"]),
            "evaluation_tier": "l1_mechanism", "evaluation_protocol": {"tier": "l1_mechanism", "seeds": SEEDS,
                "formal_comparison": False, "claim_policy": "component formulas/contracts only, not a capability or full paper reproduction"},
            "diagnostic_only": True, "fixture_demo": True, "formal_comparison": False,
            "promotion_eligible": False, "evolve_integrated": False, "full_experiment_status": "not_reproduced_high_cost",
            "full_experiment_review_done": True, "provenance": {"commit": source["code_commit"],
                "artifact_path": metric_path(key, catalog).as_posix(), "accelerator": source["accelerator"],
                "executed_source_sha256": source["source_sha256"],
                "raw_runner_artifact_sha256": hashlib.sha256((AUDIT / f"raw-{device}.json").read_bytes()).hexdigest(),
                "dataset_fingerprint": "sha256:" + digest(dataset)}}


def receipt_for(key, result, catalog):
    p = result["provenance"]
    return {"schema_version": 1, "adapter_key": key, "validated_at": "2026-10-29",
            "accelerator": {"vendor": "NVIDIA", "model": p["accelerator"], "count": 1},
            "command": ["python3", RUNNER, "--device", "cuda", "--source-commit", p["commit"],
                        "--frozen-proof", "oct29-frozen-proof.json", "--output", "results/components-cuda.json"],
            "dataset": result["dataset"], "checkpoint": {"public_id": "none-seeded-component-initialization",
                "revision": p["commit"], "pretrained": False}, "seeds": SEEDS, "result": "passed",
            "metrics": result["metrics"], "executed_source_sha256": p["executed_source_sha256"],
            "provenance": {**p, "artifact_path": catalog[key]["gpu_validation_artifact"],
                           "metric_artifact_path": metric_path(key, catalog).as_posix()},
            "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
            "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True}


def ingest(cpu, cuda):
    require(not (AUDIT / "raw-cuda.json").exists(), "immutable accepted evidence; refuse overwrite")
    raw = {"cpu": json.loads(cpu.read_text()), "cuda": json.loads(cuda.read_text())}
    spec, catalog = execution_spec(), catalogue()
    validate_raw(raw, spec)
    proof = capture_sources(ROOT, raw["cpu"]["code_commit"], sources(spec))
    verify_sources(ROOT, raw["cpu"]["code_commit"], raw["cpu"]["source_sha256"], proof)
    for device, path in (("cpu", cpu), ("cuda", cuda)):
        (AUDIT / f"raw-{device}.json").write_bytes(path.read_bytes())
    write(AUDIT / "frozen-sources.json", {"schema_version": 1, "commit": raw["cpu"]["code_commit"], "proof": proof})
    for key, (_, device) in COMPONENTS.items():
        result = result_for(key, raw, catalog)
        write(ROOT / metric_path(key, catalog), result)
        if device == "cuda":
            write(ROOT / catalog[key]["gpu_validation_artifact"], receipt_for(key, result, catalog))
            path = ROOT / "src/auto_research/paper_specs/catalog" / catalog[key]["domain"] / f"{key}.json"
            record = json.loads(path.read_text())
            record["gpu_validation_passed"] = True
            record["review_done"] = True
            write(path, record)


def check_evidence():
    require(ROOT == RUN_ROOT, "runner and curator root disagree")
    catalog, spec = catalogue(), execution_spec()
    raw = {d: json.loads((AUDIT / f"raw-{d}.json").read_text()) for d in ("cpu", "cuda")}
    validate_raw(raw, spec)
    frozen = json.loads((AUDIT / "frozen-sources.json").read_text())
    require(frozen["commit"] == raw["cpu"]["code_commit"], "frozen commit")
    verify_sources(ROOT, frozen["commit"], raw["cpu"]["source_sha256"], frozen["proof"])
    for key, (_, device) in COMPONENTS.items():
        item = catalog[key]
        require(item["implementation_status"] == "component_only" and item["diagnostic_only"] is True
                and item["evaluation_tier"] == "l1_mechanism" and item["adapter"] is None
                and item["evolve_integrated"] is False and item["promotion_eligible"] is False
                and item["full_experiment_review_done"] is True and item["automatic_retry"] is False,
                "catalog L1 and terminal full-cost boundary")
        expected = result_for(key, raw, catalog)
        require(json.loads((ROOT / metric_path(key, catalog)).read_text()) == expected, key + ": exact raw/metrics")
        require(item["requires_gpu_validation"] is (device == "cuda"), "GPU declaration")
        if device == "cuda":
            require(item.get("gpu_validation_passed") is True, "actual GPU acceptance required")
            require(load_gpu_receipt(ROOT / item["gpu_validation_artifact"]) == receipt_for(key, expected, catalog), "exact GPU receipt")


def sync_projections():
    """Regenerate derived schema only; actual raw runs and proof stay immutable."""
    raw = {d: json.loads((AUDIT / f"raw-{d}.json").read_text()) for d in ("cpu", "cuda")}
    spec, catalog = execution_spec(), catalogue()
    validate_raw(raw, spec)
    frozen = json.loads((AUDIT / "frozen-sources.json").read_text())
    require(frozen["commit"] == raw["cpu"]["code_commit"], "frozen snapshot identity")
    verify_sources(ROOT, frozen["commit"], raw["cpu"]["source_sha256"], frozen["proof"])
    for key, (_, device) in COMPONENTS.items():
        result = result_for(key, raw, catalog)
        write(ROOT / metric_path(key, catalog), result)
        if device == "cuda":
            write(ROOT / catalog[key]["gpu_validation_artifact"], receipt_for(key, result, catalog))


def review(capture, priority, additional, inventory, details):
    check_evidence()
    catalog = catalogue()
    ledger_path = ROOT / "docs/paper-discovery-ledger.json"
    ledger = json.loads(ledger_path.read_text())
    require(not any(b["batch"] == BATCH for b in ledger["batches"]), "immutable review batch")
    rows = json.loads(capture.read_text())
    pages = [r for r in rows if r["kind"] == "arxiv-new"]
    recent = [r for r in rows if r["kind"] == "arxiv-recent"]
    categories = {"cs.AI", "cs.CL", "cs.IR", "cs.LG", "cs.CV", "cs.RO", "cs.SD", "eess.AS"}
    require(len(pages) == len(recent) == 8 and {r["source"] for r in pages} == categories
            and {r["source"] for r in recent} == categories, "eight latest and eight recent pages")
    require(all(p["status"] == "retrieved" and p["parse_complete"] is True
                and p["expected_entries"] == p["parsed_entries"] == len(p["records"]) for p in rows), "complete parsed captures")
    require({p["announced_on"] for p in pages} == {"2026-10-28"}, "actual bulletin date, not wall clock")
    priority_review = json.loads(priority.read_text())
    directory_inventory = json.loads(inventory.read_text())
    require(len(directory_inventory["pages"]) == 44 and all(p["status"] == "retrieved" for p in directory_inventory["pages"]),
            "44 current bounded official directory pages")
    priority_review["raw_directory_capture"] = "official-source-inventory.json"
    priority_review["directory_detail_capture"] = "official-source-details.json"
    write(AUDIT / "official-source-inventory.json", directory_inventory)
    write(AUDIT / "official-source-details.json", json.loads(details.read_text()))
    review_rows = []
    for key in sorted(set(COMPONENTS) | REFERENCES):
        r, component = catalog[key], key in COMPONENTS
        require(r["full_experiment_status"] == "not_reproduced_high_cost" and r["full_experiment_review_done"] is True
                and r["review_done"] is True and r["automatic_retry"] is False, "terminal cost disposition")
        item = {k: r[k] for k in ("domain", "key", "title", "paper_url", "detail_path", "priority", "first_author",
                                  "first_author_affiliation", "published_at", "cost_assessment", "implementation_status")}
        item.update(id=r["paper_url"].split("/")[-1].split("v")[0],
            intake_class=r["intake_class"], status="implemented" if component else "deferred",
            first_publication_after_previous_capture=r["published_at"] > "2026-10-26T09:43:00Z",
            component_accepted=component, component_implemented=component, review_done=True,
            full_experiment_status="not_reproduced_high_cost", full_experiment_review_done=True,
            resolution="bounded_l1_component_accepted" if component else "not_reproduced_high_cost",
            requires_gpu_validation=r["requires_gpu_validation"], gpu_validation_passed=r.get("gpu_validation_passed", False),
            component_evidence=metric_path(key, catalog).as_posix() if component else None,
            automatic_retry=False, automatic_implementation_queue=False, promotion_eligible=False, evolve_integrated=False)
        if not component:
            require(r["review_resolution"] == "not_reproduced_high_cost" and bool(r["deferral_reason"]),
                    "terminal reference needs an explicit non-reproduction reason")
            item["reason"] = r["deferral_reason"]
        review_rows.append(item)
    counts = {"selected_papers": len(review_rows), "components_accepted": 8,
              "gpu_validated_components": 4, "cpu_only_components": 4, "reference_only_high_cost_done": 1,
              "components_pending_verification": 0, "capability_reproductions_claimed": 0,
              "latest_category_entries": sum(len(p["records"]) for p in pages),
              "latest_unique_identities": len({r["id"].split("v")[0] for p in pages for r in p["records"]}),
              "selected_first_publications_after_previous_capture": sum(r["first_publication_after_previous_capture"] for r in review_rows),
              "selected_historical_official_source_backfills": 2,
              "section_entry_counts": dict(Counter(r["entry_kind"] for p in pages for r in p["records"]))}
    common = {"schema_version": 1, "batch": BATCH, "counts": counts, "selected_scope_complete": True,
              "delivery_status": "bounded_scope_complete", "all_sources_exhaustive": False,
              "review_watermark_advanced": False, "review_watermark": {"before": "2026-10-15", "after": "2026-10-15"}}
    extra = json.loads(additional.read_text())["candidates"]
    coverage = {**common, "checked_on": "2026-10-29", "actual_announced_on": "2026-10-28",
        "raw_capture_sha256": hashlib.sha256(capture.read_bytes()).hexdigest(),
        "retrieval_receipts": [{k: v for k, v in p.items() if k != "records"} for p in rows],
        "bulletin_ids_by_category": {p["source"]: [r["id"] for r in p["records"]] for p in pages},
        "recent_ids_by_category_and_date": {p["source"]: {d: [r["id"] for r in p["records"] if r["announced_on"] == d]
             for d in ("2026-10-27", "2026-10-28")} for p in recent},
        "priority_review": priority_review, "additional_dispositions": extra,
        "full_bulletin_full_text_review_complete": False,
        "limitations": ["Latest actual official bulletin is Oct28; no Oct29 announcement is fabricated.",
            "Recent pages include Oct27 plus overlap; listings and replacements are not new first-publication counts.",
            "Official-source comparison is bounded and partly reconstructed, not whole-web exhaustiveness.",
            "Eight accepted L1 components do not establish model capabilities or full reproduction.",
            "Sleep and HOPE are historical official-source-triggered backfills; EG2/RPL updates retain existing identities.",
            "The global full-review watermark remains Oct15; this selected delivery does not close every recalled identity."]}
    scope = {**common, "fixed_component_keys": sorted(COMPONENTS), "reference_only_keys": sorted(REFERENCES),
             "papers": review_rows, "updated_existing_keys": ["embedding-gemma2", "rpl"], "additional_dispositions": extra}
    batch = {**common, "date": "2026-10-29", "source_artifact": "research-audits/oct29-components/README.md",
        "additional_dispositions": extra, "candidates": [{**r, "doc": r["detail_path"], "catalog_key": r["key"],
            "catalog_detail": r["detail_path"], "track": {"agent-research": "agent", "foundation-models": "foundation-model"}.get(r["domain"], r["domain"]),
            "source_provenance": [{"source_url": r["paper_url"], "source_kind": "primary-method-resource-affiliation-review"}]} for r in review_rows]}
    updated = deepcopy(ledger)
    updated["batches"].append(batch)
    for path, payload in ((AUDIT / "source-coverage.json", coverage), (AUDIT / "task-scope.json", scope), (ledger_path, updated)):
        write(path, payload)


def validate_scope(scope, batch, catalog):
    require(scope["fixed_component_keys"] == sorted(COMPONENTS) and scope["reference_only_keys"] == sorted(REFERENCES), "fixed scope")
    require(scope.get("batch") == batch.get("batch") == BATCH
            and len(scope["papers"]) == 9 and len(batch["candidates"]) == 9
            and {r["key"] for r in scope["papers"]} == set(COMPONENTS) | REFERENCES, "nonduplicated complete scope")
    for row, candidate in zip(scope["papers"], batch["candidates"]):
        require(all(candidate[k] == v for k, v in row.items()), "scope/ledger exact match")
        r = catalog[row["key"]]
        require(all(row[k] == r[k] for k in ("domain", "title", "paper_url", "detail_path", "priority", "published_at", "cost_assessment")), "canonical scope facts")
        component = row["key"] in COMPONENTS
        gpu = component and COMPONENTS[row["key"]][1] == "cuda"
        if not component:
            require(r["review_resolution"] == "not_reproduced_high_cost"
                    and bool(r["deferral_reason"]) and row.get("reason") == r["deferral_reason"],
                    "canonical terminal non-reproduction reason")
        require(row["component_accepted"] is component and row["component_implemented"] is component
                and row["id"] == r["paper_url"].split("/")[-1].split("v")[0]
                and row["component_evidence"] == (metric_path(row["key"], catalog).as_posix() if component else None), "canonical acceptance/evidence")
        require(row["requires_gpu_validation"] is gpu and row["gpu_validation_passed"] is gpu
                and row["review_done"] is True and row["full_experiment_review_done"] is True
                and row["full_experiment_status"] == "not_reproduced_high_cost"
                and row["status"] == ("implemented" if component else "deferred")
                and row["resolution"] == ("bounded_l1_component_accepted" if component else "not_reproduced_high_cost")
                and row["implementation_status"] == ("component_only" if component else "deferred_high_cost")
                and row["promotion_eligible"] is False and row["evolve_integrated"] is False,
                "canonical device, resolution and capability boundary")
    fixed_counts = {"selected_papers": 9, "components_accepted": 8, "gpu_validated_components": 4,
                    "cpu_only_components": 4, "reference_only_high_cost_done": 1,
                    "components_pending_verification": 0, "capability_reproductions_claimed": 0}
    require(all(scope["counts"][k] == v for k, v in fixed_counts.items()), "canonical fixed-scope counts")
    require(scope["review_watermark"] == {"before": "2026-10-15", "after": "2026-10-15"}
            and batch["counts"] == scope["counts"] and scope["review_watermark_advanced"] is False,
            "bounded review not full-watermark advance")


def check():
    check_evidence()
    scope = json.loads((AUDIT / "task-scope.json").read_text())
    batches = [b for b in json.loads((ROOT / "docs/paper-discovery-ledger.json").read_text())["batches"] if b["batch"] == BATCH]
    require(len(batches) == 1, "one reviewed batch")
    validate_scope(scope, batches[0], catalogue())


def sync_figures():
    from PIL import Image

    catalog = catalogue()
    path = ROOT / "docs/paper-figures-manifest.json"
    rows = json.loads(path.read_text())
    for key in sorted(set(COMPONENTS) | REFERENCES | {"embedding-gemma2"}):
        record = catalog[key]
        page = Path("docs") / record["detail_path"]
        assets = page.parent / "assets"
        proof = json.loads((ROOT / assets / "provenance.json").read_text())
        require(proof.get("visually_verified") is True or proof.get("visually_inspected") is True,
                f"{key}: original figure visual review required")
        image = assets / "paper-figure-01.png"
        blob = (ROOT / image).read_bytes()
        require(proof.get("sha256", proof.get("image_sha256")) == hashlib.sha256(blob).hexdigest(), "figure digest")
        with Image.open(ROOT / image) as img:
            width, height = img.size
        row = {"page": page.as_posix(), "paper_url": record["paper_url"],
            "arxiv_id": record["paper_url"].split("/")[-1].split("v")[0],
            "figure": proof["figure"], "original_caption": "", "source_url": proof["source_url"],
            "extraction": proof.get("transformation", "original source figure"), "asset": image.as_posix(),
            "width": width, "height": height, "score": 0, "error": "", "sha256": hashlib.sha256(blob).hexdigest(),
            "visually_inspected": True}
        existing = [i for i, r in enumerate(rows) if r["page"] == row["page"]]
        require(len(existing) <= 1, "one source figure entry per page")
        if existing:
            rows[existing[0]] = row
        else:
            rows.append(row)
    write(path, rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cpu", type=Path)
    parser.add_argument("--cuda", type=Path)
    parser.add_argument("--capture", type=Path)
    parser.add_argument("--priority", type=Path)
    parser.add_argument("--additional", type=Path)
    parser.add_argument("--priority-inventory", type=Path)
    parser.add_argument("--priority-details", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--sync-figures", action="store_true")
    parser.add_argument("--sync-projections", action="store_true")
    args = parser.parse_args()
    if args.cpu or args.cuda:
        if not (args.cpu and args.cuda):
            parser.error("both actual runs required")
        ingest(args.cpu, args.cuda)
    if args.sync_projections:
        sync_projections()
    if args.capture:
        if not (args.priority and args.additional and args.priority_inventory and args.priority_details):
            parser.error("explicit primary-source and additional review required")
        review(args.capture, args.priority, args.additional, args.priority_inventory, args.priority_details)
    if args.check:
        check()
    if args.sync_figures:
        sync_figures()
