"""Admit immutable Oct30 component runs; never promote diagnostics to capabilities."""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from auto_research.gpu_validation import load_gpu_receipt  # noqa: E402
from auto_research.paper_specs.catalog import catalog_records  # noqa: E402
from curate_oct21_component_evidence import aggregate, digest, require, write  # noqa: E402
from oct18_frozen_sources import capture_sources, verify_sources  # noqa: E402
from run_google_emnlp25_components import validate_row  # noqa: E402
from run_oct30_components import (  # noqa: E402
    COMPONENTS, PREFLIGHT, ROOT as RUN_ROOT, RUNNER, SEEDS, execution_spec, sources,
)

AUDIT = ROOT / "docs/research-audits/oct30-overlap-components"
BATCH = "2026-10-30-overlap-components"
FROZEN_COMMIT = "af9b9245aa85b4cbeb3da27ca701cc01cb94da86"
GPU_KEYS = {"merlin", "fold-bias", "swim", "mpopd", "pinger", "pinterest-rlbp"}
CPU_KEYS = {"concur", "crop", "emma", "evalalloc"}
REFERENCES = set()
WATERMARK = {"before": "2026-10-15", "after": "2026-10-15"}
BASELINE = ROOT / "docs/research-audits/oct29-components/source-coverage.json"
BASELINE_SHA256 = "de5b77edb65a2e99e6a0fe33a6a24f5abf10fe0c2cc90d2376dacbb6668bc98e"
CATEGORIES = {"cs.AI", "cs.CL", "cs.IR", "cs.LG", "cs.CV", "cs.RO", "cs.SD", "eess.AS"}
CROP_SOURCE = "https://research.google/pubs/crop-token-efficient-reasoning-in-large-language-models-via-regularized-prompt-optimization/"
FIXED_COUNTS = {
    "selected_papers": 10, "components_accepted": 10, "gpu_validated_components": 6,
    "cpu_only_components": 4, "reference_only_high_cost_done": 0,
    "components_pending_verification": 0, "capability_reproductions_claimed": 0,
}


def fixed_contract():
    require(set(COMPONENTS) == GPU_KEYS | CPU_KEYS and not GPU_KEYS & CPU_KEYS,
            "fixed ten-component identity set")
    require({k for k, (_, d) in COMPONENTS.items() if d == "cuda"} == GPU_KEYS
            and {k for k, (_, d) in COMPONENTS.items() if d == "cpu"} == CPU_KEYS,
            "fixed six CUDA/four CPU allocation")


def catalogue():
    fixed_contract()
    rows = catalog_records()
    records = {r["key"]: r for r in rows}
    require(set(COMPONENTS) <= records.keys(), "missing fixed-scope catalog records")
    return records


def metric_path(key, catalog):
    require(key in COMPONENTS and key in catalog, "unknown component metric")
    return (Path("docs") / Path(catalog[key]["detail_path"]).parent
            / f"metrics/component-{COMPONENTS[key][1]}-seeds42-44.json")


def validate_raw(raw, spec):
    """Require actual frozen runs, exact numerical gates and explicit device stamps."""
    fixed_contract()
    try:
        require(set(raw) == {"cpu", "cuda"}, "actual CPU and CUDA runs required")
        contracts = {r["key"]: r for r in spec["components"]}
        require(spec["schema_version"] == 1 and spec["seeds"] == SEEDS
                and len(spec["components"]) == 10 and set(contracts) == set(COMPONENTS),
                "fixed execution contracts")
        for key, contract in contracts.items():
            require(contract["source"] == "src/auto_research/" + COMPONENTS[key][0]
                    and contract["device"] == COMPONENTS[key][1], "fixed source/device contracts")
        require(raw["cpu"]["code_commit"] == raw["cuda"]["code_commit"] == FROZEN_COMMIT
                and raw["cpu"]["source_sha256"] == raw["cuda"]["source_sha256"],
                "one accepted frozen execution snapshot")
        expected_sources = set(sources(spec))
        require(len(expected_sources) == 15, "fifteen frozen execution files")
        for device, result in raw.items():
            expected = set(COMPONENTS) if device == "cpu" else GPU_KEYS
            require(result["schema_version"] == 2 and result["device"] == device
                    and result["seeds"] == SEEDS and set(result["components"]) == expected
                    and result["evaluation_tier"] == "l1_mechanism"
                    and result["diagnostic_only"] is True and result["formal_comparison"] is False
                    and result["promotion_eligible"] is False and result["evolve_integrated"] is False
                    and type(result["pretrained_model_calls"]) is int and result["pretrained_model_calls"] == 0
                    and result["full_experiments_executed"] is False,
                    "fixed component/device/diagnostic boundary")
            accelerator = result["accelerator"]
            require(accelerator == "CPU" if device == "cpu" else
                    isinstance(accelerator, str) and accelerator.startswith(("NVIDIA A100", "NVIDIA A30")),
                    "actual allowed accelerator required")
            require(type(result["elapsed_seconds"]) in (int, float)
                    and math.isfinite(result["elapsed_seconds"]) and result["elapsed_seconds"] >= 0,
                    "actual finite elapsed time")
            hashes = result["source_sha256"]
            require(set(hashes) == expected_sources and all(
                isinstance(v, str) and re.fullmatch(r"[0-9a-f]{64}", v) for v in hashes.values()),
                "complete executed source hash map")
            for key in expected:
                component = result["components"][key]
                require(set(component) == {"per_seed"}, "only actual per-seed rows")
                rows = component["per_seed"]
                require(len(rows) == 3 and [r["seed"] for r in rows] == SEEDS,
                        "three actual fixed seeds required")
                for row, seed in zip(rows, SEEDS):
                    validate_row(row, contracts[key], seed)
                    require(row["execution_device"] == device and row["execution_accelerator"] == accelerator,
                            "per-seed device stamp")
    except (KeyError, TypeError, AttributeError, IndexError) as exc:
        raise ValueError("malformed actual execution evidence") from exc


def result_for(key, raw, catalog):
    device = COMPONENTS[key][1]
    source = raw[device]
    dataset = {
        "id": f"synthetic:oct30-{key}-v1",
        "revision": "sha256:" + source["source_sha256"]["src/auto_research/" + COMPONENTS[key][0]],
        "recipe": "fixed seeded formula/state/statistical contracts; no public capability dataset",
        "capability_benchmark": False,
    }
    return {
        "schema_version": 2, "method": key, "manifest_ref": catalog[key]["domain"] + ":" + key,
        "paper": {"key": key, "title": catalog[key]["title"]}, "dataset": dataset,
        "seed": SEEDS, "seeds": SEEDS, "per_seed": source["components"][key]["per_seed"],
        "metrics": aggregate(source["components"][key]["per_seed"]),
        "evaluation_tier": "l1_mechanism",
        "evaluation_protocol": {
            "tier": "l1_mechanism", "seeds": SEEDS, "formal_comparison": False,
            "claim_policy": "bounded component contracts only, not a capability or complete paper reproduction",
        },
        "diagnostic_only": True, "fixture_demo": True, "formal_comparison": False,
        "promotion_eligible": False, "evolve_integrated": False,
        "automatic_retry": False, "automatic_implementation_queue": False,
        "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True,
        "provenance": {
            "commit": source["code_commit"], "artifact_path": metric_path(key, catalog).as_posix(),
            "accelerator": source["accelerator"], "executed_source_sha256": source["source_sha256"],
            "raw_runner_artifact_sha256": hashlib.sha256((AUDIT / f"raw-{device}.json").read_bytes()).hexdigest(),
            "dataset_fingerprint": "sha256:" + digest(dataset),
        },
    }


def receipt_for(key, result, catalog):
    require(key in GPU_KEYS, "only CUDA components receive GPU receipts")
    expected_path = f"docs/gpu-validations/{key}-a100-20261030.json"
    require(catalog[key]["gpu_validation_artifact"] == expected_path, "fixed Oct30 GPU receipt path")
    p = result["provenance"]
    require(p["commit"] == FROZEN_COMMIT, "GPU receipt frozen commit")
    return {
        "schema_version": 1, "adapter_key": key, "validated_at": "2026-10-30",
        "accelerator": {"vendor": "NVIDIA", "model": p["accelerator"], "count": 1},
        "command": ["python3", RUNNER, "--device", "cuda", "--source-commit", p["commit"],
                    "--frozen-proof", "oct30-frozen-proof.json", "--output", "results/components-cuda.json"],
        "dataset": result["dataset"],
        "checkpoint": {"public_id": "none-seeded-component-initialization", "revision": p["commit"], "pretrained": False},
        "seeds": SEEDS, "result": "passed", "metrics": result["metrics"],
        "executed_source_sha256": p["executed_source_sha256"],
        "provenance": {**p, "artifact_path": expected_path, "metric_artifact_path": metric_path(key, catalog).as_posix()},
        "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
        "automatic_retry": False, "automatic_implementation_queue": False,
        "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True,
    }


def _spec_path(key, catalog):
    return ROOT / "src/auto_research/paper_specs/catalog" / catalog[key]["domain"] / f"{key}.json"


def _load_actual():
    raw = {d: json.loads((AUDIT / f"raw-{d}.json").read_text()) for d in ("cpu", "cuda")}
    spec = execution_spec()
    validate_raw(raw, spec)
    frozen = json.loads((AUDIT / "frozen-sources.json").read_text())
    require(frozen["schema_version"] == 1 and frozen["commit"] == FROZEN_COMMIT, "fixed portable proof identity")
    verify_sources(ROOT, FROZEN_COMMIT, raw["cpu"]["source_sha256"], frozen["proof"])
    return raw


def ingest(cpu, cuda):
    """Explicit one-time acceptance; raw runner bytes and portable proof cannot be overwritten."""
    require(ROOT == RUN_ROOT, "runner and curator root disagree")
    cpu, cuda = Path(cpu), Path(cuda)
    blobs = {"cpu": cpu.read_bytes(), "cuda": cuda.read_bytes()}
    raw = {d: json.loads(blob) for d, blob in blobs.items()}
    spec, catalog = execution_spec(), catalogue()
    validate_raw(raw, spec)
    proof = capture_sources(ROOT, FROZEN_COMMIT, sources(spec))
    verify_sources(ROOT, FROZEN_COMMIT, raw["cpu"]["source_sha256"], proof)
    targets = [AUDIT / "raw-cpu.json", AUDIT / "raw-cuda.json", AUDIT / "frozen-sources.json"]
    records = {}
    for key, (_, device) in COMPONENTS.items():
        targets.append(ROOT / metric_path(key, catalog))
        record = json.loads(_spec_path(key, catalog).read_text())
        require(record["requires_gpu_validation"] is (device == "cuda"), "predeclared GPU requirement")
        record["gpu_validation_passed"] = device == "cuda"
        record["review_done"] = True
        records[key] = record
        if device == "cuda":
            receipt = f"docs/gpu-validations/{key}-a100-20261030.json"
            require(record["gpu_validation_artifact"] == receipt, "predeclared receipt identity")
            targets.append(ROOT / receipt)
    require(all(not p.exists() for p in targets), "immutable evidence admission; refuse existing raw/proof/projection")
    AUDIT.mkdir(parents=True, exist_ok=True)
    for device, blob in blobs.items():
        with (AUDIT / f"raw-{device}.json").open("xb") as stream:
            stream.write(blob)
    with (AUDIT / "frozen-sources.json").open("x") as stream:
        json.dump({"schema_version": 1, "commit": FROZEN_COMMIT, "proof": proof}, stream,
                  ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
    for key, (_, device) in COMPONENTS.items():
        result = result_for(key, raw, catalog)
        write(ROOT / metric_path(key, catalog), result)
        if device == "cuda":
            write(ROOT / catalog[key]["gpu_validation_artifact"], receipt_for(key, result, catalog))
        write(_spec_path(key, catalog), records[key])


def _catalog_boundary(item, gpu):
    require(item["implementation_status"] == "component_only" and item["adapter"] is None
            and item["evaluation_tier"] == "l1_mechanism" and item["diagnostic_only"] is True
            and item["promotion_eligible"] is False and item["evolve_integrated"] is False
            and item["automatic_retry"] is False and item["automatic_implementation_queue"] is False
            and item["full_experiment_status"] == "not_reproduced_high_cost"
            and item["full_experiment_review_done"] is True and item["review_done"] is True
            and item["review_resolution"] == "not_reproduced_high_cost"
            and item["requires_gpu_validation"] is gpu and item.get("gpu_validation_passed", False) is gpu,
            "catalog L1/device and terminal full-cost boundary")


def check_evidence():
    require(ROOT == RUN_ROOT, "runner and curator root disagree")
    raw, catalog = _load_actual(), catalogue()
    for key, (_, device) in COMPONENTS.items():
        item = catalog[key]
        _catalog_boundary(item, device == "cuda")
        expected = result_for(key, raw, catalog)
        require(json.loads((ROOT / metric_path(key, catalog)).read_text()) == expected, key + ": exact raw/metrics binding")
        if device == "cuda":
            require(load_gpu_receipt(ROOT / item["gpu_validation_artifact"]) == receipt_for(key, expected, catalog),
                    key + ": exact actual GPU receipt")


def _identities(values):
    require(isinstance(values, list) and all(isinstance(v, str) and re.fullmatch(r"\d{4}\.\d{4,5}(?:v\d+)?", v)
                                           for v in values), "versioned arXiv identities required")
    return {value.split("v", 1)[0] for value in values}


def source_facts(catalog, coverage=None, primary_receipts=None):
    """Recompute source claims from the committed baseline and actual bounded capture."""
    if coverage is None:
        coverage = json.loads((AUDIT / "source-coverage.json").read_text())
    try:
        require(hashlib.sha256(BASELINE.read_bytes()).hexdigest() == BASELINE_SHA256,
                "committed Oct29 coverage baseline changed")
        previous = json.loads(BASELINE.read_text())
        require(coverage["baseline"] == BASELINE.relative_to(ROOT).as_posix()
                and coverage["baseline_sha256"] == BASELINE_SHA256
                and coverage["batch"] == BATCH and coverage["checked_on"] == "2026-10-30"
                and coverage["actual_announced_on"] == "2026-10-28"
                and coverage["review_watermark"] == WATERMARK
                and coverage["review_watermark_advanced"] is False
                and coverage["all_sources_exhaustive"] is False
                and coverage["full_bulletin_full_text_review_complete"] is False
                and coverage["selected_scope_complete"] is True
                and coverage["delivery_status"] == "bounded_scope_complete"
                and isinstance(coverage["raw_capture_sha256"], str)
                and re.fullmatch(r"[0-9a-f]{64}", coverage["raw_capture_sha256"]),
                "bounded source review identity and non-exhaustive watermark")
        current = coverage["bulletin_ids_by_category"]
        recent = coverage["recent_ids_by_category_and_date"]
        require(set(current) == set(recent) == CATEGORIES, "exact eight source categories")
        delta = {kind: {} for kind in ("added", "removed")}
        for category in CATEGORIES:
            now, before = _identities(current[category]), _identities(previous["bulletin_ids_by_category"][category])
            delta["added"][category] = sorted(now - before)
            delta["removed"][category] = sorted(before - now)
        require(not any(delta["added"].values()) and not any(delta["removed"].values())
                and coverage["bulletin_delta"] == delta, "actual zero bulletin identity delta")
        shared = {}
        for category, days in previous["recent_ids_by_category_and_date"].items():
            for day, values in days.items():
                now, before = _identities(recent[category][day]), _identities(values)
                shared[category + ":" + day] = {"added": sorted(now - before), "removed": sorted(before - now)}
        require(coverage["shared_recent_date_delta"] == shared
                and all(not d["added"] and not d["removed"] for d in shared.values()),
                "actual zero shared-recent identity delta")
        receipts = coverage["retrieval_receipts"]
        require(len(receipts) == 16 and {(p["kind"], p["source"]) for p in receipts}
                == {(kind, category) for kind in ("arxiv-new", "arxiv-recent") for category in CATEGORIES},
                "one actual retrieval per category and list type")
        for page in receipts:
            kind, category = page["kind"], page["source"]
            listing = "new" if kind == "arxiv-new" else "recent"
            require(page["url"] == f"https://arxiv.org/list/{category}/{listing}?show=2000"
                    and page["status"] == "retrieved" and page["parse_complete"] is True
                    and datetime.fromisoformat(page["checked_at"].replace("Z", "+00:00")).date().isoformat() == "2026-10-30"
                    and isinstance(page["sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", page["sha256"]),
                    "actual fixed official source retrieval receipt")
            sections = page["sections"]
            require(all(type(s["shown"]) is int and s["shown"] >= 0 and s["shown"] == s["expected"] for s in sections),
                    "complete section counts")
            if kind == "arxiv-new":
                count = len(current[category])
                require(page["announced_on"] == "2026-10-28"
                        and len(sections) == 3 and {s["kind"] for s in sections} == {"new", "cross-list", "replacement"},
                        "actual bulletin date and three entry kinds")
            else:
                require(len(sections) == len(recent[category])
                        and {s["date"] for s in sections} == set(recent[category])
                        and all(s["shown"] == len(recent[category][s["date"]]) for s in sections),
                        "actual recent date partitions")
                count = sum(len(values) for values in recent[category].values())
                for values in recent[category].values():
                    _identities(values)
            require(type(page["expected_entries"]) is int and type(page["parsed_entries"]) is int
                    and page["expected_entries"] == page["parsed_entries"] == count == sum(s["shown"] for s in sections),
                    "complete list counts bound to retained identities")
        before_capture = min(datetime.fromisoformat(p["checked_at"].replace("Z", "+00:00"))
                             for p in previous["retrieval_receipts"])
        facts = {}
        for key in COMPONENTS:
            item = catalog[key]
            identity = item["paper_url"].split("/")[-1].split("v", 1)[0]
            provenance = [{"source_kind": "reviewed-fixed-primary-paper",
                           "source_url": item.get("reviewed_version_url", item["paper_url"])}]
            if key == "crop":
                primary = (json.loads((AUDIT / "official-primary-receipts.json").read_text())
                           if primary_receipts is None else primary_receipts)
                require(any(p["url"] == CROP_SOURCE and p["status"] == "retrieved" for p in primary["pages"]),
                        "historical Google source must have an actual primary receipt")
                provenance.append({"source_kind": "historical-google-directory-backfill", "source_url": CROP_SOURCE})
            listed = False
            for page in receipts:
                category = page["source"]
                dates = ([page["announced_on"]] if page["kind"] == "arxiv-new" and identity in _identities(current[category])
                         else sorted(day for day, ids in recent[category].items() if identity in _identities(ids))
                         if page["kind"] == "arxiv-recent" else [])
                if dates:
                    listed = True
                    provenance.append({"source_kind": page["kind"], "source_url": page["url"], "announced_dates": dates})
            require(listed is (key != "crop"), "one historical source and nine actually listed overlap backfills")
            facts[key] = {
                "first_publication_after_previous_capture": datetime.fromisoformat(item["published_at"].replace("Z", "+00:00")) > before_capture,
                "intake_class": item["intake_class"], "source_provenance": provenance, "historical": not listed,
            }
        counts = {
            **FIXED_COUNTS,
            "latest_category_entries": sum(len(values) for values in current.values()),
            "latest_unique_identities": len(set().union(*(_identities(values) for values in current.values()))),
            "new_bulletin_identities_since_previous_capture": len(set().union(*(set(v) for v in delta["added"].values()))),
            "selected_first_publications_after_previous_capture": sum(f["first_publication_after_previous_capture"] for f in facts.values()),
            "selected_historical_official_source_backfills": sum(f["historical"] for f in facts.values()),
            "selected_recent_overlap_backfills": sum(not f["historical"] for f in facts.values()),
        }
        require(counts["selected_first_publications_after_previous_capture"] == 0
                and counts["new_bulletin_identities_since_previous_capture"] == 0
                and coverage["counts"] == counts and all(type(v) is int for v in coverage["counts"].values()),
                "derived zero-new and overlap/historical counts")
        return facts, counts
    except (KeyError, TypeError, AttributeError, IndexError) as exc:
        raise ValueError("malformed retained source coverage") from exc


def validate_scope(scope, batch, catalog, coverage=None, primary_receipts=None):
    """Joint scope/ledger edits cannot forge acceptance, counts or review closure."""
    fixed_contract()
    try:
        source_rows, expected_counts = source_facts(catalog, coverage, primary_receipts)
        require(scope["fixed_component_keys"] == sorted(COMPONENTS) and scope.get("reference_only_keys", []) == [],
                "fixed ten components and zero reference-only papers")
        require(scope["batch"] == batch["batch"] == BATCH, "fixed review batch")
        papers, candidates = scope["papers"], batch["candidates"]
        require(len(papers) == len(candidates) == 10
                and {r["key"] for r in papers} == {r["key"] for r in candidates} == set(COMPONENTS),
                "nonduplicated complete ten-paper scope")
        preflight = json.loads((ROOT / PREFLIGHT).read_text())
        declared = {r["key"]: r for r in preflight["papers"]}
        require(preflight["batch"] == BATCH and len(declared) == 10 and set(declared) == set(COMPONENTS),
                "frozen preflight scope")
        for row, candidate in zip(papers, candidates):
            require(all(candidate.get(k) == v for k, v in row.items()), "scope/ledger exact row match")
            key, item = row["key"], catalog[row["key"]]
            gpu = key in GPU_KEYS
            _catalog_boundary(item, gpu)
            require(all(row[k] == item[k] for k in (
                "domain", "title", "paper_url", "detail_path", "priority", "first_author",
                "first_author_affiliation", "published_at", "cost_assessment", "implementation_status")),
                "canonical paper/cost facts")
            identity = item["paper_url"].split("/")[-1].split("v", 1)[0]
            require(row["id"] == identity == declared[key]["id"]
                    and declared[key]["component_device"] == COMPONENTS[key][1]
                    and row["component_evidence"] == metric_path(key, catalog).as_posix(),
                    "canonical identity/evidence/device")
            require(all(row[field] == source_rows[key][field] for field in (
                "intake_class", "first_publication_after_previous_capture", "source_provenance"))
                    and type(row["first_publication_after_previous_capture"]) is bool,
                "actual intake, first-publication timing and primary/listing provenance")
            require(row["component_accepted"] is True and row["component_implemented"] is True
                    and row["review_done"] is True and row["full_experiment_review_done"] is True
                    and row["full_experiment_status"] == "not_reproduced_high_cost"
                    and row["status"] == "implemented" and row["resolution"] == "bounded_l1_component_accepted"
                    and row["requires_gpu_validation"] is gpu and row["gpu_validation_passed"] is gpu
                    and row["promotion_eligible"] is False and row["evolve_integrated"] is False
                    and row["automatic_retry"] is False and row["automatic_implementation_queue"] is False,
                    "canonical acceptance, terminal full-cost and no capability/automatic retry boundary")
        for payload in (scope, batch):
            require(payload["counts"] == expected_counts and all(type(v) is int for v in payload["counts"].values()),
                    "derived fixed-scope and source-delta counts")
            require(payload["review_watermark"] == WATERMARK and payload["review_watermark_advanced"] is False
                    and payload["all_sources_exhaustive"] is False and payload["selected_scope_complete"] is True
                    and payload["delivery_status"] == "bounded_scope_complete",
                    "bounded delivery does not advance the global review watermark")
        require(batch["counts"] == scope["counts"], "scope/ledger identical counts")
    except (KeyError, TypeError, AttributeError, IndexError) as exc:
        raise ValueError("malformed fixed-scope review evidence") from exc


def check():
    check_evidence()
    scope = json.loads((AUDIT / "task-scope.json").read_text())
    batches = [b for b in json.loads((ROOT / "docs/paper-discovery-ledger.json").read_text())["batches"]
               if b["batch"] == BATCH]
    require(len(batches) == 1, "one immutable reviewed batch")
    validate_scope(scope, batches[0], catalogue())


def sync_figures():
    from PIL import Image

    catalog = catalogue()
    path = ROOT / "docs/paper-figures-manifest.json"
    rows = json.loads(path.read_text())
    for key in sorted(COMPONENTS):
        record = catalog[key]
        page = Path("docs") / record["detail_path"]
        assets = page.parent / "assets"
        proof = json.loads((ROOT / assets / "provenance.json").read_text())
        require(proof.get("visually_verified") is True or proof.get("visually_inspected") is True
                or (isinstance(proof.get("visual_review"), str) and bool(proof["visual_review"].strip())),
                key + ": recorded original-figure visual inspection required")
        image = assets / "paper-figure-01.png"
        blob = (ROOT / image).read_bytes()
        checksum = hashlib.sha256(blob).hexdigest()
        require(proof.get("sha256", proof.get("image_sha256")) == checksum, key + ": original figure digest")
        with Image.open(ROOT / image) as img:
            width, height = img.size
        if "width" in proof or "height" in proof:
            require((proof.get("width"), proof.get("height")) == (width, height), "figure dimensions")
        if "pixel_dimensions" in proof:
            require(proof["pixel_dimensions"] == [width, height], "figure pixel dimensions")
        row = {
            "page": page.as_posix(), "paper_url": record["paper_url"],
            "arxiv_id": record["paper_url"].split("/")[-1].split("v", 1)[0],
            "figure": proof["figure"], "original_caption": proof.get("caption", ""),
            "source_url": proof["source_url"], "extraction": proof.get("transformation", "original source figure"),
            "asset": image.as_posix(), "width": width, "height": height, "score": 0, "error": "",
            "sha256": checksum, "visually_inspected": True,
        }
        indices = [i for i, existing in enumerate(rows) if existing["page"] == row["page"]]
        require(len(indices) <= 1, "one original source figure per page")
        if indices:
            rows[indices[0]] = row
        else:
            rows.append(row)
    write(path, rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cpu", type=Path)
    parser.add_argument("--cuda", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--sync-figures", action="store_true")
    args = parser.parse_args()
    if args.cpu or args.cuda:
        if not (args.cpu and args.cuda):
            parser.error("both actual CPU and CUDA runs required")
        ingest(args.cpu, args.cuda)
    if args.check:
        check()
    if args.sync_figures:
        sync_figures()
