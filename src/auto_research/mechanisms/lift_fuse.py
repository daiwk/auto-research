"""Extracted unchanged from auto_research.foundation_latest_20260930_followup; stable mechanism boundary."""
from __future__ import annotations



def lift_fuse(token_hidden, state, embedding, gate, up, down):
    """LIFT Eq. (5): embedding-space state projection plus residual SwiGLU fusion."""
    import torch
    import torch.nn.functional as F

    if state.shape[:-1] != token_hidden.shape[:-1] or state.shape[-1] != embedding.shape[0]:
        raise ValueError("state/token/embedding shapes do not align")
    projected = state @ embedding
    joined = torch.cat((F.rms_norm(token_hidden, token_hidden.shape[-1:]), F.rms_norm(projected, projected.shape[-1:])), -1)
    return token_hidden + down(F.silu(gate(joined)) * up(joined))
