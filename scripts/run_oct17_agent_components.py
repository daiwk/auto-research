"""Bounded CPU diagnostics: inert audit records and synthetic operator fixtures.

No checkpoint, model endpoint, shell tool, or autonomous agent is executed.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import statistics
import subprocess
import time

import numpy as np

from auto_research.agent_research import disagreement_routing as routing
from auto_research.agent_research import shortcut_sensitivity as shortcut
from auto_research.agent_research import tracer

ROOT = Path(__file__).resolve().parents[1]
KEYS = ("shortcut-sensitivity", "disagreement-routing", "tracer")
SOURCE_PATHS = ("scripts/run_oct17_agent_components.py", *(
    f"src/auto_research/agent_research/{key}.py" for key in
    ("shortcut_sensitivity", "disagreement_routing", "tracer")))


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def summarize(rows):
    result = {}
    for key in rows[0]["metrics"]:
        values = [row["metrics"][key] for row in rows]
        result[key] = {"mean": statistics.mean(values),
                       "std": statistics.stdev(values) if len(values) > 1 else 0., "n": len(values)}
    return result


def _reference_lookup(rows):
    """Brute-force reference independent of module majority/metric helpers."""
    predictions = []
    for target in rows:
        train = [r for r in rows if r.domain != target.domain]
        matching = [r.label for r in train if r.tool.lower() == target.tool.lower()]
        values = matching or [r.label for r in train]
        predictions.append(int(sum(values) >= len(values) / 2))
    return predictions


def shortcut_diagnostic(seeds, cache):
    rows = [shortcut.AuditRow(f"d{d}-i{i}-s{s}", f"d{d}", f"i{i}",
                             f"tool{d}_{i % 4}", int(i % 4 >= 2))
            for d in range(4) for i in range(20) for s in range(1 + i % 3)]
    if cache is not None:
        rows, harm, predictions, sources = shortcut.load_public_audit(cache)
        weighting = shortcut.evaluation_units(harm, predictions)
        dataset = {"id": "MurrayTom/ToolSafe-TS-Bench-public-audit", "revision": shortcut.DATA_REVISION,
                   "artifacts": sources, "raw_records_redistributed": False}
    else:
        harm, weighting = [], None
        dataset = {"id": "synthetic-shortcut-unit-fixture", "revision": fingerprint([
            [r.row_id, r.domain, r.interaction, r.tool, r.label] for r in rows]),
            "public_benchmark_evaluated": False}
    lodo = shortcut.leave_one_domain_out(rows)
    reference = _reference_lookup(rows)
    assert reference == lodo["predictions"]
    deterministic = {"rows": len(rows), "domains": len({r.domain for r in rows}),
                     "lodo_f1": lodo["metrics"]["row"]["f1"],
                     "lodo_balanced_accuracy": lodo["metrics"]["row"]["balanced_accuracy"],
                     "seen_tool_fraction": lodo["seen_tool_fraction"],
                     "independent_reference_prediction_errors": sum(a != b for a, b in zip(reference, lodo["predictions"], strict=True)),
                     "dropped_rows": 0, "new_guard_calls": 0}
    if weighting is not None:
        deterministic.update({"agentharm_rows": len(harm), "agentharm_interactions": weighting["interactions"],
                              "guard_row_f1": weighting["row"]["f1"],
                              "guard_equal_interaction_f1": weighting["equal_interaction"]["f1"],
                              "guard_row_balanced_accuracy": weighting["row"]["balanced_accuracy"],
                              "guard_equal_interaction_balanced_accuracy": weighting["equal_interaction"]["balanced_accuracy"]})
    per_seed = []
    for seed in seeds:
        cv = shortcut.grouped_lookup_cv(rows, seed=seed)
        per_seed.append({"seed": seed, "seed_role": "interaction_fold_shuffle_not_model_training",
                         "metrics": {"mixed_domain_grouped_cv_f1": cv["metrics"]["row"]["f1"],
                                     "cv_minus_domain_holdout_f1": cv["metrics"]["row"]["f1"] - deterministic["lodo_f1"],
                                     "retained_row_fraction": 1.}})
    return {"dataset": dataset, "per_seed": per_seed, "metrics": summarize(per_seed),
            "deterministic": {"metrics": deterministic, "repetitions": 1,
                              "interpretation": "released-label lookup / frozen guard prediction audit, not new capability"},
            "isolation": {"held_out_domain_labels_used_for_lookup_fit": False,
                          "lookup_label_access_is_diagnostic_only": True,
                          "no_tool_record_executed": True},
            "full_experiment_status": "not_reproduced_high_cost"}


def _routing_fixture(seed):
    rng = np.random.default_rng(seed)
    features = rng.normal(size=(128, 3))
    logits = np.column_stack((features[:, 0], -features[:, 0] + features[:, 1], features[:, 2]))
    probabilities = np.exp(logits - logits.max(1, keepdims=True))
    probabilities /= probabilities.sum(1, keepdims=True)
    weak, strong = [], []
    for p in probabilities:
        weak.append(tuple(int(x) for x in rng.choice(3, 2)))
        strong.append(tuple(int(x) for x in rng.choice(3, 12, p=p)))
    responses = np.stack([np.stack([np.concatenate((x, np.eye(3)[w])) for w in candidates])
                          for x, candidates in zip(features, weak, strict=True)])
    return features, responses, weak, strong


def routing_diagnostic(seed):
    x, responses, weak, strong = _routing_fixture(seed)
    # Explicit disjoint prompt IDs: 0..79 train, 80..103 validation, 104..127 test.
    trained = routing.fit_router(x[:80], responses[:80], weak[:80], strong[:80], seed=seed, steps=200)
    validation_scores = trained.scores(x[80:104], responses[80:104])
    calibration = routing.calibrate_budget(validation_scores, .25)
    score = trained.scores(x[104:], responses[104:])
    d_target, g_target, reference_errors = [], [], []
    for candidates, draws in zip(weak, strong, strict=True):
        d, g = routing.empirical_targets(candidates, draws)
        count = Counter(draws)
        reference_d = np.array([1 - count[c] / len(draws) for c in candidates])
        reference_g = 1 - sum(v * (v - 1) for v in count.values()) / (len(draws) * (len(draws) - 1))
        reference_errors.append(max(float(np.abs(reference_d - d).max()), abs(reference_g - g)))
        d_target.append(d)
        g_target.append(g)
    target_score = np.array([min(d) - g for d, g in zip(d_target, g_target, strict=True)])
    shuffled = np.random.default_rng(seed + 123).permutation(80)
    negative = routing.fit_probability_probe(x[:80], np.asarray(g_target)[:80][shuffled], seed=seed + 1)
    clean_mae = float(np.abs(trained.prompt_probe.predict(x[104:]) - np.asarray(g_target)[104:]).mean())
    negative_mae = float(np.abs(negative.predict(x[104:]) - np.asarray(g_target)[104:]).mean())
    assert max(reference_errors) < 1e-12
    assert calibration.validation_routed <= 6
    assert trained.response_probe.final_loss < trained.response_probe.initial_loss
    assert trained.prompt_probe.final_loss < trained.prompt_probe.initial_loss
    return {"seed": seed, "fixture_sha256": fingerprint([x.tolist(), weak, strong]), "metrics": {
        "response_probe_bce_initial": trained.response_probe.initial_loss,
        "response_probe_bce_final": trained.response_probe.final_loss,
        "prompt_probe_bce_initial": trained.prompt_probe.initial_loss,
        "prompt_probe_bce_final": trained.prompt_probe.final_loss,
        "independent_target_max_absolute_error": max(reference_errors),
        "held_out_score_mae": float(np.abs(score - target_score[104:]).mean()),
        "validation_routed_fraction": calibration.validation_routed / 24,
        "test_realized_routed_fraction": float(calibration.route(score).mean()),
        "clean_prompt_probe_test_mae": clean_mae,
        "shuffled_target_prompt_probe_test_mae": negative_mae,
        "parameter_delta_response_l2": trained.response_probe.parameter_delta_l2,
        "retained_test_fraction": 1.},
        "calibration": {"requested_budget": .25,
                        "threshold": calibration.threshold if math.isfinite(calibration.threshold) else None,
                        "threshold_is_positive_infinity": math.isinf(calibration.threshold),
                        "split": "validation", "train_prompts": 80, "validation_prompts": 24, "test_prompts": 24}}


def _tracer_fixture(seed):
    rng = np.random.default_rng(seed)
    registry = {"lookup": (1., 0., 0.), "verify_red": (0., 1., 0.),
                "verify_blue": (0., 0., 1.), "finish": (.1, .7, .7), "unused": (-1., 0., 0.)}
    steps = []
    for i in range(60):
        color = "red" if i % 4 else "blue"
        vector = np.array((.4, 1., .1) if color == "red" else (.4, .1, 1.))
        vector += rng.normal(0, .06, 3)
        tools = ("lookup", f"verify_{color}", "finish")
        for j, tool in enumerate(tools):
            steps.append(tracer.TrainingStep(f"trajectory-{i}", tools[:j], tuple(vector), 6 + i % 5, i % 3, tool))
    return registry, steps[:120], steps[120:]


def tracer_diagnostic(seed):
    registry, train, test = _tracer_fixture(seed)
    model, training = tracer.fit_tracer(train, registry, seed=seed, epochs=150)
    examples, _ = tracer.crossfit_examples(train, registry, seed=seed)
    assert all(e.target_trajectory not in e.index_trajectories for e in examples)
    assert not ({s.trajectory_id for s in test} & model.index.trajectory_ids)
    correct, shuffled_correct, fallback, weights, temperatures = 0, 0, 0, [], []
    for step in test:
        out = model.retrieve(step.prefix, step.context, query_words=step.query_words,
                             prior_turns=step.prior_turns, k=1)
        corrupt_context = (step.context[0], step.context[2], step.context[1])
        corrupt = model.retrieve(step.prefix, corrupt_context, query_words=step.query_words,
                                 prior_turns=step.prior_turns, k=1)
        correct += step.next_tool in out["tools"]
        shuffled_correct += step.next_tool in corrupt["tools"]
        fallback += out["used_global_fallback"]
        weights.append(out["empirical_weight"])
        temperatures.append(out["temperature"])
    unknown = model.retrieve(("unused",), (0., 1., 0.), query_words=5, prior_turns=0, k=2)
    assert unknown["used_global_fallback"] and len(unknown["tools"]) == 2
    assert training["parameter_delta_l2"] > 0
    assert training["final_crossfit_nll"] < training["initial_crossfit_nll"]
    return {"seed": seed, "metrics": {
        **{k: v for k, v in training.items() if isinstance(v, (int, float))},
        "fixture_held_out_next_tool_recall_at_1": correct / len(test),
        "corrupted_context_recall_at_1": shuffled_correct / len(test),
        "held_out_fallback_fraction": fallback / len(test),
        "minimum_empirical_weight": min(weights), "maximum_empirical_weight": max(weights),
        "minimum_temperature": min(temperatures), "retained_test_fraction": 1.,
        "unseen_prefix_fallback_checked": 1.},
        "fixture_sha256": fingerprint([[s.trajectory_id, s.prefix, s.context, s.next_tool] for s in train + test]),
        "training_protocol": {"train_trajectories": 40, "test_trajectories": 20,
                              "inner_folds": 5, "standardizer": "crossfit training examples only",
                              "context_encoder": "synthetic 3-vector, not text-embedding-3-small"}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--methods", default=",".join(KEYS))
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--device", choices=("cpu",), default="cpu")
    parser.add_argument("--shortcut-cache", type=Path)
    parser.add_argument("--fetch-shortcut", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    methods = args.methods.split(",")
    seeds = [int(s) for s in args.seeds.split(",")]
    if len(set(methods)) != len(methods) or set(methods) - set(KEYS):
        parser.error("unknown or duplicated method")
    if not seeds or len(seeds) != len(set(seeds)) or len(seeds) > 5 or any(s < 0 or s > 2**32 - 1 for s in seeds):
        parser.error("one to five distinct nonnegative 32-bit seeds required")
    if args.fetch_shortcut and (args.shortcut_cache is None or "shortcut-sensitivity" not in methods):
        parser.error("fetch requires the Shortcut method and an explicit cache directory")
    if args.output.exists():
        raise FileExistsError("immutable output already exists")
    started = time.monotonic()
    if args.fetch_shortcut:
        shortcut.fetch_public_assets(args.shortcut_cache)
    components = {}
    for key in methods:
        if key == "shortcut-sensitivity":
            components[key] = shortcut_diagnostic(seeds, args.shortcut_cache)
        else:
            function = routing_diagnostic if key == "disagreement-routing" else tracer_diagnostic
            rows = [function(seed) for seed in seeds]
            components[key] = {"dataset": {"id": f"synthetic-{key}-mechanism-fixture",
                                           "revision": fingerprint([r["fixture_sha256"] for r in rows]),
                                           "public_benchmark_evaluated": False},
                               "per_seed": rows, "metrics": summarize(rows),
                               "full_experiment_status": "not_reproduced_high_cost",
                               "isolation": {"test_in_fit_or_calibration": False, "formal_comparison": False,
                                             "new_language_model_evaluated": False}}
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    dirty = bool(subprocess.check_output(["git", "status", "--porcelain", "--", *SOURCE_PATHS], cwd=ROOT, text=True).strip())
    output = {"schema_version": 2, "code_commit": commit, "executed_source_uncommitted": dirty,
              "device": "cpu", "diagnostic_only": True, "promotion_eligible": False,
              "evolve_integrated": False, "seeds": seeds, "components": components,
              "evaluation_protocol": {"tier": "l1_mechanism", "formal_comparison": False,
                                      "claim_policy": "CPU audit/algorithm fixtures, not agent capability or original-paper reproduction"},
              "executed_source_sha256": {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in SOURCE_PATHS},
              "elapsed_seconds": time.monotonic() - started,
              "command": "PYTHONPATH=src python scripts/run_oct17_agent_components.py "
                         f"--methods {args.methods} --device cpu --seeds {args.seeds} "
                         + ("--shortcut-cache <pinned-public-cache> " if args.shortcut_cache else "")
                         + "--output <fresh-result.json>"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(output, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"methods": methods, "seeds": seeds, "elapsed_seconds": output["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
