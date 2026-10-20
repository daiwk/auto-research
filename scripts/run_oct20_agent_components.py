"""CPU diagnostics for MemPrice, SCOPE replay and TokenWorth; no Agent capability."""
from __future__ import annotations

import argparse
from dataclasses import asdict, fields, replace
import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import re
import statistics
import subprocess
import time

import numpy as np

from auto_research.agent_research import memprice as mp, scope_replay as scope, tokenworth as tw

ROOT = Path(__file__).resolve().parents[1]
MODULES = {"memprice": "memprice", "scope-replay": "scope_replay", "tokenworth": "tokenworth"}
SOURCE_PATHS = ("scripts/run_oct20_agent_components.py", *(
    f"src/auto_research/agent_research/{name}.py" for name in MODULES.values()))


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def row(seed, fixture, metrics, records):
    if any(type(v) not in (float, int, bool) or not math.isfinite(v) for v in metrics.values()):
        raise ValueError("finite scalar protocol measurements required")
    return {"seed": seed, "fixture_sha256": fingerprint(fixture), "metrics": metrics,
            "protocol_records": records,
            "seed_role": "randomized synthetic CPU mechanisms; not an Agent/official benchmark comparison"}


def memprice_diagnostic(seed):
    rng = random.Random(seed)
    errors, violations, records, fixture = [], 0, [], []
    for trial in range(rng.randrange(12, 18)):
        items = []
        for i in range(rng.randrange(2, 5)):
            values = sorted([rng.uniform(.01, 1.) for _ in range(4)], reverse=True)+[0.]
            sizes = sorted([rng.randrange(1, 12) for _ in range(4)], reverse=True)+[0]
            items.append(mp.Item(str(i), tuple(mp.Representation(j, sizes[j], values[j]) for j in range(5))))
        budget, price = rng.randrange(3, 20), rng.uniform(0., 2.)
        selected, size, value = mp.allocate(tuple(items), capacity=budget, price=price)
        reference = max(sum(o.utility-price*o.tokens/budget for o in options)
            for options in itertools.product(*(i.options for i in items))
            if sum(o.tokens for o in options) <= budget)
        errors.append(abs(value-reference))
        violations += size > budget
        fixture.append({"items": [asdict(item) for item in items], "budget": budget, "price": price})
        records.append({"trial": trial, "selection": [(key, o.level) for key, o in selected],
                        "objective": value, "reference": reference, "tokens": size})
    budget = rng.randrange(8, 16)*2
    adversarial = tuple(mp.Item(key, (mp.Representation(0, size, utility), mp.Representation(4, 0, 0.)))
        for key, size, utility in (("largest", budget//2+1, .9), ("pair-a", budget//2, .7),
                                  ("pair-b", budget//2, .7)))
    _path, _size, exact = mp.allocate(adversarial, capacity=budget, price=0.)
    remaining, greedy = budget, 0.
    for item in sorted(adversarial, key=lambda i: -i.options[0].utility):
        option = item.options[0]
        if option.tokens <= remaining:
            remaining -= option.tokens
            greedy += option.utility
    allocator = mp.MemPrice(budget, target=.2, c=100.)
    single = mp.Item("resident", (mp.Representation(0, budget, 1.), mp.Representation(4, 0, 0.)))
    first, second = allocator.step((single,)), allocator.step((single,))
    before = (allocator.queue, allocator.round)
    allocator.refresh()
    persisted = before == (allocator.queue, allocator.round)
    rejected = 0
    for data in ((single, single), (replace(single, options=(mp.Representation(0, -1, 1.),)),)):
        try:
            mp.allocate(data, capacity=budget, price=0.)
        except ValueError:
            rejected += 1
    metrics = {"fixture_allocations": len(errors), "maximum_objective_reference_error": max(errors),
        "hard_budget_violations": int(violations), "greedy_negative_control_gap": exact-greedy,
        "pressure_induced_token_reduction": first.tokens-second.tokens,
        "persistent_queue_and_clock_after_refresh": persisted,
        "rejected_invalid_allocations": rejected,
        "forbidden_query_or_gold_allocator_parameters": len({"gold", "answer", "query"} & set(
            __import__("inspect").signature(mp.allocate).parameters))}
    records.append({"first": asdict(first), "second": asdict(second), "refresh_state": before,
                    "greedy_negative_control": greedy, "exact": exact})
    return row(seed, fixture, metrics, records)


def scope_diagnostic(seed):
    rng = random.Random(seed)
    certified, false_certificates, fault_trials, broken_failures, unavailables = 0, 0, 0, 0, 0
    records, fixture = [], []
    for trial in range(rng.randrange(9, 15)):
        initial, increment = rng.randrange(1, 40), rng.randrange(1, 20)
        def api(name, state, *args):
            if name == "append":
                args[0].append(args[1])
                return args[0]
            if name == "read":
                return tuple(args[0])
            if name == "checked_error":
                state["error_seen"] = True
                raise ValueError("expected public API error")
            raise KeyError(name)
        def program(call, state):
            assert state["a"] is state["b"]
            returned = call("append", state["a"], state["increment"])
            assert returned is state["b"]
            assert len(state["b"]) == 2
            assert call("read", state["b"])[-1] == state["increment"]
            try:
                call("checked_error")
            except ValueError:
                assert state["error_seen"]
            call("read", state["a"])
        shared = [initial]
        witness = scope.record(program, source=f"trusted-callback-{trial}", instance=f"development-{trial}",
            state={"a": shared, "b": shared, "increment": increment}, api=api,
            native_grader=lambda state: state["a"] == [initial, increment] and state["error_seen"])
        result = scope.certify(program, witness, candidate_source="same-behavior-revision", instance=witness.instance)
        certified += result.status == "certified"
        fault_records = []
        for fault in ("wrong_argument", "break_alias", "extra", "short", "final_state"):
            def changed(call, state):
                if fault == "wrong_argument":
                    return call("append", state["a"], increment+1)
                if fault == "break_alias":
                    state["b"] = list(state["a"])
                if fault == "short":
                    return
                program(call, state)
                if fault == "final_state":
                    state["a"].clear()
                else:
                    call("read", state["a"])
            bad = scope.certify(changed, witness, candidate_source=fault, instance=witness.instance)
            false_certificates += bad.status == "certified"
            fault_trials += 1
            fault_records.append(asdict(bad))
        def unsupported(call, state):
            call("read", np.array([initial]))
        unavailable = scope.certify(unsupported, witness, candidate_source="unsupported-array", instance=witness.instance)
        unavailables += unavailable.status == "unavailable"
        # Return-only negative control omits mutations/alias restoration. It
        # cannot even execute the second state-dependent call correctly.
        broken_state = {"a": [initial], "b": None, "increment": increment}
        broken_state["b"] = broken_state["a"]
        def broken(_name, *_args):
            return [initial, increment]
        try:
            program(broken, broken_state)
        except (AssertionError, TypeError, ValueError):
            broken_failures += 1
        accepted = scope.AcceptedPrograms("initial")
        accepted.observe(f"trusted-callback-{trial}", success=True, witness=witness)
        fixture.append({"initial": initial, "increment": increment})
        records.append({"certificate": asdict(result), "faults": fault_records,
            "unsupported": asdict(unavailable), "tape_sha256": scope.tape_hash(witness),
            "accepted_by_environment_not_replay": accepted.accepted_source})
    metrics = {"fixture_witnesses": len(fixture), "full_stateful_certificates": certified,
        "fault_injections": fault_trials, "false_certificates_under_faults": false_certificates,
        "broken_replay_negative_control_failures": broken_failures,
        "unsupported_graphs_retained_unavailable": unavailables,
        "instance_transfer_certificates": 0}
    # Actually exercise the instance guard, rather than assign a success metric.
    try:
        scope.certify(program, witness, candidate_source="revision", instance="different-instance")
    except ValueError:
        metrics["instance_mismatch_rejected"] = True
    else:
        metrics["instance_mismatch_rejected"] = False
        metrics["instance_transfer_certificates"] += 1
    return row(seed, fixture, metrics, records)


def tokenworth_diagnostic(seed):
    rng = np.random.default_rng(seed)
    n, dimensions = int(rng.integers(8, 14)), 7
    x, y = rng.normal(size=(n, dimensions)), rng.uniform(-1., 1., n)
    rfm = tw.ResidualRFM(dimensions)
    rfm.metric = rng.uniform(.5, 1.5, dimensions)
    rfm.fit(x, y)
    gram = np.array([[math.exp(-math.sqrt(sum(float(rfm.metric[k])*(float(a[k])-float(b[k]))**2
        for k in range(dimensions)))) for b in x] for a in x])
    reference_alpha = np.linalg.solve(gram+.01*np.eye(n), y)
    kernel_error = float(np.max(np.abs(rfm.coefficients-reference_alpha)))
    queries = rng.normal(size=(5, dimensions))
    finite = np.zeros_like(queries)
    for k in range(dimensions):
        step = np.zeros_like(queries)
        step[:, k] = 1e-6
        finite[:, k] = (rfm.predict(queries+step)-rfm.predict(queries-step))/(2e-6)
    gradient_error = float(np.max(np.abs(finite-rfm.gradients(queries))))
    before = rfm.metric.copy()
    rfm.adapt(queries, x, y)
    metric_shift = float(np.linalg.norm(rfm.metric-before))
    linear_x = rng.normal(size=(40, 4))
    labels = np.where(linear_x[:, 1] > 0, 1., -1.)
    weights = tw.fit_base(linear_x, labels)
    loss_reduction = tw.logistic_loss(tw.PRIOR, linear_x, labels)-tw.logistic_loss(weights, linear_x, labels)
    # The small stream uses explicit diagnostic intervals, not paper DB defaults.
    controller = tw.TokenWorth(capacity=5, base_interval=10, krr_interval=8, agop_interval=24)
    controller.begin("public cold start")
    controller.finish(True, new_memory=("seed-memory", "previous successful public action"))
    fixtures, records, rejected = [], [], 0
    for t in range(51):
        query = f"public action class {int(rng.integers(0, 8))} step {t}"
        selection = controller.begin(query)
        # Synthetic task result is private until native evaluation has ended;
        # its random coin is neither query input nor a memory-selection oracle.
        reward = bool(rng.random() > .4)
        if t == 0:
            try:
                controller.begin("future task")
            except ValueError:
                rejected += 1
        candidate = (f"successful-{t}", f"public completed action {t}") if reward and t % 7 == 0 else None
        reason = controller.finish(reward, new_memory=candidate)
        fixtures.append({"query": query, "native_completed_reward": reward})
        records.append({"selection": asdict(selection), "admission": reason,
                        "bank_size": len(controller.bank), "feedback_count": controller.feedback})
    old = tw.Memory("old", "same representation", 0)
    new = tw.Memory("new", "different unfamiliar fragment 92831", 1)
    retained, reason = tw.admission_decision((old,), new, ("q",), capacity=1,
        score=lambda _q, m: 1. if m.key == "old" else -1.)
    # Admit-only negative control would retain this low-worth candidate; the
    # real enlarged-bank eviction may evict the just-admitted candidate itself.
    negative_control_bad_admissions = int(new not in retained and reason == "candidate_self_evicted")
    metrics = {"maximum_kernel_reference_error": kernel_error,
        "gradient_finite_difference_error": gradient_error, "agop_metric_shift": metric_shift,
        "base_logistic_loss_reduction": loss_reduction, "fixture_completed_tasks": len(fixtures)+1,
        "selected_pair_feedback": controller.feedback, "fit_updates": controller.rfm.fits,
        "maximum_bank_capacity_violation": max(0, max(r["bank_size"] for r in records)-controller.capacity),
        "chronology_violation_rejections": rejected,
        "admit_only_negative_control_bad_admissions": negative_control_bad_admissions,
        "private_gold_fields_in_actor_selection": len({"gold", "answer", "reward", "reference"} & {
            field.name for field in fields(tw.Selection)}),
        "final_metric_mean_error": abs(float(controller.rfm.metric.mean())-1.),
        "final_weights_change": float(np.linalg.norm(controller.weights-tw.PRIOR))}
    records.append({"standalone_rfm_metric": rfm.metric.tolist(), "weights": controller.weights.tolist(),
        "diagnostic_intervals": {"base": 10, "krr": 8, "agop": 24},
        "self_eviction_reason": reason, "selected_feedback_not_causal_effect": True})
    fixture = {"stream": fixtures, "kernel_x": x.tolist(), "kernel_y": y.tolist(),
               "linear_x": linear_x.tolist(), "labels": labels.tolist()}
    return row(seed, fixture, metrics, records)


FUNCTIONS = {"memprice": memprice_diagnostic, "scope-replay": scope_diagnostic, "tokenworth": tokenworth_diagnostic}


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
    started = time.monotonic()
    hashes = {path: hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in SOURCE_PATHS}
    components = {}
    for method in methods:
        rows = [FUNCTIONS[method](seed) for seed in seeds]
        metrics = {}
        for key in rows[0]["metrics"]:
            values = [r["metrics"][key] for r in rows]
            metrics[key] = all(values) if all(type(v) is bool for v in values) else {
                "mean": statistics.mean(values), "std": statistics.stdev(values) if len(values) > 1 else 0.,
                "n": len(values)}
        components[method] = {"dataset": {"id": f"synthetic:oct20-{method}-v1",
            "revision": "sha256:"+hashes[SOURCE_PATHS[0]], "capability_benchmark": False,
            "initialization": "seeded synthetic integer options, trusted Python tape and numerical online learning fixtures"},
            "per_seed": rows, "metrics": metrics, "review_status": "DONE", "diagnostic_only": True,
            "promotion_eligible": False, "evolve_integrated": False,
            "full_experiment_status": "not_reproduced_high_cost",
            "isolation": {"gold_to_agent_callbacks": False, "test_in_fit_or_acceptance": False,
                          "new_language_model_evaluated": False, "formal_comparison": False}}
    dirty = bool(subprocess.check_output(["git", "status", "--porcelain", "--", *SOURCE_PATHS],
                                         cwd=ROOT, text=True).strip())
    result = {"schema_version": 2, "code_commit": commit, "executed_source_uncommitted": dirty,
        "device": "cpu", "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
        "seeds": seeds, "components": components, "executed_source_sha256": hashes,
        "elapsed_seconds": time.monotonic()-started,
        "evaluation_protocol": {"tier": "l1_mechanism", "seeds": seeds, "formal_comparison": False,
            "claim_policy": "CPU mechanisms only; not official benchmarks, Agent capability or full-paper reproduction"},
        "command": "PYTHONPATH=src python scripts/run_oct20_agent_components.py "
            f"--methods {args.methods} --seeds {args.seeds} --device cpu --code-commit {commit} --output <fresh-result.json>"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"methods": methods, "seeds": seeds, "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
