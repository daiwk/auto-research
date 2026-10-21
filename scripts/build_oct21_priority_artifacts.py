"""Curate source-bound affordable diagnostics and honest bounded scan receipts."""
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
from build_oct21_followup_artifacts import validate_receipt_binding  # noqa: E402

AUDIT = ROOT / "docs/research-audits/oct21-priority-backfill"
COMPONENTS = {"spec-driven-tests": "cpu", "mice": "cuda", "flint": "cuda", "system-one-rerank": "cuda"}
MODULES = {"spec-driven-tests": "src/auto_research/agent_research/spec_driven_tests.py",
           "mice": "src/auto_research/multimodal/mice.py", "flint": "src/auto_research/foundation_models/flint.py",
           "system-one-rerank": "src/auto_research/multimodal/system_one_rerank.py"}
SEEDS = [42, 43, 44]
COSTS = {
    "spec-driven-tests": "90 Google-private defects, five runs per arm with Gemini3 Flash plus Gemini3.1 Pro judging and private build environments.",
    "mice": "4B/9B/12B/32B image-editor backbone matrix and full multi-instance editing evaluation; no complete generator/checkpoint experiment.",
    "flint": "267K-step MS MARCO training, original four-GPU setup and million-document PLAID campaign; no trained retrieval benchmark.",
    "system-one-rerank": "27B VLM, top16 multi-image context up to64K,14,419 choice requests on H200; no full benchmark or decision tuning.",
}


def records():
    index = {r["key"]: r for r in catalog_records()}
    require(COMPONENTS.keys() <= index.keys(), "missing selected component")
    return index


def metric_path(row, device):
    return Path("docs") / Path(row["detail_path"]).parent / "metrics" / f"component-{device}-seeds42-44.json"


def curate(inputs):
    index, proofs = records(), {"schema_version": 1, "commits": {}}
    require(set(inputs) == set(COMPONENTS), "exact fixed scope required")
    for key, device in COMPONENTS.items():
        raw_bytes = Path(inputs[key]).read_bytes()
        raw = json.loads(raw_bytes)
        require(raw["device"] == device and raw["seeds"] == SEEDS and raw["diagnostic_only"] is True, "wrong run boundary")
        require(device != "cuda" or any(gpu in raw["accelerator"] for gpu in ("A100", "A30")), "real supported CUDA required")
        rows = raw["components"][key]["per_seed"]
        require(all(r.get("checks") and all(v is True for v in r["checks"].values()) for r in rows), "defining checks failed")
        hashes, commit = raw["source_sha256"], raw["code_commit"]
        require({"scripts/run_oct21_priority_backfill.py", MODULES[key]} <= hashes.keys(), "missing executed component source")
        for path, expected in hashes.items():
            require(hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == expected, "executed source changed")
        # This checks the actual committed Git blobs, not the runner's asserted commit.
        proof = capture_sources(ROOT, commit, hashes)
        verify_sources(ROOT, commit, hashes, proof)
        prior = proofs["commits"].get(commit, {}).get("executed_source_sha256", {})
        merged = {**prior, **hashes}
        proofs["commits"][commit] = {"executed_source_sha256": merged, "proof": capture_sources(ROOT, commit, merged)}
        result_path = metric_path(index[key], device)
        dataset = {"id": f"synthetic:oct21-priority-{key}-v1", "revision": "sha256:"+digest(hashes),
                   "capability_benchmark": False, "recipe": "source-frozen-generated-interface-inputs"}
        provenance = {"commit": commit, "artifact_path": result_path.as_posix(),
            "raw_runner_artifact_sha256": hashlib.sha256(raw_bytes).hexdigest(), "executed_source_sha256": hashes,
            "dataset_fingerprint": "sha256:"+digest({"dataset": dataset, "source": hashes, "seeds": SEEDS}),
            "accelerator": raw["accelerator"]}
        checkpoint = raw["checkpoint"] if key == "system-one-rerank" else {
            "public_id": "none-seeded-component-initialization", "revision": commit, "pretrained": False}
        result = {"schema_version": 2, "method": key, "manifest_ref": index[key]["domain"]+":"+key,
            "seeds": SEEDS, "dataset": dataset, "checkpoint": checkpoint, "per_seed": rows,
            "metrics": aggregate(rows), "provenance": provenance, "evaluation_tier": "l1_mechanism",
            "evaluation_protocol": {"tier": "l1_mechanism", "seeds": SEEDS, "formal_comparison": False,
                "claim_policy": "component/interface diagnostics only; generated inputs are not public benchmark capability evidence"},
            "diagnostic_only": True, "fixture_demo": key != "system-one-rerank", "formal_comparison": False,
            "pretrained_model_calls": sum(r["metrics"].get("vlm_forward_passes", 0) for r in rows) if key == "system-one-rerank" else 0,
            "promotion_eligible": False, "evolve_integrated": False,
            "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True}
        write(ROOT/result_path, result)
        if device == "cuda":
            receipt_path = f"docs/gpu-validations/{key}-a100-20261021-late.json"
            receipt = {"schema_version": 1, "adapter_key": key, "validated_at": "2026-10-21",
                "accelerator": {"vendor": "NVIDIA", "model": raw["accelerator"], "count": 1},
                "command": ["python", "scripts/run_oct21_priority_backfill.py", "--device", "cuda", "--components", ",".join(raw["components"]),
                            "--seeds", "42,43,44", "--source-commit", commit, "--output", "results/priority-cuda.json"],
                "dataset": dataset, "checkpoint": checkpoint, "seeds": SEEDS, "result": "passed",
                "metrics": result["metrics"], "executed_source_sha256": hashes,
                "provenance": {**provenance, "artifact_path": receipt_path, "metric_artifact_path": result_path.as_posix()},
                "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
                "full_experiment_status": "not_reproduced_high_cost"}
            if key == "system-one-rerank":
                receipt["command"] += ["--checkpoint", "<public-checkpoint-cache>", "--checkpoint-id", checkpoint["public_id"],
                                       "--checkpoint-revision", checkpoint["revision"]]
            write(ROOT/receipt_path, receipt)
            load_gpu_receipt(ROOT/receipt_path)
    write(AUDIT/"frozen-sources.json", proofs)


def source_audit(directory):
    raw_bytes = (directory/"retrieval.json").read_bytes()
    raw = json.loads(raw_bytes)
    baseline = json.loads((ROOT/"docs/research-audits/oct21-followup/source-coverage.json").read_text())
    arxiv = [p for p in raw if p["kind"] == "arxiv"]
    require(len(arxiv) == 8 and all(p.get("parse_complete") for p in arxiv), "complete eight-category receipts required")
    ids = {r["id"].split("v")[0] for p in arxiv for r in p["records"]}
    old_ids = {identity.split("v")[0] for values in baseline["bulletin_ids_by_category"].values() for identity in values}
    deltas = []
    for name in ("google", "meta", "google-deepmind"):
        delta = json.loads((directory/f"{name}-delta.json").read_text())
        require(delta["baseline_sha256"] == baseline["raw_capture_sha256"], "wrong official baseline")
        if delta["retrieved_pages"] < delta["attempted_pages"]:
            delta.update(status="source_unavailable_not_zero_delta", new_directory_urls=None, changed_records=None)
        else:
            delta["status"] = "bounded_directory_difference_checked"
        deltas.append(delta)
    coverage = {"schema_version": 1, "checked_on": "2026-10-21", "scope_kind": "bounded-priority-backfill",
        "raw_capture_sha256": hashlib.sha256(raw_bytes).hexdigest(), "baseline": "../oct21-followup/source-coverage.json",
        "baseline_raw_sha256": baseline["raw_capture_sha256"], "all_sources_exhaustive": False,
        "review_watermark_advanced": False, "review_watermark": {"before": "2026-10-15", "after": "2026-10-15"},
        "new_bulletin_identities": sorted(ids-old_ids), "removed_bulletin_identities": sorted(old_ids-ids),
        "bulletin_ids_by_category": {p["source"]: [r["id"] for r in p["records"]] for p in arxiv},
        "retrieval_receipts": [{k:v for k,v in p.items() if k != "records"} for p in raw],
        "official_directory_deltas": deltas,
        "counts": {"selected_papers": 4, "component_only": 4, "fresh_since_last_scan": len(ids-old_ids),
                   "historical_backfill": 2, "same_bulletin_backfill": 2, "unique_bulletin_identities": len(ids)},
        "cross_year_review": {"source": "https://research.google/pubs/", "scope": "unfiltered first page plus three future-venue entries; not all pages",
            "excluded": [
                {"title": "3D Scene Graphs", "url": "https://arxiv.org/abs/2606.19383", "reason": "June survey, no defining algorithm"},
                {"title": "When Android Apps Request Location with a Reason", "url": "https://research.google/pubs/when-android-apps-request-location-with-a-reason-a-developer-study-and-user-behavior-experiment/", "reason": "privacy UI user study, outside model-algorithm scope"},
                {"title": "Agentic AI in Enterprise Systems", "url": "https://research.google/pubs/agentic-ai-in-enterprise-systems-a-systematic-review-of-human-in-the-loop-governance-and-autonomous-workflow-control/", "reason": "survey, no defining algorithm"}]},
        "outside_fixed_scope_not_review_done": ["2610.27195"],
        "limitations": ["Same October21 arXiv bulletin, not four newly published papers since PR218.",
            "Google filtered directory and Meta timed out; empty results do not certify no new papers.",
            "DeepMind265 bounded directory entries unchanged; neither whole-web nor all-paper full-text exhaustion claimed.",
            "Two Google-associated historical papers are backfill; affordable components are not full-paper replications."]}
    write(AUDIT/"source-coverage.json", coverage)
    index = records()
    rows = [{"key": key, "domain": index[key]["domain"], "title": index[key]["title"], "paper_url": index[key]["paper_url"],
             "detail_path": index[key]["detail_path"], "published_at": index[key]["published_at"], "priority": index[key]["priority"],
             "implementation_status": "component_only", "review_done": True, "component_implemented": True,
             "intake_class": "historical-backfill" if key in {"mice", "spec-driven-tests"} else "same-bulletin-recent-backfill",
             "automatic_retry": False, "automatic_implementation_queue": False,
             "full_experiment_status": "not_reproduced_high_cost",
             "cost_assessment": {"source_url": index[key]["paper_url"], "scale": COSTS[key], "basis": "paper configuration, not measured full-run time"}}
            for key in COMPONENTS]
    write(AUDIT/"task-scope.json", {"schema_version": 1, "batch": "2026-10-21-priority-backfill", "papers": rows})
    ledger_path = ROOT/"docs/paper-discovery-ledger.json"
    ledger = json.loads(ledger_path.read_text())
    batch = {"batch": "2026-10-21-priority-backfill", "date": "2026-10-21", "scope_kind": "bounded-priority-backfill",
        "source_artifact": "research-audits/oct21-priority-backfill/README.md", "counts": coverage["counts"],
        "review_watermark_advanced": False, "all_sources_exhaustive": False,
        "candidates": [{**r, "id": r["paper_url"].split("/abs/")[-1].split("v")[0], "doc": r["detail_path"],
            "catalog_key": r["key"], "catalog_detail": r["detail_path"], "status": "implemented",
            "track": {"agent-research": "agent", "foundation-models": "foundation-model", "multimodal-models": "multimodal"}[r["domain"]],
            "full_text_review": {"scope": "full-text", "read_scope": "defining method, cost configuration, code availability and key figure", "full_article_read": False},
            "source_provenance": [{"source_url": r["paper_url"], "source_kind": "primary-method-and-cost-review",
                                   "organization": index[r["key"]]["first_author_affiliation"]}],
            "resolution": "bounded_component_implemented_full_experiment_not_reproduced_high_cost",
            "reason": "低成本组件与接口已验证；完整实验成本过高，不复现（审查 DONE）。"} for r in rows]}
    ledger["batches"] = [b for b in ledger["batches"] if b["batch"] != batch["batch"]] + [batch]
    write(ledger_path, ledger)


def validate_binding(key, receipt, result, path):
    validate_receipt_binding(key, receipt, result, path)
    require(receipt["checkpoint"] == result["checkpoint"], "GPU checkpoint mismatch")
    require(receipt["accelerator"]["model"] == result["provenance"]["accelerator"], "GPU accelerator mismatch")
    require(receipt["provenance"]["dataset_fingerprint"] == result["provenance"]["dataset_fingerprint"], "GPU dataset fingerprint mismatch")


def validate_result(key, result):
    require(result["evaluation_tier"] == result["evaluation_protocol"]["tier"] == "l1_mechanism"
            and result["formal_comparison"] is False and result["evaluation_protocol"]["formal_comparison"] is False
            and result["diagnostic_only"] is True and result["promotion_eligible"] is False
            and result["evolve_integrated"] is False and result["full_experiment_status"] == "not_reproduced_high_cost"
            and result["full_experiment_review_done"] is True, "diagnostic claim boundary mismatch")
    hashes, p = result["provenance"]["executed_source_sha256"], result["provenance"]
    dataset = {"id": f"synthetic:oct21-priority-{key}-v1", "revision": "sha256:"+digest(hashes),
               "capability_benchmark": False, "recipe": "source-frozen-generated-interface-inputs"}
    require(result["dataset"] == dataset and result["seeds"] == SEEDS, "dataset identity/recipe/seeds mismatch")
    require(p["dataset_fingerprint"] == "sha256:"+digest({"dataset": dataset, "source": hashes, "seeds": SEEDS}), "dataset fingerprint mismatch")
    require({"scripts/run_oct21_priority_backfill.py", MODULES[key]} <= hashes.keys(), "missing executed component source")
    if key == "system-one-rerank":
        checkpoint = result["checkpoint"]
        require(checkpoint["public_id"] == "HuggingFaceTB/SmolVLM-256M-Instruct"
                and checkpoint["revision"] == "7e3e67edbbed1bf9888184d9df282b700a323964"
                and checkpoint["files_sha256"]["model.safetensors"] == "74dea5904032e5ae99a2e0eef5179e6ac0f1dedc3ab0c7c2a5d4d387c843203e",
                "public checkpoint identity/revision/content mismatch")
        require(result["pretrained_model_calls"] == 3 and all(r["metrics"]["vlm_forward_passes"] == 1 for r in result["per_seed"]), "real VLM forward count mismatch")


def check():
    proofs, index = json.loads((AUDIT/"frozen-sources.json").read_text()), records()
    for key, device in COMPONENTS.items():
        path = metric_path(index[key], device)
        result = json.loads((ROOT/path).read_text())
        validate_result(key, result)
        require(result["diagnostic_only"] and not result["promotion_eligible"] and not result["evolve_integrated"], "claim boundary")
        require(result["metrics"] == aggregate(result["per_seed"]), "aggregate mismatch")
        require(all(r["checks"] and all(v is True for v in r["checks"].values()) for r in result["per_seed"]), "failed checks")
        p = result["provenance"]
        proof = proofs["commits"][p["commit"]]["proof"]
        verify_sources(ROOT, p["commit"], p["executed_source_sha256"], {**proof, "paths": sorted(p["executed_source_sha256"])})
        if device == "cuda":
            receipt = load_gpu_receipt(ROOT/index[key]["gpu_validation_artifact"])
            validate_binding(key, receipt, result, path)
    print("Four source-bound priority-backfill evidence contracts passed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path)
    parser.add_argument("--capture", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.inputs:
        curate(json.loads(args.inputs.read_text()))
    if args.capture:
        source_audit(args.capture)
    if args.check or args.inputs:
        check()
