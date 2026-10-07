"""Extracted unchanged from auto_research.foundation_latest_20260930_followup; stable mechanism boundary."""
from __future__ import annotations



def triadic_linear_attention(query, second_query, key, second_key, value, *, decay=None):
    """Triadic Linear Attention Eqs. (2)-(3), recurrent reference implementation."""
    import torch

    if not (query.shape == key.shape) or not (second_query.shape == second_key.shape):
        raise ValueError("query/key pairs must match")
    if query.shape[:-1] != value.shape[:-1] or query.shape[:-1] != second_query.shape[:-1]:
        raise ValueError("all sequences must share batch and time axes")
    batch, length, key_dim = query.shape
    second_dim, value_dim = second_query.shape[-1], value.shape[-1]
    state = torch.zeros(batch, key_dim, second_dim, value_dim, device=query.device, dtype=query.dtype)
    outputs = []
    for index in range(length):
        if decay is not None:
            if decay.shape != (batch, length, second_dim):
                raise ValueError("decay must be [batch,time,second-key]")
            state = state * decay[:, index, None, :, None]
        state = state + torch.einsum("bi,bj,bk->bijk", key[:, index], second_key[:, index], value[:, index])
        outputs.append(torch.einsum("bi,bj,bijk->bk", query[:, index], second_query[:, index], state))
    return torch.stack(outputs, 1), state
