import pytest
import torch

from auto_research.reproductions.uxsid.model import (
    ResidualKmeansFSQ, SemanticMemoryCache, UxSID, objective, orthogonality_loss,
)


def test_residual_hybrid_has_finite_scalar_codes_and_first_sid():
    torch.manual_seed(4)
    vectors = torch.randn(40, 8)
    quantizer = ResidualKmeansFSQ(codebook_size=5, kmeans_stages=2, scalar_levels=7).fit(vectors[:30], seed=42)
    encoded = quantizer.encode(vectors)
    assert encoded.first_ids.shape == (40,)
    assert encoded.first_ids.max() < 5
    assert len(encoded.residual_ids) == 2
    assert encoded.residual_ids[-1].shape == vectors.shape
    assert 0 <= encoded.residual_ids[-1].min() <= encoded.residual_ids[-1].max() <= 6
    assert torch.isfinite(encoded.reconstruction).all()
    assert encoded.reconstruction_mse < vectors.square().mean()


def test_paper_orthogonality_is_not_cosine_orthogonality():
    anchors = torch.eye(3)[None]
    assert torch.allclose(orthogonality_loss(anchors), torch.tensor((3 * (2 / 3) ** 2) ** .5))
    assert torch.allclose(orthogonality_loss(5 * anchors), orthogonality_loss(anchors))


def test_two_items_with_same_sid_share_memory_but_can_have_different_scores():
    torch.manual_seed(42)
    model = UxSID(items=20, users=5, sid_count=4, dimension=8, anchors=3).eval()
    history = torch.tensor([[0, 1, 2, 3]])
    valid = history > 0
    cache = SemanticMemoryCache()
    left = cache.get(model, user=1, sid=2, history_ids=history, valid=valid, model_revision="first")
    right = cache.get(model, user=1, sid=2, history_ids=history, valid=valid, model_revision="first")
    assert left.data_ptr() == right.data_ptr()
    uncached, _ = model.memory(history, valid, torch.tensor([2]))
    assert torch.equal(left, uncached)
    scores = [model.score(memory=left, users=torch.tensor([1]), targets=torch.tensor([target]),
                          history_ids=history, valid=valid, context=torch.tensor([.2]), sid_ids=torch.tensor([2])) for target in (4, 5)]
    assert not torch.equal(*scores)
    cache.get(model, user=1, sid=2, history_ids=history, valid=valid, model_revision="second")
    assert len(cache.values) == 2


def test_padding_cannot_affect_interest_and_core_submodules_get_gradients():
    torch.manual_seed(42)
    model = UxSID(items=20, users=5, sid_count=4, dimension=8, anchors=3)
    history = torch.tensor([[0, 1, 2, 3], [0, 0, 4, 5]])
    valid = history > 0
    inputs = dict(users=torch.tensor([1, 2]), targets=torch.tensor([6, 7]),
                  history_ids=history, valid=valid, context=torch.tensor([.2, .3]), sid_ids=torch.tensor([2, 3]))
    logits, regularizer = model(**inputs)
    objective(logits, torch.tensor([0., 1.]), regularizer).backward()
    for module in (model.compressor, model.global_attention, model.local_attention, model.gate):
        assert any(p.grad is not None and p.grad.abs().sum() > 0 for p in module.parameters())
    padded = history.clone()
    padded[~valid] = 19
    assert torch.allclose(model.memory(history, valid, inputs["sid_ids"])[0],
                          model.memory(padded, valid, inputs["sid_ids"])[0])
    with pytest.raises(ValueError, match="real history"):
        model.memory(torch.zeros_like(history), torch.zeros_like(valid), inputs["sid_ids"])
