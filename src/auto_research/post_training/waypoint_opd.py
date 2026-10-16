"""Waypoint-OPD (2610.21601v1), Eqs. 5--13 and Appendix B PPO."""
from __future__ import annotations

from dataclasses import dataclass
import torch
from torch import Tensor


@dataclass(frozen=True)
class WaypointCredit:
    candidates: Tensor
    old_candidate_logp: Tensor
    advantages: Tensor
    gate: Tensor
    scale: Tensor
    valid_mask: Tensor
    old_sample_logp: Tensor
    reference_sample_logp: Tensor


def validate_snapshot_lineage(identities: list[dict]) -> None:
    """Three ordered snapshots must come from one teacher training trajectory."""
    if len(identities) != 3 or not identities[0].get("run_id"):
        raise ValueError("initial/waypoint/final snapshot identities required")
    if len({x.get("run_id") for x in identities}) != 1:
        raise ValueError("teacher snapshots must share one training run")
    steps = [x.get("step", -1) for x in identities]
    if not 0 <= steps[0] < steps[1] < steps[2]:
        raise ValueError("teacher snapshot steps must be strictly ordered")


@torch.no_grad()
def prepare_credit(old_logits: Tensor, initial_logits: Tensor, waypoint_logits: Tensor,
                   final_logits: Tensor, sampled_ids: Tensor, reference_sample_logp: Tensor,
                   valid_mask: Tensor, *, top_k: int = 16, target_mean: float = .8,
                   scale_bounds: tuple[float, float] = (.75, 1.5), norm_epsilon: float = 1e-8,
                   snapshot_identities: list[dict] | None = None) -> WaypointCredit:
    if snapshot_identities is not None:
        validate_snapshot_lineage(snapshot_identities)
    if not all(x.shape == old_logits.shape for x in (initial_logits, waypoint_logits, final_logits)):
        raise ValueError("three teacher views must score the same prefix/vocabulary")
    if valid_mask.shape != old_logits.shape[:-1] or sampled_ids.shape != valid_mask.shape:
        raise ValueError("response mask and sampled token shape mismatch")
    if reference_sample_logp.shape != valid_mask.shape or valid_mask.dtype != torch.bool:
        raise ValueError("reference scores and boolean valid-token mask required")
    if not 1 <= top_k <= old_logits.shape[-1] or target_mean <= 0 or norm_epsilon <= 0:
        raise ValueError("invalid gate configuration")
    if not 0 < scale_bounds[0] <= scale_bounds[1]:
        raise ValueError("invalid positive scale bounds")
    old = old_logits.log_softmax(-1)
    candidates = old.topk(top_k, -1).indices
    q = old.gather(-1, candidates).softmax(-1)
    first, middle, last = [x.log_softmax(-1).gather(-1, candidates)
                           for x in (initial_logits, waypoint_logits, final_logits)]
    early, late = middle - first, last - middle
    early = early - (q * early).sum(-1, keepdim=True)
    late = late - (q * late).sum(-1, keepdim=True)
    early_norm = (q * early.square()).sum(-1).sqrt()
    late_norm = (q * late.square()).sum(-1).sqrt()
    fallback = (early_norm <= norm_epsilon) | (late_norm <= norm_epsilon)
    denom = (early_norm * late_norm).clamp_min(torch.finfo(q.dtype).tiny)
    cosine = ((q * early * late).sum(-1) / denom).clamp(-1, 1)
    gate = torch.where(fallback, torch.ones_like(cosine), cosine.clamp_min(0))
    gate = torch.where(valid_mask, gate, torch.zeros_like(gate))
    mean = gate[valid_mask].mean() if valid_mask.any() else gate.sum()
    scale = (target_mean / mean.clamp_min(torch.finfo(torch.float32).tiny)).clamp(*scale_bounds)
    advantages = scale * q * gate.unsqueeze(-1) * (early + late)
    return WaypointCredit(candidates, old.gather(-1, candidates), advantages.detach(), gate, scale,
        valid_mask.detach().clone(), old.gather(-1, sampled_ids.unsqueeze(-1)).squeeze(-1),
        reference_sample_logp.detach().clone())


def waypoint_ppo_loss(current_logits: Tensor, sampled_ids: Tensor, credit: WaypointCredit, *,
                      clip_epsilon: float = .2, dual_clip: float = 3., kl_coefficient: float = 2.5):
    """Dense candidate dual-clipped PPO plus sampled-token low-variance KL.

    Credit/support and all teacher/reference terms stay detached. The sampled KL
    estimator is exp(log pi_ref - log pi) - (log pi_ref - log pi) - 1.
    """
    if not 0 < clip_epsilon < 1 or dual_clip <= 1 or kl_coefficient < 0:
        raise ValueError("invalid PPO configuration")
    valid = credit.valid_mask
    # Remove padding before nonlinear operations. Masking an already-overflowed
    # exp afterwards leaves inf*0/NaN in its backward graph.
    logp = current_logits.masked_fill(~valid.unsqueeze(-1), 0).log_softmax(-1)
    candidate_lp = logp.gather(-1, credit.candidates)
    candidate_log_ratio = (candidate_lp - credit.old_candidate_logp.detach()).masked_fill(~valid.unsqueeze(-1), 0)
    ratio = candidate_log_ratio.exp()
    advantage = credit.advantages.detach()
    ordinary = torch.minimum(ratio * advantage, ratio.clamp(1 - clip_epsilon, 1 + clip_epsilon) * advantage)
    surrogate = torch.where(advantage < 0, torch.maximum(ordinary, dual_clip * advantage), ordinary)
    sampled_lp = logp.gather(-1, sampled_ids.unsqueeze(-1)).squeeze(-1)
    log_ratio = (credit.reference_sample_logp.detach() - sampled_lp).masked_fill(~valid, 0)
    kl = log_ratio.exp() - log_ratio - 1
    per_token = -surrogate.sum(-1) + kl_coefficient * kl
    loss = per_token.masked_fill(~valid, 0).sum() / valid.sum().clamp_min(1)
    return loss, {"mean_gate": float(credit.gate[valid].mean()) if valid.any() else 0.,
        "zero_gate_fraction": float((credit.gate[valid] == 0).float().mean()) if valid.any() else 0.,
        "batch_scale": float(credit.scale), "valid_tokens": int(valid.sum())}
