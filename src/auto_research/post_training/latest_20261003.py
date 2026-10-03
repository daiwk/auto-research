"""Post-training mechanisms selected from the 2026-10-03 intake."""

from __future__ import annotations


def carm_response_mask(current_log_probs, rollout_log_probs, *, threshold: float):
    """Cancellation-aware sequence gate using mean absolute log ratio."""
    import torch

    drift = (current_log_probs - rollout_log_probs).abs().mean(-1)
    return torch.exp(drift) <= threshold, drift


def group_mass_cap(importance_ratios, *, mass_cap: float):
    """Cap total importance mass per rollout group and renormalize."""
    import torch

    if mass_cap <= 0:
        raise ValueError("mass_cap must be positive")
    ratios = importance_ratios.clamp_min(0)
    scale = torch.minimum(torch.ones_like(ratios.sum(-1)), mass_cap / ratios.sum(-1).clamp_min(1e-12))
    return ratios * scale.unsqueeze(-1)


def gradient_aligned_rejected_weights(rejected_gradients, preferred_direction):
    """Down-weight rejected tokens whose update conflicts with preferred behavior."""
    import torch.nn.functional as F

    alignment = F.cosine_similarity(rejected_gradients, preferred_direction.unsqueeze(0), dim=-1)
    return (1 - alignment.clamp(min=0, max=1)).detach()


def sharpo_segment_advantages(base_advantage, teacher_log_probs, student_log_probs, segments):
    """Apply a bounded teacher-student multiplier to each interaction segment."""
    import torch

    result = torch.empty_like(student_log_probs)
    for start, end in segments:
        gap = (teacher_log_probs[start:end] - student_log_probs[start:end]).mean().detach()
        result[start:end] = base_advantage * (2 * torch.sigmoid(gap))
    return result


def token_level_video_credit(reward_gradient, *, group_advantage: float):
    """Normalize frozen-VLM gradient magnitudes into dense TVRL credit."""
    import torch

    credit = reward_gradient.norm(dim=-1)
    credit = credit / credit.mean(dim=-1, keepdim=True).clamp_min(1e-12)
    return credit.detach() * group_advantage


def sharpening_tax(base_success, post_success, *, samples: int):
    """Measure coverage lost after post-training at a fixed sampling budget."""
    import torch

    base_coverage = 1 - (1 - base_success).pow(samples)
    post_coverage = 1 - (1 - post_success).pow(samples)
    return base_coverage - post_coverage


def lego_opd_teacher(language_logits, grounded_logits, *, grounding_strength: float):
    """Compose a language prior with a grounding likelihood factor."""
    import torch

    language_prior = torch.softmax(language_logits.detach(), dim=-1)
    visual_likelihood = torch.softmax(grounded_logits.detach(), dim=-1)
    composed = language_prior * visual_likelihood.pow(grounding_strength)
    return composed / composed.sum(dim=-1, keepdim=True).clamp_min(1e-12)


def drift_opd_loss(student_logits, one_step_teacher_logits, future_potential, *, potential_weight: float):
    """One-step reverse-KL plus the offline future-potential correction."""
    import torch.nn.functional as F

    student_log = F.log_softmax(student_logits, dim=-1)
    student = student_log.exp()
    teacher_log = F.log_softmax(one_step_teacher_logits.detach(), dim=-1)
    reverse_kl = (student * (student_log - teacher_log)).sum(-1).mean()
    return reverse_kl - potential_weight * future_potential.mean()
