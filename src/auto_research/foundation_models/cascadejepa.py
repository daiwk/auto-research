"""CascadeJEPA v1 Eq3–5: two-crop spatial coupling with shared EMA targets."""

from __future__ import annotations

from copy import deepcopy
import torch
from torch import Tensor, nn

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/cascadejepa-a100-20261118-latest.json"


def zero_mask_before_position(patches: Tensor, position: Tensor, targets: Tensor) -> Tensor:
    if targets.dtype != torch.bool or targets.shape != patches.shape[1:2]:
        raise ValueError("one common boolean target mask across the batch required")
    return patches.masked_fill(targets[None, :, None], 0) + position


class CascadeJEPA(nn.Module):
    """Tiny executable token architecture; not a trained ViT or image pipeline."""

    def __init__(self, width: int = 8, heads: int = 2):
        super().__init__()
        encoder = nn.TransformerEncoderLayer(width, heads, 2 * width, dropout=0, batch_first=True)
        self.context = nn.TransformerEncoder(encoder, 1, enable_nested_tensor=False)
        self.target = deepcopy(self.context).requires_grad_(False)
        self.predictor1 = nn.TransformerEncoder(deepcopy(encoder), 1, enable_nested_tensor=False)
        self.predictor2 = nn.TransformerEncoder(deepcopy(encoder), 1, enable_nested_tensor=False)
        self.cross = nn.MultiheadAttention(width, heads, dropout=0, batch_first=True)
        self.mask = nn.Parameter(torch.zeros(1, 1, width))

    @torch.no_grad()
    def update_target(self, momentum: float = 0.99) -> None:
        if not 0 <= momentum <= 1:
            raise ValueError("EMA coefficient must be in [0,1]")
        for target, context in zip(self.target.parameters(), self.context.parameters()):
            target.mul_(momentum).add_(context, alpha=1 - momentum)

    def forward(
        self,
        crop1: Tensor,
        crop2: Tensor,
        pos1: Tensor,
        pos2: Tensor,
        target1: Tensor,
        target2: Tensor,
    ) -> tuple[Tensor, Tensor, Tensor]:
        if (
            crop1.ndim != 3
            or crop2.shape != crop1.shape
            or pos1.shape != crop1.shape[1:]
            or pos2.shape != pos1.shape
            or target1.shape != crop1.shape[1:2]
            or target2.shape != target1.shape
            or target1.dtype != torch.bool
            or target2.dtype != torch.bool
            or not bool(target1.any() and target2.any() and (~target2).any())
        ):
            raise ValueError(
                "two [B,N,D] crops, independent [N,D] positions and nonempty boolean targets required"
            )
        full1 = self.context(zero_mask_before_position(crop1, pos1, target1))
        visible2 = self.context((crop2 + pos2)[:, ~target2])
        mask2 = self.mask.expand(crop2.shape[0], int(target2.sum()), -1) + pos2[target2]
        queries2 = torch.cat([visible2, mask2], 1)
        conditioned2 = queries2 + self.cross(queries2, full1, full1, need_weights=False)[0]
        pred1 = self.predictor1(full1)[:, target1]
        pred2 = self.predictor2(conditioned2)[:, -int(target2.sum()) :]
        with torch.no_grad():
            expected1 = self.target(crop1 + pos1)[:, target1]
            expected2 = self.target(crop2 + pos2)[:, target2]
        # Sum feature coordinates, mean target tokens and batch: paper Eq5, not elementwise mean.
        loss1 = (pred1 - expected1).square().sum(-1).mean()
        loss2 = (pred2 - expected2).square().sum(-1).mean()
        return 0.5 * (loss1 + loss2), pred1, pred2


def diagnostic(seed: int, device: str = "cpu") -> dict:
    torch.manual_seed(seed)
    model = CascadeJEPA().to(device)
    crop1, crop2 = (torch.randn(2, 6, 8, device=device) for _ in range(2))
    pos1, pos2 = (torch.randn(6, 8, device=device) for _ in range(2))
    target1 = torch.tensor([False, True, False, False, True, False], device=device)
    target2 = torch.tensor([False, False, True, True, False, True], device=device)
    loss, first, _ = model(crop1, crop2, pos1, pos2, target1, target2)
    _, altered_first, _ = model(crop1, crop2 * 4, pos1, pos2, target1, target2)
    loss.backward()
    zeroed = zero_mask_before_position(crop1, pos1, target1)
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "metrics": {"two_stage_objective": float(loss.detach())},
        "checks": {
            "masked_grid_keeps_positions": bool(
                torch.equal(zeroed[:, target1], pos1[target1].expand(2, -1, -1))
            ),
            "stage2_cannot_change_stage1": bool(torch.equal(first, altered_first)),
            "ema_target_has_no_gradients": all(p.grad is None for p in model.target.parameters()),
            "spatial_cross_attention_trained": bool(
                model.cross.in_proj_weight.grad is not None
                and model.cross.in_proj_weight.grad.abs().sum() > 0
            ),
        },
    }
