"""CPU L1 experience-selection mathematics from arXiv:2611.27159v1.

Explicit gradients/moments and historical action contents are caller inputs.
No language agent, ALFWorld executor, model training or evaluation answers are
read. In particular, public support gradients are not query-answer gradients.
"""

from __future__ import annotations

from collections.abc import Hashable, Sequence
import math

import numpy as np

REQUIRES_GPU_VALIDATION = False


def _array(value, ndim: int) -> np.ndarray:
    result = np.asarray(value, dtype=np.float64)
    if result.ndim != ndim or not result.size or not np.isfinite(result).all():
        raise ValueError("nonempty finite array of the required rank expected")
    return result


def _unit(value: np.ndarray) -> np.ndarray:
    # Scaling avoids a norm overflow for finite inputs. Zero vectors have no
    # paper-defined u(x), so fail rather than inventing an influence score.
    scale = np.max(np.abs(value), axis=-1, keepdims=True)
    if np.any(scale == 0):
        raise ValueError("zero feature/support gradients have undefined direction")
    scaled = value / scale
    return scaled / np.linalg.norm(scaled, axis=-1, keepdims=True)


def optimizer_aware_features(gradients, first_moments, second_moments, *,
                             beta1: float = .9, beta2: float = .999,
                             epsilon: float = 1e-8) -> np.ndarray:
    """LESS-style ranking feature, not the full bias-corrected AdamW update.

    gradients: [checkpoint, candidate, parameter]; moments: [checkpoint,
    parameter]. The paper uses checkpoints 8/16/24/32, held fixed while each
    candidate is scored. No projection or moment update is performed here.
    """
    g, m, v = _array(gradients, 3), _array(first_moments, 2), _array(second_moments, 2)
    if m.shape != v.shape or m.shape != (g.shape[0], g.shape[2]) or np.any(v < 0):
        raise ValueError("matching checkpoint/parameter moments with v>=0 required")
    if not all(isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)
               for x in (beta1, beta2, epsilon)) or not 0 <= beta1 < 1 or not 0 <= beta2 < 1 or epsilon <= 0:
        raise ValueError("beta values in [0,1), positive finite epsilon required")
    try:
        with np.errstate(over="raise", invalid="raise", divide="raise"):
            features = (beta1 * m[:, None, :] + (1 - beta1) * g) / np.sqrt(
                beta2 * v[:, None, :] + (1 - beta2) * g * g + epsilon)
    except FloatingPointError as exc:
        raise ValueError("optimizer feature intermediate overflow") from exc
    if not np.isfinite(features).all():
        raise ValueError("optimizer feature overflow")
    return features


def relevance_scores(features, support_families: Sequence[np.ndarray]) -> np.ndarray:
    """Average checkpoints before max over families; normalize each support.

    Each support family has shape [checkpoint, public_action, parameter].
    Its mean is NOT normalized again after averaging individually unit vectors.
    Uniform checkpoint weights are the paper's 1/4 for four checkpoints.
    """
    feature = _array(features, 3)
    if not support_families:
        raise ValueError("at least one explicit public-support family required")
    normalized = _unit(feature)
    family_scores = []
    for family in support_families:
        support = _array(family, 3)
        if support.shape[0] != feature.shape[0] or support.shape[2] != feature.shape[2]:
            raise ValueError("support checkpoint and parameter dimensions must match")
        mean_support = _unit(support).mean(axis=1)
        family_scores.append(np.einsum("cnd,cd->cn", normalized, mean_support).mean(axis=0))
    scores = np.max(np.stack(family_scores), axis=0)
    if not np.isfinite(scores).all():
        raise ValueError("nonfinite relevance scores")
    return scores


def _contents(contents: Sequence[str]) -> tuple[tuple[int, ...], dict[str, int]]:
    if not contents or len(contents) > 10000 or any(not isinstance(x, str) or not x for x in contents):
        raise ValueError("1..10000 explicit nonempty message contents required")
    first: dict[str, int] = {}
    for index, content in enumerate(contents):
        first.setdefault(content, index)
    return tuple(first.values()), first


def _seed(seed: int) -> None:
    if not isinstance(seed, int) or isinstance(seed, bool) or seed < 0:
        raise ValueError("nonnegative integer seed required")


def global_schedule(contents: Sequence[str], scores, *, support_size: int = 256,
                    seed: int = 42, passes: int = 3, rule: str = "gradient") -> tuple[int, ...]:
    """Deduplicate before selection; replay complete seeded shuffled passes.

    Scores are canonical content scores. Repeated rows cannot gain selection
    probability. Top-score ties use first representative corpus index.
    """
    representatives, _ = _contents(contents)
    values = _array(scores, 1)
    if len(values) != len(contents):
        raise ValueError("one canonical score per input row required")
    if (not isinstance(support_size, int) or isinstance(support_size, bool)
            or not 1 <= support_size <= len(representatives)
            or not isinstance(passes, int) or isinstance(passes, bool) or not 1 <= passes <= 100):
        raise ValueError("valid support size and 1..100 replay passes required")
    _seed(seed)
    rng = np.random.default_rng(seed)
    if rule == "random":
        selected = rng.choice(representatives, support_size, replace=False).tolist()
    elif rule in ("gradient", "high_nll"):
        selected = sorted(representatives, key=lambda index: (-values[index], index))[:support_size]
    else:
        raise ValueError("rule must be gradient, high_nll or random")
    return tuple(int(index) for _ in range(passes) for index in rng.permutation(selected))


def matched_schedule(contents: Sequence[str], scores, strata: Sequence[Hashable],
                     reference: Sequence[int], *, seed: int = 42,
                     rule: str = "high") -> tuple[int, ...]:
    """Preserve every reference stratum and its distinct-content quota.

    All eligible rows in a stratum may be selected, not just reference members.
    Each seeded cycle visits its selected identities before any repetition.
    """
    representatives, first = _contents(contents)
    values = _array(scores, 1)
    if len(values) != len(contents) or len(strata) != len(contents) or not reference or len(reference) > 100000:
        raise ValueError("aligned rows/strata and bounded nonempty reference required")
    try:
        for index, content in enumerate(contents):
            if strata[index] != strata[first[content]]:
                raise ValueError("identical contents cannot belong to different strata")
        eligible: dict[Hashable, list[int]] = {}
        for index in representatives:
            eligible.setdefault(strata[index], []).append(index)
        quotas: dict[Hashable, set[str]] = {}
        for index in reference:
            if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index < len(contents):
                raise ValueError("reference indices must address corpus rows")
            quotas.setdefault(strata[index], set()).add(contents[index])
    except TypeError as exc:
        raise ValueError("hashable stratum labels required") from exc
    _seed(seed)
    rng = np.random.default_rng(seed)
    streams: dict[Hashable, list[int]] = {}
    for stratum, identities in quotas.items():
        options = eligible[stratum]
        if rule == "random":
            selected = rng.choice(options, len(identities), replace=False).tolist()
        elif rule in ("high", "low"):
            direction = -1 if rule == "high" else 1
            selected = sorted(options, key=lambda index: (direction * values[index], index))[:len(identities)]
        else:
            raise ValueError("rule must be high, low or random")
        needed = sum(strata[index] == stratum for index in reference)
        stream = []
        while len(stream) < needed:
            stream.extend(int(index) for index in rng.permutation(selected))
        streams[stratum] = stream[:needed]
    cursors = dict.fromkeys(streams, 0)
    result = []
    for index in reference:
        stratum = strata[index]
        result.append(streams[stratum][cursors[stratum]])
        cursors[stratum] += 1
    return tuple(result)


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("CPU-only component; no CUDA path advertised")
    _seed(seed)
    rng = np.random.default_rng(seed)
    gradients = rng.normal(size=(4, 8, 6))
    moments = rng.normal(size=(4, 6)) * .1
    second = np.abs(rng.normal(size=(4, 6))) + .1
    features = optimizer_aware_features(gradients, moments, second)
    support = [rng.normal(size=(4, 3, 6)), rng.normal(size=(4, 2, 6))]
    score = relevance_scores(features, support)
    contents = tuple(f"historical-action-{i}" for i in range(8)) + ("historical-action-0",)
    scores = np.r_[score, score[0]]
    schedule = global_schedule(contents, scores, support_size=3, seed=seed)
    strata = ("place",) * 4 + ("clean",) * 4 + ("place",)
    reference = (0, 4, 1, 5, 0, 4, 1, 5)
    matched = matched_schedule(contents, scores, strata, reference, seed=seed)
    zero_rejected = False
    try:
        relevance_scores(np.zeros((4, 1, 6)), support)
    except ValueError:
        zero_rejected = True
    checks = {
        "scores_finite": bool(np.isfinite(score).all()),
        "three_complete_passes": all(set(schedule[i:i + 3]) == set(schedule[:3]) for i in (0, 3, 6)),
        "first_duplicate_representative": 8 not in schedule,
        "matched_stratum_positions": all(strata[a] == strata[b] for a, b in zip(matched, reference)),
        "matched_distinct_quotas": all(len({contents[i] for i in matched if strata[i] == s}) == 2 for s in ("place", "clean")),
        "zero_direction_rejected": zero_rejected,
        "seed_replay_stable": schedule == global_schedule(contents, scores, support_size=3, seed=seed),
    }
    return {"seed": seed, "device": "cpu", "evaluation_tier": "l1_mechanism",
            "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
            "checks": checks, "selected_representatives": list(schedule[:3]),
            "metrics": {"checkpoint_count": 4, "candidate_count": 8,
                        "selected_content_count": 3, "replay_presentations": len(schedule),
                        "matched_presentations": len(matched), "mean_relevance_score": float(score.mean())},
            "training_executed": False,
            "agent_evaluation_executed": False}
