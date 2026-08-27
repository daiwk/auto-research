#!/usr/bin/env python3
"""Regenerate committed three-seed Agent L2 no-oracle evidence."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auto_research.agent_research.capability_runner import (  # noqa: E402
    CapabilitySuiteConfig,
    run_capability_suite,
)


SEEDS = (42, 43, 44)
EPISODES = 60
ARTIFACTS = {
    "long-context": "docs/agent-research/metrics/toolroute-l2-long-context-seeds42-44.json",
    "react": "docs/agent-research/2210.03629-react/metrics/toolroute-l2-seeds42-44.json",
    "reflexion": "docs/agent-research/2303.11366-reflexion/metrics/toolroute-l2-seeds42-44.json",
    "agent-g2": "docs/agent-research/2608.23318-agent-g2/metrics/toolroute-l2-seeds42-44.json",
    "ahead": "docs/agent-research/2608.24114-ahead/metrics/toolroute-l2-seeds42-44.json",
    "auso": "docs/agent-research/2608.21292-auso/metrics/toolroute-l2-seeds42-44.json",
}


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        results = run_capability_suite(CapabilitySuiteConfig(
            methods=tuple(ARTIFACTS),
            seeds=SEEDS,
            episodes=EPISODES,
            output_dir=Path(directory),
        ))
    summary = {
        "schema_version": 2,
        "manifest_ref": "experiments:agent-toolroute-l2-seeds42-44",
        "benchmark": "toolroute-l2-v1",
        "seeds": list(SEEDS),
        "episodes_per_seed": EPISODES,
        "oracle_fields_exposed": False,
        "results": {},
        "evaluation_protocol": {
            "tier": "l2_capability",
            "seeds": list(SEEDS),
            "formal_comparison": True,
            "claim_policy": (
                "shared no-oracle benchmark; compare only within toolroute-l2-v1"
            ),
        },
    }
    for method, relative in ARTIFACTS.items():
        payload = results[method]
        payload["manifest_ref"] = f"agent-research:{method}:toolroute-l2-v1"
        payload["provenance"]["artifact_path"] = relative
        payload["provenance"]["original_code_commit"] = "generated from repository source"
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        summary["results"][method] = {
            "metrics": payload["metrics"],
            "aggregate_metrics": payload["aggregate_metrics"],
            "artifact_path": relative,
        }
    summary_path = ROOT / "docs/experiments/agent-toolroute-l2-seeds42-44.json"
    summary["provenance"] = {
        "artifact_path": str(summary_path.relative_to(ROOT)),
        "dataset_fingerprint": next(iter(results.values()))["provenance"][
            "dataset_fingerprint"
        ],
        "original_code_commit": "generated from repository source",
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {len(ARTIFACTS)} L2 artifacts and {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
