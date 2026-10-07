"""Extracted unchanged from auto_research.foundation_latest_20260914; stable mechanism boundary."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

@dataclass(frozen=True)
class QuantizedBlock:
    codes: np.ndarray
    minimum: np.ndarray
    scale: np.ndarray
    bits: int

def windowed_key_quantize(keys: np.ndarray, *, bits: int = 2, window: int = 8) -> list[QuantizedBlock]:
    """OmniKVQuant short-window asymmetric quantization for temporal keys."""
    keys = np.asarray(keys, dtype=np.float64)
    if keys.ndim != 2 or bits < 1 or window < 1:
        raise ValueError("keys must be [tokens, dimensions], with positive bits/window")
    levels = 2**bits - 1
    blocks = []
    for start in range(0, len(keys), window):
        values = keys[start : start + window]
        minimum = values.min(0)
        maximum = values.max(0)
        scale = np.maximum((maximum - minimum) / levels, 1e-12)
        codes = np.clip(np.rint((values - minimum) / scale), 0, levels).astype(np.uint8)
        blocks.append(QuantizedBlock(codes, minimum, scale, bits))
    return blocks

def dequantize_blocks(blocks: list[QuantizedBlock]) -> np.ndarray:
    return np.concatenate([
        block.minimum + block.scale * block.codes.astype(np.float64)
        for block in blocks
    ])
