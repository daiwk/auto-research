"""2610.36520v1 Eqs.4--6/9: plain-key folding and value-refit subcomponents.

The caller supplies actually selected keys, fitted AM biases and full-cache
reference outputs. AM selection/NNLS, model prefill, vLLM connectors, paged
caches and native speed claims are absent. No full KV-compaction path is implied.
"""
import math

import torch
from torch import Tensor

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/fold-bias-a100-20261030.json"


def _finite(x: Tensor, ndim: int) -> None:
    if (x.ndim != ndim or not 0 < x.numel() <= 1_048_576
            or x.dtype not in (torch.float32, torch.float64)
            or not bool(torch.isfinite(x).all())):
        raise ValueError("bounded finite float32/float64 tensor required")


def fit_direction(context_queries: Tensor, *, ridge_ratio: float = .01) -> dict:
    """Eq.6 with covariance divided by N, lambda=ratio*trace(Sigma)/d.

    Zero-mean or zero-spread/singular fits fail closed; no arbitrary fallback
    direction, extra epsilon or normalization of future queries is invented.
    """
    _finite(context_queries, 2)
    if context_queries.shape[1] ** 2 > 1_048_576:
        raise ValueError("bounded derived covariance required")
    if isinstance(ridge_ratio, bool) or not math.isfinite(ridge_ratio) or ridge_ratio <= 0:
        raise ValueError("finite positive ridge ratio required")
    with torch.no_grad():
        q = context_queries.detach()
        mean = q.mean(0)
        centered = q - mean
        covariance = centered.T @ centered / len(q)
        _finite(covariance, 2)
        ridge = ridge_ratio * covariance.trace() / q.shape[1]
        if not bool(torch.isfinite(ridge)) or ridge <= 0:
            raise ValueError("nonzero context covariance required by the paper ridge rule")
        a = torch.linalg.solve(covariance + ridge * torch.eye(q.shape[1], device=q.device, dtype=q.dtype), mean)
        denominator = mean @ a
        if not bool(torch.isfinite(denominator)) or denominator <= 0:
            raise ValueError("nonzero mean and representable constrained direction required")
        direction = a / denominator
        _finite(direction, 1)
        return {"direction": direction, "mean": mean, "covariance": covariance, "ridge": ridge}


def fold_keys(keys: Tensor, biases: Tensor, direction: Tensor) -> Tensor:
    """Eq.4 before cache rounding, same head dimension and unchanged queries."""
    _finite(keys, 2)
    _finite(biases, 1)
    _finite(direction, 1)
    if (biases.shape != keys.shape[:1] or direction.shape != keys.shape[1:]
            or any(x.dtype != keys.dtype or x.device != keys.device for x in (biases, direction))):
        raise ValueError("aligned retained keys, per-entry biases and shared direction required")
    folded = keys + math.sqrt(keys.shape[1]) * biases[:, None] * direction
    _finite(folded, 2)
    return folded


def refit_rounded_cache(context_queries: Tensor, reference_queries: Tensor,
                        retained_keys: Tensor, biases: Tensor, reference_outputs: Tensor,
                        *, cache_dtype=torch.bfloat16, ridge_ratio: float = .01) -> dict:
    """Algorithm1: fit u -> fold K -> ACTUAL bf16 cast -> refit V.

    The Moore-Penrose solution handles rank-deficient reference attention. The
    returned values are fit-precision Eq.9 coefficients, NOT installed runtime
    cache blocks. Their eventual backend storage/rounding needs separate testing.
    """
    for x, n in ((context_queries, 2), (reference_queries, 2), (retained_keys, 2),
                 (biases, 1), (reference_outputs, 2)):
        _finite(x, n)
    dtype, device = context_queries.dtype, context_queries.device
    if (reference_queries.shape[1] != context_queries.shape[1]
            or len(reference_queries) * len(retained_keys) > 1_048_576
            or retained_keys.shape[1] != context_queries.shape[1]
            or biases.shape != retained_keys.shape[:1]
            or reference_outputs.shape[0] != reference_queries.shape[0]
            or any(x.dtype != dtype or x.device != device for x in
                   (reference_queries, retained_keys, biases, reference_outputs))
            or cache_dtype not in (torch.bfloat16, torch.float16)):
        raise ValueError("aligned context/reference/cache tensors and bf16/fp16 storage required")
    with torch.no_grad():
        fitted = fit_direction(context_queries, ridge_ratio=ridge_ratio)
        unrounded = fold_keys(retained_keys, biases, fitted["direction"])
        rounded = unrounded.to(cache_dtype)
        if not bool(torch.isfinite(rounded).all()):
            raise ValueError("folded keys overflow the declared cache precision")
        attention = (reference_queries @ rounded.to(dtype).T / math.sqrt(retained_keys.shape[1])).softmax(-1)
        _finite(attention, 2)
        values = torch.linalg.pinv(attention) @ reference_outputs
        _finite(values, 2)
        return {**fitted, "keys": rounded, "unrounded_keys": unrounded,
                "values": values, "reference_attention": attention}


def output_error_bound(query: Tensor, direction: Tensor, biases: Tensor, values: Tensor) -> Tensor:
    """Section3.3 general static-bias bound (range(beta)/4)*diam(V)*|q.u-1|.

    All compared entries must be supplied, including beta=0 for unbiased ones.
    This bound is for SAME values before/after the unrounded fold, not refit V.
    """
    _finite(query, 2)
    _finite(direction, 1)
    _finite(biases, 1)
    _finite(values, 2)
    if (len(values) ** 2 > 1_048_576 or query.shape[1:] != direction.shape or len(values) != len(biases)
            or any(x.dtype != query.dtype or x.device != query.device for x in (direction, biases, values))):
        raise ValueError("aligned queries, direction, static biases and same values required")
    diameter = torch.cdist(values, values).max()
    return .25 * (biases.max() - biases.min()) * diameter * (query @ direction - 1).abs()


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device not in ("cpu", "cuda") or device == "cuda" and not torch.cuda.is_available():
        raise ValueError("cpu or actual available cuda required; no fallback")
    gen = torch.Generator(device=device).manual_seed(seed)
    args = {"device": device, "dtype": torch.float64, "generator": gen}
    context = torch.randn(48, 6, **args) + torch.tensor([2., 1., -.5, .7, .3, -.2], device=device)
    query = context[:24]
    keys = torch.randn(5, 6, **args)
    beta = torch.randn(5, **args).clamp(-2, 2)
    values = torch.randn(5, 4, **args)
    target = torch.randn(24, 4, **args)
    fitted = refit_rounded_cache(context, query, keys, beta, target)
    direction = fitted["direction"]
    plain = query @ keys.T / math.sqrt(6)
    biased = plain + beta
    folded = query @ fitted["unrounded_keys"].T / math.sqrt(6)
    identity_error = (folded - plain - (query @ direction)[:, None] * beta).abs().max().item()
    mean_error = abs((context @ direction).mean().item() - 1)
    covariance = fitted["covariance"]
    ridge = fitted["ridge"]
    kkt = (covariance + ridge * torch.eye(6, device=device, dtype=context.dtype)) @ direction
    projection = (kkt @ fitted["mean"]) / fitted["mean"].square().sum()
    kkt_error = (kkt - projection * fitted["mean"]).abs().max().item()
    rounded_attention = fitted["reference_attention"]
    normal_error = (rounded_attention.T @ (rounded_attention @ fitted["values"] - target)).abs().max().item()
    wrong_attention = (query @ fitted["unrounded_keys"].T / math.sqrt(6)).softmax(-1)
    rounding_gap = (wrong_attention - rounded_attention).abs().max().item()
    output_error = ((folded.softmax(-1) - biased.softmax(-1)) @ values).norm(dim=-1)
    bounds = output_error_bound(query, direction, beta, values)
    drop_error = ((plain.softmax(-1) - biased.softmax(-1)) @ values).norm().item()
    checks = {"rank_one_logit_identity_reference": identity_error < 1e-12,
        "context_projection_mean_constraint": mean_error < 1e-12,
        "ridge_constrained_kkt_reference": kkt_error < 1e-12,
        "keys_really_rounded_before_value_refit": fitted["keys"].dtype == torch.bfloat16 and rounding_gap > 1e-8,
        "rounded_value_fit_normal_equations": normal_error < 1e-10,
        "same_value_output_error_bound": bool((output_error <= bounds + 1e-12).all()),
        "dropping_bias_changes_attention": drop_error > 1e-8,
        "offline_fit_is_frozen": not any(fitted[k].requires_grad for k in ("keys", "direction", "values"))}
    if not all(checks.values()):
        raise RuntimeError(f"FoldBias checks failed: {checks}")
    return {"seed": seed, "metrics": {"logit_identity_error": identity_error,
        "projection_mean_error": mean_error, "kkt_reference_error": kkt_error,
        "value_normal_equation_error": normal_error, "cache_rounding_attention_gap": rounding_gap,
        "drop_bias_output_error": drop_error, "minimum_output_bound_slack": (bounds - output_error).min().item(),
        "model_calls": 0}, "checks": checks}
