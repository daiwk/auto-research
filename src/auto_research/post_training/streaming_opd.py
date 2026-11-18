"""Streaming OPD v1 prefix/mask/version and implemented top-k objective.

This is not an asynchronous engine or an observed throughput improvement.
"""

from dataclasses import dataclass
import torch
from ._nov18_contracts import mask, receipt, scalar, seeded, tensor

REQUIRES_GPU_VALIDATION = True


@dataclass(frozen=True)
class Segment:
    prefix: tuple
    loss_mask: tuple[bool, ...]
    generation_versions: tuple[int, ...]
    terminal: bool


def segment(response_prefix, delivered_tokens, generation_versions, *, terminal=False):
    prefix = tuple(response_prefix)
    versions = tuple(generation_versions)
    if type(delivered_tokens) is not int or not 0 <= delivered_tokens < len(prefix):
        raise ValueError("a nonempty newly delivered segment is required")
    if (
        len(versions) != len(prefix)
        or any(type(v) is not int or v < 0 for v in versions)
        or type(terminal) is not bool
    ):
        raise ValueError("actual per-token nonnegative version tags and Boolean terminal required")
    return Segment(
        prefix, tuple(i >= delivered_tokens for i in range(len(prefix))), versions, terminal
    )


def version_lags(sample, consuming_version):
    if type(consuming_version) is not int or consuming_version < max(sample.generation_versions):
        raise ValueError("consuming version predates generation")
    return tuple(consuming_version - v for v in sample.generation_versions)


def topk_loss(student_logits, teacher_logits, token_mask, *, k, log_floor=-20.0, ceiling=10.0):
    tensor(student_logits, "student", ndim=3)
    tensor(teacher_logits, "teacher", shape=student_logits.shape, device=student_logits.device)
    mask(token_mask, student_logits[..., 0])
    if type(k) is not int or not 1 <= k <= student_logits.shape[-1]:
        raise ValueError("k must be a valid vocabulary count")
    floor = scalar(log_floor, "log_floor", upper=0)
    cap = scalar(ceiling, "ceiling", lower=0, strict_lower=True)
    logq, index = teacher_logits.detach().log_softmax(-1).topk(k, -1)
    logp = student_logits.log_softmax(-1).gather(-1, index)
    q, p = logq.clamp_min(floor), logp.clamp_min(floor)
    # Full-vocabulary probabilities are retained: never softmax the top-k slice.
    per_token = (q.exp() * (q - p)).sum(-1).clamp(0, cap)
    return per_token[token_mask].mean(), per_token


def weighted_reduce(losses, weights):
    tensor(losses, "losses")
    tensor(weights, "weights", shape=losses.shape, device=losses.device)
    if bool((weights < 0).any()) or not bool(weights.sum() > 0):
        raise ValueError("nonnegative weights with positive total required")
    return (losses * weights.detach()).sum() / weights.detach().sum()


def diagnostic(seed, device="cpu"):
    g = seeded(seed, device)
    sample = segment([1, 2, 3, 4], 2, [0, 0, 1, 1])
    s = torch.randn(1, 4, 5, generator=g, dtype=torch.float64).to(device).requires_grad_()
    t = torch.randn(1, 4, 5, generator=g, dtype=torch.float64).to(device).requires_grad_()
    m = torch.tensor([sample.loss_mask], device=device)
    out, pt = topk_loss(s, t, m, k=2)
    out.backward()
    qlog, ix = t.detach().log_softmax(-1).topk(2, -1)
    raw = (qlog.exp() * (qlog - s.detach().log_softmax(-1).gather(-1, ix))).sum(-1).clamp(0, 10)
    return receipt(
        seed,
        "l1_mechanism",
        {
            "full_prefix_not_truncated": sample.prefix == (1, 2, 3, 4),
            "sealing_not_eos": sample.terminal is False,
            "old_prefix_zero_loss_gradient": bool((s.grad[~m] == 0).all()),
            "topk_not_renormalized": bool(torch.allclose(pt.detach(), raw)),
            "teacher_frozen": t.grad is None,
            "actual_versions_retained": version_lags(sample, 2) == (2, 2, 1, 1),
        },
        {
            "loss": out.item(),
            "supervised_tokens": int(m.sum()),
            "topk_teacher_mass": float(qlog.exp().sum(-1).mean()),
        },
    )
