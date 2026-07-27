from __future__ import annotations

import numpy as np

from ..industrial_2026 import softmax


def build_mdl_scorer(data):
    """Feature, scenario and task tokens with domain-feature attention."""
    features = data.sequences.features.astype(float)
    domain_count = int(data.domains.max()) + 1
    global_token = features.mean(0)
    domain_tokens = np.stack([
        (
            features[data.domains == domain].mean(0)
            if np.any(data.domains == domain)
            else global_token
        )
        for domain in range(domain_count)
    ])
    domain_attention = softmax(domain_tokens @ features.T, axis=-1)

    def scorer(history):
        recent = np.asarray(history[-12:])
        scenario = np.bincount(
            data.domains[recent], minlength=domain_count
        ).argmax()
        feature_token = features[recent].mean(0)
        self_attention = softmax(features @ feature_token)
        task_token = 0.5 * data.transition[recent].mean(0) + 0.5 * data.popularity
        return (
            0.40 * self_attention
            + 0.35 * domain_attention[scenario]
            + 0.25 * task_token
        )

    return scorer, {
        "feature_tokens": int(features.shape[1]),
        "scenario_tokens": domain_count,
        "task_tokens": 2,
        "domain_feature_attention": True,
    }
