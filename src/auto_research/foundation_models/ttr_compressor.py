"""TTR-Compressor, arXiv:2610.31574v1 Eqs. 3--7 and 9.

Independent implementation from the paper, not copied from the upstream core
(29f643f1348a4b3893f4740433b1fc8b8c39b2e7, no explicit core license found).
This is the uniform-weight base compressor, without optional convolution, an
LLM, sparse-attention routing, or a vision/language backbone.
"""
from __future__ import annotations

import math

import torch
from torch import Tensor, nn
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/ttr-compressor-a100-20261024.json"


def ttr_compress(tokens: Tensor, target_vector: Tensor, ridge_logits: Tensor, *,
                 ridge_floor: float = 0.) -> Tensor:
    """Compress [...,T,d] to [...,d] using the exact dual Cholesky solve.

    Keys use token directions; scalar targets retain ORIGINAL token magnitudes.
    D=softplus(rho), with an optional explicit nonnegative floor. The paper's
    formula has floor zero; the fixed upstream implementation adds 0.01. No
    floor, jitter, truncation, pseudo-inverse, or detached solve is added silently.
    Float32/float64 only: this reference does not claim BF16 serving parity.
    """
    if (tokens.ndim < 2 or min(tokens.shape) < 1
            or tokens.dtype not in (torch.float32, torch.float64)):
        raise ValueError("nonempty float32/float64 tokens [...,T,d] required")
    if tokens.shape[-2] > 128 or tokens.shape[-1] > 4096 or tokens.numel() > 1048576:
        raise ValueError("cost gate: T<=128, d<=4096, at most 1048576 token scalars")
    dimension = tokens.shape[-1]
    for value, name in ((target_vector, "target vector"), (ridge_logits, "ridge logits")):
        if value.shape != (dimension,) or value.dtype != tokens.dtype or value.device != tokens.device:
            raise ValueError(f"{name} must be a matching-dtype/device vector of dimension d")
        if not bool(torch.isfinite(value).all()):
            raise ValueError(f"{name} must be finite")
    if not math.isfinite(ridge_floor) or ridge_floor < 0:
        raise ValueError("ridge_floor must be finite and nonnegative")
    if not bool(torch.isfinite(tokens).all()):
        raise ValueError("tokens must be finite")
    lengths = torch.linalg.vector_norm(tokens, dim=-1, keepdim=True)
    if not bool(torch.isfinite(lengths).all()) or bool((lengths <= 0).any()):
        raise ValueError("zero or numerically nonfinite token norm: normalized key undefined")
    keys = tokens / lengths
    targets = tokens @ target_vector
    diagonal = F.softplus(ridge_logits) + ridge_floor
    if not bool(torch.isfinite(diagonal).all()) or bool((diagonal <= 0).any()):
        raise ValueError("ridge diagonal must be strictly positive and finite")
    inverse_root = diagonal.rsqrt()
    whitened = keys * inverse_root
    gram = whitened @ whitened.transpose(-1, -2)
    dual = gram + torch.eye(tokens.shape[-2], device=tokens.device, dtype=tokens.dtype)
    if not bool(torch.isfinite(dual).all()) or not bool(torch.isfinite(targets).all()):
        raise ValueError("nonfinite regression system; no silent numerical fallback")
    factor, info = torch.linalg.cholesky_ex(dual)
    if bool((info != 0).any()) or not bool(torch.isfinite(factor).all()):
        raise ValueError("dual system numerically not positive definite; no silent jitter")
    coefficients = torch.cholesky_solve(targets.unsqueeze(-1), factor)
    summary = (whitened.transpose(-1, -2) @ coefficients).squeeze(-1) * inverse_root
    if not bool(torch.isfinite(summary).all()):
        raise ValueError("nonfinite compressed representation")
    return summary


class TTRCompressor(nn.Module):
    """2d trainable parameters: learned target projection and positive diagonal.

    This single-compressor module shares its parameters across token groups.
    Independent attention heads can own separate instances; no GQA integration
    or visual-group packing is implied by this reference.
    """
    def __init__(self, dimension: int, *, initial_ridge: float = .1,
                 ridge_floor: float = 0.):
        super().__init__()
        if not isinstance(dimension, int) or not 1 <= dimension <= 4096:
            raise ValueError("dimension must be an integer in [1,4096]")
        if not (math.isfinite(initial_ridge) and math.isfinite(ridge_floor)
                and initial_ridge > ridge_floor >= 0):
            raise ValueError("initial_ridge > ridge_floor >= 0, all finite, required")
        self.ridge_floor = float(ridge_floor)
        self.target_vector = nn.Parameter(torch.empty(dimension))
        self.ridge_logits = nn.Parameter(torch.empty(dimension))
        nn.init.normal_(self.target_vector, std=dimension ** -.5)
        # Stable inverse softplus, including very large positive initialization.
        value = initial_ridge - ridge_floor
        nn.init.constant_(self.ridge_logits, value + math.log(-math.expm1(-value)))

    def forward(self, tokens: Tensor) -> Tensor:
        return ttr_compress(tokens, self.target_vector, self.ridge_logits,
                            ridge_floor=self.ridge_floor)


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """Small tensor/outer-gradient diagnostic, not pretrained-model capability."""
    if device not in ("cpu", "cuda"):
        raise ValueError("diagnostic device must be cpu or cuda")
    if device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA unavailable; CPU fallback forbidden")
    generator = torch.Generator(device=device).manual_seed(seed)
    tokens = (torch.randn(4, 7, 12, generator=generator, device=device)
              * torch.linspace(.4, 2.0, 7, device=device)[None, :, None]).requires_grad_()
    target_vector = torch.randn(12, generator=generator, device=device).requires_grad_()
    rho = (torch.randn(12, generator=generator, device=device) * .2 - 1).requires_grad_()
    summary = ttr_compress(tokens, target_vector, rho)
    probe = torch.randn(4, 12, generator=generator, device=device)
    outer_loss = (summary * probe).sum()
    token_gradient, a_gradient, rho_gradient = torch.autograd.grad(outer_loss, (tokens, target_vector, rho))

    # Independent FP64 primal solve and Eq. 9 gradient references.
    x64 = tokens.detach().double()
    a64, rho64 = target_vector.detach().double(), rho.detach().double()
    keys = x64 / torch.linalg.vector_norm(x64, dim=-1, keepdim=True)
    diagonal = F.softplus(rho64)
    primal = keys.transpose(-1, -2) @ keys + torch.diag(diagonal)
    reference = torch.linalg.solve(primal, (keys.transpose(-1, -2) @ (x64 @ a64).unsqueeze(-1))).squeeze(-1)
    adjoint = torch.linalg.solve(primal, probe.double().unsqueeze(-1)).squeeze(-1)
    expected_a = (x64.transpose(-1, -2) @ (keys @ adjoint.unsqueeze(-1))).squeeze(-1).sum(0)
    expected_rho = (-rho64.sigmoid() * reference * adjoint).sum(0)
    primal_error = float((summary.detach().double() - reference).abs().max())
    a_error = float((a_gradient.double() - expected_a).abs().max())
    rho_error = float((rho_gradient.double() - expected_rho).abs().max())
    permutation = torch.tensor([6, 2, 0, 5, 1, 4, 3], device=device)
    permutation_error = float((ttr_compress(tokens, target_vector, rho)
                               - ttr_compress(tokens[:, permutation], target_vector, rho)).detach().abs().max())
    scale_error = float((ttr_compress(tokens * 2, target_vector, rho) - summary * 2).detach().abs().max())

    # Wrong normalized targets eliminate the intended token-magnitude response.
    wrong_targets = keys @ a64
    wrong = torch.linalg.solve(primal, keys.transpose(-1, -2) @ wrong_targets.unsqueeze(-1)).squeeze(-1)
    negative_control_gap = float((reference - wrong).abs().max())
    ridge_one = torch.full((2,), math.log(math.expm1(1.)), device=device)
    repeated = torch.tensor([[1., 0.]] * 5 + [[0., 1.]], device=device)
    saturation = ttr_compress(repeated, torch.ones(2, device=device), ridge_one)
    saturation_error = float((saturation - torch.tensor([5 / 6, 1 / 2], device=device)).abs().max())

    # An actual outer optimization step; data stay fixed, no pretrained model.
    trained_a = target_vector.detach().clone().requires_grad_()
    trained_rho = rho.detach().clone().requires_grad_()
    optimizer = torch.optim.SGD((trained_a, trained_rho), lr=1e-3)
    before = ttr_compress(tokens.detach(), trained_a, trained_rho).square().mean()
    optimizer.zero_grad()
    before.backward()
    optimizer.step()
    after = ttr_compress(tokens.detach(), trained_a, trained_rho).square().mean()
    changed_a = bool((trained_a.detach() != target_vector.detach()).any())
    changed_rho = bool((trained_rho.detach() != rho.detach()).any())
    checks = {"dual_matches_independent_primal": primal_error < 2e-5,
              "outer_a_gradient_eq9": a_error < 2e-4,
              "outer_rho_gradient_eq9": rho_error < 2e-4,
              "token_gradient_finite_nonzero": bool(torch.isfinite(token_gradient).all()) and float(token_gradient.norm()) > 0,
              "base_token_permutation_invariance": permutation_error < 2e-5,
              "unnormalized_target_scale_response": scale_error < 2e-5,
              "normalized_target_negative_control_differs": negative_control_gap > 1e-3,
              "repeated_evidence_closed_form": saturation_error < 2e-5,
              "actual_outer_step_updates_both_parameters": changed_a and changed_rho,
              "outer_step_finite_nonincreasing_fixture_loss": bool(torch.isfinite(after)) and float(after.detach()) <= float(before.detach()) + 1e-6}
    if not all(checks.values()):
        raise RuntimeError(f"TTR defining contract failed: {checks}")
    return {"seed": seed, "metrics": {
        "primal_dual_max_abs_error": primal_error,
        "a_gradient_max_abs_error": a_error, "rho_gradient_max_abs_error": rho_error,
        "permutation_max_abs_error": permutation_error, "global_scale_max_abs_error": scale_error,
        "normalized_target_negative_control_gap": negative_control_gap,
        "repeated_evidence_max_abs_error": saturation_error,
        "token_gradient_norm": float(token_gradient.norm()),
        "outer_fixture_loss_before": float(before.detach()), "outer_fixture_loss_after": float(after.detach()),
        "groups": 4, "tokens_per_group": 7, "dimension": 12, "outer_steps": 1},
        "checks": checks}
