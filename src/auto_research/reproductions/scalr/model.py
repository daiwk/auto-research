from __future__ import annotations

import numpy as np


def build_translation(data) -> dict:
    """Estimate P(target item | source event) from overlapping users."""
    domain_count = int(data.domains.max()) + 1
    counts = np.full((domain_count, data.item_count), 1e-3, dtype=np.float64)
    source_events = []
    for user, sequence in enumerate(data.sequences.train):
        target_items = np.asarray(sequence[1:], dtype=np.int64)
        for source in sequence[:-1]:
            counts[data.domains[source], target_items] += 1.0
            source_events.append((user, source))
    probabilities = counts / counts.sum(axis=1, keepdims=True)
    return {"probabilities": probabilities, "source_events": source_events}


def synthesize_events(data, state: dict, seed: int, samples_per_event: int = 2) -> dict:
    rng = np.random.default_rng(seed)
    sampled = np.full((data.item_count, data.item_count), 1e-3, dtype=np.float64)
    deterministic = np.full_like(sampled, 1e-3)
    sampled_items: list[int] = []
    deterministic_items: list[int] = []
    probabilities = state["probabilities"]
    for user, source in state["source_events"]:
        del user
        distribution = probabilities[data.domains[source]]
        drawn = rng.choice(data.item_count, size=samples_per_event, replace=True, p=distribution)
        top = np.argsort(-distribution)[:samples_per_event]
        sampled[source, drawn] += 1.0
        deterministic[source, top] += 1.0
        sampled_items.extend(drawn.tolist())
        deterministic_items.extend(top.tolist())
    sampled /= sampled.sum(axis=1, keepdims=True)
    deterministic /= deterministic.sum(axis=1, keepdims=True)
    return {
        "sampled": sampled,
        "deterministic": deterministic,
        "sampled_catalog_coverage": len(set(sampled_items)) / data.item_count,
        "deterministic_catalog_coverage": len(set(deterministic_items)) / data.item_count,
        "synthetic_events": len(sampled_items),
    }


def score_scalr(data, synthetic: dict, history, strategy: str = "sampled") -> np.ndarray:
    recent = np.asarray(history[-8:], dtype=np.int64)
    translated = synthetic[strategy][recent].mean(axis=0)
    content = data.cosine[recent].mean(axis=0)
    return 0.72 * translated + 0.20 * content + 0.08 * data.popularity
