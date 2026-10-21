#!/usr/bin/env python3
"""Curate actual follow-up diagnostics and distinguish backlog from fresh announcements."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from auto_research.paper_specs.catalog import catalog_records  # noqa: E402
from auto_research.gpu_validation import load_gpu_receipt  # noqa: E402
from curate_oct21_component_evidence import aggregate, digest, require, write  # noqa: E402
from oct18_frozen_sources import capture_sources, verify_sources  # noqa: E402

AUDIT = ROOT / "docs/research-audits/oct21-followup"
BATCH = "2026-10-21-same-bulletin-followup"
COMPONENTS = {"agent-s4": "cpu", "ask-to-distill": "cuda", "projected-distillation": "cuda",
              "stratified-sparse-attention": "cuda", "race-rope-compression": "cuda"}
REFERENCES = {"residency-rl"}
SEEDS = [42, 43, 44]
COSTS = {
    "agent-s4": "Qwen3.8-27B, 30 evolutionary generations, 30/48 training and15 validation tasks, long GUI rollouts and cloud VMs; no full OSWorld evaluation.",
    "ask-to-distill": "Multi-model ask/answer/distill training and long on-policy generations; no teacher/student checkpoint or dataset downloaded for this component.",
    "projected-distillation": "Original eight-A100 training and paid API projection/verifier matrix; no full checkpoint training or projector service.",
    "stratified-sparse-attention": "Original multi-billion-parameter long-context model/kernel benchmark campaign; no checkpoint, throughput claim or serving system.",
    "race-rope-compression": "Original multi-billion-parameter model calibration, recovery training and long-context benchmark matrix; no complete checkpoint experiment. Native projection folding does not require a custom CUDA kernel.",
    "residency-rl": "Internal Gemini3.5 Flash GRPO, Gemini3.1 Pro simulation/judging,57,453 scenarios and up to60 dialogue turns plus8 tool calls; author code explicitly not released.",
}


def records():
    index = {r["key"]: r for r in catalog_records()}
    require(set(COMPONENTS) | REFERENCES <= index.keys(), "missing fixed-scope paper")
    return index


def metric_path(row, device):
    return Path("docs") / Path(row["detail_path"]).parent / "metrics" / f"component-{device}-seeds42-44.json"


def curate(inputs):
    index = records()
    proofs = {"schema_version": 1, "commits": {}}
    for key, device in COMPONENTS.items():
        raw_bytes = Path(inputs[key]).read_bytes()
        raw = json.loads(raw_bytes)
        require(raw["device"] == device and raw["seeds"] == SEEDS and raw["diagnostic_only"] is True,
                f"wrong run boundary: {key}")
        require(device == "cpu" or "A100" in raw["accelerator"] or "A30" in raw["accelerator"], "real NVIDIA receipt required")
        rows = raw["components"][key]["per_seed"]
        require(all(r.get("checks") and all(v is True for v in r["checks"].values()) for r in rows), "defining checks failed")
        hashes, commit = raw["source_sha256"], raw["code_commit"]
        for path, expected in hashes.items():
            require(hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == expected, "executed source changed")
        old = proofs["commits"].get(commit, {}).get("executed_source_sha256", {})
        merged = {**old, **hashes}
        proofs["commits"][commit] = {"executed_source_sha256": merged, "proof": capture_sources(ROOT, commit, merged)}
        result_path = metric_path(index[key], device)
        dataset = {"id": f"synthetic:oct21-followup-{key}-v1", "revision": "sha256:"+digest(hashes),
                   "capability_benchmark": False, "recipe": "fixed-source-generated-component-inputs-v1"}
        provenance = {"commit": commit, "artifact_path": result_path.as_posix(),
                      "raw_runner_artifact_sha256": hashlib.sha256(raw_bytes).hexdigest(), "executed_source_sha256": hashes,
                      "dataset_fingerprint": "sha256:"+digest({"dataset": dataset, "seeds": SEEDS, "source": hashes}),
                      "accelerator": raw.get("accelerator", "CPU")}
        result = {"schema_version": 2, "method": key, "manifest_ref": index[key]["domain"]+":"+key,
                  "seeds": SEEDS, "dataset": dataset, "per_seed": rows, "metrics": aggregate(rows), "provenance": provenance,
                  "evaluation_tier": "l1_mechanism", "evaluation_protocol": {"tier": "l1_mechanism", "seeds": SEEDS, "formal_comparison": False,
                      "claim_policy": "synthetic mechanism/interface diagnostics; no pretrained model, official benchmark or production capability claims"},
                  "diagnostic_only": True, "fixture_demo": True, "pretrained_model_calls": 0,
                  "formal_comparison": False, "promotion_eligible": False, "evolve_integrated": False,
                  "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True}
        write(ROOT/result_path, result)
        if device == "cuda":
            receipt_path = f"docs/gpu-validations/{key}-a100-20261021-followup.json"
            runner = next(p for p in hashes if p.startswith("scripts/"))
            receipt = {"schema_version": 1, "adapter_key": key, "validated_at": "2026-10-21",
                       "accelerator": {"vendor": "NVIDIA", "model": raw["accelerator"], "count": 1},
                       "command": ["python", runner, "--device", "cuda", "--seeds", "42,43,44", "--output", "results/followup-cuda.json"],
                       "dataset": dataset, "checkpoint": {"public_id": "none-seeded-component-initialization", "revision": commit, "pretrained": False},
                       "seeds": SEEDS, "result": "passed", "metrics": result["metrics"], "executed_source_sha256": hashes,
                       "provenance": {**provenance, "artifact_path": receipt_path, "metric_artifact_path": result_path.as_posix()},
                       "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
                       "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True}
            write(ROOT/receipt_path, receipt)
            load_gpu_receipt(ROOT/receipt_path)
    write(AUDIT/"frozen-sources.json", proofs)


def source_audit(directory, baseline):
    current_bytes = (directory/"retrieval.json").read_bytes()
    old_bytes = (baseline/"retrieval.json").read_bytes()
    current, old = json.loads(current_bytes), json.loads(old_bytes)
    prior_coverage = json.loads((ROOT/"docs/research-audits/oct21-components/source-coverage.json").read_text())
    require(hashlib.sha256(old_bytes).hexdigest() == prior_coverage["raw_capture_sha256"], "baseline does not match PR217 capture")
    arxiv = [r for r in current if r["kind"] == "arxiv"]
    require({r["source"] for r in arxiv} == {"cs.AI", "cs.CL", "cs.IR", "cs.LG", "cs.CV", "cs.RO", "cs.SD", "eess.AS"}
            and len(arxiv) == 8, "wrong bulletin coverage")
    require(all(r.get("parse_complete") and r["status"] == "retrieved"
                and len(r["records"]) == r["parsed_entries"] == r["expected_entries"] for r in arxiv), "incomplete bulletin capture")
    ids = {r["id"].split("v")[0] for p in arxiv for r in p["records"]}
    previous_ids = {r["id"].split("v")[0] for p in old if p["kind"] == "arxiv" for r in p["records"]}
    deltas = [json.loads((directory/f"{name}-delta.json").read_text()) for name in ("google", "meta", "google-deepmind")]
    for delta in deltas:
        org = delta["organization"]
        pages = [p for p in current if p["kind"] == "official" and p["source"] == org]
        require(pages and all(p["status"] == "retrieved" for p in pages), "unavailable official page cannot certify zero delta")
        prior_urls = {r["url"] for p in old if p["kind"] == "official" and p["source"] == org for r in p["records"]}
        urls = {r["url"] for p in pages for r in p["records"]}
        require({r["url"] for r in delta["new_directory_urls"]} == urls-prior_urls, "official delta differs from captured records")
        require(delta["unique_records"] == len(urls) and delta["baseline_sha256"] == hashlib.sha256(old_bytes).hexdigest(), "official delta baseline/count mismatch")
    coverage = {"schema_version": 1, "checked_on": "2026-10-21", "scope_kind": "same-bulletin-backlog-followup",
                "raw_capture_sha256": hashlib.sha256(current_bytes).hexdigest(), "baseline_raw_sha256": hashlib.sha256(old_bytes).hexdigest(),
                "baseline": "../oct21-components/source-coverage.json", "all_sources_exhaustive": False,
                "review_watermark_advanced": False, "review_watermark": {"before": "2026-10-15", "after": "2026-10-15"},
                "new_bulletin_identities": sorted(ids-previous_ids), "removed_bulletin_identities": sorted(previous_ids-ids),
                "bulletin_ids_by_category": {p["source"]: [r["id"] for r in p["records"]] for p in arxiv},
                "retrieval_receipts": [{k:v for k,v in p.items() if k != "records"} for p in current],
                "official_directory_deltas": deltas,
                "additional_candidates_not_implemented": [{"id": "2610.28435", "title": "Multimodal Reranking Is a System One Decision",
                    "paper_url": "https://arxiv.org/abs/2610.28435", "status": "outside_fixed_scope_not_review_done",
                    "reason": "Identity noticed in the same bulletin; not part of the fixed six-paper delivery, no implementation or full-text closure claim."}],
                "counts": {"selected_papers": len(set(COMPONENTS) | REFERENCES), "component_only": len(COMPONENTS), "reference_only": len(REFERENCES),
                           "fresh_since_last_scan": len(ids-previous_ids), "historical_backfill": 1,
                           "same_bulletin_recent_backfill": len(COMPONENTS), "unique_bulletin_identities": len(ids),
                           "new_official_urls": sum(len(d["new_directory_urls"]) for d in deltas)},
                "limitations": ["Same daily bulletin as PR217; previously unimplemented papers are not newly published since that scan.",
                                "Official Google29/Meta6/DeepMind9 pages are a bounded directory check, not all-web/full-text exhaustiveness.",
                                "ResidencyRL was first published August7, not October; v1 method reviewed, v2 observed only.",
                                "Full expensive experiments are terminal review DONE, not capability implementations."]}
    write(AUDIT/"source-coverage.json", coverage)
    index = records()
    rows = []
    for key in sorted(set(COMPONENTS) | REFERENCES):
        record = index[key]
        component = key in COMPONENTS
        rows.append({"key": key, "domain": record["domain"], "title": record["title"], "paper_url": record["paper_url"],
                     "detail_path": record["detail_path"], "published_at": record["published_at"], "priority": record["priority"],
                     "component_implemented": component, "implementation_status": record["implementation_status"],
                     "review_done": True, "full_experiment_status": "not_reproduced_high_cost",
                     "intake_class": "historical-backfill" if key == "residency-rl" else "same-bulletin-recent-backfill",
                     "automatic_retry": False, "automatic_implementation_queue": False,
                     "cost_assessment": {"source_url": record["paper_url"], "scale": COSTS[key],
                                         "available_resource": "One NVIDIA A100 or A30, or local Mac", "basis": "paper configuration, not local runtime measurement"}})
    write(AUDIT/"task-scope.json", {"schema_version": 1, "batch": BATCH, "papers": rows})
    ledger_path = ROOT/"docs/paper-discovery-ledger.json"
    ledger = json.loads(ledger_path.read_text())
    batch = {"batch": BATCH, "date": "2026-10-21", "scope_kind": "same-bulletin-followup", "counts": coverage["counts"],
             "source_artifact": "research-audits/oct21-followup/README.md", "review_watermark_advanced": False, "all_sources_exhaustive": False,
             "candidates": [{**r, "id": r["paper_url"].split("/abs/")[-1].split("v")[0], "doc": r["detail_path"],
                             "catalog_key": r["key"], "catalog_detail": r["detail_path"],
                             "track": {"agent-research": "agent", "post-training": "post-training", "foundation-models": "foundation-model"}[r["domain"]],
                             "status": "implemented" if r["component_implemented"] else "deferred",
                             "full_text_review": {"scope": "full-text", "read_scope": "Defining method, experimental configuration, code availability and key figure; not the whole article", "full_article_read": False},
                             "source_provenance": [{"source_url": r["paper_url"], "source_kind": "primary-method-and-cost-review", "organization": index[r["key"]]["first_author_affiliation"]}],
                             "resolution": "bounded_component_implemented_full_experiment_not_reproduced_high_cost" if r["component_implemented"] else "not_reproduced_high_cost",
                             "reason": "低成本公式/控制器组件已实跑；完整实验成本过高，不复现（审查 DONE）。" if r["component_implemented"] else "成本过高，不复现（审查 DONE）。"} for r in rows]}
    ledger["batches"] = [b for b in ledger["batches"] if b["batch"] != BATCH] + [batch]
    write(ledger_path, ledger)


def validate_receipt_binding(key, receipt, result, result_path):
    p = result["provenance"]
    require(receipt["adapter_key"] == key, "GPU paper key mismatch")
    require(receipt["seeds"] == result["seeds"] == SEEDS, "GPU seeds mismatch")
    require(receipt["dataset"] == result["dataset"], "GPU dataset mismatch")
    require(receipt["provenance"]["commit"] == p["commit"], "GPU commit mismatch")
    require(receipt["executed_source_sha256"] == receipt["provenance"]["executed_source_sha256"] == p["executed_source_sha256"], "GPU source mismatch")
    require(receipt["provenance"]["metric_artifact_path"] == result_path.as_posix(), "GPU metric path mismatch")
    require(receipt["provenance"]["raw_runner_artifact_sha256"] == p["raw_runner_artifact_sha256"], "GPU raw artifact mismatch")
    require(receipt["metrics"] == result["metrics"] and receipt["result"] == "passed", "GPU metrics mismatch")


def check():
    index = records()
    proofs = json.loads((AUDIT/"frozen-sources.json").read_text())
    for key, device in COMPONENTS.items():
        row = index[key]
        result = json.loads((ROOT/metric_path(row, device)).read_text())
        require(result["diagnostic_only"] and not result["promotion_eligible"] and not result["evolve_integrated"], "claim boundary")
        require(result["metrics"] == aggregate(result["per_seed"]), "aggregate mismatch")
        require(all(r["checks"] and all(v is True for v in r["checks"].values()) for r in result["per_seed"]), "failed check")
        p = result["provenance"]
        proof = proofs["commits"][p["commit"]]["proof"]
        verify_sources(ROOT, p["commit"], p["executed_source_sha256"], {**proof, "paths": sorted(p["executed_source_sha256"])})
        if device == "cuda":
            receipt = load_gpu_receipt(ROOT/row["gpu_validation_artifact"])
            validate_receipt_binding(key, receipt, result, metric_path(row, device))
    print("Five follow-up component evidence contracts passed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path)
    parser.add_argument("--capture", type=Path)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.inputs:
        curate(json.loads(args.inputs.read_text()))
    if args.capture:
        require(args.baseline is not None, "baseline capture required")
        source_audit(args.capture, args.baseline)
    if args.check or args.inputs:
        check()
