"""Shuffled OPSD conditioning and signed capped KL (arXiv:2611.04958).

L1 text/tensor components only. No pretrained model, student generation,
teacher scoring, LoRA trainer or intact-problem benchmark is run here.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import math
import random

import torch
from torch import Tensor

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/shuffled-opsd-a100-20261104.json"


@dataclass(frozen=True)
class SharedConditioning:
    shared_problems: tuple[str, ...]
    teacher_examples: tuple[str, ...]
    reference_indices: tuple[int, ...]

    @property
    def student_problems(self):
        return self.shared_problems

    @property
    def teacher_problems(self):
        return self.shared_problems


def prepare_shared_inputs(problems: list[str], worked_examples: list[str], *, seed: int,
                          block_size: int = 1, reference_shift: int = 111) -> SharedConditioning:
    """Appendix A.2: whitespace blocks, fixed (i+111)%N references.

    Worked examples are explicitly separate teacher-only fields. This helper
    does not construct chat prompts or apply any transformation at evaluation.
    A local pool for which the fixed shift self-pairs must be rejected rather
    than silently substituting an unpublished reference assignment.
    """
    count = len(problems)
    if count < 2 or len(worked_examples) != count:
        raise ValueError("aligned pools with at least two records required")
    if type(block_size) is not int or block_size < 1 or type(reference_shift) is not int or reference_shift % count == 0:
        raise ValueError("positive block size and non-self-pairing integer reference shift required")
    if any(not isinstance(value, str) or not value.strip() for value in problems + worked_examples):
        raise ValueError("nonempty problem and worked-example strings required")
    generator = random.Random(seed)
    transformed = []
    for problem in problems:
        words = problem.split()
        blocks = [words[index:index + block_size] for index in range(0, len(words), block_size)]
        generator.shuffle(blocks)
        transformed.append(" ".join(word for block in blocks for word in block))
    indices = tuple((index + reference_shift) % count for index in range(count))
    return SharedConditioning(tuple(transformed), tuple(worked_examples[index] for index in indices), indices)


def capped_distillation_loss(student_logits: Tensor, teacher_logits: Tensor, response_mask: Tensor,
                             *, temperature: float = 1.1, cap: float = .05) -> Tensor:
    """Appendix A.1 Eq.8, NOT ordinary KL and NOT a nonnegative clipping.

    Upper-cap each signed teacher-to-student vocabulary contribution, retain
    negatives, mean tokens inside each response, then mean responses equally.
    Teacher scores and sampled histories are detached. No T-squared multiplier.
    """
    if (student_logits.ndim != 3 or min(student_logits.shape) < 1
            or teacher_logits.shape != student_logits.shape):
        raise ValueError("aligned nonempty [response,time,vocabulary] logits required")
    if (not student_logits.is_floating_point() or not teacher_logits.is_floating_point()
            or student_logits.device != teacher_logits.device):
        raise ValueError("floating logits on one device required")
    if (response_mask.shape != student_logits.shape[:2] or response_mask.dtype != torch.bool
            or response_mask.device != student_logits.device or not bool(response_mask.any(-1).all())):
        raise ValueError("nonempty Boolean response mask per example required")
    if not math.isfinite(temperature) or temperature <= 0 or not math.isfinite(cap) or cap <= 0:
        raise ValueError("finite positive temperature and contribution cap required")
    if not bool(torch.isfinite(student_logits[response_mask]).all()) or not bool(torch.isfinite(teacher_logits[response_mask]).all()):
        raise ValueError("finite active student and teacher logits required")
    dtype = torch.promote_types(student_logits.dtype, teacher_logits.dtype)
    if dtype in (torch.float16, torch.bfloat16):
        dtype = torch.float32
    student_logp = (student_logits[response_mask].to(dtype) / temperature).log_softmax(-1)
    teacher_logp = (teacher_logits.detach()[response_mask].to(dtype) / temperature).log_softmax(-1)
    signed = teacher_logp.exp() * (teacher_logp - student_logp)
    token_loss = signed.clamp(max=cap).sum(-1)
    padded = token_loss.new_zeros(response_mask.shape).masked_scatter(response_mask, token_loss)
    return (padded.sum(-1) / response_mask.sum(-1)).mean()


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    generator = torch.Generator(device="cpu").manual_seed(seed)
    problems = [f"problem {i} needs five distinct word tokens" for i in range(5)]
    examples = [f"reference {i}: the worked solution stays intact" for i in range(5)]
    conditioning = prepare_shared_inputs(problems, examples, seed=seed)
    student = torch.randn(2, 3, 5, generator=generator, dtype=torch.float64).to(device).requires_grad_()
    teacher = torch.randn(2, 3, 5, generator=generator, dtype=torch.float64).to(device).requires_grad_()
    mask = torch.tensor([[True, False, False], [True, True, True]], device=device)
    loss = capped_distillation_loss(student, teacher, mask)
    reference = []
    p = (student.detach() / 1.1).softmax(-1)
    q = (teacher.detach() / 1.1).softmax(-1)
    for row in range(2):
        terms = []
        for step in range(3):
            if bool(mask[row, step]):
                terms.append(sum(min(float(q[row, step, token]) * math.log(float(q[row, step, token] / p[row, step, token])), .05) for token in range(5)))
        reference.append(sum(terms) / len(terms))
    error = abs(float(loss.detach()) - sum(reference) / 2)
    loss.backward()
    gradient = student.grad.detach().clone()
    after = capped_distillation_loss(student.detach() - .01 * gradient, teacher, mask)
    negative_example = capped_distillation_loss(
        torch.tensor([[[.99, .01]]], dtype=torch.float64, device=device).log(),
        torch.tensor([[[.5, .5]]], dtype=torch.float64, device=device).log(),
        torch.ones(1, 1, dtype=torch.bool, device=device), temperature=1.)
    checks = {
        "student_teacher_share_exact_transformed_problem": conditioning.student_problems == conditioning.teacher_problems,
        "word_multisets_preserved": all(Counter(before.split()) == Counter(after.split()) for before, after in zip(problems, conditioning.shared_problems)),
        "fixed_shift_and_intact_teacher_reference": conditioning.reference_indices == (1, 2, 3, 4, 0) and conditioning.teacher_examples == tuple(examples[index] for index in conditioning.reference_indices),
        "signed_capped_manual_reference_agrees": error < 1e-10,
        "negative_contributions_retained": float(negative_example) < 0,
        "teacher_frozen": teacher.grad is None,
        "padding_zero_gradient": bool((gradient[~mask] == 0).all()),
        "gradient_finite_nonzero": bool(torch.isfinite(gradient).all()) and float(gradient.norm()) > 0,
        "small_update_reduces_component_loss": float(after.detach()) < float(loss.detach()),
    }
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"loss": float(loss.detach()), "loss_after": float(after.detach()),
                        "manual_loss_error": error, "signed_cap_negative_example": float(negative_example),
                        "gradient_norm": float(gradient.norm()), "model_calls": 0}, "checks": checks}
