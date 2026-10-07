"""Extracted unchanged from auto_research.foundation_latest_20260919; stable mechanism boundary."""
from __future__ import annotations

import numpy as np

def on_demand_attention(query, local_keys, local_values, global_keys, global_values, recall_head, threshold=0.0):
    query = np.asarray(query, dtype=np.float64)
    def attend(keys, values):
        scores = np.asarray(keys) @ query / np.sqrt(query.size)
        weights = np.exp(scores - scores.max()); weights /= weights.sum()
        return weights @ np.asarray(values)
    local = attend(local_keys, local_values)
    predicted_gain = float(local @ np.asarray(recall_head))
    used_global = predicted_gain > threshold
    output = attend(global_keys, global_values) if used_global else local
    return output, {"predicted_global_gain": predicted_gain, "global_attention_used": used_global, "kv_retained": len(global_keys)}
