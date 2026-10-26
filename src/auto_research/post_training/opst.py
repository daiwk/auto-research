"""OPST's unambiguous curriculum gate, external-divergence reduction and EMA.

The canonical JSD is deliberately NOT implemented: v1 p.5 prints inconsistent
mixture and KL weights. This is not an OPST model, generator or verifier.
"""
from __future__ import annotations

import math
import torch
from torch import Tensor

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/opst-a100-20261026.json"


def verification_gate(fresh_matches: Tensor, paraphrase_matches: Tensor,
                      student_matches_candidate: Tensor, *, duplicate: Tensor | None = None) -> Tensor:
    """Sec.3.4: retain pseudo-verified questions unless ALL G answers match a.

    Boolean inputs are externally measured TRAINING-side observations, not gold
    answers, teacher prompts or a replacement for natural-language verification.
    Consensus on a different answer does not trigger the easy-question filter.
    Semantic duplicate detection, when needed, is external as well.
    """
    if student_matches_candidate.ndim != 2 or min(student_matches_candidate.shape) < 1:
        raise ValueError("nonempty [question,rollout] candidate-match observations required")
    shape = student_matches_candidate.shape[:1]
    inputs = [fresh_matches, paraphrase_matches, student_matches_candidate]
    if fresh_matches.shape != shape or paraphrase_matches.shape != shape:
        raise ValueError("one fresh-context and paraphrase check per question required")
    if duplicate is not None:
        if duplicate.shape != shape:
            raise ValueError("one external duplicate flag per question required")
        inputs.append(duplicate)
    if any(t.dtype != torch.bool or t.device != fresh_matches.device for t in inputs):
        raise ValueError("aligned Boolean observations on one device required")
    result = fresh_matches & paraphrase_matches & ~student_matches_candidate.all(1)
    if duplicate is not None:
        result = result & ~duplicate
    return result.detach().clone()


def masked_divergence_mean(token_divergence: Tensor, response_mask: Tensor) -> Tensor:
    """Eq.6 ONLY: response-token mean, then equal-weight question mean.

    Caller supplies an explicitly chosen per-token divergence. This component
    neither selects nor repairs the inconsistent v1 Eq.5 canonical loss. There
    is no gold/reference-answer input. Padding is removed before arithmetic.
    """
    if token_divergence.ndim != 2 or min(token_divergence.shape) < 1 or not token_divergence.is_floating_point():
        raise ValueError("nonempty floating [question,token] divergences required")
    if response_mask.shape != token_divergence.shape or response_mask.dtype != torch.bool or response_mask.device != token_divergence.device:
        raise ValueError("aligned Boolean response mask required")
    if not bool(response_mask.any(1).all()):
        raise ValueError("each response must contain at least one token")
    values = token_divergence[response_mask]
    if not bool(torch.isfinite(values).all()) or bool((values < 0).any()):
        raise ValueError("finite nonnegative active divergences required")
    dtype = torch.float32 if token_divergence.dtype in (torch.float16, torch.bfloat16) else token_divergence.dtype
    clean = torch.where(response_mask, token_divergence.to(dtype), 0.)
    return (clean.sum(1) / response_mask.sum(1)).mean()


def ema_update(teacher: Tensor, student: Tensor, *, beta: float = .05) -> Tensor:
    """phi_new=(1-beta)*phi_old+beta*theta; beta is NEW student weight.

    Returns a new detached tensor; the caller applies this after its optimizer
    step to each floating parameter and evaluates the EMA teacher, not student.
    Nonfloating buffers and tokenizer/model alignment are outside this operator.
    """
    if not math.isfinite(beta) or not 0 <= beta <= 1:
        raise ValueError("finite beta in [0,1] required")
    if teacher.shape != student.shape or teacher.device != student.device or not teacher.is_floating_point() or not student.is_floating_point():
        raise ValueError("aligned floating teacher/student weights required")
    if not bool(torch.isfinite(teacher).all() & torch.isfinite(student).all()):
        raise ValueError("finite weights required")
    dtype = torch.promote_types(teacher.dtype, student.dtype)
    if dtype in (torch.float16, torch.bfloat16):
        dtype = torch.float32
    return ((1-beta)*teacher.detach().to(dtype) + beta*student.detach().to(dtype)).detach()


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """Synthetic external-divergence autograd check; no JSD or LLM evaluation."""
    resolved=torch.device(device)
    if resolved.type not in ('cpu','cuda') or (resolved.type=='cuda' and not torch.cuda.is_available()):
        raise ValueError("diagnostic requires available CPU or real CUDA; no fallback")
    generator = torch.Generator(device=device).manual_seed(seed)
    values = torch.rand(3, 4, generator=generator, dtype=torch.float64, device=device).requires_grad_()
    mask = torch.tensor([[1,1,1,1],[1,0,0,0],[1,1,0,0]],dtype=torch.bool,device=device)
    loss = masked_divergence_mean(values, mask)
    expected = (values[0].mean()+values[1,0]+values[2,:2].mean())/3
    ref_grad = torch.autograd.grad(expected, values, retain_graph=True)[0]
    loss.backward()
    grad = values.grad.detach().clone()
    updated = ema_update(torch.zeros_like(values), values, beta=.05)
    fresh=torch.tensor([1,1,0],dtype=torch.bool,device=device)
    matches=torch.tensor([[0,0],[1,1],[0,1]],dtype=torch.bool,device=device)
    gate=verification_gate(fresh,torch.ones_like(fresh),matches)
    error=float((loss.detach()-expected.detach()).abs())
    grad_error=float((grad-ref_grad).abs().max())
    return {"seed":seed,"diagnostic_only":True,
        "component":"opst_gate_external_divergence_reducer_ema_not_canonical_jsd",
        "metrics":{"external_divergence_loss":float(loss.detach()),"gradient_norm":float(grad.norm()),
                   "reference_error":error,"gradient_reference_error":grad_error,"retained_questions":int(gate.sum()),
                   "ema_parameter_delta":float(updated.norm())},
        "checks":{"equal_response_weighting":error<1e-12,"gradient_matches_reference":grad_error<1e-12,
                  "padding_zero_gradient":bool((grad[~mask]==0).all()),
                  "different_answer_consensus_retained":bool(gate[0]),
                  "candidate_consensus_rejected":not bool(gate[1]),
                  "failed_verification_rejected":not bool(gate[2]),
                  "ema_new_student_weight":bool(torch.allclose(updated,.05*values.detach())),
                  "ema_detached":not updated.requires_grad}}
