"""ReSID v1 Eqs. 1--3 and partial SID matching; no learned recommender.

Caller supplies frozen logits, training-only priors, normalized content vectors
and a user representation. This finite CPU mechanism never receives a target.
"""
from __future__ import annotations

import math
from collections.abc import Callable, Sequence

import numpy as np

REQUIRES_GPU_VALIDATION = False


def parallel_quantize(latents, codebooks):
    z, books = np.asarray(latents, float), np.asarray(codebooks, float)
    if z.ndim != 3 or books.ndim != 3 or z.shape[1] != books.shape[0] or z.shape[2] != books.shape[2]:
        raise ValueError("expected [items, levels, subdim] and [levels, codes, subdim]")
    if not np.isfinite(z).all() or not np.isfinite(books).all():
        raise ValueError("finite inputs required")
    return ((z[:, :, None, :] - books[None, :, :, :]) ** 2).sum(-1).argmin(-1)


def _logsumexp(values):
    values = np.asarray(values, float)
    maximum = values.max()
    return float(maximum + np.log(np.exp(values - maximum).sum()))


def guided_beam(catalog_sids: Sequence[Sequence[int]], similarities, logits: Callable,
                training_prior: Callable, *, vocabulary_size: int, beam_size: int,
                popularity_weight: float, semantic_weight: float, temperature: float):
    """Trie-constrained Eq.3. Normalize over supplied full vocabulary, then mask.

    `similarities` are user/content dot products, not held-out relevance labels.
    Priors must be positive training transition frequencies (smoothing is caller
    policy). Empty-prefix score is zero; semantic differences telescope.
    """
    sids = np.asarray(catalog_sids, int)
    sim = np.asarray(similarities, float)
    if (sids.ndim != 2 or not sids.size or sim.shape != (len(sids),)
            or vocabulary_size < 1 or beam_size < 1 or temperature <= 0
            or min(popularity_weight, semantic_weight) < 0 or not np.isfinite(sim).all()
            or (sids < 0).any() or (sids >= vocabulary_size).any()):
        raise ValueError("invalid catalog or guidance controls")
    prefixes = {}
    for index, sid in enumerate(sids):
        for length in range(sids.shape[1] + 1):
            prefixes.setdefault(tuple(sid[:length]), []).append(index)

    def potential(prefix):
        indices = prefixes[prefix]
        return _logsumexp(sim[indices] / temperature) - math.log(len(indices))

    beam = [((), 0.0)]
    for _ in range(sids.shape[1]):
        expanded = []
        for prefix, score in beam:
            raw, prior = np.asarray(logits(prefix), float), np.asarray(training_prior(prefix), float)
            if (raw.shape != (vocabulary_size,) or prior.shape != raw.shape
                    or not np.isfinite(raw).all() or not np.isfinite(prior).all() or (prior <= 0).any()):
                raise ValueError("finite logits and positive train-only priors required")
            calibrated = raw - popularity_weight * np.log(prior)
            logp = calibrated - _logsumexp(calibrated)
            for token in range(vocabulary_size):
                child = prefix + (token,)
                if child in prefixes:
                    expanded.append((child, score + float(logp[token])
                                     + semantic_weight * (potential(child) - potential(prefix))))
        beam = sorted(expanded, key=lambda value: (-value[1], value[0]))[:beam_size]
    return beam


def partial_match(catalog_sids, beams, mismatch_tolerance):
    """Return item indices ordered by least Hamming mismatch, then beam score.

    Exact duplicates remain distinct catalog items. Final ties use item index.
    """
    sids = np.asarray(catalog_sids, int)
    if sids.ndim != 2 or not 0 <= mismatch_tolerance <= sids.shape[1] or not beams:
        raise ValueError("nonempty beams and valid mismatch tolerance required")
    ranked = []
    for index, sid in enumerate(sids):
        matches = []
        for tokens, score in beams:
            if len(tokens) != len(sid) or not math.isfinite(score):
                raise ValueError("beam shape or score invalid")
            distance = int((sid != np.asarray(tokens)).sum())
            if distance <= mismatch_tolerance:
                matches.append((distance, -float(score)))
        if matches:
            ranked.append((*min(matches), index))
    return [index for _, _, index in sorted(ranked)]


def diagnostic(seed=42, device="cpu"):
    if device != "cpu":
        raise ValueError("CPU mechanism only")
    rng = np.random.default_rng(seed)
    books = np.array([[[0.0], [1.0]], [[0.0], [1.0]]])
    latents = np.array([[[0.1], [0.9]], [[0.8], [0.2]]])
    sids = [(0, 0), (0, 1), (1, 0), (1, 1)]
    logits = lambda prefix: np.log([0.8, 0.2])
    prior = lambda prefix: np.array([0.9, 0.1])
    baseline = guided_beam(sids, [0, 0, 0, 1], logits, prior, vocabulary_size=2,
                           beam_size=1, popularity_weight=0, semantic_weight=0, temperature=1)
    guided = guided_beam(sids, [0, 0, 0, 1], logits, prior, vocabulary_size=2,
                         beam_size=1, popularity_weight=1, semantic_weight=2, temperature=1)
    score = float(rng.uniform(-2, -1))
    matches = partial_match(sids, [((0, 0), score), ((1, 1), score - 1)], 1)
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "checks": {"independent_subspaces": parallel_quantize(latents, books).tolist() == [[0, 1], [1, 0]],
                       "unguided_head": baseline[0][0] == (0, 0),
                       "guided_tail": guided[0][0] == (1, 1),
                       "distance_before_score": matches == [0, 3, 1, 2]},
            "metrics": {"guided_tail_score": guided[0][1], "partial_candidates": len(matches)}}
