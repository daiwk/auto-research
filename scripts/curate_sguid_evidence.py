#!/usr/bin/env python3
"""Validate measured SGUID lifecycle evidence; never turn failed selection into a pass.

This curator checks internal accounting. The operator must independently verify
remote executed files/checkpoint/data against their public immutable sources.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import date
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCES = (
    "src/auto_research/post_training/sguid_checkpoint.py", "scripts/run_sguid_checkpoint.py",
    "src/auto_research/post_training/oct11_objectives.py",
    "src/auto_research/post_training/oct10_checkpoint.py", "src/auto_research/public_holdout.py",
)


def _finite(value, *, positive=False):
    if (isinstance(value, bool) or not isinstance(value, (int, float))
            or not math.isfinite(value) or (positive and value <= 0)):
        raise ValueError("finite measured value required")
    return value


def _sha(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        raise ValueError("SHA256 provenance required")
    return value


def _validate_base(report):
    if (report.get("adapter_key") != "sguid" or report.get("diagnostic_only") is not True
            or report.get("evaluation_tier") != "l1_mechanism"
            or report.get("test_read") is not False
            or report.get("validation_used_for_selection") is not False):
        raise ValueError("isolated train-only SGUID mechanism diagnostic required")
    split = report.get("split_provenance", {})
    if split.get("verified") is not True or split.get("test_read") is not False:
        raise ValueError("verified train-only holdout required")
    dataset = report.get("dataset", {})
    if (dataset.get("id") != split.get("source_id")
            or dataset.get("revision") != split.get("source_revision")):
        raise ValueError("dataset revision differs from verified holdout")
    for key in ("train", "validation"):
        _sha(split.get("partition_sha256", {}).get(key))
    _sha(split.get("source_sha256"))
    for item in (dataset, report.get("checkpoint", {})):
        if not item.get("id") or not re.fullmatch(r"[0-9a-f]{40}", item.get("revision", "")):
            raise ValueError("public immutable model/data revision required")
    for source in SOURCES:
        _sha(report.get("executed_source_sha256", {}).get(source))
    # Strict JSON serializability also rejects nonfinite measurements nested in events.
    json.dumps(report, allow_nan=False)


def _validate_history(history, bank, protocol, *, steps, initial_sha):
    if not isinstance(history, list) or len(history) != steps:
        raise ValueError("actual complete probe/internalization history required")
    counts = {key: {"early_retrievals": 0, "late_retrievals": 0,
                    "early_positive": 0, "late_positive": 0} for key in bank}
    previous = initial_sha
    updates = gates = 0
    for index, item in enumerate(history):
        if (item.get("step") != index or item.get("early") != (index < steps // 2)
                or item.get("training_index") != index % protocol["training_examples"]):
            raise ValueError("phase/index accounting differs from actual training budget")
        if _sha(item.get("policy_sha256_before")) != previous:
            raise ValueError("policy chain does not begin from/reuse the actual stage base")
        following = _sha(item.get("policy_sha256_after"))
        gradient = _finite(item.get("gradient_l2"))
        _finite(item.get("loss"))
        if gradient < 0 or item.get("active_update") is not (gradient > 0):
            raise ValueError("active update must have measured finite nonzero gradient")
        if (gradient > 0) == (previous == following):
            raise ValueError("gradient/update accounting differs from actual policy movement")
        if not isinstance(item.get("correct"), bool) or not isinstance(item.get("eos_completed"), bool):
            raise ValueError("actual external verifier and EOS flags required")
        tokens = item.get("response_tokens", 0)
        if not isinstance(tokens, int) or not 1 <= tokens <= protocol["max_tokens"]:
            raise ValueError("response token budget accounting required")
        events = item.get("events", [])
        if len(events) != min(len(bank), protocol["retrieve_count"]):
            raise ValueError("actual retrieved skill events required")
        if len({e.get("skill") for e in events}) != len(events):
            raise ValueError("duplicate skill cannot inflate teaching activity")
        item_gates = 0
        for event in events:
            key = event.get("skill")
            if key not in bank:
                raise ValueError("activity outside the student-generated bank")
            support = _finite(event.get("support"))
            coefficient = _finite(event.get("coefficient"))
            if abs(support) > protocol["gap_clip"] + 1e-6:
                raise ValueError("support exceeds clipped sampled-token gap")
            sign = 1 if support > 0 else -1 if support < 0 else 0
            expected = sign * (1 if item["correct"] else -1) if abs(support) > protocol["kappa"] else 0
            if coefficient != expected:
                raise ValueError("coefficient not derived from actual verifier/gate/support")
            if (event.get("full_vocabulary_size") != protocol["full_vocabulary_size"]
                    or event.get("teacher_requires_grad") is not False
                    or event.get("student_requires_grad") is not True):
                raise ValueError("full vocabulary and synchronized no-grad teacher required")
            phase = "early" if item["early"] else "late"
            counts[key][phase + "_retrievals"] += 1
            counts[key][phase + "_positive"] += int(coefficient > 0)
            item_gates += int(coefficient != 0)
        if item.get("gate_nonzero_skills") != item_gates or (gradient > 0 and not item_gates):
            raise ValueError("nonzero gates differ from measured teaching events")
        updates += int(gradient > 0)
        gates += item_gates
        previous = following
    if not updates:
        raise ValueError("no actual finite nonzero-gradient updates in stage")
    return counts, updates, gates, previous


def summarize(report):
    _validate_base(report)
    if report.get("status") != "completed" or len(report.get("rounds", [])) != 2:
        raise ValueError("failed/partial selection cannot produce a passed GPU receipt")
    accelerator = report.get("accelerator", {})
    if accelerator.get("vendor") != "NVIDIA" or not re.fullmatch(
            r"(?:NVIDIA )?A(?:100|30)(?:[- ](?:SXM4|SXM|PCIE|PCIe))?(?:[- ]\d+GB)?", accelerator.get("model", "")):
        raise ValueError("actual supported NVIDIA A100/A30 required")
    protocol = report["protocol"]
    audit = protocol.get("thinking_template_audit", {})
    modes = {"student": False, "teacher": True, "evaluation": True}
    prefixes = audit.get("rendered_prefixes", {})
    if (audit.get("supported") is not True or audit.get("requested") != modes
            or audit.get("effective") != modes or audit.get("probe_question") != "Solve 2 plus 3."):
        raise ValueError("actual requested/effective thinking template audit required")
    for key in ("enabled", "disabled"):
        text = prefixes.get(key)
        if (not isinstance(text, str) or "Solve 2 plus 3." not in text
                or hashlib.sha256(text.encode()).hexdigest()
                != _sha(audit.get("rendered_prefix_sha256", {}).get(key))):
            raise ValueError("actual rendered thinking prefixes/digests required")
    if (prefixes["enabled"] == prefixes["disabled"]
            or not prefixes["enabled"].rstrip().endswith("<think>")
            or not prefixes["disabled"].rstrip().endswith("</think>")):
        raise ValueError("thinking kwarg ignored or actual mode switch absent")
    backbone = protocol.get("backbone", {})
    supported_classes = {"qwen3": "Qwen3ForCausalLM", "qwen3_5": "Qwen3_5ForConditionalGeneration"}
    if (backbone.get("model_type") not in supported_classes
            or backbone.get("loaded_class") != supported_classes.get(backbone.get("model_type"))
            or backbone.get("input_modality") != "text only; vision weights frozen and unused"
            or not isinstance(protocol.get("adapter_module_count"), int)
            or protocol["adapter_module_count"] < 1):
        raise ValueError("audited actual text backbone and LoRA module count required")
    if (protocol.get("teacher") != "live synchronized same-model no_grad"
            or protocol.get("loss") != "signed generalized full-vocabulary forward KL"
            or protocol.get("logits_projection") != "full model output vocabulary; no top-k approximation"
            or protocol.get("kappa") != .05 or protocol.get("gap_clip") != 3.
            or protocol.get("tau") != 5. or protocol.get("late_minimum", 0) < 2
            or protocol.get("compact_counts") != [6, 3] or protocol.get("rounds") != 2
            or protocol.get("student_thinking") is not False
            or protocol.get("teacher_thinking") is not True
            or protocol.get("evaluation_thinking") is not True
            or protocol.get("gold_role") != "training verifier/curation only; absent from student and retrieval"):
        raise ValueError("actual synchronized SGUID protocol required; no weakened selection gate")
    for field in ("probe_steps", "internalization_steps", "max_tokens", "skill_tokens",
                  "training_examples", "candidate_count", "retrieve_count", "full_vocabulary_size"):
        if not isinstance(protocol.get(field), int) or protocol[field] < 1:
            raise ValueError("actual nonzero execution budgets required")
    from auto_research.post_training.sguid_checkpoint import evaluation_token_budget
    # Missing/None means the original shared generation cap. Never infer a
    # larger budget from a validation outcome or rewrite historical evidence.
    evaluation_budget = evaluation_token_budget(protocol["max_tokens"],
                                                 protocol.get("evaluation_max_tokens"))
    if protocol["full_vocabulary_size"] < 1000:
        raise ValueError("real public model full vocabulary required")
    previous_policy = None
    summaries = []
    for r, record in enumerate(report["rounds"]):
        initial = _sha(record.get("round_base_sha256"))
        if (record.get("round") != r or record.get("status") != "completed"
                or record.get("restored_sha256") != initial
                or (previous_policy is not None and previous_policy != initial)):
            raise ValueError("round restart/fresh next policy chain is inconsistent")
        bank, curation = record.get("candidate_bank", {}), record.get("curation", [])
        if not bank or len(curation) != min(protocol["training_examples"], protocol["candidate_count"]):
            raise ValueError("actual current-student generated candidate bank required")
        accepted = set()
        for i, trace in enumerate(curation):
            if trace.get("training_index") != i or trace.get("student_policy_sha256") != initial:
                raise ValueError("next round must freshly curate from its current policy")
            for raw, digest in (("student_rollout", "student_rollout_sha256"),
                                ("generated_skill_response", "generated_skill_sha256")):
                if not isinstance(trace.get(raw), str) or hashlib.sha256(trace[raw].encode()).hexdigest() != _sha(trace.get(digest)):
                    raise ValueError("generated skill/rollout provenance digest mismatch")
            if "accepted_skill" in trace:
                key = trace["accepted_skill"]
                if key not in bank or key != f"r{r}-s{i}" or key in accepted:
                    raise ValueError("bank skill does not trace to this round's generated output")
                # Parse exactly the generated model output, never a curator-made replacement.
                from auto_research.post_training.sguid_checkpoint import parse_skill
                if parse_skill(trace["generated_skill_response"]) != bank[key]:
                    raise ValueError("candidate skill was not generated by the actual current student")
                accepted.add(key)
            elif not trace.get("rejection"):
                raise ValueError("failed model-generated skills must retain rejection reason")
        if accepted != set(bank):
            raise ValueError("untraceable candidate skill in generated bank")
        counts, probe_updates, probe_gates, probe_policy = _validate_history(
            record.get("probe"), bank, protocol, steps=protocol["probe_steps"], initial_sha=initial)
        if counts != record.get("activities"):
            raise ValueError("activity statistics not derived from actual probe events")
        eligible = []
        for key, a in counts.items():
            if a["early_positive"] > 0 and a["late_positive"] >= protocol["late_minimum"]:
                qe = a["early_positive"] / a["early_retrievals"]
                ql = a["late_positive"] / a["late_retrievals"]
                if ql >= qe / protocol["tau"]:
                    eligible.append((key, a["late_positive"], ql))
        eligible.sort(key=lambda x: (-x[1], -x[2], x[0]))
        selected = [key for key, _, _ in eligible[:protocol["compact_counts"][r]]]
        if not selected or selected != record.get("selected_skills"):
            raise ValueError("selected skills do not satisfy/rank by persistent positive teaching")
        compact = {key: bank[key] for key in selected}
        _, updates, gates, final_policy = _validate_history(record.get("internalization"), compact,
            protocol, steps=protocol["internalization_steps"], initial_sha=initial)
        if final_policy != record.get("next_policy_sha256") or final_policy == initial:
            raise ValueError("compact distillation did not create the fresh next policy")
        _finite(record.get("probe_parameter_delta_l2"), positive=True)
        if probe_policy == initial:
            raise ValueError("probe parameter movement does not match its policy digest")
        _finite(record.get("internalization_parameter_delta_l2"), positive=True)
        previous_policy = final_policy
        summaries.append({"round": r, "candidate_skills": len(bank), "selected_skills": len(selected),
                          "probe_updates": probe_updates, "internalization_updates": updates,
                          "probe_nonzero_gates": probe_gates, "internalization_nonzero_gates": gates,
                          "internalization_parameter_delta_l2": record["internalization_parameter_delta_l2"]})
    _finite(report.get("adapter_parameter_delta_l2"), positive=True)
    for name in ("baseline", "final_validation"):
        metrics = report[name]
        n = metrics.get("examples", 0)
        if not isinstance(n, int) or n < 1 or not 0 <= _finite(metrics.get("exact_match")) <= 1:
            raise ValueError("actual bounded validation measurements required")
        if (not isinstance(metrics.get("eos_completed"), int) or not isinstance(metrics.get("truncated"), int)
                or min(metrics["eos_completed"], metrics["truncated"]) < 0
                or metrics["eos_completed"] + metrics["truncated"] != n):
            raise ValueError("retain every EOS completion and truncation")
    if report["baseline"]["examples"] != report["final_validation"]["examples"]:
        raise ValueError("same bounded validation case count required")
    return {"completed_rounds": 2, "adapter_parameter_delta_l2": report["adapter_parameter_delta_l2"],
            "evaluation_max_tokens": evaluation_budget,
            "baseline_validation_exact_match": report["baseline"]["exact_match"],
            "final_validation_exact_match": report["final_validation"]["exact_match"],
            "validation_examples": report["final_validation"]["examples"],
            "validation_truncated": report["final_validation"]["truncated"], "rounds": summaries}


def source_hashes(commit):
    return {source: hashlib.sha256(subprocess.check_output(
        ["git", "show", f"{commit}:{source}"], cwd=ROOT)).hexdigest() for source in SOURCES}


def curate(report, *, commit, validated_at, committed_hashes):
    metrics = summarize(report)
    if committed_hashes != report["executed_source_sha256"]:
        raise ValueError("executed source differs from historical committed source")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("full historical source commit required")
    date.fromisoformat(validated_at)
    stable = deepcopy(report)
    for record in stable["rounds"]:
        for trace in record["curation"]:
            trace.pop("student_rollout")
            trace.pop("generated_skill_response")
    seed = report["seed"]
    metric_path = f"docs/post-training/2610.12367-sguid/metrics/checkpoint-a100-seed{seed}.json"
    receipt_path = f"docs/gpu-validations/sguid-a100-{validated_at.replace('-', '')}.json"
    limitations = ["single-seed bounded L1 mechanism diagnostic; not AIME/HMMT improvement",
                   "GSM8K training-only holdout instead of DAPO-Math-17K",
                   "current LM hidden cosine retrieval, not original embedding checkpoint",
                   "q/v rank-8 LoRA and reduced early/late window/h; not original all-linear rank-64 run",
                   "signed generalized full-vocabulary KL, not original SGSD bounded discrepancy",
                   "EOS/truncations and any negative validation outcome retained"]
    if report["protocol"]["backbone"]["model_type"] == "qwen3_5":
        limitations.append("Qwen3.5 hybrid text decoder, not original Qwen3 backbone; "
                           "vision unused; q/v LoRA applies only to full-attention layers")
    protocol = report["protocol"]
    command = ["python", "scripts/run_sguid_checkpoint.py", "--checkpoint-path", "checkpoints/public-sguid-model",
               "--checkpoint-id", report["checkpoint"]["id"], "--checkpoint-revision", report["checkpoint"]["revision"],
               "--train-path", "data/gsm8k-holdout/train.jsonl", "--validation-path", "data/gsm8k-holdout/validation.jsonl",
               "--split-manifest", "data/gsm8k-holdout/split.json", "--dataset-revision", report["dataset"]["revision"]]
    for name in ("training_examples", "probe_steps", "internalization_steps", "max_tokens", "skill_tokens",
                 "candidate_count", "retrieve_count", "late_minimum", "rounds"):
        command += ["--" + name.replace("_", "-"), str(protocol[name])]
    if protocol.get("evaluation_max_tokens") is not None:
        command += ["--evaluation-max-tokens", str(metrics["evaluation_max_tokens"])]
    command += ["--validation-examples", str(metrics["validation_examples"]), "--seed", str(seed),
                "--device", "cuda", "--output", f"runs/sguid-seed{seed}.json"]
    payload = {"schema_version": 2, "manifest_ref": "post-training:sguid", "method": "sguid",
               "dataset": report["dataset"]["id"], "seeds": [seed], "metrics": metrics,
               "seed_results": [{"seed": seed, **metrics}],
               "evaluation_protocol": {"tier": "l1_mechanism", "diagnostic_only": True,
                   "formal_comparison": False, "test_read": False, "seeds": [seed],
                   "claim_policy": "bounded executed two-round mechanism; no benchmark gain claim"},
               "runtime_details": stable, "limitations": limitations,
               "provenance": {"original_code_commit": commit, "artifact_path": metric_path,
                   "executed_source_sha256": committed_hashes,
                   "dataset_fingerprint": hashlib.sha256(json.dumps(report["split_provenance"], sort_keys=True).encode()).hexdigest()}}
    receipt = {"schema_version": 1, "adapter_key": "sguid", "validated_at": validated_at,
               "accelerator": report["accelerator"], "command": command, "dataset": report["dataset"],
               "checkpoint": report["checkpoint"], "result": "passed", "evaluation_tier": "l1_mechanism",
               "metrics": metrics, "limitations": limitations, "executed_source_sha256": committed_hashes,
               "provenance": {"commit": commit, "artifact_path": receipt_path,
                   "metrics_artifact": metric_path, "checkpoint_committed": False}}
    return {metric_path: payload, receipt_path: receipt}


def failure_diagnostic(report, *, commit, validated_at, committed_hashes):
    _validate_base(report)
    if report.get("status") != "failed" and not any(r.get("status") == "failed" for r in report.get("rounds", [])):
        raise ValueError("actual failed selection/round required for failure-only archive")
    if committed_hashes != report["executed_source_sha256"]:
        raise ValueError("executed source differs from historical committed source")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("full historical source commit required")
    date.fromisoformat(validated_at)
    stable = deepcopy(report)
    for record in stable.get("rounds", []):
        for trace in record.get("curation", []):
            trace.pop("student_rollout", None)
            trace.pop("generated_skill_response", None)
    return {"schema_version": 1, "adapter_key": "sguid", "result": "failed",
            "diagnostic_only": True, "gpu_pass_receipt": False, "runtime_details": stable,
            "provenance": {"original_code_commit": commit, "validated_at": validated_at,
                           "executed_source_sha256": committed_hashes}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--validated-at", required=True)
    parser.add_argument("--failure-output", type=Path)
    args = parser.parse_args()
    report = json.loads(args.input.read_text())
    commit = subprocess.check_output(["git", "rev-parse", args.source_commit], cwd=ROOT, text=True).strip()
    if args.failure_output:
        args.failure_output.parent.mkdir(parents=True, exist_ok=True)
        args.failure_output.write_text(json.dumps(failure_diagnostic(
            report, commit=commit, validated_at=args.validated_at,
            committed_hashes=source_hashes(commit)), indent=2, allow_nan=False) + "\n")
        return
    for relative, payload in curate(report, commit=commit, validated_at=args.validated_at,
                                    committed_hashes=source_hashes(commit)).items():
        target = ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
