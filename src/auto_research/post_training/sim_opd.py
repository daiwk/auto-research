"""SimOPD's paired FIFO relational distillation, without feature projection."""
from __future__ import annotations

import math

import torch
from torch import Tensor
from torch.nn import functional as F


def pool_response_states(states: Tensor, response_mask: Tensor) -> Tensor:
    """Normalize each selected-layer/token vector, then mean over layers/tokens.

    states is [selected layer, response batch, position, hidden dimension].
    Zero vectors use PyTorch's finite normalization convention; empty responses
    are rejected. This does not align teacher and student feature coordinates.
    """
    if states.ndim != 4 or not states.is_floating_point() or min(states.shape) < 1:
        raise ValueError("nonempty floating [layer,batch,token,dim] states required")
    if response_mask.shape != states.shape[1:3] or response_mask.dtype != torch.bool:
        raise ValueError("aligned Boolean response mask required")
    if states.device != response_mask.device or not bool(response_mask.any(1).all()):
        raise ValueError("each response needs active tokens on the same device")
    active = response_mask[None, :, :, None]
    selected = torch.where(active, states, 0.)
    if not torch.isfinite(selected).all():
        raise ValueError("finite active hidden states required")
    normalized = F.normalize(selected, p=2, dim=-1, eps=torch.finfo(states.dtype).eps)
    return normalized.sum((0, 2)) / (response_mask.sum(1) * states.shape[0])[:, None]


class PairedMemoryBank:
    """Paired detached response states; query extraction must precede update.

    The caller is responsible for appending the pre-update representations only
    after optimization. IDs are retained to audit pairing and FIFO eviction.
    """
    def __init__(self, capacity: int = 2048):
        if type(capacity) is not int or capacity < 2:
            raise ValueError("paired bank capacity must be at least two")
        self.capacity = capacity
        self.student: Tensor | None = None
        self.teacher: Tensor | None = None
        self.ids: tuple[str, ...] = ()

    def __len__(self) -> int:
        return len(self.ids)

    def append(self, student: Tensor, teacher: Tensor, response_ids: tuple[str, ...]) -> None:
        if student.ndim != 2 or teacher.ndim != 2 or student.shape[0] != teacher.shape[0] or min(student.shape) < 1 or min(teacher.shape) < 1:
            raise ValueError("paired nonempty matrices required; hidden dimensions may differ")
        if not student.is_floating_point() or not teacher.is_floating_point() or student.device != teacher.device or student.dtype != teacher.dtype:
            raise ValueError("floating paired matrices with matching dtype on one device required")
        if not torch.isfinite(student).all() or not torch.isfinite(teacher).all():
            raise ValueError("finite bank representations required")
        if len(response_ids) != student.shape[0] or any(not isinstance(i, str) or not i for i in response_ids):
            raise ValueError("one response identity per paired entry required")
        if self.student is not None:
            if student.shape[1] != self.student.shape[1] or teacher.shape[1] != self.teacher.shape[1]:
                raise ValueError("bank feature dimensions cannot change")
            if student.device != self.student.device or teacher.device != self.teacher.device:
                raise ValueError("bank device cannot change")
            if student.dtype != self.student.dtype or teacher.dtype != self.teacher.dtype:
                raise ValueError("bank dtype cannot change")
            student = torch.cat((self.student, student.detach()))
            teacher = torch.cat((self.teacher, teacher.detach()))
        self.student = student.detach()[-self.capacity:].clone()
        self.teacher = teacher.detach()[-self.capacity:].clone()
        self.ids = (self.ids + tuple(response_ids))[-self.capacity:]

    def loss(self, student: Tensor, teacher: Tensor, *, temperature: float = .1) -> tuple[Tensor, dict]:
        """Forward KL(P_teacher || P_student), frozen bank and teacher query."""
        if len(self) < 2:
            raise ValueError("warm up the bank first; one entry has degenerate similarity distribution")
        if not 0 < temperature or not math.isfinite(temperature):
            raise ValueError("positive finite temperature required")
        if student.ndim != 2 or teacher.ndim != 2 or student.shape[0] != teacher.shape[0] or min(student.shape) < 1 or min(teacher.shape) < 1:
            raise ValueError("paired nonempty query matrices required")
        if not student.is_floating_point() or not teacher.is_floating_point() or student.dtype != teacher.dtype or student.dtype != self.student.dtype or teacher.dtype != self.teacher.dtype:
            raise ValueError("floating query dtypes must match their paired banks")
        if student.shape[1] != self.student.shape[1] or teacher.shape[1] != self.teacher.shape[1]:
            raise ValueError("queries must match their own bank dimensions")
        if student.device != self.student.device or teacher.device != self.teacher.device:
            raise ValueError("queries and banks must share a device")
        if not torch.isfinite(student).all() or not torch.isfinite(teacher).all():
            raise ValueError("finite query representations required")
        # Cross-model coordinates never interact, so unequal dimensions are fine.
        def log_distribution(query, bank):
            eps = torch.finfo(query.dtype).eps
            return ((F.normalize(query, dim=-1, eps=eps) @ F.normalize(bank, dim=-1, eps=eps).T) / temperature).log_softmax(-1)
        log_student = log_distribution(student, self.student.detach())
        log_teacher = log_distribution(teacher.detach(), self.teacher.detach()).detach()
        target = log_teacher.exp()
        loss = (target * (log_teacher - log_student)).sum(-1).mean()
        return loss, {"teacher_distribution": target, "student_distribution": log_student.detach().exp(),
                      "bank_response_ids": self.ids}
