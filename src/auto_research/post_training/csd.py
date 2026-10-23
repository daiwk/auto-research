"""CSD's cross-tokenizer event construction and differentiable loss (2610.28895).

This is an L1 mathematical component, not a language-model benchmark. Logit row
i must predict observed token i from its *own model's* preceding token history.
Special-token role matching and distributed training are intentionally absent.
"""
from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
import math
import unicodedata

import torch
from torch import Tensor
from torch.nn import functional as F

Decoder = Callable[[Sequence[int]], str]


@dataclass(frozen=True)
class Chunk:
    student_start: int
    student_end: int
    teacher_start: int
    teacher_end: int
    char_start: int
    char_end: int


def _ids(ids: Sequence[int], size: int) -> tuple[int, ...]:
    values = tuple(ids)
    if not values or any(isinstance(i, bool) or not isinstance(i, int) or not 0 <= i < size for i in values):
        raise ValueError("nonempty in-vocabulary integer token IDs required")
    return values


def _verified_text(left: str, right: str) -> bool:
    """App. B's NFC and whitespace checks; support matching stays exact."""
    left, right = unicodedata.normalize("NFC", left), unicodedata.normalize("NFC", right)
    return left == right or "".join(left.split()) == "".join(right.split())


def align_offsets(student_ids: Sequence[int], teacher_ids: Sequence[int],
                  student_offsets: Sequence[tuple[int, int]],
                  teacher_offsets: Sequence[tuple[int, int]],
                  student_decode: Decoder, teacher_decode: Decoder,
                  *, source_text: str | None = None) -> tuple[Chunk, ...]:
    """Find minimal common-boundary chunks, verifying decoded *whole* ranges.

    Offsets are original character offsets, not byte offsets. Zero-width special
    tokens must be removed/matched by role by the caller; they are rejected here.
    source_text is required to accept tokenizer gaps: only omitted whitespace
    may lie between token spans. Without it, gapped chunks are conservatively
    skipped. Unmatched ranges or failed whole-chunk checks contribute no KD.
    """
    if source_text is not None and not isinstance(source_text, str):
        raise ValueError("source_text must be the original character string")

    def boundaries(ids, offsets):
        if len(ids) != len(offsets) or not ids:
            raise ValueError("IDs and nonempty character offsets must align")
        result = {}
        previous = -1
        for i, pair in enumerate(offsets):
            if len(pair) != 2 or any(isinstance(x, bool) or not isinstance(x, int) for x in pair):
                raise ValueError("integer character-offset pairs required")
            a, b = pair
            if not 0 <= a < b or a < previous:
                raise ValueError("positive, nonoverlapping character spans required")
            if source_text is not None and b > len(source_text):
                raise ValueError("character offsets exceed source_text")
            result[a] = i
            result[b] = i + 1
            previous = b
        return result

    sb, tb = boundaries(student_ids, student_offsets), boundaries(teacher_ids, teacher_offsets)
    common = sorted(sb.keys() & tb.keys())
    chunks = []
    for a, b in zip(common, common[1:]):
        si, sj, ti, tj = sb[a], sb[b], tb[a], tb[b]
        if si >= sj or ti >= tj:
            continue
        spans_s, spans_t = student_offsets[si:sj], teacher_offsets[ti:tj]
        if spans_s[0][0] != a or spans_t[0][0] != a or spans_s[-1][1] != b or spans_t[-1][1] != b:
            continue
        gaps = [(x[1], y[0]) for spans in (spans_s, spans_t)
                for x, y in zip(spans, spans[1:]) if x[1] != y[0]]
        if gaps and (source_text is None or any(not source_text[left:right].isspace() for left, right in gaps)):
            continue
        decoded_s = student_decode(student_ids[si:sj])
        decoded_t = teacher_decode(teacher_ids[ti:tj])
        if source_text is not None and (not _verified_text(decoded_s, source_text[a:b])
                                        or not _verified_text(decoded_t, source_text[a:b])):
            continue
        if _verified_text(decoded_s, decoded_t):
            chunks.append(Chunk(si, sj, ti, tj, a, b))
    return tuple(chunks)


def paired_completions(student_chunk: Sequence[int], teacher_chunk: Sequence[int],
                       student_size: int, teacher_size: int,
                       student_decode: Decoder, teacher_decode: Decoder,
                       *, teacher_candidates: Sequence[int] | None = None) -> tuple[tuple[int, int], ...]:
    """Build text-equivalent events, not same-ID or rank-sorted correspondences.

    One:one and one:many/many:one enumerate fixed-prefix final-token alternatives.
    Many:many uses only the observed pair (the paper's default). Ambiguous decoded
    spellings are omitted rather than duplicating an event's probability mass.
    Empty decoded continuations are omitted; special roles need a separate map.
    """
    s, t = _ids(student_chunk, student_size), _ids(teacher_chunk, teacher_size)
    allowed = set(range(teacher_size) if teacher_candidates is None else teacher_candidates)
    if any(isinstance(v, bool) or not isinstance(v, int) or not 0 <= v < teacher_size for v in allowed):
        raise ValueError("teacher candidate IDs out of range")
    if len(s) > 1 and len(t) > 1:
        return ((s[-1], t[-1]),) if t[-1] in allowed and student_decode(s) == teacher_decode(t) else ()

    def unique_text(prefix, size, decode, candidates):
        texts: dict[str, list[int]] = {}
        for token in candidates:
            text = decode((*prefix, token))
            if text:
                texts.setdefault(text, []).append(token)
        return {text: ids[0] for text, ids in texts.items() if len(ids) == 1}

    # The prefix is the observed prefix, not a newly sampled/re-tokenized string.
    sm = unique_text(s[:-1], student_size, student_decode, range(student_size))
    tm = unique_text(t[:-1], teacher_size, teacher_decode, sorted(allowed))
    return tuple(sorted(((sm[text], tm[text]) for text in sm.keys() & tm.keys())))


def event_distribution(logits: Tensor, observed_ids: Sequence[int], final_ids: Sequence[int]) -> Tensor:
    """Eq. 1 chain probability for fixed prefixes, plus unrenormalized REST mass."""
    if logits.ndim != 2 or min(logits.shape) < 1 or not logits.is_floating_point() or not bool(torch.isfinite(logits).all()):
        raise ValueError("finite floating [chunk_tokens,vocabulary] logits required")
    observed = _ids(observed_ids, logits.shape[1])
    if len(observed) != len(logits):
        raise ValueError("one prediction row per observed token required")
    selected = tuple(final_ids)
    if not selected:
        return logits.sum().reshape(1) * 0 + 1
    _ids(selected, logits.shape[1])
    if len(set(selected)) != len(selected):
        raise ValueError("explicit events need distinct final token IDs")
    work = logits.float() if logits.dtype in (torch.float16, torch.bfloat16) else logits
    lp = work.log_softmax(-1)
    prefix = lp.new_zeros(())
    for row, token in enumerate(observed[:-1]):
        prefix = prefix + lp[row, token]
    log_q = prefix + lp[-1, list(selected)]
    q = log_q.exp()
    # All candidate chains share their prefix and have different last tokens.
    rest = (-torch.expm1(torch.logsumexp(log_q, 0).clamp_max(0))).reshape(1)
    return torch.cat((q, rest))


def divergence(teacher: Tensor, student: Tensor, kind: str = "jsd") -> Tensor:
    """A single selected divergence across every chunk shape; teacher is frozen."""
    if teacher.shape != student.shape or teacher.ndim != 1 or not len(teacher):
        raise ValueError("aligned event distributions required")
    teacher = teacher.detach()
    tiny = torch.finfo(student.dtype).tiny

    def kl(p, q):
        return (p * (p.clamp_min(tiny).log() - q.clamp_min(tiny).log())).sum()

    if kind == "forward_kl":
        return kl(teacher, student)
    if kind == "reverse_kl":
        return kl(student, teacher)
    if kind == "jsd":
        mixture = (student + teacher) / 2
        return (kl(teacher, mixture) + kl(student, mixture)) / 2
    raise ValueError("kind must be jsd, forward_kl or reverse_kl")


def common_support_loss(student_logits: Tensor, teacher_logits: Tensor,
                        student_ids: Sequence[int], teacher_ids: Sequence[int],
                        chunks: Sequence[Chunk], student_decode: Decoder, teacher_decode: Decoder,
                        *, beta: float = 5., kind: str = "jsd",
                        teacher_top_k: int | None = None) -> tuple[Tensor, dict]:
    """Algorithm 1 KD + CE with detached batch-loss scaling.

    Top-k changes explicit support, never the full-vocabulary softmax normalizer.
    The denominator counts accepted chunks, not their sum of weights. Logit rows
    already point to causal predictor positions; this API performs no shifting.
    """
    if not math.isfinite(beta) or beta < 0:
        raise ValueError("finite nonnegative non-one-to-one weight required")
    if student_logits.ndim != 2 or teacher_logits.ndim != 2 or student_logits.device != teacher_logits.device:
        raise ValueError("two [token,vocabulary] logit arrays on the same device required")
    s, t = _ids(student_ids, student_logits.shape[1]), _ids(teacher_ids, teacher_logits.shape[1])
    if len(s) != len(student_logits) or len(t) != len(teacher_logits):
        raise ValueError("IDs and predictor rows must align")
    if not student_logits.is_floating_point() or not teacher_logits.is_floating_point() or not bool(torch.isfinite(student_logits).all()) or not bool(torch.isfinite(teacher_logits).all()):
        raise ValueError("finite floating logits required")
    if kind not in {"jsd", "forward_kl", "reverse_kl"}:
        raise ValueError("unsupported divergence")
    if teacher_top_k is not None and (isinstance(teacher_top_k, bool) or not isinstance(teacher_top_k, int) or not 1 <= teacher_top_k <= teacher_logits.shape[1]):
        raise ValueError("teacher top-k must be in [1, teacher vocabulary]")
    losses, audit = [], []
    previous_s = previous_t = 0
    for c in chunks:
        if not isinstance(c, Chunk) or not 0 <= c.student_start < c.student_end <= len(s) or not 0 <= c.teacher_start < c.teacher_end <= len(t):
            raise ValueError("nonempty in-range chunks required")
        if c.student_start < previous_s or c.teacher_start < previous_t:
            raise ValueError("chunks must be ordered and nonoverlapping")
        previous_s, previous_t = c.student_end, c.teacher_end
        sc, tc = s[c.student_start:c.student_end], t[c.teacher_start:c.teacher_end]
        if not _verified_text(student_decode(sc), teacher_decode(tc)):
            raise ValueError("chunk decoder texts do not align")
        candidates = None if teacher_top_k is None else teacher_logits[c.teacher_end - 1].detach().topk(teacher_top_k).indices.tolist()
        pairs = paired_completions(sc, tc, student_logits.shape[1], teacher_logits.shape[1], student_decode, teacher_decode, teacher_candidates=candidates)
        if not pairs:
            continue
        ps = event_distribution(student_logits[c.student_start:c.student_end], sc, [u for u, _ in pairs])
        pt = event_distribution(teacher_logits[c.teacher_start:c.teacher_end].detach(), tc, [v for _, v in pairs])
        one_to_one = len(sc) == len(tc) == 1
        losses.append((1. if one_to_one else beta) * divergence(pt, ps, kind))
        audit.append({"pairs": pairs, "student": ps, "teacher": pt, "one_to_one": one_to_one})
    ce = F.cross_entropy(student_logits, torch.tensor(s, dtype=torch.long, device=student_logits.device))
    kd = torch.stack(losses).sum() / len(losses) if losses else student_logits.sum() * 0
    scale = (ce / kd).detach() if bool(kd.detach() > 0) else kd.detach() * 0
    return ce + scale * kd, {"ce": ce, "kd": kd, "scale": scale, "accepted_chunks": len(losses), "events": audit}


def diagnostic(seed: int, device: str = "cpu") -> dict:
    """Three tiny neural updates; no pretrained weights, public benchmark or LLM."""
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("integer seed required")
    dev = torch.device(device)
    if dev.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable; no CPU fallback")
    sv = ("120", "129", "a", "b", "x", "bc", "ab", "c", "0", "9")
    tv = ("1", "2", "0", "9", "ab", "x", "a", "b", "c", "120", "129", "bc")
    s, t = (0, 1, 2, 3, 4, 2, 5), (0, 1, 2, 0, 1, 3, 4, 5, 4, 8)
    so = ((0, 3), (3, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 12))
    to = ((0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 8), (8, 9), (9, 11), (11, 12))
    ds, dt = lambda ids: "".join(sv[i] for i in ids), lambda ids: "".join(tv[i] for i in ids)
    chunks = align_offsets(s, t, so, to, ds, dt)
    # Fixed full-prefix text views use different token IDs/segmentations. The tiny
    # conditional models use the previous token only (a restricted Markov LM).
    with torch.random.fork_rng():
        torch.manual_seed(seed)
        student = torch.nn.Sequential(torch.nn.Embedding(len(sv) + 1, 8), torch.nn.Linear(8, len(sv))).to(device=dev, dtype=torch.float64)
        teacher = torch.nn.Sequential(torch.nn.Embedding(len(tv) + 1, 8), torch.nn.Linear(8, len(tv))).to(device=dev, dtype=torch.float64)
    teacher.requires_grad_(False)
    xs = torch.tensor((len(sv), *s[:-1]), device=dev)
    xt = torch.tensor((len(tv), *t[:-1]), device=dev)
    initial = torch.cat([p.detach().flatten().clone() for p in student.parameters()])
    optimizer = torch.optim.SGD(student.parameters(), lr=.03)
    loss_error = grad_error = norm_error = 0.
    no_chain_gap = no_rest_gap = 0.
    for _ in range(3):
        optimizer.zero_grad(set_to_none=True)
        sl, tl = student(xs), teacher(xt)
        total, audit = common_support_loss(sl, tl, s, t, chunks, ds, dt)
        # Independent dense-probability/product reference. Explicit event IDs
        # come from decoder matching; this path does not call event_distribution.
        ref_sl = sl.detach().clone().requires_grad_()
        sp, tp = ref_sl.softmax(-1), tl.detach().softmax(-1)
        reference, no_chain, no_rest = [], [], []
        for c, item in zip(chunks, audit["events"]):
            sprefix = sp.new_ones(())
            tprefix = tp.new_ones(())
            for row in range(c.student_start, c.student_end - 1):
                sprefix = sprefix * sp[row, s[row]]
            for row in range(c.teacher_start, c.teacher_end - 1):
                tprefix = tprefix * tp[row, t[row]]
            qs = torch.stack([sprefix * sp[c.student_end - 1, u] for u, _ in item["pairs"]])
            qt = torch.stack([tprefix * tp[c.teacher_end - 1, v] for _, v in item["pairs"]])
            ps, pt = torch.cat((qs, (1 - qs.sum()).reshape(1))), torch.cat((qt, (1 - qt.sum()).reshape(1)))
            mixture = (ps + pt) / 2
            tiny = torch.finfo(ps.dtype).tiny
            value = sum((p * (p.clamp_min(tiny).log() - mixture.clamp_min(tiny).log())).sum() for p in (ps, pt)) / 2
            weight = 1 if item["one_to_one"] else 5
            reference.append(weight * value)
            raw_s = sp[c.student_end - 1, [u for u, _ in item["pairs"]]]
            raw_t = tp[c.teacher_end - 1, [v for _, v in item["pairs"]]]
            no_chain.append(weight * divergence(torch.cat((raw_t, (1 - raw_t.sum()).reshape(1))), torch.cat((raw_s, (1 - raw_s.sum()).reshape(1)))))
            no_rest.append(weight * divergence(qt / qt.sum(), qs / qs.sum()))
            norm_error = max(norm_error, abs(float(item["student"].detach().sum()) - 1), abs(float(item["teacher"].sum()) - 1))
        kd_ref = torch.stack(reference).sum() / len(reference)
        ce_ref = -sp[torch.arange(len(s), device=dev), list(s)].log().mean()
        ref = ce_ref + (ce_ref / kd_ref).detach() * kd_ref
        loss_error = max(loss_error, abs(float((total - ref).detach())))
        gradient = torch.autograd.grad(total, sl, retain_graph=True)[0]
        gradient_ref = torch.autograd.grad(ref, ref_sl)[0]
        grad_error = max(grad_error, float((gradient - gradient_ref).abs().max()))
        no_chain_gap = max(no_chain_gap, abs(float(audit["kd"].detach() - torch.stack(no_chain).mean().detach())))
        no_rest_gap = max(no_rest_gap, abs(float(audit["kd"].detach() - torch.stack(no_rest).mean().detach())))
        total.backward()
        optimizer.step()
    final = torch.cat([p.detach().flatten() for p in student.parameters()])
    return {"seed": seed, "metrics": {
        "optimizer_updates": 3, "accepted_chunks": len(chunks),
        "student_vocabulary": len(sv), "teacher_vocabulary": len(tv),
        "loss_reference_error": loss_error, "gradient_reference_error": grad_error,
        "normalization_error": norm_error, "no_chain_negative_gap": no_chain_gap,
        "no_residual_negative_gap": no_rest_gap,
        "student_parameter_delta": float((final - initial).norm()),
        "final_loss": float(total.detach()), "final_kd": float(audit["kd"].detach())},
        "checks": {"three_real_updates": bool((final - initial).norm() > 0),
                   "frozen_teacher": all(p.grad is None for p in teacher.parameters()),
                   "all_four_chunk_shapes": {(c.student_end - c.student_start > 1, c.teacher_end - c.teacher_start > 1) for c in chunks} == {(False, False), (False, True), (True, False), (True, True)},
                   "value_reference_agrees": loss_error < 1e-10,
                   "gradient_reference_agrees": grad_error < 1e-10,
                   "normalized_with_rest": norm_error < 1e-12,
                   "no_chain_negative_control": no_chain_gap > 1e-6,
                   "no_residual_negative_control": no_rest_gap > 1e-6}}
