"""Selective Internal Feedback (2610.21392v1), ranked profiles and dual masks.

Default windows preserve the paper's 550-token eligibility. Smaller explicit
configurations are mechanism diagnostics, never a replacement for that rule.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
import torch
from torch import Tensor


@dataclass(frozen=True)
class VotingConfig:
    windows: int = 10
    width: int = 100
    minimum_stride: int = 50
    window_wins: int = 8
    peer_fraction: float = .75
    epsilon: float = 1e-6

    def __post_init__(self):
        if min(self.windows, self.width, self.minimum_stride) < 1:
            raise ValueError("positive window dimensions required")
        if not 1 <= self.window_wins <= self.windows or not 0 < self.peer_fraction <= 1 or self.epsilon <= 0:
            raise ValueError("invalid voting thresholds")

    @property
    def minimum_length(self) -> int:
        return self.width + (self.windows - 1) * self.minimum_stride


def token_self_certainty(logits: Tensor) -> Tensor:
    """KL(U || pi), not negative entropy or sampled-token confidence."""
    return -math.log(logits.shape[-1]) - logits.log_softmax(-1).mean(-1)


@dataclass(frozen=True)
class SIFCredit:
    profiles: Tensor
    eligible: Tensor
    pairwise_votes: Tensor
    rewards: Tensor
    advantages: Tensor
    update_mask: Tensor
    retained_groups: Tensor


@torch.no_grad()
def prepare_credit(certainties: Tensor, valid_mask: Tensor, *, config: VotingConfig = VotingConfig()) -> SIFCredit:
    if certainties.ndim != 3 or certainties.shape != valid_mask.shape or valid_mask.dtype != torch.bool:
        raise ValueError("[groups,responses,tokens] certainties and boolean token mask required")
    if not torch.isfinite(certainties[valid_mask]).all():
        raise ValueError("valid token certainty must be finite")
    groups, responses, _ = certainties.shape
    lengths = valid_mask.sum(-1)
    eligible = lengths >= config.minimum_length
    profiles = torch.zeros(groups, responses, config.windows, device=certainties.device, dtype=certainties.dtype)
    for g in range(groups):
        for i in range(responses):
            if not eligible[g, i]:
                continue
            ranked = certainties[g, i][valid_mask[g, i]].sort(descending=True).values
            starts = [0] if config.windows == 1 else [k * (len(ranked) - config.width) // (config.windows - 1)
                                                       for k in range(config.windows)]
            profiles[g, i] = torch.stack([ranked[a:a + config.width].mean() for a in starts])
    wins = (profiles.unsqueeze(2) > profiles.unsqueeze(1)).sum(-1)
    pair_eligible = eligible.unsqueeze(2) & eligible.unsqueeze(1)
    pair_eligible &= ~torch.eye(responses, dtype=torch.bool, device=certainties.device).unsqueeze(0)
    pairwise = (wins >= config.window_wins) & pair_eligible
    peer_count = eligible.sum(-1, keepdim=True)
    rewards = ((pairwise.sum(-1) >= config.peer_fraction * (peer_count - 1)) & eligible & (peer_count >= 2)).to(certainties)
    advantages = torch.zeros_like(rewards)
    retained_groups = torch.zeros(groups, dtype=torch.bool, device=certainties.device)
    for g in range(groups):
        r = rewards[g, eligible[g]]
        if r.numel() < 2 or bool((r == r[0]).all()):
            continue
        retained_groups[g] = True
        # Appendix A.2 explicitly specifies sample standard deviation (n-1).
        advantages[g, eligible[g]] = (r - r.mean()) / (r.std(correction=1) + config.epsilon)
    update_mask = valid_mask & eligible.unsqueeze(-1) & retained_groups[:, None, None]
    return SIFCredit(profiles, eligible, pairwise, rewards, advantages.detach(), update_mask,
                     retained_groups)


def sif_ppo_loss(current_logp: Tensor, old_logp: Tensor, reference_logp: Tensor,
                 credit: SIFCredit, *, clip_epsilon: float = .2, kl_coefficient: float = .005) -> tuple[Tensor, dict]:
    """GRPO response-mean aggregation with policy *and* KL selection masks."""
    if current_logp.shape != credit.update_mask.shape or old_logp.shape != current_logp.shape or reference_logp.shape != current_logp.shape:
        raise ValueError("sampled score shapes must match the credit masks")
    if not 0 < clip_epsilon < 1 or kl_coefficient < 0:
        raise ValueError("invalid PPO configuration")
    mask = credit.update_mask
    # Apply the combined eligibility/group/token mask before exponentiation.
    # Post-exp masking cannot undo inf*0 in autograd at extreme padding scores.
    current = current_logp.masked_fill(~mask, 0)
    old = old_logp.detach().masked_fill(~mask, 0)
    reference = reference_logp.detach().masked_fill(~mask, 0)
    ratio = (current - old).exp()
    advantage = credit.advantages.detach().unsqueeze(-1)
    policy = -torch.minimum(ratio * advantage, ratio.clamp(1 - clip_epsilon, 1 + clip_epsilon) * advantage)
    ref_ratio = reference - current
    kl = ref_ratio.exp() - ref_ratio - 1
    # Every excluded token is removed from both terms, including KL-only updates.
    lengths = mask.sum(-1).clamp_min(1)
    response_loss = (policy + kl_coefficient * kl).masked_fill(~mask, 0).sum(-1) / lengths
    # Eq. 11 retains the original 1/G response factor within each retained
    # prompt group; an ineligible response contributes zero, not a new 1/G'.
    denominator = (credit.retained_groups.sum() * current_logp.shape[1]).clamp_min(1)
    loss = response_loss.sum() / denominator
    return loss, {"eligible_responses": int(credit.eligible.sum()),
        "retained_groups": int(credit.retained_groups.sum()), "updated_tokens": int(mask.sum()),
        "policy_loss": float((policy.masked_fill(~mask, 0).sum(-1) / lengths).sum().detach() / denominator),
        "kl_loss": float((kl.masked_fill(~mask, 0).sum(-1) / lengths).sum().detach() / denominator)}
