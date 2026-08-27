from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json

from .papers import (
    AGENT_MUTATIONS, INSTALLED_MUTATIONS, LLM_MUTATIONS, POST_TRAINING_MUTATIONS,
)


@dataclass(frozen=True)
class OperatorSpec:
    key: str
    domain: str
    slot: str
    paper_ids: tuple[str, ...]
    compatible_models: tuple[str, ...]
    requires: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()
    composable: bool = False
    compute_cost: int = 1
    memory_cost: int = 1
    latency_cost: int = 1

    def to_dict(self) -> dict:
        return asdict(self)


MODEL_DOMAIN = {
    "rankmixer": "recommendation", "hyformer": "recommendation",
    "genrec": "recommendation", "micro-llm": "foundation-model",
    "micro-vlm": "multimodal", "vlm-checkpoint": "multimodal",
    "reasoning-checkpoint": "foundation-model", "post-training": "post-training",
    "agent": "agent",
}


def _slot(operator: str, domain: str) -> str:
    if ":" in operator:
        return operator.split(":", 1)[0]
    if operator.startswith(("rankmixer_", "hyformer_")):
        return "architecture"
    if domain == "post-training":
        return "objective"
    if domain in {"foundation-model", "multimodal"}:
        return "architecture"
    return "mechanism"


def _models(operator: str, domain: str) -> tuple[str, ...]:
    if domain == "recommendation":
        if operator.startswith("hyformer"):
            return ("hyformer",)
        if operator.startswith("rankmixer"):
            return ("rankmixer",)
        if operator.startswith(("context:", "head:", "reward:", "distillation:")):
            return ("genrec",)
        return ("rankmixer", "hyformer", "genrec")
    if domain == "multimodal":
        return ("micro-vlm", "vlm-checkpoint")
    if domain == "foundation-model":
        return ("micro-llm", "reasoning-checkpoint")
    return (domain,)


def operator_registry() -> dict[str, OperatorSpec]:
    sources = (
        (INSTALLED_MUTATIONS, "recommendation"),
        (LLM_MUTATIONS, "foundation-model"),
        (POST_TRAINING_MUTATIONS, "post-training"),
        (AGENT_MUTATIONS, "agent"),
    )
    grouped: dict[tuple[str, str], list[str]] = {}
    for mapping, domain in sources:
        for paper_id, (operator, _) in mapping.items():
            operator_domain = domain
            if operator.startswith(("micro_vlm_", "checkpoint_vlm:")) or operator in {
                "objective:siglip2", "objective:gas-nep",
            }:
                operator_domain = "multimodal"
            grouped.setdefault((operator_domain, operator), []).append(paper_id)
    registry = {}
    for (domain, operator), paper_ids in grouped.items():
        slot = _slot(operator, domain)
        registry[operator] = OperatorSpec(
            key=operator, domain=domain, slot=slot,
            paper_ids=tuple(sorted(paper_ids)), compatible_models=_models(operator, domain),
            composable=slot in {
                "memory", "planner", "tool", "critic", "policy", "recovery",
                "reflection", "verifier", "context",
            },
            compute_cost=2 if any(term in operator for term in ("long", "moe", "rollout", "search")) else 1,
            memory_cost=2 if any(term in operator for term in ("memory", "long", "kv", "hstu")) else 1,
            latency_cost=2 if any(term in operator for term in ("agent", "search", "rollout", "planner")) else 1,
        )
    return registry


def describe_operator(operator: str, model: str | None = None) -> OperatorSpec:
    registry = operator_registry()
    if operator in registry:
        return registry[operator]
    domain = MODEL_DOMAIN.get(model or "", "general")
    return OperatorSpec(
        key=operator, domain=domain, slot=_slot(operator, domain), paper_ids=(),
        compatible_models=(model,) if model else (), composable=False,
    )


def validate_operator_set(
    model: str, operators: list[str] | tuple[str, ...], *,
    max_compute: int | None = None, max_memory: int | None = None,
    max_latency: int | None = None,
) -> list[str]:
    specs = [describe_operator(operator, model) for operator in operators]
    errors: list[str] = []
    for spec in specs:
        if spec.compatible_models and model not in spec.compatible_models:
            errors.append(f"{spec.key} is not compatible with {model}")
        missing = set(spec.requires) - set(operators)
        if missing:
            errors.append(f"{spec.key} requires {', '.join(sorted(missing))}")
        conflicts = set(spec.conflicts) & set(operators)
        if conflicts:
            errors.append(f"{spec.key} conflicts with {', '.join(sorted(conflicts))}")
    by_slot: dict[str, list[OperatorSpec]] = {}
    for spec in specs:
        by_slot.setdefault(spec.slot, []).append(spec)
    for slot, values in by_slot.items():
        if len(values) > 1 and not all(value.composable for value in values):
            errors.append(
                f"slot {slot} accepts one operator, got "
                + ", ".join(value.key for value in values)
            )
    totals = {
        "compute": sum(item.compute_cost for item in specs),
        "memory": sum(item.memory_cost for item in specs),
        "latency": sum(item.latency_cost for item in specs),
    }
    for name, maximum in (("compute", max_compute), ("memory", max_memory), ("latency", max_latency)):
        if maximum is not None and totals[name] > maximum:
            errors.append(f"{name} budget exceeded: {totals[name]} > {maximum}")
    return errors


def compatible_architectures(model: str, architectures: list[str]) -> list[str]:
    return [value for value in architectures if not validate_operator_set(model, [value])]


def write_compatibility_graph(path: Path) -> Path:
    registry = operator_registry()
    payload = {
        "schema_version": 1,
        "operators": [registry[key].to_dict() for key in sorted(registry)],
        "edges": [
            {"from": spec.key, "to": target, "type": edge_type}
            for spec in registry.values()
            for edge_type, targets in (("requires", spec.requires), ("conflicts", spec.conflicts))
            for target in targets
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return path
