"""Differentiable fixed-cache RoPERelay, arXiv:2610.21126 Eqs. 3-4 / App. A.

No selector, historical re-prefill, language model or capability evaluator is
supplied. Model-provided rotary factors support scaled/partial RoPE.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import torch
from torch import Tensor

FactorProvider = Callable[[Tensor], tuple[Tensor, Tensor]]


def rotary_factors(positions: Tensor, inverse_frequency: Tensor,
                   amplitude: float | Tensor = 1.) -> tuple[Tensor, Tensor]:
    """Convenience for static RoPE; production callers may supply model factors."""
    if inverse_frequency.ndim != 1 or inverse_frequency.numel() < 1:
        raise ValueError("inverse_frequency must be a nonempty vector")
    dtype = torch.float64 if inverse_frequency.dtype == torch.float64 else torch.float32
    phase = positions.to(dtype).unsqueeze(-1) * inverse_frequency.to(dtype)
    return amplitude * phase.cos(), amplitude * phase.sin()


def apply_rotary(value: Tensor, cosine: Tensor, sine: Tensor, *, inverse: bool = False,
                 layout: str = "split_half") -> Tensor:
    """Apply factors to rotary dimensions only, retaining real autograd paths.

    With c=a*cos(phi), s=a*sin(phi), the inverse divides by c²+s².
    FP16/BF16/FP32 caches use FP32 intermediates; double stays double for
    independent high-precision verification and gradcheck.
    """
    if not value.is_floating_point() or cosine.shape != sine.shape:
        raise ValueError("floating value and identically shaped factors required")
    if layout not in {"split_half", "interleaved"}:
        raise ValueError("unsupported rotary layout")
    rotary_dim = 2 * cosine.shape[-1]
    if not 0 < rotary_dim <= value.shape[-1]:
        raise ValueError("factors must describe an even nonempty rotary prefix")
    try:
        shape = torch.broadcast_shapes(value.shape[:-1], cosine.shape[:-1])
    except RuntimeError as error:
        raise ValueError("rotary factor prefix is not broadcastable") from error
    if shape != value.shape[:-1] or value.device != cosine.device or value.device != sine.device:
        raise ValueError("factors must broadcast within the value shape on the same device")
    dtype = torch.float64 if value.dtype == torch.float64 else torch.float32
    c, s = cosine.to(dtype), sine.to(dtype)
    if not bool(torch.isfinite(c).all() & torch.isfinite(s).all()):
        raise ValueError("rotary factors must be finite")
    rotated = value[..., :rotary_dim].to(dtype)
    if layout == "split_half":
        left, right = rotated.chunk(2, dim=-1)
    else:
        left, right = rotated[..., 0::2], rotated[..., 1::2]
    if inverse:
        denominator = c.square() + s.square()
        if bool((denominator <= 0).any()):
            raise ValueError("source rotation is not invertible")
        first, second = (left * c + right * s) / denominator, (right * c - left * s) / denominator
    else:
        first, second = left * c - right * s, left * s + right * c
    transformed = (torch.cat((first, second), -1) if layout == "split_half" else
                   torch.stack((first, second), -1).flatten(-2))
    return torch.cat((transformed.to(value.dtype), value[..., rotary_dim:]), -1)


def relocate_keys(keys: Tensor, source_factors: tuple[Tensor, Tensor],
                  target_factors: tuple[Tensor, Tensor], *, layout: str = "split_half") -> Tensor:
    """R(target) R(source)^-1 K, including scaled source factors."""
    # Keep both rotations in working precision; cast only once at cache output.
    dtype = torch.float64 if keys.dtype == torch.float64 else torch.float32
    work = apply_rotary(keys.to(dtype), *source_factors, inverse=True, layout=layout)
    return apply_rotary(work, *target_factors, layout=layout).to(keys.dtype)


@dataclass(frozen=True)
class RelayedCache:
    keys: Tensor
    values: Tensor
    source_positions: Tensor
    compact_positions: Tensor
    valid_mask: Tensor
    permutation: Tensor
    anchor: int

    def question_positions(self, length: int) -> Tensor:
        if length < 1:
            raise ValueError("a question must have at least one token")
        return torch.arange(self.anchor, self.anchor + length, device=self.keys.device)

    def answer_input_positions(self, question_length: int, length: int) -> Tensor:
        """First sampled answer is fed back at M+Q, not at M+Q-1."""
        if question_length < 1 or length < 0:
            raise ValueError("invalid continuation length")
        return torch.arange(self.anchor + question_length,
                            self.anchor + question_length + length, device=self.keys.device)

    def causal_mask(self, continuation_length: int) -> Tensor:
        """True=attend; padded history is hidden, current continuation causal."""
        if continuation_length < 1:
            raise ValueError("continuation_length must be positive")
        history = self.valid_mask.unsqueeze(-2).expand(*self.valid_mask.shape[:-1],
                                                     continuation_length, -1)
        current = torch.ones((continuation_length, continuation_length), dtype=torch.bool,
                             device=self.keys.device).tril()
        current = current.expand(*self.valid_mask.shape[:-1], -1, -1)
        return torch.cat((history, current), -1)


def relay_cache(keys: Tensor, values: Tensor, source_positions: Tensor,
                 factors: FactorProvider, valid_mask: Tensor | None = None, *,
                 layout: str = "split_half") -> RelayedCache:
    """Stable time-sort, right-align heterogeneous heads, and relocate K only.

    Prefix dimensions enumerate physical KV heads/layers (and optionally
    batches). Their maximum retained count defines the one shared anchor M.
    Masked slots sort after valid states and never acquire a new RoPE phase.
    """
    if (keys.ndim < 2 or values.shape[:-1] != keys.shape[:-1] or
            source_positions.shape != keys.shape[:-1] or not keys.is_floating_point() or
            not values.is_floating_point() or source_positions.dtype != torch.int64):
        raise ValueError("expected K/V [...,slots,dim] and int64 source positions [...,slots]")
    if keys.device != values.device or keys.device != source_positions.device:
        raise ValueError("all cache inputs must share a device")
    mask = torch.ones_like(source_positions, dtype=torch.bool) if valid_mask is None else valid_mask
    if mask.shape != source_positions.shape or mask.dtype != torch.bool or mask.device != keys.device:
        raise ValueError("valid_mask must be a same-device boolean position mask")
    if bool((source_positions[mask] < 0).any()) or source_positions.shape[-1] < 1:
        raise ValueError("valid source positions must be nonnegative; storage must have slots")
    sentinel = torch.iinfo(torch.int64).max
    permutation = torch.argsort(torch.where(mask, source_positions, sentinel), dim=-1, stable=True)
    source = source_positions.gather(-1, permutation)
    valid = mask.gather(-1, permutation)
    if bool(((source[..., 1:] == source[..., :-1]) & valid[..., 1:] & valid[..., :-1]).any()):
        raise ValueError("duplicate valid source positions within a physical head")
    def ordered(tensor: Tensor) -> Tensor:
        return tensor.gather(-2, permutation.unsqueeze(-1).expand(*permutation.shape, tensor.shape[-1]))
    sorted_keys, sorted_values = ordered(keys), ordered(values)
    counts = valid.sum(-1)
    anchor = int(counts.max().item())
    rank = torch.arange(source.shape[-1], device=keys.device)
    compact = anchor - counts.unsqueeze(-1) + rank
    compact = torch.where(valid, compact, -1)
    safe_source = torch.where(valid, source, 0)
    safe_target = compact.clamp_min(0)
    transformed = relocate_keys(sorted_keys, factors(safe_source), factors(safe_target), layout=layout)
    new_keys = torch.where(valid.unsqueeze(-1), transformed, sorted_keys)
    return RelayedCache(new_keys, sorted_values, source, compact, valid, permutation, anchor)
