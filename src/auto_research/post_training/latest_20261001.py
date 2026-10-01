"""Post-training objectives from the Oct-1 intake batch."""

from __future__ import annotations


def advisd_contrast(logp_with_advice, logp_without_advice):
    """Mean paired response contrast from AdviSD Eq. 3."""
    import torch

    if logp_with_advice.shape != logp_without_advice.shape:
        raise ValueError("paired scoring tensors must align")
    return (logp_with_advice - logp_without_advice).mean(-1)


def advisd_gate(contrasts, donor_contrasts, abstentions, *, quantile: float):
    """Keep abstentions and issued advice above the donor-calibrated gate."""
    import torch

    if not 0 < quantile < 1 or contrasts.shape != abstentions.shape:
        raise ValueError("invalid AdviSD gate inputs")
    threshold = torch.quantile(donor_contrasts.abs(), quantile)
    selected = abstentions.bool() | (contrasts.abs() > threshold)
    return selected, threshold


def gats_schedule(teacher_scores, student_history, *, window: int, withdrawn: bool = False):
    """One-step-lagged GATS weight and permanent teacher withdrawal."""
    import numpy as np

    if window < 1 or len(teacher_scores) < window or not student_history:
        raise ValueError("GATS requires teacher tail and prior student measurements")
    teacher_ref = float(np.mean(teacher_scores[-window:]))
    student_ref = float(np.mean(student_history[-window:]))
    if teacher_ref <= 0:
        raise ValueError("teacher reference must be positive")
    withdrawn = bool(withdrawn or student_ref >= teacher_ref)
    weight = 0.0 if withdrawn else max(1.0 - student_ref / teacher_ref, 0.0)
    return weight, withdrawn, {"teacher_reference": teacher_ref, "student_reference": student_ref}


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


def interpolated_policy(student_prob, teacher_prob, gamma: float):
    """IPD token policy m_gamma=(1-gamma)pi_student+gamma*pi_teacher."""
    if student_prob.shape != teacher_prob.shape or not 0 <= gamma <= 1:
        raise ValueError("invalid interpolated-policy inputs")
    return (1 - gamma) * student_prob + gamma * teacher_prob


def flowmap_separated_loss(sampled_states, student_kernel, teacher_kernel):
    """FlowMap-OPD: rollout states are detached from the comparison kernel."""
    import torch
    import torch.nn.functional as F

    states = sampled_states.detach()
    student_logp = torch.log_softmax(student_kernel(states), dim=-1)
    with torch.no_grad():
        teacher_prob = torch.softmax(teacher_kernel(states), dim=-1)
    return F.kl_div(student_logp, teacher_prob, reduction="batchmean"), states
