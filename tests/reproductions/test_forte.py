import numpy as np
import pytest
import torch

from auto_research.reproductions.forte.experiment import (
    FeatureRanker,
    LineageAudit,
    Ragged,
    TemporalGate,
    VirtualBatch,
    binary_metrics,
    collate,
    parameter_digest,
    perturb,
    signed_change,
)


def test_typed_permutation_and_nulls_preserve_batch_and_content():
    sparse = torch.tensor([[1.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 3.0]]).to_sparse()
    ragged = Ragged(torch.tensor([1, 2, 3]), torch.tensor([0, 2, 2, 3]))
    order = torch.tensor([2, 0, 1])
    assert torch.equal(perturb(sparse, order).to_dense(), sparse.to_dense()[order])
    reordered = perturb(ragged, order)
    assert reordered.values.tolist() == [3, 1, 2]
    assert reordered.offsets.tolist() == [0, 1, 3, 3]
    assert perturb(sparse, None)._nnz() == 0
    assert perturb(ragged, None).offsets.tolist() == [0, 0, 0, 0]
    with pytest.raises(ValueError):
        perturb(sparse, torch.tensor([0, 0, 1]))


def test_virtualization_shares_materialization_and_does_not_mutate_input():
    x = torch.arange(12).reshape(4, 3).float()
    virtual = VirtualBatch({"a": x, "b": x.clone()}, seed=3)
    view = virtual.view(("a",))
    assert view["b"] is virtual.original["b"]
    assert view["a"] is virtual.perturbed["a"]
    assert torch.equal(x, torch.arange(12).reshape(4, 3).float())
    with pytest.raises(ValueError):
        virtual.view(("gold",))


def test_signed_convention_and_tied_metrics():
    assert signed_change(0.8, 0.72) == pytest.approx(-10)
    assert signed_change(0.8, 0.72, higher_is_better=False) == pytest.approx(10)
    with pytest.raises(ValueError):
        signed_change(0, 0.5)
    result = binary_metrics(np.array([0, 1, 0, 1]), np.ones(4))
    assert result == {"roc_auc": 0.5, "pr_auc": 0.5}


def test_temporal_all_heads_windows_and_rising_reliance_veto():
    # Feature a becomes less relied upon; b becomes stronger in one head only.
    scores = np.array(
        [
            [[0.3, -0.1, -2], [0.3, -0.1, -2]],
            [[0.4, -0.2, -2], [0.4, -0.1, -2]],
            [[0.5, -0.3, -2], [0.5, -0.1, -2]],
        ]
    )
    result = TemporalGate().select(scores, ("a", "b", "c"))
    assert result["a"]["passed"]
    assert not result["b"]["passed"]
    assert not result["c"]["passed"]
    with pytest.raises(ValueError):
        TemporalGate().select(scores[:1], ("a", "b", "c"))


def test_audit_is_ordered_requires_owner_and_all_consumers():
    audit = LineageAudit({"x": {"a", "b"}})
    audit.retire_consumer("x", "a")
    with pytest.raises(ValueError):
        audit.approve("x", "dataloader", owner_approved=True)
    audit.retire_consumer("x", "b")
    with pytest.raises(ValueError):
        audit.approve("x", "dataloader", owner_approved=False)
    with pytest.raises(ValueError):
        audit.approve("x", "logging", owner_approved=True)
    for stage in ("dataloader", "dataset", "ingestion", "logging"):
        audit.approve("x", stage, owner_approved=True)
    assert audit.completed["x"][-1] == "logging"


def test_real_model_gradient_and_frozen_perturbation():
    rows = [
        {"user": 0, "genres": [1, 2], "age": 0.2, "targets": [1, 0]},
        {"user": 1, "genres": [], "age": 0.8, "targets": [0, 1]},
    ]
    schema = {"user": ("sparse", 2), "genres": ("ragged", 3), "age": ("dense", 1)}
    model = FeatureRanker(schema)
    features, labels = collate(rows, schema, "cpu")
    logits = model(features)
    torch.nn.functional.binary_cross_entropy_with_logits(logits, labels).backward()
    assert all(p.grad is not None and torch.isfinite(p.grad).all() for p in model.parameters())
    before = parameter_digest(model)
    null = VirtualBatch(features, seed=4, ablate=True)
    assert not torch.equal(model(null.view(("user", "genres"))), logits)
    assert parameter_digest(model) == before
