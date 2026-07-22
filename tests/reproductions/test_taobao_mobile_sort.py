import numpy as np


def test_recgpt_mobile_intent_drift_is_zero_without_change():
    from auto_research.reproductions.recgpt_mobile.model import intent_drift
    item_genres = (("Action",), ("Comedy",), ("Action", "Comedy"))
    assert intent_drift((0, 2), (0, 2), 2, item_genres) == 0.0
    assert intent_drift((0, 0), (1, 1), 2, item_genres) > 0.4


def test_sort_ordered_targets_are_monotone():
    import torch
    from auto_research.reproductions.sort_gen.model import ordered_targets
    labels = ordered_targets(torch.tensor([[1.0, 0.0, 1.0]]), 3, torch)
    assert labels.shape == (1, 3, 3)
    assert labels[0, 2].tolist() == [1.0, 1.0, 0.0]
    assert bool((labels[..., 1:] <= labels[..., :-1]).all())


def test_sort_formula_returns_unique_positions():
    from auto_research.reproductions.sort_gen.data import Slate
    from auto_research.reproductions.sort_gen.model import formula_greedy
    row = Slate(np.arange(5), np.ones(2), np.arange(15, dtype=np.float32).reshape(5, 3), np.ones(5), np.ones(5), np.ones(5))
    order = formula_greedy(row, 4)
    assert len(order) == len(set(order.tolist())) == 4
