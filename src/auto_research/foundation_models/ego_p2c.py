"""EgoP2C role upcycling, isolated contexts and segment-level MOPD.

arXiv:2610.22681, Eqs.2/3/10 and Appendix B.2. This is a tiny causal
decoder/operator diagnostic, not a trained video model or spatial benchmark.
"""
from __future__ import annotations

from collections.abc import Sequence
import copy
from dataclasses import dataclass
import math

import torch
from torch import nn

ROLES = ("PC", "V", "G")


def _tokens(values: Sequence[int], *, nonempty: bool = False) -> tuple[int, ...]:
    result = tuple(values)
    if (nonempty and not result) or any(isinstance(x, bool) or not isinstance(x, int) or x < 0 for x in result):
        raise ValueError("nonnegative integer token ids required")
    return result


@dataclass(frozen=True)
class RoleContext:
    role: str
    video: tuple[int, ...]
    text: tuple[int, ...]
    visible_fields: tuple[str, ...]


def role_context(role: str, *, video: Sequence[int], question: Sequence[int] = (),
                 options: Sequence[int] = (), history: Sequence[int] = (),
                 subquestion: Sequence[int] = ()) -> RoleContext:
    """Build an allowlisted information view; no gold/reference-answer argument.

    V cannot receive the original question/options/history; G cannot receive PC
    history or mode text. The caller supplies a self-contained V subquestion.
    """
    if role not in ROLES:
        raise ValueError("role must be PC, V or G")
    video = _tokens(video, nonempty=True)
    question, options, history, subquestion = map(_tokens, (question, options, history, subquestion))
    if role == "V":
        if question or options or history or not subquestion:
            raise ValueError("Perception receives video and subquestion only")
        return RoleContext(role, video, subquestion, ("video", "subquestion"))
    if subquestion or not question or (role == "G" and history):
        raise ValueError("PC/G requires original question; G excludes private history")
    fields = ("video", "question", "options", "history") if role == "PC" else ("video", "question", "options")
    # Fixed separators belong to the synthetic recipe, not paper-specific tokens.
    text = question + ((1,) + options if options else ()) + ((1,) + history if history else ())
    return RoleContext(role, video, text, fields)


class RoleLinear(nn.Module):
    def __init__(self, dim: int, rank: int):
        super().__init__()
        self.base = nn.Linear(dim, dim, bias=False)
        self.base.requires_grad_(False)
        self.a = nn.ParameterDict({r: nn.Parameter(torch.randn(rank, dim) / math.sqrt(dim)) for r in ROLES})
        self.b = nn.ParameterDict({r: nn.Parameter(torch.zeros(dim, rank)) for r in ROLES})
        self.general_enabled = False
        self.a["G"].requires_grad_(False)
        self.b["G"].requires_grad_(False)

    def forward(self, x: torch.Tensor, role: str, prefix_length: int) -> torch.Tensor:
        base = self.base(x)
        if role == "G" and not self.general_enabled:
            return base
        residual = (x[prefix_length:] @ self.a[role].T) @ self.b[role].T
        return torch.cat((base[:prefix_length], base[prefix_length:] + residual), 0)


class RoleDecoder(nn.Module):
    """One-block causal role decoder with copied FFNs and q/k/v/o residuals.

    Synthetic video *token ids*, not a vision encoder. The common video prefix
    always uses frozen base projections and General FFN, independent of role.
    """

    def __init__(self, vocab: int = 32, dim: int = 12, hidden: int = 20, rank: int = 2):
        super().__init__()
        if any(isinstance(x, bool) or not isinstance(x, int) or x < 1 for x in (vocab, dim, hidden, rank)) or vocab < 4:
            raise ValueError("positive integer dimensions and vocab>=4 required")
        self.embedding = nn.Embedding(vocab, dim).requires_grad_(False)
        self.norm1, self.norm2 = nn.LayerNorm(dim), nn.LayerNorm(dim)
        self.norm1.requires_grad_(False)
        self.norm2.requires_grad_(False)
        self.q, self.k, self.v, self.o = (RoleLinear(dim, rank) for _ in range(4))
        ffn = nn.Sequential(nn.Linear(dim, hidden), nn.GELU(), nn.Linear(hidden, dim))
        self.experts = nn.ModuleDict({r: copy.deepcopy(ffn) for r in ROLES})
        self.experts["G"].requires_grad_(False)
        self.head = nn.Linear(dim, vocab, bias=False).requires_grad_(False)

    def enable_general_residual(self) -> None:
        for layer in (self.q, self.k, self.v, self.o):
            layer.general_enabled = True
            layer.a["G"].requires_grad_(True)
            layer.b["G"].requires_grad_(True)

    def forward(self, context: RoleContext, continuation: Sequence[int] = ()) -> torch.Tensor:
        if context.role not in ROLES or not context.video or not context.text:
            raise ValueError("valid nonempty role context required")
        ids = _tokens(context.video + context.text + _tokens(continuation), nonempty=True)
        if max(ids) >= self.embedding.num_embeddings:
            raise ValueError("token outside vocabulary")
        tokens = torch.tensor(ids, device=self.embedding.weight.device)
        x = self.embedding(tokens)
        normalized = self.norm1(x)
        n = len(context.video)
        q, k, v = (layer(normalized, context.role, n) for layer in (self.q, self.k, self.v))
        logits = q @ k.T / math.sqrt(q.shape[-1])
        causal = torch.ones_like(logits, dtype=torch.bool).triu(1)
        attention = logits.masked_fill(causal, -torch.inf).softmax(-1) @ v
        x = x + self.o(attention, context.role, n)
        norm = self.norm2(x)
        ffn = torch.cat((self.experts["G"](norm[:n]), self.experts[context.role](norm[n:])), 0)
        return self.head(x + ffn)


@dataclass(frozen=True)
class SampledSegment:
    context: RoleContext
    tokens: tuple[int, ...]
    rollout_log_probs: torch.Tensor


@torch.no_grad()
def sample_segment(model: RoleDecoder, context: RoleContext, *, steps: int,
                   generator: torch.Generator | None = None) -> SampledSegment:
    """Fresh on-policy tokens, temperature=1/top-p=1; fixed diagnostic length."""
    if isinstance(steps, bool) or not isinstance(steps, int) or not 1 <= steps <= 64:
        raise ValueError("1..64 diagnostic output tokens required")
    output, log_probs = [], []
    for _ in range(steps):
        logits = model(context, output)[-1]
        token = int(torch.multinomial(logits.softmax(-1), 1, generator=generator))
        log_probs.append(logits.log_softmax(-1)[token])
        output.append(token)
    return SampledSegment(context, tuple(output), torch.stack(log_probs).detach())


def score_segment(model: RoleDecoder, segment: SampledSegment) -> torch.Tensor:
    """Logits for the SAME sampled continuation/context, never teacher generation."""
    if not segment.tokens or segment.rollout_log_probs.shape != (len(segment.tokens),):
        raise ValueError("nonempty sampled segment with aligned old log probabilities required")
    all_logits = model(segment.context, segment.tokens[:-1])
    first = len(segment.context.video) + len(segment.context.text) - 1
    return all_logits[first:first + len(segment.tokens)]


@dataclass(frozen=True)
class SegmentScores:
    role: str
    student_log_probs: torch.Tensor
    teacher_log_probs: torch.Tensor
    rollout_log_probs: torch.Tensor


def segment_mopd_loss(segments: Sequence[SegmentScores], *, clip: float = 5.,
                      role_weights: dict[str, float] | None = None) -> torch.Tensor:
    """Eq.3 for ONE trajectory: normalize each role over all of its segments.

    Old-policy/teacher scores and clipped advantages are detached. This is a
    local fixed-snapshot reverse-KL surrogate, not exact full-trajectory KL.
    """
    weights = {r: 1. for r in ROLES} if role_weights is None else role_weights
    if set(weights) != set(ROLES) or any(not math.isfinite(w) or w < 0 for w in weights.values()):
        raise ValueError("finite nonnegative weight for every role required")
    if not segments or not math.isfinite(clip) or clip <= 0:
        raise ValueError("nonempty segments and positive finite clipping bound required")
    counts = {r: 0 for r in ROLES}
    sample = segments[0].student_log_probs
    for segment in segments:
        values = (segment.student_log_probs, segment.teacher_log_probs, segment.rollout_log_probs)
        if segment.role not in ROLES or sample.ndim != 1 or not segment.student_log_probs.numel():
            raise ValueError("valid role and nonempty one-dimensional scores required")
        if any(v.shape != values[0].shape or v.ndim != 1 or not v.is_floating_point() or v.dtype != sample.dtype or v.device != sample.device or not bool(torch.isfinite(v).all()) for v in values):
            raise ValueError("finite aligned same-device/dtype score vectors required")
        counts[segment.role] += segment.student_log_probs.numel()
    loss = sample.sum() * 0
    for segment in segments:
        advantage = (segment.teacher_log_probs.detach() - segment.rollout_log_probs.detach()).clamp(-clip, clip)
        loss = loss - weights[segment.role] * (advantage * segment.student_log_probs).sum() / counts[segment.role]
    return loss
