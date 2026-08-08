#!/usr/bin/env python3
"""Re-run the closed P0/P1 paper batch and persist scalar-only artifacts."""

from __future__ import annotations

import json
import os
from pathlib import Path

from auto_research.agent_research import AgentResearchConfig, AgentResearchRunner
from auto_research.post_training import PostTrainingConfig, PostTrainingRunner
from auto_research.reproductions.registry import get_adapter


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ROOT / "docs" / "experiments"
DATA = ROOT / "data"
POST = (
    "distilled-rl", "u-opsd", "rp-opsd", "pcsd", "adrs", "mopd", "opd-lm",
)
AGENT = ("agent-opsd", "ocsd", "vermem", "coevo-mem")
REPRODUCTIONS = ("dme", "steps", "spear", "open-language-model")


def main() -> None:
    EXPERIMENTS.mkdir(parents=True, exist_ok=True)
    scratch = ROOT / "runs" / "20260808-p0-p1"
    payload: dict[str, object] = {
        "batch": "2026-08-08-p0-p1-closed-audit",
        "seed": 42,
        "post_training": {},
        "agent": {},
    }
    for algorithm in POST:
        result, _ = PostTrainingRunner(PostTrainingConfig(
            algorithm=algorithm,
            steps=120,
            maximum_examples=256,
            seed=42,
            output_dir=scratch / "post-training",
        )).run()
        payload["post_training"][algorithm] = {
            "baseline": result.baseline,
            "final": result.final,
            "relative_accuracy": result.relative_accuracy,
            "diagnostics": result.training["last_diagnostics"],
        }
    for method in AGENT:
        result, _ = AgentResearchRunner(AgentResearchConfig(
            method=method,
            benchmark="planbench-mini",
            episodes=120,
            memory_size=24,
            seed=42,
            output_dir=scratch / "agent",
        )).run()
        payload["agent"][method] = {
            "metrics": result.metrics,
            "diagnostics": {
                key: value for key, value in result.diagnostics.items()
                if value and key != "fidelity"
            },
        }
    (EXPERIMENTS / "p0-p1-closed-audit-20260808-seed42.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    os.environ.setdefault("AUTO_RESEARCH_LLM_P0_STEPS", "30")
    for key in REPRODUCTIONS:
        adapter = get_adapter(key)
        result = adapter.run(DATA, 42)
        slug = f"{adapter.paper.arxiv_id}-{adapter.key}"
        metrics_dir = ROOT / "docs" / "reproductions" / slug / "metrics"
        metrics_dir.mkdir(parents=True, exist_ok=True)
        (metrics_dir / "public-seed42.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )


if __name__ == "__main__":
    main()
