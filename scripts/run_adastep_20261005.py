#!/usr/bin/env python3
"""Three-seed synthetic return-statistic diagnostic for AdaStep."""

import json
from pathlib import Path

import numpy as np

from auto_research.agent_research.adastep import StepObservation, assign_step_credit


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/agent-research/2610.03223-adastep/metrics/variance-seeds42-44.json"


def run(seed: int) -> dict:
    rng = np.random.default_rng(seed)
    rows = [
        StepObservation("synthetic-task", "signal", action, float(mean + rng.normal(0, 0.1)), 0.25)
        for action, mean in (("a", 0.0), ("b", 1.0))
        for _ in range(16)
    ]
    rows.extend(
        StepObservation("synthetic-task", "noise", action, float(rng.normal(0, 1)), 0.25)
        for action in ("a", "b") for _ in range(16)
    )
    credits = assign_step_credit(rows)
    return {
        "seed": seed,
        "signal_coefficient": credits[0].coefficient,
        "noise_coefficient": credits[-1].coefficient,
        "all_finite": all(np.isfinite(item.combined_advantage) for item in credits),
    }


def main() -> None:
    results = [run(seed) for seed in (42, 43, 44)]
    payload = {
        "schema_version": 2,
        "paper": "2610.03223",
        "tier": "L1",
        "diagnostic_only": True,
        "device": "cpu",
        "dataset": "synthetic action-conditioned return groups",
        "manifest_ref": "agent-research:adastep",
        "protocol": "Eq. 17-18 variance decomposition with N/n_a population denominators and paper sparse-group fallback; no policy training",
        "seeds": [42, 43, 44],
        "evaluation_protocol": {
            "tier": "l1_mechanism", "seeds": [42, 43, 44],
            "formal_comparison": False,
            "claim_policy": "coefficient arithmetic diagnostic only; no ALFWorld/WebShop/ScienceWorld comparison",
        },
        "provenance": {
            "artifact_path": str(OUTPUT.relative_to(ROOT)),
            "dataset_fingerprint": "synthetic-action-returns-rng-seeds42-44",
        },
        "metrics": {
            "signal_coefficient_mean": sum(result["signal_coefficient"] for result in results) / 3,
            "noise_coefficient_mean": sum(result["noise_coefficient"] for result in results) / 3,
        },
        "results": results,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
