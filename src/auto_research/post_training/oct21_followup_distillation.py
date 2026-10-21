"""A2D reward/candidate update and Projected Distillation's diff-local loss.

Formula-only L1 components: no learned question synthesizer, language projector,
benchmark training, or claim that supplied logits were sampled on-policy.
"""
from __future__ import annotations

import math
from collections.abc import Callable, Sequence

import torch
from torch import Tensor


def _logits(values: Tensor, mask: Tensor) -> Tensor:
    if values.ndim != 3 or min(values.shape) < 1 or not values.is_floating_point():
        raise ValueError("nonempty floating [batch,token,vocabulary] logits required")
    if mask.shape != values.shape[:2] or mask.dtype != torch.bool or mask.device != values.device:
        raise ValueError("aligned Boolean response mask required")
    if not bool(mask.any(1).all()) or not bool(torch.isfinite(values[mask]).all()):
        raise ValueError("every response needs finite active logits")
    safe = torch.where(mask[..., None], values, 0.)
    return safe.float() if safe.dtype in (torch.float16, torch.bfloat16) else safe


def _aligned(left: Tensor, right: Tensor) -> None:
    if left.shape != right.shape or left.device != right.device or left.dtype != right.dtype:
        raise ValueError("same shape, dtype and device required")


def _top_k(k: int, vocabulary: int) -> None:
    if isinstance(k, bool) or not isinstance(k, int) or not 1 <= k <= vocabulary:
        raise ValueError("top_k must be an integer inside the vocabulary")


@torch.no_grad()
def a2d_token_signal(student_logits: Tensor, teacher_logits: Tensor, mask: Tensor,
                     *, top_k: int = 16) -> dict[str, Tensor]:
    """A2D Eq. 2--5: union-renormalized forward KL; ORIGINAL teacher mass.

Both distributions must refer to the same tokenizer and student prefix. The
operator cannot infer tokenizer compatibility from tensor shape alone.
    """
    _aligned(student_logits, teacher_logits)
    s, t = _logits(student_logits, mask).log_softmax(-1), _logits(teacher_logits, mask).log_softmax(-1)
    _top_k(top_k, s.shape[-1])
    ids_s, ids_t = s.topk(top_k, -1).indices, t.topk(top_k, -1).indices
    support = torch.zeros_like(s, dtype=torch.bool).scatter_(-1, ids_s, True).scatter_(-1, ids_t, True)
    log_s = s.masked_fill(~support, -torch.inf)
    log_t = t.masked_fill(~support, -torch.inf)
    log_s = log_s - log_s.logsumexp(-1, keepdim=True)
    log_t = log_t - log_t.logsumexp(-1, keepdim=True)
    # Replace excluded infinities before subtraction (0 * NaN is still NaN).
    difference = torch.where(support, log_t, 0.) - torch.where(support, log_s, 0.)
    discrepancy = (log_t.exp() * difference).sum(-1).clamp_min(0)
    compatibility = t.gather(-1, ids_s).exp().sum(-1)
    return {"discrepancy": torch.where(mask, discrepancy, 0.),
            "compatibility": torch.where(mask, compatibility, 0.), "student_candidate_ids": ids_s,
            "union_support": support}


@torch.no_grad()
def calibrate_a2d_scale(discrepancy: Tensor, mask: Tensor, *, percentile: float = 95.) -> Tensor:
    """Freeze the pooled token percentile; never recalibrate inside an update."""
    if not discrepancy.is_floating_point() or discrepancy.shape != mask.shape or mask.dtype != torch.bool or discrepancy.device != mask.device:
        raise ValueError("aligned token discrepancy and Boolean mask required")
    if not bool(mask.any()) or not bool(torch.isfinite(discrepancy[mask]).all()) or bool((discrepancy[mask] < 0).any()):
        raise ValueError("nonempty finite nonnegative calibration values required")
    if not math.isfinite(percentile) or not 0 <= percentile <= 100:
        raise ValueError("percentile must be in [0,100]")
    return torch.quantile(discrepancy[mask].double(), percentile / 100).to(discrepancy.dtype)


@torch.no_grad()
def a2d_question_reward(student_logits: Tensor, teacher_logits: Tensor, mask: Tensor,
                        cluster_shares: Tensor, *, delta_ref: float, top_k: int = 16,
                        response_budget: int = 7168, alpha: float = .5,
                        length_weight: float = .3, diversity_weight: float = 1.,
                        epsilon: float = 1e-8) -> tuple[Tensor, dict]:
    """Eq. 6--11. Cluster shares are supplied, NOT a semantic dedup surrogate.

Callers must compute shares over the FULL scoring batch with the paper's BLEU
average-linkage clustering, not within separate GRPO groups.
    """
    if not all(math.isfinite(v) for v in (delta_ref, alpha, length_weight, diversity_weight, epsilon)):
        raise ValueError("finite reward options required")
    if delta_ref < 0 or not 0 <= alpha <= 1 or not 0 <= length_weight < 1 or diversity_weight < 0 or epsilon <= 0:
        raise ValueError("invalid reward options")
    if isinstance(response_budget, bool) or not isinstance(response_budget, int) or response_budget < 1:
        raise ValueError("positive integer response budget required")
    signal = a2d_token_signal(student_logits, teacher_logits, mask, top_k=top_k)
    if cluster_shares.shape != (mask.shape[0],) or cluster_shares.device != mask.device:
        raise ValueError("one cluster share per response on the same device required")
    if not bool(torch.isfinite(cluster_shares).all()) or bool(((cluster_shares <= 0) | (cluster_shares > 1)).any()):
        raise ValueError("cluster shares must be in (0,1]")
    lengths = mask.sum(-1)
    if bool((lengths > response_budget).any()):
        raise ValueError("response exceeds declared generation budget")
    score = (signal["discrepancy"] / (delta_ref + epsilon)).clamp_max(1) * signal["compatibility"]
    float_lengths = lengths.to(score.dtype)
    length_factor = 1 - length_weight * (float_lengths / response_budget).clamp_max(1)
    diversity_factor = (1 - diversity_weight * cluster_shares.to(score.dtype)).clamp_min(0)
    reward = length_factor * diversity_factor * score.sum(-1) / float_lengths.pow(alpha)
    return reward, {**signal, "token_score": score, "length_factor": length_factor,
                    "diversity_factor": diversity_factor, "reward_detached": True}


def a2d_candidate_opd_loss(current_logits: Tensor, old_logits: Tensor, teacher_logits: Tensor,
                          mask: Tensor, *, top_k: int = 16, clip: float = .2) -> tuple[Tensor, dict]:
    """Eq. 12--15: fixed old-policy candidates/advantages, candidate SUM.

No advantage/group normalization, reference KL anchor, or teacher renormalized
log-probabilities. This is not exact full-vocabulary reverse-KL minimization.
    """
    _aligned(current_logits, old_logits)
    _aligned(current_logits, teacher_logits)
    current = _logits(current_logits, mask).log_softmax(-1)
    old, teacher = _logits(old_logits.detach(), mask).log_softmax(-1), _logits(teacher_logits.detach(), mask).log_softmax(-1)
    _top_k(top_k, current.shape[-1])
    if not math.isfinite(clip) or not 0 <= clip < 1:
        raise ValueError("clip must be in [0,1)")
    ids = old.topk(top_k, -1).indices
    a, b, q = current.gather(-1, ids), old.gather(-1, ids), teacher.gather(-1, ids)
    advantage = (b.softmax(-1) * (q - b)).detach()
    ratio = (a - b).exp()
    if not bool(torch.isfinite(ratio[mask]).all()):
        raise ValueError("policy ratio overflow; smaller update or higher precision required")
    per_token = torch.minimum(ratio * advantage, ratio.clamp(1 - clip, 1 + clip) * advantage).sum(-1)
    loss = -torch.where(mask, per_token, 0.).sum() / mask.sum()
    return loss, {"candidate_ids": ids, "fixed_advantage": advantage, "probability_ratio": ratio,
                  "teacher_detached": True, "old_policy_detached": True}


def minimal_edit_masks(original: Sequence[int], corrected: Sequence[int]) -> tuple[list[bool], list[bool]]:
    """Exact unit-cost token Levenshtein alignment; deterministic ties.

Returns all changed spans, including separated insertions/deletions. This is
alignment of SUPPLIED texts, not a learned minimal-correction projector.
    """
    a, b = list(original), list(corrected)
    n, m = len(a), len(b)
    if (n + 1) * (m + 1) > 1_000_000:
        raise ValueError("bounded diagnostic alignment supports at most one million dynamic-program cells")
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        d[i][0] = i
    for j in range(m + 1):
        d[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            d[i][j] = min(d[i - 1][j - 1] + (a[i - 1] != b[j - 1]), d[i - 1][j] + 1, d[i][j - 1] + 1)
    left, right = [False] * n, [False] * m
    i, j = n, m
    while i or j:
        if i and j and a[i - 1] == b[j - 1] and d[i][j] == d[i - 1][j - 1]:
            i, j = i - 1, j - 1
        elif i and j and d[i][j] == d[i - 1][j - 1] + 1:
            left[i - 1], right[j - 1] = True, True
            i, j = i - 1, j - 1
        elif i and d[i][j] == d[i - 1][j] + 1:
            left[i - 1], i = True, i - 1
        else:
            right[j - 1], j = True, j - 1
    return left, right


def verified_edit_masks(original: Sequence[int], corrected: Sequence[int],
                         verifier: Callable[[Sequence[int]], bool]) -> tuple[list[bool], list[bool]]:
    """Reject already-correct attempts and unverified corrections before pairing."""
    if bool(verifier(original)) or not bool(verifier(corrected)):
        raise ValueError("a failed attempt and independently verified correction required")
    return minimal_edit_masks(original, corrected)


def _sequence(values: Tensor, mask: Tensor, *, allow_empty: bool = False) -> Tensor:
    if values.ndim != 2 or not values.is_floating_point() or values.shape != mask.shape or mask.dtype != torch.bool or values.device != mask.device:
        raise ValueError("aligned floating [batch,token] log-probabilities and Boolean mask required")
    if not allow_empty and not bool(mask.any(1).all()):
        raise ValueError("nonempty active sequence required")
    if not bool(torch.isfinite(values[mask]).all()) or bool((values[mask] > 1e-6).any()):
        raise ValueError("finite nonpositive active log-probabilities required")
    safe = torch.where(mask, values, 0.)
    return safe.float() if safe.dtype in (torch.float16, torch.bfloat16) else safe


def projected_distillation_loss(positive_log_probs: Tensor, negative_log_probs: Tensor,
                                reference_positive: Tensor, reference_negative: Tensor,
                                positive_edit_mask: Tensor, negative_edit_mask: Tensor,
                                *, beta: float = .1, self_correct_log_probs: Tensor | None = None,
                                self_correct_mask: Tensor | None = None) -> tuple[Tensor, dict]:
    """Eq. 1--2: unnormalized changed-span DPO + self-correct (NOT fix) SFT.

Log-probabilities must be computed on each sequence's own complete causal
prefix. Zero gradients on retained gathered log-probs do not mean that shared
model parameters or the retained prefix have no influence on edited tokens.
    """
    _aligned(positive_log_probs, reference_positive)
    _aligned(negative_log_probs, reference_negative)
    if positive_log_probs.shape[0] != negative_log_probs.shape[0] or positive_log_probs.device != negative_log_probs.device or positive_log_probs.dtype != negative_log_probs.dtype:
        raise ValueError("paired batches must share size, device and dtype")
    if not math.isfinite(beta) or beta <= 0:
        raise ValueError("positive finite beta required")
    p = _sequence(positive_log_probs, positive_edit_mask, allow_empty=True)
    n = _sequence(negative_log_probs, negative_edit_mask, allow_empty=True)
    rp = _sequence(reference_positive.detach(), positive_edit_mask, allow_empty=True)
    rn = _sequence(reference_negative.detach(), negative_edit_mask, allow_empty=True)
    if p.shape[0] < 1 or not bool((positive_edit_mask.sum(-1) + negative_edit_mask.sum(-1) > 0).all()):
        raise ValueError("each preference pair must contain an edit")
    margin = (p - rp).sum(-1) - (n - rn).sum(-1)
    contrast = -torch.nn.functional.logsigmoid(beta * margin).mean()
    sft = p.sum() * 0
    if (self_correct_log_probs is None) != (self_correct_mask is None):
        raise ValueError("self-correct probabilities and mask must be supplied together")
    if self_correct_log_probs is not None:
        if self_correct_log_probs.device != p.device or self_correct_log_probs.dtype != positive_log_probs.dtype:
            raise ValueError("self-correct responses must share device and dtype")
        correct = _sequence(self_correct_log_probs, self_correct_mask)
        if correct.shape[0] < 1:
            raise ValueError("omit SFT arguments if there are no self-correct responses")
        sft = -correct.sum(-1).mean()
    return contrast + sft, {"contrast_loss": contrast.detach(), "self_correct_sft_loss": sft.detach(),
                            "pair_margin": margin.detach(), "reference_detached": True,
                            "span_reduction": "sum", "sft_target": "student_own_verified_correct"}
