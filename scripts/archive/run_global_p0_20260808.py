#!/usr/bin/env python3
"""Run all 38 P0 implementations and persist scalar/trace-free documentation artifacts."""

from __future__ import annotations

import json
import os
import argparse
from pathlib import Path

from auto_research.agent_research import AgentResearchConfig, AgentResearchRunner
from auto_research.post_training import PostTrainingConfig, PostTrainingRunner
from auto_research.reproductions.registry import get_adapter


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
EXPERIMENTS = ROOT / "docs" / "experiments"
REPRODUCTIONS = (
    "glorank", "dual-rerank", "oneranker", "radar", "dualgr", "mpformer",
    "hap", "onepiece", "intsr", "cdm", "cwm", "rope", "alibi", "gqa",
    "hymba", "moba", "blt", "doremi", "data-mixing-laws",
)
POST = (
    "rlaif", "process-supervision", "math-shepherd", "self-rewarding",
    "luffy", "ttrl", "absolute-zero", "intuitor", "cispo", "spiral",
    "conspo",
)
AGENT = (
    "deepresearcher", "retool", "toolrl", "sage", "memskill",
    "memento-skills", "searl", "agent0",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--section", choices=("all", "reproductions", "post-training", "agent"),
        default="all",
    )
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    os.environ.setdefault("AUTO_RESEARCH_LLM_P0_STEPS", "12")
    payload = {"batch": "2026-08-08-global-theme-gap-review-p0", "seed": 42,
               "post_training": {}, "agent": {}}
    scratch = ROOT / "runs" / "20260808-global-p0"
    if args.section in {"all", "reproductions"}:
        for key in REPRODUCTIONS:
            adapter = get_adapter(key)
            target = ROOT / "docs" / "reproductions" / f"{adapter.paper.arxiv_id}-{key}" / "metrics"
            artifact = target / "public-seed42.json"
            if artifact.exists() and not args.force:
                continue
            result = adapter.run(DATA, 42)
            target.mkdir(parents=True, exist_ok=True)
            artifact.write_text(
                json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
    if args.section in {"all", "post-training"}:
        for algorithm in POST:
            result, _ = PostTrainingRunner(PostTrainingConfig(
                algorithm=algorithm, steps=120, maximum_examples=256, seed=42,
                output_dir=scratch / "post-training",
            )).run()
            payload["post_training"][algorithm] = {
                "baseline": result.baseline, "final": result.final,
                "relative_accuracy": result.relative_accuracy,
                "diagnostics": result.training["last_diagnostics"],
            }
    if args.section in {"all", "agent"}:
        for method in AGENT:
            result, _ = AgentResearchRunner(AgentResearchConfig(
                method=method, benchmark="planbench-mini", episodes=120,
                memory_size=24, seed=42, output_dir=scratch / "agent",
            )).run()
            payload["agent"][method] = {
                "metrics": result.metrics,
                "diagnostics": {
                    key: value for key, value in result.diagnostics.items()
                    if value and key != "fidelity"
                },
            }
    EXPERIMENTS.mkdir(parents=True, exist_ok=True)
    artifact = EXPERIMENTS / "global-p0-20260808-seed42.json"
    existing = json.loads(artifact.read_text(encoding="utf-8")) if artifact.exists() else {}
    for section in ("post_training", "agent"):
        existing.setdefault(section, {}).update(payload[section])
    existing.update({"batch": payload["batch"], "seed": payload["seed"]})
    artifact.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
