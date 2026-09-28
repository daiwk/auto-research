#!/usr/bin/env python3
"""Run a no-oracle, three-seed GRAFT tool-policy diagnostic."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from statistics import mean

from auto_research.agent_research.graft_public import run_graft_tool_policy


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--train-episodes", type=int, default=36)
    parser.add_argument("--evaluation-episodes", type=int, default=60)
    parser.add_argument("--epochs", type=int, default=4)
    parser.add_argument("--learning-rate", type=float, default=0.25)
    parser.add_argument("--output", type=Path, default=Path("runs/agent-research/graft-public.json"))
    args = parser.parse_args()
    seeds = tuple(int(value) for value in args.seeds.split(","))
    if len(set(seeds)) != len(seeds):
        raise ValueError("seeds must be unique")
    runs = [run_graft_tool_policy(
        seed=seed, train_episodes=args.train_episodes,
        validation_episodes=args.evaluation_episodes,
        test_episodes=args.evaluation_episodes,
        epochs=args.epochs, learning_rate=args.learning_rate,
    ) for seed in seeds]
    summary = {
        method: {
            split: {metric: mean(run["methods"][method][split][metric] for run in runs)
                    for metric in runs[0]["methods"][method][split]}
            for split in ("validation", "test")
        }
        for method in ("outcome", "graph_td")
    }
    payload = {
        "schema_version": 2,
        "domain": "agent",
        "method": "graft-public-tool-policy",
        "manifest_ref": "experiments:graft-public-toolroute-l21",
        "dataset": "toolroute-l2.1-v1",
        "seeds": list(seeds),
        "evaluation_protocol": {
            "tier": "l1_mechanism_diagnostic", "formal_comparison": False,
            "diagnostic_only": True,
            "seeds": list(seeds),
            "claim_policy": "tabular policy diagnostic; not GRAFT LLM reproduction",
        },
        "provenance": {
            "artifact_path": str(args.output.resolve().relative_to(ROOT)),
            "dataset_fingerprint": hashlib.sha256(
                (ROOT / "src/auto_research/agent_research/capability_benchmark.py").read_bytes()
            ).hexdigest(),
        },
        "metrics": {
            "graph_test_joint_success": summary["graph_td"]["test"]["joint_success"],
            "outcome_test_joint_success": summary["outcome"]["test"]["joint_success"],
            "joint_success_delta": (
                summary["graph_td"]["test"]["joint_success"]
                - summary["outcome"]["test"]["joint_success"]
            ),
        },
        "summary": summary,
        "seed_results": runs,
        "diagnostic_only": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
