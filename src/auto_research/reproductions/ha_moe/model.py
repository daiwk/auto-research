from __future__ import annotations

import numpy as np

from ..industrial_2026 import base_scores, softmax


def build_ha_moe(data):
    """Build item-side statistics used by heterogeneous experts."""
    domain_pop = np.zeros((int(data.domains.max()) + 1, data.item_count))
    for domain in range(len(domain_pop)):
        mask = data.domains == domain
        domain_pop[domain, mask] = data.popularity[mask]
        total = domain_pop[domain].sum()
        if total:
            domain_pop[domain] /= total
    fresh = 1.0 - data.popularity
    return {"domain_pop": domain_pop, "fresh": fresh}


def score_ha_moe(data, state, history):
    recent = np.asarray(history[-12:], dtype=np.int64)
    domains = data.domains[recent]
    histogram = np.bincount(domains, minlength=len(state["domain_pop"])).astype(float)
    histogram /= max(histogram.sum(), 1.0)
    entropy = -(histogram * np.log(histogram + 1e-12)).sum() / np.log(max(len(histogram), 2))
    # Heterogeneity-aware gates: homogeneous sessions emphasize their domain;
    # heterogeneous sessions route more mass to transition and freshness experts.
    gates = softmax(np.asarray([1.6 - entropy, 0.8 + entropy, 0.2 + 1.4 * entropy, 0.5]))
    domain_expert = histogram @ state["domain_pop"]
    transition_expert = np.mean(data.transition[recent[-4:]], axis=0)
    content_expert = np.mean(data.cosine[recent], axis=0)
    fresh_expert = state["fresh"] * (0.25 + entropy)
    experts = np.stack([domain_expert, transition_expert, content_expert, fresh_expert])
    return gates @ experts


def score_baseline(data, history):
    return base_scores(data, history)
