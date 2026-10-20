#!/usr/bin/env python3
"""Admit actual frozen Oct20 diagnostics, not full paper capability."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from auto_research.gpu_validation import load_gpu_receipt  # noqa: E402
from auto_research.paper_specs.catalog import catalog_records  # noqa: E402
from curate_oct18_component_evidence import aggregate, generated_input_fingerprint, reject_failure, require, write_json  # noqa: E402
from oct18_frozen_sources import capture_sources, verify_sources  # noqa: E402

SEEDS = [42, 43, 44]
BATCH = "2026-10-20-new-announcement-components"
AUDIT = ROOT / "docs/research-audits/oct20-components"
SOURCE_PROOFS = AUDIT / "frozen-sources.json"
GROUPS = {
    "foundation": ("cuda", "scripts/run_oct20_foundation_components.py", {
        "t-muon": "foundation_models/t_muon", "time-jepa": "foundation_models/time_jepa", "kronlstm": "foundation_models/kronlstm"}),
    "post": ("cuda", "scripts/run_oct20_post_components.py", {
        "spod": "post_training/spod", "apsd": "post_training/apsd", "tar-adaptive-replay": "post_training/tar"}),
    "agent": ("cpu", "scripts/run_oct20_agent_components.py", {
        "memprice": "agent_research/memprice", "scope-replay": "agent_research/scope_replay", "tokenworth": "agent_research/tokenworth"}),
    "sid": ("cpu", "scripts/run_oct20_sid_topology.py", {"sid-topology": "reproductions/sid_topology"}),
}
REFERENCES = {"maps-creative", "muse-glimmer-30b", "world-of-swecraft"}
COSTS = {
    "t-muon": "最大1.3B模型与13.1B训练tokens的多优化器比较矩阵。",
    "time-jepa": "ViT-g/16、8GPU、三个物理视频领域各20epoch及后续探针/外部评测。",
    "kronlstm": "1.5B模型、100B tokens，16节点每节点4张GH200。",
    "spod": "27B/31B教师与2B/E4B学生，双GPU、三环境、40–50更新与频繁评估。",
    "apsd": "4张H200，每run约5小时，7B/8B与长rollout；另有RLRF矩阵。",
    "tar-adaptive-replay": "7500题每题128基础采样及BGE-M3；双A6000/A100完整训练每run不超过15小时。",
    "memprice": "完整LLM估值、写记忆和多任务交互矩阵超出组件级预算。",
    "scope-replay": "完整机器人仿真与策略矩阵使用8张PRO6000和8张A100。",
    "tokenworth": "Qwen2.5-14B、A800与外部DeepSeek调用，3环境9基线完整矩阵。",
    "sid-topology": "64GPU、9000万/2000万私有日志、RQ-VAE与Qwen2.5-0.5B三阶段训练及生产A/B。",
    "maps-creative": "Qwen3-VL-32B/8B、Kling-Omni，8H100、SFT20epoch再RL5000步及私有线上闭环。",
    "muse-glimmer-30b": "约30B密集模型、Muse Spark教师、多阶段预训练/OPD/RL，128K长轨迹与多域评测。",
    "world-of-swecraft": "8模型、55K会话、180B以上tokens、超过10000小时Agent工作及隔离软件世界。",
}
CHECKS = {
    "memprice": {"maximum_objective_reference_error": ("max", 1e-10), "hard_budget_violations": ("equal", 0),
        "greedy_negative_control_gap": ("positive", 0), "pressure_induced_token_reduction": ("positive", 0),
        "persistent_queue_and_clock_after_refresh": ("is", True), "rejected_invalid_allocations": ("equal", 2),
        "forbidden_query_or_gold_allocator_parameters": ("equal", 0)},
    "scope-replay": {"false_certificates_under_faults": ("equal", 0), "instance_transfer_certificates": ("equal", 0),
        "fixture_witnesses": ("positive", 0), "full_stateful_certificates": ("positive", 0),
        "broken_replay_negative_control_failures": ("positive", 0), "unsupported_graphs_retained_unavailable": ("positive", 0),
        "instance_mismatch_rejected": ("is", True)},
    "tokenworth": {"maximum_kernel_reference_error": ("max", 1e-10), "gradient_finite_difference_error": ("max", 1e-5),
        "agop_metric_shift": ("positive", 0), "base_logistic_loss_reduction": ("positive", 0), "fit_updates": ("positive", 0),
        "maximum_bank_capacity_violation": ("equal", 0), "chronology_violation_rejections": ("equal", 1),
        "admit_only_negative_control_bad_admissions": ("equal", 1), "private_gold_fields_in_actor_selection": ("equal", 0),
        "final_metric_mean_error": ("max", 1e-10), "final_weights_change": ("positive", 0)},
    "t-muon": {"gradient_reference_max_error": ("max", 1e-9), "transform_polar_reference_max_error": ("max", 1e-9),
        "optimizer_update_reference_max_error": ("max", 1e-9), "momentum_reference_max_error": ("max", 1e-9),
        "zero_tensor_update_max": ("equal", 0), "gradient_norm": ("positive", 0), "parameter_update_norm": ("positive", 0),
        "unfolded_muon_negative_difference_norm": ("positive", 0), "optimizer_steps": ("equal", 2), "tested_transforms": ("equal", 4)},
    "time-jepa": {"joint_loss_reference_absolute_error": ("max", 1e-9), "loss_gradient_reference_max_error": ("max", 1e-9),
        "ema_reference_max_error": ("max", 1e-9), "teacher_gradient_norm": ("equal", 0), "target_optimizer_update_max": ("equal", 0),
        "state_target_gradient_norm": ("equal", 0), "masked_context_leak_max": ("equal", 0), "normalizer_mutation_max": ("equal", 0),
        "validation_fit_rejected": ("is", True), "gradient_norm": ("positive", 0), "parameter_update_norm": ("positive", 0),
        "auxiliary_online_gradient_norm": ("positive", 0), "latent_online_gradient_norm": ("positive", 0),
        "unmasked_auxiliary_sensitivity": ("positive", 0), "shuffled_state_loss_absolute_delta": ("positive", 0)},
    "kronlstm": {"recurrence_read_reference_max_error": ("max", 1e-9), "recurrence_state_reference_max_error": ("max", 1e-9),
        "gradient_reference_max_error": ("max", 1e-9), "causal_prefix_max_error": ("max", 1e-9),
        "key_norm_max_error": ("max", 1e-9), "value_norm_max_error": ("max", 1e-9),
        "gradient_norm": ("positive", 0), "gate_gradient_norm": ("positive", 0), "parameter_update_norm": ("positive", 0),
        "vector_deltanet_negative_difference_norm": ("positive", 0)},
    "spod": {"parameter_delta_l2": ("positive", 0), "gradient_norm_min": ("positive", 0), "optimizer_updates": ("equal", 3),
        "loss_reference_max_abs_error": ("max", 1e-9), "protected_decisions_total": ("positive", 0),
        "floor_without_mask_negative_control_difference_max": ("positive", 0), "teacher_parameter_delta_l2": ("equal", 0),
        "teacher_gradient_count": ("equal", 0), "raw_model_logits_used": ("is", True),
        "evaluation_outcomes_used_by_gate": ("is", False), "agent_benchmark_evaluated": ("is", False)},
    "apsd": {"parameter_delta_l2": ("positive", 0), "gradient_norm_min": ("positive", 0), "optimizer_updates": ("equal", 3),
        "loss_reference_max_abs_error": ("max", 1e-9), "logit_gradient_reference_max_abs_error": ("max", 1e-9),
        "finite_difference_max_abs_error": ("max", 1e-7), "detached_target_negative_control_gradient_difference_min": ("positive", 0),
        "self_teacher_parameter_delta_during_update_max": ("equal", 0), "self_teacher_gradient_count": ("equal", 0)},
    "tar-adaptive-replay": {"parameter_delta_l2": ("positive", 0), "gradient_norm_min": ("positive", 0), "optimizer_updates": ("equal", 3),
        "loss_reference_max_abs_error": ("max", 1e-9), "replay_gradient_reference_max_abs_error": ("max", 1e-9),
        "replay_gradient_norm_max": ("positive", 0), "nonzero_replay_updates": ("positive", 0),
        "bank_trajectory_count": ("positive", 0), "ungated_sft_negative_control_difference_max": ("positive", 0),
        "base_parameter_delta_l2": ("equal", 0), "base_gradient_count": ("equal", 0)},
    "sid-topology": {"old_sid_remapped_fraction": ("equal", 0), "full_remap_negative_control_fraction": ("positive", 0),
        "frozen_old_path_address_recovery": ("equal", 1), "full_remap_old_address_losses": ("positive", 0),
        "insertion_order_mismatches": ("equal", 0), "input_mapping_mutated": ("is", False),
        "learned_retriever_evaluated": ("is", False), "production_ab_reproduced": ("is", False)},
}


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False).encode()).hexdigest()


def item_for(key):
    matches = [(group, device, runner, module) for group, (device, runner, items) in GROUPS.items() for k, module in items.items() if k == key]
    require(len(matches) == 1, "unknown component")
    return matches[0]


def catalog_for(key):
    catalog_key = key
    rows = [r for r in catalog_records() if r["key"] == catalog_key]
    require(len(rows) == 1, "catalog identity must be unique")
    return rows[0]


def metric_path(key):
    _, device, _, _ = item_for(key)
    return "docs/" + str(Path(catalog_for(key)["detail_path"]).parent / "metrics" / f"component-{device}-seeds42-44.json")


def source_hashes(commit, hashes, *, portable=False):
    require(re.fullmatch(r"[0-9a-f]{40}", str(commit)), "full frozen commit required")
    for name, value in hashes.items():
        path = (ROOT / name).resolve()
        require(path.is_relative_to(ROOT) and path.is_file(), "invalid source path")
        require(hashlib.sha256(path.read_bytes()).hexdigest() == value, "current executed source differs")
        if not portable:
            frozen = subprocess.check_output(["git", "show", f"{commit}:{name}"], cwd=ROOT, stderr=subprocess.DEVNULL)
            require(hashlib.sha256(frozen).hexdigest() == value, "unfrozen executed source")
    if portable:
        record = json.loads(SOURCE_PROOFS.read_text())["commits"][commit]
        require(all(record["executed_source_sha256"].get(p) == h for p, h in hashes.items()), "unproven digest")
        verify_sources(ROOT, commit, hashes, {**record["proof"], "paths": sorted(hashes)})


def boundaries(value):
    reject_failure(value)
    require(value.get("diagnostic_only") is True and value.get("promotion_eligible") is False
            and value.get("evolve_integrated") is False, "diagnostic/no-promotion boundary missing")


def validate_outcomes(key, metrics):
    aggregate([{"seed": seed, "metrics": metrics} for seed in SEEDS])  # finite scalar/boolean schema
    require(key in CHECKS and len(CHECKS[key]) >= 4, "defining acceptance gates required")
    for name, (kind, bound) in CHECKS[key].items():
        value = metrics.get(name)
        if kind == "is":
            require(value is bound, f"{key}: {name} boundary differs")
        else:
            require(type(value) in (int, float), f"{key}: missing {name}")
            passed = value == bound if kind == "equal" else 0 <= value <= bound if kind == "max" else value > bound
            require(passed, f"{key}: {name} failed {kind} gate")
    if key == "scope-replay":
        witnesses = metrics["fixture_witnesses"]
        require(metrics["full_stateful_certificates"] == metrics["broken_replay_negative_control_failures"]
                == metrics["unsupported_graphs_retained_unavailable"] == witnesses
                and metrics.get("fault_injections") == 5 * witnesses, "stateful fault coverage differs")


def expected_sources(group):
    _, runner, items = GROUPS[group]
    sources = {runner, *(f"src/auto_research/{module}.py" for module in items.values())}
    return sources


def validate_dataset(dataset, key, group, hashes):
    expected_id = "synthetic-sid-topology-mapping-fixture" if group == "sid" else f"synthetic:oct20-{key}-v1"
    expected_revision = "oct20-sid-topology-v1" if group == "sid" else "sha256:" + hashes[GROUPS[group][1]]
    require(dataset.get("id") == expected_id and dataset.get("revision") == expected_revision,
            "fixed executed input recipe differs")
    require(dataset.get("capability_benchmark") is False and not dataset.get("public_benchmark_evaluated"),
            "fixture cannot be promoted to a public capability benchmark")


def validate_payload(payload, group):
    boundaries(payload)
    device, _, items = GROUPS[group]
    require(payload.get("seeds") == SEEDS and payload.get("device") == device, "device/seeds differ")
    require(not payload.get("executed_source_uncommitted"), "uncommitted execution")
    hashes = payload.get("executed_source_sha256", {})
    require(set(hashes) == expected_sources(group), "executed source scope differs")
    source_hashes(payload.get("code_commit"), hashes)
    if device == "cuda":
        model = payload.get("accelerator", "").upper()
        require("NVIDIA" in model and any(name in model for name in ("A100", "A30")), "actual A100/A30 required")
    require(set(payload.get("components", {})) == set(items), "component scope differs")
    for key, component in payload["components"].items():
        boundaries(component)
        require(component.get("full_experiment_status") == "not_reproduced_high_cost", "cost decision missing")
        rows = component.get("per_seed", [])
        reduced = aggregate(rows)
        # Older runners report plain scalar means; the curated schema is uniform.
        for name, reported in component.get("metrics", {}).items():
            expected = reduced[name]
            if isinstance(reported, dict):
                require(reported == expected, "runner aggregate differs")
            elif type(reported) is bool:
                require(reported is expected, "runner boolean aggregate differs")
            else:
                require(reported == expected["mean"], "runner scalar mean differs")
        dataset = component.get("dataset", {})
        require(isinstance(dataset.get("id"), str) and dataset["id"].startswith("synthetic") and dataset.get("revision"), "fixed synthetic recipe required")
        require(not dataset.get("capability_benchmark") and not dataset.get("public_benchmark_evaluated"), "fixture promoted")
        validate_dataset(dataset, key, group, hashes)
        for row in rows:
            validate_outcomes(key, row["metrics"])


def validate_curated(metric, key):
    boundaries(metric)
    group, device, _, _ = item_for(key)
    require(metric.get("method") == key and metric.get("seeds") == SEEDS, "curated identity differs")
    require(metric.get("manifest_ref") == f"{catalog_for(key)['domain']}:{catalog_for(key)['key']}", "manifest differs")
    protocol = metric.get("evaluation_protocol", {})
    require(metric.get("evaluation_tier") == "l1_mechanism" and protocol.get("tier") == "l1_mechanism"
            and protocol.get("seeds") == SEEDS and protocol.get("formal_comparison") is False, "mechanism evidence cannot be promoted to formal capability comparison")
    require(not metric["dataset"].get("capability_benchmark") and not metric["dataset"].get("public_benchmark_evaluated"), "fixture cannot be advertised as public benchmark")
    require(metric.get("full_experiment_status") == "not_reproduced_high_cost" and metric.get("full_experiment_review_done") is True, "full experiment mislabeled")
    require(metric.get("metrics") == aggregate(metric.get("per_seed", [])), "curated aggregation differs")
    provenance = metric.get("provenance", {})
    hashes = provenance.get("executed_source_sha256", {})
    require(set(hashes) == expected_sources(group), "curated source scope differs")
    validate_dataset(metric["dataset"], key, group, hashes)
    source_hashes(provenance.get("commit"), hashes, portable=True)
    require(provenance.get("artifact_path") == metric_path(key), "metric path binding differs")
    require(provenance.get("dataset_fingerprint") == generated_input_fingerprint(metric["dataset"], hashes), "recipe fingerprint differs")
    require(re.fullmatch(r"[0-9a-f]{64}", str(provenance.get("raw_runner_artifact_sha256"))), "raw digest missing")
    for row in metric["per_seed"]:
        require(set(row) <= {"seed", "metrics", "audit_sha256", "fixture_sha256"}, "raw trajectory must not be copied into curated metrics")
        require(re.fullmatch(r"[0-9a-f]{64}", str(row.get("audit_sha256"))), "audit digest missing")
        validate_outcomes(key, row["metrics"])
    if device == "cuda":
        receipt = load_gpu_receipt(ROOT / catalog_for(key)["gpu_validation_artifact"])
        validate_receipt_binding(receipt, metric, key)


def validate_receipt_binding(receipt, metric, key):
    boundaries(receipt)
    _, device, runner, _ = item_for(key)
    require(device == "cuda" and receipt.get("adapter_key") == key, "receipt identity differs")
    require(receipt.get("result") == "passed" and receipt.get("full_experiment_status") == "not_reproduced_high_cost"
            and receipt.get("full_experiment_review_done") is True, "receipt must preserve bounded result and full-experiment cost closure")
    provenance = metric["provenance"]
    require(receipt.get("seeds") == SEEDS and receipt.get("metrics") == metric["metrics"], "receipt outcomes differ")
    require(receipt.get("dataset") == metric["dataset"] and receipt.get("executed_source_sha256") == provenance["executed_source_sha256"], "receipt inputs differ")
    require(receipt.get("accelerator") == {"vendor": "NVIDIA", "model": provenance["accelerator"], "count": 1}, "accelerator differs")
    require(any(x in provenance["accelerator"].upper() for x in ("A100", "A30")), "unsupported accelerator")
    require(receipt.get("provenance", {}).get("commit") == provenance["commit"]
            and receipt["provenance"].get("metric_artifact_path") == metric_path(key)
            and receipt["provenance"].get("artifact_path") == catalog_for(key)["gpu_validation_artifact"], "receipt provenance differs")
    require(all(receipt["provenance"].get(field) == provenance.get(field)
                for field in ("raw_runner_artifact_sha256", "dataset_fingerprint")), "receipt raw-input provenance binding differs")
    prefix = ["python", runner, "--device", "cuda", "--seeds", "42,43,44", "--code-commit", provenance["commit"], "--output"]
    command = receipt.get("command", [])
    require(isinstance(command, list) and command[:-1] == prefix and command[-1] == "results/" + Path(command[-1]).name, "actual command shape differs")
    require(receipt.get("checkpoint") == {"public_id": "none-seeded-component-initialization", "revision": provenance["commit"], "pretrained": False}, "checkpoint differs")


def curate(path, group):
    payload = json.loads(path.read_text())
    validate_payload(payload, group)
    commit, hashes = payload["code_commit"], payload["executed_source_sha256"]
    bundle = json.loads(SOURCE_PROOFS.read_text()) if SOURCE_PROOFS.exists() else {"schema_version": 1, "commits": {}}
    previous = bundle["commits"].get(commit, {})
    old_hashes = previous.get("executed_source_sha256", {})
    require(all(p not in old_hashes or old_hashes[p] == h for p, h in hashes.items()), "same-commit digest conflict")
    proof = capture_sources(ROOT, commit, hashes)
    objects = previous.get("proof", {}).get("objects", {})
    require(all(p not in objects or objects[p] == h for p, h in proof["objects"].items()), "Merkle object conflict")
    combined = {**old_hashes, **hashes}
    bundle["commits"][commit] = {"executed_source_sha256": combined,
        "proof": {**proof, "paths": sorted(combined), "objects": {**objects, **proof["objects"]}}}
    write_json(SOURCE_PROOFS, bundle)
    for key, component in payload["components"].items():
        _, device, runner, _ = item_for(key)
        artifact = metric_path(key)
        rows = []
        for row in component["per_seed"]:
            audit = {k: v for k, v in row.items() if k not in {"seed", "metrics", "status"}}
            rows.append({"seed": row["seed"], "metrics": row["metrics"], "audit_sha256": digest(audit),
                         **({"fixture_sha256": row["fixture_sha256"]} if "fixture_sha256" in row else {})})
        common = {"diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
                  "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True}
        provenance = {"commit": commit, "artifact_path": artifact, "raw_runner_artifact_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "executed_source_sha256": hashes, "accelerator": payload.get("accelerator", "CPU"),
            "dataset_fingerprint": generated_input_fingerprint(component["dataset"], hashes)}
        metric = {"schema_version": 2, "method": key, "manifest_ref": f"{catalog_for(key)['domain']}:{catalog_for(key)['key']}",
            "seeds": SEEDS, "dataset": component["dataset"], "evaluation_tier": "l1_mechanism", "per_seed": rows,
            "metrics": aggregate(rows), "evaluation_protocol": {"tier": "l1_mechanism", "seeds": SEEDS, "formal_comparison": False,
                "claim_policy": "synthetic mechanism/protocol diagnostics only; not official model/Agent capability or end-to-end performance"},
            "provenance": provenance, **common}
        write_json(ROOT / artifact, metric)
        if device == "cuda":
            receipt_path = catalog_for(key)["gpu_validation_artifact"]
            receipt = {"schema_version": 1, "adapter_key": key, "validated_at": "2026-10-20",
                "accelerator": {"vendor": "NVIDIA", "model": payload["accelerator"], "count": 1},
                "command": ["python", runner, "--device", "cuda", "--seeds", "42,43,44", "--code-commit", commit, "--output", f"results/{path.name}"],
                "dataset": component["dataset"], "checkpoint": {"public_id": "none-seeded-component-initialization", "revision": commit, "pretrained": False},
                "seeds": SEEDS, "result": "passed", "metrics": metric["metrics"], "executed_source_sha256": hashes,
                "provenance": {**provenance, "artifact_path": receipt_path, "metric_artifact_path": artifact}, **common}
            write_json(ROOT / receipt_path, receipt)
        print(artifact)


def finalize():
    candidates = []
    for key in COSTS:
        row = catalog_for(key)
        boundaries(row)
        require(row.get("full_experiment_status") == "not_reproduced_high_cost" and row.get("review_done") is True, "catalog cost closure missing")
        validation = {"status": "review_only_not_reproduced", "gpu_validation_passed": False}
        if key in REFERENCES:
            require(row.get("implementation_status") == "deferred_high_cost" and not row.get("local_operator")
                    and not row.get("requires_gpu_validation") and not row.get("gpu_validation_artifact") and row.get("adapter") is None, "reference cannot claim execution")
        else:
            metric = json.loads((ROOT / metric_path(key)).read_text())
            validate_curated(metric, key)
            _, device, _, _ = item_for(key)
            require(row.get("requires_gpu_validation", False) is (device == "cuda"), "catalog GPU gate differs")
            validation.update(status="validated_bounded_diagnostic", metrics=[metric_path(key)], code_commit=metric["provenance"]["commit"], gpu_validation_passed=device == "cuda")
            if device == "cuda":
                validation["gpu_validation_artifact"] = row["gpu_validation_artifact"]
        candidates.append({"id": re.search(r"\d{4}\.\d{4,5}", row["paper_url"]).group(), "key": row["key"],
            "component_key": key if key != row["key"] else None, "title": row["title"], "priority": row.get("priority", "P1"),
            "track": {
                "foundation-models": "foundation-model", "post-training": "post-training", "agent-research": "agent", "recommendation": "recommendation"}[row["domain"]],
            "publication_date": row["published"], "intake_class": "new-announcement-new-to-review",
            "status": "deferred", "status_scope": "full_paper_reproduction", "resolution": "not_reproduced_high_cost",
            "full_experiment_status": "not_reproduced_high_cost", "review_done": True, "terminal": True,
            "automatic_retry": False, "automatic_implementation_queue": False,
            "reason": "成本过高，不复现（审查 DONE）。" + COSTS[key],
            "cost_assessment": {"basis": COSTS[key], "source_url": row["paper_url"], "available_resource": "单张A100或A30，或Mac",
                "cost_type": "published_configuration_not_local_measurement"}, "doc": row["detail_path"],
            "implementation_status": row["implementation_status"], "bounded_implementation_scope": row["summary"],
            "local_operator": row.get("local_operator"), "component_validation": validation,
            "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
            "source_provenance": [{"source_kind": "original-paper", "source_url": row["paper_url"]}]})
    path = ROOT / "docs/paper-discovery-ledger.json"
    ledger = json.loads(path.read_text())
    batch = {"batch": BATCH, "date": "2026-10-20", "scope_kind": "selected-paper-implementation", "coverage_complete": False,
        "window": "Oct20 announcements: distinct v1 dates; not thirteen papers first published today",
        "required_tracks": ["recommendation", "foundation-model", "post-training", "agent"],
        "review_watermark_advanced": False, "review_snapshot_modified": False,
        "scope_artifact": "research-audits/oct20-components/README.md",
        "accepted_scope_counts": {"bounded_components_and_interfaces": 10, "review_only_papers": 3},
        "component_validation_counts": {"gpu_validated_components": 6, "cpu_validated_components_or_interfaces": 4, "review_only": 3},
        "candidates": candidates}
    ledger["batches"] = [b for b in ledger["batches"] if b["batch"] != BATCH] + [batch]
    write_json(path, ledger)
    print(json.dumps(batch["component_validation_counts"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("group", choices=(*GROUPS, "finalize"))
    parser.add_argument("input", type=Path, nargs="?")
    args = parser.parse_args()
    if args.group == "finalize":
        finalize()
    elif args.input is None:
        parser.error("actual immutable runner output required")
    else:
        curate(args.input, args.group)


if __name__ == "__main__":
    main()
