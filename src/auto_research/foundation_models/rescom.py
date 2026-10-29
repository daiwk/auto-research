"""ResCom v1 Eqs.1--6: streaming output-aware residual correction.

Only the closed-form linear calibration branch is implemented. The caller
supplies residuals and targets from ONE frozen calibrated host, before attaching
any correction. This is not a quantizer, native low-bit kernel or LLM benchmark.
"""
from dataclasses import dataclass
import math

import torch
from torch import Tensor

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/rescom-a100-20261029.json"


def _finite(x: Tensor, ndim: int) -> None:
    if (x.ndim != ndim or not 0 < x.numel() <= 1_048_576
            or x.dtype not in (torch.float32, torch.float64)
            or not bool(torch.isfinite(x).all())):
        raise ValueError("bounded finite float32/float64 tensor required")


@dataclass(frozen=True)
class ResidualMoments:
    """Unnormalized centered moments, merged without retaining calibration rows."""
    count: int
    mean_d: Tensor
    mean_e: Tensor
    gram: Tensor
    cross: Tensor

    @classmethod
    def from_batch(cls, residuals: Tensor, errors: Tensor):
        _finite(residuals, 2)
        _finite(errors, 2)
        if (errors.shape[0] != residuals.shape[0] or errors.device != residuals.device
                or errors.dtype != residuals.dtype):
            raise ValueError("aligned calibration pairs required")
        d, e = residuals.detach(), errors.detach()
        md, me = d.mean(0), e.mean(0)
        dc, ec = d - md, e - me
        return cls(len(d), md, me, dc.T @ dc, ec.T @ dc)

    def merge(self, other: "ResidualMoments") -> "ResidualMoments":
        for a, b in zip((self.mean_d, self.mean_e, self.gram, self.cross),
                        (other.mean_d, other.mean_e, other.gram, other.cross)):
            if a.shape != b.shape or a.dtype != b.dtype or a.device != b.device:
                raise ValueError("moment schemas must agree")
        total = self.count + other.count
        dd, de = other.mean_d - self.mean_d, other.mean_e - self.mean_e
        scale = self.count * other.count / total
        return ResidualMoments(total,
            self.mean_d + dd * (other.count / total),
            self.mean_e + de * (other.count / total),
            self.gram + other.gram + scale * torch.outer(dd, dd),
            self.cross + other.cross + scale * torch.outer(de, dd))


@dataclass(frozen=True)
class ResidualCorrection:
    u: Tensor
    v: Tensor
    bias: Tensor

    def __call__(self, residuals: Tensor) -> Tensor:
        _finite(residuals, 2)
        if (residuals.shape[1] != self.v.shape[1] or residuals.device != self.v.device
                or residuals.dtype != self.v.dtype):
            raise ValueError("correction coordinates/dtype/device must match calibration")
        return (residuals @ self.v.T) @ self.u.T + self.bias


def fit_residual_correction(moments: ResidualMoments, *, rank: int,
                            ridge: float) -> ResidualCorrection:
    """Eq.6, with UNNORMALIZED G/C and positive ridge; no host mutation."""
    if (not isinstance(moments, ResidualMoments)
            or isinstance(moments.count, bool) or not isinstance(moments.count, int) or moments.count < 1
            or isinstance(rank, bool) or not isinstance(rank, int)
            or isinstance(ridge, bool) or not math.isfinite(ridge) or ridge <= 0):
        raise ValueError("integer rank and finite positive ridge required")
    for x, ndim in ((moments.mean_d, 1), (moments.mean_e, 1),
                    (moments.gram, 2), (moments.cross, 2)):
        _finite(x, ndim)
    n, m = moments.mean_d.numel(), moments.mean_e.numel()
    if (moments.count < 1 or not 0 <= rank <= min(n, m, moments.count)
            or moments.gram.shape != (n, n) or moments.cross.shape != (m, n)):
        raise ValueError("valid centered moment dimensions and rank budget required")
    base = moments.gram
    if any(x.device != base.device or x.dtype != base.dtype
           for x in (moments.mean_d, moments.mean_e, moments.cross)):
        raise ValueError("moment dtype and device must agree")
    tolerance = 1e-6 if base.dtype == torch.float32 else 1e-12
    if not torch.allclose(base, base.T, rtol=tolerance, atol=0):
        raise ValueError("centered Gram must be symmetric; no triangular reinterpretation")
    chol = torch.linalg.cholesky(base + ridge * torch.eye(n, dtype=base.dtype, device=base.device))
    whitened = torch.linalg.solve_triangular(chol, moments.cross.T, upper=False).T
    left, singular, right = torch.linalg.svd(whitened, full_matrices=False)
    u = left[:, :rank] * singular[:rank]
    v = torch.linalg.solve_triangular(chol.T, right[:rank].T, upper=True).T
    bias = moments.mean_e - u @ v @ moments.mean_d
    return ResidualCorrection(u.detach(), v.detach(), bias.detach())


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device not in ("cpu", "cuda") or device == "cuda" and not torch.cuda.is_available():
        raise ValueError("cpu or real available cuda required; no fallback")
    gen = torch.Generator(device=device).manual_seed(seed)
    args = {"generator": gen, "device": device, "dtype": torch.float64}
    x = torch.randn(48, 5, **args)
    d = x - torch.round(3 * x) / 3
    host = torch.randn(4, 2, **args) @ torch.randn(2, 5, **args)
    e = d @ host.T
    moments = ResidualMoments.from_batch(d, e)
    streamed = ResidualMoments.from_batch(d[:17], e[:17]).merge(ResidualMoments.from_batch(d[17:], e[17:]))
    stream_error = max((a - b).abs().max().item() for a, b in
        ((moments.gram, streamed.gram), (moments.cross, streamed.cross),
         (moments.mean_d, streamed.mean_d), (moments.mean_e, streamed.mean_e)))
    ridge = .01 * moments.gram.trace().item() / 5
    fit = fit_residual_correction(streamed, rank=2, ridge=ridge)
    full = fit_residual_correction(moments, rank=4, ridge=ridge)
    reference = torch.linalg.solve(moments.gram + ridge * torch.eye(5, device=device, dtype=d.dtype), moments.cross.T).T
    reference_error = (full.u @ full.v - reference).abs().max().item()
    test_x = torch.randn(19, 5, **args)
    test_d = test_x - torch.round(3 * test_x) / 3
    test_e = test_d @ host.T
    before, after = test_e.square().mean().item(), (test_e - fit(test_d)).square().mean().item()
    mean_error = (fit(d).mean(0) - e.mean(0)).abs().max().item()
    zero = fit_residual_correction(moments, rank=0, ridge=ridge)
    same_bin = torch.stack((torch.zeros(5, device=device, dtype=d.dtype),
                            torch.full((5,), .04, device=device, dtype=d.dtype)))
    checks = {"streamed_centered_moments_reference": stream_error < 1e-12,
        "full_rank_ridge_independent_reference": reference_error < 1e-11,
        "rank_budget_retained": int(torch.linalg.matrix_rank(fit.u @ fit.v)) <= 2,
        "intercept_matches_calibration_mean": mean_error < 1e-12,
        "heldout_activation_residual_error_reduced": after < before,
        "rank_zero_is_mean_only": torch.allclose(zero(test_d), e.mean(0).expand(19, -1)),
        "same_quantized_bin_retains_distinct_residual": bool(torch.equal(torch.round(3 * same_bin), torch.zeros_like(same_bin)))
            and not torch.allclose(fit(same_bin)[0], fit(same_bin)[1]),
        "calibration_factors_frozen": not any(t.requires_grad for t in (fit.u, fit.v, fit.bias))}
    if not all(checks.values()):
        raise RuntimeError(f"ResCom checks failed: {checks}")
    return {"seed": seed, "metrics": {"stream_reference_error": stream_error,
        "ridge_reference_error": reference_error, "mean_reference_error": mean_error,
        "heldout_error_before": before, "heldout_error_after": after,
        "correction_rank": int(torch.linalg.matrix_rank(fit.u @ fit.v)),
        "model_calls": 0}, "checks": checks}
