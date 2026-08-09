"""Run the 2026-08-09 P0/P1 audit batch and persist reviewable metrics."""

from __future__ import annotations

import json
from pathlib import Path

from auto_research.agent_research.models import AgentResearchConfig
from auto_research.agent_research.runner import AgentResearchRunner
from auto_research.post_training.models import PostTrainingConfig
from auto_research.post_training.runner import PostTrainingRunner
from auto_research.reproductions.registry import get_adapter


ROOT = Path(__file__).resolve().parents[2]
REPRODUCTIONS = {
    "kgd": "2608.02738-kgd", "twitch-mor": "2608.04455-twitch-mor",
    "hrpo": "2608.00750-hrpo", "llm-ts-prior": "2608.03382-llm-ts-prior",
    "macro": "2608.05872-macro", "hilp": "2608.05806-hilp",
    "qevict": "2608.05326-qevict", "bakron": "2608.06291-bakron",
    "dblast": "2608.05448-dblast",
}
POST = {
    "rrc": "2608.06310-rrc",
    "rail": "2608.05080-rail",
    "specroll": "2608.04962-specroll",
}
AGENT = {
    "evoharness-rl": "2608.05446-evoharness-rl",
    "vag": "2608.05810-vag",
    "gse": "2608.06153-gse",
    "cipo": "2608.06128-cipo",
    "state2state": "2608.04934-state2state",
    "harnessopt-bench": "2608.06301-harnessopt-bench",
    "codegrep": "2608.05886-codegrep",
    "memorycpt": "2608.04843-memorycpt",
    "hindsearch": "2608.01597-hindsearch",
}


def write_metric(path: Path, payload: dict, manifest_ref: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        **payload,
        "schema_version": 2,
        "manifest_ref": manifest_ref,
        "evaluation_protocol": {
            "tier": "l1_mechanism",
            "seeds": [42],
            "formal_comparison": False,
            "claim_policy": "single-seed smoke result; do not claim a stable improvement",
        },
        "provenance": {
            "artifact_path": str(path.relative_to(ROOT)),
            "original_code_commit": "working tree",
            "dataset_fingerprint": "deterministic built-in mini-suite",
        },
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def main() -> None:
    for key, slug in REPRODUCTIONS.items():
        payload = get_adapter(key).run(ROOT / "data", 42)
        target = ROOT / "docs" / "reproductions" / slug / "metrics" / "public-seed42.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")

    for key, slug in POST.items():
        result, _ = PostTrainingRunner(PostTrainingConfig(
            key, steps=120, maximum_examples=256, allow_network=False,
            output_dir=ROOT / "runs" / "post-training",
        )).run()
        payload = {
            "algorithm": key,
            "seed": 42,
            "dataset": result.dataset, "baseline": result.baseline,
            "final": result.final, "relative_accuracy": result.relative_accuracy,
            "training": result.training,
        }
        write_metric(
            ROOT / "docs" / "post-training" / slug / "metrics" / "arithmetic-smoke-seed42.json",
            payload,
            f"post-training:{key}",
        )
    for key, slug in AGENT.items():
        result, _ = AgentResearchRunner(AgentResearchConfig(
            key, benchmark="planbench-mini", episodes=120,
            output_dir=ROOT / "runs" / "agent-research",
        )).run()
        payload = {
            "method": key,
            "seed": 42,
            "episodes": 120,
            "benchmark": result.benchmark, "metrics": result.metrics,
            "axis_metrics": result.axis_metrics, "diagnostics": result.diagnostics,
        }
        write_metric(
            ROOT / "docs" / "agent-research" / slug / "metrics" / "planbench-mini-seed42.json",
            payload,
            f"agent-research:{key}",
        )


if __name__ == "__main__":
    main()
