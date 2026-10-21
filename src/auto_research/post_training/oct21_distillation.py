"""AP-OPD block pullback and OPTD's detached predictive-weight update.

These are defining loss components, not full language-model reproductions.
Equations follow arXiv:2610.28194v1 §2/4 and 2610.28048v1 App. B/C.3.
"""
from __future__ import annotations

import math

import torch
from torch import Tensor


def _mask(values: Tensor, mask: Tensor) -> None:
    if values.ndim != 2 or min(values.shape) < 1 or not values.is_floating_point():
        raise ValueError("nonempty floating [batch,token] values required")
    if mask.shape != values.shape or mask.dtype != torch.bool or mask.device != values.device:
        raise ValueError("aligned Boolean mask on the same device required")
    if not bool(mask.any(1).all()) or not bool(torch.isfinite(values[mask]).all()):
        raise ValueError("each response requires finite active tokens")


def adaptive_pullback_weights(log_ratio: Tensor, response_mask: Tensor, *, block_size: int = 64,
                              detector: str = "z", z: float = 2., alpha: float = .05) -> tuple[Tensor, dict]:
    """Compute weights from the ORIGINAL, unweighted positive-ratio profile.

    All signed coefficients in a selected post-jump block share one weight.
    Active positions are partitioned per response (padding never forms a block).
    The z threshold is not a calibrated p-value for correlated language tokens.
    """
    _mask(log_ratio, response_mask)
    if isinstance(block_size, bool) or not isinstance(block_size, int) or block_size < 1:
        raise ValueError("positive integer block size required")
    if detector not in {"z", "top-alpha"} or not math.isfinite(z) or z < 0 or not math.isfinite(alpha) or not 0 <= alpha <= 1:
        raise ValueError("valid detector, finite nonnegative z and alpha in [0,1] required")
    # Convert only the statistics, not the differentiable policy input.
    ratio = log_ratio.detach().float() if log_ratio.dtype in (torch.float16, torch.bfloat16) else log_ratio.detach()
    weights = torch.ones_like(ratio)
    profiles, selected_boundaries = [], []
    for row in range(len(ratio)):
        indices = response_mask[row].nonzero(as_tuple=False).flatten()
        blocks = list(indices.split(block_size))
        penalties = [ratio[row, ids].clamp_min(0) for ids in blocks]
        means = torch.stack([v.mean() for v in penalties])
        changes = means[1:] - means[:-1]
        selected: list[int] = []
        if detector == "z":
            for i, change in enumerate(changes):
                if len(blocks[i]) < 2 or len(blocks[i + 1]) < 2:
                    continue
                se = (penalties[i].var(correction=1) / len(blocks[i])
                      + penalties[i + 1].var(correction=1) / len(blocks[i + 1])).sqrt()
                if bool(change > z * se):
                    selected.append(i)
        else:
            count = min(math.ceil(alpha * len(changes)), int((changes > 0).sum()))
            # Stable sorting makes tied rises deterministic; retain positive only.
            selected = [int(i) for i in torch.argsort(changes, descending=True, stable=True)[:count]]
        for i in selected:
            weights[row, blocks[i + 1]] = means[i] / means[i + 1]
        profiles.append(means.tolist())
        selected_boundaries.append(selected)
    return weights.detach(), {"original_block_mean_penalties": profiles,
                               "selected_boundaries": selected_boundaries,
                               "weights_detached": True, "profile_is_unweighted": True}


def adaptive_pullback_loss(student_log_probs: Tensor, teacher_log_probs: Tensor, response_mask: Tensor,
                           **options) -> tuple[Tensor, dict]:
    """AP-OPD Eq. 2: token-mean w * sg(log pS - log pT) * log pS.

    Inputs score exactly the same student-sampled token and prefix. This
    operator cannot verify that an upstream caller actually sampled on-policy.
    """
    _mask(student_log_probs, response_mask)
    if teacher_log_probs.shape != student_log_probs.shape or teacher_log_probs.device != student_log_probs.device or teacher_log_probs.dtype != student_log_probs.dtype:
        raise ValueError("aligned student/teacher dtype, device and shape required")
    _mask(teacher_log_probs, response_mask)
    safe_student = torch.where(response_mask, student_log_probs, 0.)
    safe_teacher = torch.where(response_mask, teacher_log_probs.detach(), 0.)
    ratio = (safe_student - safe_teacher).detach()
    weights, audit = adaptive_pullback_weights(ratio, response_mask, **options)
    loss = (weights * ratio * safe_student).sum() / response_mask.sum()
    return loss, {**audit, "weights": weights, "log_ratio": ratio}


def transition_distillation_loss(student_logits: Tensor, teacher_logits: Tensor, response_mask: Tensor,
                                 *, top_k: int = 16, transition_tail: int = 2000,
                                 transition_weight: float | None = None) -> tuple[Tensor, dict]:
    """OPTD App. B practical update, NOT reverse transition KL or hidden MSE.

    [batch,depth,token,vocab] readouts must use each model's final normalization
    and shared unembedding head, ordered shallow to final. Candidate IDs come
    from the student's FINAL layer and stay fixed across the whole path.
    Default scaling sums transitions (C.3), i.e. M * their mean (Eq. 12).
    """
    if student_logits.ndim != 4 or min(student_logits.shape) < 1 or student_logits.shape[1] < 2 or not student_logits.is_floating_point():
        raise ValueError("nonempty floating [batch,depth>=2,token,vocab] logits required")
    if teacher_logits.shape != student_logits.shape or teacher_logits.dtype != student_logits.dtype or teacher_logits.device != student_logits.device:
        raise ValueError("aligned teacher/student readouts required")
    _mask(student_logits[:, -1, :, 0], response_mask)
    active = response_mask[:, None, :, None].expand_as(student_logits)
    if not bool(torch.isfinite(student_logits[active]).all()) or not bool(torch.isfinite(teacher_logits[active]).all()):
        raise ValueError("finite active path logits required")
    if isinstance(top_k, bool) or not isinstance(top_k, int) or not 1 <= top_k <= student_logits.shape[-1]:
        raise ValueError("top_k must be an integer within vocabulary size")
    if isinstance(transition_tail, bool) or not isinstance(transition_tail, int) or transition_tail < 1:
        raise ValueError("positive transition tail required")
    count = student_logits.shape[1] - 1
    scale = count if transition_weight is None else transition_weight
    if not math.isfinite(scale) or scale < 0:
        raise ValueError("finite nonnegative transition weight required")
    if student_logits.dtype in (torch.float16, torch.bfloat16):
        student_logits, teacher_logits = student_logits.float(), teacher_logits.float()
    student = torch.where(active, student_logits, 0.).log_softmax(-1)
    teacher = torch.where(active, teacher_logits.detach(), 0.).log_softmax(-1)
    ids = student[:, -1].detach().topk(top_k, dim=-1).indices
    path_ids = ids[:, None].expand(-1, student.shape[1], -1, -1)
    path_s, path_t = student.gather(-1, path_ids), teacher.gather(-1, path_ids)
    final_coefficient = (path_s[:, -1].detach().softmax(-1)
                         * (path_s[:, -1].detach() - path_t[:, -1])).detach()
    final_per_token = (final_coefficient * path_s[:, -1]).sum(-1)
    final_loss = torch.where(response_mask, final_per_token, 0.).sum() / response_mask.sum()
    delta_s, delta_t = path_s[:, 1:] - path_s[:, :-1], path_t[:, 1:] - path_t[:, :-1]
    coefficient = (path_s[:, 1:].detach().softmax(-1) * (delta_s.detach() - delta_t)).detach()
    transition_per_token = (coefficient * delta_s).sum(-1)
    tail_mask = response_mask & (response_mask.flip(1).cumsum(1).flip(1) <= transition_tail)
    transition_mean = torch.where(tail_mask[:, None], transition_per_token, 0.).sum() / (tail_mask.sum() * count)
    total = final_loss + scale * transition_mean
    return total, {"final_loss": final_loss.detach(), "transition_mean_loss": transition_mean.detach(),
                   "transition_scale": scale, "candidate_ids": ids, "transition_mask": tail_mask,
                   "transition_coefficients": coefficient, "student_delta": delta_s,
                   "teacher_detached": True, "destination_predictive_weights": True}
