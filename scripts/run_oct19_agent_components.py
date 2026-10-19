"""CPU-only executable protocol fixtures, not official Agent benchmark results."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
import math
from pathlib import Path
import random
import re
import statistics
import subprocess
import time

from auto_research.agent_research import agent_perturb as perturb, alpha_diana as diana

ROOT = Path(__file__).resolve().parents[1]
MODULES = {"alpha-diana": "alpha_diana", "agent-perturb": "agent_perturb"}
SOURCE_PATHS = ("scripts/run_oct19_agent_components.py", *(
    f"src/auto_research/agent_research/{name}.py" for name in MODULES.values()))


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def row(seed, fixture, metrics, records):
    if any(type(v) not in (float, int, bool) or not math.isfinite(v) for v in metrics.values()):
        raise ValueError("finite scalar protocol measurements required")
    return {"seed": seed, "fixture_sha256": fingerprint(fixture), "metrics": metrics,
            "protocol_records": records,
            "seed_role": "randomized inert CPU protocol fixtures; no model/official benchmark evaluation"}


def alpha_diana_diagnostic(seed):
    rng = random.Random(seed)
    count = rng.randrange(15, 22)
    tasks, references, public_fixture = [], {}, []
    for i in range(count):
        x, y = rng.randrange(10, 99), rng.randrange(10, 99)
        tag = "grader-fault" if i % 7 == 1 else "normal"
        task = diana.PublicTask(f"task-{i}", f"add {x} {y} {tag}")
        tasks.append(task)
        references[task.task_id] = {"answer": str(x+y), "fault": tag == "grader-fault"}
        public_fixture.append(asdict(task))
    first_failure_ids = {task.task_id for task in tasks if rng.random() < .35}
    wrong_ids = {task.task_id for task in tasks if rng.random() < .2}
    calls, exposed = {}, []

    def actor(public, session):
        exposed.extend(key for key in public.__dataclass_fields__
                       if key in {"reference", "ground_truth", "correct", "answer"})
        assert not session.workspace
        assert not session.memory
        session.workspace["scratch"] = public.task_id
        session.memory["note"] = "public work started"
        calls[public.task_id] = calls.get(public.task_id, 0)+1
        if public.task_id in first_failure_ids and calls[public.task_id] == 1:
            raise diana.ExecutionFailure("injected runtime fault", output_tokens=3)
        _, x, y, _ = public.problem.split()
        value = int(x)-int(y) if public.task_id in wrong_ids else int(x)+int(y)
        # These are declared fixture accounting units, not tokenizer/model measurements.
        return diana.AgentOutput(str(value), output_tokens=len(public.problem.split())+len(str(value)))

    def grader(answer, private):
        if private["fault"]:
            raise RuntimeError("injected scorer outage")
        return answer == private["answer"]

    runner = diana.ProtocolRunner(diana.SessionPolicy(max_retries=1))
    for task in tasks:
        runner.run_sample(task, "sample-0", actor=actor, grader=grader,
                          reference=references[task.task_id])
    requested = [(task.task_id, "sample-0") for task in tasks]
    result = diana.summarize(runner.records, requested_samples=requested)
    latest = {record.task_id: record for record in runner.records}
    expected_correct = sum(task.task_id not in wrong_ids and not references[task.task_id]["fault"]
                           for task in tasks)
    assert result["correct_samples"] == expected_correct
    retained_tokens = sum(record.output_tokens or 0 for record in latest.values())
    ignored_unscored_rate = expected_correct / max(1, result["scored_samples"])
    blocked = 0
    for changes in ({"workers": 2}, {"max_retries": 1}):
        try:
            diana.SessionPolicy(memory_scope="cross_task", memory_writable=True, **changes)
        except ValueError:
            blocked += 1
    # Demonstrate why unsafe retry is forbidden: a failed attempt already mutates a bank.
    unsafe_bank = {"counter": 0}
    for _ in range(2):
        unsafe_bank["counter"] += 1
    metrics = {key: value for key, value in result.items() if value is not None}
    metrics.update({"independent_correct_count_error": abs(expected_correct-result["correct_samples"]),
                    "ignored_unscored_negative_control_inflation": ignored_unscored_rate-result[
                        "success_rate_all_requested"],
                    "latest_only_cost_negative_control_undercount": result[
                        "known_output_tokens_all_attempts"]-retained_tokens,
                    "blocked_unsafe_shared_memory_policies": blocked,
                    "unsafe_retry_negative_control_duplicate_writes": unsafe_bank["counter"]-1,
                    "gold_fields_exposed_to_actor": len(exposed)})
    return row(seed, [public_fixture, sorted(first_failure_ids), sorted(wrong_ids)], metrics,
               [asdict(record) for record in runner.records])


def agent_perturb_diagnostic(seed):
    rng = random.Random(seed)
    outcomes, fixtures, exposed = [], [], []
    rejected, unverified_bad_goals = 0, 0

    def semantic(clean, changed, target, kind, annotation):
        before, after = clean.surfaces(), changed.surfaces()
        untouched = all(before[key] == after[key] for key in before if key != perturb.SURFACES[target])
        base = clean.user_utterance.split()
        expected = [int(base[1]), int(base[2])]
        words = changed.user_utterance.lower().split()
        numbers = [int(word) for word in words[1:] if word.isdecimal()]
        goal = words[0] == "add" and numbers == expected[:len(numbers)]
        # The fixture's original context retains the needed operand. This is a
        # domain-specific independent check, not a general LLM semantic oracle.
        recoverable = len(numbers) == 2 or f"backup_y={expected[1]}" in changed.carried_context
        return perturb.SemanticChecks(untouched, goal, recoverable,
                                      isinstance(changed.tool_contract, dict))

    def validator(public, annotation):
        return all(isinstance(value, str) for value in public.tool_contract.values())

    def actor(public):
        exposed.extend(key for key in public.__dataclass_fields__
                       if key in {"reference", "gold", "target", "kind", "evaluation_annotation"})
        words = public.user_utterance.split()
        if words[0] != "add" or "add" not in public.tool_contract:
            raise RuntimeError("public parser/tool contract failure")
        x, y = int(words[1]), int(words[2])
        if public.procedural_spec.startswith("operation=subtract"):
            value = x-y
        elif public.carried_context.startswith("prefer_y="):
            value = x+int(public.carried_context.split(";")[0].split("=")[1])
        else:
            value = x+y
        return perturb.ActorOutput(str(value), recorded_tokens=len(words)+len(str(value)))

    def grader(answer, private):
        if private["scorer_fault"]:
            raise RuntimeError("injected native grader failure")
        return float(answer == private["answer"])

    base_tasks = rng.randrange(3, 6)
    for index in range(base_tasks):
        x, y = rng.randrange(10, 80), rng.randrange(10, 80)
        clean = perturb.PublicInstance(f"fixture-{index}", f"add {x} {y}", "operation=add",
                                       f"backup_y={y}; native_tool=add", {"add": "add two integers"})
        for target in perturb.SURFACES:
            for kind in sorted(perturb.KINDS):
                replacements = {
                    "U": {"missing": f"add {x}", "incorrect": f"ADD {x} {y}",
                          "redundant": f"add {x} {y} irrelevant-{rng.randrange(10000)}"},
                    "P": {"missing": "", "incorrect": "operation=subtract",
                          "redundant": f"operation=add; irrelevant-{rng.randrange(10000)}"},
                    "C": {"missing": "", "incorrect": f"prefer_y={y+1}; backup_y={y}",
                          "redundant": clean.carried_context+f"; noise={rng.randrange(10000)}"},
                    "T": {"missing": {}, "incorrect": {"ADD": "add two integers"},
                          "redundant": {"add": "add two integers", "ghost": "unrelated capability"}},
                }
                pair = perturb.prepare_pair(clean, target=target, kind=kind,
                    replacement=replacements[target][kind], generator_id="fixture-author",
                    verifier_id="independent-arithmetic-verifier", semantic_verifier=semantic,
                    native_validator=validator, evaluation_annotation={"clarification_field": "right operand"})
                private = {"answer": str(x+y), "scorer_fault": index == base_tasks-1 and target == "P"
                           and (kind == "missing" or rng.random() < .5)}
                outcome = perturb.evaluate_pair(pair, actor=actor, native_grader=grader, reference=private)
                outcomes.append(outcome)
                fixtures.append([asdict(pair.clean), asdict(pair.perturbed), target, kind])
        bad = dict(target="U", kind="incorrect", replacement=f"add {x+1} {y}",
                   generator_id="fixture-author", verifier_id="independent-arithmetic-verifier",
                   semantic_verifier=semantic, native_validator=validator)
        unverified_bad_goals += int(validator(clean, {}))
        try:
            perturb.prepare_pair(clean, **bad)
        except ValueError:
            rejected += 1
    result = perturb.paired_metrics(outcomes, requested_pairs=[
        (record.task_id, record.target, record.kind) for record in outcomes])
    independent_complete = sum(r.clean.score is not None and r.perturbed.score is not None for r in outcomes)
    assert result["complete_scored_pairs"] == independent_complete
    metrics = {key: value for key, value in result.items() if value is not None}
    metrics.update({"perturbation_families": len({(r.target, r.kind) for r in outcomes}),
        "rejected_changed_goals": rejected, "syntax_only_negative_control_bad_goal_admissions": unverified_bad_goals,
        "independent_complete_pair_count_error": abs(independent_complete-result["complete_scored_pairs"]),
        "drop_unscored_negative_control_coverage_overstatement": 1-result["pair_coverage"],
        "gold_or_condition_fields_exposed_to_actor": len(exposed)})
    return row(seed, fixtures, metrics, [asdict(record) for record in outcomes])


FUNCTIONS = {"alpha-diana": alpha_diana_diagnostic, "agent-perturb": agent_perturb_diagnostic}


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
        seeds = [int(value) for value in args.seeds.split(",")]
    except ValueError:
        parser.error("integer seeds required")
    if not methods or len(set(methods)) != len(methods) or set(methods)-set(FUNCTIONS):
        parser.error("distinct known methods required")
    if not 1 <= len(seeds) <= 5 or len(set(seeds)) != len(seeds) or any(s < 0 or s >= 2**32 for s in seeds):
        parser.error("one to five distinct uint32 seeds required")
    if args.output.exists():
        raise FileExistsError("refusing to replace an immutable result")
    commit = args.code_commit or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        parser.error("full 40-character code commit required")
    started, components = time.monotonic(), {}
    for method in methods:
        rows = [FUNCTIONS[method](seed) for seed in seeds]
        metrics = {}
        for key in rows[0]["metrics"]:
            values = [r["metrics"][key] for r in rows]
            metrics[key] = {"mean": statistics.mean(values),
                            "std": statistics.stdev(values) if len(values) > 1 else 0., "n": len(values)}
        components[method] = {"dataset": {"id": f"synthetic-{method}-contract-fixture",
            "revision": fingerprint([r["fixture_sha256"] for r in rows]), "public_benchmark_evaluated": False,
            "initialization": "Python random.Random(seed); inert public arithmetic/session fixtures"},
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
            "claim_policy": "CPU protocol fixtures only; not official benchmarks, Agent capability or full-paper reproduction"},
        "command": "PYTHONPATH=src python scripts/run_oct19_agent_components.py "
            f"--methods {args.methods} --seeds {args.seeds} --device cpu --code-commit {commit} --output <fresh-result.json>"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"methods": methods, "seeds": seeds, "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
