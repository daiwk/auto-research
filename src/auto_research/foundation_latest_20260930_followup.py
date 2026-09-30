"""Executable L1 mechanisms from the 2026-09-29 foundation-model follow-up."""

from __future__ import annotations


def lift_topk_state(logits, *, k: int, temperature: float = 1.0):
    """LIFT Eq. (4): sparse next-token distribution used as feedback state."""
    import torch

    if logits.ndim < 2 or not 0 < k <= logits.shape[-1] or temperature <= 0:
        raise ValueError("invalid logits, k, or temperature")
    values, indices = torch.topk(logits, k, dim=-1)
    probabilities = torch.softmax(values / temperature, dim=-1)
    return torch.zeros_like(logits).scatter(-1, indices, probabilities)


def lift_fuse(token_hidden, state, embedding, gate, up, down):
    """LIFT Eq. (5): embedding-space state projection plus residual SwiGLU fusion."""
    import torch
    import torch.nn.functional as F

    if state.shape[:-1] != token_hidden.shape[:-1] or state.shape[-1] != embedding.shape[0]:
        raise ValueError("state/token/embedding shapes do not align")
    projected = state @ embedding
    joined = torch.cat((F.rms_norm(token_hidden, token_hidden.shape[-1:]), F.rms_norm(projected, projected.shape[-1:])), -1)
    return token_hidden + down(F.silu(gate(joined)) * up(joined))


def lift_loss(student_logits, teacher_logits, target_ids, *, state_weight: float = 1.0, k: int = 8):
    """LIFT Eq. (6): next-token CE plus forward KL on teacher top-k states."""
    import torch
    import torch.nn.functional as F

    if student_logits.shape != teacher_logits.shape or target_ids.shape != student_logits.shape[:-1]:
        raise ValueError("logit and target shapes do not align")
    ce = F.cross_entropy(student_logits.reshape(-1, student_logits.shape[-1]), target_ids.reshape(-1))
    teacher_state = lift_topk_state(teacher_logits.detach(), k=k)
    state_kl = (teacher_state * (teacher_state.clamp_min(1e-12).log() - F.log_softmax(student_logits, -1))).sum(-1).mean()
    return ce + state_weight * state_kl, {"token_ce": float(ce.detach()), "state_kl": float(state_kl.detach())}


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
