import numpy as np
import pytest

from auto_research.agent_research.actkv_policy import action_lrfu_step


def test_action_attention_retains_intermittent_entry():
    first = action_lrfu_step(np.array([0.8, 0.1, 0.1]), np.array([]), budget=2)
    assert first.retained_indices == (0, 1)
    # First slot is temporarily quiet, but its decayed history survives.
    second = action_lrfu_step(
        np.array([0.0, 0.2, 0.3, 0.5]), np.array(first.keep_scores),
        budget=2, decay=0.8,
    )
    assert 0 in second.retained_indices
    assert 3 in second.retained_indices


def test_new_slots_start_at_zero_and_output_keeps_sequence_order():
    result = action_lrfu_step(
        np.array([0.05, 0.15, 0.8]), np.array([0.6]), budget=2,
    )
    assert result.retained_indices == (0, 2)
    assert len(result.keep_scores) == 2


@pytest.mark.parametrize("attention,prior,budget", [
    ([0.1, -0.1], [], 1),
    ([0.1], [0.0, 0.0], 1),
    ([0.1], [], 0),
])
def test_invalid_inputs_rejected(attention, prior, budget):
    with pytest.raises(ValueError):
        action_lrfu_step(np.array(attention), np.array(prior), budget=budget)
