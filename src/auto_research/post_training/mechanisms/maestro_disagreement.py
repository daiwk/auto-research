"""Extracted unchanged from auto_research.post_training.latest_20261001; stable mechanism boundary."""
from __future__ import annotations



def maestro_disagreement(teacher_prob, student_prob, *, top_k: int, alpha: float = 1.0, tau: float = 1.0):
    """MAESTRO top-k coverage/Bhattacharyya token PDS and prefix aggregation."""
    import torch

    if teacher_prob.shape != student_prob.shape or not 0 < top_k <= teacher_prob.shape[-1]:
        raise ValueError("invalid policy distributions or top-k")
    t_values, t_index = teacher_prob.topk(top_k, dim=-1)
    s_values, s_index = student_prob.topk(top_k, dim=-1)
    t_values = t_values / t_values.sum(-1, keepdim=True)
    s_lookup = student_prob.gather(-1, t_index)
    s_lookup = s_lookup / student_prob.gather(-1, s_index).sum(-1, keepdim=True).clamp_min(1e-12)
    coverage = (t_index[..., :, None] == s_index[..., None, :]).any(-1).to(t_values.dtype)
    c_score = (t_values * coverage).sum(-1)
    b_score = torch.sqrt(t_values * s_lookup.clamp_min(0)).sum(-1)
    token_pds = 1 - c_score * b_score
    positions = torch.arange(token_pds.shape[-1], device=token_pds.device, dtype=token_pds.dtype)
    weights = 1 + alpha * torch.exp(-positions / tau)
    prefix_pds = (token_pds * weights).sum(-1) / weights.sum()
    return token_pds, prefix_pds
