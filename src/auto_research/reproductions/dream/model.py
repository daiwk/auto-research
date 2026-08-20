from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from ..industrial_2026 import IndustrialData, base_scores


@dataclass(frozen=True)
class HierarchicalIntent:
    physical: dict[str, float | int]
    demand: dict[str, float | int]
    preference: dict[str, float | int]
    signature: str
    send_to_cloud: bool


@dataclass(frozen=True)
class StrategyBundle:
    relevance: int = 0
    affinity: int = 0
    novelty: int = 0
    exploration: int = 0
    scatter: int = 0
    fatigue: int = 0

    def validate(self) -> None:
        for name, value in self.__dict__.items():
            if not isinstance(value, int) or value < -2 or value > 2:
                raise ValueError(f"{name} must be an integer in [-2, 2]")


@dataclass
class StrategyMemory:
    conclusions: dict[str, StrategyBundle] = field(default_factory=dict)
    accepted: int = 0
    rejected: int = 0

    def deposit(self, signature: str, bundle: StrategyBundle, delta: float) -> None:
        if delta > 0:
            self.conclusions[signature] = bundle
            self.accepted += 1
        else:
            self.rejected += 1

    def retrieve(self, signature: str) -> StrategyBundle:
        return self.conclusions.get(signature, self.conclusions.get("global", StrategyBundle()))


def infer_intent(data: IndustrialData, history) -> HierarchicalIntent:
    recent = np.asarray(history[-12:], dtype=np.int64)
    domains = data.domains[recent]
    counts = np.bincount(domains, minlength=int(data.domains.max()) + 1)
    dominant = int(counts.argmax())
    concentration = float(counts.max() / len(recent))
    mean_popularity = float(data.popularity[recent].mean())
    transitions = [data.transition[left, right] for left, right in zip(recent, recent[1:])]
    continuity = float(np.mean(transitions)) if transitions else 0.0
    exploration = float(1.0 - concentration)
    send_to_cloud = bool(exploration > 0.42 or mean_popularity < 0.35 or continuity < 0.002)
    band = "explore" if exploration > 0.42 else "focused"
    return HierarchicalIntent(
        physical={"history_length": len(history), "last_domain": int(domains[-1])},
        demand={"dominant_domain": dominant, "continuity": continuity},
        preference={"exploration": exploration, "mean_popularity": mean_popularity},
        signature=f"domain-{dominant}:{band}", send_to_cloud=send_to_cloud,
    )


def _bounded(value: np.ndarray) -> np.ndarray:
    minimum, maximum = float(value.min()), float(value.max())
    return 2.0 * (value - minimum) / max(maximum - minimum, 1e-12) - 1.0


def compile_strategy(
    data: IndustrialData, history, intent: HierarchicalIntent, bundle: StrategyBundle,
) -> tuple[np.ndarray, dict[str, object]]:
    """M3: validate and deterministically compile a typed strategy bundle."""
    bundle.validate()
    baseline = base_scores(data, history)
    recent = tuple(history[-8:])
    affinity = (data.domains == intent.demand["dominant_domain"]).astype(np.float64)
    novelty = -_bounded(data.popularity)
    similarity = _bounded(np.mean(data.cosine[list(recent)], axis=0))
    signals = (similarity, affinity, novelty)
    levels = (bundle.relevance, bundle.affinity, bundle.novelty)
    score = np.maximum(baseline, 1e-12).copy()
    # Equation 4 in the paper: bounded semantic levels compile to multiplicative deltas.
    for signal, level in zip(signals, levels):
        delta = 0.10 * level
        score *= np.maximum(1.0 + delta * signal, 0.20)
    rng_key = np.sin(np.arange(data.item_count) * 12.9898 + len(history) * 78.233)
    score *= np.maximum(1.0 + 0.025 * bundle.exploration * rng_key, 0.70)
    if bundle.fatigue > 0:
        score[list(set(history[-min(4 + bundle.fatigue, len(history)):]))] *= 0.05

    # Equation 5 category scatter is list-level, so compile it into a stable full ranking.
    order = np.argsort(-score)
    max_per_domain = data.item_count if bundle.scatter <= 0 else max(1, 4 - bundle.scatter)
    counts: dict[int, int] = {}
    accepted, deferred = [], []
    for item in order:
        domain = int(data.domains[item])
        if counts.get(domain, 0) < max_per_domain:
            accepted.append(int(item)); counts[domain] = counts.get(domain, 0) + 1
        else:
            deferred.append(int(item))
    ranking = accepted + deferred
    compiled = np.empty(data.item_count, dtype=np.float64)
    compiled[ranking] = np.linspace(1.0, 0.0, data.item_count, endpoint=False)
    return compiled, {
        "schema_valid": True, "allowlisted_fields": tuple(bundle.__dict__),
        "max_per_domain": max_per_domain, "cloud_triggered": intent.send_to_cloud,
    }


def candidate_bundles(center: StrategyBundle | None = None) -> tuple[StrategyBundle, ...]:
    base = center or StrategyBundle()
    rows = [base]
    for field_name in base.__dict__:
        for delta in (-1, 1):
            values = dict(base.__dict__)
            values[field_name] = int(np.clip(values[field_name] + delta, -2, 2))
            rows.append(StrategyBundle(**values))
    return tuple(dict.fromkeys(rows))
