from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from auto_research.recommendation_latest_20261001 import cohortmix_prior, cohortmix_slate, cohortmix_update


def reproduce(_dataset_dir: Path, seed: int = 42) -> dict:
    membership = np.array([.75, .25])
    success = np.array([[8, 2, 5, 1], [1, 7, 2, 5]], dtype=float)
    failure = np.array([[2, 8, 5, 9], [9, 3, 8, 5]], dtype=float)
    alpha, beta = cohortmix_prior(membership, success, failure, alpha0=1, beta0=1, strength=10)
    chosen, draws = cohortmix_slate(alpha, beta, size=2, seed=seed)
    updated_alpha, updated_beta = cohortmix_update(alpha, beta, chosen, [1, 0])
    return {
        "paper": {"arxiv_id": "2609.37800", "url": "https://arxiv.org/abs/2609.37800"},
        "dataset": "deterministic public cross-cohort bandit fixture",
        "setup": {"seed": seed, "groups": 2, "arms": 4, "slate_size": 2},
        "baseline": {"name": "uninformative Beta(1,1) Thompson sampling", "prior_mean": .5},
        "method": {
            "name": "metadata-conditioned fixed-strength mixture prior",
            "prior_mean": float((alpha / (alpha + beta)).mean()),
            "selected_slate": list(chosen),
            "maximum_draw": float(draws.max()),
            "posterior_mass": float((updated_alpha + updated_beta).sum()),
        },
        "scope": "执行 mixture Beta warm start、Thompson slate 和用户后验更新；未复刻矩阵分解和真实部署。",
    }


def render(result: dict) -> str:
    return "# CohortMix-TS\n\n```json\n" + json.dumps(result, ensure_ascii=False, indent=2) + "\n```\n"
