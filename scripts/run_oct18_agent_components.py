"""Seeded CPU contracts for six Oct-18 reviewed components; never Agent capability.

No network, GPU, language model, official benchmark or production data is used.
Every score below describes a randomized inert protocol fixture only.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import json
import math
from pathlib import Path
import random
import re
import statistics
import subprocess
import time

from auto_research.agent_research import aria_repair as aria
from auto_research.agent_research import coda, diviner, jev_agent_harness as jev, memscope, torsi

ROOT = Path(__file__).resolve().parents[1]
MODULES = {"diviner": "diviner", "torsi": "torsi", "aria": "aria_repair", "coda": "coda",
           "memscope": "memscope", "jev-agent-harness": "jev_agent_harness"}
SOURCE_PATHS = ("scripts/run_oct18_agent_components.py", *(
    f"src/auto_research/agent_research/{name}.py" for name in MODULES.values()))


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def row(seed, fixture, metrics):
    assert all(type(v) in (int, float, bool) and math.isfinite(v) for v in metrics.values())
    return {"seed": seed, "fixture_sha256": fingerprint(fixture), "metrics": metrics,
            "seed_role": "randomized inert public contract fixture; no model training or capability evaluation"}


def diviner_diagnostic(seed):
    rng = random.Random(seed)
    ledger = diviner.EvidenceLedger(diviner.InvestigationScope("incident", "ranking", 10., 20., 22.))
    fixture, expected, naive_false = [], 0, 0
    statuses = ["data", "valid_empty", "timeout", "partial", "denied"]
    for i in range(24):
        status = rng.choice(statuses)
        available = rng.uniform(20., 25.)
        item = diviner.Evidence(f"e-{i}", "incident", "ranking", 10., 20., available,
                                 status, "seeded-public-event-fixture", {"value": rng.randrange(1000)})
        admitted = ledger.admit(item)
        independent = status in {"data", "valid_empty"} and available <= 22.
        assert admitted == independent
        expected += independent
        naive_false += bool(item.payload) and not independent
        fixture.append([status, available, item.payload["value"]])
    valid = diviner.Evidence("supported", "incident", "ranking", 10., 20., 21., "data", "fixture")
    ledger.admit(valid)
    ledger.update_hypothesis("candidate-cause", "supported", ["supported"])
    update = diviner.KnowledgeUpdate("skill", "owner", 1, 2, True, "agent")
    blocked = 0
    try:
        diviner.publish_update(update)
    except ValueError:
        blocked += 1
    assert diviner.publish_update(replace(update, approved_by="owner")) == 2
    return row(seed, fixture, {"observations": len(fixture), "admitted_observations": expected,
        "rejected_observations": len(ledger.rejected), "independent_admission_count_error": abs(
            len(ledger.observations)-1-expected), "nonempty_is_evidence_negative_control_false_admissions": naive_false,
        "blocked_agent_self_approvals": blocked, "published_owner_approved_updates": 1})


def torsi_diagnostic(seed):
    rng = random.Random(seed)
    timings, latencies, ages = [], [], []
    for i in range(16):
        latency, scheduling = rng.uniform(.01, 2.), rng.uniform(.01, .5)
        timing = torsi.ActionTiming(float(i)*3, i*3+latency, i*3+latency+scheduling)
        measured = timing.measurements()
        timings.append([latency, scheduling])
        latencies.append(measured["response_latency"])
        ages.append(measured["action_age"])
    scores = {f"validation-{i}": rng.uniform(0, 10) for i in range(12)}
    gain = rng.uniform(.01, .3)
    improved = {i: x+gain for i, x in scores.items()}
    accepted = torsi.select_guidance("old", "candidate", scores, improved, test_task_ids=["test-only"])
    tie = torsi.select_guidance("old", "tie", scores, dict(scores))
    regression = torsi.select_guidance("old", "worse", scores, {i: x-gain for i, x in scores.items()})
    private_exposures = []
    trace = torsi.FeedbackTrace("feedback-only", ({"public": rng.randrange(10000)},),
                                ("left",), (torsi.ActionTiming(0, .1, .2),))
    def teacher(current, traces):
        private_exposures.extend(t.task_id for t in traces if t.task_id != "feedback-only")
        return current + " revised from feedback"
    torsi.propose_guidance("old", [trace], teacher)
    assert accepted.accepted and not tie.accepted and not regression.accepted and not private_exposures
    return row(seed, [timings, scores, gain, trace.observations], {
        "mean_response_latency": statistics.mean(latencies), "mean_action_age": statistics.mean(ages),
        "latency_only_negative_control_underestimate": statistics.mean(ages)-statistics.mean(latencies),
        "paired_validation_gain": accepted.paired_validation_gain,
        "independent_validation_gain_error": abs(accepted.paired_validation_gain-gain),
        "accepted_improvements": int(accepted.accepted), "rejected_ties_and_regressions": 2,
        "validation_or_test_tasks_to_teacher": len(private_exposures)})


def aria_diagnostic(seed):
    rng = random.Random(seed)
    n = rng.randrange(8, 20)
    cut = rng.randrange(1, n-2)
    content = [f"public-observation-{rng.randrange(100000)}" for _ in range(n)]
    events = tuple(aria.Event(f"e-{i}", "assistant", "message", text) for i, text in enumerate(content))
    replacement = (aria.Event("new-step", "assistant", "tool_call", f"inspect-current-{rng.randrange(10000)}"),)
    patch = aria.RepairPatch("observable branch needs correction", f"e-{cut}", replacement)
    repaired = aria.apply_repair(events, patch, first_bad_event_id=f"e-{cut+1}")
    assert repaired == events[:cut+1] + replacement
    invalid = [replace(patch, cut_event_id="missing"),
               replace(patch, replacement=(aria.Event("forged", "tool", "tool_result", "private invented value"),)),
               replace(patch, replacement=(replace(replacement[0], event_id="e-0"),))]
    rejected = 0
    for bad in invalid:
        try:
            aria.apply_repair(events, bad)
        except ValueError:
            rejected += 1
    controls = [(bool(rng.randrange(2)), bool(rng.randrange(2))) for _ in range(20)]
    verified = sum(aria.verified_repair(fresh_control_passed=a, patched_execution_passed=b) for a, b in controls)
    assert verified == sum(not a and b for a, b in controls)
    return row(seed, [content, cut, controls], {"source_events": n, "retained_prefix_events": cut+1,
        "discarded_suffix_events": n-cut-1, "replacement_events": len(replacement),
        "invalid_patches_rejected": rejected, "independent_prefix_construction_error": int(
            repaired != events[:cut+1]+replacement), "verified_paired_fixture_repairs": verified,
        "patch_pass_only_negative_control_false_positives": sum(a and b for a, b in controls)})


def coda_diagnostic(seed):
    rng = random.Random(seed)
    ids = [f"task-{i}" for i in range(32)]
    base = {i: rng.random() > .3 for i in ids}
    outcomes = {"delivered": base, "repeat": {i: (not base[i] if rng.random()<.05 else base[i]) for i in ids},
        "reword": {i: (not base[i] if rng.random()<.25 else base[i]) for i in ids},
        "incomplete": {i: base[i] and rng.random() > .3 for i in ids},
        "misleading": {i: base[i] and rng.random() > .4 for i in ids},
        "no_skill": {i: rng.random() > .5 for i in ids}}
    result = coda.audit(outcomes)
    reference = sum(outcomes["no_skill"][i] and outcomes["incomplete"][i] for i in ids)/len(ids)
    wrong_conditional = (sum(outcomes["no_skill"][i] and outcomes["incomplete"][i] for i in ids)
                         / max(1, sum(outcomes["no_skill"].values())))
    skill = coda.Skill("one", {"trigger": f"word-{rng.randrange(10000)}"}, {"steps": "check then report"})
    changed = coda.rewrite_selected([skill], ["one"], {"one": {"steps": "report without checking"}})[0]
    assert changed.retrieval_fields == skill.retrieval_fields
    assert reference == result["resistance_incomplete"]
    return row(seed, [outcomes, dict(skill.retrieval_fields)], {**result,
        "independent_full_denominator_resistance_error": abs(reference-result["resistance_incomplete"]),
        "conditional_denominator_negative_control_difference": abs(reference-wrong_conditional),
        "retrieval_field_mutations": int(changed.retrieval_fields != skill.retrieval_fields)})


def memscope_diagnostic(seed):
    rng = random.Random(seed)
    threshold = rng.uniform(.5, .75)
    old, new = f"{threshold:.5f}", f"{threshold+.05:.5f}"
    code = f"def retrieve(memory, query):\n    threshold = {old}\n    return memory.get(query) if threshold < 1 else None\n"
    provider = memscope.Provider("same-provider", "schema-v1", code)
    memory = {f"item-{i}": rng.randrange(100000) for i in range(rng.randrange(4, 12))}
    probes = []
    def probe(candidate, bank):
        probes.append(candidate.provider_id)
        bank["probe-private-mutation"] = 1
        return new in candidate.code
    accepted = memscope.patch_provider(provider, memory, old=old, new=new, probe=probe)
    failed = memscope.patch_provider(provider, memory, old=old, new=new, probe=lambda *a: False)
    changed_interface = memscope.patch_provider(provider, memory, old="retrieve(memory, query)",
                                               new="retrieve(memory)", probe=probe)
    assert accepted.accepted and not failed.accepted and not changed_interface.accepted
    assert accepted.memory == failed.memory == memory and failed.provider == provider
    return row(seed, [code, memory, new], {"memory_records": len(memory), "accepted_local_patches": 1,
        "change_ratio": accepted.change_ratio, "failed_probe_rollbacks": int(not failed.accepted),
        "rejected_interface_changes": int(not changed_interface.accepted),
        "persisted_probe_side_effects": int("probe-private-mutation" in accepted.memory),
        "independent_original_code_rollback_error": int(failed.provider.code != code),
        "unchecked_install_negative_control_incompatible_edits": 1})


def jev_diagnostic(seed):
    rng = random.Random(seed)
    low, high = rng.uniform(.52, .65), rng.uniform(.85, .95)
    rows = [jev.ShadowDecision(f"cal-{i}", "tool", low if i < 20 else high,
                               i >= 20, True, .05) for i in range(40)]
    calibration = jev.calibrate(rows, min_bin=20, excluded_task_ids=[f"test-{i}" for i in range(12)])
    assert calibration.thresholds["tool"] == high
    costs, delegated, strong, exposed, fixture, naive_wrong = [], 0, 0, [], [], 0
    for i in range(12):
        confidence = low if i % 2 else high
        request = jev.PublicDecision(f"test-{i}", "tool", f"public context {rng.randrange(10000)}", ("a", "b"))
        def model(view):
            exposed.extend(k for k in view.__dataclass_fields__ if k in {"gold", "correct", "answer"})
            return (confidence, 1-confidence)
        result = jev.route(request, calibration, decision_model=model, strong_model=lambda view: 1,
                           decision_cost=.01, strong_cost=.2)
        naive = jev.route(request, replace(calibration, thresholds={"tool": .5}),
                          decision_model=model, strong_model=lambda view: 1)
        naive_wrong += i % 2 == 1 and naive.source == "decision_model"
        costs.append(result.total_cost)
        delegated += result.source == "decision_model"
        strong += result.source == "strong_model"
        fixture.append([request.context, confidence, result.action_index, result.source])
    fault = jev.route(jev.PublicDecision("fault", "tool", "public", ("a", "b")), calibration,
                      decision_model=lambda view: (math.nan, .1), strong_model=lambda view: 1,
                      decision_cost=.01, strong_cost=.2)
    reference_cost = delegated*.01 + strong*.21
    assert math.isclose(sum(costs), reference_cost) and not exposed
    return row(seed, [low, high, fixture], {"fitted_tool_threshold": high,
        "shadow_rows": len(rows), "delegated_decisions": delegated, "strong_fallbacks": strong,
        "declared_total_cost": sum(costs), "independent_cost_accounting_error": abs(sum(costs)-reference_cost),
        "fixed_low_threshold_negative_control_wrong_delegations": naive_wrong,
        "failed_model_fallbacks": int(fault.fallback_reason == "decision_model_failure"),
        "gold_fields_exposed_to_runtime_callbacks": len(exposed)})


FUNCTIONS = {"diviner": diviner_diagnostic, "torsi": torsi_diagnostic, "aria": aria_diagnostic,
             "coda": coda_diagnostic, "memscope": memscope_diagnostic, "jev-agent-harness": jev_diagnostic}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--methods", default=",".join(FUNCTIONS))
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--device", choices=("cpu",), default="cpu")
    parser.add_argument("--code-commit")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    methods = args.methods.split(",")
    try:
        seeds = [int(x) for x in args.seeds.split(",")]
    except ValueError:
        parser.error("integer seeds required")
    if not methods or len(set(methods)) != len(methods) or set(methods)-set(FUNCTIONS):
        parser.error("distinct known methods required")
    if not 1 <= len(seeds) <= 5 or len(set(seeds)) != len(seeds) or any(x < 0 or x >= 2**32 for x in seeds):
        parser.error("one to five distinct uint32 seeds required")
    if args.output.exists():
        raise FileExistsError("refusing to replace an immutable result")
    commit = args.code_commit or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        parser.error("full 40-character code commit required")
    start, components = time.monotonic(), {}
    for key in methods:
        rows = [FUNCTIONS[key](seed) for seed in seeds]
        metrics = {}
        for field in rows[0]["metrics"]:
            values = [r["metrics"][field] for r in rows]
            metrics[field] = {"mean": statistics.mean(values),
                "std": statistics.stdev(values) if len(values)>1 else 0., "n": len(values)}
        components[key] = {"dataset": {"id": f"synthetic-{key}-contract-fixture",
            "revision": fingerprint([r["fixture_sha256"] for r in rows]), "public_benchmark_evaluated": False,
            "initialization": "Python random.Random(seed); inert public CPU events/numbers"},
            "per_seed": rows, "metrics": metrics, "review_status": "DONE",
            "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
            "full_experiment_status": "not_reproduced_high_cost",
            "isolation": {"gold_to_agent_callbacks": False, "test_in_fit_or_acceptance": False,
                          "new_language_model_evaluated": False, "formal_comparison": False}}
    dirty = bool(subprocess.check_output(["git", "status", "--porcelain", "--", *SOURCE_PATHS],
                                        cwd=ROOT, text=True).strip())
    result = {"schema_version": 2, "code_commit": commit, "executed_source_uncommitted": dirty,
        "device": "cpu", "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
        "seeds": seeds, "components": components,
        "executed_source_sha256": {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCE_PATHS},
        "elapsed_seconds": time.monotonic()-start,
        "evaluation_protocol": {"tier": "l1_mechanism", "seeds": seeds, "formal_comparison": False,
            "claim_policy": "CPU protocol fixtures only; no Agent capability, training, production or full-paper reproduction"},
        "command": "PYTHONPATH=src python scripts/run_oct18_agent_components.py "
            f"--methods {args.methods} --seeds {args.seeds} --device cpu --code-commit {commit} --output <fresh-result.json>"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"methods": methods, "seeds": seeds, "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
