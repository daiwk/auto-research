"""Persistent exact-context memory for failed and non-improving experiments."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class NegativeResult:
    domain: str
    model: str
    dataset: str
    protocol_id: str
    method: str
    budget: str
    seeds: tuple[int, ...]
    category: str
    reason: str
    fitness_delta: float | None = None

    @property
    def context_key(self) -> str:
        payload = {key: value for key, value in asdict(self).items()
                   if key not in {"category", "reason", "fitness_delta"}}
        payload["seeds"] = list(self.seeds)
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:20]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self); payload["seeds"] = list(self.seeds)
        payload["context_key"] = self.context_key
        return payload


class NegativeResultStore:
    def __init__(self, path: Path):
        self.path = path

    def rows(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return list(json.loads(self.path.read_text(encoding="utf-8")).get("results", []))

    def record(self, result: NegativeResult) -> None:
        rows = [item for item in self.rows() if item.get("context_key") != result.context_key]
        rows.append(result.to_dict())
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(json.dumps({"schema_version": 1, "results": rows},
                                        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(self.path)

    def should_skip(self, *, domain, model, dataset, protocol_id, method, budget, seeds):
        probe = NegativeResult(domain, model, dataset, protocol_id, method, budget,
                               tuple(seeds), "probe", "probe")
        match = next((item for item in self.rows()
                      if item.get("context_key") == probe.context_key), None)
        if not match:
            return False, None
        permanent = match.get("category") in {"runtime_failure", "numerical_failure",
                                               "no_improvement", "objective_conflict"}
        return permanent, match


def classify_negative(*, status: str, error: str | None, fitness_delta: float | None):
    text = (error or "").lower()
    if status != "completed":
        return ("numerical_failure" if any(token in text for token in ("nan", "inf", "overflow"))
                else "runtime_failure")
    if fitness_delta is not None and fitness_delta <= 0:
        return "no_improvement"
    return "objective_conflict"
