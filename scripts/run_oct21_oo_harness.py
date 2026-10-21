"""CPU-only executable OO-Harness mechanism diagnostic, without LLM calls."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import random
import re
import statistics
import subprocess

from auto_research.agent_research.oo_harness import (
    Action, Harness, HarnessDiscovery, PublicTask, ToolObservation,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATHS = ("scripts/run_oct21_oo_harness.py", "src/auto_research/agent_research/oo_harness.py")


class MissingWriteHarness(Harness):
    def verify_before_finish(self, task, observations):
        parent = super().verify_before_finish(task, observations)
        if parent:
            return parent
        if not any(item.mutated for item in observations):
            return "The public task requests a write, but no mutating tool call has succeeded."
        return None


class InheritedPromptHarness(MissingWriteHarness):
    def system_prompt(self, task):
        return super().system_prompt(task) + " Preserve the inherited completion check."


class RemovedGuardControl(InheritedPromptHarness):
    def verify_before_finish(self, task, observations):
        return None


def scripted_actor(context):
    """A deliberately premature deterministic actor, not a language model."""
    if not context.observations:
        return Action("tool", "public-source", "read")
    if any(item.tool == "__finish_guard__" for item in context.observations):
        if not any(item.mutated for item in context.observations):
            return Action("tool", context.observations[0].content, "write")
    return Action("finish", "fixture completion")


def environment_factory(payload, states):
    def factory():
        state = {"writes": [], "reads": 0}
        states.append(state)
        def execute(tool, argument):
            if tool == "read":
                state["reads"] += 1
                return ToolObservation(tool, payload)
            state["writes"].append(argument)
            return ToolObservation(tool, "write observed", mutated=True)
        return execute
    return factory


def diagnostic(seed):
    rng = random.Random(seed)
    train = PublicTask("discovery-copy", "Copy public-source to the output.")
    heldout = tuple(PublicTask(f"heldout-{index}", "Copy public-source to the output.") for index in range(8))
    discovery = HarnessDiscovery(Harness, discovery_task_ids=(train.task_id,),
        heldout_task_ids=tuple(task.task_id for task in heldout))
    # The independent deterministic discovery grader checks actual tool state;
    # its verdict is never part of the actor or router context.
    def score(cls):
        states = []
        cls().run(train, actor=scripted_actor, tools=environment_factory("discovery public data", states)())
        return float(states[0]["writes"] == ["discovery public data"])
    baseline_score, guard_score = score(Harness), score(MissingWriteHarness)
    discovery.add_cluster("write-required", baseline_score, task_ids=(train.task_id,))
    first = discovery.consider("write-guard", MissingWriteHarness, parent_key="base",
        cluster="write-required", score=guard_score, checks_passed=True, mechanism="missing-write completion check")
    # Equal score is rejected: no fabricated gain for the inherited prompt.
    second = discovery.consider("same-score", InheritedPromptHarness, parent_key="write-guard",
        cluster="write-required", score=score(InheritedPromptHarness), checks_passed=True,
        mechanism="inherited check plus a prompt change")
    frozen = discovery.freeze(routing_lessons=("For public tasks requiring a write, select write-guard.",))
    copied, negative_writes, leak_fields, calls, fixtures = [], [], [], [], []
    for task in heldout:
        payload = f"public payload {rng.randrange(10**9)}"
        states, views = [], []
        def route(view):
            views.append(view)
            return "write-guard"
        result = frozen.deploy(task, actor=scripted_actor,
            tool_factory=environment_factory(payload, states), router=route)
        copied.append(int(states[1]["writes"] == [payload]))
        # Removing only the inherited finish guard is the mechanism ablation.
        negative = []
        RemovedGuardControl().run(task, actor=scripted_actor,
            tools=environment_factory(payload, negative)())
        negative_writes.append(len(negative[0]["writes"]))
        visible = asdict(views[0])
        leak_fields.append(len(set(visible) & {"score", "grader", "reference_answer", "outcomes"}))
        calls.append(result.total_actor_calls)
        fixtures.append({"task": asdict(task), "payload": payload})
        assert len(states) == 2 and not states[0]["writes"]
        assert not result.base_reused and result.run.finish_rejections == 1
    reuse_states = []
    reuse = frozen.deploy(heldout[0], actor=scripted_actor,
        tool_factory=environment_factory("reuse", reuse_states), router=lambda _: "base")
    metrics = {"heldout_fixture_tasks": len(heldout), "observed_guarded_writes": sum(copied),
        "removed_guard_control_writes": sum(negative_writes), "router_private_top_level_fields": sum(leak_fields),
        "accepted_candidates": int(first.accepted), "equal_score_candidates_rejected": int(not second.accepted),
        "base_reuse_environment_count": len(reuse_states), "base_reuse_actor_calls": reuse.total_actor_calls,
        "specialist_total_actor_calls": sum(calls), "actual_llm_calls": 0}
    assert sum(copied) == len(heldout) and sum(negative_writes) == 0 and sum(leak_fields) == 0
    assert reuse.base_reused and len(reuse_states) == 1
    return {"seed": seed, "fixture_sha256": hashlib.sha256(
        json.dumps(fixtures, sort_keys=True).encode()).hexdigest(), "metrics": metrics}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", choices=("cpu",), default="cpu")
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        seeds = [int(value) for value in args.seeds.split(",")]
    except ValueError:
        parser.error("integer seeds required")
    if not 1 <= len(seeds) <= 5 or len(set(seeds)) != len(seeds) or any(not 0 <= seed < 2**32 for seed in seeds):
        parser.error("one to five distinct uint32 seeds required")
    if args.output.exists():
        parser.error("immutable output already exists")
    rows = [diagnostic(seed) for seed in seeds]
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        parser.error("full source commit required")
    source_hashes = {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in SOURCE_PATHS}
    dirty = bool(subprocess.check_output(["git", "status", "--porcelain", "--", *SOURCE_PATHS], cwd=ROOT, text=True).strip())
    payload = {"schema_version": 2, "method": "oo-harness", "seeds": seeds,
        "manifest_ref": "agent-research:oo-harness", "device": "cpu", "evaluation_tier": "l1_mechanism",
        "dataset": {"id": "synthetic-oo-harness-public-write", "revision": "oct21-contract-v1", "capability_benchmark": False},
        "evaluation_protocol": {"tier": "l1_mechanism", "seeds": seeds, "formal_comparison": False,
            "claim_policy": "scripted CPU runtime mechanism diagnostic, not LLM or official benchmark evidence"},
        "per_seed": rows, "metrics": {key: {"mean": statistics.mean(row["metrics"][key] for row in rows),
            "std": statistics.stdev(row["metrics"][key] for row in rows) if len(rows) > 1 else 0., "n": len(rows)}
            for key in rows[0]["metrics"]},
        "provenance": {"commit": commit, "artifact_path": args.output.as_posix(),
            "dataset_fingerprint": "sha256:" + hashlib.sha256("".join(row["fixture_sha256"] for row in rows).encode()).hexdigest(),
            "executed_source_uncommitted": dirty, "executed_source_sha256": source_hashes, "accelerator": "CPU"},
        "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
        "formal_comparison": False, "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"method": "oo-harness", "seeds": seeds, "output": str(args.output)}))


if __name__ == "__main__":
    main()
