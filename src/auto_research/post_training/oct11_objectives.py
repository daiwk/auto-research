"""October 8 post-training objectives, with frozen rollout labels.

Pure tensor calls are L0/L1 evidence only. Public checkpoint runners must supply
student rollouts, a verifier, and split-isolated training/evaluation data.
"""
from __future__ import annotations

import math
from dataclasses import dataclass


def conditional_kl(student_logits, reference_logits):
    """Full-vocabulary KL(student || reference), not sampled-token k1."""
    if student_logits.shape != reference_logits.shape:
        raise ValueError("aligned full-vocabulary distributions required")
    p = student_logits.detach().float().log_softmax(-1)
    q = reference_logits.detach().float().log_softmax(-1)
    return (p.exp() * (p - q)).sum(-1)


def zcpo_coefficients(rewards, conditional_kls, mask, beta=0.02):
    """Eq. 4: one prompt group; skip equal-reward groups before dividing."""
    import torch

    if rewards.ndim != 1 or mask.ndim != 2 or mask.shape[0] != rewards.numel():
        raise ValueError("expected G rewards and G x T response mask")
    if beta < 0 or not math.isfinite(beta) or not bool(torch.isfinite(rewards).all()):
        raise ValueError("finite rewards and nonnegative beta required")
    a = rewards.detach().float() - rewards.detach().float().mean()
    scale = a.abs().max()
    if rewards.numel() < 2 or float(scale) == 0:
        return torch.zeros_like(a), False
    if conditional_kls.shape != mask.shape or not bool(mask.bool().any(-1).all()):
        raise ValueError("every active response needs aligned nonempty KL statistics")
    if not bool(torch.isfinite(conditional_kls[mask.bool()]).all()):
        raise ValueError("nonfinite active conditional KL")
    # masked_fill, rather than multiplication, also rejects padding NaN leakage.
    d = conditional_kls.detach().masked_fill(~mask.bool(), 0).sum(-1) / mask.sum(-1)
    c = a / scale - beta * (d - d.mean())
    return c.detach(), True


def zcpo_loss(current_logp, old_logp, student_logits, reference_logits, rewards, mask,
              *, beta=0.02, clip_low=0.2, clip_high=0.28):
    """DAPO token-mean surrogate with joint coefficients and no separate KL loss."""
    import torch

    if current_logp.shape != old_logp.shape or current_logp.shape != mask.shape:
        raise ValueError("aligned sampled log probabilities required")
    if not 0 <= clip_low < 1 or clip_high < 0:
        raise ValueError("invalid clipping bounds")
    a = rewards.detach().float() - rewards.detach().float().mean()
    if rewards.numel() < 2 or float(a.abs().max()) == 0:
        # Do not even evaluate the reference distribution on inactive groups.
        return current_logp.masked_fill(~mask.bool(), 0).sum() * 0, {
            "active": False, "coefficient_sum": 0.0,
        }
    c, _ = zcpo_coefficients(rewards, conditional_kl(student_logits, reference_logits), mask, beta)
    ratio = (current_logp - old_logp.detach()).exp()
    loss = torch.maximum(-c[:, None] * ratio,
                         -c[:, None] * ratio.clamp(1 - clip_low, 1 + clip_high))
    return loss[mask.bool()].mean(), {
        "active": True, "coefficient_sum": float(c.sum()),
        "coefficient_min": float(c.min()), "coefficient_max": float(c.max()),
    }


def pivot_routing(teacher_sample_logp, mask, *, step, total_steps):
    """Eqs. 6-11: average response PPL, minibatch z-score, cosine rank routing."""
    import torch

    if teacher_sample_logp.ndim != 3 or teacher_sample_logp.shape != mask.shape:
        raise ValueError("expected B x G x T teacher sampled-token log probabilities")
    if total_steps < 1 or not 0 <= step <= total_steps or not bool(mask.bool().any(-1).all()):
        raise ValueError("valid schedule and nonempty responses required")
    logp = teacher_sample_logp.detach().float().masked_fill(~mask.bool(), 0)
    ppl = (-(logp.sum(-1) / mask.sum(-1))).exp().mean(-1)
    if not bool(torch.isfinite(ppl).all()):
        raise ValueError("nonfinite teacher perplexity")
    z = (ppl - ppl.mean()) / (ppl.std(unbiased=False) + 1e-8)
    fraction = .5 * (1 - math.cos(math.pi * step / total_steps))
    count = min(len(z), int(math.floor(fraction * len(z) + 1e-10)))
    routed = torch.zeros_like(z, dtype=torch.bool)
    routed[z.argsort(stable=True)[:count]] = True
    return routed, z, fraction


def pivot_loss(student_logits, teacher_logits, actions, old_logp, rewards, mask,
               *, step, total_steps, clip=0.2):
    """Forward-KL OPD and per-response-token-sum GRPO, averaged over G and B."""
    import torch

    if student_logits.shape != teacher_logits.shape or student_logits.ndim != 4:
        raise ValueError("expected aligned B x G x T x V logits")
    if actions.shape != mask.shape or mask.shape != student_logits.shape[:-1]:
        raise ValueError("unaligned response actions/masks")
    if old_logp.shape != mask.shape or rewards.shape != mask.shape[:2] or not 0 < clip < 1:
        raise ValueError("unaligned rollout scores/rewards or clip")
    s, t = student_logits.float().log_softmax(-1), teacher_logits.detach().float().log_softmax(-1)
    sampled_t = t.gather(-1, actions[..., None]).squeeze(-1)
    routed, scores, fraction = pivot_routing(sampled_t, mask, step=step, total_steps=total_steps)
    forward_kl = (t.exp() * (t - s)).sum(-1).masked_fill(~mask.bool(), 0)
    opd = forward_kl.sum(-1).mean(-1)
    advantages = (rewards - rewards.mean(-1, keepdim=True)) / (
        rewards.std(-1, keepdim=True, unbiased=False) + 1e-8)
    sampled_s = s.gather(-1, actions[..., None]).squeeze(-1)
    ratio = (sampled_s - old_logp.detach()).exp()
    advantage = advantages.detach()[..., None]
    actor = torch.maximum(-ratio * advantage, -ratio.clamp(1 - clip, 1 + clip) * advantage)
    grpo = actor.masked_fill(~mask.bool(), 0).sum(-1).mean(-1)
    return torch.where(routed, grpo, opd).mean(), {
        "routed_grpo": routed.detach(), "acquisition_scores": scores,
        "cosine_ratio": fraction, "opd_by_prompt": opd.detach(),
    }


def sguid_coefficient(teacher_logp, student_logp, mask, correct, *, kappa=0.05, gap_clip=2.0):
    """Robust sampled-token gap; verifier-aligned sign and strict gate (Eqs.7-10)."""
    import torch

    if teacher_logp.shape != student_logp.shape or mask.shape != student_logp.shape:
        raise ValueError("aligned skill-conditioned teacher/student token scores required")
    if correct.shape != mask.shape[:-1] or kappa <= 0 or gap_clip <= 0:
        raise ValueError("one verifier result per response and positive gate/clip required")
    if not bool(mask.bool().any(-1).all()):
        raise ValueError("relevant token masks cannot be empty")
    gap = (teacher_logp.detach() - student_logp.detach()).clamp(-gap_clip, gap_clip)
    support = gap.masked_fill(~mask.bool(), 0).sum(-1) / mask.sum(-1)
    verifier = torch.where(correct.bool(), 1., -1.)
    return torch.sign(verifier * support) * (support.abs() > kappa), support


@dataclass
class SkillActivity:
    early_retrievals: int = 0
    late_retrievals: int = 0
    early_positive: int = 0
    late_positive: int = 0

    def record(self, *, early: bool, coefficient: float):
        if early:
            self.early_retrievals += 1
            self.early_positive += int(coefficient > 0)
        else:
            self.late_retrievals += 1
            self.late_positive += int(coefficient > 0)


def select_sguid_skills(activities: dict[str, SkillActivity], *, count=6, late_minimum=2, tau=2.0):
    """Eq.11, rank A_L then Q_L; never rank retrieval frequency alone."""
    if count < 1 or late_minimum < 1 or tau <= 1:
        raise ValueError("positive count/minimum and tau > 1 required")
    eligible = []
    for key, a in activities.items():
        if not (0 <= a.early_positive <= a.early_retrievals
                and 0 <= a.late_positive <= a.late_retrievals):
            raise ValueError("invalid activity counts")
        if a.early_positive > 0 and a.late_positive >= late_minimum:
            qe, ql = a.early_positive / a.early_retrievals, a.late_positive / a.late_retrievals
            if ql >= qe / tau:
                eligible.append((key, a.late_positive, ql))
    eligible.sort(key=lambda x: (-x[1], -x[2], x[0]))
    return tuple(key for key, _, _ in eligible[:count])


def sguid_round(model, training_rows, *, curate, distill, count=6, late_minimum=2, tau=2.0):
    """Curate -> probe -> restore theta_r -> compact distillation.

    Both callbacks receive *only* training rows. curate must generate skills from
    the current student's verified training rollouts. distill(model, rows, bank,
    collect_activity) must execute real updates and return activity statistics.
    No eligible bank is an explicit failure, never a fallback to hand-written skills.
    """
    from copy import deepcopy

    initial = deepcopy(model.state_dict())
    bank = curate(model, training_rows)
    if not bank:
        raise ValueError("student-generated skill bank is empty")
    try:
        activities = distill(model, training_rows, bank, True)
        selected = select_sguid_skills(activities, count=count, late_minimum=late_minimum, tau=tau)
    finally:
        model.load_state_dict(initial)
    if not selected:
        raise ValueError("no skills passed the persistence criterion")
    if any(key not in bank for key in selected):
        raise ValueError("activity refers to a skill outside the curated bank")
    compact = {key: bank[key] for key in selected}
    distill(model, training_rows, compact, False)
    return {"selected_skills": selected, "candidate_count": len(bank), "restarted_from_round_base": True}
