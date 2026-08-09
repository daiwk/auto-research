from __future__ import annotations

import itertools
import numpy as np

from ..industrial_2026 import evaluate


def actor_critic_search(data, generations: int = 3):
    """Actor proposes recipes; critic evaluates; SkillHub carries the champion."""
    skills = [(0.50, 0.35, 0.15)]
    trace = []
    champion = skills[0]
    champion_score = float("-inf")
    for generation in range(generations):
        radius = 0.20 / (generation + 1)
        candidates = {champion}
        for delta_t, delta_c in itertools.product((-radius, 0.0, radius), repeat=2):
            t = np.clip(champion[0] + delta_t, 0.05, 0.85)
            c = np.clip(champion[1] + delta_c, 0.05, 0.85)
            p = max(0.05, 1.0 - t - c)
            total = t + c + p
            candidates.add((t / total, c / total, p / total))
        observations = []
        for weights in sorted(candidates):
            scorer = recipe_scorer(data, weights)
            metrics = evaluate(data, scorer, target_split="validation")
            value = metrics["ndcg_at_10"] + 0.25 * metrics["hit_at_10"] + 0.05 * metrics["fresh_hit_at_10"]
            observations.append({"weights": weights, "objective": value})
            if value > champion_score:
                champion, champion_score = weights, value
        skills.append(champion)
        trace.append({"generation": generation, "actor_candidates": len(candidates), "critic_observations": observations, "skillhub_champion": champion})
    return champion, trace


def recipe_scorer(data, weights):
    def score(history):
        recent = np.asarray(history[-8:], dtype=np.int64)
        transition = np.mean(data.transition[recent[-3:]], axis=0)
        content = np.mean(data.cosine[recent], axis=0)
        diversity = 1.0 - np.mean(data.cosine[recent], axis=0)
        return weights[0] * transition + weights[1] * content + weights[2] * diversity
    return score
