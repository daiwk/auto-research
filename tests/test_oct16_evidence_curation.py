"""Unit-only admission fixtures. All receipt writes are intercepted in memory.

These records exercise the frozen runners' JSON schema; they are not GPU
executions, are never written under repository docs/, and prove no capability.
"""
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import runpy

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("oct16_curation_test_module", ROOT / "scripts/curate_oct16_p0p1_evidence.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_expected_fourteen_source_bindings_match_the_controlled_export_recorder():
    recorder = runpy.run_path(str(ROOT / "scripts/record_oct16_executed_sources.py"))
    assert len(MODULE.EXPECTED_SOURCES) == 14
    assert MODULE.EXPECTED_SOURCES == set(recorder["SOURCES"])


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value))


@pytest.fixture
def bundle(tmp_path, monkeypatch):
    root, inputs = tmp_path / "unit-export", tmp_path / "unit-raw"
    inputs.mkdir()
    monkeypatch.setattr(MODULE, "ROOT", root)
    hashes = {}
    for name in MODULE.EXPECTED_SOURCES:
        source = root / name
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("unit-only source export, not executable GPU evidence\n" + name)
        hashes[name] = hashlib.sha256(source.read_bytes()).hexdigest()
    commit = "a" * 40
    snapshot = {"commit": commit, "executed_source_sha256": hashes}
    public = {"id": "KuaiRand-Pure/official-standard-log-fixed-prefix", "revision": MODULE.PUBLIC_REC_REVISION,
              "rows": 4096}
    rec_rows = []
    for seed in MODULE.SEEDS:
        static = {"method": "static-constraint-decoding", "seed": seed, "dataset": deepcopy(public),
                  "diagnostic_only": True, "promotion_eligible": False,
                  "decoded": 64, "valid_decoded": 64, "validity": 1., "constraint_items": 1852,
                  "mean_extraction_ms": .1}
        cross = {"method": "cross-task-relationships", "seed": seed, "dataset": deepcopy(public),
                 "diagnostic_only": True, "promotion_eligible": False,
                 "test_used_only_after_fixed_training": True, "input_contains_feedback": False,
                 "hyperparameter_selection": False, "training_pair_counts": dict.fromkeys(("00", "01", "10", "11"), 1),
                 "arms": {key: {"optimizer_steps": 32, "parameter_delta_l2": .1,
                                "validation_bce": .6, "test_bce": .6, "validation_brier": .2, "test_brier": .2}
                          for key in ("marginals", "cross-label", "shuffled-cross-control")}}
        transx = {"method": "transx-report-components", "seed": seed,
                  "diagnostic_only": True, "promotion_eligible": False,
                  "dataset": {"id": "explicit-multi-cutoff-memory-and-sparse-gradient-fixture", "revision": "unit-only"},
                  "maximum_forward_error": 1e-14, "maximum_gradient_error": 1e-14,
                  "embedding_delta_l2": .1, "untouched_row_error": 0., "row_accumulator_elements": 32,
                  "counts": {"atomic_tokens_pooled": 60, "direct_tokens_pooled": 187, "events": 7}}
        rec_rows.append({"seed": seed, "static": static, "cross_task": cross, "transx": transx})
    rec = {"device": "cuda", "accelerator": MODULE.MODEL, "seeds": MODULE.SEEDS,
           "diagnostic_only": True, "promotion_eligible": False, "results": rec_rows}
    foundation = {"diagnostic_only": True, "promotion_eligible": False, "components": {}}
    rope_metrics = {"max_reference_absolute_error": 1e-6, "values_unchanged": True,
                    "nonrotary_tail_unchanged": True, "heterogeneous_endpoints_aligned": True,
                    "query_and_answer_positions_synchronized": True, "gradient_norm_keys": .1,
                    "gradient_norm_values": .1, "gradient_norm_queries": .1,
                    "unsynchronized_query_mean_logit_error": 1.}
    cots_metrics = {"minimum_discrete_anchor_weight": .6, "alpha_minimum": .1, "alpha_maximum": .4,
                    "maximum_half_drift_bound_excess": -.1, "phase_lock_and_protection_correct": True,
                    "gradient_norm_logits": .1, "gradient_norm_embeddings": .1}
    for key, measured in (("rope-relay", rope_metrics), ("cots", cots_metrics)):
        rows = [{"seed": seed, "metrics": deepcopy(measured)} for seed in MODULE.SEEDS]
        aggregate = {name: value if isinstance(value, bool) else MODULE.average([value] * 3)
                     for name, value in measured.items()}
        source = f"src/auto_research/foundation_models/{key.replace('-', '_')}.py"
        foundation["components"][key] = {"method": key, "device": "cuda", "accelerator": MODULE.MODEL,
            "seeds": MODULE.SEEDS, "measured_locally": True, "diagnostic_only": True, "promotion_eligible": False,
            "provenance": {"code_commit": commit, "implementation_sha256": hashes[source],
                           "runner_sha256": hashes[MODULE.RUNNERS["foundation"]]},
            "dataset": {"id": "synthetic-formula-tensors", "revision": "oct16-component-v1",
                        "checkpoint": None, "capability_benchmark": False},
            "metrics": aggregate, "per_seed": rows}
    post_results = {}
    for key in MODULE.POST_METHODS:
        rows = []
        for seed in MODULE.SEEDS:
            row = {"seed": seed, "parameter_delta_l2": .1, "baseline_validation_nll": 5.,
                   "final_validation_nll": 4.9, "final_test_nll": 5.1,
                   "frozen_teacher_parameter_deltas_l2": [0., 0.],
                   "frozen_rl_snapshot_parameter_deltas_l2": [0., 0., 0.]}
            if key == "tf-opd":
                row.update(method_optimizer_updates=0, teacher_rollout_audits=[{
                    "source": "teacher_self_generated_then_teacher_forced", "correctness_filter": False,
                    "kept_rollouts": 4, "seen_rollouts": 5, "layer_token_counts": {"head": 40}} for _ in range(2)],
                    linear_layers={"head": {"normal_equation_residual_l2": 1e-14, "solve_dtype": "float64",
                       "storage_dtype": "float32", "pseudoinverse": False, "unreproduced_share": [.1, .2]}})
            else:
                row.update(generated_tokens=128, natural_eos_rollouts=0, rejected_diagnostic_groups=0,
                           history=[{"step": step, "loss": .1, "gradient_norm": .1} for step in range(2)])
                if key == "waypoint-opd":
                    row["teacher_snapshot_lineage"] = [{"run_id": "unit-only", "step": s} for s in (0, 4, 8)]
                    row["teacher_rl_audit"] = {"updates": 8, "rollouts_per_update": 64, "rollout_horizon": 1,
                        "checkpoint_steps": [0, 4, 8], "total_sampled_actions": 512, "learning_rate": .2,
                        "selection": "none; fixed 0/4/8 checkpoints, no retries or reward/gate-based selection",
                        "history": [{"step": step, "sampled_actions": 64, "mean_rule_reward": .5, "gradient_norm": .1}
                                    for step in range(1, 9)]}
                    for step in row["history"]:
                        step.update(mean_gate=.5, zero_gate_fraction=0., batch_scale=1.5, valid_tokens=64)
                elif key == "ggpo":
                    row.update(reference_refreshes=1, behavior_syncs=1, behavior_is_reference=False)
                    for index, step in enumerate(row["history"]):
                        step.update(branch="direct_autograd", reference_refreshed=bool(index), retained_groups=1,
                                    raw_gap=.1, mean_length=16.)
                elif key == "stopd":
                    for index, step in enumerate(row["history"]):
                        step.update(warmup=index == 0, denominator=64., weighted_count_for_next_batch=64.,
                                    retained_tokens=64, cutoffs=[16] * 4,
                                    normalizer_source="current_exact_warmup" if index == 0 else "previous_batch")
                elif key == "cce-opd":
                    row["condition_pair_source"] = "unit-only supplied controlled premise"
                    for step in row["history"]:
                        step.update(valid_tokens=64, auxiliary_tokens=64, max_union_size=18,
                                    opd_loss=.04, auxiliary_loss=.06)
                else:
                    for step in row["history"]:
                        step.update(paper_default_minimum_length=550, paper_default_eligible_responses=0,
                                    diagnostic_minimum_length=6, short_window_diagnostic_only=True,
                                    eligible_responses=4, retained_groups=1, updated_tokens=64)
            rows.append(row)
        post_results[key] = rows
    post = {"diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
            "accelerator": MODULE.MODEL, "seeds": MODULE.SEEDS, "methods": list(MODULE.POST_METHODS),
            "papers": MODULE.POST_PAPERS,
            "public_resources": {"corpus_id": "gutenberg:1524", "corpus_revision": "sha256:" + MODULE.CORPUS_SHA256,
                "corpus_sha256": MODULE.CORPUS_SHA256,
                "byte_ranges": {"train": [0, 165516], "validation": [165516, 186205], "test": [186205, 206895]}},
            "protocol": {"separate_train_validation_test": True, "teacher_steps": 8,
                         "specialist_steps": 4, "student_steps": 2, "max_new_tokens": 16}, "results": post_results}
    for key in ("static-constraint-decoding", "cross-task-relationships", "transx", "rope-relay", "cots", *MODULE.POST_METHODS):
        # Deliberately omit TransX tier: the backwards-compatible fallback must remain.
        catalog = {"key": key, "domain": "unit-only", "detail_path": f"unit-only/{key}/README.md"}
        if key != "transx":
            catalog["evaluation_tier"] = "l1_mechanism"
        dump(root / "src/auto_research/paper_specs/catalog/unit-only" / f"{key}.json", catalog)
    data = {"executed-source.json": snapshot, "recommendation.json": rec,
            "foundation.json": foundation, "post-training.json": post}
    writes = []
    monkeypatch.setattr(MODULE, "write", lambda name, payload: writes.append((name, payload)))
    def run():
        for name, payload in data.items():
            dump(inputs / name, payload)
        MODULE.curate(inputs)
    return data, writes, run, root


def test_unit_bundle_validates_all_eleven_before_emitting_and_preserves_boundaries(bundle):
    _, writes, run, _ = bundle
    run()
    assert len(writes) == len({name for name, _ in writes}) == 22
    receipts = [payload for name, payload in writes if name.startswith("docs/gpu-validations/")]
    assert len(receipts) == 11
    assert {row["adapter_key"] for row in receipts} == {
        "static-constraint-decoding", "cross-task-relationships", "transx-report-components",
        "rope-relay", "cots", *MODULE.POST_METHODS}
    for _, payload in writes:
        assert payload["diagnostic_only"] and not payload["promotion_eligible"]
        assert len(payload["provenance"]["raw_result_sha256"]) == 64
        assert len(payload["provenance"]["source_snapshot_sha256"]) == 64
        assert payload["provenance"]["dataset_fingerprint"]
        assert "not recorded" not in payload["provenance"]["dataset_fingerprint"]
        if payload["schema_version"] == 2:
            assert payload["adapter"] is None and not payload["evolve_integrated"]
    ggpo = next(r for r in receipts if r["adapter_key"] == "ggpo")
    assert not ggpo["execution_checks"]["teacher_self_generation_and_filtered_replay"]
    assert ggpo["provenance"]["dataset_fingerprint"] == "sha256:" + MODULE.CORPUS_SHA256
    static = next(r for r in receipts if r["adapter_key"] == "static-constraint-decoding")
    assert static["provenance"]["dataset_fingerprint"] == MODULE.PUBLIC_REC_REVISION
    cots = next(r for r in receipts if r["adapter_key"] == "cots")
    assert "synthetic-formula-tensors@oct16-component-v1;seeds=42,43,44" in cots["provenance"]["dataset_fingerprint"]


def test_unrelated_cross_domain_short_keys_do_not_block_selected_bundle(bundle):
    _, writes, run, root = bundle
    for domain in ("agent-research", "recommendation"):
        dump(root / "src/auto_research/paper_specs/catalog" / domain / "spear.json",
             {"domain": domain, "key": "spear"})
    run()
    assert len(writes) == 22


def test_selected_key_ambiguity_is_rejected_before_any_write(bundle):
    _, writes, run, root = bundle
    dump(root / "src/auto_research/paper_specs/catalog/duplicate/cots.json", {"key": "cots"})
    with pytest.raises(ValueError, match="duplicate catalog key"):
        run()
    assert writes == []


@pytest.mark.parametrize("mutation,match", [
    ("implementation", "raw implementation/runner"), ("runner", "raw implementation/runner"),
    ("commit", "raw commit"), ("phase", "phase-lock"), ("zero_gradient", "positive measured"),
    ("aggregate", "aggregate/contract"), ("rope_error", "maximum"), ("anchor", "minimum"),
])
def test_foundation_rejects_conflicting_raw_source_failed_contracts_and_aggregates(bundle, mutation, match):
    data, writes, run, _ = bundle
    cots = data["foundation.json"]["components"]["cots"]
    if mutation == "implementation":
        cots["provenance"]["implementation_sha256"] = "0" * 64
    elif mutation == "runner":
        cots["provenance"]["runner_sha256"] = "0" * 64
    elif mutation == "commit":
        cots["provenance"]["code_commit"] = "b" * 40
    elif mutation == "phase":
        cots["per_seed"][0]["metrics"]["phase_lock_and_protection_correct"] = False
    elif mutation == "zero_gradient":
        cots["per_seed"][1]["metrics"]["gradient_norm_logits"] = 0.
    elif mutation == "aggregate":
        cots["metrics"]["gradient_norm_logits"]["mean"] = 10.
    elif mutation == "anchor":
        cots["per_seed"][0]["metrics"]["minimum_discrete_anchor_weight"] = .49
    else:
        data["foundation.json"]["components"]["rope-relay"]["per_seed"][0]["metrics"]["max_reference_absolute_error"] = 1.
    with pytest.raises(ValueError, match=match):
        run()
    assert writes == []


@pytest.mark.parametrize("target", ["missing_post", "extra_post", "missing_foundation", "extra_foundation", "missing_source", "extra_source"])
def test_exact_two_six_and_fourteen_sets_are_required_before_any_write(bundle, target):
    data, writes, run, _ = bundle
    if target.endswith("post"):
        results = data["post-training.json"]["results"]
        results.pop("sif") if target.startswith("missing") else results.update(unknown=[])
    elif target.endswith("foundation"):
        results = data["foundation.json"]["components"]
        results.pop("cots") if target.startswith("missing") else results.update(unknown={})
    else:
        sources = data["executed-source.json"]["executed_source_sha256"]
        sources.pop(next(iter(sources))) if target.startswith("missing") else sources.update({"../escape.py": "0" * 64})
    with pytest.raises(ValueError, match="exact"):
        run()
    assert writes == []


@pytest.mark.parametrize("target", ["recommendation", "foundation", "post", "inner_seed", "nonfinite"])
def test_all_seed_identities_and_finite_evidence_are_required(bundle, target):
    data, writes, run, _ = bundle
    if target == "recommendation":
        data["recommendation.json"]["results"][2]["seed"] = 43
    elif target == "foundation":
        data["foundation.json"]["components"]["cots"]["per_seed"].pop()
    elif target == "post":
        data["post-training.json"]["results"]["sif"][1]["seed"] = 42
    elif target == "inner_seed":
        data["recommendation.json"]["results"][0]["static"]["seed"] = 999
    else:
        data["post-training.json"]["results"]["sif"][0]["final_test_nll"] = float("nan")
    with pytest.raises(ValueError):
        run()
    assert writes == []


@pytest.mark.parametrize("target", ["no_rollout", "wrong_teacher_source", "solver", "snapshot_changed", "lineage", "zero_gradient", "stopd_lag", "sif_default", "feedback", "transx_gradient", "teacher_rl_count", "teacher_rl_gradient", "teacher_rl_selection"])
def test_actual_method_specific_contracts_are_checked_not_only_parameter_delta(bundle, target):
    data, writes, run, _ = bundle
    post = data["post-training.json"]["results"]
    if target == "no_rollout":
        post["tf-opd"][0]["teacher_rollout_audits"][0]["kept_rollouts"] = 0
    elif target == "wrong_teacher_source":
        post["tf-opd"][0]["teacher_rollout_audits"][0]["source"] = "gold-reference-text"
    elif target == "solver":
        post["tf-opd"][0]["linear_layers"]["head"]["normal_equation_residual_l2"] = 1.
    elif target == "snapshot_changed":
        post["waypoint-opd"][0]["frozen_rl_snapshot_parameter_deltas_l2"][1] = .1
    elif target == "lineage":
        post["waypoint-opd"][0]["teacher_snapshot_lineage"][1]["run_id"] = "another-run"
    elif target == "zero_gradient":
        post["sif"][2]["history"][1]["gradient_norm"] = 0.
    elif target == "stopd_lag":
        post["stopd"][0]["history"][1]["denominator"] = 128.
    elif target == "sif_default":
        post["sif"][0]["history"][0]["paper_default_eligible_responses"] = 4
    elif target == "feedback":
        data["recommendation.json"]["results"][0]["cross_task"]["input_contains_feedback"] = True
    elif target == "teacher_rl_count":
        post["waypoint-opd"][0]["teacher_rl_audit"]["total_sampled_actions"] = 0
    elif target == "teacher_rl_gradient":
        post["waypoint-opd"][0]["teacher_rl_audit"]["history"][3]["gradient_norm"] = 0.
    elif target == "teacher_rl_selection":
        post["waypoint-opd"][0]["teacher_rl_audit"]["selection"] = "select highest reward snapshot"
    else:
        data["recommendation.json"]["results"][0]["transx"]["maximum_gradient_error"] = 1.
    with pytest.raises(ValueError):
        run()
    assert writes == []


def test_current_source_mismatch_and_invalid_commit_are_rejected(bundle):
    data, writes, run, root = bundle
    source = root / next(iter(MODULE.EXPECTED_SOURCES))
    source.write_text("changed after unit-only source capture")
    with pytest.raises(ValueError, match="source changed"):
        run()
    data["executed-source.json"]["commit"] = "not-a-commit"
    with pytest.raises(ValueError, match="40-hex"):
        run()
    assert writes == []


@pytest.mark.parametrize("target", ["recommendation", "foundation", "post-training"])
def test_cpu_records_cannot_be_curated_as_cuda_receipts(bundle, target):
    data, writes, run, _ = bundle
    raw = data[target + ".json"]
    if target == "foundation":
        raw["components"]["cots"]["accelerator"] = "CPU"
        raw["components"]["cots"]["device"] = "cpu"
    else:
        raw["accelerator"] = "CPU"
        if target == "recommendation":
            raw["device"] = "cpu"
    with pytest.raises(ValueError, match="CUDA"):
        run()
    assert writes == []
