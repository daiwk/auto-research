"""Extracted unchanged from auto_research.foundation_latest_20260919; stable mechanism boundary."""
from __future__ import annotations

import numpy as np

def dqwen35_hybrid(hidden, recurrent_matrix, attention_matrix, mask_ratio=0.3):
    x = np.asarray(hidden, dtype=np.float64)
    forward = np.zeros_like(x); backward = np.zeros_like(x)
    for index in range(len(x)):
        forward[index] = np.tanh(x[index] + (forward[index - 1] @ recurrent_matrix if index else 0))
    for index in range(len(x) - 1, -1, -1):
        backward[index] = np.tanh(x[index] + (backward[index + 1] @ recurrent_matrix if index + 1 < len(x) else 0))
    attention = x @ attention_matrix
    output = (1 - mask_ratio) * (forward + backward) / 2 + mask_ratio * attention
    return output, {"bidirectional_passes": 2, "mask_ratio": float(mask_ratio), "hybrid_state_norm": float(np.linalg.norm(output))}
