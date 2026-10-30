"""MPOPD v2 Eqs.5,7--10: frozen rollout weighting and two KL objectives.

Tensor mechanism only: no LM, tokenizer, rollout sampler or teacher query.
The teacher top-k conditional support is explicit (AppendixA.2); importance
ratios use full-vocabulary sampled probabilities and lag one token (w_0=1).
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import torch
from torch import Tensor

REQUIRES_GPU_VALIDATION = True


def _aligned(*logits):
    first = logits[0]
    if first.ndim != 3 or min(first.shape) < 1 or first.shape[-1] < 2:
        raise ValueError("nonempty [batch,time,vocabulary>=2] logits required")
    for value in logits:
        if value.shape != first.shape or value.device != first.device or not value.is_floating_point():
            raise ValueError("aligned floating logits on one device required")


def _mask(mask, logits):
    if mask.shape != logits.shape[:2] or mask.dtype != torch.bool or mask.device != logits.device:
        raise ValueError("aligned Boolean response mask required")
    if not bool(mask[:, 0].all()) or bool((~mask[:, :-1] & mask[:, 1:]).any()):
        raise ValueError("nonempty contiguous response prefixes required")


def _log_probs(logits, mask):
    if not bool(torch.isfinite(logits[mask]).all()):
        raise ValueError("finite active logits required")
    dtype = torch.float32 if logits.dtype in (torch.float16, torch.bfloat16) else logits.dtype
    clean = torch.where(mask[..., None], logits.to(dtype), 0.)
    result = clean.log_softmax(-1)
    if not bool(torch.isfinite(result[mask]).all()):
        raise ValueError("active log probabilities must be representable")
    return result


def _eta(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError("finite tilt strength in [0,1] required")
    return float(value)


def tilted_log_target(student_logits, teacher_logits, mask, *, eta: float, top_k: int):
    """Eq.5/9: normalized geometric mixture on frozen teacher top-k support.

    Returns conditional log probabilities and their original vocabulary IDs.
    No sampled-token label is used to choose the support.
    """
    _aligned(student_logits, teacher_logits)
    _mask(mask, student_logits)
    eta = _eta(eta)
    if type(top_k) is not int or not 1 <= top_k <= student_logits.shape[-1]:
        raise ValueError("explicit teacher support size within vocabulary required")
    student = _log_probs(student_logits.detach(), mask)
    teacher = _log_probs(teacher_logits.detach(), mask)
    ids = teacher.topk(top_k, dim=-1).indices
    mixture = (1 - eta) * student.gather(-1, ids) + eta * teacher.gather(-1, ids)
    return mixture.log_softmax(-1).detach(), ids.detach()


@dataclass(frozen=True)
class RolloutWeights:
    prefix_weights: Tensor
    mask: Tensor
    clip: float

    def __post_init__(self):
        if isinstance(self.clip, bool) or not math.isfinite(self.clip) or self.clip <= 1:
            raise ValueError("finite C>1 required")
        if self.prefix_weights.ndim != 2 or min(self.prefix_weights.shape) < 1 or self.mask.shape != self.prefix_weights.shape or self.mask.dtype != torch.bool or self.mask.device != self.prefix_weights.device:
            raise ValueError("aligned prefix weights and Boolean mask required")
        if not self.prefix_weights.is_floating_point() or self.prefix_weights.requires_grad or not bool(self.mask[:, 0].all()) or bool((~self.mask[:, :-1] & self.mask[:, 1:]).any()):
            raise ValueError("detached floating weights on contiguous nonempty prefixes required")
        active = self.prefix_weights[self.mask]
        tolerance = 8 * torch.finfo(self.prefix_weights.dtype).eps * max(1., self.clip)
        if not bool(torch.isfinite(active).all()) or bool(((active < 1 / self.clip - tolerance) | (active > self.clip + tolerance)).any()) or not bool((self.prefix_weights[:, 0] == 1).all()):
            raise ValueError("lagged weights must start at1 and stay within [1/C,C]")
        object.__setattr__(self, "prefix_weights", torch.where(self.mask, self.prefix_weights, 0.).detach().clone())
        object.__setattr__(self, "mask", self.mask.detach().clone())


def freeze_rollout_weights(old_student_logits, old_proposal_logits, actions, mask, *, clip: float = 5.):
    """Eqs.7--8: detached ONE-step ratio, lagged to the next prefix.

    Not a product of all earlier ratios. First token always has weight1;
    the action at j weights KL at j+1. Snapshot probability comes from OLD
    rollout policies, not the differentiable student being updated.
    """
    _aligned(old_student_logits, old_proposal_logits)
    _mask(mask, old_student_logits)
    if isinstance(clip, bool) or not math.isfinite(clip) or clip <= 1:
        raise ValueError("finite importance clip C>1 required")
    if actions.shape != mask.shape or actions.dtype != torch.long or actions.device != mask.device:
        raise ValueError("aligned sampled action IDs required")
    if not bool(((actions[mask] >= 0) & (actions[mask] < old_student_logits.shape[-1])).all()):
        raise ValueError("active actions must be valid vocabulary IDs")
    clean_actions = torch.where(mask, actions, 0)[..., None]
    student = _log_probs(old_student_logits.detach(), mask).gather(-1, clean_actions).squeeze(-1)
    proposal = _log_probs(old_proposal_logits.detach(), mask).gather(-1, clean_actions).squeeze(-1)
    ratio = (student - proposal).clamp(-math.log(clip), math.log(clip)).exp()
    prefix = torch.cat([torch.ones_like(ratio[:, :1]), ratio[:, :-1]], dim=1)
    return RolloutWeights(torch.where(mask, prefix, 0.).detach().clone(), mask.detach().clone(), float(clip))


def student_loss(current_logits, teacher_logits, snapshot: RolloutWeights, *, top_k: int = 16):
    """Eq.7: mean trajectories of SUM tokens, reverse KL on teacher top-k.

    This is not token-mean. Teacher and old weights are frozen; only the
    current student's selected-support conditional distribution is trained.
    """
    _aligned(current_logits, teacher_logits)
    mask = snapshot.mask
    _mask(mask, current_logits)
    if snapshot.prefix_weights.shape != mask.shape or snapshot.prefix_weights.device != mask.device:
        raise ValueError("aligned frozen prefix weights required")
    if snapshot.prefix_weights.requires_grad or not bool(torch.isfinite(snapshot.prefix_weights[mask]).all()) or not bool((snapshot.prefix_weights[mask] > 0).all()):
        raise ValueError("finite positive detached frozen weights required")
    if type(top_k) is not int or not 1 <= top_k <= current_logits.shape[-1]:
        raise ValueError("explicit teacher support size within vocabulary required")
    full_student = _log_probs(current_logits, mask)
    full_teacher = _log_probs(teacher_logits.detach(), mask)
    ids = full_teacher.topk(top_k, dim=-1).indices
    logp = full_student.gather(-1, ids).log_softmax(-1)
    logt = full_teacher.gather(-1, ids).log_softmax(-1)
    divergence = (logp.exp() * (logp - logt)).sum(-1)
    value = (torch.where(mask, divergence, 0.) * snapshot.prefix_weights).sum(1).mean()
    if not bool(torch.isfinite(value)):
        raise ValueError("weighted distillation objective is not representable")
    return value


def proposal_loss(proposal_logits, updated_student_logits, teacher_logits, mask, *, eta: float, top_k: int = 16):
    """Eq.10: KL(proposal||new geometric target), not forward KL.

    Caller must initialize proposal parameters from the UPDATED student each
    round; logits alone cannot certify that initialization or actual rollouts.
    """
    _aligned(proposal_logits, updated_student_logits, teacher_logits)
    _mask(mask, proposal_logits)
    target, ids = tilted_log_target(updated_student_logits, teacher_logits, mask, eta=eta, top_k=top_k)
    logq = _log_probs(proposal_logits, mask).gather(-1, ids).log_softmax(-1)
    divergence = (logq.exp() * (logq - target)).sum(-1)
    value = torch.where(mask, divergence, 0.).sum(1).mean()
    if not bool(torch.isfinite(value)):
        raise ValueError("proposal objective is not representable")
    return value


def diagnostic(seed: int = 42, device: str = "cpu"):
    if type(seed) is not int or device not in ("cpu", "cuda"):
        raise ValueError("CPU or real CUDA numerical diagnostic required")
    generator = torch.Generator(device="cpu").manual_seed(seed)
    student = torch.randn((2, 4, 20), generator=generator, dtype=torch.float64).to(device)
    teacher = torch.randn((2, 4, 20), generator=generator, dtype=torch.float64).to(device).requires_grad_()
    old_proposal = (student + torch.randn((2, 4, 20), generator=generator, dtype=torch.float64).to(device)).requires_grad_()
    actions = torch.tensor([[0, 1, 2, 3], [4, 3, 2, -9]], device=device)
    mask = torch.tensor([[1, 1, 1, 1], [1, 1, 1, 0]], device=device, dtype=torch.bool)
    weights = freeze_rollout_weights(student, old_proposal, actions, mask)
    current = student.clone().requires_grad_()
    initial = student_loss(current, teacher, weights)
    initial.backward()
    grad = current.grad.detach().clone()
    with torch.no_grad():
        current -= .2 * grad
    after = student_loss(current, teacher, weights)
    proposal = current.detach().clone().requires_grad_()
    initial_proposal = proposal_loss(proposal, current, teacher, mask, eta=.4)
    initial_proposal.backward()
    pgrad = proposal.grad.detach().clone()
    with torch.no_grad():
        proposal -= .2 * pgrad
    after_proposal = proposal_loss(proposal, current, teacher, mask, eta=.4)
    target, ids = tilted_log_target(current, teacher, mask, eta=.4, top_k=16)
    s0, _ = tilted_log_target(current, teacher, mask, eta=0, top_k=16)
    s1, _ = tilted_log_target(current, teacher, mask, eta=1, top_k=16)
    student_ref = _log_probs(current.detach(), mask).gather(-1, ids).log_softmax(-1)
    teacher_ref = _log_probs(teacher.detach(), mask).gather(-1, ids).log_softmax(-1)
    arithmetic = ((1 - .4) * student_ref.exp() + .4 * teacher_ref.exp()).log()
    return {"seed": seed, "diagnostic_only": True,
        "metrics": {"student_loss_before": float(initial.detach()), "student_loss_after": float(after.detach()),
                    "proposal_loss_before": float(initial_proposal.detach()), "proposal_loss_after": float(after_proposal.detach()),
                    "student_gradient_norm": float(grad.norm()), "proposal_gradient_norm": float(pgrad.norm()),
                    "geometric_arithmetic_distance": float((target.exp() - arithmetic.exp()).abs().max()),
                    "active_tokens": int(mask.sum())},
        "checks": {"student_update_decreases_fixed_objective": bool(after < initial),
                   "proposal_update_decreases_fixed_objective": bool(after_proposal < initial_proposal),
                   "first_prefix_weight_one": bool((weights.prefix_weights[:, 0] == 1).all()),
                   "weights_detached": not weights.prefix_weights.requires_grad,
                   "teacher_and_old_proposal_frozen": teacher.grad is None and old_proposal.grad is None,
                   "padding_gradient_zero": bool((grad[~mask] == 0).all()),
                   "geometric_not_arithmetic": bool((target.exp() - arithmetic.exp()).abs().max() > 1e-5),
                   "eta_endpoints_match": bool(torch.allclose(s0, student_ref) and torch.allclose(s1, teacher_ref)),
                   "conditional_support_normalized": bool(torch.allclose(target.exp().sum(-1), torch.ones_like(mask, dtype=target.dtype)))}}
