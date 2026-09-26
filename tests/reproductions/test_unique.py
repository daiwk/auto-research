from __future__ import annotations

import torch

from auto_research.reproductions.unique.experiment import (
    Data, Impression, evaluate, train_variant,
)
from auto_research.reproductions.unique.model import Unique


def test_flat_balanced_codebook_and_target_attention_split():
    torch.manual_seed(7)
    model = Unique(30, 3, torch.arange(30) % 3, tags=3, codes=8)
    user = torch.tensor([0])
    history = torch.arange(24)[None] % 30
    a, code, vectors = model(user, history, torch.tensor([[25, 26]]))
    b, _, _ = model(user, history, torch.tensor([[25, 29]]))
    torch.testing.assert_close(a[:, 0], b[:, 0])
    assert code.shape == (1, 8)
    assert model.assign(vectors).max() < 8
    a.sum().backward()
    assert model.query.weight.grad is not None
    prior = model.codebook.clone()
    model.update_codebook(vectors)
    assert not torch.equal(prior, model.codebook)


def test_public_shaped_training_and_isolated_evaluation():
    rows = tuple(Impression(index % 3, tuple(range(24)), 24 + index % 6,
                            index % 2, (index % 4) / 4) for index in range(20))
    data = Data(rows, rows[:8], rows[8:16], torch.arange(30) % 3, 3, 3, 20)
    model, final_loss = train_variant(data, seed=42, steps=2)
    result = evaluate(model, data.test, seed=43, limit=8)
    assert final_loss > 0
    assert result["evaluated_impressions"] == 8
    assert 0 <= result["ctr_auc"] <= 1
    assert result["retrieval_evaluated"] == 4
    assert 0 <= result["candidate_recall_at_4_codes"] <= 1
