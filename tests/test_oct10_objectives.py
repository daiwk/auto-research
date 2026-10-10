import copy

import pytest
import torch
from torch.func import functional_call

from auto_research.post_training.oct10_objectives import (
    dial_opd_loss, dial_opd_scores, grpo_dropout, meta_opd_descriptor,
    meta_opd_step, meta_opd_weights, residual_advantage, virtual_adamw,
    SemiOPDCache, co_ra_step, semi_opd_loss, topk_overlap,
)


def test_dial_limits_scaling_masks_and_stop_gradient():
    p, q = torch.tensor([[0.08, 1e-4]]), torch.tensor([[0.8, 1e-3]])
    s = dial_opd_scores(p.log(), q.log(), 1)
    assert torch.allclose(s, (q - p).abs())
    assert torch.allclose(dial_opd_scores((p * 0.1).log(), (q * 0.1).log(), 0.5),
                          dial_opd_scores(p.log(), q.log(), 0.5) * 0.1**0.5)
    current, teacher = p.log().requires_grad_(), q.log().requires_grad_()
    loss, selected = dial_opd_loss(current, teacher, torch.ones_like(p, dtype=torch.bool), retention=0.5)
    assert selected.tolist() == [[True, False]]
    loss.backward()
    assert current.grad[0, 1] == 0 and teacher.grad is None
    assert torch.isfinite(dial_opd_scores(p.log(), p.log())).all()
    with pytest.raises(ValueError):
        dial_opd_loss(current, teacher, torch.zeros_like(p, dtype=torch.bool))


def test_meta_descriptor_and_response_normalization():
    logits = torch.randn(2, 4, 40, requires_grad=True)
    descriptor = meta_opd_descriptor(logits, logits + 0.2, torch.zeros(2, 4, dtype=torch.long))
    assert descriptor.shape == (2, 4, 74) and not descriptor.requires_grad
    assert torch.allclose(descriptor[0, :, 8], torch.tensor([0., 1/3, 2/3, 1.]))
    mask = torch.tensor([[1., 1., 0., 0.], [0., 0., 0., 0.]])
    score = torch.randn(2, 4, requires_grad=True)
    weights = meta_opd_weights(score, mask)
    assert torch.allclose(weights[0].sum(), torch.tensor(2.))
    assert weights[1].sum() == 0
    assert torch.allclose(meta_opd_weights(score + 100, mask), weights, atol=1e-5)


def test_virtual_adamw_matches_real_existing_state_and_does_not_mutate():
    torch.manual_seed(42)
    model = torch.nn.Linear(3, 2)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.01, weight_decay=0.1)
    x = torch.randn(5, 3)
    for _ in range(2):
        optimizer.zero_grad()
        model(x).square().mean().backward()
        optimizer.step()
    saved = copy.deepcopy(optimizer.state_dict())
    before = {name: value.detach().clone() for name, value in model.named_parameters()}
    loss = model(x).square().mean()
    virtual = virtual_adamw(model, optimizer, loss, max_grad_norm=0.5)
    assert all(torch.equal(before[name], value) for name, value in model.named_parameters())
    for key in saved["state"]:
        assert torch.equal(saved["state"][key]["exp_avg"], optimizer.state_dict()["state"][key]["exp_avg"])
    optimizer.zero_grad()
    model(x).square().mean().backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 0.5)
    optimizer.step()
    assert all(torch.allclose(virtual[name], value, atol=1e-6) for name, value in model.named_parameters())


def test_meta_step_has_real_hypergradient_and_updates_both_networks():
    torch.manual_seed(4)
    model = torch.nn.Linear(5, 40)
    network = torch.nn.Sequential(torch.nn.Linear(74, 16), torch.nn.Tanh(), torch.nn.Linear(16, 1))
    torch.nn.init.zeros_(network[-1].weight)
    torch.nn.init.zeros_(network[-1].bias)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.02)
    meta_optimizer = torch.optim.AdamW(network.parameters(), lr=0.01)
    x, ref = torch.randn(2, 4, 5), torch.randn(2, 4, 5)
    actions = torch.randint(40, (2, 4))
    teacher = torch.randn(2, 4, 40)
    old = model(x).detach().log_softmax(-1).gather(-1, actions[..., None]).squeeze(-1)
    before = model.weight.detach().clone()
    def logits_fn(parameters):
        return model(x) if parameters is None else functional_call(model, parameters, (x,))
    def reference_loss_fn(parameters):
        return functional_call(model, parameters, (ref,)).log_softmax(-1)[..., 3].neg().mean()
    result = meta_opd_step(model, network, optimizer, meta_optimizer, logits_fn=logits_fn,
                           reference_loss_fn=reference_loss_fn, teacher_logits=teacher,
                           actions=actions, old_logp=old, mask=torch.ones(2, 4))
    assert torch.isfinite(torch.tensor(result["outer_loss"]))
    assert not torch.equal(before, model.weight)
    assert network[-1].weight.abs().sum() > 0
    assert result["weight_std"] > 0


def test_residual_keeps_verifier_mean_and_dropout_keeps_negatives():
    torch.manual_seed(2)
    student, teacher = torch.randn(2, 3, 40), torch.randn(2, 3, 40)
    mask = torch.tensor([[1., 1., 1.], [1., 0., 0.]])
    verification = torch.tensor([1., -1.])
    result = residual_advantage(student, teacher, torch.zeros(2, 3, dtype=torch.long), mask, verification)
    assert torch.allclose(result.sum(-1) / mask.sum(-1), verification)
    old_lp = torch.tensor([[-0.1, -0.1], [-1., -1.], [-3., -3.], [-4., -4.]])
    advantage = torch.tensor([1., 1., -1., -1.])
    retained, centered = grpo_dropout(old_lp, torch.ones_like(old_lp), advantage)
    assert retained[2:].all()
    probability = old_lp.mean(-1)[retained].softmax(0)
    assert abs(float((probability * centered[retained]).sum())) < 1e-6


def test_semi_cache_is_frozen_and_advantage_is_recomputed():
    from dataclasses import FrozenInstanceError

    cache = SemiOPDCache("student-sha", "teacher-sha", "tokenizer-sha", "data-sha",
                         ((2, 3, 4),), ((False, True),), ((-2., -3.),))
    with pytest.raises(FrozenInstanceError):
        cache.initial_student_revision = "new-student"
    with pytest.raises(ValueError):
        SemiOPDCache("", "teacher", "tok", "data", cache.token_ids,
                     cache.response_masks, cache.teacher_logp)
    lp = torch.tensor([[-2., -5.]], requires_grad=True)
    mask = torch.tensor([[False, True]])
    teacher = torch.tensor(cache.teacher_logp, requires_grad=True)
    semi_opd_loss(lp, teacher, mask).backward()
    assert lp.grad.tolist() == [[0., -2.]] and teacher.grad is None
    lp2 = torch.tensor([[-2., -4.]], requires_grad=True)
    semi_opd_loss(lp2, teacher, mask).backward()
    assert lp2.grad.tolist() == [[0., -1.]]
    s = torch.tensor([[[4., 3., 2., 1.], [4., 3., 2., 1.]]])
    t = torch.tensor([[[4., 3., 2., 1.], [1., 2., 3., 4.]]])
    assert topk_overlap(s, t, mask, k=2) == 0


def test_co_ra_updates_adapter_only_and_uses_same_scored_batch():
    class AdapterModel(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.base = torch.nn.Linear(3, 40)
            self.base.requires_grad_(False)
            self.adapter = torch.nn.Linear(3, 40, bias=False)
            torch.nn.init.zeros_(self.adapter.weight)

        def forward(self, x):
            return self.base(x) + self.adapter(x)

    torch.manual_seed(42)
    student, teacher = torch.nn.Linear(3, 40), AdapterModel()
    x = torch.randn(2, 4, 3)
    base = teacher.base.weight.detach().clone()
    student_before = student.weight.detach().clone()
    result = co_ra_step(student, teacher,
                        torch.optim.AdamW(student.parameters(), lr=.01),
                        torch.optim.AdamW(teacher.adapter.parameters(), lr=.01),
                        student_logits_fn=lambda: student(x), teacher_logits_fn=lambda: teacher(x),
                        actions=torch.randint(40, (2, 4)), mask=torch.ones(2, 4),
                        verifier_advantage=torch.tensor([1., -1.]))
    assert torch.equal(teacher.base.weight, base)
    assert not torch.equal(student.weight, student_before)
    assert teacher.adapter.weight.abs().sum() > 0
    assert result["guidance_mean_error"] < 1e-5
