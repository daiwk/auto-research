"""Extracted unchanged from auto_research.foundation_latest_20260930; stable mechanism boundary."""
from __future__ import annotations

import math

def masked_block_average(hidden, scale: int, attention_mask=None):
    """Equation (8): right-padded, non-overlapping masked average pooling."""
    import torch
    import torch.nn.functional as F

    if hidden.ndim != 3 or scale < 1:
        raise ValueError("hidden must be [batch, time, dim] and scale positive")
    batch, length, dim = hidden.shape
    if attention_mask is None:
        attention_mask = torch.ones(batch, length, device=hidden.device, dtype=hidden.dtype)
    if attention_mask.shape != (batch, length):
        raise ValueError("attention_mask must be [batch, time]")
    padded_length = math.ceil(length / scale) * scale
    pad = padded_length - length
    padded_hidden = F.pad(hidden, (0, 0, 0, pad))
    padded_mask = F.pad(attention_mask.to(hidden.dtype), (0, pad))
    blocks = padded_hidden.reshape(batch, -1, scale, dim)
    mask_blocks = padded_mask.reshape(batch, -1, scale, 1)
    pooled = (blocks * mask_blocks).sum(dim=2) / mask_blocks.sum(dim=2).clamp_min(1)
    pooled_mask = (mask_blocks.sum(dim=2).squeeze(-1) > 0).to(attention_mask.dtype)
    return pooled, pooled_mask

def causal_hold_upsample(branch_output, scale: int, target_length: int):
    """Equation (10) alignment: reveal a block only after its last token."""
    import torch.nn.functional as F

    if scale < 1:
        raise ValueError("scale must be positive")
    repeated = branch_output.repeat_interleave(scale, dim=1)
    if scale > 1:
        repeated = F.pad(repeated, (0, 0, scale - 1, 0))
    return repeated[:, :target_length]

def fuse_scales(hidden, aligned_outputs, fusion_projection):
    """Equations (10)-(11): input-dependent softmax routing across scales."""
    import torch

    if not aligned_outputs:
        raise ValueError("at least one scale output is required")
    stacked = torch.stack(aligned_outputs, dim=2)
    weights = torch.softmax(fusion_projection(hidden), dim=-1)
    if weights.shape != stacked.shape[:3]:
        raise ValueError("fusion projection scale count differs from outputs")
    return (stacked * weights.unsqueeze(-1)).sum(dim=2), weights

def gated_linear_recurrence(hidden, in_projection, out_projection):
    """Small recurrent GLA branch used for executable mechanism validation."""
    import torch

    q, k, value, gate = in_projection(hidden).chunk(4, dim=-1)
    gate = torch.sigmoid(gate)
    state = torch.zeros(
        hidden.shape[0], hidden.shape[-1], hidden.shape[-1],
        device=hidden.device, dtype=hidden.dtype,
    )
    outputs = []
    for index in range(hidden.shape[1]):
        decay = gate[:, index].unsqueeze(-1)
        state = decay * state + torch.einsum("bi,bj->bij", k[:, index], value[:, index])
        outputs.append(torch.einsum("bi,bij->bj", q[:, index], state))
    return out_projection(torch.stack(outputs, dim=1))

class MultiScaleGLA:
    """A compact executable MS-GLA layer preserving the paper's three stages.

    This implementation validates the architecture rather than the paper's
    flash-linear-attention kernel or matched 340M parameter training recipe.
    """

    def __new__(cls, hidden_size: int, scales=(1, 2, 4)):
        import torch.nn as nn

        if not scales or any(scale < 1 for scale in scales) or len(set(scales)) != len(scales):
            raise ValueError("scales must be unique positive integers")

        class _Layer(nn.Module):
            def __init__(self):
                super().__init__()
                self.scales = tuple(scales)
                self.in_projections = nn.ModuleList(
                    nn.Linear(hidden_size, 4 * hidden_size) for _ in self.scales
                )
                self.out_projections = nn.ModuleList(
                    nn.Linear(hidden_size, hidden_size) for _ in self.scales
                )
                self.fusion = nn.Linear(hidden_size, len(self.scales))

            def forward(self, hidden, attention_mask=None):
                aligned = []
                for scale, in_projection, out_projection in zip(
                    self.scales, self.in_projections, self.out_projections
                ):
                    pooled, _ = masked_block_average(hidden, scale, attention_mask)
                    branch = gated_linear_recurrence(pooled, in_projection, out_projection)
                    aligned.append(causal_hold_upsample(branch, scale, hidden.shape[1]))
                output, weights = fuse_scales(hidden, aligned, self.fusion)
                return output, {"routing_weights": weights, "scales": self.scales}

        return _Layer()
