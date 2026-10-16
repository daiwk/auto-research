"""Competitive Token Selection core, arXiv:2610.20642 Eqs. 1-6.

Independent formula implementation; does not vendor the upstream repository.
Sampling policy and language model are caller-owned. All soft paths remain
PyTorch tensors with real gradients (top-k membership is piecewise constant).
"""
from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import Tensor


@dataclass(frozen=True)
class CotsState:
    reasoning: Tensor
    finished: Tensor

    @classmethod
    def initial(cls, batch_shape: tuple[int, ...], *, device: str | torch.device = "cpu") -> CotsState:
        return cls(torch.ones(batch_shape, dtype=torch.bool, device=device),
                   torch.zeros(batch_shape, dtype=torch.bool, device=device))


@dataclass(frozen=True)
class CotsStep:
    next_embedding: Tensor
    discrete_embedding: Tensor
    soft_embedding: Tensor
    alpha: Tensor
    effective_alpha: Tensor
    sampled_coefficient: Tensor
    support: Tensor
    support_weights: Tensor
    state: CotsState


def _member(tokens: Tensor, identifiers: tuple[int, ...]) -> Tensor:
    found = torch.zeros_like(tokens, dtype=torch.bool)
    for identifier in identifiers:
        found = found | tokens.eq(identifier)
    return found


def competitive_token_selection(probabilities: Tensor, embeddings: Tensor, sampled_tokens: Tensor,
                                state: CotsState, *, top_k: int = 9,
                                end_think_token_ids: tuple[int, ...] = (),
                                protected_token_ids: tuple[int, ...] = (),
                                eos_token_ids: tuple[int, ...] = ()) -> CotsStep:
    """Create next-step input and advance an irreversible per-sequence phase lock.

    `probabilities` is the caller's actual next-token distribution, including
    any caller-owned sampling transformation. `sampled_tokens` need not be in
    top-k. End-of-thinking and EOS tokens are discrete on their emission step;
    protected operators only disable mixing for that step. Callers stop model
    decoding when `state.finished` is true, rather than treating this function
    as a complete generation loop.
    """
    if (probabilities.ndim < 1 or not probabilities.is_floating_point() or
            embeddings.ndim != 2 or not embeddings.is_floating_point() or
            embeddings.shape[0] != probabilities.shape[-1] or probabilities.shape[-1] < 2):
        raise ValueError("expected probability [...,vocab>=2] and embedding [vocab,dim]")
    prefix, vocabulary = probabilities.shape[:-1], probabilities.shape[-1]
    if not isinstance(top_k, int) or isinstance(top_k, bool) or not 1 <= top_k <= vocabulary:
        raise ValueError("top_k must fit the vocabulary")
    if (sampled_tokens.shape != prefix or sampled_tokens.dtype != torch.int64 or
            any(flag.shape != prefix or flag.dtype != torch.bool for flag in
                (state.reasoning, state.finished))):
        raise ValueError("sampled tokens and boolean state must match the probability batch")
    tensors = (embeddings, sampled_tokens, state.reasoning, state.finished)
    if any(tensor.device != probabilities.device for tensor in tensors):
        raise ValueError("all inputs must share a device")
    if bool(((sampled_tokens < 0) | (sampled_tokens >= vocabulary)).any()):
        raise ValueError("sampled token outside vocabulary")
    for identifiers in (end_think_token_ids, protected_token_ids, eos_token_ids):
        if any(not isinstance(i, int) or not 0 <= i < vocabulary for i in identifiers):
            raise ValueError("control token outside vocabulary")
    if not bool(torch.isfinite(probabilities).all()) or bool((probabilities < 0).any()):
        raise ValueError("probabilities must be finite and nonnegative")
    tolerance = 5e-3 if probabilities.dtype in {torch.float16, torch.bfloat16} else 1e-5
    if not torch.allclose(probabilities.sum(-1), torch.ones_like(probabilities.sum(-1)),
                          rtol=tolerance, atol=tolerance):
        raise ValueError("probabilities must sum to one")
    # Compute probability weights in FP32 for low-precision backbones, without detaching.
    work_dtype = torch.float64 if probabilities.dtype == torch.float64 else torch.float32
    work = probabilities.to(work_dtype)
    top_two = work.topk(2, dim=-1).values
    alpha = top_two[..., 1] / top_two.sum(-1)
    weights, support = work.topk(top_k, dim=-1)
    weights = weights / weights.sum(-1, keepdim=True)
    soft = (weights.unsqueeze(-1) * embeddings[support].to(work_dtype)).sum(-2)
    discrete = embeddings[sampled_tokens].to(work_dtype)
    finished = state.finished | _member(sampled_tokens, eos_token_ids)
    reasoning = state.reasoning & ~_member(sampled_tokens, end_think_token_ids) & ~finished
    protected = _member(sampled_tokens, protected_token_ids)
    effective = alpha * (reasoning & ~protected).to(work_dtype)
    mixed = (1 - effective.unsqueeze(-1)) * discrete + effective.unsqueeze(-1) * soft
    support_anchor = (weights * support.eq(sampled_tokens.unsqueeze(-1))).sum(-1)
    coefficient = 1 - effective + effective * support_anchor
    return CotsStep(mixed.to(embeddings.dtype), discrete.to(embeddings.dtype),
                    soft.to(embeddings.dtype), alpha, effective, coefficient,
                    support, weights, CotsState(reasoning, finished))
