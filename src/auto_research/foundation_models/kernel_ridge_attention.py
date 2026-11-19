"""KRA Fourier features and OU/recursive-ridge core, fixed v1 equations 2,5,6,10.

No causal-convolution frontend, trained LM, parallel scan kernel or throughput
claim is included. The dual solve is an independent diagnostic reference.
"""

import math
import torch

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/kernel-ridge-attention-a100-20261119-latest.json"


def _finite(*xs):
    if not all(
        isinstance(x, torch.Tensor) and x.is_floating_point() and torch.isfinite(x).all()
        for x in xs
    ):
        raise ValueError("finite floating tensors required")
    if len({(x.device, x.dtype) for x in xs}) != 1:
        raise ValueError("matching dtype/device required")


def fourier_features(x, frequencies):
    _finite(x, frequencies)
    if (
        x.ndim != 2
        or frequencies.ndim != 2
        or frequencies.shape[1] != x.shape[1]
        or not frequencies.shape[0]
    ):
        raise ValueError("expected [tokens,input] and [frequencies,input]")
    phase = x @ frequencies.T
    return torch.cat((phase.cos(), phase.sin()), -1) / math.sqrt(frequencies.shape[0])


def recurrent(keys, queries, values, clock, ridge=1.0, *, state=None):
    """Inclusive read-after-write core; state=(Theta,P) supports exact continuation."""
    _finite(keys, queries, values, clock)
    if (
        keys.ndim != 2
        or queries.shape != keys.shape
        or values.ndim != 2
        or values.shape[0] != keys.shape[0]
        or clock.shape != (keys.shape[0],)
        or keys.shape[1] == 0
        or values.shape[1] == 0
        or (clock < 0).any()
        or isinstance(ridge, bool)
        or not isinstance(ridge, (float, int))
        or not math.isfinite(ridge)
        or ridge <= 0
    ):
        raise ValueError("invalid recurrent dimensions/clock/ridge")
    eye = torch.eye(keys.shape[1], dtype=keys.dtype, device=keys.device)
    if state is None:
        theta = keys.new_zeros(keys.shape[1], values.shape[1])
        covariance = eye / ridge
    else:
        theta, covariance = state
        _finite(keys, theta, covariance)
        if theta.shape != (keys.shape[1], values.shape[1]) or covariance.shape != eye.shape:
            raise ValueError("state shape mismatch")
        if (
            not torch.allclose(covariance, covariance.T)
            or not (torch.linalg.eigvalsh(covariance) > 0).all()
        ):
            raise ValueError("state covariance must be symmetric positive definite")
    outputs = []
    for key, query, value, rho in zip(keys, queries, values, clock, strict=True):
        delta = torch.exp(-rho)
        predicted_theta = delta * theta
        predicted_p = delta.square() * covariance + (1 - delta.square()) * eye / ridge
        z = predicted_p @ key
        denominator = 1 + key @ z
        gain = z / denominator
        residual = value - predicted_theta.T @ key
        theta = predicted_theta + gain[:, None] * residual[None, :]
        covariance = predicted_p - z[:, None] * z[None, :] / denominator
        outputs.append(theta.T @ query)
    result = torch.stack(outputs) if outputs else values.new_empty(0, values.shape[1])
    return result, (theta, covariance)


def prefix_dual(keys, queries, values, clock, ridge=1.0):
    """Equation10 reference, deliberately O(T^3), never the serving path."""
    recurrent(keys, queries, values, clock, ridge)  # shared input validation
    times = clock.cumsum(0)
    outputs = []
    for t in range(len(keys)):
        k = keys[: t + 1]
        u = times[: t + 1]
        gram = (k @ k.T) * torch.exp(-(u[:, None] - u[None, :]).abs())
        cross = (k @ queries[t]) * torch.exp(-(times[t] - u))
        eye = torch.eye(t + 1, dtype=k.dtype, device=k.device)
        outputs.append(cross @ torch.linalg.solve(gram + ridge * eye, values[: t + 1]))
    return torch.stack(outputs) if outputs else values.new_empty(0, values.shape[1])


def diagnostic(seed, device="cpu"):
    if type(seed) is not int or seed < 0:
        raise ValueError("nonnegative integer seed required")
    generator = torch.Generator(device=device).manual_seed(seed)
    x = torch.randn(
        9, 3, generator=generator, device=device, dtype=torch.float64, requires_grad=True
    )
    omega = torch.randn(
        3, 3, generator=generator, device=device, dtype=torch.float64, requires_grad=True
    )
    q = torch.randn(9, 3, generator=generator, device=device, dtype=torch.float64)
    values = torch.randn(9, 2, generator=generator, device=device, dtype=torch.float64)
    clock = torch.linspace(0.01, 0.7, 9, device=device, dtype=torch.float64)
    keys, queries = fourier_features(x, omega), fourier_features(q, omega)
    out, state = recurrent(keys, queries, values, clock, 0.8)
    dual = prefix_dual(keys, queries, values, clock, 0.8)
    first, continuation = recurrent(keys[:4], queries[:4], values[:4], clock[:4], 0.8)
    second, _ = recurrent(keys[4:], queries[4:], values[4:], clock[4:], 0.8, state=continuation)
    out.square().sum().backward()
    # A scalar/uniform write or covariance decay without prior recovery changes the algorithm.
    no_clock, _ = recurrent(keys, queries, values, clock * 0, 0.8)
    error = (out - dual).abs().max().item()
    eig = torch.linalg.eigvalsh(state[1])
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "checks": {
            "dual_prefix_parity": error < 1e-10,
            "streaming_continuation": bool(
                torch.allclose(out, torch.cat((first, second)), atol=1e-12)
            ),
            "unit_norm_features": bool(
                torch.allclose(keys.square().sum(-1), torch.ones_like(clock))
            ),
            "covariance_bounds": bool((eig > 0).all() and (eig <= 1 / 0.8 + 1e-10).all()),
            "clock_changes_outputs": bool((out - no_clock).abs().max() > 1e-4),
            "learned_feature_gradients": bool(
                torch.isfinite(omega.grad).all() and omega.grad.abs().sum() > 1e-8
            ),
        },
        "metrics": {
            "dual_max_abs_error": error,
            "covariance_min_eigenvalue": eig.min().item(),
            "clock_ablation_max_difference": (out - no_clock).abs().max().item(),
        },
    }
