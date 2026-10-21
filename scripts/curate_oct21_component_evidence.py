#!/usr/bin/env python3
"""Admit actual Oct21 bounded diagnostics and keep portable frozen-source proof."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from auto_research.paper_specs.catalog import catalog_records  # noqa: E402
from auto_research.gpu_validation import load_gpu_receipt  # noqa: E402
from oct18_frozen_sources import capture_sources, verify_sources  # noqa: E402

AUDIT = ROOT / "docs/research-audits/oct21-components"
SEEDS = [42, 43, 44]
COMPONENTS = {"baseline-incremental": "cpu", "spar-prefix-balance": "cpu",
              "echo-selector-loss": "cuda", "ap-opd": "cuda", "optd": "cuda",
              "locale-jepa": "cuda", "oo-harness": "cpu", "rpl": "cpu"}
REFERENCES = {"visually-attributable-opd", "cache-engineering", "esc", "aptamer-lab-loop"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+"\n")


def aggregate(rows):
    metrics = {}
    require([r["seed"] for r in rows] == SEEDS, "three fixed seeds required")
    names = set(rows[0]["metrics"])
    require(all(set(row["metrics"]) == names for row in rows), "per-seed metric schema differs")
    for name in sorted(names):
        values = [row["metrics"][name] for row in rows]
        require(all(type(v) in (float, int, bool) and math.isfinite(v) for v in values), "finite scalar metrics required")
        metrics[name] = (all(values) if all(type(v) is bool for v in values) else
                         {"mean": statistics.mean(values), "std": statistics.stdev(values), "n": len(values)})
    return metrics


def gates(key, rows):
    for row in rows:
        m = row["metrics"]
        if key in {"baseline-incremental", "spar-prefix-balance", "echo-selector-loss"}:
            require(row.get("checks") and all(v is True for v in row["checks"].values()), f"{key} failed defining checks")
        elif key in {"ap-opd", "optd"}:
            require(m["optimizer_updates"] == 3 and m["parameter_delta_l2"] > 0 and m["gradient_norm_min"] > 0,
                    "actual policy updates required")
            require(m["loss_reference_max_abs_error"] < 1e-9 and m["logit_gradient_reference_max_abs_error"] < 1e-9,
                    "independent objective/gradient reference failed")
            require(m["negative_control_difference_max"] > 0 and m["teacher_parameter_delta_max"] == 0
                    and m["teacher_gradient_count"] == 0 and m["pretrained_or_public_benchmark_evaluated"] is False,
                    "teacher isolation or diagnostic boundary failed")
            if key == "ap-opd":
                require(m["staircase_original_profile_reference_error"] < 1e-12
                        and m["staircase_recursive_profile_negative_control_difference"] > 0,
                        "original-profile pullback regression failed")
        elif key == "locale-jepa":
            require(m["steps"] == 8 and m["projector_gradient_norm"] > 0
                    and m["collapsed_uniform_ball_penalty"] > 0 and m["effective_clusters"] > 0,
                    "local-ball mechanism was not executed")
        elif key == "oo-harness":
            require(m["observed_guarded_writes"] == m["heldout_fixture_tasks"] == 8
                    and m["removed_guard_control_writes"] == 0 and m["router_private_top_level_fields"] == 0
                    and m["base_reuse_environment_count"] == 1 and m["actual_llm_calls"] == 0,
                    "harness execution/isolation or fixture boundary failed")
        elif key == "rpl":
            require(m["baseline_fixture_support_covered"] == 0 and m["selected_fixture_support_covered"] == 1
                    and m["wide_program_retrieved_candidates"] == 20 and m["wide_program_printed_documents"] == 3
                    and m["continuation_private_top_level_fields"] == 0 and m["incorrect_answer_supervised"] == 0
                    and m["actual_llm_calls"] == 0, "RPL interface boundary failed")


def catalogue():
    records = {r["key"]: r for r in catalog_records()}
    require(set(COMPONENTS) | REFERENCES <= records.keys(), "missing fixed-scope catalog item")
    return records


def normalize(key, raw):
    if key in {"oo-harness", "rpl"}:
        provenance = raw["provenance"]
        require(provenance.get("executed_source_uncommitted") is False, "uncommitted Agent source")
        return raw["per_seed"], provenance["commit"], provenance["executed_source_sha256"]
    rows = (raw["components"][key]["per_seed"] if key in {"ap-opd", "optd"} else
            raw["results"] if key == "locale-jepa" else raw["components"][key])
    return rows, raw["code_commit"], raw.get("source_sha256", raw.get("executed_source_sha256"))


def ingest(paths):
    records = catalogue()
    proofs = {"schema_version": 1, "commits": {}}
    for key, device in COMPONENTS.items():
        path = paths[key]
        raw = json.loads(path.read_text())
        require(raw["device"] == device and raw["seeds"] == SEEDS and raw["diagnostic_only"] is True, "wrong device/seeds/boundary")
        require(device != "cuda" or "A100" in raw["accelerator"] or "A30" in raw["accelerator"], "real supported NVIDIA accelerator required")
        rows, commit, hashes = normalize(key, raw)
        require(hashes and len(commit) == 40, "frozen source provenance required")
        for source, expected in hashes.items():
            require(hashlib.sha256((ROOT/source).read_bytes()).hexdigest() == expected, "executed source changed after run")
        proof = capture_sources(ROOT, commit, hashes)
        previous = proofs["commits"].get(commit)
        all_hashes = {**(previous["executed_source_sha256"] if previous else {}), **hashes}
        proofs["commits"][commit] = {"executed_source_sha256": all_hashes,
                                    "proof": capture_sources(ROOT, commit, all_hashes)}
        verify_sources(ROOT, commit, hashes, proof)
        gates(key, rows)
        metrics = aggregate(rows)
        metric_path = Path("docs") / Path(records[key]["detail_path"]).parent / "metrics" / f"component-{device}-seeds42-44.json"
        dataset = {"id": f"synthetic:oct21-{key}-v1", "revision": "sha256:"+digest(hashes),
                   "capability_benchmark": False, "recipe": "fixed-source-generated-component-inputs-v1"}
        provenance = {"commit": commit, "artifact_path": metric_path.as_posix(),
                      "raw_runner_artifact_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                      "executed_source_sha256": hashes, "accelerator": raw.get("accelerator", "CPU"),
                      "dataset_fingerprint": "sha256:"+digest({"dataset": dataset, "seeds": SEEDS, "source": hashes})}
        result = {"schema_version": 2, "method": key, "manifest_ref": records[key]["domain"]+":"+key,
                  "seeds": SEEDS, "dataset": dataset, "evaluation_tier": "l1_mechanism",
                  "per_seed": [{"seed": r["seed"], "metrics": r["metrics"],
                                "audit_sha256": digest(r), **({"checks": r["checks"]} if "checks" in r else {})} for r in rows],
                  "metrics": metrics, "provenance": provenance,
                  "evaluation_protocol": {"tier": "l1_mechanism", "seeds": SEEDS, "formal_comparison": False,
                    "claim_policy": "synthetic mechanism/interface diagnostics; no pretrained model, official benchmark or production capability claims"},
                  "diagnostic_only": True, "fixture_demo": True, "pretrained_model_calls": 0,
                  "formal_comparison": False, "promotion_eligible": False, "evolve_integrated": False,
                  "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True}
        write(ROOT/metric_path, result)
        if device == "cuda":
            receipt_path = f"docs/gpu-validations/{key}-a100-20261021.json"
            runner = next(p for p in hashes if p.startswith("scripts/"))
            command = ["python", runner, "--device", "cuda", "--seeds", "42,43,44"]
            if key == "echo-selector-loss":
                command += ["--component", key]
            command += ["--output", f"results/{key}-cuda.json"]
            receipt = {"schema_version": 1, "adapter_key": key, "validated_at": "2026-10-21",
                       "accelerator": {"vendor": "NVIDIA", "model": raw["accelerator"], "count": 1},
                       "command": command, "dataset": dataset,
                       "checkpoint": {"public_id": "none-seeded-component-initialization", "revision": commit, "pretrained": False},
                       "seeds": SEEDS, "result": "passed", "metrics": metrics,
                       "executed_source_sha256": hashes,
                       "provenance": {**provenance, "artifact_path": receipt_path,
                                      "metric_artifact_path": metric_path.as_posix()},
                       "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
                       "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True}
            write(ROOT/receipt_path, receipt)
            load_gpu_receipt(ROOT/receipt_path)
    write(AUDIT/"frozen-sources.json", proofs)


def check():
    proofs = json.loads((AUDIT/"frozen-sources.json").read_text())
    for key, device in COMPONENTS.items():
        record = catalogue()[key]
        result = json.loads((ROOT/"docs"/Path(record["detail_path"]).parent/"metrics"/f"component-{device}-seeds42-44.json").read_text())
        require(result["diagnostic_only"] is True and result["promotion_eligible"] is False
                and result["evolve_integrated"] is False and result["formal_comparison"] is False,
                "claim boundary changed")
        gates(key, result["per_seed"])
        require(aggregate(result["per_seed"]) == result["metrics"], "metrics no longer match raw rows")
        provenance = result["provenance"]
        proof = proofs["commits"][provenance["commit"]]["proof"]
        verify_sources(ROOT, provenance["commit"], provenance["executed_source_sha256"],
                       {**proof, "paths": sorted(provenance["executed_source_sha256"])})
        if device == "cuda":
            receipt = load_gpu_receipt(ROOT/record["gpu_validation_artifact"])
            require(receipt["metrics"] == result["metrics"] and receipt["provenance"]["commit"] == provenance["commit"],
                    "GPU receipt and metric evidence differ")
    print("Oct21 eight component evidence contracts passed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--inputs", type=Path, help="JSON map from all eight keys to actual runner artifacts")
    args = parser.parse_args()
    if args.inputs:
        ingest({k: Path(v) for k, v in json.loads(args.inputs.read_text()).items()})
    elif not args.check:
        parser.error("supply actual --inputs or --check")
    check()
