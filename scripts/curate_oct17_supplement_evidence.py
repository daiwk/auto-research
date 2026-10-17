#!/usr/bin/env python3
"""Admit actual bounded supplement outputs, binding frozen/current sources.

This does not run experiments or invent measurements. Four CUDA components
need real A100/A30 execution; seven CPU components/interfaces need actual runs.
All remain mechanism diagnostics, never model/Agent capability comparisons.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import statistics
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SEEDS = [42, 43, 44]
# The runner's short name predates catalog integration. Keep the measured raw
# identity unchanged; do not overwrite the unrelated 2609.08798 `oprd` adapter.
CATALOG_KEYS = {"oprd": "oprd-reminder"}
GROUPS = {
    "foundation": ("cuda", "scripts/run_oct17_supplement_foundation.py", {
        "prism-1": ("foundation-models", "2610.22066", "foundation_models/prism_one"),
        "langdit": ("foundation-models", "2610.22330", "foundation_models/langdit"),
    }),
    "post": ("cuda", "scripts/run_oct17_supplement_post.py", {
        "oprd": ("post-training", "2610.21496", "post_training/reminder_distillation"),
        "opcredit": ("post-training", "2610.21345", "post_training/operation_credit"),
    }),
    "protocols": ("cpu", "scripts/run_oct17_supplement_protocols.py", {
        "structural-signal-retriever": ("agent-research", "2610.21113", "agent_research/structural_signal_retriever"),
        "muon-paired-budget": ("foundation-models", "2610.21555", "foundation_models/muon_paired_budget"),
    }),
    "agent": ("cpu", "scripts/run_oct17_supplement_agent.py", {
        "rsiflow": ("agent-research", "2610.21791", "agent_research/rsi_flow"),
        "leash": ("agent-research", "2610.22280", "agent_research/leash"),
        "probe": ("agent-research", "2610.22124", "agent_research/probe_audit"),
        "terminal-rsi": ("agent-research", "2610.22192", "agent_research/terminal_rsi"),
        "gacc-bench": ("agent-research", "2610.21893", "agent_research/gacc_bench"),
    }),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def reject_failure(value):
    require(isinstance(value, dict), "expected structured result")
    for key in ("status", "result"):
        state = value.get(key)
        require(not isinstance(state, str) or state.lower() not in {
            "failed", "failure", "error", "partial", "skipped", "cancelled", "canceled", "timeout",
        }, f"explicit {key} failure cannot be admitted")
    require(not value.get("error") and not value.get("errors"), "nonempty execution error")


def finite_tree(value):
    if isinstance(value, float):
        require(math.isfinite(value), "nonfinite measured value")
    elif isinstance(value, dict):
        for child in value.values():
            finite_tree(child)
    elif isinstance(value, list):
        for child in value:
            finite_tree(child)


def aggregate(rows):
    fields = set(rows[0]["metrics"])
    require(fields and all(set(row["metrics"]) == fields for row in rows), "per-seed metric schema differs")
    result = {}
    for field in sorted(fields):
        values = [row["metrics"][field] for row in rows]
        if all(isinstance(value, bool) for value in values):
            result[field] = all(values)
        elif all(type(value) in (int, float) for value in values):
            result[field] = {"mean": statistics.mean(values), "std": statistics.stdev(values), "n": len(values)}
        else:
            require(all(value == values[0] for value in values), f"non-scalar metric differs: {field}")
            result[field] = values[0]
    return result


def validate_measurement(key, metrics):
    """Recheck defining measured outcomes rather than trust a success label."""
    upper = {
        "prism-1": {"independent_causal_forward_max_error": 1e-10, "permutation_score_max_error": 1e-10,
                    "original_score_max_error": 1e-10, "renormalized_original_probability_tv": 1e-10},
        "langdit": {"shortcut_independent_reference_max_error": 1e-10,
                    "entropy_gated_bootstrap_max_error": 1e-10, "inference_posterior_mean_max_error": 1e-10},
        "oprd": {"reference_max_abs_error": 1e-10, "teacher_delta_between_refresh_l2": 0,
                 "teacher_gradient_count": 0, "identical_teacher_negative_control_max_abs_kl": 1e-10},
        "opcredit": {"boc_reference_max_abs_error": 1e-10, "ftc_reference_max_abs_error": 1e-10,
                     "loss_reference_max_abs_error": 1e-10, "duplicate_support_negative_control_max_abs_error": 1e-10,
                     "frozen_reference_delta_l2": 0, "unavailable_frontier_negative_control_credit": 0},
        "structural-signal-retriever": {"fullscan_score_max_error": 1e-12, "orchestrator_model_calls": 0},
        "muon-paired-budget": {"analytic_piecewise_auc_max_error": 1e-12,
                               "paired_bootstrap_analytic_ratio_max_error": 1e-12, "full_budget_regret": 0,
                               "actual_model_training_runs": 0},
        "rsiflow": {"independent_final_state_error": 1e-12, "report_feedback_selection_calls": 0},
        "leash": {"independent_quadratic_score_max_error": 1e-10, "test_tasks_in_reference": 0},
        "probe": {"independent_first_repeat_reward_error": 1e-12, "private_marker_exposures": 0,
                  "independent_raw_verifier_hit_count_error": 0, "new_trained_auditors": 0},
        "terminal-rsi": {"independent_expansion_max_error": 1e-10, "exact_chunk_max_error": 1e-10,
                         "skipped_observation_max_error": 1e-10},
        "gacc-bench": {"independent_micro_error": 1e-12, "budget_violations": 0,
                       "cached_repeat_compressor_calls": 0, "question_gold_exposures_to_compressor": 0,
                       "official_cl100k_measurements": 0},
    }
    positive = {
        "prism-1": ("cross_option_attention_negative_control_error", "vocabulary_head_gradient_norm", "vocabulary_head_update_norm"),
        "langdit": ("shortcut_input_gradient_norm", "retained_codebook_input_gradient_norm",
                    "unweighted_sampling_negative_control_difference", "codebook_update_norm", "bidirectional_attention_gradient_norm"),
        "oprd": ("parameter_delta_l2", "gradient_norm_min", "sampled_success_trajectories", "sampled_failure_trajectories"),
        "opcredit": ("parameter_delta_l2", "gradient_norm_min"),
        "rsiflow": ("accepted_candidates", "retained_implementation_failures", "retained_skill_records"),
        "leash": ("shadow_probes", "shadow_interventions"),
        "terminal-rsi": ("reset_trace_negative_control_max_error",),
    }
    truth = {
        "langdit": ("explicit_shortcut_codebook_gradient_absent",),
        "oprd": ("student_context_unchanged", "local_reminder_only_next_turn"),
        "opcredit": ("unavailable_frontier_is_ineligible", "nonzero_signed_ftc_observed", "gold_is_training_credit_only"),
        "structural-signal-retriever": ("no_match_returns_empty",),
        "muon-paired-budget": ("data_time_ranking_reversal_preserved", "selection_uses_auc_not_final_loss"),
    }
    for field, bound in upper.get(key, {}).items():
        value = metrics.get(field)
        require(type(value) in (int, float) and 0 <= value <= bound, f"{key}: {field} violates bound")
    for field in positive.get(key, ()):
        value = metrics.get(field)
        require(type(value) in (int, float) and value > 0, f"{key}: {field} must be positive")
    for field in truth.get(key, ()):
        require(metrics.get(field) is True, f"{key}: {field} failed")
    if key == "langdit":
        require(.5 <= metrics.get("learned_calibration_min", -1) <= metrics.get("learned_calibration_max", -1) <= 2,
                "LangDiT calibration outside published bounds")
        require(metrics.get("extreme_codebook_scale_gradient_cases") == 4, "LangDiT extreme-scale regression missing")
    if key in {"oprd", "opcredit"}:
        require(metrics.get("optimizer_updates") == 4, f"{key}: fixed four-step diagnostic differs")
    if key == "probe":
        require(metrics.get("verifier_hits", 0) > metrics.get("distinct_episode_policy_hits", 0) > 0,
                "PROBE repeated raw hits must remain separate from distinct episode-policy pairs")
        require(math.isclose(metrics.get("violation_yield_per_100_episodes", -1),
                             100 * metrics["verifier_hits"] / metrics["episodes"], abs_tol=1e-10),
                "PROBE raw hit yield denominator differs")


def validate_curated(metric, expected_key):
    """Finalization must re-admit per-seed outcomes and frozen provenance.

    A prior curation step is not trusted as a pass certificate: failures, stale
    sources or edited summaries must not become terminal acceptance later.
    """
    reject_failure(metric)
    require(metric.get("method") == expected_key and metric.get("seeds") == SEEDS,
            "curated metric identity/seed coverage differs")
    require(metric.get("diagnostic_only") is True and metric.get("promotion_eligible") is False
            and metric.get("evolve_integrated") is False, "curated diagnostic boundary missing")
    protocol = metric.get("evaluation_protocol", {})
    require(protocol.get("seeds") == SEEDS and protocol.get("formal_comparison") is False,
            "curated evaluation protocol differs")
    raw_key = next((raw for raw, stable in CATALOG_KEYS.items() if stable == expected_key), expected_key)
    groups = [(device, runner, items[raw_key]) for device, runner, items in GROUPS.values() if raw_key in items]
    require(len(groups) == 1, "unknown accepted curated key")
    _, runner, (domain, _, module) = groups[0]
    require(metric.get("manifest_ref") == f"{domain}:{expected_key}", "curated manifest identity differs")
    dataset = metric.get("dataset", {})
    require(dataset.get("id") and dataset.get("revision"), "curated dataset identity missing")
    rows = metric.get("per_seed", [])
    require([row.get("seed") for row in rows] == SEEDS, "curated per-seed coverage differs")
    finite_tree(rows)
    for row in rows:
        reject_failure(row)
        require(row.get("metrics"), "curated measurement missing")
        validate_measurement(raw_key, row["metrics"])
    require(metric.get("metrics") == aggregate(rows), "curated aggregate differs from measured trials")
    provenance = metric.get("provenance", {})
    commit = provenance.get("commit", "")
    require(re.fullmatch(r"[0-9a-f]{40}", commit), "curated frozen commit missing")
    hashes = provenance.get("executed_source_sha256", {})
    require(set(hashes) == {runner, f"src/auto_research/{module}.py"}, "curated source coverage differs")
    for name, digest in hashes.items():
        require(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, f"curated source stale: {name}")
        try:
            frozen = subprocess.check_output(["git", "show", f"{commit}:{name}"], cwd=ROOT, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as error:
            raise ValueError(f"curated frozen source unavailable: {name}") from error
        require(hashlib.sha256(frozen).hexdigest() == digest, f"curated frozen source differs: {name}")


def validate(payload, group):
    reject_failure(payload)
    require(payload.get("executed_source_uncommitted") is not True, "dirty executed source cannot be admitted")
    device, runner, items = GROUPS[group]
    require(payload.get("device") == device, "device differs; no CPU fallback for CUDA")
    require(payload.get("seeds") == SEEDS, "all three fixed seeds required")
    require(payload.get("diagnostic_only") is True and payload.get("promotion_eligible") is False,
            "diagnostic boundary missing")
    if device == "cuda":
        model = payload.get("accelerator", "").upper()
        require("NVIDIA" in model and any(gpu in model for gpu in ("A100", "A30")), "real A100/A30 required")
    commit = payload.get("code_commit", "")
    require(re.fullmatch(r"[0-9a-f]{40}", commit), "full frozen source commit required")
    expected = {runner, *(f"src/auto_research/{module}.py" for _, _, module in items.values())}
    hashes = payload.get("executed_source_sha256", {})
    require(set(hashes) == expected, "executed source coverage differs")
    for name, digest in hashes.items():
        require(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, f"current source differs: {name}")
        frozen = subprocess.check_output(["git", "show", f"{commit}:{name}"], cwd=ROOT)
        require(hashlib.sha256(frozen).hexdigest() == digest, f"uncommitted source evidence: {name}")
    require(set(payload.get("components", {})) == set(items), "accepted component coverage differs")
    for key, component in payload["components"].items():
        reject_failure(component)
        dataset = component.get("dataset", {})
        require(dataset.get("id") and dataset.get("revision"), f"{key}: input identity missing")
        rows = component.get("per_seed", [])
        require([row.get("seed") for row in rows] == SEEDS, f"{key}: seed coverage differs")
        finite_tree(rows)
        for row in rows:
            reject_failure(row)
            require(row.get("metrics"), f"{key}: empty measurement")
            validate_measurement(key, row["metrics"])
        aggregate(rows)
    return device, runner, items


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def curate(path: Path, group: str):
    payload = json.loads(path.read_text())
    device, runner, items = validate(payload, group)
    raw_digest = hashlib.sha256(path.read_bytes()).hexdigest()
    for key, (domain, identity, module) in items.items():
        component = payload["components"][key]
        key = CATALOG_KEYS.get(key, key)
        metric_path = f"docs/{domain}/{identity}-{key}/metrics/component-{device}-seeds42-44.json"
        sources = {name: digest for name, digest in payload["executed_source_sha256"].items()
                   if name == runner or name == f"src/auto_research/{module}.py"}
        dataset = component["dataset"]
        metrics = aggregate(component["per_seed"])
        common = {"diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
                  "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True}
        provenance = {"commit": payload["code_commit"], "artifact_path": metric_path,
                      "dataset_fingerprint": f"{dataset['id']}@{dataset['revision']};seeds=42,43,44",
                      "raw_runner_artifact_sha256": raw_digest, "executed_source_sha256": sources,
                      "accelerator": payload.get("accelerator", "CPU")}
        metric = {"schema_version": 2, "method": key, "manifest_ref": f"{domain}:{key}",
                  "seeds": SEEDS, "dataset": dataset, "evaluation_tier": "l1_mechanism",
                  "evaluation_protocol": {"tier": "l1_mechanism", "seeds": SEEDS, "formal_comparison": False,
                                          "claim_policy": "bounded independent mechanism/protocol diagnostic; not model capability"},
                  "metrics": metrics, "per_seed": component["per_seed"], "provenance": provenance, **common}
        write(ROOT / metric_path, metric)
        if device == "cuda":
            receipt_path = f"docs/gpu-validations/{key}-supplement-a100-20261017.json"
            command = ["python", runner, "--device", "cuda", "--seeds", "42,43,44", "--code-commit",
                       payload["code_commit"], "--output", f"{group}-cuda.json"]
            receipt = {"schema_version": 1, "adapter_key": key, "validated_at": "2026-10-17",
                       "accelerator": {"vendor": "NVIDIA", "model": payload["accelerator"], "count": 1},
                       "command": command, "dataset": dataset,
                       "checkpoint": {"public_id": "none-seeded-independent-component-initialization",
                                      "revision": payload["code_commit"], "pretrained": False},
                       "seeds": SEEDS, "result": "passed", "metrics": metrics,
                       "executed_source_sha256": sources,
                       "provenance": {**provenance, "artifact_path": receipt_path, "metric_artifact_path": metric_path},
                       **common}
            write(ROOT / receipt_path, receipt)
        print(metric_path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("group", choices=GROUPS)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    curate(args.input, args.group)


if __name__ == "__main__":
    main()
