"""Three-pass interpolated null calibration, arXiv:2609.17764 Eqs.4--7.

Scores must be produced using the paper's real-query/instruction-null/bare-null
passes with aligned document identities. No LLM, attention extractor or benchmark
is executed here; weight selection belongs to validation, never test labels.
"""
import math

import torch
from torch import Tensor

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/interpolated-null-calibration-a100-20261025.json"


def interpolated_null_calibration(query: Tensor, instruction_null: Tensor, bare_null: Tensor,
                                  *, weight: float) -> dict[str, Tensor]:
    """S = query - [lambda*instruction_null + (1-lambda)*bare_null].

    lambda0 is bare-null calibration, NOT no calibration. No sign, normalization,
    independent per-pass ranking or relevance-label adjustment is introduced.
    """
    if not math.isfinite(weight) or not 0 <= weight <= 1:
        raise ValueError("finite interpolation weight in [0,1] required")
    if query.ndim not in (1, 2) or min(query.shape) < 1 or query.numel() > 65536:
        raise ValueError("bounded [documents] or [queries,documents] score tensors required")
    for value in (query, instruction_null, bare_null):
        if (value.shape != query.shape or value.device != query.device or value.dtype != query.dtype
                or not value.is_floating_point() or not bool(torch.isfinite(value).all())):
            raise ValueError("aligned finite floating scores sharing dtype/device required")
    footprint = instruction_null - bare_null
    calibrated = query - (weight * instruction_null + (1 - weight) * bare_null)
    if not bool(torch.isfinite(footprint).all()) or not bool(torch.isfinite(calibrated).all()):
        raise ValueError("nonfinite calibration; no silent clamp")
    return {"scores": calibrated, "instruction_footprint": footprint,
            "ranking": calibrated.argsort(dim=-1, descending=True, stable=True)}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device not in ("cpu", "cuda") or device == "cuda" and not torch.cuda.is_available():
        raise ValueError("cpu or real available cuda required; no fallback")
    gen = torch.Generator(device=device).manual_seed(seed)
    q = torch.rand(3, 6, generator=gen, device=device, dtype=torch.float64).requires_grad_()
    ni = torch.rand(3, 6, generator=gen, device=device, dtype=torch.float64).requires_grad_()
    nb = torch.rand(3, 6, generator=gen, device=device, dtype=torch.float64).requires_grad_()
    result = interpolated_null_calibration(q, ni, nb, weight=.3)
    reference = (q - nb) - .3 * (ni - nb)
    error = (result["scores"] - reference).detach().abs().max().item()
    gradients = torch.autograd.grad(result["scores"].sum(), (q, ni, nb))
    gradient_error = max((a - b).abs().max().item() for a, b in zip(gradients, (1., -.3, -.7)))
    zero = interpolated_null_calibration(q, ni, nb, weight=0)["scores"]
    one = interpolated_null_calibration(q, ni, nb, weight=1)["scores"]
    endpoint_error = max((zero - (q - nb)).detach().abs().max().item(),
                         (one - (q - ni)).detach().abs().max().item())
    # A fixed analytic instruction-footprint fixture, not a relevance benchmark.
    c = torch.tensor([.8, .7], device=device, dtype=torch.float64)
    foot = torch.tensor([.5, 0.], device=device, dtype=torch.float64)
    bare = torch.tensor([.1, .1], device=device, dtype=torch.float64)
    r0 = interpolated_null_calibration(c, bare + foot, bare, weight=0)["ranking"]
    r1 = interpolated_null_calibration(c, bare + foot, bare, weight=1)["ranking"]
    checks = {"eq6_eq7_decomposition": error < 1e-12,
              "exact_three_pass_gradient": gradient_error < 1e-12,
              "zero_and_one_endpoints": endpoint_error < 1e-12,
              "lambda0_is_not_no_calibration": (zero - q).detach().abs().max().item() > 0,
              "instruction_footprint_can_change_ranking": not torch.equal(r0, r1)}
    if not all(checks.values()):
        raise RuntimeError(f"interpolated calibration contract failed: {checks}")
    return {"seed": seed, "metrics": {"decomposition_error": error, "gradient_error": gradient_error,
        "endpoint_error": endpoint_error, "bare_null_negative_control_gap": (zero - q).detach().abs().max().item(),
        "queries": 3, "documents_per_query": 6, "passes": 3, "pretrained_model_calls": 0}, "checks": checks}
