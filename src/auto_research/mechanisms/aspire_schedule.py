"""Extracted unchanged from auto_research.foundation_latest_20260919; stable mechanism boundary."""
from __future__ import annotations

import numpy as np

def aspire_schedule(acceptance, draft_cost, verify_cost, batch_sizes, refresh_interval=4):
    acceptance = np.asarray(acceptance, dtype=np.float64)
    batch = np.asarray(batch_sizes, dtype=np.float64)
    speculative_gain = acceptance * verify_cost - draft_cost * (1 + 0.1 * batch)
    draft_lengths = np.maximum(1, np.floor(1 + 7 * np.clip(speculative_gain / max(verify_cost, 1e-8), 0, 1))).astype(int)
    refresh = np.arange(len(draft_lengths)) % refresh_interval == 0
    return draft_lengths, refresh, {"mean_draft_length": float(draft_lengths.mean()), "refresh_fraction": float(refresh.mean()), "positive_gain_fraction": float((speculative_gain > 0).mean())}
