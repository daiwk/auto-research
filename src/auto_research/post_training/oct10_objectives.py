"""Token/rollout operators from the October 8 OPD/RL papers.

These operators accept actual rollout statistics. Tensor-only invocations are
mechanism diagnostics, not evidence of mathematical reasoning improvement.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


def _mask_mean(values, mask):
    if values.shape != mask.shape or not bool(mask.any()):
        raise ValueError("a shape-aligned nonempty token mask is required")
    return values.masked_select(mask.bool()).mean()


def dial_opd_scores(student_logp, teacher_logp, beta=0.5):
    """Eq.4; stable logarithmic mean, including equal-probability limit."""
    import torch

    if beta < 0 or not math.isfinite(beta) or student_logp.shape != teacher_logp.shape:
        raise ValueError("invalid beta or incompatible log probabilities")
    if not bool(torch.isfinite(student_logp).all() and torch.isfinite(teacher_logp).all()):
        raise ValueError("log probabilities must be finite")
    p, q = student_logp.detach(), teacher_logp.detach()
    gap = (q - p).abs()
    high, low = torch.maximum(p, q), torch.minimum(p, q)
    # L(p,q)=exp(high)*(1-exp(low-high))/abs(log q-log p).
    ratio = -torch.expm1(low - high) / gap.clamp_min(1e-12)
    mean = high.exp() * torch.where(gap > 1e-7, ratio, torch.ones_like(ratio))
    return mean.pow(beta) * gap


def dial_opd_loss(student_logp, teacher_logp, mask, *, beta=0.5, retention=0.4):
    import torch

    if student_logp.ndim != 2 or mask.shape != student_logp.shape or not 0 < retention <= 1:
        raise ValueError("expected [response, token] arrays and retention in (0,1]")
    scores = dial_opd_scores(student_logp, teacher_logp, beta)
    selected = torch.zeros_like(mask, dtype=torch.bool)
    for row in range(mask.shape[0]):
        positions = torch.where(mask[row].bool())[0]
        if positions.numel():
            count = max(1, round(retention * positions.numel()))
            indices = scores[row, positions].argsort(descending=True, stable=True)[:count]
            selected[row, positions[indices]] = True
    reward = (teacher_logp - student_logp).detach()
    return _mask_mean(-reward * student_logp, selected), selected


def meta_opd_descriptor(student_logits, teacher_logits, actions):
    """Detached 74-dimensional descriptor, Table 4, shared window position."""
    import torch

    if student_logits.shape != teacher_logits.shape or student_logits.shape[-1] < 32:
        raise ValueError("aligned vocabularies with at least 32 entries are required")
    if actions.shape != student_logits.shape[:-1] or actions.ndim != 2:
        raise ValueError("expected [batch, window, vocabulary] statistics")
    s = student_logits.detach().float().log_softmax(-1)
    t = teacher_logits.detach().float().log_softmax(-1)
    sp, tp = s.exp(), t.exp()
    sampled_s = s.gather(-1, actions[..., None]).squeeze(-1)
    sampled_t = t.gather(-1, actions[..., None]).squeeze(-1)
    sv, si = s.topk(32, dim=-1)
    tv, ti = t.topk(32, dim=-1)
    overlap = (si[..., :, None] == ti[..., None, :]).any(-1).float().mean(-1)
    width = actions.shape[1]
    position = torch.arange(width, device=s.device, dtype=s.dtype) / max(1, width - 1)
    position = position.expand_as(sampled_s)
    scalars = torch.stack((sampled_s, sampled_t, sampled_t - sampled_s,
                          -(sp * s).sum(-1) / math.log(s.shape[-1]),
                          -(tp * t).sum(-1) / math.log(t.shape[-1]),
                          sv[..., 0].exp(), tv[..., 0].exp(),
                          (si[..., 0] == ti[..., 0]).float(), position, overlap), -1)
    return torch.cat((scalars, sv, tv), -1).detach()


def meta_opd_weights(scores, mask, rho=0.25):
    if not 0 < rho < 1 or scores.shape != mask.shape:
        raise ValueError("invalid residual scale or mask shape")
    count = mask.sum(-1, keepdim=True).clamp_min(1)
    centered = scores - (scores * mask).sum(-1, keepdim=True) / count
    raw = (1 + rho * centered.tanh()) * mask
    return raw * count / raw.sum(-1, keepdim=True).clamp_min(1e-8)


def clipped_opd_loss(current_logp, old_logp, teacher_logp, mask, weights, clip=0.2):
    import torch

    if not 0 < clip < 1:
        raise ValueError("clip must be in (0,1)")
    advantage = (teacher_logp - old_logp).detach()
    ratio = (current_logp - old_logp.detach()).exp()
    token_loss = torch.maximum(-advantage * ratio, -advantage * ratio.clamp(1 - clip, 1 + clip))
    return _mask_mean(weights * token_loss, mask)


def virtual_adamw(model, optimizer, loss, *, max_grad_norm=1.0):
    """Differentiable one-step AdamW, without mutating real state (Eq.6/23)."""
    import torch

    if not isinstance(optimizer, torch.optim.AdamW):
        raise ValueError("MetaOPD requires AdamW state")
    named = {name: p for name, p in model.named_parameters() if p.requires_grad}
    gradients = torch.autograd.grad(loss, tuple(named.values()), create_graph=True)
    norm = torch.stack([g.square().sum() for g in gradients]).sum().sqrt()
    scale = (max_grad_norm / (norm + 1e-6)).clamp(max=1.0) if max_grad_norm else 1.0
    settings = {id(p): group for group in optimizer.param_groups for p in group["params"]}
    result = dict(model.named_parameters())
    for (name, parameter), gradient in zip(named.items(), gradients):
        group, state = settings[id(parameter)], optimizer.state.get(parameter, {})
        if group.get("amsgrad", False) or group.get("maximize", False):
            raise ValueError("AMSGrad/maximize are outside this AdamW implementation")
        beta1, beta2 = group["betas"]
        step = int(state.get("step", 0)) + 1
        g = gradient * scale
        m = beta1 * state.get("exp_avg", torch.zeros_like(parameter)).detach() + (1 - beta1) * g
        v = beta2 * state.get("exp_avg_sq", torch.zeros_like(parameter)).detach() + (1 - beta2) * g.square()
        mhat, vhat = m / (1 - beta1**step), v / (1 - beta2**step)
        # torch sqrt has an undefined derivative at exactly zero. The selected
        # zero branch implements the continuous composite AdamW limit.
        root = torch.where(vhat > 0, vhat.clamp_min(1e-30).sqrt(), torch.zeros_like(vhat))
        result[name] = parameter * (1 - group["lr"] * group["weight_decay"]) - group["lr"] * mhat / (root + group["eps"])
    return result


def meta_opd_step(model, weight_network, optimizer, meta_optimizer, *,
                  logits_fn, reference_loss_fn, teacher_logits, actions, old_logp, mask,
                  regularization=0.01, max_grad_norm=1.0):
    """Algorithm 1: virtual step -> meta update -> fresh weights -> real step.

    logits_fn(parameters_or_None) must evaluate the *same* sampled trajectories.
    reference_loss_fn(parameters) teacher-forces only training references.
    Callers own split isolation; neither callback receives benchmark test data.
    """
    import torch

    if not bool(mask.any()):
        raise ValueError("empty optimizer minibatch")
    logits = logits_fn(None)
    descriptor = meta_opd_descriptor(logits, teacher_logits, actions)
    teacher_lp = teacher_logits.log_softmax(-1).gather(-1, actions[..., None]).squeeze(-1)
    lp = logits.log_softmax(-1).gather(-1, actions[..., None]).squeeze(-1)
    weights = meta_opd_weights(weight_network(descriptor).squeeze(-1), mask)
    inner = clipped_opd_loss(lp, old_logp, teacher_lp, mask, weights)
    virtual = virtual_adamw(model, optimizer, inner, max_grad_norm=max_grad_norm)
    outer = reference_loss_fn(virtual) + regularization * _mask_mean((weights - 1).square(), mask)
    meta_optimizer.zero_grad(set_to_none=True)
    meta_grads = torch.autograd.grad(outer, tuple(weight_network.parameters()))
    for parameter, gradient in zip(weight_network.parameters(), meta_grads):
        parameter.grad = gradient
    meta_optimizer.step()
    fresh_weights = meta_opd_weights(weight_network(descriptor).squeeze(-1), mask).detach()
    current = logits_fn(None).log_softmax(-1).gather(-1, actions[..., None]).squeeze(-1)
    real_loss = clipped_opd_loss(current, old_logp, teacher_lp, mask, fresh_weights)
    optimizer.zero_grad(set_to_none=True)
    real_loss.backward()
    if max_grad_norm:
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
    optimizer.step()
    return {"inner_loss": float(real_loss.detach()), "outer_loss": float(outer.detach()),
            "weight_std": float(fresh_weights[mask.bool()].std(unbiased=False))}


def residual_advantage(student_logits, teacher_logits, actions, mask, verifier_advantage,
                       guidance_weight=1.0):
    """Full-vocabulary RA: state baseline and response centering, Eq.1–3."""
    p, q = student_logits.detach().softmax(-1), teacher_logits.detach().softmax(-1)
    if p.shape != q.shape or actions.shape != p.shape[:-1] or mask.shape != actions.shape:
        raise ValueError("unaligned RA statistics")
    residual = q - p
    local = residual.gather(-1, actions[..., None]).squeeze(-1) - (p * residual).sum(-1)
    mean = (local * mask).sum(-1, keepdim=True) / mask.sum(-1, keepdim=True).clamp_min(1)
    return (verifier_advantage[..., None] + guidance_weight * (local - mean)) * mask


def clipped_actor_loss(current_logp, old_logp, advantages, mask, clip=0.2):
    """Token-mean PPO surrogate; labels fixed at the rollout policy."""
    import torch

    if current_logp.shape != old_logp.shape or mask.shape != current_logp.shape:
        raise ValueError("unaligned actor statistics")
    if advantages.shape != current_logp.shape or not 0 < clip < 1:
        raise ValueError("one fixed advantage per token and clip in (0,1) required")
    ratio = (current_logp - old_logp.detach()).exp()
    label = advantages.detach()
    return _mask_mean(torch.maximum(-ratio * label,
                                   -ratio.clamp(1 - clip, 1 + clip) * label), mask)


def co_ra_step(student, teacher, student_optimizer, teacher_optimizer, *,
               student_logits_fn, teacher_logits_fn, actions, mask,
               verifier_advantage, guidance_weight=10.0, clip=0.2):
    """B.8 score-then-update cycle, teacher adapter used next iteration.

    teacher must expose only a LoRA adapter as trainable parameters; its frozen
    base must not be included in teacher_optimizer. This function cannot inspect
    an external verifier; it consumes its fixed response-level labels.
    """
    import torch

    trainable = [p for p in teacher.parameters() if p.requires_grad]
    frozen = [p for p in teacher.parameters() if not p.requires_grad]
    optimized = [p for group in teacher_optimizer.param_groups for p in group["params"]]
    if not trainable or not frozen or {id(p) for p in trainable} != {id(p) for p in optimized}:
        raise ValueError("teacher optimizer must update only its trainable adapter")
    with torch.no_grad():
        old_student = student_logits_fn()
        old_teacher = teacher_logits_fn()
        student_old_lp = old_student.log_softmax(-1).gather(-1, actions[..., None]).squeeze(-1)
        teacher_old_lp = old_teacher.log_softmax(-1).gather(-1, actions[..., None]).squeeze(-1)
        labels = residual_advantage(old_student, old_teacher, actions, mask,
                                    verifier_advantage, guidance_weight)
    student_optimizer.zero_grad(set_to_none=True)
    student_lp = student_logits_fn().log_softmax(-1).gather(-1, actions[..., None]).squeeze(-1)
    student_loss = clipped_actor_loss(student_lp, student_old_lp, labels, mask, clip)
    student_loss.backward()
    torch.nn.utils.clip_grad_norm_(student.parameters(), 1.0)
    student_optimizer.step()
    # Old teacher likelihoods and labels above are retained, not rescored after
    # the student update. This is the same scored student batch.
    teacher_optimizer.zero_grad(set_to_none=True)
    teacher_lp = teacher_logits_fn().log_softmax(-1).gather(-1, actions[..., None]).squeeze(-1)
    teacher_labels = verifier_advantage[..., None].expand_as(teacher_lp)
    teacher_loss = clipped_actor_loss(teacher_lp, teacher_old_lp, teacher_labels, mask, clip)
    teacher_loss.backward()
    torch.nn.utils.clip_grad_norm_(trainable, 1.0)
    teacher_optimizer.step()
    return {"student_loss": float(student_loss.detach()),
            "teacher_loss": float(teacher_loss.detach()),
            "guidance_mean_error": float(((labels * mask).sum(-1) / mask.sum(-1)
                                           - verifier_advantage).abs().max())}


@dataclass(frozen=True)
class SemiOPDCache:
    """Frozen pi_0 samples and teacher scores; never refreshed by train steps."""

    initial_student_revision: str
    teacher_revision: str
    tokenizer_revision: str
    dataset_revision: str
    token_ids: tuple[tuple[int, ...], ...]
    response_masks: tuple[tuple[bool, ...], ...]
    teacher_logp: tuple[tuple[float, ...], ...]

    def __post_init__(self):
        if not all((self.initial_student_revision, self.teacher_revision,
                    self.tokenizer_revision, self.dataset_revision)):
            raise ValueError("all cache sources require immutable revisions")
        if not self.token_ids or not (len(self.token_ids) == len(self.response_masks)
                                     == len(self.teacher_logp)):
            raise ValueError("empty or misaligned cached trajectories")
        for ids, mask, scores in zip(self.token_ids, self.response_masks, self.teacher_logp):
            if len(ids) - 1 != len(mask) or len(mask) != len(scores) or not any(mask):
                raise ValueError("scores/masks align with next-token targets, including full responses")
            if not all(math.isfinite(v) and v <= 0 for v in scores):
                raise ValueError("teacher log probabilities must be finite and nonpositive")


def semi_opd_loss(current_logp, cached_teacher_logp, mask):
    """Eq.3: fixed responses, but recompute advantage from current student."""
    if current_logp.shape != cached_teacher_logp.shape:
        raise ValueError("cache and current student must share token positions")
    advantage = (cached_teacher_logp.detach() - current_logp).detach()
    return _mask_mean(-advantage * current_logp, mask)


def topk_overlap(student_logits, teacher_logits, mask, k=64):
    """Token-weighted initial-student/teacher support overlap, not a cutoff rule."""
    if student_logits.shape != teacher_logits.shape or not 0 < k <= student_logits.shape[-1]:
        raise ValueError("aligned vocabulary and valid k required")
    student = student_logits.detach().topk(k, dim=-1).indices
    teacher = teacher_logits.detach().topk(k, dim=-1).indices
    overlap = (student[..., :, None] == teacher[..., None, :]).any(-1).float().mean(-1)
    return _mask_mean(overlap, mask)


def grpo_dropout(old_token_logp, mask, advantages):
    """Greedy Eq.4 -> restore nonpositives Eq.7 -> weighted center Eq.9."""
    import torch

    if old_token_logp.ndim != 2 or mask.shape != old_token_logp.shape:
        raise ValueError("one prompt's [rollout, token] log probabilities required")
    if advantages.shape != (mask.shape[0],) or bool((mask.sum(-1) == 0).any()):
        raise ValueError("one advantage per nonempty rollout is required")
    surprisal = -(old_token_logp.detach() * mask).sum(-1) / mask.sum(-1)
    contributions = advantages.detach() * (surprisal - surprisal.mean()) / len(advantages)
    retained = torch.ones_like(advantages, dtype=torch.bool)
    total = contributions.sum()
    for index in contributions.argsort(stable=True):
        if total >= 0 or contributions[index] >= 0:
            break
        retained[index] = False
        total = total - contributions[index]
    retained |= advantages <= 0
    if not bool(retained.any()):
        raise ValueError("filter unexpectedly removed every rollout")
    probability = (-surprisal[retained]).softmax(0)
    baseline = (probability * advantages[retained]).sum()
    centered = torch.where(retained, advantages - baseline, torch.zeros_like(advantages))
    return retained, centered.detach()
