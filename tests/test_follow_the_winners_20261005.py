import numpy as np
import pytest
import torch

from auto_research.post_training.follow_the_winners import (
    FIFOReplay,
    Trajectory,
    elite_indices,
    projection_loss,
    rank_occupancy,
    run_bandit,
)


def test_rank_occupancy_is_normalized_and_has_the_paper_boundary_cases():
    for batch_size, winners in ((2, 1), (5, 1), (5, 3), (5, 5), (10, 2)):
        masses = [rank_occupancy(buffer_size=10, batch_size=batch_size, winners=winners, rank=r)
                  for r in range(1, 11)]
        assert sum(masses) == pytest.approx(1)
        if batch_size == winners:
            assert masses == pytest.approx([0.1] * 10)
        else:
            assert masses[0] > masses[-1]
    assert rank_occupancy(buffer_size=10, batch_size=10, winners=2, rank=3) == 0


def test_minibatch_elites_keep_repeated_winners_and_fifo_expires_old_items():
    rng = np.random.default_rng(7)
    assert elite_indices(np.array([0., 1., 2.]), batch_size=3, winners=1, batches=4, rng=rng) == [2] * 4
    replay = FIFOReplay(2)
    for i in range(3):
        replay.append(Trajectory(i, float(i)))
    assert [item.action for item in replay.snapshot()] == [1, 2]
    with pytest.raises(ValueError):
        elite_indices(np.array([0., 1.]), batch_size=3, winners=1, batches=1, rng=rng)


def test_projection_gradient_and_bandit_update():
    logits = torch.zeros(2, dtype=torch.float64, requires_grad=True)
    loss = projection_loss(
        logits, torch.tensor([0, 0, 1]), torch.tensor([0.5, 0.5], dtype=torch.float64),
        kl_weight=0.05,
    )
    loss.backward()
    assert float(logits.grad[0]) < 0
    for seed in (42, 43, 44):
        result = run_bandit(seed)
        assert result["best_action_probability_final"] > 0.8
    with pytest.raises(ValueError):
        projection_loss(logits, torch.tensor([2]), torch.tensor([0.5, 0.5]), kl_weight=0)
