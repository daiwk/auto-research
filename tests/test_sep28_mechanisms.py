"""Paper-equation and data-isolation contracts for the Sep 28 mechanism batch."""

import numpy as np
import pytest

from auto_research.agent_research.graft import Step, Trajectory, trajectory_credit
from auto_research.multimodal.deltas_eviction import (
    TokenScore, append_chunk, retain_positions, state_drift,
)


def test_graft_bellman_credits_shared_state_not_terminal_rollout():
    paths = (
        Trajectory((Step("root", "explore", "shared"), Step("shared", "finish", "win")), 1),
        Trajectory((Step("root", "explore", "shared"), Step("shared", "quit", "lose")), 0),
        Trajectory((Step("root", "skip", "lose"),), 0),
    )
    result = trajectory_credit(paths, gamma=0.8, gae_lambda=0.5)
    assert result.values["shared"] == pytest.approx(0.4)
    assert result.values["root"] == pytest.approx(0.8 * (0.4 * 2 / 3))
    # The first step of a *failed* rollout can still be beneficial.
    assert result.td[1][0] > 0
    assert result.td[1][1] < 0
    # With exact Bellman convergence and all empirical outgoing edges, each
    # downstream mean TD residual is zero; Graph GAE collapses to one-step TD.
    assert result.graph_gae[0][0] == pytest.approx(result.td[0][0])
    assert result.td[0][0] == result.td[1][0]


def test_graft_rejects_gold_like_terminal_collision_and_bad_paths():
    with pytest.raises(ValueError, match="conflicting"):
        trajectory_credit((Trajectory((Step("s", "a", "end"),), 1),
                           Trajectory((Step("s", "b", "end"),), 0)))
    with pytest.raises(ValueError, match="disconnected"):
        trajectory_credit((Trajectory((Step("s", "a", "u"), Step("v", "b", "end")), 1),))


def test_deltas_state_drift_and_temporal_retention():
    before = [np.eye(2), np.ones((2, 2))]
    after = [2 * np.eye(2), 1.5 * np.ones((2, 2))]
    assert state_drift(before, after) == pytest.approx(0.75)
    tokens = tuple(TokenScore(i, i // 2, float(i % 4)) for i in range(12))
    kept = retain_positions(tokens, budget=6, sinks=1, window=2, spans=3)
    assert len(kept) == 6
    assert {0, 10, 11}.issubset(kept)
    assert any(item < 5 for item in kept if item != 0)
    assert any(5 <= item < 10 for item in kept)
    # Scores are query-agnostic, original position IDs survive repeated eviction.
    first = append_chunk((), positions=(0, 1, 2), chunk=0, before=before, after=after,
                         budget=4, sinks=1, window=1, spans=2)
    second = append_chunk(first, positions=(3, 4, 5), chunk=1, before=before, after=after,
                          budget=4, sinks=1, window=1, spans=2)
    assert len(second) == 4
    assert second[0].position == 0 and second[-1].position == 5
    assert all(item.score == pytest.approx(0.75) for item in second)


def test_deltas_underfull_bucket_donates_capacity():
    tokens = tuple(TokenScore(i, 0 if i < 2 else 20 + i, float(i)) for i in range(8))
    kept = retain_positions(tokens, budget=5, sinks=0, window=0, spans=4)
    assert len(kept) == 5


def test_kite_training_gradients_and_cached_decode_equivalence():
    torch = pytest.importorskip("torch")
    from auto_research.foundation_models.kite_sst import SmallSST, train_two_stages

    torch.manual_seed(7)
    model = SmallSST(17, width=16, layers=2, max_positions=32)
    samples = torch.randint(0, 17, (4, 8))
    losses = train_two_stages(model, samples, source_steps=2, continuation_steps=2)
    assert all(np.isfinite(value) for value in losses.values())
    assert model.expanded
    model.eval()
    full, _ = model(samples[:1, :-1])
    last, _ = model(samples[:1, :-1], last_only=True)
    assert torch.allclose(full[:, -1:], last, atol=1e-5)
    past = None
    logits = None
    for position in range(samples.shape[1] - 1):
        logits, past = model(samples[:1, position:position + 1], past=past)
    assert torch.allclose(full[:, -1:], logits, atol=1e-5)
    # Decoder attends Prefiller KV; optimization reaches both towers.
    model.train()
    result, _ = model(samples[:, :-1])
    result.square().mean().backward()
    assert model.prefiller[0].k.weight.grad.abs().sum() > 0
    assert model.decoder[0].q.weight.grad.abs().sum() > 0
