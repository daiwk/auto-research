"""Admit only fixed L1 component evidence backed by a frozen source proof."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from auto_research.gpu_validation import load_gpu_receipt  # noqa: E402
from auto_research.paper_specs.catalog import catalog_records  # noqa: E402
from curate_oct21_component_evidence import aggregate, digest, require, write  # noqa: E402
from oct18_frozen_sources import capture_sources, verify_sources  # noqa: E402
from run_oct22_bulletin_components import CUDA_KEYS, MODULES, RUNNER, SEEDS, SOURCES  # noqa: E402

AUDIT = ROOT / "docs/research-audits/oct22-bulletin-components"
CHECKS = {
    "alps": {"independent_formula_match", "finite_student_query_gradients", "frozen_teacher_has_no_gradient",
        "masked_patch_gradient_is_zero", "remove_overlap_mask_changes_loss", "remove_fixed_statistics_changes_loss", "remove_geometry_changes_queries"},
    "asteroid": {"finite_metrics", "real_parameter_update", "real_finite_gradient", "expert_only_nll_matches_reference",
        "student_never_receives_latent_or_label", "history_changes_learned_policy", "causal_padding_isolation",
        "curriculum_zero_one_two_episodes", "successful_teacher_episodes_only"},
    "cord": {"three_real_updates", "independent_gradient_reference", "protected_first_order_identity",
        "accumulate_before_project_negative_control", "always_differs_on_aligned_gradients", "no_optimizer_direction_guarantee_claim"},
    "csd": {"three_real_updates", "frozen_teacher", "all_four_chunk_shapes", "value_reference_agrees",
        "gradient_reference_agrees", "normalized_with_rest", "no_chain_negative_control", "no_residual_negative_control"},
    "jev-multicorrect": {"ranking_not_set_recovery", "low_mass_correct_choice_counted", "test_does_not_refit_threshold",
        "validation_test_overlap_rejected", "refusal_not_empty_set_success", "public_predictor_has_no_gold",
        "identical_copy_reference", "ece_excluding_low_bin_renormalizes"},
}
METRICS = {
    "alps": {"formula_absolute_error", "overlap_patch_count", "removed_overlap_loss_delta", "removed_standardization_loss_delta",
        "removed_geometry_query_mse", "masked_patch_gradient_max", "query_parameter_gradient_norm", "pretrained_model_calls"},
    "asteroid": {"initial_context_free_nll", "last_training_nll", "accumulated_expert_nll", "parameter_update_l2",
        "last_gradient_l2", "optimizer_steps", "expert_query_count", "student_context_episodes", "nll_reference_abs_error",
        "same_public_history_logit_abs_error", "history_reward_logit_effect", "masked_future_logit_abs_error"},
    "cord": {"optimizer_updates", "micro_batches_per_update", "projection_count", "gradient_reference_error",
        "protected_first_order_error", "per_micro_projection_negative_gap", "always_vs_conflict_gate_gap",
        "student_parameter_delta", "final_first_loss", "final_second_loss"},
    "csd": {"optimizer_updates", "accepted_chunks", "student_vocabulary", "teacher_vocabulary", "loss_reference_error",
        "gradient_reference_error", "normalization_error", "no_chain_negative_gap", "no_residual_negative_gap",
        "student_parameter_delta", "final_loss", "final_kd"},
    "jev-multicorrect": {"scorer_contract_cases", "validation_overlap_rejections", "model_calls"},
}


def records():
    return {r["key"]: r for r in catalog_records()}


def metric_path(key):
    device = "cuda" if key in CUDA_KEYS else "cpu"
    return Path("docs")/Path(records()[key]["detail_path"]).parent/f"metrics/component-{device}-seeds42-44.json"


def dataset(key, hashes):
    return {"id": f"synthetic:oct22-bulletin-{key}-v1", "revision": "sha256:"+digest(hashes),
        "recipe": "source-frozen-generated-mechanism-contract-inputs", "capability_benchmark": False}


def gates(key, rows):
    require([r["seed"] for r in rows] == SEEDS, "exact three seeds required")
    for row in rows:
        require(set(row["checks"]) == CHECKS[key] and all(v is True for v in row["checks"].values()), "missing/failed defining contract")
        require(set(row["metrics"]) == METRICS[key], "diagnostic metric schema changed")
        m = row["metrics"]
        if key == "alps":
            # FP32 independent reductions use the module's allclose check; do not
            # demand FP64 absolute tolerance for a much larger FP32 loss.
            require(m["formula_absolute_error"] < 1e-3 and m["overlap_patch_count"] > 0
                and m["masked_patch_gradient_max"] == m["pretrained_model_calls"] == 0
                and min(m[n] for n in ("removed_overlap_loss_delta", "removed_standardization_loss_delta",
                    "removed_geometry_query_mse", "query_parameter_gradient_norm")) > 0, "ALPS geometry/gradient/isolation")
        elif key == "asteroid":
            require(m["optimizer_steps"] == 54 and m["expert_query_count"] == m["student_context_episodes"] == 72
                and m["parameter_update_l2"] > 0 and m["last_gradient_l2"] > 0
                and max(m[n] for n in ("nll_reference_abs_error", "same_public_history_logit_abs_error", "masked_future_logit_abs_error")) < 1e-6
                and m["history_reward_logit_effect"] > 1e-6, "ASTEROID real update/history isolation")
        elif key == "cord":
            require(m["optimizer_updates"] == 3 and m["micro_batches_per_update"] == 2
                and m["student_parameter_delta"] > 0 and m["gradient_reference_error"] < 1e-10
                and m["protected_first_order_error"] < 1e-10
                and m["per_micro_projection_negative_gap"] > 0 and m["always_vs_conflict_gate_gap"] > 0, "CORD reference/update")
        elif key == "csd":
            require(m["optimizer_updates"] == 3 and m["accepted_chunks"] == 5
                and m["student_vocabulary"] != m["teacher_vocabulary"] and m["student_parameter_delta"] > 0
                and max(m[n] for n in ("loss_reference_error", "gradient_reference_error", "normalization_error")) < 1e-9
                and m["no_chain_negative_gap"] > 0 and m["no_residual_negative_gap"] > 0, "CSD cross-tokenizer reference/update")
        else:
            require(m == {"scorer_contract_cases": 8, "validation_overlap_rejections": 1, "model_calls": 0}, "JEV scorer/isolation")


def validate_result(key, result):
    require(result["schema_version"] == 2 and result["method"] == key
        and result["manifest_ref"] == records()[key]["domain"]+":"+key, "component identity")
    require(result["evaluation_tier"] == result["evaluation_protocol"]["tier"] == "l1_mechanism"
        and result["diagnostic_only"] is True and result["fixture_demo"] is True
        and result["formal_comparison"] is result["evaluation_protocol"]["formal_comparison"] is False
        and result["promotion_eligible"] is False and result["evolve_integrated"] is False
        and result["pretrained_model_calls"] == 0 and result["full_experiment_review_done"] is True
        and result["full_experiment_status"] == "not_reproduced_high_cost", "L1 claim boundary")
    p = result["provenance"]
    hashes = p["executed_source_sha256"]
    require(set(hashes) == set(SOURCES), "frozen executed source scope")
    require(re.fullmatch(r"[0-9a-f]{64}", p["raw_runner_artifact_sha256"]) is not None, "raw artifact hash")
    require(result["seeds"] == result["evaluation_protocol"]["seeds"] == SEEDS, "seed identity")
    require(result["dataset"] == dataset(key, hashes) and p["artifact_path"] == metric_path(key).as_posix(), "dataset/artifact binding")
    require(p["dataset_fingerprint"] == "sha256:"+digest({"dataset": result["dataset"], "seeds": SEEDS, "source": hashes}), "fingerprint")
    require((key not in CUDA_KEYS and p["accelerator"] == "CPU") or
        (key in CUDA_KEYS and any(n in p["accelerator"] for n in ("A100", "A30"))), "actual accelerator")
    gates(key, result["per_seed"])
    require(result["metrics"] == aggregate(result["per_seed"]), "aggregate mismatch")


def validate_raw_runs(raw):
    """Validate the complete actual runner outputs before deriving any record."""
    require(raw["cpu"]["code_commit"] == raw["cuda"]["code_commit"]
        and raw["cpu"]["source_sha256"] == raw["cuda"]["source_sha256"], "CPU/CUDA frozen source mismatch")
    for device, item in raw.items():
        expected = set(MODULES) if device == "cpu" else CUDA_KEYS
        require(item["schema_version"] == 2 and item["device"] == device and item["seeds"] == SEEDS
            and set(item["components"]) == expected and item["diagnostic_only"] is True
            and item["formal_comparison"] is False and item["promotion_eligible"] is False
            and item["evolve_integrated"] is False and item["pretrained_model_calls"] == 0
            and item["full_experiment_status"] == "not_reproduced_high_cost", "raw scope/device/claim boundary")
        require((device == "cpu" and item["accelerator"] == "CPU") or
            (device == "cuda" and any(n in item["accelerator"] for n in ("A100", "A30"))), "no CUDA fallback")
        for key, component in item["components"].items():
            gates(key, component["per_seed"])
            aggregate(component["per_seed"])


def receipt_for(key, result):
    """One exact sanitized receipt identity, derived from bound runner evidence."""
    require(key in CUDA_KEYS, "CUDA receipt requires a CUDA component")
    provenance = result["provenance"]
    commit = provenance["commit"]
    target = metric_path(key)
    receipt_path = f"docs/gpu-validations/{key}-a100-20261022.json"
    return {"schema_version": 1, "adapter_key": key, "validated_at": "2026-10-22",
        "accelerator": {"vendor": "NVIDIA", "model": provenance["accelerator"], "count": 1},
        "command": ["python3", RUNNER, "--device", "cuda", "--seeds", "42,43,44", "--source-commit", commit,
            "--frozen-proof", "oct22-bulletin-frozen-proof.json", "--output", "results/components-cuda.json"],
        "dataset": result["dataset"],
        "checkpoint": {"public_id": "none-seeded-component-initialization", "revision": commit, "pretrained": False},
        "seeds": SEEDS, "result": "passed", "metrics": result["metrics"],
        "executed_source_sha256": provenance["executed_source_sha256"],
        "provenance": {**provenance, "artifact_path": receipt_path, "metric_artifact_path": target.as_posix()},
        "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
        "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True}


def validate_raw_binding(key, result, raw, raw_bytes):
    """Hash the persisted raw bytes and bind every seed, source and accelerator."""
    device = "cuda" if key in CUDA_KEYS else "cpu"
    item, provenance = raw[device], result["provenance"]
    require(provenance["raw_runner_artifact_sha256"] == hashlib.sha256(raw_bytes[device]).hexdigest(),
        "persisted raw runner SHA mismatch")
    require(provenance["commit"] == item["code_commit"]
        and provenance["executed_source_sha256"] == item["source_sha256"]
        and provenance["accelerator"] == item["accelerator"], "raw runner source/accelerator identity mismatch")
    require(digest(result["per_seed"]) == digest(item["components"][key]["per_seed"]),
        "raw runner per-seed evidence mismatch")


def ingest(cpu_path, cuda_path):
    raw_paths = {"cpu": cpu_path, "cuda": cuda_path}
    raw_bytes = {device: path.read_bytes() for device, path in raw_paths.items()}
    raw = {device: json.loads(data) for device, data in raw_bytes.items()}
    validate_raw_runs(raw)
    commit, hashes = raw["cpu"]["code_commit"], raw["cpu"]["source_sha256"]
    proof = capture_sources(ROOT, commit, hashes)
    verify_sources(ROOT, commit, hashes, proof)
    prepared = []
    for key in MODULES:
        device = "cuda" if key in CUDA_KEYS else "cpu"
        item = raw[device]
        ds = dataset(key, hashes)
        target = metric_path(key)
        provenance = {"commit": commit, "artifact_path": target.as_posix(), "accelerator": item["accelerator"],
            "executed_source_sha256": hashes, "raw_runner_artifact_sha256": hashlib.sha256(raw_bytes[device]).hexdigest(),
            "dataset_fingerprint": "sha256:"+digest({"dataset": ds, "seeds": SEEDS, "source": hashes})}
        rows = item["components"][key]["per_seed"]
        result = {"schema_version": 2, "method": key, "manifest_ref": records()[key]["domain"]+":"+key,
            "dataset": ds, "seeds": SEEDS, "per_seed": rows, "metrics": aggregate(rows),
            "evaluation_tier": "l1_mechanism", "evaluation_protocol": {"tier": "l1_mechanism", "seeds": SEEDS,
                "formal_comparison": False, "claim_policy": "generated mechanism/scorer contracts, no pretrained capability or full-paper comparison"},
            "provenance": provenance, "diagnostic_only": True, "fixture_demo": True, "pretrained_model_calls": 0,
            "formal_comparison": False, "promotion_eligible": False, "evolve_integrated": False,
            "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True}
        validate_result(key, result)
        validate_raw_binding(key, result, raw, raw_bytes)
        prepared.append((ROOT/target, result))
        if key in CUDA_KEYS:
            receipt_path = f"docs/gpu-validations/{key}-a100-20261022.json"
            receipt = receipt_for(key, result)
            require(records()[key]["gpu_validation_artifact"] == receipt_path, "catalog GPU receipt binding")
            prepared.append((ROOT/receipt_path, receipt))
    for path, value in prepared:
        write(path, value)
    write(AUDIT/"frozen-sources.json", {"schema_version": 1, "commit": commit, "proof": proof})
    # Preserve the original sanitized bytes, not a reserialized near-copy. Their
    # hash binds the committed per-seed evidence even after local /tmp cleanup.
    for device, data in raw_bytes.items():
        (AUDIT/f"raw-{device}.json").write_bytes(data)


def check():
    frozen = json.loads((AUDIT/"frozen-sources.json").read_text())
    raw_bytes = {device: (AUDIT/f"raw-{device}.json").read_bytes() for device in ("cpu", "cuda")}
    raw = {device: json.loads(data) for device, data in raw_bytes.items()}
    validate_raw_runs(raw)
    for key in MODULES:
        result = json.loads((ROOT/metric_path(key)).read_text())
        validate_result(key, result)
        validate_raw_binding(key, result, raw, raw_bytes)
        p = result["provenance"]
        require(p["commit"] == frozen["commit"], "proof identity")
        verify_sources(ROOT, p["commit"], p["executed_source_sha256"], frozen["proof"])
        if key in CUDA_KEYS:
            receipt = load_gpu_receipt(ROOT/records()[key]["gpu_validation_artifact"])
            require(digest(receipt) == digest(receipt_for(key, result)), "exact GPU receipt/run identity binding")
    for key in ("aw0", "right-on-q", "finesid"):
        row = records()[key]
        require(row["implementation_status"] == "deferred_high_cost" and row["adapter"] is None
            and row["review_done"] is True and row["full_experiment_status"] == "not_reproduced_high_cost"
            and row["requires_gpu_validation"] is False, "high-cost terminal review decision")
    print("Oct22 bulletin: five L1 components and three terminal high-cost reviews passed")


def finalize_scope():
    """Accept only this fixed batch AFTER real frozen evidence passes check()."""
    check()
    scope_path = AUDIT/"task-scope.json"
    coverage_path = AUDIT/"source-coverage.json"
    scope = json.loads(scope_path.read_text())
    coverage = json.loads(coverage_path.read_text())
    ledger_path = ROOT/"docs/paper-discovery-ledger.json"
    ledger = json.loads(ledger_path.read_text())
    batches = [b for b in ledger["batches"] if b["batch"] == "2026-10-22-bulletin-components"]
    require(len(batches) == 1 and {p["key"] for p in scope["papers"]} == set(MODULES)|{"aw0", "right-on-q", "finesid"}, "fixed acceptance scope")
    for rows in (scope["papers"], batches[0]["candidates"]):
        for row in rows:
            if row["key"] not in MODULES:
                continue
            row.update(status="implemented", implementation_status="component_only", component_implemented=True,
                component_accepted=True, review_done=True, delivery_status="bounded_component_accepted",
                component_evidence=metric_path(row["key"]).as_posix(),
                resolution="bounded_component_implemented_full_experiment_not_reproduced_high_cost",
                reason="L1组件通过冻结源码和三种子契约；CUDA组件真实A100验收。完整实验高成本不复现，不宣称能力效果。")
            if row["key"] in CUDA_KEYS:
                row["gpu_validation_artifact"] = records()[row["key"]]["gpu_validation_artifact"]
    scope.update(selected_scope_complete=True, delivery_status="bounded_scope_complete",
        gpu_validated_component_count=4, component_count=5, capability_reproductions_claimed=0)
    coverage["counts"].update(components_pending_gpu_and_integration=0, components_accepted=5,
        gpu_validated_components=4, capability_reproductions_claimed=0)
    coverage["delivery_status"] = "bounded_scope_complete"
    coverage["limitations"] = [
        "Five L1 components passed frozen-source CPU/GPU integration acceptance; three high-cost references are review DONE, not implementations."
        if line.startswith("Five L1 components are pending") else line
        for line in coverage["limitations"]
    ]
    batches[0].update(delivery_status="bounded_scope_complete", selected_scope_complete=True,
        counts=coverage["counts"])
    for path, value in ((scope_path, scope), (coverage_path, coverage), (ledger_path, ledger)):
        write(path, value)


def sync_figures():
    """Register the eight original figures already visually reviewed this turn."""
    from PIL import Image
    import xml.etree.ElementTree as ET

    info = {
        "alps": ("paper-figure-01.png", "Figure 2", "https://arxiv.org/html/2610.30120v1/fig2_gemini_v5.png"),
        "asteroid": ("paper-figure-03.svg", "Figure 3", "https://arxiv.org/html/2610.30105v1/fig_aicd.svg"),
        "cord": ("paper-figure-01.png", "Figure 2", "https://arxiv.org/pdf/2610.29965v1#page=4"),
        "csd": ("paper-figure-01.png", "Figure 1", "https://arxiv.org/pdf/2610.28895v1#page=3"),
        "jev-multicorrect": ("paper-figure-02.png", "Figure 2", "https://raw.githubusercontent.com/Rushab1/gr-jev/7b161f96cd0ff1842845fc66f981d1471cc18151/paper/figures/exact_set.pdf"),
        "aw0": ("paper-figure-01.png", "Figure 2", "https://arxiv.org/html/2610.30136v1/method_v6_0926.png"),
        "right-on-q": ("paper-figure-02.png", "Figure 2", "https://arxiv.org/pdf/2610.29378v1#page=3"),
        "finesid": ("paper-figure-01.png", "Figure 1", "https://arxiv.org/pdf/2610.29138v1#page=3"),
    }
    path = ROOT/"docs/paper-figures-manifest.json"
    figures = json.loads(path.read_text())
    pages = {"docs/"+records()[key]["detail_path"] for key in info}
    figures = [r for r in figures if r["page"] not in pages]
    for key, (filename, label, source) in info.items():
        record = records()[key]
        page = Path("docs")/record["detail_path"]
        asset = page.parent/"assets"/filename
        if asset.suffix == ".svg":
            bounds = ET.fromstring((ROOT/asset).read_text()).attrib["viewBox"].split()
            width, height = (round(float(v)) for v in bounds[-2:])
        else:
            with Image.open(ROOT/asset) as im:
                width, height = im.size
        figures.append({"page": page.as_posix(), "paper_url": record["paper_url"],
            "arxiv_id": re.search(r"\d{4}\.\d{4,5}", record["paper_url"])[0],
            "figure": label, "original_caption": "", "source_url": source,
            "extraction": "original-source-image-or-visually-reviewed-pdf-crop", "asset": asset.as_posix(),
            "width": width, "height": height, "score": 0, "error": "",
            "sha256": hashlib.sha256((ROOT/asset).read_bytes()).hexdigest(), "visually_inspected": True})
    write(path, figures)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cpu", type=Path)
    parser.add_argument("--cuda", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--finalize", action="store_true", help="accept only the validated fixed scope and register reviewed figures")
    args = parser.parse_args()
    if args.cpu and args.cuda:
        ingest(args.cpu, args.cuda)
    elif not (args.check or args.finalize):
        parser.error("supply both actual --cpu/--cuda runner artifacts, or --check")
    check()
    if args.finalize:
        finalize_scope()
        sync_figures()
