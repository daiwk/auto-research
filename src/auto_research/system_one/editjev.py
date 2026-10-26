"""EditJev v1 Eqs. 2--9, bounded numerical reference, not an image editor.

Only training consumes offline judge labels. Routing sees predicted utilities
and fixed model latencies; it cannot inspect candidate edits or quality labels.
"""
import math

import torch
from torch import Tensor, nn
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/editjev-a100-20261026.json"


def _finite(x: Tensor, ndim: int) -> None:
    if (x.ndim != ndim or min(x.shape) < 1 or x.numel() > 1_048_576
            or not x.is_floating_point() or not bool(torch.isfinite(x).all())):
        raise ValueError("bounded nonempty finite floating tensor required")


def offline_quality(ratings: Tensor) -> Tensor:
    """Eq.6: [request,editor,success/preservation/naturalness/artifact-free]."""
    _finite(ratings, 3)
    if ratings.shape[-1] != 4 or bool(((ratings < 0) | (ratings > 10)).any()):
        raise ValueError("four offline judge ratings in [0,10] required")
    scores = ratings.detach()
    return (scores[..., :2].amin(-1) * scores[..., 2:].amin(-1)).sqrt()


def pairwise_ranking_loss(utilities: Tensor, quality: Tensor, *, delta: float = 0.5) -> Tensor:
    """Eqs.7--9: normalize pairs per request, then average requests.

    An empty pair set contributes exactly zero, not an invented best-editor
    label. Quality is training supervision and detached from the objective.
    """
    _finite(utilities, 2)
    _finite(quality, 2)
    if (quality.shape != utilities.shape or quality.device != utilities.device
            or quality.dtype != utilities.dtype or isinstance(delta, bool)
            or not math.isfinite(delta) or delta < 0):
        raise ValueError("aligned utilities/quality and finite nonnegative delta required")
    if utilities.shape[1] > 128:
        raise ValueError("cost gate: at most 128 editors")
    q = quality.detach()
    gap = q[:, :, None] - q[:, None, :]
    pairs = (gap > 0) & (gap >= delta)
    difference = utilities[:, None, :] - utilities[:, :, None]
    # Avoid inactive huge differences affecting backward through softplus.
    terms = F.softplus(torch.where(pairs, difference, torch.zeros_like(difference)))
    loss = (torch.where(pairs, terms, 0).sum((1, 2)) / pairs.sum((1, 2)).clamp_min(1)).mean()
    if not bool(torch.isfinite(loss)):
        raise ValueError("nonfinite pairwise loss; no silent clipping")
    return loss


class PreferenceHead(nn.Module):
    """Eq.2 last non-padding token -> Eq.3 linear head (Section4.1).

    External hidden states must come from the declared multimodal router.
    The tiny diagnostic encoder is not Qwen3-VL or an image understanding model.
    """

    def __init__(self, hidden_dim: int, editors: int):
        super().__init__()
        if not 1 <= hidden_dim <= 4096 or not 2 <= editors <= 128:
            raise ValueError("bounded hidden dimension/editor count required")
        self.projection = nn.Linear(hidden_dim, editors)

    def forward(self, hidden: Tensor, attention_mask: Tensor) -> Tensor:
        _finite(hidden, 3)
        if (attention_mask.shape != hidden.shape[:2] or attention_mask.dtype != torch.bool
                or attention_mask.device != hidden.device or not bool(attention_mask.any(-1).all())):
            raise ValueError("aligned bool nonempty token mask required")
        positions = torch.arange(hidden.shape[1], device=hidden.device).expand(hidden.shape[:2])
        last = positions.masked_fill(~attention_mask, -1).amax(-1)
        return self.projection(hidden[torch.arange(hidden.shape[0], device=hidden.device), last])


def route(utilities: Tensor, mean_latencies: Tensor, *, beta: float) -> dict:
    """Eqs.4--5, no offline scores/output images accepted by this API.

    Equal latencies make Eq.4 undefined and are rejected explicitly. Exact ties
    use torch.argmax's first candidate (local deterministic convention).
    """
    _finite(utilities, 2)
    _finite(mean_latencies, 1)
    if (mean_latencies.shape[0] != utilities.shape[1] or mean_latencies.device != utilities.device
            or mean_latencies.dtype != utilities.dtype or bool((mean_latencies <= 0).any())
            or isinstance(beta, bool) or not math.isfinite(beta) or beta < 0):
        raise ValueError("aligned positive model latencies and finite beta>=0 required")
    spread = mean_latencies.max() - mean_latencies.min()
    if not bool(spread > 0):
        raise ValueError("Eq.4 undefined for identical latencies; caller must declare policy")
    speed = (mean_latencies.max() - mean_latencies) / spread
    scores = utilities + beta * speed
    if not bool(torch.isfinite(scores).all()):
        raise ValueError("nonfinite routing scores")
    return {"editor_indices": scores.argmax(-1), "speed_scores": speed, "scores": scores}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device not in ("cpu", "cuda") or device == "cuda" and not torch.cuda.is_available():
        raise ValueError("cpu or actual available cuda required; no fallback")
    gen = torch.Generator(device=device).manual_seed(seed)
    utilities = torch.randn(3, 4, generator=gen, dtype=torch.float64, device=device, requires_grad=True)
    quality = torch.tensor([[9., 7., 4., 2.], [5., 5., 5., 5.], [8., 7.8, 7.7, 1.]], device=device, dtype=torch.float64)
    loss = pairwise_ranking_loss(utilities, quality)
    manual = []
    for b in range(3):
        pairs = [(a, c) for a in range(4) for c in range(4)
                 if quality[b, a] > quality[b, c] and quality[b, a] - quality[b, c] >= .5]
        manual.append(sum((F.softplus(utilities[b, c] - utilities[b, a]) for a, c in pairs),
                          utilities[b].sum() * 0) / max(1, len(pairs)))
    error = (loss - torch.stack(manual).mean()).abs().item()
    loss.backward()
    gradient = utilities.grad.detach().clone()
    before = loss.item()
    after = pairwise_ranking_loss((utilities - .1 * gradient).detach(), quality).item()
    rates = torch.tensor([10., 20., 40., 80.], device=device, dtype=torch.float64)
    neutral = torch.zeros(1, 4, device=device, dtype=torch.float64)
    fast = route(neutral, rates, beta=1.)
    zero = route(utilities.detach(), rates, beta=0.)
    ratings = torch.tensor([[[9., 4., 8., 1.]]], device=device, dtype=torch.float64)
    with torch.random.fork_rng(devices=[torch.cuda.current_device()] if device == "cuda" else []):
        torch.manual_seed(seed)
        head = PreferenceHead(4, 4).to(device=device, dtype=torch.float64)
    hidden = torch.randn(2, 5, 4, generator=gen, device=device, dtype=torch.float64)
    token_mask = torch.tensor([[False, True, False, True, False], [True, True, False, False, False]], device=device)
    predicted = head(hidden, token_mask)
    pooling_error = (predicted - head.projection(torch.stack((hidden[0, 3], hidden[1, 1])))).abs().max().item()
    predicted.sum().backward()
    checks = {
        "per_request_pair_mean_reference": error < 1e-12,
        "empty_pair_request_zero_gradient": bool((gradient[1] == 0).all()),
        "ranking_step_reduces_loss": after < before,
        "four_rating_min_geometric_mean": offline_quality(ratings).item() == 2.,
        "beta_zero_uses_only_predicted_utility": torch.equal(zero["editor_indices"], utilities.detach().argmax(-1)),
        "positive_beta_prefers_faster_tied_utility": fast["editor_indices"].item() == 0,
        "routing_does_not_accept_quality_labels": "quality" not in route.__annotations__,
        "last_nonpadding_hidden_linear_head": pooling_error < 1e-12,
        "preference_head_has_actual_gradient": head.projection.weight.grad.norm().item() > 0,
    }
    if not all(checks.values()):
        raise RuntimeError(f"EditJev mechanism check failed: {checks}")
    return {"seed": seed, "metrics": {"loss": before, "loss_after_step": after,
            "ranking_reference_error": error, "gradient_norm": gradient.norm().item(),
            "head_pooling_reference_error": pooling_error,
            "head_gradient_norm": head.projection.weight.grad.norm().item(),
            "requests": 3, "candidate_editors": 4, "editor_model_calls": 0}, "checks": checks}
