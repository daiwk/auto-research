"""Extracted unchanged from auto_research.foundation_latest_20260914; stable mechanism boundary."""
from __future__ import annotations

import math

def repetition_regularization(repetition_factor: float, *, sparse_model: bool) -> dict[str, float]:
    """Repeat-aware masking/dropout schedule from the dense-vs-MoE study."""
    if repetition_factor < 1:
        raise ValueError("repetition_factor must be >= 1")
    pressure = math.log2(repetition_factor) / 6.0
    dropout = min(0.45, 0.05 + (0.18 if sparse_model else 0.10) * pressure)
    masking = min(0.50, 0.08 + (0.22 if sparse_model else 0.12) * pressure)
    return {"dropout": dropout, "token_masking": masking, "repeat_pressure": pressure}
