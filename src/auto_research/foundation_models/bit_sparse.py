"""BitSparse tile bitmask/value format and real autograd, independently implemented.

Torch reference only: boolean compaction synchronizes shape; no fused Triton,
shared asynchronous arena, FP8 support, or training-throughput claim.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import torch
from torch import Tensor


@dataclass(frozen=True)
class SparseActivation:
    mask_bytes: Tensor
    values: Tensor
    tile_prefix: Tensor
    shape: tuple[int, int]
    tile_size: int

    @property
    def storage_bytes(self) -> int:
        return sum(x.numel() * x.element_size() for x in (self.mask_bytes, self.values, self.tile_prefix))


def pack_activation(activation: Tensor, tile_size: int = 64) -> SparseActivation:
    if (activation.ndim != 2 or not activation.is_floating_point() or activation.numel() == 0 or
            not bool(torch.isfinite(activation).all()) or bool(torch.signbit(activation).any())):
        raise ValueError("nonempty finite nonnegative 2D activation, including positive zero, required")
    if not isinstance(tile_size, int) or tile_size < 1 or tile_size ** 2 % 8:
        raise ValueError("tile_size squared must be byte aligned")
    m, n = activation.shape
    gm, gn = math.ceil(m / tile_size), math.ceil(n / tile_size)
    padded = activation.new_zeros(gm * tile_size, gn * tile_size)
    padded[:m, :n] = activation
    tiles = padded.reshape(gm, tile_size, gn, tile_size).permute(0, 2, 1, 3).reshape(-1, tile_size ** 2)
    support = tiles > 0
    shifts = torch.arange(8, device=activation.device)
    mask = (support.reshape(-1, 8).to(torch.int64) << shifts).sum(-1).to(torch.uint8)
    counts = support.sum(-1)
    if int(counts.sum()) >= 2 ** 31:
        raise ValueError("reference prefix supports fewer than 2^31 stored positives")
    prefix = (counts.cumsum(0) - counts).to(torch.int32)
    return SparseActivation(mask, tiles[support], prefix, (m, n), tile_size)


def unpack_activation(packed: SparseActivation) -> Tensor:
    m, n = packed.shape
    b = packed.tile_size
    gm, gn = math.ceil(m / b), math.ceil(n / b)
    shifts = torch.arange(8, device=packed.mask_bytes.device)
    support = ((packed.mask_bytes.to(torch.int64).unsqueeze(-1) >> shifts) & 1).bool().reshape(gm * gn, b * b)
    counts = support.sum(-1)
    expected = (counts.cumsum(0) - counts).to(torch.int32)
    if not torch.equal(expected, packed.tile_prefix) or int(counts.sum()) != packed.values.numel():
        raise ValueError("inconsistent compact values/prefix")
    tiles = packed.values.new_zeros(gm * gn, b * b)
    tiles[support] = packed.values
    padded = tiles.reshape(gm, gn, b, b).permute(0, 2, 1, 3).reshape(gm * b, gn * b)
    return padded[:m, :n]


class _SparseActivationLinear(torch.autograd.Function):
    @staticmethod
    def forward(ctx, z: Tensor, weight: Tensor, power: int, tile_size: int):
        if (power not in (1, 2) or z.ndim != 2 or weight.ndim != 2 or
                z.shape[-1] != weight.shape[-1] or z.device != weight.device or z.dtype != weight.dtype):
            raise ValueError("compatible 2D linear inputs and power 1/2 required")
        h = torch.where(z > 0, z, torch.zeros_like(z))
        packed = pack_activation(h, tile_size)
        ctx.save_for_backward(packed.mask_bytes, packed.values, packed.tile_prefix, weight)
        ctx.shape, ctx.tile_size, ctx.power = packed.shape, tile_size, power
        return h.pow(power) @ weight.t()

    @staticmethod
    def backward(ctx, gradient: Tensor):
        mask, values, prefix, weight = ctx.saved_tensors
        h = unpack_activation(SparseActivation(mask, values, prefix, ctx.shape, ctx.tile_size))
        grad_z = gradient @ weight
        grad_z = grad_z * ((h > 0).to(h.dtype) if ctx.power == 1 else 2 * h)
        grad_weight = gradient.t() @ h.pow(ctx.power)
        return grad_z, grad_weight, None, None


def sparse_activation_linear(z: Tensor, weight: Tensor, *, power: int = 2, tile_size: int = 64) -> Tensor:
    return _SparseActivationLinear.apply(z, weight, power, tile_size)
