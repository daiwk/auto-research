"""ALPS paper-v1 Stage-2 geometry, query and frozen-target loss components.

The equations follow arXiv:2610.30120v1 and the Apache-2.0 author release at
30ab44b9fcdf3253fc67f5a53e31ea5141eb45c1 (Copyright 2026 The ALPS Authors).
No ViT encoder, cross-view transformer predictor, checkpoint or training data
is substituted: callers supply their real predicted/teacher patch tokens.
The bounded diagnostic uses random tensors, is L1 only, and cannot establish
trained-encoder performance. Torch is lazy-imported to preserve minimal install.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from torch import Tensor


PAPER_ID = "2610.30120v1"
UPSTREAM_REVISION = "30ab44b9fcdf3253fc67f5a53e31ea5141eb45c1"


def _finite(value: Tensor, name: str, *, ndim: int | None = None) -> None:
    import torch

    if (not isinstance(value, torch.Tensor) or not value.is_floating_point()
            or value.numel() == 0 or (ndim is not None and value.ndim != ndim)
            or not bool(torch.isfinite(value).all())):
        raise ValueError(f"{name} must be a nonempty finite floating tensor")


def crossview_geometry(box_a: Tensor, box_b: Tensor, grid: int = 14):
    """Paper S1: B-patch centers in A's frame, overlap mask and ln(side_B/side_A).

    Boxes are (batch, 3)=(top, left, side), normalized to the original image's
    central square. Returned positions are row-major (y, x), in A-patch units.
    The author's half-open overlap rule includes the lower but not upper edge.
    """
    import torch

    if isinstance(grid, bool) or not isinstance(grid, int) or grid < 1:
        raise ValueError("grid must be a positive integer")
    for name, box in (("box_a", box_a), ("box_b", box_b)):
        _finite(box, name, ndim=2)
        if box.shape[1] != 3 or bool((box[:, :2] < 0).any()) or bool((box[:, 2] <= 0).any()):
            raise ValueError("boxes must contain nonnegative top/left and positive side")
        if bool((box[:, :2] + box[:, 2:] > 1 + 1e-6).any()):
            raise ValueError("crop boxes must fit inside the normalized central square")
    if box_a.shape != box_b.shape or box_a.device != box_b.device:
        raise ValueError("crop boxes must have the same batch shape and device")
    # The fixed author implementation performs geometry in float32.
    a, b = box_a.float(), box_b.float()
    c = (torch.arange(grid, dtype=torch.float32, device=a.device) + 0.5) / grid
    y = (b[:, 0:1] + c[None] * b[:, 2:3] - a[:, 0:1]) / a[:, 2:3]
    x = (b[:, 1:2] + c[None] * b[:, 2:3] - a[:, 1:2]) / a[:, 2:3]
    yy = y[:, :, None].expand(-1, grid, grid)
    xx = x[:, None, :].expand(-1, grid, grid)
    positions = torch.stack((yy, xx), dim=-1).reshape(-1, grid * grid, 2) * grid
    valid = ((yy >= 0) & (yy < 1) & (xx >= 0) & (xx < 1)).reshape(-1, grid * grid)
    log_ratio = torch.log(b[:, 2] / a[:, 2])
    return positions, valid, log_ratio


def sincos_2d(positions_yx: Tensor, width: int = 512) -> Tensor:
    """Predictor PE=[sin y, cos y, sin x, cos x], omega=10000**(-k/(W/4)).

    This is NOT the image encoder's x-first position table with exponent k/(d-1).
    """
    import torch

    _finite(positions_yx, "positions_yx")
    if positions_yx.shape[-1] != 2:
        raise ValueError("position's last dimension must be (y, x)")
    if isinstance(width, bool) or not isinstance(width, int) or width < 4 or width % 4:
        raise ValueError("width must be a positive multiple of four")
    quarter = width // 4
    omega = 10000.0 ** (-torch.arange(quarter, dtype=torch.float32,
                                     device=positions_yx.device) / quarter)
    y, x = positions_yx[..., 0:1].float() * omega, positions_yx[..., 1:2].float() * omega
    return torch.cat((y.sin(), y.cos(), x.sin(), x.cos()), dim=-1)


def geometry_queries(positions_yx: Tensor, log_ratio: Tensor, mask_token: Tensor,
                     scale_weight: Tensor, scale_bias: Tensor) -> Tensor:
    """q_i=m+PE(p_i)+Linear([ln r,(ln r)^2]), including the author's affine bias.

    mask_token/scale_bias are (width,), scale_weight is (width,2). This only
    constructs the input queries; it does NOT replace the four-layer predictor.
    """
    import torch
    from torch.nn import functional as F

    for name, value, ndim in (("positions_yx", positions_yx, 3), ("log_ratio", log_ratio, 1),
                              ("mask_token", mask_token, 1), ("scale_weight", scale_weight, 2),
                              ("scale_bias", scale_bias, 1)):
        _finite(value, name, ndim=ndim)
    width = mask_token.numel()
    if (log_ratio.shape != (positions_yx.shape[0],) or scale_weight.shape != (width, 2)
            or scale_bias.shape != (width,)):
        raise ValueError("query batch or learned affine parameter shape mismatch")
    if any(x.device != positions_yx.device for x in (log_ratio, mask_token, scale_weight, scale_bias)):
        raise ValueError("query inputs must share one device")
    log_ratio = log_ratio.float()
    features = torch.stack((log_ratio, log_ratio.square()), dim=-1)
    scale = F.linear(features, scale_weight.float(), scale_bias.float())
    return mask_token.float()[None, None] + sincos_2d(positions_yx, width) + scale[:, None]


def teacher_targets(teacher_tokens: Tensor, mean: Tensor, std: Tensor) -> Tensor:
    """stop_grad((teacher_tokens-mu)/sigma), using fixed training-only statistics.

    The caller supplies immutable per-channel calibration statistics. This
    function never estimates them on an evaluated batch and never updates an EMA
    teacher. The paper's Stage-1 teacher is fixed, not a momentum teacher.
    """
    _finite(teacher_tokens, "teacher_tokens", ndim=3)
    _finite(mean, "mean", ndim=1)
    _finite(std, "std", ndim=1)
    if mean.shape != std.shape or mean.shape != (teacher_tokens.shape[-1],):
        raise ValueError("fixed statistics must match the teacher channel dimension")
    if mean.device != teacher_tokens.device or std.device != teacher_tokens.device:
        raise ValueError("teacher tokens and statistics must share one device")
    if bool((std <= 0).any()):
        raise ValueError("fixed teacher standard deviations must be strictly positive")
    return ((teacher_tokens.float() - mean.float()) / std.float()).detach()


def crossview_loss_from_pred(predictions: Tensor, targets: Tensor, valid: Tensor) -> Tensor:
    """Mean over images of per-image overlap-patch/channel MSE (Eq.2, S1).

    Zero-overlap images contribute zero with denominator max(n_valid,1), exactly
    as the release loss. It is not a single global average over all valid tokens.
    Supplied targets are detached as a safety boundary; gradients flow to pred.
    """
    import torch

    _finite(predictions, "predictions", ndim=3)
    _finite(targets, "targets", ndim=3)
    if (predictions.shape != targets.shape or predictions.device != targets.device
            or not isinstance(valid, torch.Tensor) or valid.dtype != torch.bool
            or valid.shape != predictions.shape[:2] or valid.device != predictions.device):
        raise ValueError("predictions, targets and boolean overlap mask must align")
    error = (predictions.float() - targets.detach().float()).square().mean(dim=-1)
    per_image = (error * valid.float()).sum(dim=1) / valid.sum(dim=1).clamp_min(1)
    return per_image.mean()


def stage2_objective(predictions: Tensor, teacher_tokens: Tensor, box_a: Tensor,
                     box_b: Tensor, mean: Tensor, std: Tensor, *, grid: int = 14) -> Tensor:
    """External-token interface: crop-aware fixed-teacher loss, no model loading."""
    _, valid, _ = crossview_geometry(box_a, box_b, grid)
    return crossview_loss_from_pred(predictions, teacher_targets(teacher_tokens, mean, std), valid)


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """Short checkpoint-free CPU/CUDA formula/gradient diagnostic, never accuracy."""
    import torch

    selected = torch.device(device)
    if selected.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable; no CPU fallback")
    generator = torch.Generator(device=selected).manual_seed(seed)
    a = torch.tensor([[.1, .1, .5], [.5, .5, .4]], device=selected)
    b = torch.tensor([[0., 0., .8], [0., 0., 1.]], device=selected)
    positions, valid, log_ratio = crossview_geometry(a, b, 4)
    m = torch.randn(8, generator=generator, device=selected, requires_grad=True)
    w = torch.randn(8, 2, generator=generator, device=selected, requires_grad=True)
    bias = torch.randn(8, generator=generator, device=selected, requires_grad=True)
    queries = geometry_queries(positions, log_ratio, m, w, bias)
    # A test-only linear readout exercises query gradients, NOT the ALPS predictor.
    readout = torch.randn(8, 6, generator=generator, device=selected)
    predictions = queries @ readout
    predictions.retain_grad()
    teacher = torch.randn(2, 16, 6, generator=generator, device=selected, requires_grad=True)
    mean = torch.linspace(-.5, .5, 6, device=selected)
    std = torch.linspace(.3, 1.2, 6, device=selected)
    targets = teacher_targets(teacher, mean, std)
    loss = crossview_loss_from_pred(predictions, targets, valid)
    independent_terms = []
    for batch in range(2):
        squares = [(predictions[batch, i, c] -
                    (teacher[batch, i, c].detach() - mean[c]) / std[c]).square()
                   for i in range(16) if bool(valid[batch, i]) for c in range(6)]
        independent_terms.append(torch.stack(squares).mean())
    reference = torch.stack(independent_terms).mean()
    no_mask = crossview_loss_from_pred(predictions, targets, torch.ones_like(valid))
    no_standardization = crossview_loss_from_pred(predictions, teacher.detach(), valid)
    no_geometry_queries = geometry_queries(torch.zeros_like(positions), torch.zeros_like(log_ratio), m, w, bias)
    query_delta = float((queries - no_geometry_queries).square().mean().detach())
    formula_error = float((loss - reference).abs().detach())
    mask_delta = float((loss - no_mask).abs().detach())
    stats_delta = float((loss - no_standardization).abs().detach())
    loss.backward()
    finite_gradients = all(x.grad is not None and bool(torch.isfinite(x.grad).all()) for x in (m, w, bias))
    masked_gradient_max = float(predictions.grad[~valid].abs().max())
    checks = {
        "independent_formula_match": bool(torch.allclose(loss, reference, rtol=1e-6, atol=1e-6)),
        "finite_student_query_gradients": finite_gradients,
        "frozen_teacher_has_no_gradient": teacher.grad is None,
        "masked_patch_gradient_is_zero": masked_gradient_max == 0,
        "remove_overlap_mask_changes_loss": mask_delta > 1e-6,
        "remove_fixed_statistics_changes_loss": stats_delta > 1e-6,
        "remove_geometry_changes_queries": query_delta > 1e-6,
    }
    if not all(checks.values()):
        raise RuntimeError(f"ALPS diagnostic failed: {checks}")
    return {
        "paper": PAPER_ID, "seed": seed, "device": selected.type,
        "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
        "promotion_eligible": False, "evolve_integrated": False,
        "full_experiment_status": "not_reproduced_high_cost",
        "pretrained_model_calls": 0, "dataset": "generated-crop-query-token-contract-suite",
        "upstream_revision": UPSTREAM_REVISION,
        "recipe": {"batch": 2, "grid": 4, "query_width": 8, "token_channels": 6,
                   "predictor": "test-only linear readout, not the ALPS transformer"},
        "checks": checks,
        "metrics": {"formula_absolute_error": formula_error, "overlap_patch_count": float(valid.sum()),
                    "removed_overlap_loss_delta": mask_delta,
                    "removed_standardization_loss_delta": stats_delta,
                    "removed_geometry_query_mse": query_delta,
                    "masked_patch_gradient_max": masked_gradient_max,
                    "query_parameter_gradient_norm": float(w.grad.norm()), "pretrained_model_calls": 0.0},
    }
