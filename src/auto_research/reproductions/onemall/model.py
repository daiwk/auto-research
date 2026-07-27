from __future__ import annotations

import numpy as np

from ..industrial_2026 import hierarchical_codes, softmax


def build_onemall_scorer(data):
    """Domain prompt + semantic tokenizer + cross-behavior fusion."""
    codes = hierarchical_codes(data.sequences.features, levels=3, width=8)
    semantic = (codes[:, None] == codes[None]).mean(-1)
    domain_transition = np.ones(
        (data.domains.max() + 1, data.item_count, data.item_count)
    ) * 1e-3
    for sequence in data.sequences.train:
        for left, right in zip(sequence, sequence[1:]):
            domain_transition[data.domains[right], left, right] += 1
    domain_transition /= domain_transition.sum(-1, keepdims=True)

    def scorer(history):
        recent = np.asarray(history[-12:])
        prompt = softmax(
            np.bincount(
                data.domains[recent], minlength=domain_transition.shape[0]
            ).astype(float)
        )
        flow = sum(
            prompt[domain] * domain_transition[domain, recent].mean(0)
            for domain in range(len(prompt))
        )
        cross_behavior = data.cosine[recent].mean(0)
        return 0.55 * flow + 0.25 * semantic[recent[-1]] + 0.20 * cross_behavior

    return scorer, {
        "semantic_id_levels": 3,
        "scenario_prompts": int(domain_transition.shape[0]),
        "cross_behavior_fusion": True,
    }
