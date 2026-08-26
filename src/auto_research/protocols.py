"""Versioned, machine-checkable fair-evaluation protocols."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class BenchmarkProtocol:
    protocol_id: str
    domain: str
    dataset: str
    data_revision: str
    split_policy: str
    candidate_policy: str
    reference_baseline: str
    primary_metric: str
    maximize: bool
    seeds: tuple[int, ...]
    budget: str
    required_metrics: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["seeds"] = list(self.seeds)
        payload["required_metrics"] = list(self.required_metrics)
        return payload


_PROTOCOLS = {
    item.protocol_id: item for item in (
        BenchmarkProtocol("recommendation.movielens1m.v2", "recommendation", "movielens-1m",
                          "ml-1m@official", "leave-one-out/latest", "full-catalog",
                          "din", "ndcg_at_10", True, (42, 43, 44), "standard-300-steps",
                          ("ndcg_at_10", "hit_at_10")),
        BenchmarkProtocol("foundation.wikitext2.v1", "foundation-model", "wikitext-2",
                          "wikitext-2-raw-v1", "official train/validation/test", "all tokens",
                          "micro-transformer", "perplexity", False, (42, 43, 44), "matched-tokens",
                          ("perplexity", "tokens_per_second")),
        BenchmarkProtocol("post_training.gsm8k.v1", "post-training", "gsm8k",
                          "gsm8k@main", "official train/test", "fixed candidate set",
                          "sft", "accuracy", True, (42, 43, 44), "matched-rollouts",
                          ("accuracy", "kl_from_reference")),
        BenchmarkProtocol("agent.swe_local.v2", "agent", "swe-local",
                          "repository-lock-v2", "fixed deterministic episodes", "fixed tools",
                          "direct-agent", "joint_success", True, (42, 43, 44), "matched-episodes",
                          ("joint_success", "average_cost")),
        BenchmarkProtocol("multimodal.scienceqa.v1", "multimodal", "scienceqa",
                          "scienceqa@official", "official test", "all answer choices",
                          "checkpoint-direct", "accuracy", True, (42,), "full-test",
                          ("accuracy", "standard_error")),
    )
}


def list_protocols() -> tuple[BenchmarkProtocol, ...]:
    return tuple(_PROTOCOLS[key] for key in sorted(_PROTOCOLS))


def get_protocol(protocol_id: str) -> BenchmarkProtocol:
    try:
        return _PROTOCOLS[protocol_id]
    except KeyError as exc:
        raise ValueError(f"unknown evaluation protocol: {protocol_id}") from exc


def validate_result(protocol_id: str, result: dict[str, Any]) -> list[str]:
    protocol = get_protocol(protocol_id)
    metrics = result.get("metrics", result)
    errors = [f"missing required metric: {name}" for name in protocol.required_metrics
              if name not in metrics]
    recorded = result.get("protocol_id")
    if recorded and recorded != protocol_id:
        errors.append(f"result declares protocol {recorded}, expected {protocol_id}")
    return errors


def comparability_errors(left: dict[str, Any], right: dict[str, Any]) -> list[str]:
    errors = []
    for key in ("protocol_id", "data_revision", "split_policy", "candidate_policy",
                "reference_baseline", "budget"):
        if left.get(key) != right.get(key):
            errors.append(f"{key} differs: {left.get(key)!r} != {right.get(key)!r}")
    return errors


def protocol_record(protocol_id: str) -> dict[str, Any]:
    return get_protocol(protocol_id).to_dict()
