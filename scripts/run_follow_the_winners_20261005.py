#!/usr/bin/env python3
"""Rebuild the FTW CPU bandit L1 receipt; no Qwen/agent result is claimed."""

import json
from pathlib import Path

from auto_research.post_training.follow_the_winners import run_bandit


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/post-training/2610.03361-follow-the-winners/metrics/bandit-seeds42-44.json"


def main() -> None:
    results = [run_bandit(seed) for seed in (42, 43, 44)]
    payload = {
        "schema_version": 2,
        "paper": "2610.03361",
        "tier": "L1",
        "diagnostic_only": True,
        "device": "cpu",
        "dataset": "synthetic two-arm continuous-reward bandit",
        "manifest_ref": "post-training:follow-the-winners",
        "protocol": "FIFO replay, C=5, K=1, J=4, KL=0.05, SGD; identical fixed configuration across seeds; no hyperparameter search or held-out task result",
        "seeds": [42, 43, 44],
        "evaluation_protocol": {
            "tier": "l1_mechanism", "seeds": [42, 43, 44],
            "formal_comparison": False,
            "claim_policy": "mechanism execution only; no LLM, Sokoban, Search-R1 or paper-result reproduction claim",
        },
        "provenance": {
            "artifact_path": str(OUTPUT.relative_to(ROOT)),
            "dataset_fingerprint": "synthetic-two-arm-rng-seeds42-44",
        },
        "metrics": {
            "best_action_probability_final_mean": sum(float(item["best_action_probability_final"]) for item in results) / 3,
            "expected_reward_final_mean": sum(float(item["expected_reward_final"]) for item in results) / 3,
        },
        "results": results,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
