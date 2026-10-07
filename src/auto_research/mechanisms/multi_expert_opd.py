"""Extracted unchanged from auto_research.foundation_latest_20260914; stable mechanism boundary."""
from __future__ import annotations

import numpy as np

def multi_expert_opd(teacher_deltas: np.ndarray, gate_logits: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """SenseNova-U1.5 mixture-of-experts OPD direction."""
    deltas = np.asarray(teacher_deltas, dtype=np.float64)
    logits = np.asarray(gate_logits, dtype=np.float64)
    weights = np.exp(logits - logits.max(-1, keepdims=True))
    weights /= weights.sum(-1, keepdims=True)
    return np.sum(deltas * weights[..., None], axis=-2), weights
