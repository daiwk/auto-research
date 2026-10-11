#!/usr/bin/env python3
"""Validate real Memento3 artifact contracts before extracting bounded metrics.

No GPU receipt is fabricated here. The source revision and every executed source
hash are checked against local Git; accepted generated code is reinterpreted and
cell-exact replay is checked against the appropriate complete-history prefix.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

from auto_research.agent_research.memento3 import Trajectory, _json, observation, replay
from auto_research.agent_research.memento3_python import RestrictedProgram, ProgramError
from auto_research.agent_research.search_checkpoint import LARGE_MODEL, LARGE_REVISION


SOURCES = {
    "scripts/run_memento3_checkpoint.py", "src/auto_research/agent_research/memento3.py",
    "src/auto_research/agent_research/memento3_python.py",
    "src/auto_research/agent_research/search_checkpoint.py",
    "src/auto_research/agent_research/frugalevo.py",
}


def curate(raw, *, git_show=None):
    if raw.get("status") != "completed" or raw.get("paper") != "2610.11794" or raw.get("method") != "memento3":
        raise ValueError("not a completed real Memento3 artifact")
    protocol = raw["protocol"]
    if (protocol.get("underlying_llm_frozen") is not True
            or protocol.get("gold_plan_read") is not False
            or protocol.get("environment_source_read_by_policy") is not False
            or protocol.get("test_read") is not False
            or protocol.get("code_as_model_not_handwritten_fallback") is not True
            or protocol.get("semantic_judge_human_calibrated") is not False):
        raise ValueError("isolation/frozen-model protocol")
    if (raw.get("evaluation_tier") != "l1_core_mechanism" or raw.get("diagnostic_only") is not True
            or raw.get("formal_comparison") is not False or raw.get("paper_benchmark_reproduced") is not False):
        raise ValueError("bounded experiment cannot be promoted to paper benchmark")
    if raw["checkpoint"]["model_id"] != LARGE_MODEL or raw["checkpoint"]["revision"] != LARGE_REVISION:
        raise ValueError("unverified public checkpoint identity")
    if raw["environment"] != {"id": "Gymnasium/FrozenLake-v1", "version": "1.1.1",
                              "map_seed": raw["run"]["seed"], "slippery": False, "size": 4}:
        raise ValueError("fixed public substitute environment required")
    commit, hashes = raw["implementation_commit"], raw["source_sha256"]
    if not re.fullmatch(r"[0-9a-f]{40}", commit) or set(hashes) != SOURCES:
        raise ValueError("complete immutable source provenance required")
    if git_show is None:
        git_show = lambda revision, path: subprocess.check_output(["git", "show", f"{revision}:{path}"])
    for path, digest in hashes.items():
        if hashlib.sha256(git_show(commit, path)).hexdigest() != digest:
            raise ValueError(f"executed source differs from commit: {path}")
    run = raw["run"]
    initial = observation(run["initial_observation"])
    interactions = run["interactions"]
    if type(run["real_actions"]) is not int or run["real_actions"] != len(interactions) or not 0 <= len(interactions) <= run["real_action_budget"]:
        raise ValueError("real action accounting")
    transitions = []
    for index, step in enumerate(interactions):
        if type(step["action"]) is not int or step["action"] not in range(4):
            raise ValueError("public action interface")
        frame = observation(step["observation"])
        if frame["terminated"] and index != len(interactions) - 1:
            raise ValueError("actions after termination")
        transitions.append((step["action"], frame))
    latest = transitions[-1][1] if transitions else initial
    if run["goal_completed"] != latest["completed"] or run["terminated"] != latest["terminated"]:
        raise ValueError("terminal outcome accounting")
    calls = run["calls"]
    if len(raw["checkpoint_calls"]) != len(calls):
        raise ValueError("checkpoint call accounting")
    for call, measured in zip(calls, raw["checkpoint_calls"]):
        if (call["input_tokens"] != measured["input_tokens"]
                or call["output_tokens"] != measured["output_tokens"]
                or not 0 < call["output_tokens"] <= call["output_budget"]
                or call["budget_reached"] != (call["output_tokens"] >= call["output_budget"])):
            raise ValueError("checkpoint token budget accounting")
    compiled_sources = []
    for call in calls:
        if call["role"] == "compile":
            try:
                compiled_sources.append(_json(call["text"])["source"])
            except (ValueError, KeyError):
                pass  # Malformed generations remain recorded failures.
    if run["accepted_versions"] != len(run["versions"]):
        raise ValueError("accepted version accounting")
    semantic_ok, accepted_events = False, []
    for event in run["events"]:
        if event["stage"] == "faithfulness":
            semantic_ok = event.get("faithful") is True and isinstance(event.get("reason"), str)
        elif event["stage"] == "accepted":
            if not semantic_ok:
                raise ValueError("accepted source lacks positive semantic judgement")
            accepted_events.append({k: event[k] for k in ("member", "generation", "rulebook", "source", "real_transitions")})
            semantic_ok = False
        elif event["stage"] == "rejected":
            semantic_ok = False
    if accepted_events != run["versions"]:
        raise ValueError("accepted version/event sequence")
    members = {}
    for version in run["versions"]:
        if version["source"] not in compiled_sources:
            raise ValueError("accepted model was not generated by checkpoint")
        count = version["real_transitions"]
        if type(count) is not int or not 0 <= count <= len(transitions):
            raise ValueError("accepted replay history prefix")
        program = RestrictedProgram(version["source"])
        replay(program, [Trajectory(initial, transitions[:count])])
        members[version["member"]] = program
    final_valid = 0
    for program in members.values():
        try:
            replay(program, [Trajectory(initial, transitions)])
            final_valid += 1
        except ProgramError:
            pass
    if run["valid_final_members"] != final_valid:
        raise ValueError("final replay-consistent model accounting")
    # A missing accepted model remains a failed learning attempt, not hidden by
    # the script successfully finishing its environment action loop.
    metrics = {"real_actions": len(interactions), "goal_completed": int(run["goal_completed"]),
               "accepted_versions": len(run["versions"]), "valid_final_members": final_valid,
               "generated_compile_calls": sum(c["role"] == "compile" for c in calls),
               "frozen_llm_calls": len(calls), "rejected_proposals": sum(e["stage"] == "rejected" for e in run["events"]),
               "prediction_mismatch_events": sum(e["stage"] == "prediction_mismatch" for e in run["events"]),
               "maximum_plan_equivalence_classes": max((e["class_count"] for e in run["events"] if e["stage"] == "plan"), default=0)}
    return {"method": "memento3", "dataset": "Gymnasium/FrozenLake-v1", "seeds": [run["seed"]],
            "metrics": metrics, "evaluation_protocol": {"tier": "l1_core_mechanism", "diagnostic_only": True,
                "formal_comparison": False, "claim_policy": "bounded generated-model mechanism; not ARC/Pong or capability improvement"},
            "checkpoint": raw["checkpoint"], "environment": raw["environment"],
            "code_commit": commit, "source_sha256": hashes,
            "learning_status": "accepted_generated_model" if run["versions"] else "no_accepted_model"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = curate(json.loads(args.input.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["metrics"]))


if __name__ == "__main__":
    main()
