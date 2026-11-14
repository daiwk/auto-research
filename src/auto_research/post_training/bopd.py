"""BOPD forward-KL and exact stage-II handoff (2611.13680, Eqs. 4/7).

No LLM, reference prompt constructor, rollout sampler or complete two-stage
training loop is supplied. The diagnostic is actual tensor loss/handoff work,
not substitute task-capability training.
"""
from __future__ import annotations

from collections.abc import Callable, Iterable
from copy import deepcopy
from dataclasses import dataclass
import torch
from torch import Tensor, nn

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/bopd-a100-20261112.json"


def forward_kl(student_logits: Tensor, teacher_logits: Tensor, mask: Tensor) -> Tensor:
    """Full-vocabulary KL(teacher||student), mean tokens THEN mean trajectories.

    Teacher distributions are detached. This implements the mathematical loss
    in Eqs. 4/7, not the incompletely specified pointwise-clipped trainer noted
    in Appendix A (the linked author repository was empty when reviewed).
    """
    if student_logits.ndim != 3 or min(student_logits.shape) < 1 or teacher_logits.shape != student_logits.shape or mask.shape != student_logits.shape[:2] or mask.dtype != torch.bool:
        raise ValueError("aligned [batch,tokens,vocab] logits and Boolean mask required")
    if student_logits.device != teacher_logits.device or student_logits.device != mask.device or not student_logits.is_floating_point() or not teacher_logits.is_floating_point():
        raise ValueError("floating logits and mask on the same device required")
    if not bool(mask.any(-1).all()) or not bool(torch.isfinite(student_logits[mask]).all()) or not bool(torch.isfinite(teacher_logits[mask]).all()):
        raise ValueError("finite valid logits and nonempty trajectories required")
    dtype = torch.promote_types(student_logits.dtype, teacher_logits.dtype)
    if dtype in {torch.bfloat16, torch.float16}:
        dtype = torch.float32
    student = torch.where(mask[..., None], student_logits.to(dtype), 0.).log_softmax(-1)
    teacher = torch.where(mask[..., None], teacher_logits.detach().to(dtype), 0.).log_softmax(-1)
    token_loss = (teacher.exp() * (teacher - student)).sum(-1)
    return ((token_loss * mask).sum(-1) / mask.sum(-1)).mean()


@dataclass
class StageTwo:
    student: nn.Module
    teacher: nn.Module
    optimizer: torch.optim.Optimizer


def stage_two_handoff(initial_model: nn.Module, intermediate_model: nn.Module,
                      optimizer_factory: Callable[[Iterable[nn.Parameter]], torch.optim.Optimizer]) -> StageTwo:
    """Algorithm 1 lines10--12: freeze M1; restore student EXACTLY to M0.

    Parameters AND persistent buffers are copied; stage-I optimizer state must
    not carry over. Caller must preserve the original initial checkpoint.
    """
    if not isinstance(initial_model, nn.Module) or not isinstance(intermediate_model, nn.Module):
        raise ValueError("initial and intermediate PyTorch modules required")
    base, intermediate = initial_model.state_dict(), intermediate_model.state_dict()
    if set(base) != set(intermediate) or any(base[k].shape != intermediate[k].shape or base[k].dtype != intermediate[k].dtype or base[k].device != intermediate[k].device for k in base):
        raise ValueError("initial/intermediate architecture, dtype and device must match")
    student, teacher = deepcopy(initial_model), deepcopy(intermediate_model)
    student.train()
    teacher.eval()
    teacher.requires_grad_(False)
    for parameter in teacher.parameters():
        parameter.grad = None
    # Fresh parameters must not inherit stale .grad fields copied by a module.
    for parameter in student.parameters():
        parameter.grad = None
    parameters = [p for p in student.parameters() if p.requires_grad]
    if not parameters:
        raise ValueError("fresh student needs trainable parameters")
    optimizer = optimizer_factory(parameters)
    if not isinstance(optimizer, torch.optim.Optimizer):
        raise ValueError("optimizer factory must return a PyTorch optimizer")
    actual = [p for group in optimizer.param_groups for p in group["params"]]
    if optimizer.state or len(actual) != len(parameters) or {id(p) for p in actual} != {id(p) for p in parameters}:
        raise ValueError("fresh empty optimizer bound only to the new student required")
    return StageTwo(student, teacher, optimizer)


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    target = torch.device(device)
    if target.type not in {"cpu", "cuda"}:
        raise ValueError("CPU or CUDA device required")
    if target.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("actual CUDA required; no CPU fallback")
    generator = torch.Generator(device="cpu").manual_seed(seed)
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(seed)
        initial = nn.Linear(5, 7, dtype=torch.float64).to(target)
    intermediate = deepcopy(initial)
    inputs = torch.randn(2, 4, 5, generator=generator, dtype=torch.float64).to(target)
    fixed_logits = torch.randn(2, 4, 7, generator=generator, dtype=torch.float64).to(target)
    mask = torch.tensor([[True, True, False, False], [True, True, True, True]], device=target)
    stage_one_optimizer = torch.optim.AdamW(intermediate.parameters(), lr=.01)
    loss = forward_kl(intermediate(inputs), fixed_logits, mask)
    loss.backward(); stage_one_optimizer.step()
    bundle = stage_two_handoff(initial, intermediate, lambda parameters: torch.optim.AdamW(parameters, lr=.01))
    initial_difference = max(float((p - q).detach().abs().max()) for p, q in zip(bundle.student.parameters(), initial.parameters()))
    teacher_difference = max(float((p - q).detach().abs().max()) for p, q in zip(bundle.teacher.parameters(), intermediate.parameters()))
    teacher_snapshot = [p.detach().clone() for p in bundle.teacher.parameters()]
    teacher_logits = bundle.teacher(inputs)
    student_logits = bundle.student(inputs)
    second_loss = forward_kl(student_logits, teacher_logits, mask)
    second_loss.backward()
    student_gradient = sum(float(p.grad.square().sum()) for p in bundle.student.parameters() if p.grad is not None) ** .5
    bundle.optimizer.step()
    after = forward_kl(bundle.student(inputs), bundle.teacher(inputs), mask)
    checks = {
        "fresh_student_restored_exact_initial_weights": initial_difference == 0.,
        "frozen_teacher_copies_intermediate_weights": teacher_difference == 0.,
        "fresh_optimizer_not_stage_one_optimizer": bundle.optimizer is not stage_one_optimizer,
        "teacher_has_no_gradient": all(p.grad is None and not p.requires_grad for p in bundle.teacher.parameters()),
        "teacher_unchanged_by_student_update": all(torch.equal(p, old) for p, old in zip(bundle.teacher.parameters(), teacher_snapshot)),
        "student_receives_actual_loss_gradient": student_gradient > 0.,
        "loss_and_update_finite": bool(torch.isfinite(second_loss)) and bool(torch.isfinite(after)),
        "student_teacher_storage_disjoint": all(p.data_ptr() != q.data_ptr() for p, q in zip(bundle.student.parameters(), bundle.teacher.parameters())),
    }
    return {"seed": seed, "device": str(inputs.device), "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"forward_kl_before_student_update": float(second_loss.detach()), "forward_kl_after_student_update": float(after.detach()), "student_gradient_norm": student_gradient, "fresh_student_max_initial_error": initial_difference, "teacher_max_copy_error": teacher_difference, "pretrained_model_calls": 0}, "checks": checks}
