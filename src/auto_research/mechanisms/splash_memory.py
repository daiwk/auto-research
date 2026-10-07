"""Extracted unchanged from auto_research.foundation_latest_20261001; stable mechanism boundary."""
from __future__ import annotations



def splash_memory(layout: str, *, attention_weights: float, batch: int, kv_heads: int, sequence: int, tensor_parallel: int):
    """Per-device attention memory model from SPLASH Section 2."""
    if tensor_parallel < 1 or min(attention_weights, batch, kv_heads, sequence) < 0:
        raise ValueError("invalid SPLASH memory inputs")
    kv = batch * kv_heads * sequence
    if layout == "tp":
        return attention_weights / tensor_parallel + kv
    if layout == "dop":
        return attention_weights / tensor_parallel + kv / tensor_parallel
    if layout in {"dp", "cp"}:
        return attention_weights + kv / tensor_parallel
    raise ValueError(f"unknown layout {layout}")
