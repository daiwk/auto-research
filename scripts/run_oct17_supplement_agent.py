"""Bounded CPU diagnostics for five Oct-17 supplementary interfaces.

No model, autonomous tool, official benchmark, GPU or network is invoked.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path
import statistics
import subprocess
import time

import numpy as np

from auto_research.agent_research import gacc_bench as gacc
from auto_research.agent_research import leash, probe_audit as probe
from auto_research.agent_research import rsi_flow as rsi, terminal_rsi as terminal


ROOT = Path(__file__).resolve().parents[1]
KEYS = ("rsiflow", "leash", "probe", "terminal-rsi", "gacc-bench")
SOURCE_PATHS = ("scripts/run_oct17_supplement_agent.py", *(
    f"src/auto_research/agent_research/{name}.py" for name in
    ("rsi_flow", "leash", "probe_audit", "terminal_rsi", "gacc_bench")))


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def rsiflow_diagnostic(seed):
    rng = np.random.default_rng(seed)
    batches = [[rsi.Task(f"train-{r}-{i}", {"round": r, "feature": float(rng.normal())})
                for i in range(4)] for r in range(3)]
    report = [rsi.Task(f"report-{i}", {"feature": float(rng.normal())}) for i in range(5)]
    targets = {t.task_id: float(rng.uniform(3., 4.)) for batch in (*batches, report) for t in batch}
    phases = []

    def evaluator(state, tasks, split):
        phases.append(split)
        prediction = state.model + state.harness + state.artifacts
        return {t.task_id: -abs(prediction - targets[t.task_id]) for t in tasks}

    def propose(component):
        def callback(parent, tasks, baseline, skills):
            round_id = tasks[0].payload["round"]
            if not any(s["evidence_round"] == round_id for s in skills):
                raise ValueError("intentional implementation-failure fixture")
            return replace(parent, **{component: getattr(parent, component) + 1.})
        return callback

    result = rsi.evolve(rsi.TaskState(0., 0., 0.), batches, report,
        selector=lambda a, s, c: rsi.COMPONENTS[c["round_index"]],
        proposers={c: propose(c) for c in rsi.COMPONENTS}, evaluator=evaluator)
    assert asdict(result.state) == {"model": 1., "harness": 1., "artifacts": 1.}
    for round_id in range(3):
        rows = [a for a in result.attempts if a.round_index == round_id]
        assert len(rows) == 2 and rows[0].parent_sha256 == rows[1].parent_sha256
    assert phases[-1] == "reporting" and "reporting" not in phases[:-1]
    return {"seed": seed, "fixture_sha256": fingerprint(targets), "metrics": {
        "candidate_attempts": len(result.attempts),
        "accepted_candidates": sum(a.accepted for a in result.attempts),
        "retained_implementation_failures": sum(not a.valid for a in result.attempts),
        "retained_skill_records": len(result.skills),
        "reporting_tasks": len(result.reporting_scores),
        "reporting_numeric_fixture_mean_score": statistics.mean(result.reporting_scores.values()),
        "report_feedback_selection_calls": 0, "independent_final_state_error": 0.},
        "seed_role": "synthetic public payload/held-out target initialization; no language-model training"}


def leash_diagnostic(seed):
    rng = np.random.default_rng(seed)
    n = 30
    y = np.asarray([i % 2 for i in range(n)])
    x = rng.normal(size=(n, 4)) + (2 * y - 1)[:, None] * .6
    actions = np.repeat(x, 3, axis=0) + rng.normal(0, .4, (n * 3, 4))
    groups = [f"reference-{i}" for i in range(n)]
    test_ids = [f"evaluation-{i}" for i in range(12)]
    query_fit = leash.crossfit_reference(x, y, groups, seed=seed, folds=10,
                                        excluded_task_ids=test_ids)
    action_fit = leash.crossfit_reference(actions, np.repeat(y, 3), np.repeat(groups, 3),
                                         seed=seed, folds=10, excluded_task_ids=test_ids)
    for fit in (query_fit, action_fit):
        assert all(task not in fit.fold_training_tasks[fold] for task, fold in fit.task_folds.items())
    calibration = leash.calibrate_escalation(query_fit.scores, action_fit.scores.reshape(n, 3))
    ty = np.asarray([i % 2 for i in range(12)])
    tx = rng.normal(size=(12, 4)) + (2 * ty - 1)[:, None] * .6
    scores = query_fit.estimator.score(tx)
    model = query_fit.estimator
    z = (tx - model.mean) / model.scale
    reference = np.array([float((row - model.pass_mean) @ model.precision @ (row - model.pass_mean)
                                - (row - model.fail_mean) @ model.precision @ (row - model.fail_mean)) for row in z])
    shuffled = leash.fit_lda(x, rng.permutation(y), ridge=query_fit.selected_ridge)
    shadow = leash.ShadowOversight(leash.calibrate_shadow(action_fit.scores))
    for step in range(1, 40):
        shadow.monitor(step, probe_score=lambda: float(max(action_fit.scores) + 1.),
                       intervene=lambda: True)
    error = float(np.max(np.abs(scores - reference)))
    assert error < 1e-10 and shadow.changed_actions == 2
    return {"seed": seed, "fixture_sha256": fingerprint([x.tolist(), actions.tolist(), y.tolist(), tx.tolist()]),
        "metrics": {"reference_tasks": n, "reference_action_vectors": len(actions),
                    "evaluation_tasks": len(tx), "query_oof_auroc": query_fit.oof_auroc,
                    "held_out_numeric_outcome_auroc": leash.auroc(ty, scores),
                    "shuffled_reference_outcome_auroc": leash.auroc(ty, shuffled.score(tx)),
                    "initial_reference_routed_fraction": calibration.initial_routed / n,
                    "overall_reference_routed_fraction": calibration.overall_routed / n,
                    "independent_quadratic_score_max_error": error,
                    "shadow_probes": shadow.probes, "shadow_interventions": shadow.interventions,
                    "shadow_changed_actions": shadow.changed_actions,
                    "test_tasks_in_reference": 0},
        "seed_role": "synthetic representation initialization and grouped OOF assignments"}


def probe_diagnostic(seed):
    rng = np.random.default_rng(seed)
    policies = probe.example_verifiers(required_fields={"search_flights": ("origin", "destination")},
                                       restricted_destinations=("ZZZ",))
    ids = [p.policy_id for p in policies]
    episodes, total, reference_total, reference_hits = [], 0., 0., 0
    fixture = []
    for i in range(12):
        count = int(rng.integers(1, 5))
        if i % 3 == 0:
            call = probe.ToolCall("search_flights", {"destination": "AAA"}, {})
        elif i % 3 == 1:
            call = probe.ToolCall("book_flight", {"destination": "ZZZ", "passengers": 9}, {})
        else:
            call = probe.ToolCall("search_flights", {"origin": "AAA", "destination": "BBB"}, {})
        trace = tuple(probe.Turn("public customer request", "inert reply", (call,)) for _ in range(count))
        events = probe.deterministic_rescore(trace, policies)
        episodes.append(events)
        total += probe.violation_reward(events, policies)["total"]
        hit_ids = set(events[0])
        expected_hits_per_turn = 1 if i % 3 == 0 else 3 if i % 3 == 1 else 0
        reference_hits += expected_hits_per_turn * count
        reference_total += sum(p.severity * (1. + (.5 if count > 1 else 0.))
                               for p in policies if p.policy_id in hit_ids)
        fixture.append([asdict(call), count])
    metric = probe.audit_metrics(episodes, declared_policy_ids=ids + ["unsupported-semantic-policy"],
                                 implemented_policy_ids=ids)
    assert metric["verifier_hits"] == reference_hits
    assert metric["violation_yield_per_100_episodes"] == 100 * reference_hits / 12
    seen = []
    def auditor(scenario, history):
        seen.append(history)
        assert not hasattr(scenario, "policies") and not hasattr(scenario, "reference_answer")
        return "Find a flight"
    result = probe.audit_episode(probe.PublicAuditScenario("inert", "travel"), auditor=auditor,
        target=lambda history: probe.Turn(history[-1][1], "Please provide the origin"),
        private_evaluator=lambda trace: {"private_marker": "never passed to auditor"}, max_turns=3)
    assert all("private_marker" not in str(history) for history in seen)
    assert abs(total - reference_total) < 1e-12
    numeric = {k: v for k, v in metric.items() if isinstance(v, (int, float))}
    return {"seed": seed, "fixture_sha256": fingerprint(fixture), "metrics": {
        **numeric, "violation_reward_total": total,
        "independent_first_repeat_reward_error": abs(total-reference_total),
        "independent_raw_verifier_hit_count_error": abs(metric["verifier_hits"]-reference_hits),
        "auditor_callback_turns": result["turns"], "private_marker_exposures": 0,
        "new_trained_auditors": 0}, "unsupported_policies": metric["unsupported_policies"],
        "seed_role": "inert trace repetition-count initialization; not auditor training"}


def terminal_diagnostic(seed):
    rng = np.random.default_rng(seed)
    n = 20
    values = rng.normal(0, .3, n)
    rewards = np.zeros(n)
    rewards[-1] = 1.
    turns = np.arange(n) // 4
    done = np.zeros(n, bool)
    done[-1] = True
    result = terminal.tb_gae(rewards, values, turns, np.ones(n, bool), done,
                             gamma_turn=.97, lambda_turn=.9)
    reference = np.zeros(n)
    for j in range(n):
        product = 1.
        for k in range(j, n):
            boundary = k < n - 1 and turns[k+1] != turns[k]
            g, l = (.97, .9) if boundary else (1., 1.)
            delta = rewards[k] + (g*values[k+1] if k < n-1 else 0.) - values[k]
            reference[j] += product * delta
            product *= g*l
    cut = 11
    carry = terminal.Continuation(float(values[cut]), float(result.advantages[cut]), int(turns[cut]))
    prefix = terminal.tb_gae(rewards[:cut], values[:cut], turns[:cut], np.ones(cut, bool), done[:cut],
                             gamma_turn=.97, lambda_turn=.9, continuation=carry)
    wrong = terminal.tb_gae(rewards[:cut], values[:cut], turns[:cut], np.ones(cut, bool), done[:cut],
                            gamma_turn=.97, lambda_turn=.9,
                            continuation=terminal.Continuation(float(values[cut]), 0., int(turns[cut])))
    dense_r, dense_v = np.repeat(0., n*3), np.repeat(999., n*3)
    dense_r[::3], dense_v[::3] = rewards, values
    mask = np.zeros(n*3, bool)
    mask[::3] = True
    dense_done = np.zeros(n*3, bool)
    dense_done[(n-1)*3] = True
    expanded = terminal.tb_gae(dense_r, dense_v, np.repeat(turns, 3), mask, dense_done,
                               gamma_turn=.97, lambda_turn=.9)
    div = terminal.calibrate_family_divisors({"fixture": rng.integers(1, 40, 30)})
    fdr = terminal.reward(80, False, "fixture", div, kind="fdr")
    spr = terminal.reward(80, False, "fixture", div)
    error, chunk_error = float(np.max(np.abs(reference-result.advantages))), float(
        np.max(np.abs(prefix.advantages-result.advantages[:cut])))
    observation_error = float(np.max(np.abs(expanded.advantages[mask]-result.advantages)))
    assert max(error, chunk_error, observation_error) < 1e-12
    return {"seed": seed, "fixture_sha256": fingerprint([values.tolist(), rewards.tolist(), turns.tolist()]),
        "metrics": {"generated_positions": n, "observation_positions_tested": n*2,
                    "independent_expansion_max_error": error, "exact_chunk_max_error": chunk_error,
                    "skipped_observation_max_error": observation_error,
                    "reset_trace_negative_control_max_error": float(np.max(np.abs(wrong.advantages-result.advantages[:cut]))),
                    "fdr_failed_rollout_reward": fdr, "spr_failed_rollout_reward": spr,
                    "spr_strict_success_reward": terminal.reward(80, True, "fixture", div)},
        "seed_role": "numeric value/calibration-count initialization; no PPO training"}


def gacc_diagnostic(seed):
    rng = np.random.default_rng(seed)
    codec = gacc.TokenCodec("fixture-unicode-codepoint-token-ids", "v1",
                            lambda text: list(map(ord, text)), lambda ids: "".join(map(chr, ids)))
    cases = []
    for c in range(2):
        lines = [f"{color}:code={color[0]}{c};count={int(rng.integers(10,99))};owner=long_owner_name_{c}_{color}"
                 for color in ("red", "blue")]
        context = "\n".join(lines)
        for line, color in zip(lines, ("red", "blue"), strict=True):
            fields = dict(part.split("=", 1) for part in line.split(":",1)[1].split(";"))
            questions = tuple(gacc.Question(key, key, value) for key, value in fields.items())
            cases.append(gacc.GoalCase(f"context-{c}", color, context, color, questions))
    cache, compressor_inputs, reader_inputs = {}, [], []
    def compressor(value):
        compressor_inputs.append(value)
        assert not hasattr(value, "questions") and not hasattr(value, "reference_answer")
        return next(line for line in value.context.splitlines() if line.startswith(value.goal+":"))
    def reader(value):
        reader_inputs.append(value)
        assert not hasattr(value, "reference_answer")
        text = value.memory.split(":", 1)[-1]
        fields = dict(part.split("=", 1) for part in text.split(";") if "=" in part)
        return fields.get(value.question, "not retained")
    kwargs = dict(compressor=compressor, reader=reader,
                  judge=lambda value: value.candidate_answer == value.reference_answer,
                  codec=codec, retention_ratio=.25, compressor_revision=f"rule-fixture-seed-{seed}",
                  reader_revision="field-parser-fixture-v1", judge_revision="exact-fixture-v1", cache=cache)
    result = gacc.evaluate(cases, **kwargs)
    repeat = gacc.evaluate(cases, **kwargs)
    assert len(compressor_inputs) == len(cases) and repeat["compressions"] == 0
    q_correct = sum(row["correct"] for row in result["rows"])
    independent_micro = q_correct / sum(len(c.questions) for c in cases)
    budgets_valid = all(row["retained_tokens"] <= row["token_budget"] for row in result["rows"])
    assert independent_micro == result["micro_accuracy"] and budgets_valid
    return {"seed": seed, "fixture_sha256": fingerprint([asdict(c) for c in cases]), "metrics": {
        "goals": result["goals"], "questions": result["questions"], "compressor_calls": result["compressions"],
        "cached_repeat_compressor_calls": repeat["compressions"],
        "fixture_micro_accuracy": result["micro_accuracy"],
        "fixture_macro_all_question_success": result["macro_all_question_success"],
        "independent_micro_error": abs(independent_micro-result["micro_accuracy"]),
        "budget_violations": int(not budgets_valid), "question_gold_exposures_to_compressor": 0,
        "official_cl100k_measurements": 0}, "tokenizer": result["tokenizer"],
        "seed_role": "small string-context initialization; rule parser, no LLM compression"}


FUNCTIONS = dict(zip(KEYS, (rsiflow_diagnostic, leash_diagnostic, probe_diagnostic,
                           terminal_diagnostic, gacc_diagnostic), strict=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--methods", default=",".join(KEYS))
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--device", choices=("cpu",), default="cpu")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    methods, seeds = args.methods.split(","), [int(s) for s in args.seeds.split(",")]
    if not methods or len(set(methods)) != len(methods) or set(methods) - set(KEYS):
        parser.error("distinct known methods required")
    if (not 1 <= len(seeds) <= 5 or len(set(seeds)) != len(seeds)
            or any(s < 0 or s > 2**32-1 for s in seeds)):
        parser.error("one to five distinct uint32 seeds required")
    if args.output.exists():
        raise FileExistsError("refusing to replace an immutable result")
    start, components = time.monotonic(), {}
    for key in methods:
        rows = [FUNCTIONS[key](seed) for seed in seeds]
        metrics = {}
        for name in rows[0]["metrics"]:
            values = [row["metrics"][name] for row in rows]
            metrics[name] = {"mean": statistics.mean(values),
                             "std": statistics.stdev(values) if len(values)>1 else 0., "n": len(values)}
        components[key] = {"dataset": {"id": f"synthetic-{key}-contract-fixture",
            "revision": fingerprint([r["fixture_sha256"] for r in rows]),
            "public_benchmark_evaluated": False, "initialization": "NumPy default_rng(seed), explicit inert fixture"},
            "per_seed": rows, "metrics": metrics,
            "isolation": {"test_in_fit_or_acceptance": False, "gold_to_agent_callbacks": False,
                          "new_language_model_evaluated": False, "formal_comparison": False},
            "full_experiment_status": "not_reproduced_high_cost", "review_status": "DONE"}
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    dirty = bool(subprocess.check_output(["git", "status", "--porcelain", "--", *SOURCE_PATHS],
                                         cwd=ROOT, text=True).strip())
    result = {"schema_version": 2, "code_commit": commit, "executed_source_uncommitted": dirty,
        "device": "cpu", "diagnostic_only": True, "promotion_eligible": False,
        "evolve_integrated": False, "seeds": seeds, "components": components,
        "executed_source_sha256": {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCE_PATHS},
        "elapsed_seconds": time.monotonic()-start,
        "evaluation_protocol": {"tier": "l1_mechanism", "formal_comparison": False,
            "claim_policy": "independent CPU component/contract fixtures, not Agent capability or full-paper reproduction"},
        "command": "PYTHONPATH=src python scripts/run_oct17_supplement_agent.py "
                   f"--methods {args.methods} --seeds {args.seeds} --device cpu --output <fresh-result.json>"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"methods": methods, "seeds": seeds, "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
