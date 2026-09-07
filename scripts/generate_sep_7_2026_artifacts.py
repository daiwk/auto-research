#!/usr/bin/env python3
"""Regenerate multi-seed metrics for the 2026-09-07 incremental batch."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from auto_research.agent_research import AgentResearchConfig, AgentResearchRunner
from auto_research.post_training import PostTrainingConfig, PostTrainingRunner


ROOT = Path(__file__).resolve().parents[1]
SEEDS = (42, 43, 44)
AGENTS = {
    "atomrec": "2609.04882-atomrec",
    "coskill": "2609.04865-coskill",
    "silr": "2609.04629-silr",
    "multi-harness-rl": "2609.04518-multi-harness-rl",
}


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    runs = []
    for seed in SEEDS:
        result, _ = PostTrainingRunner(
            PostTrainingConfig(
                algorithm="sparse-opd",
                dataset="arithmetic-smoke",
                steps=100,
                maximum_examples=192,
                seed=seed,
                allow_network=False,
                output_dir=ROOT / "runs" / "post-training",
            )
        ).run()
        runs.append({**asdict(result), "relative_accuracy": result.relative_accuracy})
    write_json(
        ROOT / "docs/post-training/2609.04565-sparse-opd/metrics/arithmetic-smoke-seeds42-44.json",
        {
            "schema_version": 2,
            "method": "sparse-opd",
            "seeds": list(SEEDS),
            "runs": runs,
            "manifest_ref": "post-training:arithmetic-smoke-seeds42-44",
            "evaluation_protocol": {
                "tier": "l1_mechanism",
                "seeds": list(SEEDS),
                "formal_comparison": True,
                "claim_policy": "formal multi-seed mechanism comparison",
            },
        },
    )

    for method, slug in AGENTS.items():
        agent_runs = []
        for seed in SEEDS:
            result, _ = AgentResearchRunner(
                AgentResearchConfig(
                    method=method,
                    benchmark="evomem-mini",
                    episodes=120,
                    memory_size=24,
                    seed=seed,
                    output_dir=ROOT / "runs" / "agent-research",
                )
            ).run()
            agent_runs.append(asdict(result))
        write_json(
            ROOT / f"docs/agent-research/{slug}/metrics/mini-suite-seeds42-44.json",
            {
                "schema_version": 2,
                "method": method,
                "dataset": "evomem-mini",
                "seeds": list(SEEDS),
                "runs": agent_runs,
                "manifest_ref": "agent-research:evomem-mini-seeds42-44",
                "evaluation_protocol": {
                    "tier": "l1_mechanism",
                    "seeds": list(SEEDS),
                    "formal_comparison": True,
                    "claim_policy": "mechanism counters, not benchmark capability",
                },
            },
        )


if __name__ == "__main__":
    main()
