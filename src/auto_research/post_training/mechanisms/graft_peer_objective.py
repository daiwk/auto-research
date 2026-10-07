"""Extracted unchanged from auto_research.post_training.latest_20260930_followup; stable mechanism boundary."""
from __future__ import annotations



def graft_peer_objective(receiver_log_prob, old_log_prob, peer_advantage, peer_log_likelihood, token_mask, *, clip: float = 0.2, gate_floor: float = 0.1):
    """GRAFT compatibility gate plus token-level clipped peer update."""
    import torch

    if not (receiver_log_prob.shape == old_log_prob.shape == token_mask.shape):
        raise ValueError("token tensors must match")
    if peer_advantage.shape != receiver_log_prob.shape[:1] or peer_log_likelihood.shape != peer_advantage.shape:
        raise ValueError("one peer advantage and compatibility score per response")
    compatibility = torch.softmax(peer_log_likelihood.detach(), 0)
    compatibility = compatibility.mul(len(compatibility)).clamp(min=gate_floor, max=2.0)
    ratio = (receiver_log_prob - old_log_prob.detach()).exp()
    advantage = peer_advantage[:, None].detach()
    surrogate = torch.minimum(ratio * advantage, ratio.clamp(1 - clip, 1 + clip) * advantage)
    mask = token_mask.to(surrogate.dtype)
    loss = -(compatibility[:, None] * surrogate * mask).sum() / mask.sum().clamp_min(1)
    return loss, {"mean_compatibility": float(compatibility.mean()), "clipped_fraction": float(((ratio < 1-clip) | (ratio > 1+clip)).float().mean())}
