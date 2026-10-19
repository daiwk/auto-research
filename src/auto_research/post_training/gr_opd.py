"""GR-OPD: detached discounted sequence credit and response-balanced PPO.

The implemented practical estimator is not claimed to inherit the unmodified
raw-sum estimator's theoretical unbiasedness after discounting/clipping/PPO.
"""
from __future__ import annotations

from collections.abc import Sequence
import math

import torch
from torch import Tensor


def sequence_credit(teacher_logp: Tensor, behavior_logp: Tensor, actor_mask: Tensor,
                    query_ids: Sequence[str], *, gamma: float = .99,
                    pressure: float = .25, epsilon: float = 1e-6,
                    feedback_clip: float = 5., advantage_clip: float = 5.) -> tuple[Tensor, dict]:
    """Practical GR-OPD credit: normalized discounted mean then group pressure."""
    if teacher_logp.ndim != 2 or teacher_logp.shape != behavior_logp.shape:
        raise ValueError("aligned [response,token] teacher and behavior log probabilities required")
    if actor_mask.shape != teacher_logp.shape or actor_mask.dtype != torch.bool or not bool(actor_mask.any(1).all()):
        raise ValueError("each response needs a nonempty Boolean actor mask")
    if not teacher_logp.is_floating_point() or not behavior_logp.is_floating_point():
        raise ValueError("floating log probabilities required")
    if any(value.device != teacher_logp.device for value in (behavior_logp, actor_mask)):
        raise ValueError("credit tensors must share a device")
    if len(query_ids) != teacher_logp.shape[0] or any(not isinstance(q, str) or not q for q in query_ids):
        raise ValueError("one nonempty query ID per response required")
    if not all(math.isfinite(v) for v in (gamma, pressure, epsilon, feedback_clip, advantage_clip)) or not 0 < gamma <= 1 or not 0 <= pressure <= 1 or min(epsilon, feedback_clip, advantage_clip) <= 0:
        raise ValueError("finite 0<gamma<=1, 0<=pressure<=1 and positive safeguards required")
    if not torch.isfinite(teacher_logp[actor_mask]).all() or not torch.isfinite(behavior_logp[actor_mask]).all():
        raise ValueError("finite active log probabilities required")
    feedback = (torch.where(actor_mask, teacher_logp.detach(), 0.) - torch.where(actor_mask, behavior_logp.detach(), 0.)).clamp(-feedback_clip, feedback_clip)
    exponent = (actor_mask.cumsum(1) - 1).clamp_min(0)
    weights = torch.where(actor_mask, gamma ** exponent.to(feedback.dtype), 0.)
    scores = (weights * feedback).sum(1) / weights.sum(1)
    advantages = torch.empty_like(scores)
    groups = []
    for query in dict.fromkeys(query_ids):
        indices = [i for i, value in enumerate(query_ids) if value == query]
        values = scores[indices]
        mean, std = values.mean(), values.std(correction=0)
        advantages[indices] = ((values - mean + pressure * mean) / (std + epsilon)).clamp(-advantage_clip, advantage_clip)
        groups.append({"query_id": query, "response_indices": indices, "mean": float(mean), "population_std": float(std)})
    return advantages.detach(), {"sequence_scores": scores.detach(), "clipped_feedback": feedback.detach(), "groups": groups}


def clipped_policy_loss(current_logp: Tensor, behavior_logp: Tensor,
                        actor_mask: Tensor, advantages: Tensor,
                        *, clip_ratio: float = .2) -> Tensor:
    """PPO minimum, first mean within response and then mean across responses."""
    if current_logp.ndim != 2 or current_logp.shape != behavior_logp.shape or actor_mask.shape != current_logp.shape:
        raise ValueError("aligned [response,token] inputs required")
    if actor_mask.dtype != torch.bool or not bool(actor_mask.any(1).all()) or advantages.shape != (current_logp.shape[0],):
        raise ValueError("nonempty actor masks and one advantage per response required")
    if any(value.device != current_logp.device for value in (behavior_logp, actor_mask, advantages)):
        raise ValueError("PPO tensors must share a device")
    if not current_logp.is_floating_point() or not behavior_logp.is_floating_point() or not advantages.is_floating_point():
        raise ValueError("floating log probabilities and advantages required")
    if not torch.isfinite(current_logp[actor_mask]).all() or not torch.isfinite(behavior_logp[actor_mask]).all() or not torch.isfinite(advantages).all():
        raise ValueError("finite active inputs required")
    if not 0 < clip_ratio < 1 or not math.isfinite(clip_ratio):
        raise ValueError("finite clipping ratio in (0,1) required")
    difference = torch.where(actor_mask, current_logp, 0.) - torch.where(actor_mask, behavior_logp.detach(), 0.)
    a = advantages.detach()[:, None]
    # Evaluate only the selected PPO branch in log space. Computing exp(1000)
    # and then selecting the clipped branch gives 0*inf -> NaN in backward.
    # Positive advantages cap the upper ratio; negative advantages floor its
    # lower ratio. This is algebraically the exact minimum, not ratio clipping
    # added to the unclipped objective. An unrepresentable selected negative-
    # advantage branch is explicitly rejected rather than silently saturated.
    selected_log_ratio = torch.where(a >= 0, difference.clamp_max(math.log1p(clip_ratio)),
                                    difference.clamp_min(math.log1p(-clip_ratio)))
    if bool((selected_log_ratio[actor_mask] > math.log(torch.finfo(current_logp.dtype).max)).any()):
        raise ValueError("selected PPO ratio is not representable in the input dtype")
    objective = selected_log_ratio.exp() * a
    if not torch.isfinite(objective[actor_mask]).all():
        raise ValueError("selected PPO objective is not representable in the input dtype")
    return -(torch.where(actor_mask, objective, 0.).sum(1) / actor_mask.sum(1)).mean()


def teacher_scoring_copy(response_tokens: Tensor, response_mask: Tensor,
                         *, student_eos: int, teacher_eos: int) -> Tensor:
    """Map a terminal EOS in a scoring-only copy; never rewrite the rollout."""
    if response_tokens.ndim != 2 or response_tokens.dtype != torch.long or response_mask.shape != response_tokens.shape or response_mask.dtype != torch.bool:
        raise ValueError("aligned int64 responses and Boolean masks required")
    if response_tokens.device != response_mask.device or not bool(response_mask.any(1).all()):
        raise ValueError("nonempty responses on one device required")
    result = response_tokens.clone()
    for row in range(result.shape[0]):
        last = int(response_mask[row].nonzero()[-1])
        if int(result[row, last]) == student_eos:
            result[row, last] = teacher_eos
    return result
