import numpy as np

from auto_research.paper_methods import (
    SequentialModel,
    _ranking_metrics,
    sis_topk_weight,
)


def test_sis_acceptance_sets_unit_weight():
    target = np.array([0.6, 0.3, 0.1])
    behavior = np.array([0.4, 0.4, 0.2])
    rng = np.random.default_rng(1)
    weights = [sis_topk_weight(target, behavior, 0, 3, rng) for _ in range(100)]
    assert any(accepted and weight == 1.0 for weight, accepted in weights)
    assert all(weight in {1.0, 1.5} for weight, _ in weights)


def test_ranking_metrics_perfect_top_item():
    model = SequentialModel(np.array([[1.0], [1.0], [1.0]]), np.array([[0.0], [1.0], [3.0]]))
    metrics = _ranking_metrics(model, None, [(0, 2)], {0: {0}}, 3)
    assert metrics["hit_at_10"] == 1.0
    assert metrics["ndcg_at_10"] == 1.0
