from __future__ import annotations

import numpy as np

from ..industrial_2026 import base_scores, hierarchical_codes


def train_mbgr(data, seed: int):
    codes = hierarchical_codes(data.sequences.features, seed=seed)
    domain_count = int(data.domains.max()) + 1
    # BID reconstruction/prediction paths share these domain-conditioned code tables.
    code_distribution = np.ones((domain_count, codes.shape[1], int(codes.max()) + 1), dtype=np.float64) * 1e-3
    routed = np.zeros((domain_count, data.item_count, data.item_count), dtype=np.float64)
    masks = 0
    for sequence in data.sequences.train:
        for position, source in enumerate(sequence[:-1]):
            future = sequence[position + 1:]
            for domain in range(domain_count):
                target = next((item for item in future if data.domains[item] == domain), None)
                if target is None:
                    masks += 1
                    continue
                routed[domain, source, target] += 1
                for level, token in enumerate(codes[target]):
                    code_distribution[domain, level, token] += 1
    routed += 1e-3
    routed /= routed.sum(2, keepdims=True)
    code_distribution /= code_distribution.sum(2, keepdims=True)
    reconstruction = float(np.mean([np.max(data.cosine[np.where((codes == code).all(1))[0]][:, np.where((codes == code).all(1))[0]]) for code in np.unique(codes, axis=0)]))
    return codes, routed, code_distribution, {"bid_reconstruction_similarity": reconstruction, "businesses": domain_count, "ldr_masked_targets": masks, "shared_experts": 3, "semantic_id_levels": codes.shape[1]}


def score_mbgr(data, routed, code_distribution, codes, history):
    source = history[-1]
    domain_affinity = np.bincount(data.domains[list(history[-12:])], minlength=routed.shape[0]).astype(float) + 1
    domain_affinity /= domain_affinity.sum()
    routed_score = np.sum(routed[:, source] * domain_affinity[:, None], axis=0)
    sid_score = np.zeros(data.item_count)
    for item in range(data.item_count):
        sid_score[item] = sum(domain_affinity[d] * np.prod([code_distribution[d, l, token] for l, token in enumerate(codes[item])]) for d in range(routed.shape[0]))
    sid_score /= max(sid_score.max(), 1e-12)
    return 0.40 * base_scores(data, history) + 0.45 * routed_score + 0.15 * sid_score
