#!/usr/bin/env python3
"""Curate actual bounded CUDA outputs; reject mismatched source or missing runs."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import statistics

ROOT = Path(__file__).resolve().parents[1]
SEEDS = [42, 43, 44]
MODEL = "NVIDIA A100-SXM4-80GB"
POST_METHODS = ("tf-opd", "waypoint-opd", "ggpo", "stopd", "cce-opd", "sif")
POST_PAPERS = dict(zip(POST_METHODS, ("2610.22236v1", "2610.21601v1", "2610.20814v1",
                                    "2610.21337v1", "2610.21195v1", "2610.21392v1"), strict=True))
FOUNDATION_METHODS = {"rope-relay", "cots"}
REC_MODULES = {
    "static": ("static-constraint-decoding", "static_constraint_decoding/algorithm.py"),
    "cross_task": ("cross-task-relationships", "cross_task_relationships/model.py"),
    "transx": ("transx-report-components", "transx/technical_report.py"),
}
RUNNERS = {name: f"scripts/run_oct16_{name}_components.py" for name in ("recommendation", "foundation", "post")}
EXPECTED_SOURCES = {
    *("src/auto_research/reproductions/" + module for _, module in REC_MODULES.values()),
    *(f"src/auto_research/foundation_models/{key.replace('-', '_')}.py" for key in FOUNDATION_METHODS),
    *(f"src/auto_research/post_training/{key.replace('-', '_')}.py" for key in POST_METHODS),
    *RUNNERS.values(),
}
CORPUS_SHA256 = "31584c19795779431b5933499a45b9cecb03e8c246b6ea7e245a2b6d65e8e784"
PUBLIC_REC_REVISION = "sha256:c07b1719c6c024d67b45197d75dece9ea7a12dff86eb363968f8871e6c850cdb"


def require(condition, message):
    """Evidence gates must also run under python -O."""
    if not condition:
        raise ValueError(message)


def finite_tree(value, label):
    if isinstance(value, dict):
        for key, child in value.items():
            finite_tree(child, f"{label}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            finite_tree(child, f"{label}[{index}]")
    elif isinstance(value, (float, int)) and not isinstance(value, bool):
        require(math.isfinite(value), f"{label}: nonfinite numeric evidence")


def number(value, label, *, minimum=None, maximum=None):
    require(isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value),
            f"{label}: finite real value required")
    require(minimum is None or value >= minimum, f"{label}: below required minimum")
    require(maximum is None or value <= maximum, f"{label}: above required maximum")
    return value


def positive(value, label):
    require(number(value, label) > 0, f"{label}: positive measured value required")


def count(value, label, *, minimum=0):
    require(type(value) is int and value >= minimum, f"{label}: integer count >= {minimum} required")


def close(value, expected, label):
    number(value, label)
    require(math.isclose(value, expected, rel_tol=1e-7, abs_tol=1e-9), f"{label}: aggregate/contract mismatch")


def rows_with_seeds(rows, label):
    require(isinstance(rows, list) and len(rows) == 3 and
            all(isinstance(row, dict) for row in rows), f"{label}: exactly three seed rows required")
    require([row.get("seed") for row in rows] == SEEDS, f"{label}: expected seeds {SEEDS}")


def diagnostic(payload, label):
    require(payload.get("diagnostic_only") is True and payload.get("promotion_eligible") is False,
            f"{label}: diagnostic/nonpromotion boundary missing")


def validate_snapshot(snapshot):
    require(isinstance(snapshot, dict) and isinstance(snapshot.get("commit"), str) and
            re.fullmatch(r"[0-9a-f]{40}", snapshot["commit"]), "snapshot: exact 40-hex commit required")
    hashes = snapshot.get("executed_source_sha256")
    require(isinstance(hashes, dict) and set(hashes) == EXPECTED_SOURCES,
            "snapshot: exact expected 14 algorithm/runner files required")
    for path, digest in hashes.items():
        require(isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest),
                f"snapshot: invalid SHA-256 for {path}")
        require(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest,
                f"source changed since real CUDA run: {path}")


def validate_recommendation(rec):
    diagnostic(rec, "recommendation")
    require(rec.get("device") == "cuda" and rec.get("accelerator") == MODEL and rec.get("seeds") == SEEDS,
            "recommendation: actual selected CUDA device/seeds required")
    rows_with_seeds(rec.get("results"), "recommendation")
    dataset = None
    for outer in rec["results"]:
        require(set(outer) == {"seed", *REC_MODULES}, "recommendation: exact three component keys required")
        for subkey, (key, _) in REC_MODULES.items():
            row = outer[subkey]
            diagnostic(row, key)
            require(row.get("seed") == outer["seed"] and row.get("method") == key,
                    f"{key}: inner seed/method differs from outer identity")
        static, cross, transx = (outer[key] for key in ("static", "cross_task", "transx"))
        for row in (static, cross):
            current = row["dataset"]
            require(current.get("id") == "KuaiRand-Pure/official-standard-log-fixed-prefix" and
                    current.get("revision") == PUBLIC_REC_REVISION and current.get("rows") == 4096,
                    "recommendation: pinned public input identity/slice differs")
            if dataset is None:
                dataset = current
            require(current == dataset, "recommendation: public slices differ between methods/seeds")
        count(static["decoded"], "STATIC.decoded", minimum=1)
        require(static["valid_decoded"] == static["decoded"] and static["validity"] == 1,
                "STATIC: emitted invalid identifiers")
        count(static["constraint_items"], "STATIC.constraint_items", minimum=101)
        positive(static["mean_extraction_ms"], "STATIC.mean_extraction_ms")
        require(cross["test_used_only_after_fixed_training"] is True and
                cross["input_contains_feedback"] is False and cross["hyperparameter_selection"] is False,
                "cross-task: feedback/selection isolation contract failed")
        require(set(cross["arms"]) == {"marginals", "cross-label", "shuffled-cross-control"},
                "cross-task: exact three training arms required")
        require(set(cross["training_pair_counts"]) == {"00", "01", "10", "11"},
                "cross-task: four binary label states required")
        for value in cross["training_pair_counts"].values():
            count(value, "cross-task.training_pair_counts", minimum=1)
        for arm, measured in cross["arms"].items():
            require(measured["optimizer_steps"] == 32, f"cross-task.{arm}: fixed 32-step budget required")
            positive(measured["parameter_delta_l2"], f"cross-task.{arm}.parameter_delta")
            for split in ("validation", "test"):
                number(measured[split + "_bce"], f"cross-task.{arm}.{split}_bce", minimum=0)
                number(measured[split + "_brier"], f"cross-task.{arm}.{split}_brier", minimum=0, maximum=1)
        number(transx["maximum_forward_error"], "TransX.forward_error", minimum=0, maximum=1e-10)
        number(transx["maximum_gradient_error"], "TransX.gradient_error", minimum=0, maximum=1e-9)
        positive(transx["embedding_delta_l2"], "TransX.embedding_delta")
        require(transx["untouched_row_error"] == 0 and transx["row_accumulator_elements"] == 32,
                "TransX: sparse-row update contract failed")
        require(0 < transx["counts"]["atomic_tokens_pooled"] < transx["counts"]["direct_tokens_pooled"] and
                transx["counts"]["events"] == 7, "TransX: shared pooling execution missing")


def validate_foundation(foundation, snapshot):
    diagnostic(foundation, "foundation")
    components = foundation.get("components")
    require(isinstance(components, dict) and set(components) == FOUNDATION_METHODS,
            "foundation: exact two component keys required")
    for key, result in components.items():
        diagnostic(result, key)
        require(result.get("device") == "cuda" and result.get("accelerator") == MODEL and result.get("seeds") == SEEDS,
                f"{key}: CUDA device/seeds mismatch")
        require(result.get("method") == key and result.get("measured_locally") is True,
                f"{key}: measured component identity missing")
        require(result["dataset"].get("id") == "synthetic-formula-tensors" and
                result["dataset"].get("revision") == "oct16-component-v1" and
                result["dataset"].get("checkpoint") is None and
                result["dataset"].get("capability_benchmark") is False,
                f"{key}: synthetic diagnostic/checkpoint boundary differs")
        source = f"src/auto_research/foundation_models/{key.replace('-', '_')}.py"
        provenance = result["provenance"]
        require(provenance.get("code_commit") == snapshot["commit"], f"{key}: raw commit differs from snapshot")
        require(provenance.get("implementation_sha256") == snapshot["executed_source_sha256"][source] and
                provenance.get("runner_sha256") == snapshot["executed_source_sha256"][RUNNERS["foundation"]],
                f"{key}: raw implementation/runner hashes differ from executed snapshot")
        rows_with_seeds(result.get("per_seed"), key)
        for row in result["per_seed"]:
            metric = row["metrics"]
            if key == "rope-relay":
                for field in ("values_unchanged", "nonrotary_tail_unchanged", "heterogeneous_endpoints_aligned",
                              "query_and_answer_positions_synchronized"):
                    require(metric[field] is True, f"{key}: {field} failed")
                number(metric["max_reference_absolute_error"], f"{key}.reference_error", minimum=0, maximum=3e-5)
                positive(metric["unsynchronized_query_mean_logit_error"] - 1e-4, f"{key}.query_negative_control")
                gradients = ("gradient_norm_keys", "gradient_norm_values", "gradient_norm_queries")
            else:
                require(metric["phase_lock_and_protection_correct"] is True, "cots: phase-lock/protection failed")
                number(metric["minimum_discrete_anchor_weight"], "cots.anchor", minimum=.5, maximum=1)
                number(metric["alpha_minimum"], "cots.alpha_min", minimum=0, maximum=.5)
                number(metric["alpha_maximum"], "cots.alpha_max", minimum=metric["alpha_minimum"], maximum=.5)
                number(metric["maximum_half_drift_bound_excess"], "cots.drift_bound", maximum=1e-6)
                gradients = ("gradient_norm_logits", "gradient_norm_embeddings")
            for field in gradients:
                positive(metric[field], f"{key}.{field}")
        expected = {}
        for field, first in result["per_seed"][0]["metrics"].items():
            values = [row["metrics"][field] for row in result["per_seed"]]
            expected[field] = all(values) if isinstance(first, bool) else average(values)
        require(set(result["metrics"]) == set(expected), f"{key}: aggregate fields differ")
        for field, value in expected.items():
            if isinstance(value, bool):
                require(result["metrics"][field] is value, f"{key}: boolean aggregate differs")
            else:
                require(set(result["metrics"][field]) == {"mean", "std", "n"}, f"{key}: invalid aggregate schema")
                require(result["metrics"][field]["n"] == 3, f"{key}: aggregate seed count differs")
                for statistic in ("mean", "std"):
                    close(result["metrics"][field][statistic], value[statistic], f"{key}.{field}.{statistic}")


def validate_post(post):
    diagnostic(post, "post-training")
    require(post.get("accelerator") == MODEL and post.get("seeds") == SEEDS,
            "post-training: CUDA accelerator/seeds mismatch")
    require(isinstance(post.get("results"), dict) and set(post["results"]) == set(POST_METHODS) and
            post.get("methods") == list(POST_METHODS), "post-training: exact six method keys/order required")
    require(post.get("papers") == POST_PAPERS and post.get("evolve_integrated") is False,
            "post-training: paper identities/nonintegration boundary differ")
    resource = post["public_resources"]
    require(resource["corpus_sha256"] == CORPUS_SHA256 and resource["corpus_id"] == "gutenberg:1524" and
            resource["corpus_revision"] == "sha256:" + CORPUS_SHA256, "post-training: pinned public corpus differs")
    require(resource["byte_ranges"] == {"train": [0, 165516], "validation": [165516, 186205], "test": [186205, 206895]},
            "post-training: isolated byte ranges differ from pinned corpus protocol")
    protocol = post["protocol"]
    require(protocol["separate_train_validation_test"] is True and protocol["teacher_steps"] == 8 and
            protocol["specialist_steps"] == 4 and protocol["student_steps"] == 2 and protocol["max_new_tokens"] == 16,
            "post-training: fixed diagnostic budget/split protocol differs")
    for key in POST_METHODS:
        rows = post["results"][key]
        rows_with_seeds(rows, key)
        for row in rows:
            positive(row["parameter_delta_l2"], f"{key}.parameter_delta")
            for field in ("baseline_validation_nll", "final_validation_nll", "final_test_nll"):
                number(row[field], f"{key}.{field}", minimum=0)
            require(row["frozen_teacher_parameter_deltas_l2"] == [0., 0.] and
                    row["frozen_rl_snapshot_parameter_deltas_l2"] == [0., 0., 0.],
                    f"{key}: frozen teacher/snapshot parameters changed")
            if key == "tf-opd":
                require(row["method_optimizer_updates"] == 0, "tf-opd: fusion must not run optimizer updates")
                require(len(row["teacher_rollout_audits"]) == 2, "tf-opd: two own-teacher rollout audits required")
                for audit in row["teacher_rollout_audits"]:
                    require(audit["source"] == "teacher_self_generated_then_teacher_forced" and
                            audit["correctness_filter"] is False and 4 <= audit["kept_rollouts"] <= audit["seen_rollouts"] <= 24,
                            "tf-opd: own-rollout filtering/replay contract failed")
                    require(audit["layer_token_counts"] and all(type(n) is int and n > 0 for n in audit["layer_token_counts"].values()),
                            "tf-opd: no actual replay token statistics")
                require(set(row["linear_layers"]) == {"head"}, "tf-opd: expected BytePolicy head solve missing")
                solved = row["linear_layers"]["head"]
                number(solved["normal_equation_residual_l2"], "tf-opd.solve_residual", minimum=0, maximum=1e-8)
                require(solved["solve_dtype"] == "float64" and solved["storage_dtype"] == "float32" and
                        solved["pseudoinverse"] is False, "tf-opd: actual closed-form solve precision differs")
                require(len(solved["unreproduced_share"]) == 2, "tf-opd: missing per-teacher solve diagnostics")
                for value in solved["unreproduced_share"]:
                    number(value, "tf-opd.unreproduced_share", minimum=0)
                continue
            count(row["generated_tokens"], f"{key}.generated_tokens", minimum=1)
            count(row["natural_eos_rollouts"], f"{key}.natural_eos_rollouts")
            count(row["rejected_diagnostic_groups"], f"{key}.rejected_groups")
            history = row["history"]
            require(len(history) == 2 and [step["step"] for step in history] == [0, 1], f"{key}: two real updates required")
            for step in history:
                number(step["loss"], f"{key}.loss")
                positive(step["gradient_norm"], f"{key}.gradient_norm")
            if key == "waypoint-opd":
                lineage = row["teacher_snapshot_lineage"]
                require(len(lineage) == 3 and all(x.get("run_id") for x in lineage) and
                        len({x["run_id"] for x in lineage}) == 1 and [x["step"] for x in lineage] == [0, 4, 8],
                        "waypoint-opd: ordered same-run RL snapshots required")
                audit = row["teacher_rl_audit"]
                require(audit["updates"] == 8 and audit["rollouts_per_update"] == 64 and
                        audit["rollout_horizon"] == 1 and audit["checkpoint_steps"] == [0, 4, 8] and
                        audit["total_sampled_actions"] == 512,
                        "waypoint-opd: fixed 8x64 causal teacher-RL execution missing")
                close(audit["learning_rate"], .2, "waypoint.teacher_rl_learning_rate")
                require(audit["selection"] == "none; fixed 0/4/8 checkpoints, no retries or reward/gate-based selection",
                        "waypoint-opd: teacher snapshots must not be selected/retried")
                require(len(audit["history"]) == 8 and [s["step"] for s in audit["history"]] == list(range(1, 9)),
                        "waypoint-opd: eight actual teacher-RL updates required")
                for update in audit["history"]:
                    require(update["sampled_actions"] == 64, "waypoint-opd: causal sampled-action count differs")
                    number(update["mean_rule_reward"], "waypoint.teacher_rule_reward", minimum=0, maximum=1)
                    positive(update["gradient_norm"], "waypoint.teacher_gradient_norm")
                for step in history:
                    number(step["mean_gate"], "waypoint.mean_gate", minimum=0, maximum=1)
                    number(step["zero_gate_fraction"], "waypoint.zero_gate_fraction", minimum=0, maximum=1)
                    number(step["batch_scale"], "waypoint.batch_scale", minimum=.75, maximum=1.5)
                    count(step["valid_tokens"], "waypoint.valid_tokens", minimum=1)
            elif key == "ggpo":
                require(row["reference_refreshes"] == 1 and row["behavior_syncs"] == 1 and row["behavior_is_reference"] is False,
                        "ggpo: behavior/reference roles or refresh missing")
                for index, step in enumerate(history):
                    require(step["branch"] == "direct_autograd" and step["reference_refreshed"] is bool(index),
                            "ggpo: direct branch/reference cadence differs")
                    count(step["retained_groups"], "ggpo.retained_groups", minimum=1)
                    number(step["raw_gap"], "ggpo.raw_gap", minimum=0)
                    positive(step["mean_length"], "ggpo.mean_length")
            elif key == "stopd":
                for index, step in enumerate(history):
                    require(step["warmup"] is (index == 0) and
                            step["normalizer_source"] == ("current_exact_warmup" if index == 0 else "previous_batch"),
                            "stopd: warmup/lagged denominator contract failed")
                    count(step["retained_tokens"], "stopd.retained_tokens", minimum=1)
                    positive(step["denominator"], "stopd.denominator")
                    number(step["weighted_count_for_next_batch"], "stopd.weighted_count", minimum=step["retained_tokens"])
                    cutoffs = step["cutoffs"]
                    require(len(cutoffs) == 4 and all(type(n) is int and 1 <= n <= 16 for n in cutoffs) and
                            step["retained_tokens"] <= sum(cutoffs), "stopd: invalid pre-generation cutoffs/counts")
                    close(step["denominator"], history[index-1]["weighted_count_for_next_batch"] if index else step["retained_tokens"],
                          "stopd.denominator")
                require(row["generated_tokens"] == sum(step["retained_tokens"] for step in history),
                        "stopd: generated/retained token accounting differs")
            elif key == "cce-opd":
                require(bool(row["condition_pair_source"]), "cce-opd: supplied condition provenance required")
                for step in history:
                    count(step["valid_tokens"], "cce.valid_tokens", minimum=1)
                    count(step["auxiliary_tokens"], "cce.auxiliary_tokens")
                    require(step["auxiliary_tokens"] <= step["valid_tokens"] and 1 <= step["max_union_size"] <= 32,
                            "cce-opd: support/entropy selection count failed")
                    close(step["loss"], step["opd_loss"] + step["auxiliary_loss"], "cce.combined_loss")
            else:
                for step in history:
                    require(step["paper_default_minimum_length"] == 550 and step["paper_default_eligible_responses"] == 0 and
                            step["diagnostic_minimum_length"] == 6 and step["short_window_diagnostic_only"] is True,
                            "sif: paper-default exclusion/explicit short-window boundary missing")
                    require(2 <= step["eligible_responses"] <= 4 and step["retained_groups"] == 1,
                            "sif: no eligible informative response group")
                    count(step["updated_tokens"], "sif.updated_tokens", minimum=1)


def read(path):
    return json.loads(path.read_text())


def average(values):
    return {"mean": statistics.mean(values), "std": statistics.stdev(values), "n": len(values)}


def write(relative, payload):
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def dataset_fingerprint(key, dataset):
    """Use actual public hashes, or the explicitly seeded fixture identity.

    A synthetic protocol ID is not misrepresented as a hash of tensor bytes.
    The separate executed-source hashes bind its exact input construction.
    """
    digest = dataset.get("source_sha256")
    if digest:
        require(isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest),
                f"{key}: invalid public dataset hash")
        return "sha256:" + digest, "public-corpus-bytes"
    revision = dataset.get("revision", "")
    if revision.startswith("sha256:"):
        require(re.fullmatch(r"sha256:[0-9a-f]{64}", revision), f"{key}: invalid selected-input revision")
        return revision, "public-selected-input-fields"
    require(bool(dataset.get("id")) and bool(revision), f"{key}: dataset/fixture identity and revision required")
    return (f"{key}:{dataset['id']}@{revision};seeds=42,43,44", "seeded-fixture-protocol-id-not-tensor-byte-hash")


def curate(directory: Path):
    snapshot = read(directory / "executed-source.json")
    rec = read(directory / "recommendation.json")
    foundation_raw = read(directory / "foundation.json")
    post = read(directory / "post-training.json")
    for label, raw in (("snapshot", snapshot), ("recommendation", rec),
                       ("foundation", foundation_raw), ("post-training", post)):
        finite_tree(raw, label)
    validate_snapshot(snapshot)
    validate_recommendation(rec)
    validate_foundation(foundation_raw, snapshot)
    validate_post(post)
    commit = snapshot["commit"]
    # Recommendation/post runners do not expose per-result source hashes in
    # their frozen raw schema. Bind their controlled-export snapshot sidecar,
    # and retain the exact raw-file fingerprints; do not invent absent fields.
    input_hashes = {name: hashlib.sha256((directory / name).read_bytes()).hexdigest() for name in
                    ("executed-source.json", "recommendation.json", "foundation.json", "post-training.json")}
    catalog = {}
    selected_keys = {"static-constraint-decoding", "cross-task-relationships", "transx",
                     *FOUNDATION_METHODS, *POST_METHODS}
    for path in (ROOT / "src/auto_research/paper_specs/catalog").glob("*/*.json"):
        row = read(path)
        # Catalog identity is normally (domain, key); unrelated methods may
        # legitimately share a short key. Only this selected bundle must be
        # unambiguous for its fixed key-to-receipt mapping.
        if row["key"] not in selected_keys:
            continue
        require(row["key"] not in catalog, f"duplicate catalog key: {row['key']}")
        catalog[row["key"]] = row
    require(set(catalog) == selected_keys, "selected CUDA catalog entries are incomplete")
    pending = []

    def emit(key, rows, dataset, metrics, command, sources, checks, raw_file, *, record_key=None):
        row = catalog[record_key or key]
        base = "docs/" + str(Path(row["detail_path"]).parent)
        metric_path = base + "/metrics/" + ("report-components-" if key == "transx-report-components" else "component-") + "a100-seeds42-44.json"
        receipt_path = f"docs/gpu-validations/{key}-a100-20261016.json"
        hashes = {path: snapshot["executed_source_sha256"][path] for path in sources}
        checkpoint = {"public_id": "none-independent-seeded-initialization", "revision": commit,
                      "pretrained": False, "initialization_seeds": SEEDS}
        tier = row.get("evaluation_tier", "l1_mechanism")
        fingerprint, fingerprint_scope = dataset_fingerprint(key, dataset)
        payload = {"schema_version": 2, "method": key, "manifest_ref": row["domain"] + ":" + row["key"],
                   "adapter": None, "implementation_status": "component_only", "evolve_integrated": False,
                   "seeds": SEEDS, "diagnostic_only": True, "promotion_eligible": False,
                   "evaluation_tier": tier, "dataset": dataset,
                   "evaluation_protocol": {"tier": tier, "seeds": SEEDS,
                       "formal_comparison": False, "claim_policy": "bounded operators/updates only, no paper benchmark or production lift"},
                   "metrics": metrics, "per_seed": rows, "execution_checks": checks,
                   "provenance": {"artifact_path": metric_path, "commit": commit,
                       "executed_source_sha256": hashes, "accelerator": MODEL, "command": command,
                       "dataset_fingerprint": fingerprint, "dataset_fingerprint_scope": fingerprint_scope,
                       "raw_result_sha256": input_hashes[raw_file],
                       "source_snapshot_sha256": input_hashes["executed-source.json"]},
                   "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True}
        pending.append((metric_path, payload))
        pending.append((receipt_path, {"schema_version": 1, "adapter_key": key, "validated_at": "2026-10-16",
              "accelerator": {"vendor": "NVIDIA", "model": MODEL}, "command": command,
              "seeds": SEEDS, "dataset": dataset, "checkpoint": checkpoint, "result": "passed",
              "metrics": metrics, "execution_checks": checks, "diagnostic_only": True,
              "promotion_eligible": False, "executed_source_sha256": hashes,
              "full_experiment_status": "not_reproduced_high_cost",
              "command_path_policy": "public input and output paths relativized; source/data content hashes retained",
              "provenance": {"commit": commit, "artifact_path": receipt_path, "metric_artifact_path": metric_path,
                  "dataset_fingerprint": fingerprint, "dataset_fingerprint_scope": fingerprint_scope,
                  "raw_result_sha256": input_hashes[raw_file],
                  "source_snapshot_sha256": input_hashes["executed-source.json"]}}))

    root_command = ["python", "scripts/run_oct16_recommendation_components.py", "--csv", "public/kuairand-prefix.csv",
                    "--device", "cuda", "--seeds", "42,43,44", "--output", "runs/oct16-p0p1/recommendation.json"]
    for subkey, key, module in (("static", "static-constraint-decoding", "static_constraint_decoding/algorithm.py"),
                               ("cross_task", "cross-task-relationships", "cross_task_relationships/model.py"),
                               ("transx", "transx-report-components", "transx/technical_report.py")):
        rows = [r[subkey] for r in rec["results"]]
        if subkey == "static":
            metrics = {name: average([r[name] for r in rows]) for name in ("validity", "mean_extraction_ms")}
            checks = {"csr_and_dense_decode_executed": True, "all_emitted_identifiers_in_public_constraint_set": True,
                      "trained_sid_or_retrieval_model": False, "microbenchmark_not_end_to_end_latency": True}
        elif subkey == "cross_task":
            metrics = {arm: {name: average([r["arms"][arm][name] for r in rows])
                       for name in ("validation_bce", "validation_brier", "test_bce", "test_brier", "parameter_delta_l2")}
                       for arm in rows[0]["arms"]}
            checks = {"three_actual_training_arms": True, "same_initialization_and_minibatch_stream": True,
                      "authentic_public_feedback_labels": True, "no_hyperparameter_selection": True,
                      "test_after_fixed_training_only": True, "production_rl_policy_trained": False}
        else:
            metrics = {name: average([r[name] for r in rows]) for name in
                       ("maximum_forward_error", "maximum_gradient_error", "embedding_delta_l2", "untouched_row_error")}
            checks = {"exact_shared_vs_direct_forward_and_gradient": True, "logical_step_duplicate_rows_coalesced": True,
                      "sparse_embedding_and_dense_parameter_updates": True, "production_model_trained": False}
        emit(key, rows, rows[0]["dataset"], metrics, root_command,
             ["src/auto_research/reproductions/" + module, "scripts/run_oct16_recommendation_components.py"],
             checks, "recommendation.json", record_key="transx" if subkey == "transx" else None)

    foundation = foundation_raw["components"]
    for key in ("rope-relay", "cots"):
        result = foundation[key]
        rows = result["per_seed"]
        emit(key, rows, result["dataset"], result["metrics"],
             ["python", "scripts/run_oct16_foundation_components.py", "--papers", "rope-relay,cots", "--device", "cuda",
              "--seeds", "42,43,44", "--code-commit", commit, "--output", "runs/oct16-p0p1/foundation.json"],
             [f"src/auto_research/foundation_models/{key.replace('-', '_')}.py", "scripts/run_oct16_foundation_components.py"],
             {"real_cuda_formula_and_gradient_diagnostic": True, "model_capability_evaluated": False}, "foundation.json")

    resource = post["public_resources"]
    dataset = {"id": resource["corpus_id"], "revision": resource["corpus_revision"],
               "source_sha256": resource["corpus_sha256"], "byte_ranges": resource["byte_ranges"],
               "source_url": "https://www.gutenberg.org/ebooks/1524"}
    command = ["python", "scripts/run_oct16_post_components.py", "--corpus-path", "public/hamlet.txt",
               "--corpus-id", resource["corpus_id"], "--corpus-revision", resource["corpus_revision"],
               "--corpus-sha256", resource["corpus_sha256"], "--device", "cuda", "--seeds", "42,43,44",
               "--output", "runs/oct16-p0p1/post-training.json"]
    for key in POST_METHODS:
        rows = post["results"][key]
        metrics = {name: average([r[name] for r in rows]) for name in
                   ("parameter_delta_l2", "baseline_validation_nll", "final_validation_nll", "final_test_nll")}
        emit(key, rows, dataset, metrics, command,
             [f"src/auto_research/post_training/{key.replace('-', '_')}.py", "scripts/run_oct16_post_components.py"],
             {"actual_policy_generation_and_parameter_change": True,
              "teacher_self_generation_and_filtered_replay": key == "tf-opd", "frozen_teachers_unchanged": True,
              "train_validation_test_bytes_separated": True, "public_unlabeled_text_or_controlled_rule_reward_diagnostic": True,
              "full_paper_benchmark": False, "default_550_token_sif_training": False}, "post-training.json")

    # Entire bundle is validated and serializable before the first write. A
    # missing late method or malformed aggregate cannot leave passed receipts.
    require(len(pending) == 22 and len({name for name, _ in pending}) == 22,
            "curation must produce exactly eleven unique metric/receipt pairs")
    for _, payload in pending:
        json.dumps(payload, ensure_ascii=False, allow_nan=False)
    for name, payload in pending:
        write(name, payload)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    curate(parser.parse_args().input_dir)
