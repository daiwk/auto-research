import numpy as np
import pytest

from auto_research.agent_research.actkv_budget import confidence_budget


def _distributions(mass):
    mass = np.asarray(mass, dtype=float)
    return np.stack((mass, 1 - mass), axis=1)


def test_falling_confidence_increases_budget_only_to_cap():
    result = confidence_budget(
        _distributions([0.99, 0.95, 0.9, 0.8, 0.7, 0.6]),
        budget=7, budget_upper=10, scale_up=2,
        top_k=1, window=2, stride=1, bottom_fraction=1,
    )
    assert result.confidence_slope < 0
    assert result.budget == 10


def test_rising_confidence_and_short_trace_do_not_increase_budget():
    rising = confidence_budget(
        _distributions([0.6, 0.7, 0.8, 0.9, 0.95, 0.99]),
        budget=7, budget_upper=10, top_k=1,
        window=2, stride=1, bottom_fraction=1,
    )
    short = confidence_budget(
        _distributions([0.8, 0.7]), budget=7, budget_upper=10,
        top_k=1, window=2,
    )
    assert rising.confidence_slope > 0
    assert rising.budget == short.budget == 7


@pytest.mark.parametrize("probabilities", [
    [[0.8, 0.8]], [[-0.2, 1.2]], [[float("nan"), 0.5]],
])
def test_rejects_invalid_distributions(probabilities):
    with pytest.raises(ValueError):
        confidence_budget(np.array(probabilities), budget=2, budget_upper=5)
