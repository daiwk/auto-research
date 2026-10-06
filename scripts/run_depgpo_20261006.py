#!/usr/bin/env python3
"""Deterministic recorded-trace diagnostic for DepGPO (no policy training)."""

import json
from pathlib import Path

from auto_research.agent_research.depgpo import CommandTrace, assign_dependency_credit


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/agent-research/2610.03634-depgpo/metrics/trace-mechanism.json"


def main() -> None:
    # A read supplies a staging write, which is then consumed by the final answer write.
    trace = [
        CommandTrace("inspect", 0),
        CommandTrace("stage", 1, written_records=(("/work/staging", 1),),
                     stdout_source_ids=("inspect",)),
        CommandTrace("answer", 2, read_files=("/work/staging",),
                     written_records=(("/work/answer", 1),)),
        CommandTrace("irrelevant", 3, written_records=(("/work/debug", 1),)),
    ]
    result = assign_dependency_credit(
        trace, verifier_files={"/work/answer"}, token_counts=(3, 2, 4, 1),
        group_advantage=-0.8,
    )
    payload = {
        "schema_version": 2,
        "paper": "2610.03634",
        "tier": "L1",
        "diagnostic_only": True,
        "device": "cpu",
        "dataset": "hand-authored recorded terminal trace",
        "seed": 42,
        "seed_note": "deterministic trace; RNG not used",
        "manifest_ref": "agent-research:depgpo",
        "protocol": "paper Eqs. 10-21 on structured read/write and stdout dependency records; no terminal tracing or policy training",
        "evaluation_protocol": {
            "tier": "l1_mechanism", "seeds": [42],
            "formal_comparison": False,
            "claim_policy": "trace arithmetic only; not Terminal-Bench or model performance",
        },
        "provenance": {
            "artifact_path": str(OUTPUT.relative_to(ROOT)),
            "dataset_fingerprint": "four-command-structured-trace-v1",
        },
        "metrics": {
            "supporting_read_credit": result.command_credit["inspect"],
            "indirect_write_credit": result.command_credit["stage"],
            "irrelevant_write_credit": result.command_credit["irrelevant"],
            "token_weighted_mean_advantage": sum(
                count * advantage for count, advantage in zip(
                    (3, 2, 4, 1), result.redistributed_advantage
                )
            ) / 10,
        },
        "step_factors": result.step_factor,
        "token_weights": result.token_weight,
        "fallback": result.fallback,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
