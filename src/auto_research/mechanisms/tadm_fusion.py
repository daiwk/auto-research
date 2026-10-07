"""Extracted unchanged from auto_research.foundation_latest_20261001; stable mechanism boundary."""
from __future__ import annotations



def tadm_fusion(stale_anchor, current_state, gate, correction):
    """Time-anchored latent cache correction h'=h+g(c,h)*Delta(c,h)."""
    if stale_anchor.shape != current_state.shape:
        raise ValueError("anchor and current state must align")
    update = correction(current_state, stale_anchor)
    weight = gate(current_state, stale_anchor).sigmoid()
    if update.shape != stale_anchor.shape or weight.shape != stale_anchor.shape:
        raise ValueError("fusion outputs must align with anchor")
    return stale_anchor + weight * update, weight
