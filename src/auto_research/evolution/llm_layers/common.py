from __future__ import annotations

import math


def _rotary(q, k, torch, *, mode: str = "standard", context_length: int | None = None):
    length, width = q.shape[-2], q.shape[-1]
    half = width // 2
    standard = 1.0 / (
        10000 ** (torch.arange(half, device=q.device, dtype=q.dtype) / half)
    )
    def rotate(values):
        frequencies = standard[None].expand(values.shape[1], -1).clone()
        if mode == "mobius":
            if not context_length:
                raise ValueError("Möbius RoPE requires a fixed training context length")
            special_heads = max(1, values.shape[1] // 4)
            anti_periodic = (
                math.pi
                * (2 * torch.arange(half, device=q.device, dtype=q.dtype) + 1)
                / context_length
            )
            frequencies[:special_heads] = anti_periodic
        angles = (
            torch.arange(length, device=q.device, dtype=q.dtype)[:, None, None]
            * frequencies[None]
        )
        cos = angles.cos().permute(1, 0, 2)[None]
        sin = angles.sin().permute(1, 0, 2)[None]
        left, right = values[..., :half], values[..., half:half * 2]
        return torch.cat((left * cos - right * sin, left * sin + right * cos, values[..., half * 2:]), dim=-1)

    return rotate(q), rotate(k)

def _correlation(left, right, torch):
    left = left.detach().float().flatten()
    right = right.detach().float().flatten()
    left = left - left.mean()
    right = right - right.mean()
    denominator = left.square().sum().sqrt() * right.square().sum().sqrt()
    if float(denominator) == 0.0:
        return torch.tensor(0.0)
    return (left * right).sum() / denominator

def _sinkhorn(logits, iterations, torch):
    values = torch.exp(logits - logits.amax(dim=(-2, -1), keepdim=True))
    for _ in range(iterations):
        values = values / values.sum(dim=-1, keepdim=True).clamp_min(1e-8)
        values = values / values.sum(dim=-2, keepdim=True).clamp_min(1e-8)
    return values
