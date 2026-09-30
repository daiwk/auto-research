"""Executable L1 objectives from the 2026-09-29 post-training follow-up."""

from __future__ import annotations


def oasis_select_scaffold(rollouts):
    """Choose the shortest verified rollout and a distinct same-problem context."""
    verified = [item for item in rollouts if item["verified"]]
    if not verified:
        return None
    scaffold = min(verified, key=lambda item: (len(item["tokens"]), item["id"]))
    alternatives = [item for item in rollouts if item["id"] != scaffold["id"]]
    if not alternatives:
        raise ValueError("OASIS requires a distinct same-problem context")
    unverified = [item for item in alternatives if not item["verified"]]
    context = min(unverified or alternatives, key=lambda item: item["id"])
    return scaffold, context


def oasis_forward_kl(student_log_prob, teacher_prob, token_mask, *, entry_clip: float = 5.0):
    """OASIS keeps the clipped OPSD forward-KL but masks to a verified scaffold."""
    if not (student_log_prob.shape == teacher_prob.shape):
        raise ValueError("student and teacher distributions must match")
    if token_mask.shape != student_log_prob.shape[:-1]:
        raise ValueError("token mask must match batch/time axes")
    contribution = teacher_prob * (teacher_prob.clamp_min(1e-12).log() - student_log_prob)
    mask = token_mask.to(contribution.dtype)[..., None]
    return contribution.clamp(max=entry_clip).mul(mask).sum() / mask.sum().clamp_min(1)


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


def ride_target(base_hidden, teacher_hidden, *, extrapolation: float = 1.5):
    """RIDE: extrapolate the RL-induced representation residual beyond teacher."""
    if base_hidden.shape != teacher_hidden.shape or extrapolation < 1:
        raise ValueError("hidden states must match and extrapolation must be >= 1")
    return base_hidden.detach() + extrapolation * (teacher_hidden.detach() - base_hidden.detach())


def ride_loss(student_hidden, base_hidden, teacher_hidden, *, extrapolation: float = 1.5, token_mask=None):
    import torch

    target = ride_target(base_hidden, teacher_hidden, extrapolation=extrapolation)
    squared = (student_hidden - target).square().mean(-1)
    if token_mask is None:
        return squared.mean()
    mask = token_mask.to(squared.dtype)
    return (squared * mask).sum() / mask.sum().clamp_min(1)


def pr_opd_alignment(student_layers, privileged_layers, response_mask, *, layer_weights=None):
    """PR-OPD hidden-state alignment to a stop-gradient skill-conditioned teacher."""
    import torch

    if len(student_layers) != len(privileged_layers) or not student_layers:
        raise ValueError("student and privileged layer lists must align")
    weights = torch.ones(len(student_layers), device=student_layers[0].device) if layer_weights is None else torch.as_tensor(layer_weights, device=student_layers[0].device)
    weights = weights / weights.sum()
    mask = response_mask.to(student_layers[0].dtype)
    losses = []
    for student, teacher in zip(student_layers, privileged_layers):
        if student.shape != teacher.shape or student.shape[:-1] != response_mask.shape:
            raise ValueError("layer and response-mask shapes do not align")
        cosine = torch.nn.functional.cosine_similarity(student, teacher.detach(), dim=-1)
        losses.append(((1 - cosine) * mask).sum() / mask.sum().clamp_min(1))
    return sum(weight * loss for weight, loss in zip(weights, losses))
