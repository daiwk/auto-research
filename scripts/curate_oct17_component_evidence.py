#!/usr/bin/env python3
"""Curate actual bounded runner outputs; reject stale sources and missing trials.

This tool never generates experiment scores. CUDA admission requires the real
device identity plus the current frozen algorithm/runner hashes. All resulting
cards remain L1 diagnostics, not capability or full-paper reproductions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import statistics

ROOT = Path(__file__).resolve().parents[1]
GROUPS = {
    "foundation": ("foundation-models", "foundation_models", (
        ("drop-kv", "2610.22130"), ("mirror-moe", "2610.22353"),
        ("bit-sparse", "2610.22256"), ("lct", "2610.22179"), ("roleq", "2610.21808"),
    )),
    "post": ("post-training", "post_training", (
        ("shared-residual-distillation", "2610.22080"), ("progress-reward", "2610.22056"),
        ("elite-replay", "2610.22290"), ("clean-rm", "2610.21138"),
    )),
}
SEEDS = [42, 43, 44]


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def finite_tree(value):
    if isinstance(value, float):
        require(math.isfinite(value), "nonfinite measured metric")
    elif isinstance(value, dict):
        for item in value.values():
            finite_tree(item)
    elif isinstance(value, list):
        for item in value:
            finite_tree(item)


def reject_explicit_failure(value):
    if not isinstance(value, dict):
        return
    for field in ("status", "result"):
        state = value.get(field)
        require(not isinstance(state, str) or state.lower() not in {
            "failed", "failure", "error", "partial", "skipped", "cancelled", "canceled", "timeout",
        }, f"explicit {field} failure cannot be admitted")
    require(not value.get("error") and not value.get("errors"), "nonempty error cannot be admitted")


def average(rows):
    result = {}
    fields = set(rows[0]["metrics"])
    require(all(set(row["metrics"]) == fields for row in rows), "per-seed metric fields differ")
    for name in sorted(fields):
        values = [row["metrics"][name] for row in rows]
        if all(isinstance(value, bool) for value in values):
            result[name] = all(values)
        elif all(type(value) in (int, float) for value in values):
            result[name] = {"mean": statistics.mean(values), "std": statistics.stdev(values), "n": len(values)}
        else:
            require(all(value == values[0] for value in values), f"non-scalar metric differs: {name}")
            result[name] = values[0]
    return result


def validate_measurement(key, measured):
    """Recheck defining execution outcomes, not just runner-provided pass labels."""
    upper = {
        "drop-kv": {"singleton_removal_reference_max_error": 1e-10},
        "mirror-moe": {"manual_aggregation_max_error": 1e-10},
        "bit-sparse": {"forward_max_error": 1e-10, "backward_max_error": 1e-10},
        "roleq": {"bruteforce_global_optimum_loss_gap": 1e-10,
                  "writer_equals_transposed_reader_max_error": 1e-10},
        "shared-residual-distillation": {"reference_max_abs_error": 1e-7,
                  "teacher_delta_l2": 0., "identical_peer_negative_control_error": 1e-12},
        "progress-reward": {"literal_equation_max_abs_error": 1e-12,
                  "terminal_telescoping_abs_error": 1e-12, "subtask_embedding_max_abs_error": 1e-12},
        "elite-replay": {"replay_reference_max_abs_error": 1e-10,
                  "frozen_base_delta_l2": 0., "question_sampling_count_gap": 0},
        "clean-rm": {"exact_ot_reference_abs_error": 1e-12,
                  "transport_marginal_max_abs_error": 1e-12,
                  "noise_estimator_delta_during_reward_phase_l2": 0.,
                  "zero_noise_negative_control_abs_error": 1e-12},
    }
    positive = {
        "drop-kv": ("query_gradient_norm", "key_gradient_norm", "value_gradient_norm",
                    "attention_only_negative_control_difference"),
        "mirror-moe": ("router_gradient_norm", "router_update_norm", "mixed_weight_negative_control_error"),
        "lct": ("overflow_raw_tail_bytes",),
        "roleq": ("actual_packed_code_bits", "actual_scale_bits"),
        "shared-residual-distillation": ("parameter_delta_l2", "gradient_norm_min", "shared_residual_mean_abs"),
        "progress-reward": ("parameter_delta_l2", "gradient_norm_min", "nonterminal_boundary_negative_control_gap"),
        "elite-replay": ("parameter_delta_l2", "gradient_norm_min", "new_cells_from_directed_search",
                         "rejected_mutation_candidates"),
        "clean-rm": ("noise_estimator_delta_l2", "reward_parameter_delta_l2", "noise_gradient_norm_min",
                     "reward_gradient_norm_min", "nondegenerate_margin_min", "corrected_vs_naive_parameter_l2"),
    }
    truth = {
        "drop-kv": ("recent_window_protected",),
        "mirror-moe": ("zero_ratio_recovers_topk",),
        "bit-sparse": ("bf16_bitwise_roundtrip",),
        "lct": ("all_bf16_exponents_bitwise_roundtrip", "roomy_buffer_roundtrip", "autograd_matches_dense"),
    }
    for field, bound in upper.get(key, {}).items():
        value = measured.get(field)
        require(type(value) in (int, float) and 0 <= value <= bound, f"{key}: {field} exceeds {bound}")
    for field in positive.get(key, ()):
        value = measured.get(field)
        require(type(value) in (int, float) and value > 0, f"{key}: {field} must be positive")
    for field in truth.get(key, ()):
        require(measured.get(field) is True, f"{key}: {field} failed")
    if key == "elite-replay":
        require(measured.get("verified_archive_fraction") == 1., "elite replay admitted unverified archives")
        require(measured.get("unrepresentable_ratio_rejected") is True, "elite replay overflow guard missing")
    if key == "bit-sparse":
        require(measured.get("nonfinite_input_rejection_cases") == 3, "BitSparse finite-input guards missing")
    if key == "roleq":
        require(measured.get("extreme_scale_invariance_cases") == 4, "RoleQ extreme-scale support checks missing")
    if key in {"shared-residual-distillation", "progress-reward", "elite-replay"}:
        require(measured.get("optimizer_updates") == 4, f"{key}: fixed four-step budget differs")
    if key == "clean-rm":
        require(measured.get("noise_optimizer_updates") == 4 and measured.get("reward_optimizer_updates") == 4,
                "CleanRM: both estimator and reward phases must execute")


def validate(payload, group):
    reject_explicit_failure(payload)
    domain, module, items = GROUPS[group]
    require(payload.get("device") == "cuda", "CUDA evidence must not be CPU fallback")
    accelerator = payload.get("accelerator", "")
    require("NVIDIA" in accelerator.upper() and any(x in accelerator.upper() for x in ("A100", "A30")),
            "expected real NVIDIA A100/A30")
    require(payload.get("diagnostic_only") is True and payload.get("promotion_eligible") is False,
            "diagnostic boundary missing")
    require(payload.get("seeds") == SEEDS, "exact three fixed seeds required")
    require(re.fullmatch(r"[0-9a-f]{40}", payload.get("code_commit", "")), "frozen Git commit missing")
    sources = {f"src/auto_research/{module}/{key.replace('-', '_')}.py" for key, _ in items}
    sources.add(f"scripts/run_oct17_{group}_components.py")
    hashes = payload.get("executed_source_sha256", {})
    require(set(hashes) == sources, "executed source coverage differs")
    for name, digest in hashes.items():
        require((ROOT / name).is_file(), f"source missing: {name}")
        require(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, f"stale executed source: {name}")
    require(set(payload.get("components", {})) == {key for key, _ in items}, "component coverage differs")
    for key, _ in items:
        component = payload["components"][key]
        reject_explicit_failure(component)
        require(component.get("dataset", {}).get("id") and component["dataset"].get("revision"), f"{key}: input identity missing")
        rows = component.get("per_seed", [])
        require([row.get("seed") for row in rows] == SEEDS, f"{key}: per-seed coverage differs")
        require(all(row.get("metrics") for row in rows), f"{key}: measured metrics missing")
        finite_tree(rows)
        for row in rows:
            reject_explicit_failure(row)
            validate_measurement(key, row["metrics"])
        average(rows)
    return domain, module, items


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def curate(path: Path, group: str):
    payload = json.loads(path.read_text())
    domain, module, items = validate(payload, group)
    raw_sha = hashlib.sha256(path.read_bytes()).hexdigest()
    for key, identity in items:
        component = payload["components"][key]
        metric_path = f"docs/{domain}/{identity}-{key}/metrics/component-cuda-seeds42-44.json"
        receipt_path = f"docs/gpu-validations/{key}-a100-20261017.json"
        sources = {name: digest for name, digest in payload["executed_source_sha256"].items()
                   if name.endswith(f"/{key.replace('-', '_')}.py") or name.startswith("scripts/")}
        metrics = average(component["per_seed"])
        dataset = component["dataset"]
        checkpoint = {"public_id": "none-seeded-independent-mechanism-initialization",
                      "revision": payload["code_commit"], "pretrained": False, "initialization_seeds": SEEDS}
        provenance = {"commit": payload["code_commit"], "artifact_path": metric_path,
                      "dataset_fingerprint": f"{dataset['id']}@{dataset['revision']};seeds=42,43,44",
                      "raw_runner_artifact_sha256": raw_sha, "executed_source_sha256": sources,
                      "accelerator": payload["accelerator"]}
        common = {"diagnostic_only": True, "promotion_eligible": False,
                  "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True}
        metric = {"schema_version": 2, "method": key, "manifest_ref": f"{domain}:{key}",
                  "seeds": SEEDS, "dataset": dataset, "evaluation_tier": "l1_mechanism",
                  "evaluation_protocol": {"tier": "l1_mechanism", "seeds": SEEDS, "formal_comparison": False,
                                          "claim_policy": "independent bounded operator diagnostic, not full paper or model capability"},
                  "metrics": metrics, "per_seed": component["per_seed"], "provenance": provenance, **common}
        command = ["python", f"scripts/run_oct17_{group}_components.py", "--device", "cuda",
                   "--seeds", "42,43,44", "--code-commit", payload["code_commit"],
                   "--output", f"runs/oct17-components/{group}.json"]
        receipt = {"schema_version": 1, "adapter_key": key, "validated_at": "2026-10-17",
                   "accelerator": {"vendor": "NVIDIA", "model": payload["accelerator"]},
                   "command": command, "seeds": SEEDS, "dataset": dataset, "checkpoint": checkpoint,
                   "result": "passed", "metrics": metrics, "executed_source_sha256": sources,
                   "provenance": {**provenance, "artifact_path": receipt_path, "metric_artifact_path": metric_path}, **common}
        write(ROOT / metric_path, metric)
        write(ROOT / receipt_path, receipt)


def curate_cpu(path: Path, *, write_outputs: bool = True):
    payload = json.loads(path.read_text())
    reject_explicit_failure(payload)
    require(payload.get("device") == "cpu" and payload.get("executed_source_uncommitted") is False,
            "CPU execution must use committed sources, without CUDA claims")
    require(payload.get("diagnostic_only") is True and payload.get("promotion_eligible") is False,
            "CPU diagnostic boundary missing")
    require(payload.get("seeds") == SEEDS, "CPU fixed seed coverage differs")
    require(re.fullmatch(r"[0-9a-f]{40}", payload.get("code_commit", "")), "CPU execution commit missing")
    items = (("shortcut-sensitivity", "2610.22243"), ("disagreement-routing", "2610.22245"),
             ("tracer", "2610.21267"))
    sources = {f"src/auto_research/agent_research/{key.replace('-', '_')}.py" for key, _ in items}
    sources.add("scripts/run_oct17_agent_components.py")
    hashes = payload.get("executed_source_sha256", {})
    require(set(hashes) == sources, "CPU executed source coverage differs")
    for name, digest in hashes.items():
        require(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, f"stale CPU source: {name}")
    require(set(payload.get("components", {})) == {key for key, _ in items}, "CPU component coverage differs")
    outputs = []
    for key, identity in items:
        component = payload["components"][key]
        reject_explicit_failure(component)
        rows = component.get("per_seed", [])
        require([row.get("seed") for row in rows] == SEEDS, f"{key}: CPU seed coverage differs")
        for row in rows:
            reject_explicit_failure(row)
        finite_tree(component)
        dataset = component["dataset"]
        require(dataset.get("id") and dataset.get("revision"), f"{key}: CPU input identity missing")
        metrics = average(rows)
        if key == "shortcut-sensitivity":
            deterministic = component["deterministic"]
            require(deterministic.get("repetitions") == 1, "deterministic audit must not fabricate seed repetitions")
            fixed = deterministic["metrics"]
            require(fixed["rows"] == 1220 and fixed["agentharm_rows"] == 731 and fixed["agentharm_interactions"] == 197,
                    "Shortcut public audit denominators differ")
            require(fixed["independent_reference_prediction_errors"] == 0 and fixed["dropped_rows"] == 0 and
                    fixed["new_guard_calls"] == 0, "Shortcut reference/isolation audit failed")
            require(len(dataset.get("artifacts", [])) == 8, "Shortcut fixed source identities missing")
            metrics.update(fixed)
        elif key == "disagreement-routing":
            for row in rows:
                measured = row["metrics"]
                require(measured["response_probe_bce_final"] < measured["response_probe_bce_initial"] and
                        measured["prompt_probe_bce_final"] < measured["prompt_probe_bce_initial"], "probe fit did not execute")
                require(measured["independent_target_max_absolute_error"] < 1e-12 and
                        measured["validation_routed_fraction"] <= .25, "routing formula/calibration failed")
                require(row["calibration"]["split"] == "validation" and row["calibration"]["test_prompts"] == 24,
                        "routing calibration accessed a different split")
        else:
            for row in rows:
                measured = row["metrics"]
                require(measured["parameter_delta_l2"] > 0 and measured["final_crossfit_nll"] < measured["initial_crossfit_nll"],
                        "TRACER blend fit did not execute")
                require(measured["retained_test_fraction"] == 1 and measured["unseen_prefix_fallback_checked"] == 1,
                        "TRACER fallback/denominator failed")
                require(row["training_protocol"]["train_trajectories"] == 40 and
                        row["training_protocol"]["test_trajectories"] == 20, "TRACER trajectory split differs")
        relative = f"docs/agent-research/{identity}-{key}/metrics/component-cpu-seeds42-44.json"
        source_hashes = {name: digest for name, digest in hashes.items()
                         if name.startswith("scripts/") or name.endswith(f"/{key.replace('-', '_')}.py")}
        result = {"schema_version": 2, "method": key, "manifest_ref": f"agent-research:{key}",
                  "seeds": SEEDS, "device": "cpu", "dataset": dataset, "metrics": metrics, "per_seed": rows,
                  "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
                  "evaluation_tier": "l1_mechanism",
                  "evaluation_protocol": {**payload["evaluation_protocol"], "seeds": SEEDS},
                  "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True,
                  "provenance": {"commit": payload["code_commit"], "artifact_path": relative,
                                 "executed_source_sha256": source_hashes,
                                 "raw_runner_artifact_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                                 "dataset_fingerprint": hashlib.sha256(json.dumps(dataset, sort_keys=True).encode()).hexdigest()}}
        for field in ("deterministic", "isolation"):
            if field in component:
                result[field] = component[field]
        outputs.append((relative, result))
    if write_outputs:
        for relative, result in outputs:
            write(ROOT / relative, result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--foundation", type=Path, required=True)
    parser.add_argument("--post", type=Path, required=True)
    parser.add_argument("--agent", type=Path)
    args = parser.parse_args()
    # Validate every input before writing any receipt; no partially admitted batch.
    for group, path in (("foundation", args.foundation), ("post", args.post)):
        validate(json.loads(path.read_text()), group)
    if args.agent:
        curate_cpu(args.agent, write_outputs=False)
    curate(args.foundation, "foundation")
    curate(args.post, "post")
    if args.agent:
        curate_cpu(args.agent)
