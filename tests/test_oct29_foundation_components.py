"""Independent references and failure contracts for bounded Oct29 components."""
import pytest
import torch
from dataclasses import replace

from auto_research.foundation_models import gui_jepa, rescom, select_ttt


@pytest.mark.parametrize("module", [rescom, select_ttt, gui_jepa])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_measured_diagnostics(module, seed):
    result = module.diagnostic(seed)
    assert result["seed"] == seed and result["checks"]
    assert all(result["checks"].values())
    assert all(torch.isfinite(torch.tensor(v)) for v in result["metrics"].values())


def test_rescom_rank_zero_and_unnormalized_ridge():
    d = torch.tensor([[0., 1.], [1., 0.], [2., 1.], [1., 3.]], dtype=torch.float64)
    weight = torch.tensor([[2., -.4], [0., 3.]], dtype=torch.float64)
    e = d @ weight.T + torch.tensor([.3, -.2])
    moments = rescom.ResidualMoments.from_batch(d, e)
    branch = rescom.fit_residual_correction(moments, rank=2, ridge=.2)
    centered_d, centered_e = d - d.mean(0), e - e.mean(0)
    reference = torch.linalg.solve(centered_d.T @ centered_d + .2 * torch.eye(2, dtype=d.dtype),
                                    centered_d.T @ centered_e).T
    assert torch.allclose(branch.u @ branch.v, reference, atol=1e-12, rtol=0)
    assert torch.allclose(branch.bias, e.mean(0) - reference @ d.mean(0))
    zero = rescom.fit_residual_correction(moments, rank=0, ridge=.2)
    assert torch.equal(zero(d), e.mean(0).expand_as(e))
    with pytest.raises(ValueError):
        rescom.fit_residual_correction(moments, rank=3, ridge=.2)
    with pytest.raises(ValueError):
        rescom.fit_residual_correction(moments, rank=1, ridge=0)


def test_rescom_stream_merge_offsets_and_freezes():
    d = torch.arange(18, dtype=torch.float64).reshape(6, 3).requires_grad_()
    e = (d[:, :2] * 2 + 9).requires_grad_()
    merged = rescom.ResidualMoments.from_batch(d[:2], e[:2]).merge(
        rescom.ResidualMoments.from_batch(d[2:], e[2:]))
    whole = rescom.ResidualMoments.from_batch(d, e)
    assert torch.allclose(merged.cross, whole.cross)
    assert torch.allclose(merged.gram, whole.gram)
    assert not merged.cross.requires_grad
    with pytest.raises(ValueError):
        rescom.ResidualMoments.from_batch(d, e[:3])


@pytest.mark.parametrize("count", [True, 0, -1, 3.5, "4"])
def test_rescom_forged_moments_reject_invalid_count(count):
    d = torch.arange(8, dtype=torch.float64).reshape(4, 2)
    moments = rescom.ResidualMoments.from_batch(d, d)
    with pytest.raises(ValueError, match="integer rank"):
        rescom.fit_residual_correction(replace(moments, count=count), rank=1, ridge=.1)


def test_rescom_nonsymmetric_gram_is_not_silently_reinterpreted():
    d = torch.arange(8, dtype=torch.float64).reshape(4, 2)
    moments = rescom.ResidualMoments.from_batch(d, d)
    forged = moments.gram.clone()
    forged[0, 1] += .1
    with pytest.raises(ValueError, match="symmetric"):
        rescom.fit_residual_correction(replace(moments, gram=forged), rank=1, ridge=.1)


def test_select_ttt_topk_smallest_ce_and_duplicate_queries():
    hidden = torch.tensor([[[1., 0.], [0., 1.]]], dtype=torch.float64)
    head = torch.tensor([[3., 0.], [0., 1.]], dtype=torch.float64)
    tokens = torch.tensor([0, 0, 1])
    norm = torch.ones(2, dtype=torch.float64)
    score = select_ttt.query_chunk_scores(hidden, head, tokens, norm_weight=norm,
        norm_eps=1e-6, pooling_ratio=.1, vocabulary_block=1)
    logits = torch.nn.functional.rms_norm(hidden, (2,), norm, 1e-6) @ head.T
    ce = -logits.log_softmax(-1)[..., tokens].mean(-1)
    assert torch.allclose(score, ce.min(-1).values, atol=1e-12, rtol=0)
    assert not score.requires_grad
    with pytest.raises(ValueError):
        select_ttt.query_chunk_scores(hidden, head, torch.tensor([2]), norm_weight=norm, norm_eps=1e-6)


def test_select_ttt_clip_is_not_renormalized_and_output_precedes_write():
    multipliers = select_ttt.write_multipliers(torch.tensor([0., 100., 100.]), temperature=1., maximum=1.2)
    assert multipliers.sum() < 3
    initial = torch.zeros(1, 1, dtype=torch.float64)
    keys = torch.ones(2, 1, 1, dtype=torch.float64)
    values = 2 * keys
    result = select_ttt.apply_then_write(initial, keys, values, torch.ones(2, dtype=torch.float64), learning_rate=.5)
    assert torch.equal(result["outputs"], torch.tensor([[[0.]], [[1.]]], dtype=torch.float64))
    assert result["final_weight"].item() == 2
    assert initial.item() == 0
    with pytest.raises(ValueError):
        select_ttt.apply_then_write(initial, keys, values, torch.ones(2, dtype=torch.float64), learning_rate=-1)


def test_gui_loss_masks_candidates_and_weights_steps_not_weight_sum():
    scores = torch.tensor([[1., 3., 500.], [2., 4., 0.]], dtype=torch.float64, requires_grad=True)
    valid = torch.tensor([[True, True, False], [True, True, True]])
    loss = gui_jepa.listwise_loss(scores, torch.tensor([1, 0]), valid,
                                   positive_is_click=torch.tensor([True, False]))
    reference = (-torch.log_softmax(scores[0, :2], 0)[1]
                 - 1.5 * torch.log_softmax(scores[1], 0)[0]) / 2
    assert torch.equal(loss, reference)
    loss.backward()
    assert scores.grad[0, 2] == 0
    with pytest.raises(ValueError):
        gui_jepa.listwise_loss(scores, torch.tensor([2, 0]), valid,
                                positive_is_click=torch.tensor([True, False]))


def test_gui_positions_geometry_not_candidate_order():
    positions = gui_jepa.sine_cosine_positions(2, 2, 8)
    assert positions.shape == (4, 8)
    assert torch.equal(positions[0, :4], positions[2, :4])
    assert torch.equal(positions[0, 4:], positions[1, 4:])
    with pytest.raises(ValueError):
        gui_jepa.sine_cosine_positions(2, 2, 7)


@pytest.mark.parametrize("module", [rescom, select_ttt, gui_jepa])
def test_gpu_diagnostic_never_silently_falls_back(module, monkeypatch):
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    with pytest.raises(ValueError, match="real available cuda"):
        module.diagnostic(42, "cuda")
