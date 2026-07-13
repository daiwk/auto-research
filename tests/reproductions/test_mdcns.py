import numpy as np

from auto_research.reproductions.mdcns.experiment import ranking_metrics
from auto_research.reproductions.mdcns.model import SequentialModel


def test_ranking_metrics_perfect_top_item():
    model = SequentialModel(
        np.array([[1.0], [1.0], [1.0]]),
        np.array([[0.0], [1.0], [3.0]]),
    )
    metrics = ranking_metrics(model, None, [(0, 2)], {0: {0}}, 3)
    assert metrics["hit_at_10"] == 1.0
    assert metrics["ndcg_at_10"] == 1.0
