"""ECHO selector supervision only: detached per-target CE and boundary loss.

Not a full ECHO ranker, live teacher pipeline, TWIN index or shared store.
"""
from __future__ import annotations

import math
import torch
from torch import Tensor
import torch.nn.functional as F


def selector_losses(student: Tensor, teacher: Tensor, valid: Tensor, *, keep: int,
                    pairs: int, temperature=1.0, mining_temperature=.5,
                    ranking_temperature=1.0, margin=0.0, epsilon=1e-8):
    if student.ndim != 2 or student.shape != teacher.shape or valid.shape != student.shape:
        raise ValueError("[user-target samples, history] tensors required")
    if valid.dtype != torch.bool or student.device != teacher.device or valid.device != student.device:
        raise ValueError("boolean mask on the same device required")
    if (student.dtype != teacher.dtype or not student.is_floating_point()
            or not torch.isfinite(student).all() or not torch.isfinite(teacher).all()):
        raise ValueError("finite same-dtype scores required")
    params = (temperature, mining_temperature, ranking_temperature, epsilon)
    if (any(not math.isfinite(x) or x <= 0 for x in params)
            or not mining_temperature < temperature or not math.isfinite(margin)
            or not isinstance(keep, int) or isinstance(keep, bool) or keep < 1
            or not isinstance(pairs, int) or isinstance(pairs, bool) or pairs < 1
            or student.shape[0] < 1 or torch.any(valid.sum(-1) < keep)):
        raise ValueError("invalid budgets, temperatures or empty history")
    # 100K histories overflow half-precision sums; epsilon also underflows in
    # fp16. Accumulate all probability/loss statistics in at least fp32 while
    # keeping the differentiable cast back to the original student tensor.
    work_student = student.float() if student.dtype in (torch.float16, torch.bfloat16) else student
    work_teacher = teacher.detach().to(work_student.dtype)
    student_masked = work_student.masked_fill(~valid, -torch.inf)
    teacher_masked = work_teacher.masked_fill(~valid, -torch.inf)
    target = (teacher_masked / temperature).softmax(-1)
    log_student = (student_masked / temperature).log_softmax(-1)
    ce = -(target * log_student.masked_fill(~valid, 0)).sum(-1).mean() * temperature**2
    with torch.no_grad():
        selected = torch.argsort(student_masked, dim=-1, descending=True, stable=True)[:, :keep]
        mining = (teacher_masked / mining_temperature).softmax(-1)
    numerator = work_student[:, :0].sum()
    denominator = work_student.new_zeros(())
    active_pairs = 0
    for row in range(len(student)):
        inside = selected[row]
        outside_mask = valid[row].clone()
        outside_mask[inside] = False
        outside = torch.where(outside_mask)[0]
        n = min(pairs, len(inside), len(outside))
        if not n:
            continue
        positive = outside[torch.argsort(mining[row, outside], descending=True, stable=True)[:n]]
        negative = inside[torch.argsort(mining[row, inside], stable=True)[:n]]
        weight = (mining[row, positive] - mining[row, negative]).clamp_min(0).detach()
        numerator = numerator + (weight * F.softplus(
            (work_student[row, negative] - work_student[row, positive] + margin) / ranking_temperature)).sum()
        denominator = denominator + weight.sum()
        active_pairs += int(torch.count_nonzero(weight))
    return {"kd": ce, "auxiliary": numerator / (denominator + epsilon),
            "selected_indices": selected, "active_pairs": active_pairs}
