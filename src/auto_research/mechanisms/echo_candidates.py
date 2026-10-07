"""Extracted unchanged from auto_research.foundation_latest_20260916_followup; stable mechanism boundary."""
from __future__ import annotations

import numpy as np

def echo_candidates(early_logits, final_logits, retrieved_tokens=(), top_k: int = 4):
    """ECHO asymmetric bonus-logit candidate union for the next draft tree."""
    early = np.asarray(early_logits, dtype=np.float64)
    final = np.asarray(final_logits, dtype=np.float64)
    if early.shape != final.shape or early.ndim != 1:
        raise ValueError("early_logits and final_logits must be equal 1-D arrays")
    k = max(1, min(int(top_k), len(early)))
    early_bonus = early + np.maximum(final - early, 0.0)
    final_bonus = final + np.maximum(early - final, 0.0)
    ranked = list(np.argsort(early_bonus)[-k:][::-1])
    ranked += list(np.argsort(final_bonus)[-k:][::-1])
    ranked += [int(token) for token in retrieved_tokens if 0 <= int(token) < len(early)]
    candidates = tuple(dict.fromkeys(ranked))
    return candidates, {
        "early_bonus_mass": float(np.maximum(final - early, 0.0).sum()),
        "final_bonus_mass": float(np.maximum(early - final, 0.0).sum()),
        "candidate_count": float(len(candidates)),
    }
