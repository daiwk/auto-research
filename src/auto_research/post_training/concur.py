"""CONCUR Eqs.1--7 / Algorithm1: gated advantage projections, not LLM RL.

Pure CPU numerical component. Rewards and the task's declared reward design
are external. Batch whitening's standard-deviation correction is explicit
because Eq.2 does not specify its implementation convention.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from numbers import Real

import numpy as np

REQUIRES_GPU_VALIDATION = False


def _vector(value, *, minimum=2):
    out = np.asarray(value, dtype=np.float64)
    if out.ndim != 1 or len(out) < minimum or not np.isfinite(out).all():
        raise ValueError("nonempty finite one-dimensional numerical input required")
    return out


def standardized(rewards):
    """Eq.1: sample standard deviation; a constant group yields exact zero."""
    values = _vector(rewards)
    with np.errstate(over="ignore", invalid="ignore"):
        centered = values - values.mean()
        variance = float(centered @ centered) / (len(values) - 1)
    if not np.isfinite(centered).all() or not math.isfinite(variance):
        raise ValueError("standardization is not representable")
    std = math.sqrt(variance)
    if not math.isfinite(std):
        raise ValueError("standardization is not representable")
    return centered / std if std else np.zeros_like(centered)


def projected_scores(primary, scores, *, tie_ceiling: bool):
    """Exact Euclidean order-cone projection (Sec4.1, AppendixB.2).

    Equal primaries below the ceiling are NOT forced equal. Sorting them by
    their current score, rather than original row order, is essential.
    The implementation convention for the ceiling is p >= 1 - 1e-6.
    """
    p, z = _vector(primary), _vector(scores)
    if p.shape != z.shape or np.any((p < 0) | (p > 1)) or type(tie_ceiling) is not bool:
        raise ValueError("aligned primary in [0,1] and explicit ceiling Boolean required")
    values = z.copy()
    ceiling = p >= 1 - 1e-6
    if tie_ceiling and ceiling.any():
        with np.errstate(over="ignore", invalid="ignore"):
            mean = float(values[ceiling].mean())
        if not math.isfinite(mean):
            raise ValueError("ceiling mean is not representable")
        values[ceiling] = mean
    order = np.lexsort((values, p))
    # Blocks contain [sum, count, sorted start, sorted stop].
    blocks = []
    for position, original in enumerate(order):
        blocks.append([float(values[original]), 1, position, position + 1])
        while len(blocks) >= 2 and blocks[-2][0] / blocks[-2][1] > blocks[-1][0] / blocks[-1][1]:
            right, left = blocks.pop(), blocks.pop()
            total = left[0] + right[0]
            if not math.isfinite(total):
                raise ValueError("PAVA pooled sum is not representable")
            blocks.append([total, left[1] + right[1], left[2], right[3]])
    projected = np.empty_like(values)
    for total, count, start, stop in blocks:
        projected[order[start:stop]] = total / count
    return projected


def agreement(primary, auxiliary):
    """Eq.4: only passing pairs with distinct primary; no reading if absent."""
    p, a = _vector(primary), _vector(auxiliary)
    if p.shape != a.shape or np.any((p < 0) | (p > 1)):
        raise ValueError("aligned primary in [0,1] required")
    eligible = p >= .5
    difference = p[:, None] - p[None, :]
    pairs = eligible[:, None] & eligible[None, :] & (difference != 0)
    if not pairs.any():
        return None
    return float((np.sign(difference) * np.sign(a[:, None] - a[None, :]))[pairs].mean())


@dataclass(frozen=True)
class EarnedTrust:
    """All valid group readings, including current batch; no significance claim."""
    readings: tuple[float, ...] = ()

    def __post_init__(self):
        try:
            values = tuple(self.readings)
        except TypeError as error:
            raise ValueError("agreement readings must be an iterable") from error
        if any(isinstance(x, bool) or not isinstance(x, Real) or not math.isfinite(x) or not -1 <= x <= 1 for x in values):
            raise ValueError("finite agreement readings in [-1,1] required")
        object.__setattr__(self, "readings", tuple(float(x) for x in values))

    def add(self, values):
        return EarnedTrust(self.readings + tuple(x for x in values if x is not None))

    @property
    def untied(self):
        n = len(self.readings)
        if n < 61:
            return False
        values = np.asarray(self.readings)
        se = float(values.std(ddof=1) / math.sqrt(n))
        return bool(values.mean() > 2 * se)


def concur_group(raw_rewards, *, primary: int, gated_auxiliaries: tuple[int, ...],
                 weights, tie_ceiling: bool | dict[int, bool]):
    """Declared gating -> sample-standardized components -> exact projection.

    A primary gates only the declared auxiliary columns. Ungated components
    are left unchanged; hence no universal total-order guarantee is claimed.
    Returns unwhitened summed scores and per-auxiliary agreement readings.
    """
    r = np.asarray(raw_rewards, dtype=np.float64)
    if r.ndim != 2 or r.shape[0] < 2 or r.shape[1] < 1 or not np.isfinite(r).all() or np.any((r < 0) | (r > 1)):
        raise ValueError("finite [group>=2,components] raw rewards in [0,1] required")
    if type(primary) is not int or not 0 <= primary < r.shape[1]:
        raise ValueError("valid primary column required")
    if len(set(gated_auxiliaries)) != len(gated_auxiliaries) or any(
        type(k) is not int or not 0 <= k < r.shape[1] or k == primary for k in gated_auxiliaries
    ):
        raise ValueError("distinct non-primary gated columns required")
    w = _vector(weights, minimum=1)
    if len(w) != r.shape[1] or np.any(w < 0):
        raise ValueError("one finite nonnegative declared weight per reward required")
    if type(tie_ceiling) is bool:
        tied = {k: tie_ceiling for k in gated_auxiliaries}
    elif isinstance(tie_ceiling, dict) and set(tie_ceiling) == set(gated_auxiliaries) and all(type(x) is bool for x in tie_ceiling.values()):
        tied = tie_ceiling
    else:
        raise ValueError("explicit ceiling policy for each gated pair required")
    p, gated = r[:, primary], r.copy()
    for k in gated_auxiliaries:
        gated[:, k] = np.where(p < .5, np.minimum(r[:, k], p), r[:, k])
    z = np.column_stack([standardized(gated[:, k]) for k in range(r.shape[1])])
    readings = {k: agreement(p, gated[:, k]) for k in gated_auxiliaries}
    for k in gated_auxiliaries:
        z[:, k] = projected_scores(p, z[:, k], tie_ceiling=tied[k])
    return z @ w, readings


def concur_batch(groups: list[dict], *, variant: str, trust: dict[tuple[str, int], EarnedTrust],
                 batch_std_correction: int):
    """Algorithm1: collect entire batch first, then one policy per task/pair.

    Each record supplies task, raw_rewards, primary, gated_auxiliaries, weights.
    CONCUR-A pools past and current valid readings before projecting ANY
    group; a pair may become tied again when later evidence changes sign.
    """
    if not groups or variant not in {"T", "A"} or any(not isinstance(value, EarnedTrust) for value in trust.values()):
        raise ValueError("groups, explicit T/A variant and typed pair histories required")
    designs, current_readings = {}, {}
    for group in groups:
        if not isinstance(group.get("task"), str) or not group["task"]:
            raise ValueError("nonempty task identity required")
        arguments = {k: group[k] for k in ("raw_rewards", "primary", "gated_auxiliaries", "weights")}
        _, readings = concur_group(**arguments, tie_ceiling=True)
        design = (group["primary"], tuple(group["gated_auxiliaries"]), tuple(group["weights"]))
        if group["task"] in designs and designs[group["task"]] != design:
            raise ValueError("one declared reward design per task required")
        designs[group["task"]] = design
        for column, value in readings.items():
            current_readings.setdefault((group["task"], column), []).append(value)
    histories = dict(trust)
    if variant == "A":
        for pair, values in current_readings.items():
            histories[pair] = histories.get(pair, EarnedTrust()).add(values)
    summed, lengths = [], []
    for group in groups:
        tied = {k: variant == "T" or not histories.get((group["task"], k), EarnedTrust()).untied
                for k in group["gated_auxiliaries"]}
        values, _ = concur_group(**{k: group[k] for k in ("raw_rewards", "primary", "gated_auxiliaries", "weights")}, tie_ceiling=tied)
        summed.append(values)
        lengths.append(len(values))
    flat = batch_whiten(np.concatenate(summed), std_correction=batch_std_correction)
    boundaries = np.cumsum([0, *lengths])
    return [flat[boundaries[i]:boundaries[i + 1]] for i in range(len(lengths))], histories


def batch_whiten(summed_scores, *, std_correction: int):
    """Eq.2 across ALL tasks, never independently renormalize each group."""
    if type(std_correction) is not int or std_correction not in (0, 1):
        raise ValueError("explicit batch std correction 0 or 1 required")
    values = _vector(summed_scores)
    with np.errstate(over="ignore", invalid="ignore"):
        centered = values - values.mean()
        variance = float(centered @ centered) / (len(values) - std_correction)
    if not np.isfinite(centered).all() or not math.isfinite(variance):
        raise ValueError("batch whitening is not representable")
    std = math.sqrt(variance)
    if not math.isfinite(std):
        raise ValueError("batch whitening is not representable")
    return centered / std if std else np.zeros_like(values)


def diagnostic(seed: int = 42, device: str = "cpu"):
    if type(seed) is not int or device != "cpu":
        raise ValueError("pure CPU mechanism diagnostic")
    rng = np.random.default_rng(seed)
    p = np.array([0., .3, .3, .7, 1., 1.])
    z = standardized(rng.normal(size=6))
    order = projected_scores(p, z, tie_ceiling=False)
    tied = projected_scores(p, z, tie_ceiling=True)
    valid = p[:, None] > p[None, :]
    binary = np.array([[0., 1.], [1., .9], [1., .1]])
    mixed, readings = concur_group(binary, primary=0, gated_auxiliaries=(1,), weights=[1, 1], tie_ceiling=True)
    all_pass, _ = concur_group(np.array([[1., .2], [1., .9]]), primary=0, gated_auxiliaries=(1,), weights=[1, 1], tie_ceiling=True)
    equal_primary = projected_scores([.3, .3], [-1, 1], tie_ceiling=False)
    trust = EarnedTrust((.4,) * 60).add([.4])
    white = batch_whiten(np.r_[mixed, mixed * 2], std_correction=0)
    return {"seed": seed, "diagnostic_only": True,
        "metrics": {"order_energy": float(order @ order), "tied_energy": float(tied @ tied),
                    "projection_mean_error": float(abs(z.sum() - tied.sum())),
                    "pythagorean_error": float(abs(z @ z - tied @ tied - (z - tied) @ (z - tied))),
                    "all_pass_magnitude": float(np.max(np.abs(all_pass))), "valid_trust_readings": len(trust.readings)},
        "checks": {"primary_order_preserved": bool(np.all((tied[:, None] - tied[None, :])[valid] >= -1e-12)),
                   "ceiling_tied": bool(tied[-1] == tied[-2]),
                   "below_ceiling_ties_not_collapsed": bool(np.array_equal(equal_primary, [-1, 1])),
                   "mean_preserved": bool(abs(z.sum() - tied.sum()) < 1e-12),
                   "cone_energy_identity": bool(abs(z @ z - tied @ tied - (z - tied) @ (z - tied)) < 1e-10),
                   "all_pass_auxiliary_removed": bool(np.max(np.abs(all_pass)) < 1e-12),
                   "binary_primary_has_no_trust_reading": readings[1] is None,
                   "sixty_one_readings_required": trust.untied and not EarnedTrust((.4,) * 60).untied,
                   "whitening_is_whole_batch": bool(abs(white.mean()) < 1e-12 and abs(white.std() - 1) < 1e-12)}}
