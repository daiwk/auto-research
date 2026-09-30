"""Post-training objectives from the Sep-30 closure."""

from __future__ import annotations


def rfpo_advantages(critic_values, *, gamma=0.99, gae_lambda=0.95, length_bias=0.0):
    """Frozen-critic reward, debiasing, binarization and GAE."""
    import numpy as np

    values = np.asarray(critic_values, dtype=np.float64)
    if values.ndim != 1 or len(values) < 2:
        raise ValueError("critic values require at least two prefix states")
    debiased = values - length_bias * np.arange(len(values))
    rewards = (debiased[1:] >= 0.5).astype(np.float64)
    deltas = rewards + gamma * debiased[1:] - debiased[:-1]
    advantages = np.zeros_like(deltas)
    running = 0.0
    for index in range(len(deltas) - 1, -1, -1):
        running = deltas[index] + gamma * gae_lambda * running
        advantages[index] = running
    return advantages, {"positive_rewards": int(rewards.sum()), "critic_frozen": True}


def olive_loss(student_logits, teacher_tokens, prefix_lengths):
    """Cross entropy only on teacher continuations sampled after student prefixes."""
    import torch
    import torch.nn.functional as F

    if student_logits.shape[:-1] != teacher_tokens.shape:
        raise ValueError("token and logit shapes do not align")
    positions = torch.arange(teacher_tokens.shape[1], device=teacher_tokens.device)[None]
    mask = positions >= torch.as_tensor(prefix_lengths, device=teacher_tokens.device)[:, None]
    losses = F.cross_entropy(student_logits.transpose(1, 2), teacher_tokens, reduction="none")
    return (losses * mask).sum() / mask.sum().clamp_min(1), mask


def ross_selective_loss(logits, tokens, selected_continuations):
    """Keep full historical context but supervise only selected model continuations."""
    import torch.nn.functional as F

    if logits.shape[:-1] != tokens.shape or tokens.shape != selected_continuations.shape:
        raise ValueError("ROSS tensors must share batch/time axes")
    losses = F.cross_entropy(logits.transpose(1, 2), tokens, reduction="none")
    mask = selected_continuations.to(losses.dtype)
    return (losses * mask).sum() / mask.sum().clamp_min(1)


def reward_aligned_weights(teacher_logp, student_logp, outcome_agreement, *, floor=0.1):
    """R²-OPD reallocates dense supervision by outcome and policy disagreement."""
    import torch

    if teacher_logp.shape != student_logp.shape or outcome_agreement.shape != teacher_logp.shape[:-1]:
        raise ValueError("outcome agreement must align with token distributions")
    disagreement = (teacher_logp.detach().exp() * (teacher_logp.detach() - student_logp.detach())).sum(-1).clamp_min(0)
    raw = outcome_agreement.to(disagreement.dtype).clamp(0, 1) * (1 + disagreement)
    return (raw + floor) / (raw.mean().clamp_min(1e-12) + floor)


def mas_role_advantage(target_role_logp, non_target_logp, response_mask):
    """MAS-OPD role-advantage specialization signal."""
    if target_role_logp.shape != non_target_logp.shape or target_role_logp.shape != response_mask.shape:
        raise ValueError("role signals and response mask must align")
    advantage = (target_role_logp.detach() - non_target_logp.detach()) * response_mask
    return advantage, {"active_tokens": int(response_mask.sum()), "mean_role_advantage": float(advantage.sum() / response_mask.sum().clamp_min(1))}


def mas_privileged_coordination(student_logp, teacher_logp, conflict_mask):
    """Teacher-only conflict attribution yields masked token distillation."""
    import torch.nn.functional as F

    if student_logp.shape != teacher_logp.shape or conflict_mask.shape != student_logp.shape[:-1]:
        raise ValueError("coordination tensors do not align")
    target = teacher_logp.detach().exp()
    kl = F.kl_div(student_logp, target, reduction="none").sum(-1)
    mask = conflict_mask.to(kl.dtype)
    return (kl * mask).sum() / mask.sum().clamp_min(1)
