from __future__ import annotations

import numpy as np

from ..industrial_2026 import ridge


def _sigmoid(values: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(values, -30, 30)))


def build_incrementality_problem(data, seed: int, budget_fraction: float = 0.30) -> dict:
    rng = np.random.default_rng(seed)
    features = []
    targets = []
    for history, target in zip(data.sequences.train, data.sequences.validation):
        context = data.sequences.features[np.asarray(history[-12:], dtype=np.int64)].mean(0)
        features.append(np.r_[1.0, context, data.popularity[target]])
        targets.append(target)
    x = np.asarray(features, dtype=np.float64)
    targets = np.asarray(targets, dtype=np.int64)

    propensity = _sigmoid(0.8 * x[:, 1] - 0.55 * x[:, -1] + 0.15)
    treatment = rng.binomial(1, propensity).astype(np.float64)
    baseline_outcome = _sigmoid(0.45 * x[:, 2] + 0.30 * x[:, -1] - 0.25)
    true_uplift = np.clip(
        0.04 + 0.22 * (1.0 - x[:, -1]) + 0.10 * np.maximum(x[:, 1], 0.0),
        0.0,
        0.45,
    )
    observed = np.clip(
        baseline_outcome + treatment * true_uplift + rng.normal(0.0, 0.035, len(x)),
        0.0,
        1.0,
    )
    treated = treatment > 0
    mu1 = x @ ridge(x[treated], observed[treated])
    mu0 = x @ ridge(x[~treated], observed[~treated])
    uplift = mu1 - mu0
    residual = observed - np.where(treated, mu1, mu0)
    uncertainty = np.sqrt(np.mean(residual**2)) * np.sqrt(np.sum(x**2, axis=1))
    incremental_score = uplift + 0.10 * uncertainty
    predictive_score = mu1
    budget = max(1, int(round(len(x) * budget_fraction)))
    return {
        "features": x,
        "targets": targets,
        "propensity": propensity,
        "treatment": treatment,
        "observed": observed,
        "true_uplift": true_uplift,
        "estimated_uplift": uplift,
        "incremental_score": incremental_score,
        "predictive_score": predictive_score,
        "budget": budget,
    }


def evaluate_policy(problem: dict, score_key: str) -> dict[str, float]:
    scores = np.asarray(problem[score_key])
    chosen = np.argsort(-scores)[: problem["budget"]]
    uplift = np.asarray(problem["true_uplift"])
    return {
        "policy_value": float(uplift[chosen].mean()),
        "total_incremental_value": float(uplift[chosen].sum()),
        "budget_fraction": float(len(chosen) / len(uplift)),
        "uplift_rank_correlation": float(
            np.corrcoef(scores, uplift)[0, 1] if np.std(scores) and np.std(uplift) else 0.0
        ),
    }
