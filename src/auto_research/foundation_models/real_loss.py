"""REAL v1 Eq. 9, 15, 16, 19 on externally supplied target-sampled blocks.

This is a differentiable loss reference, not a target/drafter or serving system.
"""
from __future__ import annotations

import torch
from torch import Tensor

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/real-loss-a100-20261112.json"


def eal_terms(draft_logits: Tensor, target_logits: Tensor, tokens: Tensor,
              valid: Tensor) -> dict[str, Tensor]:
    """Return per-block estimators; tokens MUST be sampled from the frozen target.

    Shapes are [blocks, fixed gamma, vocabulary] and [blocks, fixed gamma].
    The caller includes EOS itself and masks only subsequent positions. Prefix
    contiguity is enforced; mask length never changes the fixed-gamma divisor.
    """
    if (draft_logits.ndim != 3 or draft_logits.shape != target_logits.shape
            or min(draft_logits.shape) < 1 or draft_logits.shape[-1] < 2
            or not draft_logits.is_floating_point() or not target_logits.is_floating_point()
            or draft_logits.device != target_logits.device
            or draft_logits.dtype != target_logits.dtype
            or not torch.isfinite(draft_logits).all() or not torch.isfinite(target_logits).all()
            or tokens.shape != draft_logits.shape[:2] or valid.shape != tokens.shape
            or tokens.device != draft_logits.device or valid.device != draft_logits.device
            or tokens.dtype != torch.long or valid.dtype != torch.bool
            or torch.any((tokens < 0) | (tokens >= draft_logits.shape[-1]))
            or not valid.any(-1).all() or torch.any(valid[:, 1:] & ~valid[:, :-1])):
        raise ValueError("finite aligned logits, target tokens, and nonempty prefix masks required")
    log_q = draft_logits.log_softmax(-1)
    log_p = target_logits.detach().log_softmax(-1)
    sampled_q = log_q.gather(-1, tokens[..., None]).squeeze(-1)
    sampled_p = log_p.gather(-1, tokens[..., None]).squeeze(-1)
    # Training ratio q/p on target samples is NOT the serving p/q ratio.
    log_b = torch.where(valid, (sampled_q - sampled_p).clamp(max=0), 0)
    weights = log_b.cumsum(-1).exp()
    previous_weights = torch.cat((torch.ones_like(weights[:, :1]), weights[:, :-1]), -1)
    overlap = torch.where(valid, torch.minimum(log_q.exp(), log_p.exp()).sum(-1), 0)
    return {
        "branch": (previous_weights * overlap).sum(-1),
        "path": (weights * valid).sum(-1),
        "wtv": overlap.cumprod(-1).sum(-1),
        "ce": -(sampled_q * valid).sum() / valid.sum(),
        "path_weights": weights,
        "overlap": overlap,
    }


def real_loss(draft_logits: Tensor, target_logits: Tensor, tokens: Tensor,
              valid: Tensor, mixture: float = 0.9) -> Tensor:
    """Eq. 19. Both prefix path weights and overlap retain draft gradients."""
    if type(mixture) not in (float, int) or not 0 <= mixture <= 1:
        raise ValueError("finite mixture in [0,1] required")
    terms = eal_terms(draft_logits, target_logits, tokens, valid)
    return (mixture * (1 - terms["branch"].mean() / draft_logits.shape[1])
            + (1 - mixture) * terms["ce"])


def counterexample(theta: Tensor, first_probability: Tensor) -> tuple[dict[str, Tensor], Tensor]:
    """All four target paths of paper Eq.13, not a learned-model evaluation."""
    if theta.ndim or first_probability.ndim or theta.device != first_probability.device:
        raise ValueError("same-device scalar probabilities required")
    if not (0.1 < float(theta.detach()) < 0.9 and 0.4 < float(first_probability.detach()) < 1):
        raise ValueError("parameters must stay inside the counterexample's smooth region")
    p1 = theta.new_tensor([0.4, 0.6])
    q1 = torch.stack((first_probability, 1 - first_probability))
    q2 = torch.stack((theta, 1 - theta))
    target = torch.stack([torch.stack((p1, theta.new_tensor(p2)))
                          for p2 in ([0.9, 0.1], [0.9, 0.1], [0.1, 0.9], [0.1, 0.9])])
    draft = torch.stack((q1, q2))[None].expand(4, -1, -1)
    tokens = torch.tensor([[0, 0], [0, 1], [1, 0], [1, 1]], device=theta.device)
    terms = eal_terms(draft.log(), target.log(), tokens, torch.ones_like(tokens, dtype=torch.bool))
    probabilities = theta.new_tensor([0.36, 0.04, 0.06, 0.54])
    return {key: (probabilities * terms[key]).sum() for key in ("branch", "path", "wtv")}, target


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device not in {"cpu", "cuda"} or (device == "cuda" and not torch.cuda.is_available()):
        raise ValueError("available CPU or real CUDA required")
    torch.manual_seed(seed)
    theta = torch.tensor(0.5, device=device, dtype=torch.float64, requires_grad=True)
    first = torch.tensor(0.8, device=device, dtype=torch.float64, requires_grad=True)
    values, _ = counterexample(theta, first)
    exact_gradient = torch.autograd.grad(values["branch"], theta, retain_graph=True)[0]
    proxy_gradient = torch.autograd.grad(values["wtv"], theta, retain_graph=True)[0]
    prefix_gradient = torch.autograd.grad(values["branch"], first)[0]
    draft = torch.randn(3, 4, 5, device=device, dtype=torch.float64, requires_grad=True)
    target = torch.randn_like(draft, requires_grad=True)
    tokens = target.detach().softmax(-1).reshape(-1, 5).multinomial(1).reshape(3, 4)
    valid = torch.tensor([[1, 1, 1, 1], [1, 1, 0, 0], [1, 0, 0, 0]],
                         device=device, dtype=torch.bool)
    loss = real_loss(draft, target, tokens, valid)
    loss.backward()
    return {
        "seed": seed, "device": str(draft.device), "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "metrics": {"counterexample_eal": float(values["branch"].detach()),
                    "exact_theta_gradient": float(exact_gradient),
                    "wtv_theta_gradient": float(proxy_gradient),
                    "prefix_parameter_gradient": float(prefix_gradient),
                    "synthetic_loss": float(loss.detach())},
        "checks": {"exact_path_and_branch_expectations": bool(torch.allclose(values["path"], values["branch"])),
                   "paper_value": abs(float(values["branch"].detach()) - .96) < 1e-10,
                   "opposite_surrogate_gradient": abs(float(exact_gradient) - .2) < 1e-10
                   and abs(float(proxy_gradient) + .12) < 1e-10,
                   "prefix_gradient_not_detached": abs(float(prefix_gradient) + 1.6) < 1e-10,
                   "target_frozen": target.grad is None,
                   "draft_gradient_finite": draft.grad is not None and bool(torch.isfinite(draft.grad).all()),
                   "actual_tensor_device": draft.device.type == device},
    }
