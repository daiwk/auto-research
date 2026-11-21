import pytest
import torch

from auto_research.foundation_models.mv_jepa import (
    REQUIRES_GPU_VALIDATION, TinyMVJEPA, diagnostic, multiview_loss, replay_schedule,
)


@pytest.fixture
def sample():
    torch.manual_seed(19)
    model = TinyMVJEPA(input_width=4, width=8, heads=2)
    context = torch.randn(2, 2, 5, 4, requires_grad=True)
    heldout = torch.randn(2, 5, 4, requires_grad=True)
    masked = torch.tensor([[[0, 1, 0, 1, 0], [1, 0, 0, 1, 0]],
                           [[0, 1, 0, 1, 0], [1, 0, 0, 1, 0]]], dtype=torch.bool)
    ids = torch.tensor([[0, 1], [2, 3]])
    return model, context, heldout, masked, ids


def test_heldout_and_masked_context_only_affect_targets_not_predictions(sample):
    model, context, heldout, masked, ids = sample
    before = model(context, heldout, masked, ids)
    after = model(context, heldout + torch.randn_like(heldout) * 10, masked, ids)
    altered_context = context.detach().clone()
    altered_context[masked] += torch.randn_like(altered_context[masked]) * 20
    altered = model(altered_context, heldout, masked, ids)
    assert torch.equal(before["pred_context"], after["pred_context"])
    assert torch.equal(before["pred_heldout"], after["pred_heldout"])
    assert torch.equal(before["pred_heldout"], altered["pred_heldout"])
    assert not torch.equal(before["target_heldout"], after["target_heldout"])
    before["loss"].backward()
    assert heldout.grad is None
    assert torch.count_nonzero(context.grad[masked]) == 0
    assert context.grad[~masked].abs().sum() > 0
    assert all(p.grad is None for p in model.teacher.parameters())


def test_loss_normalizes_examples_before_batch_and_detaches_targets():
    pc = torch.tensor([[[[2.0], [0.0]]], [[[5.0], [9.0]]]], requires_grad=True)
    tc = torch.zeros_like(pc, requires_grad=True)
    ph = torch.tensor([[[4.0]], [[7.0]]], requires_grad=True)
    th = torch.zeros_like(ph, requires_grad=True)
    mask = torch.tensor([[[1, 0]], [[1, 1]]], dtype=torch.bool)
    loss = multiview_loss(pc, tc, ph, th, mask)
    assert loss.item() == pytest.approx(((2 + 4) / 2 + (5 + 9 + 7) / 3) / 2)
    loss.backward()
    assert tc.grad is None and th.grad is None
    assert pc.grad[0, 0, 1].item() == 0


@pytest.mark.parametrize("dtype", [torch.float16, torch.bfloat16, torch.float32, torch.float64])
def test_loss_extremes_are_finite_and_keep_student_gradient(dtype):
    pc = torch.full((1, 2, 3, 4), 60000.0, dtype=dtype, requires_grad=True)
    tc = torch.full_like(pc, -60000, requires_grad=True)
    ph = torch.full((1, 3, 4), -60000.0, dtype=dtype, requires_grad=True)
    th = torch.full_like(ph, 60000, requires_grad=True)
    loss = multiview_loss(pc, tc, ph, th, torch.ones((1, 2, 3), dtype=torch.bool))
    assert torch.isfinite(loss) and (loss.dtype == torch.float64) == (dtype == torch.float64)
    loss.backward()
    assert torch.isfinite(pc.grad).all() and pc.grad.abs().sum() > 0
    assert tc.grad is None and th.grad is None


def test_teacher_ema_only_changes_after_explicit_update(sample):
    model, context, heldout, masked, ids = sample
    teacher = [p.detach().clone() for p in model.teacher.parameters()]
    result = model(context, heldout, masked, ids)
    result["loss"].backward()
    torch.optim.SGD(model.encoder.parameters(), lr=0.1).step()
    assert all(torch.equal(old, p) for old, p in zip(teacher, model.teacher.parameters(), strict=True))
    online = [p.detach().clone() for p in model.encoder.parameters()]
    model.update_teacher(0.5)
    for old, new, p in zip(teacher, online, model.teacher.parameters(), strict=True):
        torch.testing.assert_close(p, 0.5 * old + 0.5 * new)
    with pytest.raises(ValueError):
        model.update_teacher(float("nan"))


def test_single_view_replay_uses_shared_encoder_and_predictor(sample):
    model, context, _, masked, _ = sample
    replay = model.single_view_replay(context[:, 0], masked[:, 0])
    replay.backward()
    assert any(p.grad is not None and p.grad.abs().sum() > 0 for p in model.encoder.parameters())
    assert any(p.grad is not None and p.grad.abs().sum() > 0 for p in model.predictor.parameters())
    assert all(p.grad is None for p in model.teacher.parameters())
    with pytest.raises(ValueError):
        model.single_view_replay(context[:, 0], torch.zeros_like(masked[:, 0]))


def test_view_identity_is_permutation_equivariant_and_reserved_ids_rejected(sample):
    model, context, heldout, masked, ids = sample
    before = model(context, heldout, masked, ids)
    after = model(context.flip(1), heldout, masked.flip(1), ids.flip(1))
    torch.testing.assert_close(before["pred_heldout"], after["pred_heldout"], atol=1e-6, rtol=1e-6)
    for bad in (ids * 0, ids + model.max_context_views):
        with pytest.raises(ValueError):
            model(context, heldout, masked, bad)


def test_nonfinite_and_all_masked_inputs_rejected(sample):
    model, context, heldout, masked, ids = sample
    with pytest.raises(ValueError):
        model(context, heldout, torch.ones_like(masked), ids)
    bad = heldout.detach().clone()
    bad[0, 0, 0] = float("nan")
    with pytest.raises(ValueError):
        model(context, bad, masked, ids)


def test_replay_schedule_counts_determinism_and_shuffle():
    first = replay_schedule(42)
    assert first == replay_schedule(42) and first != replay_schedule(43)
    assert len(first) == 300 and first.count("multiview") == 152 and first.count("replay") == 148
    with pytest.raises(ValueError):
        replay_schedule(42, multiview=0, replay=0)


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic_executes_real_tiny_wiring(seed):
    assert REQUIRES_GPU_VALIDATION is True
    output = diagnostic(seed, "cpu")
    assert output["diagnostic_only"] and output["evaluation_tier"] == "l1_mechanism"
    assert all(output["checks"].values())
    assert output["metrics"]["online_gradient_l1"] > 0
