"""Differentiable ToolSearcher event-level clipped policy objective.

The caller must create grouped on-policy rollouts and assign each generated
token to a search event or the final selection. Prompt/retrieved tokens use
the ignored index and never receive policy or KL gradients.
"""

from __future__ import annotations

import torch

from auto_research.agent_research.toolsearcher_credit import TraceCredit


IGNORED = -2
SELECTION = -1


def grouped_policy_loss(
    logprobs: torch.Tensor,
    old_logprobs: torch.Tensor,
    token_events: torch.Tensor,
    credits: tuple[TraceCredit, ...],
    *,
    clip_epsilon: float = 0.2,
    reference_logprobs: torch.Tensor | None = None,
    kl_weight: float = 0.0,
) -> torch.Tensor:
    """Minimize negative Eq. 4 plus an optional nonnegative sampled KL.

    ``logprobs`` are differentiable log probabilities of sampled tokens.
    ``old_logprobs`` and the optional reference are detached rollouts. Each
    search event's advantage comes from Eq. 5; the final selection's from
    Eq. 7. The token event map MUST come from the model/tool transcript, not
    from target tool IDs, which are evaluator-private.
    """
    if logprobs.ndim != 2 or not logprobs.shape[0] or not logprobs.shape[1]:
        raise ValueError("expected nonempty [rollouts, tokens] log probabilities")
    if old_logprobs.shape != logprobs.shape or token_events.shape != logprobs.shape:
        raise ValueError("rollout tensors must share a shape")
    if reference_logprobs is not None and reference_logprobs.shape != logprobs.shape:
        raise ValueError("reference log probabilities must share the rollout shape")
    if len(credits) != logprobs.shape[0] or clip_epsilon <= 0 or kl_weight < 0:
        raise ValueError("credit count, clip range, or KL weight is invalid")
    if kl_weight and reference_logprobs is None:
        raise ValueError("a reference policy is required for KL regularization")
    if token_events.dtype not in (torch.int8, torch.int16, torch.int32, torch.int64):
        raise ValueError("token event IDs must be integers")
    if not torch.isfinite(logprobs).all() or not torch.isfinite(old_logprobs).all():
        raise ValueError("log probabilities must be finite")
    if reference_logprobs is not None and not torch.isfinite(reference_logprobs).all():
        raise ValueError("reference log probabilities must be finite")

    losses = []
    for index, credit in enumerate(credits):
        event_ids = token_events[index]
        if (event_ids < IGNORED).any() or (event_ids >= len(credit.search_advantages)).any():
            raise ValueError("token references an unknown search event")
        generated = event_ids != IGNORED
        if not generated.any():
            raise ValueError("each rollout must contain generated tokens")
        advantage = torch.zeros_like(logprobs[index])
        for event, value in enumerate(credit.search_advantages):
            advantage = torch.where(event_ids == event, float(value), advantage)
        advantage = torch.where(
            event_ids == SELECTION, float(credit.selection_advantage), advantage,
        )
        # The importance ratio is defined for generated policy tokens only.
        ratio = (logprobs[index] - old_logprobs[index].detach()).exp()
        surrogate = torch.minimum(
            ratio * advantage,
            ratio.clamp(1 - clip_epsilon, 1 + clip_epsilon) * advantage,
        )
        per_token_loss = -surrogate
        if reference_logprobs is not None and kl_weight:
            log_ratio = reference_logprobs[index].detach() - logprobs[index]
            per_token_loss = per_token_loss + kl_weight * (
                log_ratio.exp() - log_ratio - 1
            )
        losses.append(per_token_loss[generated].mean())
    return torch.stack(losses).mean()
