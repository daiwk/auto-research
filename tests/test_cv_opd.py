import math

import pytest
import torch

from auto_research.multimodal.cv_opd import intersection_over_union, jsd, negative_crop, objective, topk_tail, verify_answer


def test_real_box_size_iou_and_impossible_crop():
    positive = (5, 5, 25, 25)
    negative = negative_crop((80, 80), positive, generator=torch.Generator().manual_seed(2))
    assert (negative[2] - negative[0], negative[3] - negative[1]) == (20, 20)
    assert intersection_over_union(positive, negative) <= .1
    with pytest.raises(ValueError, match="no same-size"):
        negative_crop((10, 10), (0, 0, 10, 10))


def test_jsd_symmetric_bounds_and_student_topk_tail_mass():
    p, q = torch.rand(2, 3, 7).softmax(-1), torch.rand(2, 3, 7).softmax(-1)
    distance = jsd(p.log(), q.log())
    torch.testing.assert_close(distance, jsd(q.log(), p.log()))
    assert (distance >= 0).all() and (distance <= math.log(2)).all()
    reduced_p, reduced_q = topk_tail(p.log(), q.log(), 2)
    torch.testing.assert_close(reduced_p.exp().sum(-1), torch.ones(2, 3))
    torch.testing.assert_close(reduced_q.exp().sum(-1), torch.ones(2, 3))
    support = p.topk(2, -1).indices
    torch.testing.assert_close(reduced_q[..., :2].exp(), q.gather(-1, support))


def test_sample_gate_keeps_incorrect_siblings_and_detaches_teacher():
    torch.manual_seed(2)
    student = torch.randn(4, 3, 6, requires_grad=True)
    positive = torch.randn(4, 3, 6, requires_grad=True)
    negative = torch.randn(4, 3, 6, requires_grad=True)
    mask = torch.ones(4, 3, dtype=torch.bool)
    loss, parts = objective(student, positive, negative, mask,
                             torch.tensor([True, False, False, False]),
                             torch.tensor([0, 0, 1, 1]), topk=2)
    assert parts["retained_samples"] == 1
    assert parts["retained_rollouts"] == 2  # don't wrongly retain only correct rollout
    assert parts["valid_tokens"] == 6
    loss.backward()
    assert positive.grad is None and negative.grad is None
    assert student.grad[:2].abs().sum() > 0
    assert student.grad[2:].abs().sum() == 0


def test_zero_correct_returns_real_zero_gradient_and_strict_batch_gate():
    student = torch.zeros(2, 3, 6, requires_grad=True)
    teacher = torch.zeros_like(student)
    loss, parts = objective(student, teacher, teacher, torch.ones(2, 3, dtype=torch.bool),
                             torch.zeros(2, dtype=torch.bool), torch.zeros(2, dtype=torch.long), topk=2)
    loss.backward()
    assert float(loss.detach()) == 0 and student.grad.abs().sum() == 0
    assert parts["gated_tokens"] == 0
    assert verify_answer("Yes, there is.", ["yes"])
    assert not verify_answer("No.", ["yes"])
    assert not verify_answer("unsure", ["yes"])
