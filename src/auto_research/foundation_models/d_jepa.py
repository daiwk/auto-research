"""D-JEPA v1 Eq.3--8 single-context objective; no CLEVR or PID capability claim."""
from __future__ import annotations

import math

import torch
from torch import Tensor, nn
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/d-jepa-a100-20261115.json"


def _matrix(x: Tensor) -> None:
    if x.ndim != 2 or min(x.shape) < 2 or not torch.isfinite(x).all():
        raise ValueError("finite [batch>=2, features>=2] tensor required")


def correlation_penalty(private: Tensor, shared: Tensor, eps: float = 1e-5) -> Tensor:
    _matrix(private)
    _matrix(shared)
    if len(private) != len(shared) or not math.isfinite(eps) or eps <= 0:
        raise ValueError("matching batches and positive stabilizer required")
    a = (private - private.mean(0)) / (private.std(0) + eps)
    b = (shared - shared.mean(0)) / (shared.std(0) + eps)
    correlation = a.T @ b / (len(a) - 1)
    return correlation.square().sum() / max(a.shape[1], b.shape[1])


def independence(cv: Tensor, uv: Tensor, ct: Tensor, ut: Tensor) -> Tensor:
    # Intentionally NO correlation_penalty(uv, ut).
    return sum(correlation_penalty(u, c) for u, c in ((uv, cv), (ut, ct), (uv, ct), (ut, cv)))


def sigreg(x: Tensor, directions: Tensor) -> Tensor:
    """Author reference Epps--Pulley quadrature: 2*integral[0,3], 17 knots."""
    _matrix(x)
    if (directions.ndim != 2 or directions.shape[0] != x.shape[-1]
            or not torch.isfinite(directions).all() or torch.any(directions.norm(dim=0) == 0)):
        raise ValueError("finite nonzero random projection directions required")
    directions = F.normalize(directions, dim=0)
    t = torch.linspace(0, 3, 17, device=x.device, dtype=x.dtype)
    phase = (x @ directions).unsqueeze(-1) * t
    target = torch.exp(-0.5 * t.square())
    error = (phase.cos().mean(0) - target).square() + phase.sin().mean(0).square()
    return 2 * len(x) * torch.trapezoid(error * target, t, dim=-1).mean()


def objective(cv: Tensor, uv: Tensor, ct: Tensor, ut: Tensor, *, invariance_loss: Tensor,
              predicted_v: Tensor, target_v: Tensor, predicted_t: Tensor, target_t: Tensor,
              directions: Tensor, lambda_sig: float = .05,
              w_rec: float = 1.0, w_ind: float = .2) -> dict[str, Tensor]:
    """Paper-normalized four-subspace loss; caller supplies within-modality views.

    The author's multi-view training.py uses a different SIGReg averaging
    convention. This function follows Eq.5, not that entire training loop.
    Targets must be caller's other-view representations, not labels or answers.
    """
    for x in (cv, uv, ct, ut):
        _matrix(x)
    if (any(x.shape != cv.shape for x in (uv, ct, ut)) or not 0 <= lambda_sig <= 1
            or not all(math.isfinite(value) for value in (lambda_sig, w_rec, w_ind))
            or min(w_rec, w_ind) < 0 or invariance_loss.numel() != 1
            or not torch.isfinite(invariance_loss)):
        raise ValueError("matching subspaces, finite scalar invariance and valid weights required")
    if (predicted_v.shape != target_v.shape or predicted_t.shape != target_t.shape
            or len(predicted_v) != len(cv) or len(predicted_t) != len(cv)):
        raise ValueError("matched per-modality prediction targets required")
    cross = (2 - 2 * (F.normalize(cv, dim=-1) * F.normalize(ct, dim=-1)).sum(-1)).mean()
    regularizer = .5 * sum(sigreg(x, directions) for x in (cv, ct, uv, ut))
    reconstruction = F.mse_loss(predicted_v, target_v.detach()) + F.mse_loss(predicted_t, target_t.detach())
    independent = independence(cv, uv, ct, ut)
    total = ((1 - lambda_sig) * (invariance_loss + cross) + lambda_sig * regularizer
             + w_rec * reconstruction + w_ind * independent)
    return {"total": total, "cross": cross, "sigreg": regularizer,
            "reconstruction": reconstruction, "independence": independent}


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device not in {"cpu", "cuda"} or (device == "cuda" and not torch.cuda.is_available()):
        raise ValueError("available CPU or real CUDA device required")
    torch.manual_seed(seed)
    heads = nn.ModuleList([nn.Linear(12, 16), nn.Linear(12, 16),
                           nn.Linear(16, 12), nn.Linear(16, 12)]).to(device)
    inputs = [torch.randn(24, 12, device=device) for _ in range(2)]
    targets = [x.detach().clone().requires_grad_(True) for x in inputs]
    directions = torch.randn(8, 16, device=device)
    optimizer = torch.optim.AdamW(heads.parameters(), lr=.01)

    def evaluate():
        v, t = heads[0](inputs[0]), heads[1](inputs[1])
        cv, uv = v.chunk(2, -1)
        ct, ut = t.chunk(2, -1)
        return objective(cv, uv, ct, ut, invariance_loss=v.new_zeros(()),
                         predicted_v=heads[2](v), target_v=targets[0],
                         predicted_t=heads[3](t), target_t=targets[1], directions=directions)

    before = float(evaluate()["total"].detach())
    for _ in range(12):
        optimizer.zero_grad()
        evaluate()["total"].backward()
        optimizer.step()
    terms = evaluate()
    after = float(terms["total"].detach())
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"training_loss_before": before, "training_loss_after": after,
                        **{k: float(v.detach()) for k, v in terms.items() if k != "total"}},
            "checks": {"other_view_targets_stop_gradient": all(x.grad is None for x in targets),
                       "shared_private_heads_trainable": all(p.grad is not None for p in heads.parameters()),
                       "single_context_objective_optimized": after < before,
                       "finite_all_terms": all(bool(torch.isfinite(x)) for x in terms.values())}}
