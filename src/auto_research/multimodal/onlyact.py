"""OnlyAct's exact contrastive bank/loss and fixed projection, without video models."""
from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import Tensor
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/onlyact-a100-20261112.json"


@dataclass(frozen=True)
class PairWindow:
    """Frame support [start, stop), including both sampled frames inside it."""
    video_id: str
    start: int
    stop: int

    def __post_init__(self):
        if (not isinstance(self.video_id, str) or not self.video_id
                or type(self.start) is not int or type(self.stop) is not int
                or not 0 <= self.start < self.stop):
            raise ValueError("identified video and nonempty integer frame window required")


def validate_hard_negative(anchor: PairWindow, negative: PairWindow) -> None:
    """Same video and non-overlap are required, not a claim of different action."""
    if anchor.video_id != negative.video_id or not (
            anchor.stop <= negative.start or negative.stop <= anchor.start):
        raise ValueError("hard negative must use a disjoint window of the SAME video")


def pooled_action(tokens: Tensor, fixed_projection: Tensor) -> Tensor:
    """Tokens must come from a JOINT two-frame encoder, never frame differencing.

    The external projection is frozen. This function does not supply V-JEPA 2.
    """
    if (tokens.ndim != 3 or fixed_projection.ndim != 2 or min(tokens.shape) < 1
            or fixed_projection.shape[1] != tokens.shape[-1]
            or fixed_projection.shape[0] < 1 or tokens.device != fixed_projection.device
            or tokens.dtype != fixed_projection.dtype or not tokens.is_floating_point()
            or not torch.isfinite(tokens).all() or not torch.isfinite(fixed_projection).all()):
        raise ValueError("aligned finite joint-clip tokens and fixed projection required")
    projected = tokens.mean(1) @ fixed_projection.detach().T
    if torch.any(projected.norm(dim=-1) <= 1e-12):
        raise ValueError("zero action embedding cannot be normalized")
    return F.normalize(projected, dim=-1)


def bank_contract(size: int, device: torch.device | str = "cpu") -> tuple[Tensor, Tensor]:
    """2N queries against [anchor|positive|hard negative]; exclude only self."""
    if type(size) is not int or size < 1:
        raise ValueError("positive batch size required")
    rows = torch.arange(2 * size, device=device)
    allowed = torch.ones((2 * size, 3 * size), device=device, dtype=torch.bool)
    allowed[rows, rows] = False
    targets = (rows + size) % (2 * size)
    return allowed, targets


def contrastive_loss(anchor: Tensor, positive: Tensor, hard_negative: Tensor,
                     temperature: float = .07) -> Tensor:
    """Symmetric InfoNCE: 2N query rows, 3N candidates, matched positive included."""
    if (anchor.ndim != 2 or min(anchor.shape) < 1 or positive.shape != anchor.shape
            or hard_negative.shape != anchor.shape
            or type(temperature) not in (int, float) or not 0 < temperature < float("inf")):
        raise ValueError("aligned normalized embeddings and finite positive temperature required")
    for value in (anchor, positive, hard_negative):
        if (value.device != anchor.device or value.dtype != anchor.dtype
                or not value.is_floating_point() or not torch.isfinite(value).all()
                or not torch.allclose(value.norm(dim=-1), torch.ones_like(value[:, 0]), atol=1e-5)):
            raise ValueError("finite same-device unit embeddings required")
    bank = torch.cat((anchor, positive, hard_negative))
    allowed, targets = bank_contract(len(anchor), anchor.device)
    logits = (bank[:2 * len(anchor)] @ bank.T / temperature).masked_fill(~allowed, -torch.inf)
    return F.cross_entropy(logits, targets)


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device not in {"cpu", "cuda"} or (device == "cuda" and not torch.cuda.is_available()):
        raise ValueError("available CPU or real CUDA required")
    torch.manual_seed(seed)
    tokens = torch.randn(2, 4, 8, device=device, dtype=torch.float64, requires_grad=True)
    projection = torch.randn(6, 8, device=device, dtype=torch.float64, requires_grad=True)
    anchor = pooled_action(tokens, projection)
    positive = F.normalize(anchor.detach() + .1 * torch.randn_like(anchor), dim=-1).requires_grad_()
    negative = F.normalize(torch.randn_like(anchor), dim=-1).requires_grad_()
    loss = contrastive_loss(anchor, positive, negative)
    bank = torch.cat((anchor, positive, negative))
    loop = []
    for i in range(4):
        candidates = torch.stack([bank[i] @ bank[j] / .07 for j in range(6) if j != i])
        loop.append(torch.logsumexp(candidates, 0) - bank[i] @ bank[(i + 2) % 4] / .07)
    reference = torch.stack(loop).mean()
    loss.backward()
    validate_hard_negative(PairWindow("training-clip", 0, 3), PairWindow("training-clip", 3, 6))
    allowed, targets = bank_contract(2, tokens.device)
    return {
        "seed": seed, "device": str(tokens.device), "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "metrics": {"synthetic_contrastive_loss": float(loss.detach()),
                    "loop_reference_error": float((loss - reference).abs().detach()),
                    "candidates_per_query": int(allowed[0].sum()),
                    "hard_negative_gradient_norm": float(negative.grad.norm())},
        "checks": {"independent_full_bank_reference": bool(torch.allclose(loss, reference)),
                   "exclude_self_only": bool((allowed.sum(-1) == 5).all())
                   and not bool(allowed[torch.arange(4, device=device), torch.arange(4, device=device)].any()),
                   "matched_positive_in_denominator": bool(allowed[torch.arange(4, device=device), targets].all()),
                   "all_hard_negatives_included": bool(allowed[:, 4:].all()),
                   "fixed_projection_frozen": projection.grad is None,
                   "joint_token_gradient_finite": tokens.grad is not None and bool(torch.isfinite(tokens.grad).all()),
                   "hard_negative_gradient_present": negative.grad is not None and float(negative.grad.norm()) > 0,
                   "actual_tensor_device": tokens.device.type == device},
    }
