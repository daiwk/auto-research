import numpy as np

from auto_research.reproductions.sis.algorithm import sis_topk_weight


def test_sis_acceptance_sets_unit_weight():
    target = np.array([0.6, 0.3, 0.1])
    behavior = np.array([0.4, 0.4, 0.2])
    rng = np.random.default_rng(1)
    weights = [sis_topk_weight(target, behavior, 0, 3, rng) for _ in range(100)]
    assert any(accepted and weight == 1.0 for weight, accepted in weights)
    assert all(weight in {1.0, 1.5} for weight, _ in weights)
