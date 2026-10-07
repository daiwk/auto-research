#!/usr/bin/env python3
"""Export auditable, corpus-free summaries of the two checkpoint experiments."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from statistics import mean


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def tokens(calls):
    return sum(call["input_tokens"] + call["output_tokens"] for call in calls)


def envelope(key, dataset, fingerprint, commit, runs, checkpoints, path):
    seeds = sorted({run["seed"] for run in runs})
    return {
        "schema_version": 2, "manifest_ref": "agent-research:" + key,
        "method": key, "dataset": dataset, "seeds": seeds,
        "diagnostic_only": True, "promotion_eligible": False,
        "evaluation_protocol": {
            "tier": "l1_mechanism_diagnostic", "seeds": seeds,
            "formal_comparison": False,
            "claim_policy": "Real frozen checkpoints, small local task budget; not original paper benchmarks or stable capability improvement.",
        },
        "provenance": {"artifact_path": path, "dataset_fingerprint": fingerprint,
                       "commit": commit},
        "checkpoints": checkpoints, "runs": runs,
    }


def summarize_frugalevo(raw, commit, path):
    rows = []
    for run in raw["runs"]:
        rows.append({
            "seed": run["config"]["seed"], "method": run["method"],
            "config": run["config"], "spent": run["spent"],
            "best_score": run["best"]["score"], "ba_auc": run["ba_auc"],
            "mean_budget_score": run["mean_budget_score"],
            "model_calls": len(run["calls"]), "tokens": tokens(run["calls"]),
            "stage_counts": dict(Counter(c["stage"] for c in run["candidates"])),
            "valid_candidates": sum(c["score"] > 0 for c in run["candidates"]),
            "evaluated_candidates": len(run["candidates"]),
            "curve": run["curve"], "archive_cells": run["archive_cells"],
            "raw_run_sha256": digest(run), "best_program_sha256": digest(run["best"]["code"]),
        })
    pairs = Counter((row["seed"], row["method"]) for row in rows)
    seeds = {row["seed"] for row in rows}
    if not seeds or pairs != Counter({(s, m): 1 for s in seeds for m in ("weak-iterative", "frugalevo")}):
        raise ValueError("incomplete or duplicate FrugalEvo method/seed pairs")
    result = envelope("frugalevo", "Circle Packing n=26", raw["dataset"]["revision"],
                      commit, rows, raw["checkpoints"], path)
    result["dataset_details"] = raw["dataset"]
    result["metrics"] = {
        method.replace("-", "_") + "_" + field + "_mean": mean(row[field] for row in rows if row["method"] == method)
        for method in ("weak-iterative", "frugalevo")
        for field in ("best_score", "mean_budget_score", "spent", "model_calls")
    }
    result["boundary"] = raw["boundary"]
    return result


def summarize_sentry(raw, commit, path):
    rows = []
    for run in raw["runs"]:
        if "monitor_events" not in run or len(run["held_out"]) != 2 * raw["split_sizes"]["held_out"]:
            raise ValueError("incomplete Sentry seed")
        memory_ids = {case["id"] for case in run["memory_cases"]}
        ids_by_method = {method: {case["id"] for case in run["held_out"] if case["method"] == method}
                         for method in ("base", "sentry")}
        if (ids_by_method["base"] != ids_by_method["sentry"]
                or len(ids_by_method["base"]) != raw["split_sizes"]["held_out"]
                or len(memory_ids) != raw["split_sizes"]["memory"]
                or memory_ids & ids_by_method["base"]):
            raise ValueError("invalid Sentry split or unpaired cases")
        cases = []
        for case in run["held_out"]:
            cases.append({k: case[k] for k in ("id", "method", "exact_match", "completed", "tool_steps", "invalid_actions")}
                         | {"agent_tokens": tokens(case["agent_generations"]), "trace_sha256": digest(case)})
        rows.append({"seed": run["seed"], "memory_ids": sorted(memory_ids),
                     "frozen_lessons": len(run["frozen_playbook"]),
                     "playbook_sha256": digest(run["frozen_playbook"]),
                     "event_counts": dict(Counter(event["event"] for event in run["monitor_events"])),
                     "retrieval_events": sum(event["event"] == "soft_repair" and event["retrieved"] > 0
                                             for event in run["monitor_events"]),
                     "manager_calls": len(run["manager_calls"]),
                     "manager_tokens_memory_plus_held_out": tokens(run["manager_calls"]),
                     "memory_agent_tokens": sum(tokens(case["agent_generations"]) for case in run["memory_cases"]),
                     "raw_run_sha256": digest(run), "held_out": cases})
    if not rows or len({row["seed"] for row in rows}) != len(rows):
        raise ValueError("missing or duplicate Sentry seeds")
    result = envelope("sentry", raw["dataset"], raw["sha256"], commit, rows, [raw["checkpoint"]], path)
    result["dataset_revision"] = raw["revision"]
    result["split_sizes"] = raw["split_sizes"]
    result["metrics"] = {
        method + "_" + field + "_mean": mean(case[field] for row in rows for case in row["held_out"] if case["method"] == method)
        for method in ("base", "sentry")
        for field in ("exact_match", "tool_steps", "agent_tokens", "invalid_actions")
    }
    result["metrics"]["frozen_lessons_mean"] = mean(row["frozen_lessons"] for row in rows)
    result["metrics"]["manager_tokens_per_seed_memory_plus_held_out"] = mean(row["manager_tokens_memory_plus_held_out"] for row in rows)
    result["boundary"] = raw["boundary"] + "; manager cost includes memory preparation, not equal-token-budget comparison"
    result["split_protocol"] = raw["protocol"]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", choices=("frugalevo", "sentry"), required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--commit", required=True)
    args = parser.parse_args()
    function = summarize_frugalevo if args.kind == "frugalevo" else summarize_sentry
    payload = function(json.loads(args.input.read_text()), args.commit, args.output.as_posix())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(payload["metrics"], indent=2))


if __name__ == "__main__":
    main()
