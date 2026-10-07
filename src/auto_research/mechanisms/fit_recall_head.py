"""Extracted unchanged from auto_research.foundation_latest_20260919; stable mechanism boundary."""
from __future__ import annotations

import numpy as np

def fit_recall_head(local_states, global_gain, ridge: float = 1e-3):
    x = np.asarray(local_states, dtype=np.float64)
    y = np.asarray(global_gain, dtype=np.float64)
    return np.linalg.solve(x.T @ x + ridge * np.eye(x.shape[1]), x.T @ y)
