"""CPU mechanism fixtures for ProPerAgent, HDA and DRAGO; no Agent capability claim."""
from __future__ import annotations

import argparse
from dataclasses import asdict, fields, replace
import hashlib
import json
import math
from pathlib import Path
import random
import re
import statistics
import subprocess
import time

from auto_research.agent_research import drago, harness_decomposition as hda, proper_agent as proper

ROOT = Path(__file__).resolve().parents[1]
MODULES = {"proper-agent": "proper_agent", "harness-decomposition": "harness_decomposition", "drago": "drago"}
SOURCE_PATHS = ("scripts/run_oct19_evening_agent_components.py", *(
    f"src/auto_research/agent_research/{name}.py" for name in MODULES.values()))


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def row(seed, fixture, metrics, records):
    if any(type(v) not in (float, int, bool) or not math.isfinite(v) for v in metrics.values()):
        raise ValueError("finite scalar protocol measurements required")
    return {"seed": seed, "fixture_sha256": fingerprint(fixture), "metrics": metrics,
            "protocol_records": records,
            "seed_role": "randomized synthetic CPU mechanisms; not model/official benchmark evaluation"}


def proper_diagnostic(seed):
    rng = random.Random(seed)
    results, baseline_results, silent_results, traces, fixture = [], [], [], [], []
    future_leaks, bad_gate_rejections, unknown, gold_exposures = 0, 0, 0, 0
    for index in range(rng.randrange(10, 16)):
        item, latent, future = f"item-{index}", f"intent-{index}", f"future-{index}"
        names = [item, latent, "user", future, "door", "closed"]
        vectors = {n: tuple(float(i == j) for i in range(len(names))) for j, n in enumerate(names)}
        quantity = rng.randrange(1, 20)
        facts = [proper.MemoryFact("need", item, "needs", latent, -2, "event-past",
                    f"Restock {quantity} {item}", open_loop=True),
                 proper.MemoryFact("standing", "door", "state", "closed", -1, "rule", "Keep door closed", "semantic"),
                 proper.MemoryFact("future", item, "observed", future, 100, "future-event", "Hidden future event")]
        graph = proper.MemoryGraph(facts, embed=vectors.__getitem__)
        observations = tuple(proper.Observation(float(t), "store aisle" if t in (2, 4) else "home",
                                                (item,)) for t in (0, 2, 4, 6, 8))
        def gate(observation, candidates):
            nonlocal future_leaks
            future_leaks += sum(f.timestamp > observation.timestamp for f in candidates)
            selected = [f for f in candidates if f.open_loop and f.subject in observation.entities]
            if observation.description == "store aisle" and selected:
                return proper.GateEvidence(tuple(f.key for f in selected), " | ".join(f.passage for f in selected))
            return None
        def actor(view):
            nonlocal gold_exposures
            gold_exposures += len({f.name for f in fields(view)} & {"gold", "reference", "window", "answer"})
            if view.evidence is not None and not view.already_spoken:
                return view.evidence.text
            return None
        interventions = proper.run_stream(graph, observations, gate=gate, actor=actor)
        private = {"window": (2., 4.), "content": f"Restock {quantity} {item}"}
        result = proper.score_clip(interventions, window=private["window"],
                                  judge=lambda intervention: intervention.text == private["content"])
        baseline = tuple(proper.Intervention(o.timestamp, private["content"]) for o in observations)
        # Explicit oracle baseline is only an evaluator-side negative control,
        # never passed to the measured actor or gate.
        baseline_results.append(proper.score_clip(baseline, window=private["window"], judge=lambda _: True))
        results.append(result)
        silent = proper.run_stream(graph, observations,
            gate=lambda _observation, _candidates: None, actor=actor)
        silent_results.append(proper.score_clip(silent, window=None, judge=lambda _: False))
        missing = proper.score_clip(interventions, window=private["window"], judge=lambda _: None)
        unknown += int(missing["perfect"] is None and not missing["scored"])
        try:
            proper.run_stream(graph, observations[:1], gate=lambda _o, _c: proper.GateEvidence(("future",), "bad"),
                              actor=actor)
        except ValueError:
            bad_gate_rejections += 1
        fixture.append([asdict(f) for f in facts])
        traces.append({"interventions": [asdict(i) for i in interventions], "score": result,
                       "oracle_always_speak_negative_control": baseline_results[-1], "unscored": missing})
    n = len(results)
    metrics = {"fixture_clips": n, "timing_content_protocol_perfect_rate": sum(r["perfect"] for r in results)/n,
        "oracle_always_speak_negative_control_perfect_rate": sum(r["perfect"] for r in baseline_results)/n,
        "oracle_always_speak_negative_control_overtrigger_rate": sum(r["over_trigger"] for r in baseline_results)/n,
        "silent_clip_false_trigger_rate": sum(r["silent_clip_false_trigger"] for r in silent_results)/n,
        "retained_unscored_clips": unknown, "rejected_nonretrieved_provenance": bad_gate_rejections,
        "future_memory_exposures": future_leaks, "gold_fields_in_actor_view": gold_exposures}
    return row(seed, fixture, metrics, traces)


def hda_diagnostic(seed):
    rng = random.Random(seed)
    n = rng.randrange(32, 55)
    ids = tuple(f"paired-{i}" for i in range(n))
    base = tuple(rng.uniform(0, .4) for _ in ids)
    scaled = tuple(v+rng.uniform(.03, .12) for v in base)
    neutral = tuple(v+rng.uniform(.02, .1) for v in scaled)
    evolved = tuple(v+rng.uniform(.06, .2) for v in neutral)
    arms = [hda.Arm(ids, values, cost, fingerprint([name, values])) for name, values, cost in (
        ("base", base, 1.), ("evolved", evolved, 3.), ("scaled", scaled, 3.), ("neutral", neutral, 3.))]
    approved = hda.ReviewedControl("fixture-reviewer", "synthetic controls checked by construction", True)
    result = hda.attribute(*arms, compute_review=approved, neutralization_review=approved, seed=seed)
    no_gain = hda.attribute(arms[0], arms[0], arms[0], arms[0], compute_review=approved,
                           neutralization_review=approved, seed=seed)
    rejected = 0
    for mutation in ("identity", "budget", "unreviewed"):
        changed, review = list(arms), approved
        if mutation == "identity":
            changed[2] = replace(changed[2], item_ids=tuple(reversed(ids)))
        elif mutation == "budget":
            changed[2] = replace(changed[2], mean_inference_cost=1.)
        else:
            review = replace(approved, approved=False)
        try:
            hda.attribute(*changed, compute_review=review, neutralization_review=approved, seed=seed)
        except ValueError:
            rejected += 1
    metrics = {k: v for k, v in result.items() if type(v) in (int, float, bool)}
    metrics.update({"rejected_invalid_controls": rejected, "noise_control_attributed": int(no_gain["attributed"]),
        "gain_only_negative_control_overstatement": result["observed_gain"]-result["residual_upper_bound"]})
    return row(seed, [asdict(a) for a in arms], metrics, [result, no_gain])


def drago_diagnostic(seed):
    rng = random.Random(seed)
    records, fixture = [], []
    accepted, rollback, budget_unknown, unreachable, joint_proofs, gold_exposures = 0, 0, 0, 0, 0, 0
    for _ in range(rng.randrange(9, 14)):
        rooms = rng.randrange(3, 7)
        objects = tuple((f"r{i}", "room") for i in range(rooms))
        actions = tuple(drago.Action(f"move-{i}", frozenset({("at", f"r{i}")}),
            frozenset({("at", f"r{i+1}")}), frozenset({("at", f"r{i}")})) for i in range(rooms-1))
        domain = drago.Domain("corridor", (("at", 1), ("ready", 0)), actions)
        goal = frozenset({("at", f"r{rooms-1}")})
        before = drago.Problem("corridor", objects, frozenset(), goal)
        candidate = replace(before, initial=frozenset({("at", "r0")}))
        # The proposal uses the public statement's initial state, not final gold.
        def proposer(public, _diagnosis):
            nonlocal gold_exposures
            gold_exposures += len({f.name for f in fields(public)} & {"gold", "reference", "answer"})
            return candidate
        repaired, trace = drago.repair_loop(domain, before, proposer=proposer)
        accepted += int(repaired == candidate and trace[0]["accepted"])
        diag = drago.diagnose(domain, before)
        unreachable += sum(f.axis == "reachability" for f in diag.findings)
        weakened = replace(before, goals=frozenset())
        rejected, why = drago.accept_repair(domain, before, weakened)
        rollback += int(not rejected and why == "goal_weakening")
        unknown = drago.diagnose(domain, candidate, search_budget=1)
        budget_unknown += int(unknown.search_status == "budget_exhausted"
                              and not any(f.axis == "joint_unsolvable" for f in unknown.findings))
        # Individually reachable goals can still be jointly impossible with deletes.
        joint = replace(candidate, goals=frozenset({("at", "r0"), ("at", f"r{rooms-1}")}))
        jd = drago.diagnose(domain, joint)
        joint_proofs += int(any(f.axis == "joint_unsolvable" for f in jd.findings)
                            and not any(f.axis == "reachability" for f in jd.findings))
        fixture.append({"rooms": rooms, "actions": len(actions)})
        records.append({"repair": trace, "before": asdict(diag), "budget_limited": asdict(unknown),
                        "joint_goals": asdict(jd), "weakening_reason": why})
    metrics = {"fixture_tasks": len(fixture), "accepted_evidence_backed_repairs": accepted,
        "blocked_goal_weakening_repairs": rollback, "delete_relaxation_unreachable_findings": unreachable,
        "joint_unsolvability_proofs": joint_proofs, "budget_exhaustion_retained_as_unknown": budget_unknown,
        "accept_any_negative_control_weakening_admissions": len(fixture), "gold_inputs_to_proposer": gold_exposures}
    return row(seed, fixture, metrics, records)


FUNCTIONS = {"proper-agent": proper_diagnostic, "harness-decomposition": hda_diagnostic, "drago": drago_diagnostic}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--methods", default=",".join(FUNCTIONS))
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--device", choices=("cpu",), default="cpu")
    parser.add_argument("--code-commit")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    methods = args.methods.split(",")
    try:
        seeds = [int(value) for value in args.seeds.split(",")]
    except ValueError:
        parser.error("integer seeds required")
    if not methods or len(set(methods)) != len(methods) or set(methods)-set(FUNCTIONS):
        parser.error("distinct known methods required")
    if not 1 <= len(seeds) <= 5 or len(set(seeds)) != len(seeds) or any(s < 0 or s >= 2**32 for s in seeds):
        parser.error("one to five distinct uint32 seeds required")
    if args.output.exists():
        raise FileExistsError("refusing to replace immutable result")
    commit = args.code_commit or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        parser.error("full code commit required")
    started, components = time.monotonic(), {}
    for method in methods:
        rows = [FUNCTIONS[method](seed) for seed in seeds]
        metrics = {}
        for key in rows[0]["metrics"]:
            values = [r["metrics"][key] for r in rows]
            metrics[key] = all(values) if all(type(v) is bool for v in values) else {
                "mean": statistics.mean(values), "std": statistics.stdev(values) if len(values) > 1 else 0., "n": len(values)}
        components[method] = {"dataset": {"id": f"synthetic-{method}-contract-fixture",
            "revision": fingerprint([r["fixture_sha256"] for r in rows]), "public_benchmark_evaluated": False,
            "initialization": "Python random.Random(seed); inert graph, paired-control and grounded STRIPS fixtures"},
            "per_seed": rows, "metrics": metrics, "review_status": "DONE", "diagnostic_only": True,
            "promotion_eligible": False, "evolve_integrated": False,
            "full_experiment_status": "not_reproduced_high_cost",
            "isolation": {"gold_to_agent_callbacks": False, "test_in_fit_or_acceptance": False,
                          "new_language_model_evaluated": False, "formal_comparison": False}}
    dirty = bool(subprocess.check_output(["git", "status", "--porcelain", "--", *SOURCE_PATHS],
                                         cwd=ROOT, text=True).strip())
    result = {"schema_version": 2, "code_commit": commit, "executed_source_uncommitted": dirty,
        "device": "cpu", "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
        "seeds": seeds, "components": components,
        "executed_source_sha256": {path: hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
                                   for path in SOURCE_PATHS}, "elapsed_seconds": time.monotonic()-started,
        "evaluation_protocol": {"tier": "l1_mechanism", "seeds": seeds, "formal_comparison": False,
            "claim_policy": "CPU mechanisms only; not official benchmarks, Agent capability or full-paper reproduction"},
        "command": "PYTHONPATH=src python scripts/run_oct19_evening_agent_components.py "
            f"--methods {args.methods} --seeds {args.seeds} --device cpu --code-commit {commit} --output <fresh-result.json>"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"methods": methods, "seeds": seeds, "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
