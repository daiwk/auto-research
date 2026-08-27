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
from auto_research.agent_research.capability_methods import (  # noqa: E402
    CAPABILITY_ABLATIONS,
)
from auto_research.evolution.engine import ModelEvolutionEngine  # noqa: E402
from auto_research.evolution.models import EvolutionConfig  # noqa: E402


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
EVOLVE_ARTIFACT = (
    "docs/agent-research/metrics/toolroute-l21-evolve-seeds42-44.json"
)


def _generate_evolve_artifact(directory: str) -> dict:
    result, _ = ModelEvolutionEngine(EvolutionConfig(
        model="agent",
        dataset="toolroute-l2.1",
        direction=(
            "组合 memory、planner、tool、critic、policy、recovery、reflection、"
            "verifier 与 context compression"
        ),
        output_dir=Path(directory) / "evolve",
        generations=3,
        population=9,
        seeds=SEEDS,
        workers=3,
        steps=1,
        agent_episodes=EPISODES,
        allow_network=False,
        negative_memory_path=Path(directory) / "negative-results.json",
    ), project_dir=ROOT).run()
    champion = next(
        trial for trial in result.trials if trial.trial_id == result.champion_id
    )
    metrics = {
        key: float(value)
        for key, value in (result.champion_test or {}).items()
        if isinstance(value, (int, float))
    }
    baseline = {
        key: float(value)
        for key, value in (result.baseline_test or {}).items()
        if isinstance(value, (int, float))
    }
    payload = {
        "schema_version": 2,
        "manifest_ref": "agent-research:agent-evolve:toolroute-l2.1-v1",
        "method": "agent-evolve",
        "benchmark": "toolroute-l2.1",
        "dataset": "toolroute-l2.1-v1",
        "seeds": list(SEEDS),
        "metrics": metrics,
        "baseline_metrics": baseline,
        "diagnostics": {
            "fidelity": "held-out no-guide multi-generation capability evolution",
            "oracle_fields_exposed": False,
            "guide_endpoint": "absent",
            "generations": 3,
            "population": 9,
            "workers": 3,
            "episodes_per_split": EPISODES,
            "trials": len(result.trials),
            "champion_id": result.champion_id,
            "champion_genome": champion.genome.to_dict(),
            "lineage": [
                {
                    "trial_id": trial.trial_id,
                    "generation": trial.generation,
                    "parent_id": trial.parent_id,
                    "source": (
                        "baseline" if trial.generation == 0 else
                        "implemented-paper-operator" if trial.source_papers else
                        "whitelisted-combination"
                    ),
                    "source_papers": list(trial.source_papers),
                    "rationale": trial.rationale,
                    "components": {
                        "memory": trial.genome.agent_memory,
                        "planner": trial.genome.agent_planner,
                        "tool": trial.genome.agent_tool_policy,
                        "critic": trial.genome.agent_critic,
                        "policy": trial.genome.agent_policy,
                        "recovery": trial.genome.agent_failure_recovery,
                        "reflection": trial.genome.agent_reflection,
                        "verifier": trial.genome.agent_verifier,
                        "context": trial.genome.agent_context_compression,
                    },
                    "validation": {
                        key: float(value)
                        for key, value in trial.validation.items()
                        if key in {
                            "fitness", "joint_success", "plan_step_f1",
                            "recovery_rate", "invalid_tool_rate", "average_cost",
                        }
                    },
                }
                for trial in result.trials
            ],
            "rounds": result.rounds,
        },
        "evaluation_protocol": {
            "tier": "l2_capability",
            "seeds": list(SEEDS),
            "formal_comparison": True,
            "claim_policy": (
                "validation selects the champion; isolated test runs once after all generations"
            ),
        },
        "provenance": {
            "artifact_path": EVOLVE_ARTIFACT,
            "dataset_fingerprint": next(iter(result.trials)).training.get(
                "dataset_fingerprint", "toolroute-l2.1 deterministic generator"
            ),
            "original_code_commit": "generated from repository source",
        },
    }
    path = ROOT / EVOLVE_ARTIFACT
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    return payload


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        results = run_capability_suite(CapabilitySuiteConfig(
            methods=(*tuple(ARTIFACTS), *CAPABILITY_ABLATIONS),
            seeds=SEEDS,
            episodes=EPISODES,
            output_dir=Path(directory),
        ))
        evolve = _generate_evolve_artifact(directory)
    summary = {
        "schema_version": 2,
        "manifest_ref": "experiments:agent-toolroute-l2.1-seeds42-44",
        "benchmark": "toolroute-l2.1-v1",
        "seeds": list(SEEDS),
        "episodes_per_seed": EPISODES,
        "oracle_fields_exposed": False,
        "guide_endpoint": "absent",
        "results": {},
        "ablations": {},
        "evolve_artifact": EVOLVE_ARTIFACT,
        "evaluation_protocol": {
            "tier": "l2_capability",
            "seeds": list(SEEDS),
            "formal_comparison": True,
            "claim_policy": (
                "held-out no-guide test; compare only within toolroute-l2.1-v1"
            ),
        },
    }
    for method, relative in ARTIFACTS.items():
        payload = results[method]
        payload["manifest_ref"] = f"agent-research:{method}:toolroute-l2.1-v1"
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
    for method in CAPABILITY_ABLATIONS:
        payload = results[method]
        summary["ablations"][method] = {
            "metrics": payload["metrics"],
            "validation_metrics": payload["validation_metrics"],
        }
    summary_path = ROOT / "docs/experiments/agent-toolroute-l2-seeds42-44.json"
    summary["provenance"] = {
        "artifact_path": str(summary_path.relative_to(ROOT)),
        "dataset_fingerprint": next(iter(results.values()))["provenance"][
            "dataset_fingerprint"
        ],
        "original_code_commit": "generated from repository source",
    }
    summary["evolve_champion"] = {
        "metrics": evolve["metrics"],
        "champion_id": evolve["diagnostics"]["champion_id"],
        "champion_genome": evolve["diagnostics"]["champion_genome"],
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {len(ARTIFACTS)} L2 artifacts and {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
