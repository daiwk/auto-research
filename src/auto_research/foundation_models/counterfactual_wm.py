"""Observed-outcome residual reuse (Counterfactual WM v1 equations6–10).

This operator does not learn/identify a world model or assert causal conditions.
The same-event factual outcome is a required input, not an unavailable future.
"""

import torch

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/counterfactual-wm-a100-20261119-latest.json"


def residual_reuse(observed, factual_prediction, alternative_prediction):
    items = (observed, factual_prediction, alternative_prediction)
    if (
        not all(
            isinstance(x, torch.Tensor)
            and x.is_floating_point()
            and x.numel()
            and torch.isfinite(x).all()
            for x in items
        )
        or len({(x.shape, x.dtype, x.device) for x in items}) != 1
    ):
        raise ValueError(
            "finite equal-shape/dtype/device floating tensors required; no broadcasting"
        )
    return observed + alternative_prediction - factual_prediction


def readout_transport(readout, observed, factual_prediction, alternative_prediction):
    """Equation7, deliberately read out all terms before residual arithmetic."""
    residual_reuse(observed, factual_prediction, alternative_prediction)
    return residual_reuse(
        readout(observed), readout(factual_prediction), readout(alternative_prediction)
    )


def diagnostic(seed, device="cpu"):
    if type(seed) is not int or seed < 0:
        raise ValueError("nonnegative integer seed required")
    g = torch.Generator(device=device).manual_seed(seed)
    options = {"generator": g, "device": device, "dtype": torch.float64}
    factual, alternative, noise = (torch.randn(16, 2, **options) for _ in range(3))
    observed = factual + noise
    transported = residual_reuse(observed, factual, alternative)
    truth = alternative + noise
    error = (transported - truth).abs().max().item()
    # Gain faults are action–disturbance interactions, not an additive shared residual.
    gain = 1 + 0.3 * noise
    faulty_observed, faulty_truth = gain * factual, gain * alternative
    faulty_result = residual_reuse(faulty_observed, factual, alternative)
    interaction_error = (faulty_result - faulty_truth).square().mean().item()
    # Nonlinear output coordinates do not commute with residual transport.
    post_readout = transported.square()
    pre_readout = readout_transport(torch.square, observed, factual, alternative)
    coordinate_difference = (post_readout - pre_readout).abs().max().item()
    differentiable = factual.clone().requires_grad_()
    result = residual_reuse(observed, differentiable, alternative)
    result.sum().backward()
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "checks": {
            "additive_exactness": error < 1e-12,
            "multiplicative_fault_not_hidden": interaction_error > 1e-4,
            "readout_coordinates_not_interchangeable": coordinate_difference > 1e-3,
            "factual_gradient_sign": bool(
                torch.equal(differentiable.grad, -torch.ones_like(factual))
            ),
            "identity_action_preserves_observation": bool(
                torch.allclose(residual_reuse(observed, factual, factual), observed)
            ),
        },
        "metrics": {
            "additive_max_abs_error": error,
            "multiplicative_fault_mse": interaction_error,
            "coordinate_order_max_difference": coordinate_difference,
        },
    }
