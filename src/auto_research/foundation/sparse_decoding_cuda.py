"""Real 50%-sparse SpMV: one uint32 per 32 columns, 16 bit scans.

Lazy optional Triton import keeps base installation free of CUDA dependencies.
Independent straightforward kernel, not the original optimized release.
"""
from __future__ import annotations

import torch


def bitmask_spmv(values, words, vector):
    if (not values.is_cuda or not words.is_cuda or not vector.is_cuda or
            values.device != words.device or values.device != vector.device):
        raise ValueError("CUDA tensors on one device required")
    if (values.ndim != 3 or values.shape[-1] != 16 or words.shape != values.shape[:2]
            or vector.shape != (words.shape[1] * 32,) or words.dtype != torch.uint32
            or values.dtype != vector.dtype or values.dtype not in {torch.float16, torch.bfloat16, torch.float32}):
        raise ValueError("aligned packed words/values and real input vector required")
    if not values.is_contiguous() or not words.is_contiguous() or not vector.is_contiguous():
        raise ValueError("contiguous packed storage required")
    import triton
    kernel = _kernel()
    output = torch.empty(values.shape[0], dtype=vector.dtype, device=vector.device)
    kernel[(triton.cdiv(len(output), 4),)](values, words, vector, output,
                                          len(output), words.shape[1], triton.next_power_of_2(words.shape[1]))
    return output


def _kernel():
    # Triton's compiler resolves annotation/module globals, not Python closure
    # imports. Keep the optional dependency in a lazily loaded dedicated module.
    from .sparse_decoding_triton import spmv
    return spmv
