import json
from pathlib import Path

import torch

from auto_research.reproductions.xrec.sid_ar import SIDAutoregressive, fit_item_codes


def test_sid_ar_ce_gradients_and_beam_prefix_order() -> None:
    torch.manual_seed(5)
    vectors = torch.nn.functional.normalize(torch.randn(32, 8), dim=-1)
    codes, codebooks = fit_item_codes(vectors, seed=5, levels=3, size=4)
    model = SIDAutoregressive(vectors, codes, codebooks, width=16, max_history=8)
    history = torch.tensor([[1, 2, 3], [4, 5, 0]])
    valid = torch.tensor([[True, True, True], [True, True, False]])
    loss = model.loss(history, valid, torch.tensor([6, 7]))
    loss.backward()
    assert model.code_heads[0].weight.grad.abs().sum() > 0
    assert model.code_embeddings[0].weight.grad.abs().sum() > 0
    beams, scores = model.beam_codes(history, valid, width=5)
    assert beams.shape == (2, 5, 3)
    assert (scores[:, :-1] >= scores[:, 1:]).all()
    assert model.trigger_vectors(history, valid, width=5).shape == (2, 5, 8)
    torch.testing.assert_close(model.trigger_vectors(history, valid, width=5).norm(dim=-1), torch.ones(2, 5))


def test_fair_budget_receipt_is_three_seed_and_explicitly_cpu() -> None:
    root = Path(__file__).resolve().parents[2]
    path = root / "docs/reproductions/2609.29180-xrec/metrics/fair-budget-seeds42-44.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["evaluation_protocol"]["formal_comparison"] is False
    assert [entry["seed"] for entry in payload["seeds"]] == [42, 43, 44]
    for row in payload["seeds"]:
        assert "CPU generation-only" in row["protocol"]
    for model in ("xrec", "sid_ar", "u2i"):
        values = [row["test_recall_at_20"][model] for row in payload["seeds"]]
        assert abs(sum(values) / 3 - payload["metrics"][f"test_recall_at_20_{model}_mean"]) < 1e-10
