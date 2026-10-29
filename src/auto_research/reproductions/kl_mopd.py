"""KL-MOPD Eqs.3.1–3.3, not a recommender or on-policy sampler.

Calibration prefixes must be sampled externally from the frozen INITIAL student;
training prefixes from the current student. This tensor kernel cannot attest to
either provenance. Both full-vocabulary teachers and calibrated weights freeze.
"""
from __future__ import annotations

import torch
from torch import Tensor

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/kl-mopd-a100-20261029.json"


def _logs(logits: Tensor, mask: Tensor) -> Tensor:
    if (logits.ndim != 3 or min(logits.shape) < 1 or logits.shape[-1] < 2
            or logits.numel() > 1_048_576 or not logits.is_floating_point()
            or mask.dtype != torch.bool or mask.device != logits.device
            or mask.shape != logits.shape[:2] or not bool(mask.any(1).all())):
        raise ValueError("bounded logits[B,T,V>=2] and nonempty Boolean masks required")
    if not bool(torch.isfinite(logits[mask]).all()):
        raise ValueError("active logits must be finite")
    dtype = torch.float32 if logits.dtype in (torch.float16, torch.bfloat16) else logits.dtype
    result = torch.where(mask[..., None], logits.to(dtype), 0.).log_softmax(-1)
    if not bool(torch.isfinite(result).all()):
        raise ValueError("log probabilities must be representable")
    return result


def _teacher_logs(student: Tensor, teachers: Tensor, mask: Tensor) -> Tensor:
    if (teachers.shape != (2, *student.shape) or teachers.device != student.device
            or teachers.dtype != student.dtype):
        raise ValueError("exactly two aligned full-vocabulary teacher logits required")
    return torch.stack([_logs(t.detach(), mask) for t in teachers])


@torch.no_grad()
def calibrate_weights(initial_student_logits: Tensor, teacher_logits: Tensor,
                      mask: Tensor) -> dict[str, Tensor]:
    """Estimate E_initial[KL(initial || teacher)] per position, ONCE.

    Valid prefixes are equally weighted within each position, not pooled across
    positions. The paper assumes both discrepancies strictly positive; exact
    zero is rejected instead of inventing an epsilon/uniform fallback.
    """
    p = _logs(initial_student_logits.detach(), mask)
    q = _teacher_logs(initial_student_logits, teacher_logits, mask)
    if not bool(mask.any(0).all()):
        raise ValueError("every calibrated token position needs observations")
    pointwise = (p.exp()[None] * (p[None] - q)).sum(-1).clamp_min(0.)
    discrepancy = (pointwise * mask[None]).sum(1) / mask.sum(0)[None]
    if not bool(torch.isfinite(discrepancy).all()) or not bool((discrepancy > 0).all()):
        raise ValueError("paper requires positive representable discrepancies for both teachers")
    # Both finite discrepancies may overflow when added in float32. Scaling
    # by the shared positive maximum preserves Eq3.2 without adding epsilon.
    scaled = discrepancy / discrepancy.amax(0, keepdim=True)
    weights = scaled / scaled.sum(0, keepdim=True)
    if not bool(torch.isfinite(weights).all()) or not bool(((weights > 0) & (weights < 1)).all()):
        raise ValueError("positive calibrated proportions must be representable")
    return {"weights": weights.detach(), "discrepancy": discrepancy.detach()}


def kl_mopd_loss(student_logits: Tensor, teacher_logits: Tensor,
                 mask: Tensor, calibrated_weights: Tensor) -> Tensor:
    """Fixed calibrated alpha[j,t] times KL(student || teacher), sum t, mean B.

    No gradient through the sampling law, teacher or calibration. Does not
    silently recalibrate on current-student logits or substitute forward KL.
    """
    p = _logs(student_logits, mask)
    q = _teacher_logs(student_logits, teacher_logits, mask)
    a = calibrated_weights.detach()
    if (a.shape != (2, student_logits.shape[1]) or a.device != p.device
            or not a.is_floating_point() or not bool(torch.isfinite(a).all())
            or not bool((a > 0).all()) or not bool((a < 1).all())
            or not torch.allclose(a.sum(0), torch.ones_like(a[0]), atol=1e-6, rtol=1e-6)):
        raise ValueError("positive frozen alpha[2,T] summing to one per token required")
    pointwise = (p.exp()[None] * (p[None] - q)).sum(-1)
    return ((pointwise * a[:, None]).sum(0) * mask).sum(1).mean()


def diagnostic(seed: int, device: str = "cpu") -> dict:
    gen = torch.Generator(device=device).manual_seed(seed)
    initial = torch.randn(4, 3, 7, generator=gen, device=device, dtype=torch.float64)
    teachers = torch.randn(2, 4, 3, 7, generator=gen, device=device,
                           dtype=torch.float64, requires_grad=True)
    mask = torch.tensor([[1, 1, 1], [1, 1, 0], [1, 1, 1], [1, 0, 0]], device=device, dtype=torch.bool)
    alpha = calibrate_weights(initial, teachers, mask)["weights"]
    student = (initial + .2 * torch.randn(initial.shape, generator=gen, device=device,
                                         dtype=torch.float64)).requires_grad_()
    loss = kl_mopd_loss(student, teachers, mask, alpha)
    prob = student.softmax(-1)
    teacher_prob = teachers.detach().softmax(-1)
    reference = sum(sum(alpha[j, t] * (prob[b, t] * torch.log(
        prob[b, t] / teacher_prob[j, b, t])).sum()
        for j in range(2) for t in range(3) if mask[b, t]) for b in range(4)) / 4
    error = float((loss - reference).abs().detach())
    loss.backward()
    grad = student.grad.clone()
    before = float(loss.detach())
    with torch.no_grad():
        student -= .1 * grad
    after = float(kl_mopd_loss(student, teachers, mask, alpha).detach())
    changed = calibrate_weights(student.detach(), teachers, mask)["weights"]
    wrong_forward = ((teacher_prob * (teacher_prob.log() - prob.detach().log()[None])).sum(-1)
                     * alpha[:, None] * mask[None]).sum() / 4
    checks = {"probability_reference": error < 1e-12,
              "teachers_frozen": teachers.grad is None,
              "calibration_frozen": not alpha.requires_grad,
              "padding_zero_gradient": bool((grad[~mask] == 0).all()),
              "real_student_update": bool(grad.norm() > 0) and after < before,
              "dynamic_recalibration_negative_control": bool((changed - alpha).abs().max() > 1e-7),
              "reverse_kl_direction": abs(float(wrong_forward) - before) > 1e-5}
    return {"seed": seed, "metrics": {"reference_error": error, "loss_before": before,
             "loss_after": after, "gradient_norm": float(grad.norm()),
             "weight_sum_error": float((alpha.sum(0) - 1).abs().max())}, "checks": checks}
