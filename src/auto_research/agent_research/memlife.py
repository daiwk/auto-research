"""Independently derived CPU FIRM arithmetic and causal access, arXiv:2609.40195v1.

L1 input-array mechanism only: no video model, writer/reader, judge, answers,
trainer, filesystem, API or checkpoint. The published Meta source is a reference,
not copied implementation. Eq.11 uses macro candidate statistics around the
group mean; B.4 clips, token-recenters each group, then globally whitens.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
import math

import numpy as np

REQUIRES_GPU_VALIDATION = False
MAX_REWARD_TOKENS = 65_536
MAX_ENTRIES = 512


def _finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _field(values, mask):
    array = np.asarray(values, dtype=np.float64)
    selected = np.asarray(mask)
    if array.ndim != 2 or not array.shape[0] or not array.shape[1] or array.size > MAX_REWARD_TOKENS:
        raise ValueError("bounded nonempty [candidate,token] reward field required")
    if selected.dtype != np.bool_ or selected.shape != array.shape:
        raise ValueError("same-shape boolean response mask required")
    if not np.isfinite(array).all():
        raise ValueError("reward inputs, including padding, must be finite")
    return array, selected


def faithfulness_from_probabilities(observed, best, response_mask) -> np.ndarray:
    """Eq.7 using supplied evaluator probabilities, not an implemented evaluator."""
    observed, mask = _field(observed, response_mask)
    best = np.asarray(best, dtype=np.float64)
    if best.shape != observed.shape or not np.isfinite(best).all() or np.any(
            (observed < 0) | (observed > 1) | (best < observed) | (best > 1)):
        raise ValueError("probabilities require 0 <= observed <= best <= 1")
    return np.where(mask, 1 - (best - observed), 0.0)


def firm_reward(faith, informativeness, retrievability, response_mask) -> np.ndarray:
    """Eq.10 product; no summed scalar fallback and no KL in rewards."""
    faith, mask = _field(faith, response_mask)
    inf = np.asarray(informativeness, dtype=np.float64)
    ret = np.asarray(retrievability, dtype=np.float64)
    if inf.shape != (faith.shape[0],) or ret.shape != inf.shape:
        raise ValueError("one informativeness and retrievability scalar per candidate required")
    if (not np.isfinite(inf).all() or not np.isfinite(ret).all() or np.any((faith < 0) | (faith > 1))
            or np.any((inf < 0) | (inf > 1) | (ret < 0) | (ret > 1))):
        raise ValueError("explicit FIRM inputs must be probabilities in [0,1]")
    return np.where(mask, faith * inf[:, None] * ret[:, None], 0.0)


def group_relative_advantage(rewards, response_mask, group_ids: Sequence[str], *,
                             normalization_epsilon: float = 1e-6, clip: float = 3.0,
                             whitening_epsilon: float = 1e-8) -> dict:
    """Eq.11--12 and B.4; NumPy float64, sample-variance global whitening.

    Empty candidates do not enter the macro group statistics. Empty groups stay
    zero. With fewer than two response tokens, global whitening is undefined and
    rejected rather than silently changing its sample-variance convention.
    """
    x, mask = _field(rewards, response_mask)
    if np.any((x[mask] < 0) | (x[mask] > 1)):
        raise ValueError("valid FIRM response-token rewards must lie in [0,1]")
    # Padding is finite but has no reward semantics. Erase it before arithmetic,
    # so even extreme finite placeholders cannot overflow a masked deviation.
    x = np.where(mask, x, 0.0)
    if any(not _finite(v) or v <= 0 for v in (normalization_epsilon, clip, whitening_epsilon)):
        raise ValueError("finite positive normalization constants required")
    if len(group_ids) != x.shape[0] or any(not isinstance(g, str) or not g.strip() for g in group_ids):
        raise ValueError("one named segment-group id per candidate required")
    token_count = int(mask.sum())
    if token_count < 2:
        raise ValueError("global sample-variance whitening requires at least two response tokens")
    groups = {g: [i for i, row_g in enumerate(group_ids) if row_g == g] for g in dict.fromkeys(group_ids)}
    raw = np.zeros_like(x)
    clipped = np.zeros_like(x)
    centered = np.zeros_like(x)
    means, variances = {}, {}
    for group, rows in groups.items():
        selected = mask[rows]
        lengths = selected.sum(axis=1)
        live = lengths > 0
        if not live.any():
            means[group] = variances[group] = 0.0
            continue
        vals = x[rows]
        candidate_means = np.where(selected, vals, 0.0).sum(axis=1)[live] / lengths[live]
        mu = float(candidate_means.mean())
        # Crucially not deviations around each candidate's own mean.
        candidate_dev2 = np.where(selected, (vals - mu) ** 2, 0.0).sum(axis=1)[live] / lengths[live]
        variance = float(candidate_dev2.mean())
        means[group], variances[group] = mu, variance
        z = (vals - mu) / (math.sqrt(variance) + normalization_epsilon)
        raw[rows] = np.where(selected, z, 0.0)
        limited = np.where(selected, np.clip(z, -clip, clip), 0.0)
        clipped[rows] = limited
        # Pooled response-token mean, not the macro mean used in Eq.11.
        center = float(limited[selected].mean())
        centered[rows] = np.where(selected, limited - center, 0.0)
    global_mean = float(centered[mask].mean())
    global_variance = float(centered[mask].var(ddof=1))
    advantages = np.where(mask, (centered - global_mean) / math.sqrt(global_variance + whitening_epsilon), 0.0)
    if not np.isfinite(advantages).all():
        raise ValueError("nonfinite normalized advantages")
    return {"raw": raw, "clipped": clipped, "centered": centered, "advantages": advantages,
            "group_means": means, "group_variances": variances,
            "global_mean": global_mean, "global_variance": global_variance,
            "global_variance_correction": 1}


def memopt_loss(probability_ratios, advantages, kl_estimates, response_mask, *,
                policy_clip: float = 0.2, beta: float = 0.01) -> float:
    """Eq.16 arithmetic on supplied quantities; no policy or KL estimator exists here."""
    ratios, mask = _field(probability_ratios, response_mask)
    advantage = np.asarray(advantages, dtype=np.float64)
    kl = np.asarray(kl_estimates, dtype=np.float64)
    if (advantage.shape != ratios.shape or kl.shape != ratios.shape
            or not np.isfinite(advantage).all() or not np.isfinite(kl).all()
            or np.any(ratios[mask] <= 0) or not mask.any()):
        raise ValueError("finite same-shaped advantages/KL and positive valid probability ratios required")
    if not _finite(policy_clip) or not 0 < policy_clip < 1 or not _finite(beta) or beta < 0:
        raise ValueError("policy clip in (0,1) and nonnegative KL coefficient required")
    try:
        with np.errstate(over="raise", invalid="raise"):
            clipped = np.clip(ratios, 1 - policy_clip, 1 + policy_clip)
            surrogate = np.minimum(ratios * advantage, clipped * advantage)
            penalty = beta * kl
            terms = surrogate - penalty
            loss = -float(terms[mask].mean())
    except FloatingPointError as error:
        raise ValueError("nonfinite MemOpt objective intermediate") from error
    if not np.isfinite(surrogate).all() or not np.isfinite(penalty).all() or not np.isfinite(terms).all() or not math.isfinite(loss):
        raise ValueError("nonfinite MemOpt objective or intermediate")
    return loss


@dataclass(frozen=True)
class MemoryEntry:
    entry_id: str
    subject: str
    start: float
    end: float
    text: str
    embedding: tuple[float, ...]

    def __post_init__(self):
        if any(not isinstance(v, str) or not v.strip() for v in (self.entry_id, self.subject, self.text)):
            raise ValueError("named entry, subject and explicit memory text required")
        if not _finite(self.start) or not _finite(self.end) or not 0 <= self.start <= self.end:
            raise ValueError("finite ordered nonnegative source interval required")
        if not isinstance(self.embedding, tuple) or not self.embedding or any(not _finite(v) for v in self.embedding):
            raise ValueError("immutable explicit unit embedding required")
        if not math.isclose(math.fsum(v * v for v in self.embedding), 1.0, rel_tol=1e-7, abs_tol=1e-7):
            raise ValueError("normalized unit embedding required; no encoder is provided")


def eligible_memories(entries: Sequence[MemoryEntry], *, subject: str, query_time: float,
                      interval: tuple[float, float] | None = None) -> tuple[MemoryEntry, ...]:
    """Eq.3 causal cutoff, with explicit single-subject and full-containment policy.

    Single-subject filtering is a local isolation contract, not the paper's mixed
    cross-subject LVQA benchmark. It does not authenticate a caller's identity.
    """
    if len(entries) > MAX_ENTRIES or any(not isinstance(e, MemoryEntry) for e in entries):
        raise ValueError("bounded typed entries required")
    if len({e.entry_id for e in entries}) != len(entries):
        raise ValueError("unique entry identifiers required")
    if not isinstance(subject, str) or not subject.strip() or not _finite(query_time) or query_time < 0:
        raise ValueError("explicit subject and nonnegative query timestamp required")
    lower, upper = 0.0, query_time
    if interval is not None:
        if len(interval) != 2 or not all(_finite(x) for x in interval) or not 0 <= interval[0] <= interval[1]:
            raise ValueError("ordered finite requested interval required")
        lower, upper = interval[0], min(interval[1], query_time)
    selected = [e for e in entries if e.subject == subject and e.end <= query_time
                and e.start >= lower and e.end <= upper]
    return tuple(sorted(selected, key=lambda e: (e.start, e.end, e.entry_id)))


def fetch_memory(entries: Sequence[MemoryEntry], *, subject: str, query_time: float,
                 interval: tuple[float, float], limit: int = 64) -> tuple[MemoryEntry, ...]:
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 64:
        raise ValueError("fetch budget must be between1and64 entries")
    return eligible_memories(entries, subject=subject, query_time=query_time, interval=interval)[:limit]


def search_memory(entries: Sequence[MemoryEntry], query_embedding: tuple[float, ...], *,
                  subject: str, query_time: float, interval: tuple[float, float] | None = None,
                  limit: int = 32) -> tuple[MemoryEntry, ...]:
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 32:
        raise ValueError("search budget must be between1and32 entries")
    # Reuse unit-vector validation without a model or any answer field.
    probe = MemoryEntry("query", subject, 0, 0, "explicit vector", query_embedding)
    candidates = eligible_memories(entries, subject=subject, query_time=query_time, interval=interval)
    if any(len(e.embedding) != len(probe.embedding) for e in candidates):
        raise ValueError("query and eligible memory embedding dimensions must match")
    ranked = sorted(candidates, key=lambda e: (-math.fsum(a * b for a, b in zip(e.embedding, query_embedding, strict=True)), e.start, e.entry_id))[:limit]
    return tuple(sorted(ranked, key=lambda e: (e.start, e.end, e.entry_id)))


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("CPU-only mechanism; no CUDA path advertised")
    mask = np.array([[True, False, False], [True, True, True]])
    faith = np.array([[1., 0., 0.], [0., 0., 0.]])
    reward = firm_reward(faith, [1, 1], [1, 1], mask)
    result = group_relative_advantage(reward, mask, ["segment", "segment"])
    flat = group_relative_advantage(np.ones((2, 2)), np.ones((2, 2), dtype=bool), ["a", "a"])
    entries = (MemoryEntry("past", "a", 0, 5, "explicit prior observation", (1., 0.)),
               MemoryEntry("future", "a", 5, 6, "future observation", (1., 0.)),
               MemoryEntry("private", "b", 0, 5, "other subject", (1., 0.)))
    visible = search_memory(entries, (1., 0.), subject="a", query_time=5)
    invalid_reward_rejected = objective_overflow_rejected = False
    try:
        group_relative_advantage([[1e200, -1e200]], np.array([[True, True]]), ["g"])
    except ValueError:
        invalid_reward_rejected = True
    try:
        memopt_loss([[1e308, 1]], [[-10, 1]], [[0, 0]], np.array([[True, True]]))
    except ValueError:
        objective_overflow_rejected = True
    return {"seed": seed, "device": device, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"group_mean": result["group_means"]["segment"],
                        "group_variance": result["group_variances"]["segment"],
                        "eligible_entries": len(visible), "response_tokens": int(mask.sum())},
            "checks": {"candidate_macro_not_token_pool": math.isclose(result["group_means"]["segment"], .5),
                       "group_centered_deviation": math.isclose(result["group_variances"]["segment"], .25),
                       "token_mask_recenter": bool(abs(result["centered"][mask].sum()) < 1e-12),
                       "padding_zero": bool(np.all(result["advantages"][~mask] == 0)),
                       "flat_group_zero": bool(np.all(flat["advantages"] == 0)),
                       "zero_dimension_gates_product": bool(np.all(firm_reward(np.ones((2, 2)), [1, 1], [0, 0], np.ones((2, 2), dtype=bool)) == 0)),
                       "out_of_range_reward_rejected": invalid_reward_rejected,
                       "finite_input_objective_overflow_rejected": objective_overflow_rejected,
                       "causal_and_subject_filter": tuple(e.entry_id for e in visible) == ("past",),
                       "fetch_interval_contains_segment": tuple(e.entry_id for e in fetch_memory(entries, subject="a", query_time=5, interval=(0, 100))) == ("past",)}}
