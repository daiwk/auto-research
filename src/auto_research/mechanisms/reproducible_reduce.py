"""Extracted unchanged from auto_research.foundation_latest_20260916_followup; stable mechanism boundary."""
from __future__ import annotations

import hashlib
import numpy as np

def reproducible_reduce(shards):
    """OPEN-1B fixed-order float64 reduction with a canonical state hash."""
    arrays = [np.asarray(shard, dtype=np.float64) for shard in shards]
    if not arrays or any(array.shape != arrays[0].shape for array in arrays):
        raise ValueError("non-empty equal-shaped shards required")
    total = np.zeros_like(arrays[0])
    for array in arrays:  # order is part of the contract
        total = np.add(total, array, dtype=np.float64)
    reduced = total * np.float64(1.0 / len(arrays))
    digest = hashlib.sha256(reduced.astype("<f8", copy=False).tobytes()).hexdigest()
    return reduced, {"shards": float(len(arrays)), "state_hash": digest, "bitwise_replay": True}
