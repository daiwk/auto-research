"""Exact static block-mass calibration and Sink-Sparse hybrid attention.

arXiv:2610.22975, Algorithms 1/2. The sparse branch actually gathers retained
blocks; Python loops are correctness-oriented, not a fast DiT inference kernel.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import torch


@dataclass(frozen=True)
class SinkMask:
    blocks: torch.Tensor
    mean_block_mass: torch.Tensor
    block_size: int


def _qk(q: torch.Tensor, k: torch.Tensor) -> None:
    if q.ndim != 4 or q.shape != k.shape or min(q.shape) < 1:
        raise ValueError("matching nonempty [batch,head,token,dim] Q/K required")
    if q.dtype not in (torch.float32, torch.float64) or k.dtype != q.dtype or k.device != q.device:
        raise ValueError("matching-device FP32/FP64 Q/K required")
    if not bool(torch.isfinite(q).all()) or not bool(torch.isfinite(k).all()):
        raise ValueError("finite Q/K required")


def calibrate_sink_mask(q: torch.Tensor, k: torch.Tensor, *, block_size: int,
                        coverage: float = .85) -> SinkMask:
    """Calibrate on dedicated observations, never on downstream/test queries."""
    _qk(q, k)
    if isinstance(block_size, bool) or not isinstance(block_size, int) or block_size < 1 or q.shape[2] % block_size:
        raise ValueError("positive block size dividing sequence length required")
    if not math.isfinite(coverage) or not 0 < coverage <= 1:
        raise ValueError("coverage must be in (0,1]")
    with torch.no_grad():
        count, heads, tokens, dim = q.shape
        blocks = tokens // block_size
        attention = ((q.detach() @ k.detach().transpose(-1, -2)) / math.sqrt(dim)).softmax(-1)
        # Exact probability mass: mean over query tokens, SUM over key tokens.
        mass = attention.reshape(count, heads, blocks, block_size, blocks, block_size).sum(-1).mean(3).mean(0)
        order = mass.argsort(dim=-1, descending=True, stable=True)
        ranked = mass.gather(-1, order)
        number = (ranked.cumsum(-1) < coverage * mass.sum(-1, keepdim=True)).sum(-1).add(1).clamp_max(blocks)
        selected = torch.arange(blocks, device=q.device) < number[..., None]
        mask = torch.zeros_like(mass, dtype=torch.bool).scatter(-1, order, selected)
        return SinkMask(mask.detach().clone(), mass.detach().clone(), block_size)


def _mask_check(mask: SinkMask, q: torch.Tensor) -> None:
    if isinstance(mask.block_size, bool) or not isinstance(mask.block_size, int) or mask.block_size < 1 or q.shape[2] % mask.block_size:
        raise ValueError("mask block size must divide sequence length")
    blocks = q.shape[2] // mask.block_size
    if mask.blocks.dtype != torch.bool or mask.blocks.shape != (q.shape[1], blocks, blocks) or mask.blocks.device != q.device:
        raise ValueError("same-device [head,queryblock,keyblock] boolean mask required")
    if not bool(mask.blocks.any(-1).all()):
        raise ValueError("every query block must retain at least one key block")


def sparse_sink_attention(q: torch.Tensor, k: torch.Tensor, v: torch.Tensor,
                          mask: SinkMask) -> tuple[torch.Tensor, torch.Tensor]:
    """Execute retained blocks only; return normalized outputs and row log-Z."""
    _qk(q, k)
    if v.ndim != 4 or v.shape[:3] != k.shape[:3] or v.shape[3] < 1 or v.device != q.device or v.dtype != q.dtype:
        raise ValueError("matching value batch/head/token, dtype and device required")
    if not bool(torch.isfinite(v).all()):
        raise ValueError("finite values required")
    _mask_check(mask, q)
    heads_out, heads_lse = [], []
    b = mask.block_size
    offsets = torch.arange(b, device=q.device)
    for head in range(q.shape[1]):
        outputs, normalizers = [], []
        for query_block in range(mask.blocks.shape[1]):
            selected_blocks = mask.blocks[head, query_block].nonzero().flatten()
            selected_tokens = (selected_blocks[:, None] * b + offsets[None]).flatten()
            scores = q[:, head, query_block * b:(query_block + 1) * b] @ k[:, head, selected_tokens].transpose(-1, -2) / math.sqrt(q.shape[-1])
            outputs.append(scores.softmax(-1) @ v[:, head, selected_tokens])
            normalizers.append(scores.logsumexp(-1))
        heads_out.append(torch.cat(outputs, 1))
        heads_lse.append(torch.cat(normalizers, 1))
    return torch.stack(heads_out, 1), torch.stack(heads_lse, 1)


def hybrid_attention(q: torch.Tensor, k: torch.Tensor, v: torch.Tensor, mask: SinkMask,
                     *, pool_gap: int = 4) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
    """Eqs.5/6, including log(pool_gap) correction and overlapping support.

    The pooled branch summarizes *all* K/V, including retained blocks, as in
    the paper. It must not silently remove sink blocks from this branch.
    """
    sink, sink_lse = sparse_sink_attention(q, k, v, mask)
    if isinstance(pool_gap, bool) or not isinstance(pool_gap, int) or pool_gap < 1 or q.shape[2] % pool_gap:
        raise ValueError("positive pooling gap dividing sequence length required")
    batch, heads, tokens, dim = k.shape
    pooled_k = k.reshape(batch, heads, tokens // pool_gap, pool_gap, dim).mean(3)
    pooled_v = v.reshape(batch, heads, tokens // pool_gap, pool_gap, v.shape[-1]).mean(3)
    logits = (q @ pooled_k.transpose(-1, -2)) / math.sqrt(dim)
    comp_lse = logits.logsumexp(-1)
    compensation = logits.softmax(-1) @ pooled_v
    alpha = torch.sigmoid(sink_lse - comp_lse - math.log(pool_gap))
    output = alpha[..., None] * sink + (1 - alpha[..., None]) * compensation
    return output, {"sink": sink, "compensation": compensation, "sink_lse": sink_lse,
                    "compensation_lse": comp_lse, "alpha": alpha}
