"""UserArena OPTD Equations 5--10: independent full-vocabulary loss component.

No upstream code or user trajectories are redistributed. This module neither
extracts privileged intent nor generates shopping actions. Callers must score
the *same student-generated prefixes* with the frozen teacher with/without
training-only intent; evaluated students must never receive that intent.
"""
from __future__ import annotations

import math

import torch
from torch import Tensor


def _log_probs(logits: Tensor, mask: Tensor) -> Tensor:
    if logits.ndim != 3 or min(logits.shape) < 1 or not logits.is_floating_point():
        raise ValueError("nonempty floating [state, response, vocabulary] logits required")
    if (mask.shape != logits.shape[:2] or mask.dtype != torch.bool
            or mask.device != logits.device or not bool(mask.any(1).all())):
        raise ValueError("aligned nonempty-per-state Boolean response mask required")
    if not bool(torch.isfinite(logits[mask]).all()):
        raise ValueError("finite active full-vocabulary logits required")
    dtype = torch.float32 if logits.dtype in (torch.float16, torch.bfloat16) else logits.dtype
    result = torch.where(mask[..., None], logits.to(dtype), 0.).log_softmax(-1)
    if not bool(torch.isfinite(result).all()):
        raise ValueError("log probabilities must be representable")
    return result


@torch.no_grad()
def trust_region_teacher(unconditioned_logits: Tensor, intent_logits: Tensor,
                         mask: Tensor, *, epsilon: float = .02,
                         lambda_max: float = 1., bisection_steps: int = 8) -> dict:
    """Largest feasible geometric interpolation, lower endpoint of bisection.

    KL(target || unconditioned teacher) is bounded separately at each token.
    Feasible lambda_max is retained exactly; otherwise the coefficient error
    is at most lambda_max/2**bisection_steps. Teachers are always detached.
    """
    if (not math.isfinite(epsilon) or epsilon < 0 or not math.isfinite(lambda_max)
            or not 0 <= lambda_max <= 1 or type(bisection_steps) is not int
            or not 1 <= bisection_steps <= 64):
        raise ValueError("finite nonnegative KL budget, lambda in [0,1], and 1..64 steps required")
    if (intent_logits.shape != unconditioned_logits.shape
            or intent_logits.dtype != unconditioned_logits.dtype
            or intent_logits.device != unconditioned_logits.device):
        raise ValueError("aligned intent and unconditioned teacher logits required")
    base = _log_probs(unconditioned_logits.detach(), mask)
    guided = _log_probs(intent_logits.detach(), mask)
    direction = guided - base
    if not bool(torch.isfinite(direction).all()):
        raise ValueError("teacher log-probability difference must be representable")

    def evaluate(coefficient):
        # Equivalent to softmax((1-lambda)*log q0 + lambda*log qz).
        log_target = (base + coefficient[..., None] * direction).log_softmax(-1)
        kl = (log_target.exp() * (log_target - base)).sum(-1).clamp_min(0.)
        return log_target, kl

    lower = torch.zeros_like(base[..., 0])
    upper = torch.full_like(lower, lambda_max)
    _, upper_kl = evaluate(upper)
    full_feasible = upper_kl <= epsilon
    for _ in range(bisection_steps):
        middle = (lower + upper) / 2
        _, kl = evaluate(middle)
        feasible = kl <= epsilon
        lower = torch.where(feasible, middle, lower)
        upper = torch.where(feasible, upper, middle)
    coefficient = torch.where(full_feasible, lambda_max, lower)
    # At zero budget, any numerically invisible positive movement is not
    # evidence of exact feasibility. Identical endpoints can retain max.
    if epsilon == 0:
        identical = (guided == base).all(-1)
        coefficient = torch.where(identical, lambda_max, 0.)
    coefficient = torch.where(mask, coefficient, 0.)
    log_target, kl = evaluate(coefficient)
    return {"log_target": log_target, "lambda": coefficient,
            "kl_from_unconditioned": kl, "log_unconditioned": base}


def optd_loss(student_rollout_logits: Tensor, teacher_unconditioned_logits: Tensor,
              teacher_intent_logits: Tensor, rollout_mask: Tensor,
              student_gold_logits: Tensor, gold_tokens: Tensor, gold_mask: Tensor,
              *, beta: float = .5, gamma: float = .1, epsilon: float = .02,
              lambda_max: float = 1., bisection_steps: int = 8) -> tuple[Tensor, dict]:
    """State-equal mean of token-equal JSD plus separate teacher-forced CE.

    Gold logits use recorded prefixes, NOT student rollout prefixes. Gold
    actions are loss-side supervision only. This loss cannot attest that an
    external rollout was actually on-policy, or certify safe intent extraction.
    """
    if not math.isfinite(beta) or not 0 < beta < 1 or not math.isfinite(gamma) or gamma < 0:
        raise ValueError("beta in (0,1) and nonnegative finite grounding weight required")
    current = _log_probs(student_rollout_logits, rollout_mask)
    if any(t.shape != student_rollout_logits.shape or t.dtype != student_rollout_logits.dtype
           or t.device != student_rollout_logits.device
           for t in (teacher_unconditioned_logits, teacher_intent_logits)):
        raise ValueError("teachers must score the same rollout positions/vocabulary")
    gold = _log_probs(student_gold_logits, gold_mask)
    if (gold.shape[0] != current.shape[0] or gold.shape[-1] != current.shape[-1]
            or gold.dtype != current.dtype or gold.device != current.device):
        raise ValueError("paired state count, vocabulary, compute dtype and device required")
    if (gold_tokens.shape != gold_mask.shape or gold_tokens.dtype != torch.long
            or gold_tokens.device != gold.device
            or not bool(((gold_tokens[gold_mask] >= 0) & (gold_tokens[gold_mask] < gold.shape[-1])).all())):
        raise ValueError("valid integer grounding targets aligned with gold mask required")
    audit = trust_region_teacher(teacher_unconditioned_logits, teacher_intent_logits, rollout_mask,
        epsilon=epsilon, lambda_max=lambda_max, bisection_steps=bisection_steps)
    target = audit["log_target"]
    mixture = torch.logaddexp(target + math.log(beta), current + math.log1p(-beta))
    jsd = beta * (target.exp() * (target - mixture)).sum(-1)
    jsd += (1 - beta) * (current.exp() * (current - mixture)).sum(-1)
    per_state_dist = torch.where(rollout_mask, jsd, 0.).sum(1) / rollout_mask.sum(1)
    safe_tokens = torch.where(gold_mask, gold_tokens, 0)
    nll = -gold.gather(-1, safe_tokens[..., None]).squeeze(-1)
    per_state_gold = torch.where(gold_mask, nll, 0.).sum(1) / gold_mask.sum(1)
    distillation = per_state_dist.mean()
    grounding = per_state_gold.mean()
    loss = distillation + gamma * grounding
    if not bool(torch.isfinite(loss) & torch.isfinite(distillation) & torch.isfinite(grounding)):
        raise ValueError("objective and reductions must be representable in compute dtype")
    return loss, {**audit, "distillation": distillation.detach(), "grounding": grounding.detach(),
                  "per_state_distillation": per_state_dist.detach(), "per_state_grounding": per_state_gold.detach()}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """Seeded full-vocabulary backward/update, not a user-simulator benchmark."""
    generator = torch.Generator(device=device).manual_seed(seed)
    kwargs = {"generator": generator, "device": device, "dtype": torch.float64}
    student = torch.randn(3, 4, 7, **kwargs).requires_grad_()
    grounding_logits = torch.randn(3, 5, 7, **kwargs).requires_grad_()
    base = torch.randn(3, 4, 7, **kwargs).requires_grad_()
    intent = torch.randn(3, 4, 7, **kwargs).requires_grad_()
    mask = torch.tensor([[1, 1, 1, 1], [1, 1, 0, 0], [1, 0, 0, 0]], dtype=torch.bool, device=device)
    gold_mask = torch.tensor([[1, 1, 1, 1, 1], [1, 1, 1, 0, 0], [1, 1, 0, 0, 0]], dtype=torch.bool, device=device)
    gold = torch.randint(7, (3, 5), generator=generator, device=device)
    loss, audit = optd_loss(student, base, intent, mask, grounding_logits, gold, gold_mask)
    p = student.softmax(-1)
    q = audit["log_target"].exp()
    mixture = (p + q) / 2
    terms = .5 * (q * (q.log() - mixture.log()) + p * (p.log() - mixture.log())).sum(-1)
    reference_dist = torch.stack([terms[i, mask[i]].mean() for i in range(3)]).mean()
    gt_log = grounding_logits.log_softmax(-1)
    reference_gt = torch.stack([-gt_log[i, gold_mask[i], gold[i, gold_mask[i]]].mean() for i in range(3)]).mean()
    reference_error = float((loss - reference_dist - .1 * reference_gt).abs().detach())
    initial = student.detach().clone()
    initial_gold = grounding_logits.detach().clone()
    loss.backward()
    finite = bool(student.grad.isfinite().all() and grounding_logits.grad.isfinite().all())
    with torch.no_grad():
        student -= .01 * student.grad
        grounding_logits -= .01 * grounding_logits.grad
    after, _ = optd_loss(student, base, intent, mask, grounding_logits, gold, gold_mask)
    delta = float((student.detach() - initial).norm() + (grounding_logits.detach() - initial_gold).norm())
    kl = float(audit["kl_from_unconditioned"][mask].max())
    endpoint, endpoint_audit = optd_loss(student, base, intent, mask, grounding_logits, gold, gold_mask, epsilon=0.)
    bound = -(.5 * math.log(.5) + .5 * math.log(.5))
    return {"seed": seed, "diagnostic_only": True, "component": "userarena_optd_equations_5_to_10",
        "metrics": {"loss_before": float(loss.detach()), "loss_after": float(after.detach()),
            "formula_reference_error": reference_error, "parameter_delta": delta,
            "max_teacher_kl": kl, "max_lambda": float(audit["lambda"][mask].max()),
            "distillation": float(audit["distillation"]), "grounding": float(audit["grounding"]),
            "optimizer_updates": 1, "model_calls": 0},
        "checks": {"teacher_detached": base.grad is None and intent.grad is None,
            "formula_reference_matches": reference_error < 1e-10,
            "per_token_trust_budget": kl <= .02 + 1e-12,
            "zero_budget_recovers_unconditioned": bool((endpoint_audit["lambda"][mask] == 0).all()) and bool(endpoint.isfinite()),
            "bounded_jsd": -.000000000001 <= float(audit["distillation"]) <= bound + 1e-12,
            "finite_gradients": finite, "real_parameter_update": delta > 0,
            "separate_grounding_branch_updated": bool((grounding_logits.detach() - initial_gold).norm() > 0),
            "padding_gradient_zero": bool((student.grad[~mask] == 0).all() and (grounding_logits.grad[~gold_mask] == 0).all()),
            "fixed_objective_decreases": bool(after.detach() < loss.detach())}}
