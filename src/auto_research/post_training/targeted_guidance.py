"""Failed-turn targeted self-distillation contract (arXiv:2611.05266).

L1 losses over externally aligned logits. No coding agent, feedback judge,
autoregressive rollout, checkpoint or full GRPO training pipeline is provided.
"""
from __future__ import annotations

import math

import torch
from torch import Tensor

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/targeted-guidance-a100-20261104.json"


def token_failure_mask(turn_ids: Tensor, failed_turns: Tensor) -> Tensor:
    """Map externally judged failed turns onto tokens; -1 is outside a turn.

    This maps supplied judgments; it neither reads gold nor fabricates a judge.
    A caller must also mark response tokens separately from any prompt tokens.
    """
    if (turn_ids.ndim != 2 or turn_ids.dtype != torch.long or failed_turns.ndim != 2
            or failed_turns.dtype != torch.bool or failed_turns.device != turn_ids.device
            or turn_ids.shape[0] != failed_turns.shape[0] or failed_turns.shape[1] < 1):
        raise ValueError("aligned int64 token turn IDs and Boolean failed-turn table required")
    if bool(((turn_ids < -1) | (turn_ids >= failed_turns.shape[1])).any()):
        raise ValueError("turn IDs must index the failure table or equal -1")
    return failed_turns.gather(1, turn_ids.clamp(min=0)) & (turn_ids >= 0)


def targeted_guidance_loss(student_logits: Tensor, teacher_logits: Tensor, response_mask: Tensor,
                           failed_mask: Tensor, *, grpo_loss: Tensor,
                           guidance_weight: float = .1) -> Tensor:
    """Eq.3: external RL + failure-gated full-vocabulary reverse KL.

    Feedback-conditioned teacher logits are frozen. KL is summed only on failed
    turns but normalized by ALL response tokens in each rollout, then averaged
    over rollouts. Padding and nonfailed teacher rows are never evaluated.
    """
    if student_logits.ndim != 3 or min(student_logits.shape) < 1 or teacher_logits.shape != student_logits.shape:
        raise ValueError("aligned nonempty [rollout,time,vocabulary] logits required")
    if (not student_logits.is_floating_point() or not teacher_logits.is_floating_point()
            or teacher_logits.device != student_logits.device):
        raise ValueError("floating logits on one device required")
    for mask in (response_mask, failed_mask):
        if mask.shape != student_logits.shape[:2] or mask.dtype != torch.bool or mask.device != student_logits.device:
            raise ValueError("aligned Boolean response and failed-turn masks required")
    if not bool(response_mask.any(-1).all()) or bool((failed_mask & ~response_mask).any()):
        raise ValueError("nonempty responses and failure tokens restricted to responses required")
    if not bool(torch.isfinite(student_logits[response_mask]).all()):
        raise ValueError("active student logits must be finite")
    if (not isinstance(grpo_loss, Tensor) or grpo_loss.ndim != 0 or not grpo_loss.is_floating_point()
            or grpo_loss.device != student_logits.device or not bool(torch.isfinite(grpo_loss))):
        raise ValueError("finite differentiable scalar external GRPO loss required")
    if not math.isfinite(guidance_weight) or guidance_weight < 0:
        raise ValueError("finite nonnegative guidance weight required")
    if not bool(failed_mask.any()) or guidance_weight == 0:
        return grpo_loss + (student_logits[response_mask] * 0).sum()
    if not bool(torch.isfinite(teacher_logits[failed_mask]).all()):
        raise ValueError("teacher logits at failed turns must be finite")
    dtype = torch.promote_types(student_logits.dtype, teacher_logits.dtype)
    if dtype in (torch.float16, torch.bfloat16):
        dtype = torch.float32
    logp = student_logits[failed_mask].to(dtype).log_softmax(-1)
    logq = teacher_logits.detach()[failed_mask].to(dtype).log_softmax(-1)
    reverse_kl = (logp.exp() * (logp - logq)).sum(-1)
    padded = reverse_kl.new_zeros(response_mask.shape).masked_scatter(failed_mask, reverse_kl)
    auxiliary = (padded.sum(-1) / response_mask.sum(-1)).mean()
    return grpo_loss + guidance_weight * auxiliary


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    generator = torch.Generator(device="cpu").manual_seed(seed)
    student = torch.randn(2, 4, 5, generator=generator, dtype=torch.float64).to(device).requires_grad_()
    teacher = torch.randn(2, 4, 5, generator=generator, dtype=torch.float64).to(device).requires_grad_()
    response = torch.tensor([[True, True, True, True], [True, True, True, False]], device=device)
    turns = torch.tensor([[0, 0, 1, 1], [0, 1, 1, -1]], device=device)
    failed = token_failure_mask(turns, torch.tensor([[False, True], [True, False]], device=device))
    grpo = student[response].sum() * 0
    loss = targeted_guidance_loss(student, teacher, response, failed, grpo_loss=grpo, guidance_weight=.3)
    p, q = student.detach().softmax(-1), teacher.detach().softmax(-1)
    reference = 0.
    for row in range(2):
        terms = 0.
        for step in range(4):
            if bool(failed[row, step]):
                terms += sum(float(p[row, step, token]) * math.log(float(p[row, step, token] / q[row, step, token])) for token in range(5))
        reference += .3 * terms / int(response[row].sum()) / 2
    error = abs(float(loss.detach()) - reference)
    loss.backward()
    gradient = student.grad.detach().clone()
    after = targeted_guidance_loss(student.detach() - .01 * gradient, teacher, response, failed,
                                   grpo_loss=grpo.detach(), guidance_weight=.3)
    no_failures = targeted_guidance_loss(student.detach(), teacher, response, torch.zeros_like(response),
                                         grpo_loss=torch.tensor(.7, dtype=torch.float64, device=device))
    checks = {
        "all_token_denominator_manual_reference_agrees": error < 1e-10,
        "teacher_frozen": teacher.grad is None,
        "nonfailed_and_padding_zero_auxiliary_gradient": bool((gradient[~failed] == 0).all()),
        "failed_turn_has_finite_nonzero_gradient": bool(torch.isfinite(gradient).all()) and float(gradient[failed].norm()) > 0,
        "small_update_reduces_component_loss": float(after.detach()) < float(loss.detach()),
        "all_criteria_satisfied_recovers_original_rl_loss": float(no_failures) == .7,
        "padding_not_a_failed_turn": not bool(failed[1, 3]),
    }
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"auxiliary_loss": float(loss.detach()), "auxiliary_loss_after": float(after.detach()),
                        "manual_loss_error": error, "gradient_norm": float(gradient.norm()),
                        "failed_tokens": int(failed.sum()), "model_calls": 0}, "checks": checks}
