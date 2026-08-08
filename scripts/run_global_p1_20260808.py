#!/usr/bin/env python3
"""Run all 15 P1 implementations and persist checkpoint-free metrics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from auto_research.agent_research import AgentResearchConfig, AgentResearchRunner
from auto_research.post_training import PostTrainingConfig, PostTrainingRunner
from auto_research.reproductions.registry import get_adapter


ROOT = Path(__file__).resolve().parents[1]
REPRODUCTIONS = ("twin-v2", "sim", "crsd", "clip", "llava", "speculative-decoding", "awq", "medusa")
POST = ("minirl", "missing-old-logits", "stare")
AGENT = ("agent-r1", "camel", "toolbench", "gaia")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--section", choices=("all", "reproductions", "post-training", "agent"), default="all")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    output = ROOT / "docs/experiments/global-p1-20260808-seed42.json"
    payload = json.loads(output.read_text()) if output.exists() else {}
    payload.update({"batch": "2026-08-08-global-theme-gap-review-p1", "seed": 42})
    payload.setdefault("post_training", {}); payload.setdefault("agent", {})
    if args.section in {"all", "reproductions"}:
        for key in REPRODUCTIONS:
            adapter = get_adapter(key)
            artifact = ROOT / "docs/reproductions" / f"{adapter.paper.arxiv_id}-{key}" / "metrics/public-seed42.json"
            if artifact.exists() and not args.force:
                continue
            result = adapter.run(ROOT / "data", 42)
            artifact.parent.mkdir(parents=True, exist_ok=True)
            artifact.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    if args.section in {"all", "post-training"}:
        for key in POST:
            result, _ = PostTrainingRunner(PostTrainingConfig(
                algorithm=key, steps=120, maximum_examples=256, seed=42,
                output_dir=ROOT / "runs/20260808-global-p1/post-training",
            )).run()
            payload["post_training"][key] = {
                "baseline": result.baseline, "final": result.final,
                "relative_accuracy": result.relative_accuracy,
                "diagnostics": result.training["last_diagnostics"],
            }
    if args.section in {"all", "agent"}:
        for key in AGENT:
            benchmark = "gaia-mini" if key == "gaia" else "planbench-mini"
            result, _ = AgentResearchRunner(AgentResearchConfig(
                method=key, benchmark=benchmark, episodes=120, memory_size=24,
                seed=42, output_dir=ROOT / "runs/20260808-global-p1/agent",
            )).run()
            payload["agent"][key] = {"benchmark": benchmark, "metrics": result.metrics,
                                       "diagnostics": {k: v for k, v in result.diagnostics.items() if v and k != "fidelity"}}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
