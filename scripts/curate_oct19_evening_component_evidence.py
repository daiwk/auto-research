#!/usr/bin/env python3
"""Admit actual frozen Oct19-evening diagnostics, not full paper capability."""
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
BATCH = "2026-10-19-evening-new-announcements-and-unirec-v3"
AUDIT = ROOT / "docs/research-audits/oct19-evening-components"
SOURCE_PROOFS = AUDIT / "frozen-sources.json"
GROUPS = {
    "foundation": ("cuda", "scripts/run_oct19_evening_foundation_components.py", {
        "ego-p2c": "foundation_models/ego_p2c", "bmuon": "foundation_models/bmuon", "sink-sparse": "foundation_models/sink_sparse"}),
    "post": ("cuda", "scripts/run_oct19_evening_post_components.py", {
        "treeopsd": "post_training/tree_opsd", "simopd": "post_training/sim_opd", "gr-opd": "post_training/gr_opd"}),
    "agent": ("cpu", "scripts/run_oct19_evening_agent_components.py", {
        "proper-agent": "agent_research/proper_agent", "harness-decomposition": "agent_research/harness_decomposition", "drago": "agent_research/drago"}),
    "unirec": ("cuda", "scripts/run_oct19_evening_unirec_components.py", {"unirec-v3-components": "reproductions/unirec/v3_objectives"}),
    "system-one": ("cpu", "scripts/run_oct19_evening_system_one.py", {"jev-portuguese-ir": "system_one/portuguese_ir"}),
}
REFERENCES = {"ppmem", "mge-po", "multiagent-opd"}
COSTS = {
    "ego-p2c": "8B、8张H100、多阶段SFT/GRPO与600次MOPD更新。",
    "bmuon": "1B、13.1B tokens、8张H100，每seed约8.4小时。",
    "sink-sparse": "81帧视频、50步扩散、多prompt校准与生成质量/系统评测；不以小算子冒充内核加速。",
    "ppmem": "5B Wan、80K以上视频、约12K次两阶段训练，第二阶段仍377M可训练参数。",
    "treeopsd": "4B/30B-A3B、单节点8 GPU、100次策略更新与60/80回合深度研究轨迹。",
    "simopd": "8张A100、每配置200步，每步87.2秒约4.84小时，尚未计完整评估。",
    "gr-opd": "8张H20、64 prompt乘8 response、最长28672 tokens、221 rollout step与多模型配对。",
    "mge-po": "2张H200、约22.6小时完整RL与评估矩阵。",
    "multiagent-opd": "约17万训练题、先教师后学生的两阶段多工作流搜索及长环境轨迹。",
    "proper-agent": "27B GRPO、7张H100、14.6小时；ProPerMem数据和作者代码待发布。",
    "harness-decomposition": "原文11模型、3框架、4任务共25配置，包含大量演化、代码容器和重评估。",
    "drago": "4张A100、PDDL/SMT/MiniZinc完整多模型协议与规划环境。",
    "unirec-v3-components": "RecFlow 1.9B阶段记录、七头DSSM/DIN预训再融合训练，另含百万请求私有日志与生产A/B。",
    "jev-portuguese-ir": "封闭Jev API的13200次相关性判断与50000重排对（5000个重排请求）；原文未给时间/费用。",
}
CHECKS = {
    "ego-p2c": {"loss_reference_max_error": ("max", 1e-9), "logit_gradient_reference_max_error": ("max", 1e-9),
        "rollout_rescore_max_error": ("max", 1e-9), "trainable_gradient_norm": ("positive", 0), "parameter_update_norm": ("positive", 0),
        "teacher_gradient_norm": ("max", 0), "frozen_parameter_update_max": ("max", 0), "perception_private_context_rejected": ("equal", 1),
        "wrong_teacher_loss_absolute_delta": ("positive", 0)},
    "bmuon": {"allocation_reference_max_error": ("max", 1e-9), "parameter_update_reference_max_error": ("max", 1e-9),
        "global_budget_absolute_error": ("max", 1e-9), "parameter_update_norm": ("positive", 0), "gradient_norm": ("positive", 0),
        "ordinary_muon_direction_difference_norm": ("positive", 0)},
    "sink-sparse": {"virtual_union_reference_max_error": ("max", 1e-9), "gradient_reference_max_error": ("max", 1e-9),
        "parameter_update_norm": ("positive", 0), "gradient_norm": ("positive", 0), "calibration_mask_mutation_count": ("max", 0),
        "fixed_average_negative_max_difference": ("positive", 0), "missing_pool_correction_negative_max_difference": ("positive", 0)},
    "treeopsd": {"parameter_delta_l2": ("positive", 0), "gradient_norm_min": ("positive", 0), "optimizer_updates": ("equal", 3),
        "credit_reference_max_abs_error": ("max", 1e-9), "loss_reference_max_abs_error": ("max", 1e-9),
        "shared_prefix_turn_savings_min": ("positive", 0), "target_gradient_max_abs_error": ("max", 1e-9),
        "overshoot_loss_gradient": ("positive", 0), "behavior_parameter_delta_l2": ("max", 0), "behavior_gradient_count": ("max", 0),
        "real_search_or_task_capability_evaluated": ("is", False)},
    "simopd": {"parameter_delta_l2": ("positive", 0), "gradient_norm_min": ("positive", 0), "optimizer_updates": ("equal", 3),
        "loss_reference_max_abs_error": ("max", 1e-9), "mispaired_bank_negative_control_abs_difference_min": ("positive", 0),
        "teacher_parameter_delta_l2": ("max", 0), "teacher_gradient_count": ("max", 0), "warmup_optimizer_updates": ("max", 0),
        "paired_preupdate_fifo_verified": ("is", True), "pretrained_teacher_capability_evaluated": ("is", False)},
    "gr-opd": {"parameter_delta_l2": ("positive", 0), "gradient_norm_min": ("positive", 0), "optimizer_updates": ("equal", 3),
        "credit_reference_max_abs_error": ("max", 1e-9), "loss_reference_max_abs_error": ("max", 1e-9),
        "global_token_weighting_negative_control_abs_difference_max": ("positive", 0), "teacher_parameter_delta_l2": ("max", 0),
        "teacher_gradient_count": ("max", 0), "raw_sum_unbiasedness_claimed_for_practical_estimator": ("is", False), "formal_math_benchmark_evaluated": ("is", False)},
    "proper-agent": {"future_memory_exposures": ("max", 0), "gold_fields_in_actor_view": ("max", 0),
        "retained_unscored_clips": ("positive", 0), "rejected_nonretrieved_provenance": ("positive", 0),
        "oracle_always_speak_negative_control_overtrigger_rate": ("positive", 0)},
    "harness-decomposition": {"raw_identity_error": ("max", 1e-10), "rejected_invalid_controls": ("positive", 0),
        "noise_control_attributed": ("max", 0), "gain_only_negative_control_overstatement": ("positive", 0)},
    "drago": {"blocked_goal_weakening_repairs": ("positive", 0), "delete_relaxation_unreachable_findings": ("positive", 0),
        "budget_exhaustion_retained_as_unknown": ("positive", 0), "gold_inputs_to_proposer": ("max", 0)},
    "unirec-v3-components": {"cppa_value_reference_max_error": ("max", 1e-9), "cppa_gradient_reference_max_error": ("max", 1e-9),
        "no_pruning_equivalence_max_error": ("max", 1e-9), "capp_pair_reference_errors": ("max", 0), "agrr_kl_reference_max_error": ("max", 1e-9),
        "group_shift_invariance_max_error": ("max", 1e-9), "reward_reference_max_error": ("max", 1e-9), "score_update_norm": ("positive", 0),
        "ranking_target_gradient_blocked": ("is", True), "majority_collapse_negative_control_difference": ("positive", 0)},
    "jev-portuguese-ir": {"batched_ranking_reference_errors": ("max", 0), "invalid_response_negative_controls_rejected": ("equal", 4),
        "linear_ndcg_reference_max_error": ("max", 1e-10), "provider_has_gold_access": ("is", False),
        "real_backend_used": ("is", False), "language_model_evaluated": ("is", False)},
}


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False).encode()).hexdigest()


def item_for(key):
    matches = [(group, device, runner, module) for group, (device, runner, items) in GROUPS.items() for k, module in items.items() if k == key]
    require(len(matches) == 1, "unknown component")
    return matches[0]


def catalog_for(key):
    catalog_key = "unirec" if key == "unirec-v3-components" else key
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
    for name, (kind, bound) in CHECKS[key].items():
        value = metrics.get(name)
        if kind == "is":
            require(value is bound, f"{key}: {name} boundary differs")
        else:
            require(type(value) in (int, float), f"{key}: missing {name}")
            passed = value == bound if kind == "equal" else 0 <= value <= bound if kind == "max" else value > bound
            require(passed, f"{key}: {name} failed {kind} gate")


def expected_sources(group):
    _, runner, items = GROUPS[group]
    sources = {runner, *(f"src/auto_research/{module}.py" for module in items.values())}
    if group == "system-one":
        sources.add("src/auto_research/system_one/contracts.py")
    return sources


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
        expected_ids = {"foundation": "synthetic-role-decoder-mlp-attention", "post": f"synthetic:oct19-evening-{key}-v1",
            "agent": f"synthetic-{key}-contract-fixture", "unirec": "synthetic-unirec-v3-objective-fixture",
            "system-one": "synthetic-portuguese-ir-protocol-fixture"}
        expected_revisions = {"foundation": "oct19-evening-foundation-mechanisms-v1",
            "post": "sha256:" + hashes[GROUPS[group][1]], "unirec": "oct19-evening-unirec-v3-v1",
            "system-one": "oct19-evening-portuguese-ir-v1"}
        require(dataset["id"] == expected_ids[group], "fixed dataset identity differs")
        if group == "agent":
            fixtures = [row.get("fixture_sha256") for row in rows]
            require(all(re.fullmatch(r"[0-9a-f]{64}", str(f)) for f in fixtures), "fixture digests missing")
            require(dataset["revision"] == digest(fixtures), "fixture recipe differs")
        else:
            require(dataset["revision"] == expected_revisions[group], "fixed recipe revision differs")
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
            receipt = {"schema_version": 1, "adapter_key": key, "validated_at": "2026-10-19",
                "accelerator": {"vendor": "NVIDIA", "model": payload["accelerator"], "count": 1},
                "command": ["python", runner, "--device", "cuda", "--seeds", "42,43,44", "--code-commit", commit, "--output", f"results/{path.name}"],
                "dataset": component["dataset"], "checkpoint": {"public_id": "none-seeded-component-initialization", "revision": commit, "pretrained": False},
                "seeds": SEEDS, "result": "passed", "metrics": metric["metrics"], "executed_source_sha256": hashes,
                "provenance": {**provenance, "artifact_path": receipt_path, "metric_artifact_path": artifact}, **common}
            write_json(ROOT / receipt_path, receipt)
        print(artifact)
    if group == "system-one":
        audit = payload["published_table_arithmetic"]
        require(audit.get("new_model_inference") is False, "published numbers cannot be new predictions")
        write_json(AUDIT / "jev-published-table-arithmetic.json", {**audit, "code_commit": commit,
            "provenance": {"raw_runner_artifact_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}, "evidence_kind": "recalculation_of_published_aggregate_tables_not_model_evaluation"})


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
            "track": {"foundation-models": "foundation-model", "post-training": "post-training", "agent-research": "agent", "recommendation": "recommendation"}[row["domain"]],
            "publication_date": row["published"], "intake_class": "substantive-version-update-v3" if key == "unirec-v3-components" else "new-announcement-new-to-review",
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
    batch = {"batch": BATCH, "date": "2026-10-19", "scope_kind": "selected-paper-implementation", "coverage_complete": False,
        "window": "Oct19 announcements: Oct15–16 first submissions plus UniRec v3; not fourteen papers first published today",
        "required_tracks": ["recommendation", "foundation-model", "post-training", "agent", "system-one"],
        "review_watermark_advanced": False, "review_snapshot_modified": False,
        "scope_artifact": "research-audits/oct19-evening-components/README.md",
        "accepted_scope_counts": {"bounded_components_and_interfaces": 11, "review_only_papers": 3},
        "component_validation_counts": {"gpu_validated_components": 7, "cpu_validated_components_or_interfaces": 4, "review_only": 3},
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
