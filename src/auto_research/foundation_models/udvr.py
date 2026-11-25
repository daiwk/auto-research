"""Fixed-v1 UDVR pair component (§3, Appendix C), CPU-only L1 diagnostics.

No Transformer retrofit, training sweep or claimed hyperparameter transfer.
FFN mode deliberately discards V's scale; it is not function-preserving.
"""

import math

import torch
from torch import nn
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = False


def _validate(u, diagonal, v, alpha, kind):
    if kind not in {"attention", "ffn"} or not math.isfinite(alpha) or alpha <= 0:
        raise ValueError("positive finite alpha and attention/ffn kind required")
    if not all(isinstance(x, torch.Tensor) for x in (u, diagonal, v)):
        raise ValueError("tensor factors required")
    if (u.ndim != 2 or not u.numel() or v.ndim != 2 or diagonal.ndim != 1
            or v.shape != (u.shape[1], u.shape[0]) or diagonal.shape != (u.shape[1],)
            or u.dtype not in {torch.float32, torch.float64}
            or any(x.device.type != "cpu" or x.dtype != u.dtype for x in (u, diagonal, v))
            or any(not torch.isfinite(x).all() for x in (u, diagonal, v))):
        raise ValueError("finite matching CPU FP32/FP64 d-by-r, r, r-by-d tensors required")


@torch.no_grad()
def rebalance(u, diagonal, v, *, alpha=.01, kind="attention"):
    """Return the post-update Algorithm1 factors without modifying the inputs."""
    _validate(u, diagonal, v, alpha, kind)
    target = alpha * math.sqrt(u.shape[0])
    s = torch.linalg.vector_norm(u, dim=0) / target
    rho = torch.linalg.vector_norm(v, dim=1) / target
    if not (s > 0).all() or not (rho > 0).all():
        raise ValueError("zero-norm directions cannot be rebalanced")
    new = (u / s, diagonal * s * (rho if kind == "attention" else 1.), v / rho[:, None])
    if any(not torch.isfinite(x).all() for x in new):
        raise ValueError("nonfinite rebalance is outside this component")
    return new


def learning_rates(width, ffn_width, *, alpha=.01, constant=.0217):
    """Eq4 uses all stacked heads, not one head's r, for attention."""
    if (type(width) is not int or type(ffn_width) is not int or min(width, ffn_width) <= 0
            or not math.isfinite(alpha) or alpha <= 0
            or not math.isfinite(constant) or constant <= 0):
        raise ValueError("positive dimensions and finite positive constants required")
    return {"attention": constant * alpha,
            "ffn": math.sqrt(ffn_width / width) * constant * alpha}


class UDVPair(nn.Module):
    """One natural pair with an optimizer-excluded diagonal buffer."""

    def __init__(self, u, v, *, kind="attention", alpha=.01):
        super().__init__()
        diagonal = u.new_ones(u.shape[1])
        _validate(u, diagonal, v, alpha, kind)
        self.kind, self.alpha = kind, alpha
        self.u = nn.Parameter(u.detach().clone())
        self.v = nn.Parameter(v.detach().clone())
        self.register_buffer("diagonal", diagonal)
        self.rebalance_()

    @torch.no_grad()
    def rebalance_(self):
        u, d, v = rebalance(self.u, self.diagonal, self.v, alpha=self.alpha, kind=self.kind)
        self.u.copy_(u)
        self.diagonal.copy_(d)
        self.v.copy_(v)

    def forward(self, x):
        _validate(self.u, self.diagonal, self.v, self.alpha, self.kind)
        if (not isinstance(x, torch.Tensor) or x.device.type != "cpu" or x.dtype != self.u.dtype
                or x.ndim < 1 or x.shape[-1] != self.u.shape[0] or not torch.isfinite(x).all()):
            raise ValueError("finite matching CPU inputs required")
        hidden = (x @ self.u) * self.diagonal
        return (hidden if self.kind == "attention" else F.gelu(hidden)) @ self.v

    def regularizer(self, gamma=1e-7):
        _validate(self.u, self.diagonal, self.v, self.alpha, self.kind)
        if not math.isfinite(gamma) or gamma < 0:
            raise ValueError("finite nonnegative gamma required")
        ud = self.u * self.diagonal
        if self.kind == "attention":
            return gamma * (ud.square().sum() + (self.diagonal[:, None] * self.v).square().sum())
        return 2 * gamma * (ud.square().sum() + self.v.square().sum())


def diagnostic(seed=42, device="cpu"):
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU-only device required")
    g = torch.Generator().manual_seed(seed)
    u = torch.randn(6, 4, generator=g, dtype=torch.float64)
    v = torch.randn(4, 6, generator=g, dtype=torch.float64)
    pair = UDVPair(u, v)
    initial_error = ((pair.u * pair.diagonal) @ pair.v - u @ v).abs().max().item()
    x = torch.randn(8, 6, generator=g, dtype=torch.float64)
    target = torch.randn(8, 6, generator=g, dtype=torch.float64)
    optimizer = torch.optim.Adam(pair.parameters(), lr=learning_rates(6, 24)["attention"])
    gradient_seen = False
    for _ in range(4):
        optimizer.zero_grad()
        loss = F.mse_loss(pair(x), target) + pair.regularizer()
        loss.backward()
        gradient_seen |= bool(pair.u.grad.abs().sum() > 0 and pair.v.grad.abs().sum() > 0)
        optimizer.step()
        pair.rebalance_()
    target_norm = pair.alpha * math.sqrt(6)
    norm_error = max((pair.u.norm(dim=0) - target_norm).abs().max().item(),
                     (pair.v.norm(dim=1) - target_norm).abs().max().item())
    ffn = UDVPair(u, v, kind="ffn")
    ffn_difference = (ffn(x) - F.gelu(x @ u) @ v).abs().max().item()
    return {"seed": seed, "device": device, "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            "checks": {"attention_initial_product_preserved": initial_error < 1e-12,
                       "factor_gradients_and_adam_run": gradient_seen,
                       "directions_pinned_after_updates": norm_error < 1e-12,
                       "diagonal_is_not_a_parameter": "diagonal" not in dict(pair.named_parameters()),
                       "ffn_projection_is_not_function_preserving": ffn_difference > 1e-6},
            "metrics": {"initial_product_max_error": initial_error, "post_step_norm_max_error": norm_error,
                        "ffn_noninvariance_max_difference": ffn_difference}}
