from __future__ import annotations

import torch

from auto_research.reproductions.muser.experiment import Data, Example, evaluate, train_variant
from auto_research.reproductions.muser.model import MuSeR


def test_progressive_pooling_retains_recent_events_and_shortens_old_history():
    model = MuSeR(100, 5, torch.zeros(100, dtype=torch.long))
    history = torch.arange(80)
    compressed = model._compress_one(history)
    recent = model.item_vectors(history[-8:])
    assert compressed.shape[0] < 80
    torch.testing.assert_close(compressed[-8:], recent)


def test_candidate_sensitive_multi_interest_routing_and_orthogonality():
    model = MuSeR(20, 3, torch.arange(20) % 3)
    histories = [torch.tensor([1, 2, 3, 4]), torch.tensor([5, 6, 7, 8, 9])]
    interests = model.encode(histories)
    scores = model.score(interests, torch.tensor([[2, 3], [8, 9]]))
    assert interests.shape == (2, 4, 32)
    assert scores.shape == (2, 2)
    assert torch.isfinite(model.orthogonality(interests))
    scores.sum().backward()
    assert model.queries.grad is not None


def test_training_and_holdout_on_tiny_public_shaped_slice():
    item_tags = torch.arange(20) % 3
    examples = tuple(Example((index, index + 1, index + 2), index + 3)
                     for index in range(10))
    data = Data(examples, examples[-3:], examples[-2:], item_tags, 3, 40)
    model, loss = train_variant(data, seed=7, compression=True, semantics=True,
                                steps=2)
    result = evaluate(model, data.test, seed=8)
    assert loss > 0
    assert result["evaluated"] == 2
    assert 0 <= result["recall_at_10"] <= 1
