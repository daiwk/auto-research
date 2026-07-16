from __future__ import annotations

import numpy as np

from ..industrial_2026 import base_scores


def train_sam(data):
    intervals = {domain: [] for domain in range(int(data.domains.max()) + 1)}
    for sequence in data.sequences.train:
        last = {}
        for timestamp, item in enumerate(sequence):
            domain = int(data.domains[item])
            if domain in last:
                intervals[domain].append(timestamp - last[domain])
            last[domain] = timestamp
    cycles = np.asarray([np.mean(intervals[d]) if intervals[d] else 8.0 for d in intervals])
    return cycles, {"dual_path_cross_attention": True, "learned_category_cycles": cycles.tolist(), "censored_domains": sum(not values for values in intervals.values()), "ttnp_auxiliary_mse": float(np.mean([(np.log1p(value) - np.log1p(cycles[d])) ** 2 for d, values in intervals.items() for value in values]) if any(intervals.values()) else 0.0)}


def score_sam(data, cycles, history):
    scores = base_scores(data, history)
    elapsed = np.full(len(cycles), 1e6)
    for reverse_position, item in enumerate(reversed(history), start=1):
        domain = data.domains[item]
        elapsed[domain] = min(elapsed[domain], reverse_position)
    # Pointwise intent localization plus adaptive satiation gate and logit intervention.
    history_features = data.sequences.features[list(history[-12:])]
    probe = history_features[-1]
    attribution = 1.0 / (1.0 + np.exp(-4.0 * (data.sequences.features @ probe - 0.35)))
    phi_logits = np.clip(4.0 * (0.8 - elapsed[data.domains] / np.maximum(cycles[data.domains], 1e-6)), -40, 40)
    phi = 1.0 / (1.0 + np.exp(-phi_logits))
    mask = np.clip(1.0 - attribution * phi, 1e-4, 1.0)
    return scores + 0.12 * np.log(mask)
