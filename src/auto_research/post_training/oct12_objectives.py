"""October 9 paper operators; unit tests are mechanism, not capability evidence."""
from __future__ import annotations

from dataclasses import dataclass
import math
import unicodedata

import torch


def actor_loss(current, old, advantage, mask, *, sequence_mean=False, epsilon=.2):
    ratio = (current - old.detach()).exp()
    credit = advantage.detach()
    token = -torch.minimum(ratio * credit, ratio.clamp(1-epsilon, 1+epsilon) * credit)
    if sequence_mean:
        return ((token * mask).sum(-1) / mask.sum(-1).clamp_min(1)).mean()
    return (token * mask).sum() / mask.sum().clamp_min(1)


def rank_normalize(values):
    """Average ranks, including ties; constant vectors have no preference."""
    if values.numel() < 2:
        return torch.zeros_like(values)
    comparison = values[:, None] - values[None, :]
    rank = (comparison > 0).sum(1) + ((comparison == 0).sum(1)-1)/2
    return rank.to(values.dtype) / (values.numel()-1)


def branch_forks(logits, student_logp, teacher_logp, eligible, *, budget=3,
                 alpha=.5, window=128, min_gap=1):
    """BranchOPD top-20 entropy + local disagreement rank selector, Eq. 6."""
    if logits.ndim != 2 or logits.shape[0] != len(student_logp):
        raise ValueError("one response and matching token scores required")
    if budget < 0 or window < 1 or min_gap < 1 or not 0 <= alpha <= 1:
        raise ValueError("invalid branch budget/selector")
    log_distribution = logits.detach().log_softmax(-1)
    top = log_distribution.topk(min(20, logits.shape[-1]), -1).values
    entropy = -(top.exp() * top).sum(-1)
    gap = student_logp.detach() - teacher_logp.detach()
    disagreement = torch.stack([gap[max(0,i-window//2):min(len(gap),i+(window+1)//2)].mean()
                                for i in range(len(gap))])
    score = alpha * rank_normalize(entropy) + (1-alpha) * rank_normalize(disagreement)
    selected = []
    for i in torch.argsort(score, descending=True, stable=True).tolist():
        if eligible[i] and all(abs(i-j) >= min_gap for j in selected):
            selected.append(i)
            if len(selected) == budget:
                break
    if budget == 0:
        selected = []
    return sorted(selected), score, entropy


def branch_loss(current, old, teacher, mask):
    credit = (teacher.clamp_min(-10) - current.detach().clamp_min(-10)).clamp(-10, 10)
    return actor_loss(current, old, credit, mask)


def protocol_boundary_loss(logits, constraints):
    """Eq. 12: (prediction index, token set, positive/negative) constraints."""
    if not constraints:
        return logits.sum() * 0
    losses = []
    probabilities = logits.float().softmax(-1)
    for position, token_set, positive in constraints:
        if not token_set or len(set(token_set)) == logits.shape[-1]:
            raise ValueError("protocol set must be nonempty and proper")
        mass = probabilities[position, list(token_set)].sum().clamp(1e-7, 1-1e-7)
        losses.append(-mass.log() if positive else -torch.log1p(-mass))
    return torch.stack(losses).mean()


def normalized_text(text):
    normalized = unicodedata.normalize("NFKC", text).replace("▁", " ").replace("Ġ", " ")
    return " ".join(normalized.split())


def decoded_alignment(student_ids, teacher_ids, student_decode, teacher_decode,
                      *, max_chunk_tokens=32):
    """DPCA two-pointer matching of actual decoded contiguous token spans.

    Failed/oversized matches remain unaligned. Whole-span decoding handles byte
    fragments. No equal-ID/equal-vocab-size shortcut is used.
    """
    if max_chunk_tokens < 1:
        raise ValueError("positive alignment limit required")
    chunks = []
    i = j = 0
    while i < len(student_ids) and j < len(teacher_ids):
        si, tj = i + 1, j + 1
        while True:
            left = normalized_text(student_decode(student_ids[i:si]))
            right = normalized_text(teacher_decode(teacher_ids[j:tj]))
            reliable = left and "\ufffd" not in left and "\ufffd" not in right
            if left == right and reliable:
                chunks.append((tuple(range(i, si)), tuple(range(j, tj))))
                i, j = si, tj
                break
            if si-i >= max_chunk_tokens or tj-j >= max_chunk_tokens:
                i, j = si, tj
                break
            if len(left) <= len(right) and si < len(student_ids):
                si += 1
            elif tj < len(teacher_ids):
                tj += 1
            else:
                i, j = si, tj
                break
    return chunks


def project_teacher_scores(student_count, teacher_scores, alignment):
    projected = teacher_scores.new_zeros(student_count)
    aligned = torch.zeros(student_count, dtype=torch.bool, device=teacher_scores.device)
    for students, teachers in alignment:
        projected[list(students)] = teacher_scores[list(teachers)].sum() / len(students)
        aligned[list(students)] = True
    return projected, aligned


def credit_chunks(aligned, size=6):
    if size < 1:
        raise ValueError("positive credit chunk size required")
    chunks, pending = [], []
    for i, valid in enumerate(aligned.tolist()):
        if not valid and pending:
            chunks.append(pending)
            pending = []
        if valid:
            pending.append(i)
            if len(pending) == size:
                chunks.append(pending)
                pending = []
    if pending:
        chunks.append(pending)
    return chunks


def cast_credit(student_logp, projected_teacher, entropy, chunks):
    """CAST uncertainty * inverse smoothness, preserving chunk advantage."""
    result = torch.zeros_like(student_logp)
    weights = torch.zeros_like(student_logp)
    for indices in chunks:
        q = projected_teacher[indices].detach()
        delta = torch.zeros_like(q)
        if len(indices) > 1:
            adjacent = (q[1:]-q[:-1]).abs()
            delta[0], delta[-1] = adjacent[0], adjacent[-1]
            if len(indices) > 2:
                delta[1:-1] = (adjacent[:-1]+adjacent[1:])/2
        epsilon = delta.mean().clamp_min(.1)
        raw = entropy[indices].detach().clamp_min(1e-8) / (delta+epsilon)
        weight = raw/raw.sum()
        gap = (q-student_logp[indices].detach()).sum()
        result[indices] = gap * weight
        weights[indices] = weight
    return result.detach(), weights.detach()


def selective_anchor(current, reference, unaligned, *, cap=10.):
    z = reference.detach() - current
    divergence = (z.exp()-z-1).clamp_max(cap)
    return (divergence*unaligned).sum() / unaligned.sum().clamp_min(1)


def road_credit(current, routed, auxiliary, reference, *, temperature=1.,
                strength=.5, minimum=.5, maximum=1.5):
    if temperature <= 0 or not 0 < minimum <= maximum:
        raise ValueError("invalid agreement gate")
    evidence = torch.tanh((routed-reference)/temperature)
    peer = torch.tanh((auxiliary-reference)/temperature)
    agreement = evidence * peer if peer.shape == evidence.shape else (evidence[None]*peer).mean(0)
    coefficient = (1+strength*agreement).clamp(minimum, maximum)
    advantage = coefficient*(routed-reference) - (current.detach()-reference)
    return advantage.clamp(-10, 10).detach(), coefficient.detach()


def preventive_projection(target, auxiliary, *, retention=.6, original_norm=None):
    """Road Eq. 7-9, per tensor, with a shared ORIGINAL norm floor."""
    if not 0 < retention <= 1:
        raise ValueError("norm retention must lie in (0,1]")
    target_norm2, auxiliary_norm2 = target.double().square().sum(), auxiliary.double().square().sum()
    floor2 = retention**2 * (target_norm2 if original_norm is None else original_norm**2)
    dot = (target.double()*auxiliary.double()).sum()
    if float(dot) >= 0 or float(auxiliary_norm2) <= 1e-20 or float(target_norm2) <= 1e-20:
        return target.clone(), 0.
    component = (dot/auxiliary_norm2).to(target.dtype)*auxiliary
    full = target-component
    full_norm2 = full.double().square().sum()
    if float(full_norm2) >= float(floor2):
        alpha = 1.
    else:
        alpha = 1-math.sqrt(max(0., float((floor2-full_norm2)/component.double().square().sum())))
        alpha = min(1., max(0., alpha))
    return target-alpha*component, alpha


@dataclass(frozen=True)
class BoundaryAssessment:
    question: str
    student_score: float
    expert_score: float
    quality: float
    clear: bool
    answerable: bool
    context_score: float
    completeness: float
    recommended: bool

    def accepted(self, *, expert_min=.65, student_max=.5, gap_min=.2,
                 quality_min=.7, context_min=.7):
        return (self.expert_score >= expert_min and self.student_score < student_max
                and self.expert_score-self.student_score >= gap_min
                and self.quality >= quality_min and self.clear and self.answerable
                and self.context_score >= context_min)


def boundary_selection(assessments, previous, *, budget, replay_quota):
    if budget < 1 or not 0 <= replay_quota <= budget:
        raise ValueError("invalid boundary acquisition budget")
    accepted = [item for item in assessments if item.accepted()]
    order = lambda a: (-a.completeness, -int(a.recommended), -a.quality, a.question)
    replay = sorted((a for a in accepted if a.question in previous), key=order)[:replay_quota]
    novel = sorted((a for a in accepted if a.question not in previous), key=order)
    return replay + novel[:budget-len(replay)]
