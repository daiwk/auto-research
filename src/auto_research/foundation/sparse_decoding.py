"""Decoding-only Wanda calibration and 32-bit N:M bitmask packing.

Wanda is the paper's alternative pruning backend, not an OBS approximation.
The optional CUDA module executes real SpMV; dense zeros are never presented
as sparse execution. Prefill deliberately uses the pruned dense matrix.
"""
from __future__ import annotations

from contextlib import contextmanager

import torch


def wanda_nm(weight, sum_squares, *, n=2, m=4):
    if (weight.ndim != 2 or sum_squares.shape != (weight.shape[1],) or
            m not in {4, 8, 16, 32} or n * 2 != m or weight.shape[1] % 32):
        raise ValueError("aligned 50% N:M matrix with 32-column words required")
    if not bool(torch.isfinite(weight).all()) or not bool(torch.isfinite(sum_squares).all()) or bool((sum_squares < 0).any()):
        raise ValueError("finite weights and nonnegative decoded activation energy required")
    score = weight.float().abs() * sum_squares.sqrt()[None, :]
    groups = score.reshape(weight.shape[0], -1, m)
    indices = groups.argsort(dim=-1, descending=True, stable=True)[..., :n]
    keep = torch.zeros_like(groups, dtype=torch.bool).scatter_(-1, indices, True).reshape_as(weight)
    return weight.masked_fill(~keep, 0), keep


def pack_bitmask(weight, keep):
    if weight.ndim != 2 or keep.shape != weight.shape or keep.dtype != torch.bool or weight.shape[1] % 32:
        raise ValueError("aligned boolean pattern and 32-column words required")
    mask = keep.reshape(weight.shape[0], -1, 32)
    if not bool((mask.sum(-1) == 16).all()):
        raise ValueError("exactly sixteen selected bits per word required")
    # Increasing columns: packed value #r corresponds to the r-th set bit.
    values = weight.reshape(*mask.shape)[mask].reshape(weight.shape[0], -1, 16).contiguous()
    bit = (mask.to(torch.int64) << torch.arange(32, device=weight.device, dtype=torch.int64)).sum(-1)
    return values, bit.to(torch.uint32).contiguous()


def unpack_bitmask(values, words):
    if values.ndim != 3 or values.shape[-1] != 16 or words.shape != values.shape[:2]:
        raise ValueError("aligned packed values/words required")
    keep = ((words.to(torch.int64)[..., None] >> torch.arange(32, device=words.device)) & 1).bool()
    if not bool((keep.sum(-1) == 16).all()):
        raise ValueError("invalid packed word")
    dense = torch.zeros(*words.shape, 32, dtype=values.dtype, device=values.device)
    dense[keep] = values.flatten()
    return dense.flatten(1)


class DecodeCalibration:
    """An explicit phase flag excludes prefill even for a one-token prompt."""

    def __init__(self, layers):
        self.phase = False
        self.counts = {key: 0 for key in layers}
        self.energy = {key: torch.zeros(layer.in_features, device=layer.weight.device) for key, layer in layers.items()}
        self.handles = []
        for key, layer in layers.items():
            def record(_, inputs, key=key):
                if not self.phase:
                    return
                activation = inputs[0].detach().float().reshape(-1, inputs[0].shape[-1])
                self.energy[key].add_(activation.square().sum(0))
                self.counts[key] += len(activation)
            self.handles.append(layer.register_forward_pre_hook(record))

    @contextmanager
    def decoding(self):
        if self.phase:
            raise ValueError("nested decoding calibration phase")
        self.phase = True
        try:
            yield
        finally:
            self.phase = False

    def close(self):
        for hook in self.handles:
            hook.remove()
        self.handles.clear()


class PackedDecodeLinear(torch.nn.Module):
    def __init__(self, weight, keep, bias=None):
        super().__init__()
        values, words = pack_bitmask(weight, keep)
        self.register_buffer("weight", weight.contiguous())
        self.register_buffer("values", values)
        self.register_buffer("words", words)
        self.register_buffer("bias", None if bias is None else bias.detach().clone())
        self.in_features, self.out_features = weight.shape[1], weight.shape[0]
        self.sparse_calls = 0
        self.prefill_calls = 0

    def forward(self, value):
        if value.numel() // self.in_features != 1:
            self.prefill_calls += 1
            return torch.nn.functional.linear(value, self.weight, self.bias)
        if value.device.type != "cuda":
            raise ValueError("single-token sparse path requires validated NVIDIA CUDA")
        from .sparse_decoding_cuda import bitmask_spmv
        self.sparse_calls += 1
        result = bitmask_spmv(self.values, self.words, value.reshape(-1))
        if self.bias is not None:
            result = result + self.bias
        return result.reshape(*value.shape[:-1], self.out_features)
