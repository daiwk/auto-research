from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CheckpointEvidence:
    path: Path
    family: str
    method: str
    seeds: tuple[int, ...]
    applicable_models: tuple[str, ...]
    operator: str | None
    payload: dict[str, Any]


def load_checkpoint_evidence(paths: tuple[Path, ...]) -> tuple[CheckpointEvidence, ...]:
    return tuple(_parse(path) for path in paths)


def promoted_operators(
    records: tuple[CheckpointEvidence, ...], model: str,
) -> tuple[str, ...]:
    return tuple(dict.fromkeys(
        record.operator for record in records
        if model in record.applicable_models and record.operator is not None
    ))


def evidence_summary(records: tuple[CheckpointEvidence, ...]) -> list[dict[str, Any]]:
    return [
        {
            "artifact": str(record.path),
            "family": record.family,
            "method": record.method,
            "seeds": list(record.seeds),
            "operator": record.operator,
            "policy": (
                "proposal prior only; every genome is re-evaluated by the active "
                "Evolve evaluator and checkpoint metrics are never copied into fitness"
            ),
        }
        for record in records
    ]


def _parse(path: Path) -> CheckpointEvidence:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("method") == "mllmclip-real-checkpoint-cka":
        rows = payload.get("metrics", {}).get("seed_results", ())
        return _validated(
            path, "multimodal", "mllmclip-cka", rows,
            ("micro-vlm",), "micro_vlm_mlp", payload,
        )
    if payload.get("task") == "ag-001-agent-lightning-checkpoint-policy":
        return _validated(
            path, "agent", "agent-lightning", payload.get("seed_results", ()),
            ("agent",), "policy:agent-lightning", payload,
        )
    config = payload.get("config", {})
    if "objective" in config and "seed_results" in payload:
        objective = str(config["objective"])
        return _validated(
            path, "post-training", objective, payload["seed_results"],
            ("post-training",), objective, payload,
        )
    raise ValueError(f"unsupported checkpoint evidence artifact: {path}")


def _validated(path, family, method, rows, models, operator, payload):
    seeds = tuple(int(row["seed"]) for row in rows)
    if len(seeds) < 3 or len(set(seeds)) < 3:
        raise ValueError(
            f"checkpoint evidence requires three independent seeds: {path}"
        )
    return CheckpointEvidence(path, family, method, seeds, models, operator, payload)
