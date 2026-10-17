#!/usr/bin/env python3
"""Admit measured Oct18 bounded components; never invent capability evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import statistics
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from auto_research.gpu_validation import load_gpu_receipt  # noqa: E402
from auto_research.paper_specs.catalog import catalog_records  # noqa: E402
from oct18_frozen_sources import capture_sources, verify_sources  # noqa: E402

SEEDS = [42, 43, 44]
BATCH = "2026-10-18-overlap-bounded-components"
SOURCE_PROOFS = ROOT / "docs/research-audits/oct18-components/frozen-sources.json"
GROUPS = {
    "foundation": ("cuda", "scripts/run_oct18_foundation_components.py", {
        "memory-mosaics-plus": ("foundation-models", "2610.20782", "foundation_models/memory_mosaics_plus"),
        "mjev-spatial": ("foundation-models", "2610.22276", "foundation_models/mjev_spatial"),
        "adaloop-vision": ("foundation-models", "2610.21323", "foundation_models/adaloop_vision"),
        "softcache": ("foundation-models", "2610.22369", "foundation_models/softcache"),
        "rr-vlm": ("foundation-models", "2610.22075", "foundation_models/rr_vlm"),
    }),
    "post": ("cuda", "scripts/run_oct18_post_components.py", {
        "tag-reward-gating": ("post-training", "2610.21404", "post_training/reviewed_oct18"),
        "mrtpo": ("post-training", "2610.21439", "post_training/reviewed_oct18"),
        "token-teacher-selection": ("post-training", "2610.21234", "post_training/reviewed_oct18"),
        "ig-opd": ("post-training", "2610.20664", "post_training/reviewed_oct18"),
        "rshd": ("post-training", "2610.21018", "post_training/reviewed_oct18"),
    }),
    "agent": ("cpu", "scripts/run_oct18_agent_components.py", {
        "diviner": ("agent-research", "2610.21281", "agent_research/diviner"),
        "torsi": ("agent-research", "2610.20665", "agent_research/torsi"),
        "aria": ("agent-research", "2610.20780", "agent_research/aria_repair"),
        "coda": ("agent-research", "2610.20845", "agent_research/coda"),
        "memscope": ("agent-research", "2610.21170", "agent_research/memscope"),
        "jev-agent-harness": ("agent-research", "2610.21412", "agent_research/jev_agent_harness"),
    }),
}
REFERENCES = {"egojepa", "orl-diffusion", "remote-kv-tiers"}
REFERENCE_IDENTITIES = {"egojepa": ("foundation-models", "2610.20904"),
                        "orl-diffusion": ("post-training", "2610.20687"),
                        "remote-kv-tiers": ("foundation-models", "2610.21500")}
COSTS = {
    "memory-mosaics-plus": "原文1.5B/8B、64–256 GPU、每步约4.19M tokens。",
    "mjev-spatial": "12.3M QA、4B模型和8 GPU完整训练。",
    "adaloop-vision": "3B/7B、多臂、batch64和30–40k更新。",
    "softcache": "FLUX、HunyuanVideo、Wan2.1的全预算和946条视频prompts。",
    "rr-vlm": "60B文本token恢复、493k视觉对齐及660k指令样本。",
    "tag-reward-gating": "每臂500步加300步探针、多模型1.7B–30B。",
    "mrtpo": "4 A100/8 H20/8 H200、多任务多seed。",
    "token-teacher-selection": "30B教师、300–400步及最高16K输出。",
    "ig-opd": "8 GPU、8B教师、2B/4B学生、70K输出和20回合。",
    "rshd": "1.7B–8B、双领域150步、重放使生成训练量约翻倍。",
    "diviner": "Meta私有事故、生产工具和数千事故规模不可获取。",
    "torsi": "180任务、多模型、多时钟、多轮商业API教师。",
    "aria": "24k以上轨迹、四框架六benchmark与五训练阶段。",
    "coda": "四种共进化方法、五benchmark及多种技能扰动。",
    "memscope": "商业模型、完整GAIA/xBench、40步搜索与ALFWorld在线记忆。",
    "jev-agent-harness": "原文一轮15.1 L40S host-hours和142.36美元API。",
    "egojepa": "20.1k小时视频、32–64 GPU以及真实多机器人。",
    "orl-diffusion": "36–60 H100-hours，另含B200/NVFP4和多卡系统评测。",
    "remote-kv-tiers": "每节点8 B300，4P+1D部署需5节点。",
}
# Defining per-paper outcomes are checked again here after runner assertions.
OUTCOME_CHECKS: dict[str, dict[str, tuple[str, float | bool]]] = {
    "memory-mosaics-plus": {
        "separate_normalizer_reference_max_error": ("max", 1e-10),
        "future_perturbation_max_error": ("max", 1e-10),
        "pooled_memory_negative_control_error": ("positive", 0),
        "key_gradient_norm": ("positive", 0),
        "key_update_norm": ("positive", 0),
    },
    "mjev-spatial": {
        "native_gqa_reference_max_error": ("max", 1e-10),
        "question_normalized_loss_max_error": ("max", 1e-10),
        "count_roundtrip_errors": ("max", 0),
        "wrong_gqa_group_negative_control_error": ("positive", 0),
        "query_update_norm": ("positive", 0),
    },
    "adaloop-vision": {
        "frozen_visual_block_reference_max_error": ("max", 1e-10),
        "depth_objective_reference_max_error": ("max", 1e-10),
        "frozen_backbone_change": ("max", 0),
        "question_condition_negative_control_difference": ("positive", 0),
        "modulator_update_norm": ("positive", 0),
    },
    "rr-vlm": {
        "unrolled_recurrence_max_error": ("max", 1e-10),
        "frozen_teacher_change": ("max", 0),
        "single_pass_negative_control_difference": ("positive", 0),
        "stage0_update_norm": ("positive", 0),
        "stage1_update_norm": ("positive", 0),
        "stage2_update_norm": ("positive", 0),
    },
    "softcache": {
        "cache_disabled_euler_reference_max_error": ("max", 1e-10),
        "residual_extrapolation_reference_max_error": ("max", 1e-10),
        "hard_cache_negative_control_difference": ("positive", 0),
        "headroom_jumps": ("positive", 0),
        "fresh_evaluations": ("positive", 1),
        "residual_network_update_norm": ("positive", 0),
    },
    "tag-reward-gating": {
        "anchor_reference_max_abs_error": ("max", 1e-10),
        "gate_reference_max_abs_error": ("max", 1e-10),
        "loss_reference_max_abs_error": ("max", 1e-10),
        "joint_restart_delta_l2": ("max", 0),
        "auxiliary_only_negative_control_credit": ("max", 0),
        "probe_parameters_are_not_joint_initialization": ("true", True),
        "probe_gradient_norm_min": ("positive", 0),
        "parameter_delta_l2": ("positive", 0),
        "gradient_norm_min": ("positive", 0),
    },
    "mrtpo": {
        "advantage_reference_max_abs_error": ("max", 1e-10),
        "credit_mean_preservation_max_abs_error": ("max", 1e-10),
        "loss_reference_max_abs_error": ("max", 1e-10),
        "empty_block_negative_control_max_abs_error": ("max", 1e-10),
        "frozen_behavior_delta_l2": ("max", 0),
        "actor_receives_verifier_blocks": ("true", False),
        "parameter_delta_l2": ("positive", 0),
        "gradient_norm_min": ("positive", 0),
    },
    "token-teacher-selection": {
        "hard_zero_weight_fp16_fp32_fp64_max_abs_error": ("max", 0),
        "mixture_reference_max_abs_error": ("max", 1e-10),
        "loss_reference_max_abs_error": ("max", 1e-10),
        "identical_teacher_negative_control_abs_loss": ("max", 1e-10),
        "teacher_delta_l2": ("max", 0),
        "teacher_gradient_count": ("max", 0),
        "routing_criteria_executed": ("positive", 2),
        "parameter_delta_l2": ("positive", 0),
        "gradient_norm_min": ("positive", 0),
    },
    "ig-opd": {
        "advantage_reference_max_abs_error": ("max", 1e-10),
        "macro_action_credit_max_abs_error": ("max", 1e-10),
        "gain_telescoping_max_abs_error": ("max", 1e-10),
        "no_gain_equal_teacher_negative_control_max_abs_advantage": ("max", 0),
        "no_gain_turn_share_max_abs_error": ("max", 1e-10),
        "formatting_iqc_max_abs_credit": ("max", 0),
        "teacher_delta_l2": ("max", 0),
        "actor_receives_reference_answer": ("true", False),
        "parameter_delta_l2": ("positive", 0),
        "gradient_norm_min": ("positive", 0),
    },
    "rshd": {
        "aux_loss_reference_max_abs_error": ("max", 1e-10),
        "empty_admission_negative_control_abs_loss": ("max", 0),
        "equal_replay_rate_is_rejected": ("true", True),
        "leaking_note_is_rejected": ("true", True),
        "frozen_behavior_delta_l2": ("max", 0),
        "teacher_gradient_count": ("max", 0),
        "note_writer_receives_reference_answer": ("true", False),
        "semantic_note_screen_implemented": ("true", False),
        "parameter_delta_l2": ("positive", 0),
        "gradient_norm_min": ("positive", 0),
    },
    "diviner": {
        "independent_admission_count_error": ("max", 0),
        "nonempty_is_evidence_negative_control_false_admissions": ("positive", 0),
        "blocked_agent_self_approvals": ("positive", 0),
        "published_owner_approved_updates": ("positive", 0),
    },
    "torsi": {
        "independent_validation_gain_error": ("max", 1e-10),
        "latency_only_negative_control_underestimate": ("positive", 0),
        "accepted_improvements": ("positive", 0),
        "rejected_ties_and_regressions": ("positive", 1),
        "validation_or_test_tasks_to_teacher": ("max", 0),
    },
    "aria": {
        "independent_prefix_construction_error": ("max", 0),
        "invalid_patches_rejected": ("positive", 2),
        "patch_pass_only_negative_control_false_positives": ("positive", 0),
    },
    "coda": {
        "independent_full_denominator_resistance_error": ("max", 0),
        "conditional_denominator_negative_control_difference": ("positive", 0),
        "retrieval_field_mutations": ("max", 0),
    },
    "memscope": {
        "failed_probe_rollbacks": ("positive", 0),
        "rejected_interface_changes": ("positive", 0),
        "persisted_probe_side_effects": ("max", 0),
        "independent_original_code_rollback_error": ("max", 0),
        "unchecked_install_negative_control_incompatible_edits": ("positive", 0),
    },
    "jev-agent-harness": {
        "independent_cost_accounting_error": ("max", 1e-10),
        "fixed_low_threshold_negative_control_wrong_delegations": ("positive", 0),
        "failed_model_fallbacks": ("positive", 0),
        "gold_fields_exposed_to_runtime_callbacks": ("max", 0),
        "delegated_decisions": ("positive", 0),
        "strong_fallbacks": ("positive", 0),
    },
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def reject_failure(row):
    require(isinstance(row, dict), "structured measurement required")
    for name in ("status", "result"):
        value = row.get(name)
        if isinstance(value, dict):
            reject_failure(value)
        else:
            require(value is None or (isinstance(value, str) and value.lower() in {
                "passed", "completed", "success", "ok",
            }), f"explicit {name} failure or nonterminal result cannot be admitted")
        require(str(value or "").lower() not in {
            "failed", "failure", "error", "partial", "skipped", "cancelled", "canceled", "timeout",
        }, f"explicit {name} failure cannot be admitted")
    require(not row.get("error") and not row.get("errors"), "execution errors cannot be admitted")


def aggregate(rows):
    require(len(rows) == 3 and [r.get("seed") for r in rows] == SEEDS, "per-seed coverage differs")
    names = set(rows[0].get("metrics", {}))
    require(names and all(set(r.get("metrics", {})) == names for r in rows), "metric schema differs")
    result = {}
    for row in rows:
        reject_failure(row)
    for name in sorted(names):
        values = [row["metrics"][name] for row in rows]
        if all(type(v) is bool for v in values):
            result[name] = all(values)
        else:
            require(all(type(v) in (int, float) and math.isfinite(v) for v in values), "finite scalar required")
            result[name] = {"mean": statistics.mean(values), "std": statistics.stdev(values), "n": 3}
    return result


def validate_outcomes(key, metrics):
    require(key in COSTS and metrics, "unknown or empty outcome")
    for name, (kind, bound) in OUTCOME_CHECKS.get(key, {}).items():
        value = metrics.get(name)
        if kind == "true":
            require(value is bound, f"{key}: {name} must be true")
        else:
            require(type(value) in (int, float) and math.isfinite(value), f"{key}: missing finite {name}")
            require((0 <= value <= bound) if kind == "max" else value > bound,
                    f"{key}: {name} violates {kind} bound")


def source_hashes(commit, hashes, expected, *, require_git=True):
    require(re.fullmatch(r"[0-9a-f]{40}", str(commit)), "full frozen source commit required")
    require(set(hashes) == expected, "executed source coverage differs")
    for name, digest in hashes.items():
        path = (ROOT / name).resolve()
        require(path.is_relative_to(ROOT) and path.is_file(), "invalid executed path")
        require(hashlib.sha256(path.read_bytes()).hexdigest() == digest, f"current source stale: {name}")
        if require_git:
            try:
                frozen = subprocess.check_output(["git", "show", f"{commit}:{name}"], cwd=ROOT, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError as error:
                raise ValueError(f"frozen source unavailable: {name}") from error
            require(hashlib.sha256(frozen).hexdigest() == digest, f"frozen source differs: {name}")
    if not require_git:
        # Preserve the actual Git Merkle proof so shallow or squash-merged
        # checkouts can verify commit/path/bytes without old Git references.
        bundle = json.loads(SOURCE_PROOFS.read_text())
        require(bundle.get("schema_version") == 1, "source proof bundle schema differs")
        record = bundle.get("commits", {}).get(commit)
        require(isinstance(record, dict), "frozen source commit proof unavailable")
        complete_hashes = record.get("executed_source_sha256", {})
        require(all(complete_hashes.get(name) == digest for name, digest in hashes.items()),
                "measured sources differ from proven source scope")
        verify_sources(ROOT, commit, complete_hashes, record.get("proof"))


def item_for(key):
    matches = [(device, runner, items[key]) for device, runner, items in GROUPS.values() if key in items]
    require(len(matches) == 1, "key not in accepted scope")
    return matches[0]


def validate_payload(payload, group):
    reject_failure(payload)
    device, runner, items = GROUPS[group]
    require(payload.get("device") == device, "device differs; no CUDA fallback")
    require(payload.get("seeds") == SEEDS, "seed coverage differs")
    require(payload.get("diagnostic_only") is True and payload.get("promotion_eligible") is False,
            "diagnostic boundary missing")
    require(not payload.get("executed_source_uncommitted"), "dirty source cannot be admitted")
    if device == "cuda":
        name = payload.get("accelerator", "").upper()
        require("NVIDIA" in name and any(model in name for model in ("A100", "A30")), "real A100/A30 required")
    expected = {runner, *(f"src/auto_research/{module}.py" for _, _, module in items.values())}
    source_hashes(payload.get("code_commit"), payload.get("executed_source_sha256", {}), expected)
    require(set(payload.get("components", {})) == set(items), "component coverage differs")
    for key, component in payload["components"].items():
        reject_failure(component)
        require(component.get("diagnostic_only") is True and component.get("promotion_eligible") is False
                and component.get("evolve_integrated") is False, f"{key}: capability promotion forbidden")
        require(component.get("full_experiment_status") == "not_reproduced_high_cost", "full cost boundary missing")
        dataset = component.get("dataset", {})
        require(dataset.get("id") and dataset.get("revision"), "input identity/revision missing")
        rows = component.get("per_seed", [])
        actual = aggregate(rows)
        if "metrics" in component:
            require(component["metrics"] == actual, "runner aggregate differs")
        for row in rows:
            validate_outcomes(key, row["metrics"])
    return device, runner, items


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def generated_input_fingerprint(dataset, hashes):
    # These diagnostics generate inputs, not a downloaded dataset. Bind the
    # recipe revision, exact generator sources and seeds without inventing a
    # fingerprint for an unobserved external benchmark.
    recipe = {"dataset": dataset, "seeds": SEEDS, "executed_source_sha256": hashes}
    return "sha256:" + hashlib.sha256(json.dumps(recipe, sort_keys=True).encode()).hexdigest()


def curate(path, group):
    payload = json.loads(path.read_text())
    device, runner, items = validate_payload(payload, group)
    bundle = json.loads(SOURCE_PROOFS.read_text()) if SOURCE_PROOFS.exists() else {"schema_version": 1, "commits": {}}
    require(bundle.get("schema_version") == 1 and isinstance(bundle.get("commits"), dict), "invalid source proof bundle")
    hashes = payload["executed_source_sha256"]
    bundle["commits"][payload["code_commit"]] = {
        "executed_source_sha256": hashes,
        "proof": capture_sources(ROOT, payload["code_commit"], hashes),
    }
    write_json(SOURCE_PROOFS, bundle)
    for key, (domain, identity, module) in items.items():
        component = payload["components"][key]
        artifact = f"docs/{domain}/{identity}-{key}/metrics/component-{device}-seeds42-44.json"
        hashes = {p: h for p, h in payload["executed_source_sha256"].items()
                  if p in {runner, f"src/auto_research/{module}.py"}}
        metrics = aggregate(component["per_seed"])
        common = {"diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
                  "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True}
        provenance = {"commit": payload["code_commit"], "artifact_path": artifact,
                      "dataset_fingerprint": generated_input_fingerprint(component["dataset"], hashes),
                      "raw_runner_artifact_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                      "executed_source_sha256": hashes, "accelerator": payload.get("accelerator", "CPU")}
        metric = {"schema_version": 2, "method": key, "manifest_ref": f"{domain}:{key}",
                  "seeds": SEEDS, "dataset": component["dataset"], "evaluation_tier": "l1_mechanism",
                  "evaluation_protocol": {"tier": "l1_mechanism", "seeds": SEEDS, "formal_comparison": False,
                                          "claim_policy": "bounded mechanism/protocol diagnostic, not capability evidence"},
                  "metrics": metrics, "per_seed": component["per_seed"], "provenance": provenance, **common}
        write_json(ROOT / artifact, metric)
        if device == "cuda":
            receipt_path = f"docs/gpu-validations/{key}-a100-20261018.json"
            receipt = {"schema_version": 1, "adapter_key": key, "validated_at": "2026-10-18",
                       "accelerator": {"vendor": "NVIDIA", "model": payload["accelerator"], "count": 1},
                       "command": ["python", runner, "--device", "cuda", "--seeds", "42,43,44", "--code-commit",
                                   payload["code_commit"], "--output", path.name],
                       "dataset": component["dataset"],
                       "checkpoint": {"public_id": "none-seeded-component-initialization",
                                      "revision": payload["code_commit"], "pretrained": False},
                       "seeds": SEEDS, "result": "passed", "metrics": metrics,
                       "executed_source_sha256": hashes,
                       "provenance": {**provenance, "artifact_path": receipt_path, "metric_artifact_path": artifact},
                       **common}
            write_json(ROOT / receipt_path, receipt)
        print(artifact)


def validate_curated(metric, key):
    reject_failure(metric)
    require(metric.get("method") == key and metric.get("seeds") == SEEDS, "curated identity/seed differs")
    require(metric.get("diagnostic_only") is True and metric.get("promotion_eligible") is False
            and metric.get("evolve_integrated") is False, "curated boundary differs")
    require(metric.get("full_experiment_status") == "not_reproduced_high_cost"
            and metric.get("full_experiment_review_done") is True, "curated full cost boundary differs")
    dataset = metric.get("dataset", {})
    require(isinstance(dataset, dict) and dataset.get("id") and dataset.get("revision"), "curated dataset identity missing")
    require(dataset.get("capability_benchmark") is not True and dataset.get("public_benchmark_evaluated") is not True,
            "diagnostic input cannot advertise a capability benchmark")
    device, runner, (domain, _, module) = item_for(key)
    require(metric.get("manifest_ref") == f"{domain}:{key}", "manifest identity differs")
    rows = metric.get("per_seed", [])
    require(metric.get("metrics") == aggregate(rows), "curated aggregate differs")
    for row in rows:
        validate_outcomes(key, row["metrics"])
    protocol = metric.get("evaluation_protocol", {})
    require(protocol.get("seeds") == SEEDS and protocol.get("formal_comparison") is False
            and protocol.get("tier") == metric.get("evaluation_tier") == "l1_mechanism", "curated protocol differs")
    provenance = metric.get("provenance", {})
    require(provenance.get("dataset_fingerprint") == generated_input_fingerprint(
        dataset, provenance.get("executed_source_sha256", {})), "curated generated-input fingerprint differs")
    source_hashes(provenance.get("commit"), provenance.get("executed_source_sha256", {}),
                  {runner, f"src/auto_research/{module}.py"}, require_git=False)
    return device


def validate_catalog_identity(row):
    key = row["key"]
    if key in REFERENCE_IDENTITIES:
        domain, identity = REFERENCE_IDENTITIES[key]
    else:
        _, _, (domain, identity, _) = item_for(key)
    require(row.get("domain") == domain and row.get("paper_url") in {
                f"https://arxiv.org/abs/{identity}", f"https://arxiv.org/abs/{identity}v1"}
            and row.get("detail_path") == f"{domain}/{identity}-{key}/README.md", "catalog paper identity differs")


def validate_receipt_binding(receipt, metric, key):
    require(receipt["adapter_key"] == key and receipt["metrics"] == metric["metrics"], "receipt/metric differs")
    require(receipt["dataset"] == metric["dataset"], "receipt dataset differs")
    require(receipt["provenance"]["commit"] == metric["provenance"]["commit"], "receipt commit differs")
    require(receipt["executed_source_sha256"] == metric["provenance"]["executed_source_sha256"], "receipt sources differ")


def finalize():
    rows = {row["key"]: row for row in catalog_records() if row["key"] in COSTS}
    require(set(rows) == set(COSTS), "accepted nineteen-paper scope incomplete")
    candidates = []
    counts = {"gpu_validated_components": 0, "cpu_validated_components_or_interfaces": 0, "review_only": 0}
    for key, row in sorted(rows.items()):
        validate_catalog_identity(row)
        require(row.get("full_experiment_status") == "not_reproduced_high_cost", "full reproduction boundary missing")
        require(row.get("promotion_eligible") is False and row.get("evolve_integrated") is False, "promotion forbidden")
        validation = {"status": "review_only_not_reproduced", "gpu_validation_passed": False}
        if key in REFERENCES:
            require(row.get("review_done") is True and row.get("implementation_status") == "deferred_high_cost",
                    "reference review not closed")
            require(not row.get("local_operator") and not row.get("gpu_validation_artifact"), "reference is not executable")
            counts["review_only"] += 1
        else:
            device, _, (domain, identity, _) = item_for(key)
            artifact = f"docs/{domain}/{identity}-{key}/metrics/component-{device}-seeds42-44.json"
            metric = json.loads((ROOT / artifact).read_text())
            validate_curated(metric, key)
            validation.update(status="validated_bounded_diagnostic", metrics=[artifact], code_commit=metric["provenance"]["commit"])
            if device == "cuda":
                receipt = load_gpu_receipt(ROOT / row["gpu_validation_artifact"])
                validate_receipt_binding(receipt, metric, key)
                validation.update(gpu_validation_passed=True, gpu_validation_artifact=row["gpu_validation_artifact"])
                counts["gpu_validated_components"] += 1
            else:
                require(not row.get("requires_gpu_validation") and not row.get("gpu_validation_artifact"), "CPU must not invent GPU evidence")
                counts["cpu_validated_components_or_interfaces"] += 1
        candidates.append({
            "id": re.search(r"\d{4}\.\d{4,5}", row["paper_url"]).group(), "key": key, "title": row["title"],
            "priority": row.get("priority", "P1"), "publication_date": row["published"],
            "track": {"foundation-models": "foundation-model", "post-training": "post-training", "agent-research": "agent"}[row["domain"]],
            "intake_class": "announcement-overlap-new-to-review", "status": "deferred", "status_scope": "full_paper_reproduction",
            "resolution": "not_reproduced_high_cost", "full_experiment_status": "not_reproduced_high_cost",
            "review_done": True, "terminal": True, "automatic_retry": False, "automatic_implementation_queue": False,
            "reason": "成本过高，不复现（审查 DONE）。" + COSTS[key],
            "cost_assessment": {"basis": COSTS[key], "source_url": row["paper_url"],
                                "available_resource": "单张A100或A30，或本地Mac；不假设多卡/同时占用两机",
                                "cost_type": "published_configuration_not_local_measurement"},
            "doc": row["detail_path"], "implementation_status": row["implementation_status"],
            "bounded_implementation_scope": row["summary"], "local_operator": row.get("local_operator"),
            "local_command": row.get("local_command"), "component_validation": validation,
            "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
            "source_provenance": [{"source_kind": "original-paper", "source_url": row["paper_url"]}],
        })
    require(counts == {"gpu_validated_components": 10, "cpu_validated_components_or_interfaces": 6, "review_only": 3},
            "acceptance counts differ")
    path = ROOT / "docs/paper-discovery-ledger.json"
    ledger = json.loads(path.read_text())
    batch = {"batch": BATCH, "date": "2026-10-18", "scope_kind": "selected-paper-implementation",
             "window": "Oct16 announcements, Oct14–15 v1 overlap; not Oct18 new publications or full-source closure",
             "required_tracks": ["foundation-model", "post-training", "agent"],
             "coverage_complete": False, "review_watermark_advanced": False, "review_snapshot_modified": False,
             "scope_artifact": "research-audits/oct18-components/README.md", "component_validation_counts": counts,
             "accepted_scope_counts": {"bounded_components_and_interfaces": 16, "review_only_papers": 3},
             "candidates": candidates}
    ledger["batches"] = [item for item in ledger["batches"] if item["batch"] != BATCH] + [batch]
    write_json(path, ledger)
    print(json.dumps(counts))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("group", choices=(*GROUPS, "finalize"))
    parser.add_argument("input", type=Path, nargs="?")
    args = parser.parse_args()
    if args.group == "finalize":
        finalize()
    elif args.input is None:
        parser.error("raw measured runner output required")
    else:
        curate(args.input, args.group)


if __name__ == "__main__":
    main()
