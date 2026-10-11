"""L0 synthetic accounting fixtures only; never submitted as GPU evidence."""
from copy import deepcopy
import hashlib
import importlib.util
import json

import pytest

pytest.importorskip("torch")


def module():
    spec = importlib.util.spec_from_file_location("sguid_curation", "scripts/curate_sguid_evidence.py")
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def accounting_fixture():
    curation = module()
    protocol = {"rounds": 2, "training_examples": 2, "probe_steps": 4,
        "internalization_steps": 4, "max_tokens": 512, "skill_tokens": 256,
        "candidate_count": 2, "retrieve_count": 6, "kappa": .05, "gap_clip": 3.,
        "tau": 5., "late_minimum": 2, "compact_counts": [6, 3],
        "teacher": "live synchronized same-model no_grad", "full_vocabulary_size": 151936,
        "logits_projection": "full model output vocabulary; no top-k approximation",
        "loss": "signed generalized full-vocabulary forward KL",
        "gold_role": "training verifier/curation only; absent from student and retrieval",
        "student_thinking": False, "teacher_thinking": True, "evaluation_thinking": True}
    prefixes = {"disabled": "Solve 2 plus 3.\nassistant\n<think>\n\n</think>\n\n",
                "enabled": "Solve 2 plus 3.\nassistant\n<think>\n"}
    protocol.update(adapter_module_count=8, backbone={"model_type": "qwen3_5",
        "loaded_class": "Qwen3_5ForConditionalGeneration",
        "input_modality": "text only; vision weights frozen and unused"},
        thinking_template_audit={"supported": True, "probe_question": "Solve 2 plus 3.",
            "requested": {"student": False, "teacher": True, "evaluation": True},
            "effective": {"student": False, "teacher": True, "evaluation": True},
            "rendered_prefixes": prefixes,
            "rendered_prefix_sha256": {k: sha(v) for k, v in prefixes.items()}})
    report = {"schema_version": 1, "adapter_key": "sguid", "seed": 42, "status": "completed",
        "diagnostic_only": True, "evaluation_tier": "l1_mechanism", "test_read": False,
        "validation_used_for_selection": False, "protocol": protocol,
        "checkpoint": {"id": "Qwen/Qwen3.5-9B", "revision": "a" * 40},
        "dataset": {"id": "openai/grade-school-math", "revision": "b" * 40},
        "split_provenance": {"verified": True, "test_read": False,
            "source_id": "openai/grade-school-math", "source_revision": "b" * 40,
            "source_sha256": sha("source"),
            "partition_sha256": {"train": sha("train"), "validation": sha("validation")}},
        "accelerator": {"vendor": "NVIDIA", "model": "NVIDIA A100-SXM4-80GB"},
        "executed_source_sha256": {s: sha(s) for s in curation.SOURCES},
        "baseline": {"examples": 2, "exact_match": 1., "eos_completed": 1, "truncated": 1},
        "final_validation": {"examples": 2, "exact_match": .5, "eos_completed": 0, "truncated": 2},
        "adapter_parameter_delta_l2": .5, "rounds": []}
    base = sha("initial")
    skill = {"title": "Units", "principle": "Convert quantities to consistent units before doing arithmetic."}
    generated = json.dumps(skill)
    for r in range(2):
        key = f"r{r}-s0"
        bank = {key: deepcopy(skill)}
        traces = []
        for i in range(2):
            trace = {"training_index": i, "student_policy_sha256": base,
                     "student_rollout": "#### 1", "student_rollout_sha256": sha("#### 1"),
                     "generated_skill_response": generated, "generated_skill_sha256": sha(generated)}
            trace.update({"accepted_skill": key} if i == 0 else {"rejection": "duplicate generated skill"})
            traces.append(trace)

        def history(stage):
            rows, current = [], base
            for step in range(4):
                following = sha(f"r{r}-{stage}-{step}")
                rows.append({"step": step, "training_index": step % 2, "early": step < 2,
                    "policy_sha256_before": current, "policy_sha256_after": following,
                    "gradient_l2": .2, "loss": .1, "active_update": True,
                    "correct": True, "eos_completed": False, "response_tokens": 512,
                    "gate_nonzero_skills": 1, "events": [{"skill": key, "coefficient": 1.,
                        "support": .2, "full_vocabulary_size": 151936,
                        "teacher_requires_grad": False, "student_requires_grad": True}]})
                current = following
            return rows, current

        probe, _ = history("probe")
        compact, next_policy = history("compact")
        report["rounds"].append({"round": r, "status": "completed", "round_base_sha256": base,
            "restored_sha256": base, "next_policy_sha256": next_policy,
            "candidate_bank": bank, "curation": traces, "probe": probe,
            "activities": {key: {"early_retrievals": 2, "late_retrievals": 2,
                                  "early_positive": 2, "late_positive": 2}},
            "selected_skills": [key], "internalization": compact,
            "probe_parameter_delta_l2": .2, "internalization_parameter_delta_l2": .1})
        base = next_policy
    return report


def test_accounting_fixture_retains_negative_validation_and_truncation():
    report = accounting_fixture()
    summary = module().summarize(report)
    assert summary["completed_rounds"] == 2
    assert summary["final_validation_exact_match"] < summary["baseline_validation_exact_match"]
    assert summary["validation_truncated"] == 2
    assert all(r["probe_updates"] == 4 for r in summary["rounds"])


@pytest.mark.parametrize("corruption", ["unsupported", "ignored", "digest", "effective", "class", "modules"])
def test_curator_rejects_unverified_actual_thinking_or_backbone(corruption):
    report = accounting_fixture()
    protocol = report["protocol"]
    audit = protocol["thinking_template_audit"]
    if corruption == "unsupported":
        audit["supported"] = False
    elif corruption == "ignored":
        text = audit["rendered_prefixes"]["disabled"]
        audit["rendered_prefixes"]["enabled"] = text
        audit["rendered_prefix_sha256"]["enabled"] = sha(text)
    elif corruption == "digest":
        audit["rendered_prefix_sha256"]["enabled"] = sha("invented")
    elif corruption == "effective":
        audit["effective"]["teacher"] = False
    elif corruption == "class":
        protocol["backbone"]["model_type"] = "unknown"
        protocol["backbone"]["loaded_class"] = None
    elif corruption == "modules":
        protocol["adapter_module_count"] = 0
    with pytest.raises(ValueError):
        module().summarize(report)


@pytest.mark.parametrize("corruption", ["status", "empty", "restore", "fresh", "activity",
    "positive", "gate", "gradient", "zero", "full-vocab", "teacher-grad", "raw-generation",
    "selected", "movement", "test", "cpu", "h", "nan", "eos"])
def test_accounting_curator_rejects_false_or_weakened_evidence(corruption):
    report = accounting_fixture()
    r = report["rounds"][0]
    event = r["probe"][0]["events"][0]
    if corruption == "status":
        report["status"] = "failed"
    elif corruption == "empty":
        r["candidate_bank"] = {}
    elif corruption == "restore":
        r["restored_sha256"] = sha("probe leaked")
    elif corruption == "fresh":
        report["rounds"][1]["curation"][0]["student_policy_sha256"] = r["round_base_sha256"]
    elif corruption == "activity":
        r["activities"]["r0-s0"]["late_retrievals"] += 1
    elif corruption == "positive":
        r["activities"]["r0-s0"]["late_positive"] += 1
    elif corruption == "gate":
        event["coefficient"] = -1.
    elif corruption == "gradient":
        r["probe"][0]["gradient_l2"] = 0.
    elif corruption == "zero":
        r["internalization_parameter_delta_l2"] = 0.
    elif corruption == "full-vocab":
        event["full_vocabulary_size"] = 20
    elif corruption == "teacher-grad":
        event["teacher_requires_grad"] = True
    elif corruption == "raw-generation":
        r["curation"][0]["generated_skill_response"] = "curator invented skill"
    elif corruption == "selected":
        r["selected_skills"] = []
    elif corruption == "movement":
        r["probe"][0]["policy_sha256_after"] = r["probe"][0]["policy_sha256_before"]
    elif corruption == "test":
        report["test_read"] = True
    elif corruption == "cpu":
        report["accelerator"] = {"vendor": "CPU", "model": "CPU"}
    elif corruption == "h":
        report["protocol"]["late_minimum"] = 1
    elif corruption == "nan":
        r["probe"][0]["loss"] = float("nan")
    elif corruption == "eos":
        report["final_validation"]["truncated"] = 0
    with pytest.raises(ValueError):
        module().summarize(report)


def test_source_digest_mismatch_cannot_create_passed_artifact():
    report = accounting_fixture()
    hashes = report["executed_source_sha256"].copy()
    hashes[next(iter(hashes))] = sha("wrong source")
    with pytest.raises(ValueError, match="executed source"):
        module().curate(report, commit="c" * 40, validated_at="2026-10-11", committed_hashes=hashes)


def test_curator_strips_public_raw_traces_and_still_retains_generated_skills():
    report = accounting_fixture()
    outputs = module().curate(report, commit="c" * 40, validated_at="2026-10-11",
                              committed_hashes=report["executed_source_sha256"])
    metrics = next(v for k, v in outputs.items() if "/metrics/" in k)
    trace = metrics["runtime_details"]["rounds"][0]["curation"][0]
    assert "student_rollout" not in trace and "generated_skill_response" not in trace
    assert trace["student_rollout_sha256"]
    assert metrics["runtime_details"]["rounds"][0]["candidate_bank"]
    assert metrics["evaluation_protocol"]["formal_comparison"] is False
    receipt = next(v for k, v in outputs.items() if "/gpu-validations/" in k)
    assert receipt["executed_source_sha256"] == report["executed_source_sha256"]
    assert report["rounds"][0]["curation"][0]["student_rollout"]  # input is untouched


def test_failed_selection_can_be_archived_but_never_promoted_to_gpu_pass():
    report = accounting_fixture()
    report["status"] = report["rounds"][0]["status"] = "failed"
    report["rounds"][0]["failure"] = "no skills passed the persistence criterion"
    diagnostic = module().failure_diagnostic(report)
    assert diagnostic["result"] == "failed" and diagnostic["gpu_pass_receipt"] is False
    with pytest.raises(ValueError, match="failed/partial"):
        module().curate(report, commit="c" * 40, validated_at="2026-10-11",
                       committed_hashes=report["executed_source_sha256"])
