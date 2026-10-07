"""Extracted unchanged from auto_research.foundation_latest_20260916_followup; stable mechanism boundary."""
from __future__ import annotations

import numpy as np

def echo_lossless_verify(draft_probabilities, target_probabilities, uniforms):
    """Exact speculative accept/reject correction for an ECHO draft path."""
    draft = np.asarray(draft_probabilities, dtype=np.float64)
    target = np.asarray(target_probabilities, dtype=np.float64)
    uniforms = np.asarray(uniforms, dtype=np.float64)
    if draft.shape != target.shape or draft.ndim != 2:
        raise ValueError("draft and target probabilities must be equal 2-D arrays")
    if len(uniforms) < len(draft):
        raise ValueError("one uniform variate is required per draft position")
    accepted = 0
    correction = None
    for index, (q, p) in enumerate(zip(draft, target)):
        token = int(np.argmax(q))
        ratio = min(1.0, float(p[token] / max(q[token], 1e-12)))
        if uniforms[index] <= ratio:
            accepted += 1
            continue
        correction = np.maximum(p - q, 0.0)
        correction /= correction.sum() + 1e-12
        break
    return accepted, correction, {
        "accepted_tokens": float(accepted),
        "state_reuse_fraction": float(accepted / max(1, len(draft))),
        "lossless_correction_used": float(correction is not None),
    }
