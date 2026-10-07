"""Extracted unchanged from auto_research.post_training.latest_20260930_closure; stable mechanism boundary."""
from __future__ import annotations



def mas_role_advantage(target_role_logp, non_target_logp, response_mask):
    """MAS-OPD role-advantage specialization signal."""
    if target_role_logp.shape != non_target_logp.shape or target_role_logp.shape != response_mask.shape:
        raise ValueError("role signals and response mask must align")
    advantage = (target_role_logp.detach() - non_target_logp.detach()) * response_mask
    return advantage, {"active_tokens": int(response_mask.sum()), "mean_role_advantage": float(advantage.sum() / response_mask.sum().clamp_min(1))}
