#!/usr/bin/env python3
"""Held-out Sentry comparison with answer-isolated HotpotQA tool episodes."""

import argparse
from dataclasses import asdict
import json
from pathlib import Path

from auto_research.agent_research.search_checkpoint import FrozenGenerator, SMALL_MODEL, SMALL_REVISION
from auto_research.agent_research.sentry import Sentry
from auto_research.agent_research.sentry_public import (
    DATASET_ID, DATASET_REVISION, DATASET_SHA256, exact_match, load_cases, public_case, run_episode,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--memory-cases", type=int, default=4)
    parser.add_argument("--held-out-cases", type=int, default=8)
    parser.add_argument("--seeds", default="42,43,44")
    args = parser.parse_args()
    if min(args.memory_cases, args.held_out_cases) < 1:
        parser.error("case counts must be positive")
    rows = load_cases(args.dataset, args.memory_cases + args.held_out_cases)
    checkpoint = FrozenGenerator(SMALL_MODEL, SMALL_REVISION, path=args.checkpoint)
    result = {"dataset": DATASET_ID, "revision": DATASET_REVISION, "sha256": DATASET_SHA256,
              "checkpoint": checkpoint.provenance(), "accelerator": checkpoint.torch.cuda.get_device_name(),
              "protocol": "disjoint hashed-id memory/held-out subsets of official dev; NOT official test; frozen playbook; same action budget; no test tuning",
              "boundary": "HotpotQA-backed local read-only tools, not Sentry's four original benchmarks",
              "runs": []}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    for seed in map(int, args.seeds.split(",")):
        manager_calls = []
        def manager_model(role, prompt):
            completion = checkpoint.generate(prompt, 320, seed + 10000 + len(manager_calls))
            manager_calls.append({"role": role, **asdict(completion)})
            return completion.text
        monitor = Sentry(manager_model)
        run = {"seed": seed, "memory_cases": [], "held_out": [], "manager_calls": manager_calls}
        for index, row in enumerate(rows[:args.memory_cases]):
            trace = run_episode(public_case(row), checkpoint.generate, sentry=monitor,
                                seed=seed + index * 100)
            # No reference label passed to the memory-building path.
            run["memory_cases"].append(trace)
            print(json.dumps({"seed": seed, "split": "memory", "index": index,
                              "lessons": len(monitor.playbook)}), flush=True)
        monitor.learning = False
        run["frozen_playbook"] = [asdict(entry) for entry in monitor.playbook]
        for index, row in enumerate(rows[args.memory_cases:]):
            for method in ("base", "sentry"):
                trace = run_episode(public_case(row), checkpoint.generate,
                                    sentry=monitor if method == "sentry" else None,
                                    seed=seed + 1000 + index * 100)
                # The held-out label is used ONLY after all agent/manager calls end.
                trace.update(method=method, exact_match=exact_match(trace["prediction"], row["answer"]))
                run["held_out"].append(trace)
                print(json.dumps({"seed": seed, "split": "held_out", "index": index,
                                  "method": method, "em": trace["exact_match"]}), flush=True)
        assert run["frozen_playbook"] == [asdict(entry) for entry in monitor.playbook]
        run["monitor_events"] = monitor.events
        result["runs"].append(run)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
