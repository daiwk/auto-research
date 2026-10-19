#!/usr/bin/env python3
"""Admit frozen Oct19 component measurements; never promote protocol fixtures."""
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
BATCH = "2026-10-19-overlap-and-official-delta-components"
SOURCE_PROOFS = ROOT / "docs/research-audits/oct19-components/frozen-sources.json"
GROUPS = {
    "foundation": ("cuda", "scripts/run_oct19_foundation_components.py", {
        "fpot": ("foundation-models", "2610.21257", "foundation_models/fpot"),
        "lamp": ("foundation-models", "2610.22182", "foundation_models/lamp"),
    }),
    "post-cuda": ("cuda", "scripts/run_oct19_post_components.py", {
        "knowgpo": ("post-training", "2610.22331", "post_training/reviewed_oct19"),
    }),
    "post-cpu": ("cpu", "scripts/run_oct19_post_components.py", {
        "diverge-ideation": ("post-training", "2610.22324", "post_training/reviewed_oct19"),
    }),
    "agent": ("cpu", "scripts/run_oct19_agent_components.py", {
        "alpha-diana": ("agent-research", "2610.20675", "agent_research/alpha_diana"),
        "agent-perturb": ("agent-research", "2610.21624", "agent_research/agent_perturb"),
    }),
    "skill": ("cpu", "scripts/run_oct19_skill_state.py", {
        "skill-state": ("agent-research", "2608.26263", "agent_research/skill_state"),
    }),
}
REFERENCES = {"gen4p": ("foundation-models", "2610.22371"), "auto-sft": ("agent-research", "2610.22194")}
COSTS = {
    "fpot": "原文1.5B–14B、OSTQuant/GPTQ校准、多模型九任务和专用硬件评测；本地不声称内核加速。",
    "lamp": "原文11个数据集、五种shot、三seed和多种冻结视觉骨干的完整协议；不是本地显存不足结论。",
    "gen4p": "原文约20万视频、75K步、8张H200，约0.88B可训练参数。",
    "knowgpo": "原文8 A100 SFT加64 H20 RL，32问题×16轨迹和外部verifier/搜索。",
    "diverge-ideation": "原文8 H200约10小时及大型judge/API；另有132个idea的限时付费执行。",
    "alpha-diana": "原文16张A100-80GB、多种27B/31B及远程模型完整矩阵。",
    "agent-perturb": "原文多模型Toolathlon完整12类扰动、独立语义验证和原生执行环境。",
    "auto-sft": "原文8 H800、20轮约130 GPU-hours及约1900美元API。",
    "skill-state": "原文多种Gemini/Gemma/Qwen、五seed和10–200轮长任务控制矩阵。",
}
# Each selected diagnostic must show defining behavior and an independent control.
CHECKS = {
    "fpot": {"approximate_grid_reference_max_error": ("max", 1e-10),
        "integer_shift_add_reference_max_error": ("max", 0), "ste_gradient_reference_max_error": ("max", 1e-10),
        "magnitude_without_minus_one_negative_control_error": ("positive", 0),
        "posthoc_grid_negative_control_difference": ("positive", 0),
        "weight_gradient_norm": ("positive", 0), "weight_update_norm": ("positive", 0)},
    "lamp": {"regional_kernel_reference_max_error": ("max", 1e-9),
        "residual_solve_reference_max_error": ("max", 1e-9), "cached_response_reference_max_error": ("max", 1e-9),
        "query_batch_invariance_max_error": ("max", 1e-9), "frozen_encoder_change": ("max", 0),
        "stale_support_residual_negative_control_difference": ("positive", 0),
        "prototype_gradient_norm": ("positive", 0), "prototype_update_norm": ("positive", 0)},
    "knowgpo": {"credit_reference_max_abs_error": ("max", 1e-10),
        "loss_reference_max_abs_error": ("max", 1e-10), "reference_delta_l2": ("max", 0),
        "reference_gradient_count": ("max", 0), "answer_process_max_abs_credit": ("max", 0),
        "observation_credit_max_abs_error": ("max", 0), "singleton_negative_control_max_abs_advantage": ("max", 0),
        "parameter_delta_l2": ("positive", 0), "gradient_norm_min": ("positive", 0),
        "non_singleton_group_count_last": ("positive", 0), "actor_receives_private_verifier_state": ("is", False)},
    "diverge-ideation": {"reward_and_exact_cu_reference_max_abs_error": ("max", 1e-10),
        "greedy_lower_bound_violation": ("max", 1e-10), "duplicate_negative_control_marginal_error": ("max", 0),
        "generation_order_negative_control_abs_difference": ("positive", 0),
        "invalid_schema_judge_calls": ("max", 0), "fixture_callback_calls": ("positive", 0),
        "invalid_schema_returns_no_observations": ("is", True), "actual_model_or_api_judge_used": ("is", False),
        "scientific_quality_measured": ("is", False)},
    "alpha-diana": {"independent_correct_count_error": ("max", 0),
        "ignored_unscored_negative_control_inflation": ("positive", 0),
        "latest_only_cost_negative_control_undercount": ("positive", 0),
        "blocked_unsafe_shared_memory_policies": ("positive", 1),
        "unsafe_retry_negative_control_duplicate_writes": ("positive", 0), "gold_fields_exposed_to_actor": ("max", 0)},
    "agent-perturb": {"perturbation_families": ("equal", 12), "rejected_changed_goals": ("positive", 0),
        "independent_complete_pair_count_error": ("max", 0),
        "syntax_only_negative_control_bad_goal_admissions": ("positive", 0),
        "drop_unscored_negative_control_coverage_overstatement": ("positive", 0),
        "gold_or_condition_fields_exposed_to_actor": ("max", 0)},
    "skill-state": {"public_turns": ("equal", 200), "executed_inert_actions": ("equal", 200),
        "invalid_patch_retries": ("equal", 1), "state_update_reference_max_error": ("max", 0),
        "recursive_deletion_reference_error": ("max", 0), "discarded_reasoning_replayed": ("max", 0),
        "retry_public_context_drift": ("max", 0), "prompt_character_range": ("max", 7),
        "append_only_fixture_negative_control_character_growth": ("positive", 1000)},
}


def item_for(key):
    matches = [(device, runner, items[key]) for device, runner, items in GROUPS.values() if key in items]
    require(len(matches) == 1, "key outside selected component scope")
    return matches[0]


def validate_outcomes(key, metrics):
    require(key in CHECKS, "unknown measured component")
    for name, (kind, bound) in CHECKS[key].items():
        value = metrics.get(name)
        if kind == "is":
            require(value is bound, f"{key}: {name} boundary differs")
        else:
            require(type(value) in (int, float), f"{key}: missing numeric {name}")
            passed = value == bound if kind == "equal" else 0 <= value <= bound if kind == "max" else value > bound
            require(passed, f"{key}: {name} violates {kind} bound")


def source_hashes(commit, hashes, expected, *, require_git=True):
    require(re.fullmatch(r"[0-9a-f]{40}", str(commit)), "full frozen commit required")
    require(isinstance(hashes, dict) and set(hashes) == set(expected), "executed source coverage differs")
    for name, digest in hashes.items():
        path = (ROOT / name).resolve()
        require(path.is_relative_to(ROOT) and path.is_file(), "invalid source path")
        require(hashlib.sha256(path.read_bytes()).hexdigest() == digest, f"current source differs: {name}")
        if require_git:
            try:
                frozen = subprocess.check_output(["git", "show", f"{commit}:{name}"], cwd=ROOT, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError as error:
                raise ValueError("frozen source unavailable") from error
            require(hashlib.sha256(frozen).hexdigest() == digest, "frozen source differs")
    if not require_git:
        bundle = json.loads(SOURCE_PROOFS.read_text())
        require(bundle.get("schema_version") == 1, "invalid proof bundle")
        record = bundle.get("commits", {}).get(commit)
        require(isinstance(record, dict), "commit proof unavailable")
        require(all(record.get("executed_source_sha256", {}).get(p) == h for p, h in hashes.items()), "unproven source digest")
        # Verify only this artifact's fixed scope, retaining Merkle tree objects.
        # A future change to another group must not invalidate unrelated evidence.
        proof = {**record["proof"], "paths": sorted(hashes)}
        verify_sources(ROOT, commit, hashes, proof)


def boundaries(row):
    reject_failure(row)
    require(row.get("diagnostic_only") is True and row.get("promotion_eligible") is False
            and row.get("evolve_integrated") is False, "diagnostic/no-promotion boundary missing")


def validate_dataset(key, dataset, rows, hashes):
    ids = {"fpot": "synthetic-fpot-and-native-layer-kernel-features", "lamp": "synthetic-fpot-and-native-layer-kernel-features",
        "knowgpo": "synthetic:oct19-knowledge-credit-v1", "diverge-ideation": "protocol:oct19-explicit-judge-observations-v1",
        "alpha-diana": "synthetic-alpha-diana-contract-fixture", "agent-perturb": "synthetic-agent-perturb-contract-fixture",
        "skill-state": "synthetic-skill-state-public-counter"}
    if key in {"fpot", "lamp"}:
        revision = "oct19-foundation-mechanisms-v1"
    elif key in {"knowgpo", "diverge-ideation"}:
        revision = "sha256:" + hashes["scripts/run_oct19_post_components.py"]
    elif key == "skill-state":
        revision = "oct19-skill-state-contract-v1"
    else:
        fixtures = [r.get("fixture_sha256") for r in rows]
        require(all(re.fullmatch(r"[0-9a-f]{64}", str(f)) for f in fixtures), "fixture fingerprints missing")
        revision = hashlib.sha256(json.dumps(fixtures, sort_keys=True, allow_nan=False).encode()).hexdigest()
    require(dataset.get("id") == ids[key] and dataset.get("revision") == revision, "fixed diagnostic recipe differs")
    require(not dataset.get("capability_benchmark") and not dataset.get("public_benchmark_evaluated"), "fixture promoted")


def validate_payload(payload, group):
    boundaries(payload)
    device, runner, items = GROUPS[group]
    require(payload.get("device") == device and payload.get("seeds") == SEEDS, "device or seeds differ")
    require(not payload.get("executed_source_uncommitted"), "uncommitted executed source")
    if device == "cuda":
        accelerator = payload.get("accelerator", "").upper()
        require("NVIDIA" in accelerator and any(m in accelerator for m in ("A100", "A30")), "real A100/A30 required")
    expected = {runner, *(f"src/auto_research/{module}.py" for _, _, module in items.values())}
    source_hashes(payload.get("code_commit"), payload.get("executed_source_sha256", {}), expected)
    require(set(payload.get("components", {})) == set(items), "component scope differs")
    for key, component in payload["components"].items():
        boundaries(component)
        require(component.get("full_experiment_status") == "not_reproduced_high_cost", "cost decision missing")
        dataset = component.get("dataset", {})
        validate_dataset(key, dataset, component.get("per_seed", []), payload["executed_source_sha256"])
        require(component.get("metrics") == aggregate(component.get("per_seed", [])), "aggregate differs")
        for row in component["per_seed"]:
            validate_outcomes(key, row["metrics"])
    return device, runner, items


def curate(path, group):
    payload = json.loads(path.read_text())
    device, runner, items = validate_payload(payload, group)
    bundle = json.loads(SOURCE_PROOFS.read_text()) if SOURCE_PROOFS.exists() else {"schema_version": 1, "commits": {}}
    commit = payload["code_commit"]
    previous = bundle["commits"].get(commit, {})
    previous_hashes = previous.get("executed_source_sha256", {})
    measured_hashes = payload["executed_source_sha256"]
    require(all(p not in previous_hashes or previous_hashes[p] == h for p, h in measured_hashes.items()), "same-commit source conflict")
    hashes = {**previous_hashes, **measured_hashes}
    # Capture the current executed scope only. Another scope may legitimately
    # have moved to a newer commit; its old proof must remain archived, not be
    # re-captured from changed working-tree bytes.
    fresh = capture_sources(ROOT, commit, measured_hashes)
    old_objects = previous.get("proof", {}).get("objects", {})
    require(all(oid not in old_objects or old_objects[oid] == value for oid, value in fresh["objects"].items()), "proof object conflict")
    proof = {**fresh, "paths": sorted(hashes), "objects": {**old_objects, **fresh["objects"]}}
    bundle["commits"][commit] = {"executed_source_sha256": hashes, "proof": proof}
    write_json(SOURCE_PROOFS, bundle)
    for key, (domain, identity, module) in items.items():
        component = payload["components"][key]
        artifact = f"docs/{domain}/{identity}-{key}/metrics/component-{device}-seeds42-44.json"
        sources = {p: h for p, h in payload["executed_source_sha256"].items() if p in {runner, f"src/auto_research/{module}.py"}}
        metrics = aggregate(component["per_seed"])
        common = {"diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
            "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True}
        provenance = {"commit": commit, "artifact_path": artifact,
            "dataset_fingerprint": generated_input_fingerprint(component["dataset"], sources),
            "raw_runner_artifact_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "executed_source_sha256": sources, "accelerator": payload.get("accelerator", "CPU")}
        metric = {"schema_version": 2, "method": key, "manifest_ref": f"{domain}:{key}", "seeds": SEEDS,
            "dataset": component["dataset"], "evaluation_tier": "l1_mechanism",
            "evaluation_protocol": {"tier": "l1_mechanism", "seeds": SEEDS, "formal_comparison": False,
                "claim_policy": "bounded component/protocol fixtures; not capability or official benchmark evidence"},
            "metrics": metrics, "per_seed": component["per_seed"], "provenance": provenance, **common}
        write_json(ROOT / artifact, metric)
        if device == "cuda":
            receipt_path = f"docs/gpu-validations/{key}-a100-20261019.json"
            extra = ["--methods", "knowgpo"] if group == "post-cuda" else []
            receipt = {"schema_version": 1, "adapter_key": key, "validated_at": "2026-10-19",
                "accelerator": {"vendor": "NVIDIA", "model": payload["accelerator"], "count": 1},
                "command": ["python", runner, "--device", "cuda", *extra, "--seeds", "42,43,44", "--code-commit", commit, "--output", f"results/{path.name}"],
                "dataset": component["dataset"], "checkpoint": {"public_id": "none-seeded-component-initialization", "revision": commit, "pretrained": False},
                "seeds": SEEDS, "result": "passed", "metrics": metrics, "executed_source_sha256": sources,
                "provenance": {**provenance, "artifact_path": receipt_path, "metric_artifact_path": artifact}, **common}
            write_json(ROOT / receipt_path, receipt)
        print(artifact)


def validate_curated(metric, key):
    boundaries(metric)
    device, runner, (domain, identity, module) = item_for(key)
    artifact = f"docs/{domain}/{identity}-{key}/metrics/component-{device}-seeds42-44.json"
    require(metric.get("method") == key and metric.get("manifest_ref") == f"{domain}:{key}", "curated identity differs")
    require(metric.get("seeds") == SEEDS and metric.get("metrics") == aggregate(metric.get("per_seed", [])), "curated seeds/aggregate differ")
    require(metric.get("full_experiment_status") == "not_reproduced_high_cost" and metric.get("full_experiment_review_done") is True, "curated cost decision missing")
    dataset = metric.get("dataset", {})
    protocol = metric.get("evaluation_protocol", {})
    require(protocol.get("seeds") == SEEDS and protocol.get("formal_comparison") is False
            and protocol.get("tier") == metric.get("evaluation_tier") == "l1_mechanism", "protocol differs")
    provenance = metric.get("provenance", {})
    validate_dataset(key, dataset, metric["per_seed"], provenance.get("executed_source_sha256", {}))
    require(provenance.get("artifact_path") == artifact, "artifact binding differs")
    require(provenance.get("dataset_fingerprint") == generated_input_fingerprint(dataset, provenance.get("executed_source_sha256", {})), "input fingerprint differs")
    source_hashes(provenance.get("commit"), provenance.get("executed_source_sha256", {}), {runner, f"src/auto_research/{module}.py"}, require_git=False)
    for row in metric["per_seed"]:
        validate_outcomes(key, row["metrics"])
    return device


def validate_catalog_identity(row):
    key = row["key"]
    domain, identity = REFERENCES[key] if key in REFERENCES else item_for(key)[2][:2]
    require(row.get("domain") == domain and row.get("paper_url") in {f"https://arxiv.org/abs/{identity}", f"https://arxiv.org/abs/{identity}v1"}
            and row.get("detail_path") == f"{domain}/{identity}-{key}/README.md", "catalog paper identity differs")


def validate_receipt_binding(receipt, metric, key):
    boundaries(receipt)
    device, runner, _ = item_for(key)
    expected_path = f"docs/gpu-validations/{key}-a100-20261019.json"
    require(device == "cuda" and receipt.get("seeds") == SEEDS, "receipt device/seeds differ")
    require(receipt.get("full_experiment_status") == "not_reproduced_high_cost"
            and receipt.get("full_experiment_review_done") is True, "receipt cost boundary missing")
    model = receipt.get("accelerator", {}).get("model", "")
    require(model == metric["provenance"].get("accelerator") and "NVIDIA" in model.upper()
            and any(m in model.upper() for m in ("A100", "A30")), "receipt accelerator differs")
    require(receipt.get("accelerator", {}).get("vendor") == "NVIDIA"
            and receipt["accelerator"].get("count") == 1, "single NVIDIA accelerator required")
    require(receipt.get("adapter_key") == key and receipt.get("metrics") == metric["metrics"], "receipt metric differs")
    require(receipt.get("dataset") == metric["dataset"], "receipt input differs")
    require(receipt.get("executed_source_sha256") == metric["provenance"]["executed_source_sha256"], "receipt source differs")
    require(receipt.get("provenance", {}).get("commit") == metric["provenance"]["commit"]
            and receipt["provenance"].get("metric_artifact_path") == metric["provenance"]["artifact_path"], "receipt provenance differs")
    require(receipt["provenance"].get("artifact_path") == expected_path, "receipt artifact binding differs")
    require(receipt.get("checkpoint") == {"public_id": "none-seeded-component-initialization",
            "revision": metric["provenance"]["commit"], "pretrained": False}, "checkpoint identity differs")
    command = receipt.get("command", [])
    extra = ["--methods", "knowgpo"] if key == "knowgpo" else []
    prefix = ["python", runner, "--device", "cuda", *extra, "--seeds", "42,43,44", "--code-commit",
              metric["provenance"]["commit"], "--output"]
    require(isinstance(command, list) and len(command) == len(prefix) + 1 and command[:-1] == prefix
            and isinstance(command[-1], str) and command[-1].startswith("results/")
            and command[-1] == "results/" + Path(command[-1]).name, "receipt command differs")


def finalize():
    rows = {r["key"]: r for r in catalog_records() if r["key"] in COSTS}
    require(set(rows) == set(COSTS), "nine-paper selected scope incomplete")
    counts = {"gpu_validated_components": 0, "cpu_validated_components_or_interfaces": 0, "review_only": 0}
    candidates = []
    for key, row in sorted(rows.items()):
        validate_catalog_identity(row)
        require(row.get("full_experiment_status") == "not_reproduced_high_cost"
                and row.get("review_done") is True and row.get("promotion_eligible") is False
                and row.get("evolve_integrated") is False and row.get("diagnostic_only") is True
                and row.get("adapter") is None, "catalog adapter/cost/no-promotion boundary missing")
        validation = {"status": "review_only_not_reproduced", "gpu_validation_passed": False}
        if key in REFERENCES:
            require(row.get("implementation_status") == "deferred_high_cost" and not row.get("local_operator")
                    and not row.get("local_command") and not row.get("gpu_validation_artifact")
                    and not row.get("requires_gpu_validation"), "reference cannot claim execution")
            counts["review_only"] += 1
        else:
            device, _, (domain, identity, _) = item_for(key)
            artifact = f"docs/{domain}/{identity}-{key}/metrics/component-{device}-seeds42-44.json"
            metric = json.loads((ROOT/artifact).read_text())
            validate_curated(metric, key)
            validation.update(status="validated_bounded_diagnostic", metrics=[artifact], code_commit=metric["provenance"]["commit"])
            if device == "cuda":
                require(row.get("requires_gpu_validation") is True, "CUDA validation gate missing")
                require(row.get("gpu_validation_artifact") == f"docs/gpu-validations/{key}-a100-20261019.json", "catalog receipt path differs")
                receipt = load_gpu_receipt(ROOT/row["gpu_validation_artifact"])
                validate_receipt_binding(receipt, metric, key)
                validation.update(gpu_validation_passed=True, gpu_validation_artifact=row["gpu_validation_artifact"])
                counts["gpu_validated_components"] += 1
            else:
                require(not row.get("requires_gpu_validation") and not row.get("gpu_validation_artifact"), "CPU must not invent GPU receipt")
                counts["cpu_validated_components_or_interfaces"] += 1
        candidates.append({"id": re.search(r"\d{4}\.\d{4,5}", row["paper_url"]).group(), "key": key, "title": row["title"],
            "priority": row.get("priority", "P1"), "publication_date": row["published"],
            "track": {"foundation-models": "foundation-model", "post-training": "post-training", "agent-research": "agent"}[row["domain"]],
            "intake_class": "historical-official-directory-delta" if key == "skill-state" else "announcement-overlap-new-to-review",
            "status": "deferred", "status_scope": "full_paper_reproduction", "resolution": "not_reproduced_high_cost",
            "full_experiment_status": "not_reproduced_high_cost", "review_done": True, "terminal": True,
            "automatic_retry": False, "automatic_implementation_queue": False,
            "reason": "成本过高，不复现（审查 DONE）。" + COSTS[key],
            "cost_assessment": {"basis": COSTS[key], "source_url": row["paper_url"], "available_resource": "单张A100或A30，或本地Mac",
                "cost_type": "published_configuration_not_local_measurement"},
            "doc": row["detail_path"], "implementation_status": row["implementation_status"],
            "bounded_implementation_scope": row["summary"], "local_operator": row.get("local_operator"), "local_command": row.get("local_command"),
            "component_validation": validation, "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
            "source_provenance": [{"source_kind": "original-paper", "source_url": row["paper_url"]}]})
    require(counts == {"gpu_validated_components": 3, "cpu_validated_components_or_interfaces": 4, "review_only": 2}, "acceptance counts differ")
    path = ROOT/"docs/paper-discovery-ledger.json"
    ledger = json.loads(path.read_text())
    batch = {"batch": BATCH, "date": "2026-10-19", "scope_kind": "selected-paper-implementation",
        "window": "Oct16 announcements (Oct14–15 v1) plus one August Google directory late-index discovery; not Oct19 new papers",
        "required_tracks": ["foundation-model", "post-training", "agent"], "coverage_complete": False,
        "review_watermark_advanced": False, "review_snapshot_modified": False,
        "scope_artifact": "research-audits/oct19-components/README.md", "component_validation_counts": counts,
        "accepted_scope_counts": {"bounded_components_and_interfaces": 7, "review_only_papers": 2}, "candidates": candidates}
    ledger["batches"] = [b for b in ledger["batches"] if b["batch"] != BATCH] + [batch]
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
        parser.error("actual immutable runner output required")
    else:
        curate(args.input, args.group)


if __name__ == "__main__":
    main()
