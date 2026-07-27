from __future__ import annotations

import numpy as np


def _ridge(features, target, weight=None, regularization=1e-2):
    if weight is None:
        weight = np.ones(len(features))
    weighted = features * np.sqrt(weight)[:, None]
    response = target * np.sqrt(weight)
    return np.linalg.solve(
        weighted.T @ weighted + regularization * np.eye(features.shape[1]),
        weighted.T @ response,
    )


def build_causal_retrieval_scorer(data):
    """Doubly robust uplift model for deciding whether to trigger shopping."""
    rows, treatment, outcome = [], [], []
    rng = np.random.default_rng(202607)
    for sequence in data.sequences.train:
        for end in range(2, len(sequence)):
            recent = np.asarray(sequence[max(0, end - 8):end])
            x = data.sequences.features[recent].mean(0)
            target = sequence[end]
            propensity = 0.25 + 0.5 * float(data.popularity[target])
            treated = rng.random() < propensity
            reward = float(
                data.domains[target] == data.domains[recent[-1]]
            )
            reward += treated * float(data.popularity[target] < 0.45) * 0.35
            rows.append(x)
            treatment.append(float(treated))
            outcome.append(reward)
    x = np.asarray(rows)
    treatment = np.asarray(treatment)
    outcome = np.asarray(outcome)
    propensity = np.clip(x @ _ridge(x, treatment), 0.05, 0.95)
    mu0 = x @ _ridge(x[treatment == 0], outcome[treatment == 0])
    mu1 = x @ _ridge(x[treatment == 1], outcome[treatment == 1])
    pseudo = (
        mu1 - mu0
        + treatment * (outcome - mu1) / propensity
        - (1 - treatment) * (outcome - mu0) / (1 - propensity)
    )
    uplift_weight = _ridge(x, pseudo)
    predicted_uplift = x @ uplift_weight
    trigger_threshold = float(np.quantile(predicted_uplift, 0.70))

    def scorer(history):
        recent = np.asarray(history[-8:])
        context = data.sequences.features[recent].mean(0)
        uplift = float(context @ uplift_weight)
        trigger = float(uplift > trigger_threshold)
        shopping = data.cosine[recent[-1]] * (
            data.domains == data.domains[recent[-1]]
        )
        return data.transition[recent].mean(0) + trigger * shopping

    return scorer, {
        "training_examples": len(x),
        "doubly_robust": True,
        "estimated_trigger_rate": float(
            np.mean(predicted_uplift > trigger_threshold)
        ),
        "trigger_threshold": trigger_threshold,
        "pseudo_outcome_std": float(pseudo.std()),
    }
