from __future__ import annotations

import numpy as np

from ..industrial_2026 import base_scores, hierarchical_codes, ridge


def construct_qp_sid(data, seed: int):
    semantic = hierarchical_codes(data.sequences.features, levels=2, width=8, seed=seed)
    prefixes = semantic[:, 0] * 8 + semantic[:, 1]
    global_order = np.zeros(data.item_count, dtype=np.int64)
    query_order = np.zeros((int(data.domains.max()) + 1, data.item_count), dtype=np.int64)
    for prefix in np.unique(prefixes):
        members = np.flatnonzero(prefixes == prefix)
        ordered = members[np.argsort(-data.popularity[members])]
        global_order[ordered] = np.arange(len(ordered))
        for domain in range(query_order.shape[0]):
            domain_items = np.flatnonzero(data.domains == domain)
            relevance = data.cosine[members][:, domain_items].mean(1) if len(domain_items) else 0.0
            value = 0.65 * data.popularity[members] + 0.35 * relevance
            ranked = members[np.argsort(-value)]
            query_order[domain, ranked] = np.arange(len(ranked))
    return semantic, prefixes, global_order, query_order


def _features(data, prefixes, global_order, query_order, history):
    base = base_scores(data, history)
    recent = history[-1]
    query_domain = int(data.domains[recent])
    prefix_match = (prefixes == prefixes[recent]).astype(np.float64)
    value_code = 1.0 / (1.0 + global_order)
    query_code = 1.0 / (1.0 + query_order[query_domain])
    user = data.sequences.features[list(history[-8:])].mean(0)
    cross_attention = data.sequences.features @ user
    return np.stack([base, prefix_match, value_code, query_code, cross_attention, data.popularity], axis=1)


def train_vrm(data, prefixes, global_order, query_order, seed: int):
    rng = np.random.default_rng(seed)
    rows, labels, weights = [], [], []
    for sequence in data.sequences.train:
        for end in range(2, len(sequence)):
            history, positive = sequence[max(0, end - 8):end], sequence[end]
            features = _features(data, prefixes, global_order, query_order, history)
            negatives = rng.choice(data.item_count, 5, replace=False)
            rows.append(features[positive]); labels.append(1.0); weights.append(3.0)
            for negative in negatives:
                rows.append(features[negative]); labels.append(0.0); weights.append(1.0)
    matrix = np.asarray(rows)
    target = np.asarray(labels)
    scale = np.sqrt(np.asarray(weights))[:, None]
    coefficients = ridge(matrix * scale, target * scale[:, 0], regularization=0.05)
    return coefficients, {
        "weighted_multi_positive_examples": int(sum(label == 1.0 for label in labels)),
        "negative_examples": int(sum(label == 0.0 for label in labels)),
        "vrm_coefficients": coefficients.tolist(),
        "pre_sft_semantic_objective": True,
        "rl_evaluated_but_not_deployed": True,
    }


def baseline_score(data, history):
    return base_scores(data, history)


def tsgr_score(data, prefixes, global_order, query_order, coefficients, history):
    features = _features(data, prefixes, global_order, query_order, history)
    return features @ coefficients
