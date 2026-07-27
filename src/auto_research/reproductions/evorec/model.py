from __future__ import annotations

import numpy as np

from ..industrial_2026 import evaluate


def evolve_skills(data, generations: int = 3):
    components = {
        "transition": lambda h: data.transition[list(h[-4:])].mean(0),
        "content": lambda h: data.cosine[list(h[-8:])].mean(0),
        "popularity": lambda h: data.popularity,
    }
    weights = np.array([0.45, 0.40, 0.15])
    memory = []
    for generation in range(generations):
        trials = []
        for index in range(3):
            candidate = weights.copy()
            candidate[index] += 0.15
            candidate /= candidate.sum()
            scorer = lambda h, w=candidate: sum(
                w[j] * fn(h) for j, fn in enumerate(components.values())
            )
            metrics = evaluate(data, scorer, target_split="validation")
            score = metrics["ndcg_at_10"] + 0.25 * metrics["hit_at_10"]
            trials.append((score, candidate, metrics, tuple(components)[index]))
        winner = max(trials, key=lambda item: item[0])
        weights = winner[1]
        memory.append({
            "generation": generation + 1,
            "learned_skill": winner[3],
            "weights": weights.tolist(),
            "validation": winner[2],
        })
    scorer = lambda h: sum(weights[j] * fn(h) for j, fn in enumerate(components.values()))
    return scorer, {"skill_memory": memory, "final_component_weights": dict(zip(components, weights.tolist()))}
