#!/usr/bin/env python3
"""Run the representative RL algorithms added from ``rl_papers_summary.md``.

The output intentionally records metrics only. Checkpoints remain in ``runs/``
and are excluded from version control.
"""

from __future__ import annotations

import json
from pathlib import Path

from auto_research.agent_research import AgentResearchConfig, AgentResearchRunner
from auto_research.post_training import PostTrainingConfig, PostTrainingRunner


ROOT = Path(__file__).resolve().parents[1]
POST_TRAINING = (
    "ripo", "tis", "icepop", "online-icepop", "kpop", "gppo", "dr-grpo",
    "armor", "reinforce-plus", "taco", "chord", "vapo",
)
AGENTS = ("gigpo", "steppo")


def main() -> None:
    payload: dict[str, dict] = {"post_training": {}, "agent_research": {}}
    for algorithm in POST_TRAINING:
        result, _ = PostTrainingRunner(
            PostTrainingConfig(
                algorithm=algorithm,
                dataset="gsm8k-candidate",
                maximum_examples=256,
                steps=120,
                seed=42,
                output_dir=ROOT / "runs" / "post-training",
            )
        ).run()
        payload["post_training"][algorithm] = {
            "baseline": result.baseline,
            "final": result.final,
            "relative_accuracy": result.relative_accuracy,
            "training": result.training,
        }

    for method in AGENTS:
        result, _ = AgentResearchRunner(
            AgentResearchConfig(
                method=method,
                benchmark="planbench-mini",
                episodes=120,
                memory_size=24,
                seed=42,
                output_dir=ROOT / "runs" / "agent-research",
            )
        ).run()
        payload["agent_research"][method] = {
            "benchmark": result.benchmark,
            "metrics": result.metrics,
            "axis_metrics": result.axis_metrics,
            "diagnostics": result.diagnostics,
        }

    target = ROOT / "docs" / "experiments" / "rl-papers-summary-seed42.json"
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
