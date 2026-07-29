#!/usr/bin/env python3
"""Generate stable local metrics for the 2026-07-29 reproduction batch."""

from __future__ import annotations

import json
from pathlib import Path

from auto_research.agent_research import AgentResearchConfig, AgentResearchRunner
from auto_research.post_training import PostTrainingConfig, PostTrainingRunner
from auto_research.reproductions.registry import get_adapter


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOCS = ROOT / "docs"
INDUSTRIAL = (
    "reco-reward",
    "twice",
    "swag-bid",
    "youtube-freshness",
    "melo",
    "penelope",
)
POST_TRAINING = ("relay-opd", "cort")
AGENTS = ("seed", "cast", "turn-opd", "hiskill", "unimem")


def dump(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    for key in INDUSTRIAL:
        adapter = get_adapter(key)
        result = adapter.run(DATA, 42)
        slug = f"{adapter.paper.arxiv_id}-{key}"
        dump(
            DOCS / "reproductions" / slug / "metrics" / "result-seed42.json",
            result,
        )

    post_payload = {}
    for algorithm in POST_TRAINING:
        result, _ = PostTrainingRunner(
            PostTrainingConfig(
                algorithm=algorithm,
                dataset="gsm8k-candidate",
                output_dir=ROOT / "runs" / "post-training",
                steps=120,
                maximum_examples=256,
                seed=42,
            )
        ).run()
        post_payload[algorithm] = {
            "baseline": result.baseline,
            "final": result.final,
            "relative_accuracy": result.relative_accuracy,
            "training": result.training,
        }
    dump(
        DOCS / "experiments" / "post-training-20260729-seed42.json",
        post_payload,
    )

    agent_payload = {}
    benchmark = {
        "seed": "planbench-mini",
        "cast": "planbench-mini",
        "turn-opd": "scalemcp-mini",
        "hiskill": "planbench-mini",
        "unimem": "evomem-mini",
    }
    for method in AGENTS:
        result, _ = AgentResearchRunner(
            AgentResearchConfig(
                method=method,
                benchmark=benchmark[method],
                episodes=120,
                memory_size=24,
                seed=42,
                output_dir=ROOT / "runs" / "agent-research",
            )
        ).run()
        agent_payload[method] = {
            "benchmark": result.benchmark,
            "metrics": result.metrics,
            "axis_metrics": result.axis_metrics,
            "diagnostics": result.diagnostics,
        }
    dump(DOCS / "experiments" / "agent-20260729-seed42.json", agent_payload)


if __name__ == "__main__":
    main()
