"""Reliability-Anchored Preference Walk, 2610.20089 equations 3--16.

This module consumes observed pairwise probabilities. It does not synthesize
video preferences, invoke a judge, or claim any video-generation improvement.
"""
from __future__ import annotations

import math
import torch


def standardize(values, epsilon=1e-8):
    centered = values - values.mean()
    return centered / (centered.square().mean().sqrt() + epsilon)


def _entropy(probability):
    return -(probability * probability.clamp_min(torch.finfo(probability.dtype).tiny).log()).sum()


def power_temper(probability, entropy_floor=.8, *, iterations=60):
    """Largest a in [0,1] satisfying H(p**a)/log(G)>=floor (eq. 12)."""
    if not 0 <= entropy_floor <= 1 or probability.ndim != 1 or len(probability) < 2 or iterations < 1:
        raise ValueError("valid entropy floor and at least two probabilities required")
    if not torch.isfinite(probability).all() or bool((probability < 0).any()):
        raise ValueError("finite nonnegative preference credit required")
    if not float(probability.sum()) > 0:
        raise ValueError("positive preference mass required")
    p = probability / probability.sum()
    if float(_entropy(p) / math.log(len(p))) >= entropy_floor:
        return p, 1.
    # A vanishing entry has a well-defined uniform limit as a -> 0.
    logs = p.clamp_min(torch.finfo(p.dtype).tiny).log()
    low, high = 0., 1.
    for _ in range(iterations):
        mid = (low + high) / 2.
        q = (logs * mid).softmax(0)
        if float(_entropy(q) / math.log(len(q))) >= entropy_floor:
            low = mid
        else:
            high = mid
    return (logs * low).softmax(0), low


def rap_walk_advantages(pairwise, *, entropy_floor=.8, trust_interval=(.1, .5),
                        epsilon=1e-8, tolerance=1e-10, max_iterations=10000):
    """Return a detached group advantage and auditable graph intermediates.

    W[i,j] means i beats j. Opposite edges must be complementary. Diagonals
    are ignored. A nonconvergent periodic chain is an explicit error, never a
    silently substituted PageRank/teleportation algorithm.
    """
    w = torch.as_tensor(pairwise).detach()
    if not w.is_floating_point():
        w = w.double()
    w = w.to(dtype=torch.float64)
    if w.ndim != 2 or w.shape[0] != w.shape[1] or len(w) < 3:
        raise ValueError("complete square preference graph with at least three nodes required")
    if not torch.isfinite(w).all() or bool(((w < 0) | (w > 1)).any()):
        raise ValueError("finite pairwise probabilities in [0,1] required")
    n = len(w)
    off_diagonal = ~torch.eye(n, dtype=torch.bool, device=w.device)
    if not torch.allclose((w + w.T)[off_diagonal], torch.ones_like(w[off_diagonal]), atol=1e-6):
        raise ValueError("opposite preferences must sum to one")
    lo, hi = trust_interval
    if not 0 <= lo <= hi <= 1 or epsilon <= 0 or tolerance <= 0 or max_iterations < 1:
        raise ValueError("invalid trust interval or numerical budget")
    w = w.clamp(epsilon, 1. - epsilon)
    hb = -w * w.log() - (1. - w) * (1. - w).log()
    clarity = 1. - hb / math.log(2.)
    logits = w.log() - (1. - w).log()
    cycle = []
    for i in range(n):
        triangles = [abs(logits[i, j] + logits[j, k] + logits[k, i])
                     for j in range(n) for k in range(j + 1, n) if i not in (j, k)]
        cycle.append(torch.stack(triangles).mean())
    cyclicity = torch.stack(cycle)
    normalized_cycle = standardize(cyclicity, epsilon)
    win_rate = (w * off_diagonal).sum(-1) / (n - 1)
    anchor = standardize(win_rate, epsilon)
    reliability = (-normalized_cycle).exp().unsqueeze(0) * (clarity + epsilon).pow(.25)
    # Destination prior and loser-to-winner orientation, not W[i,j].
    weights = w.T * anchor.exp().unsqueeze(0) * reliability
    weights = weights.masked_fill(~off_diagonal, 0.)
    transition = weights / weights.sum(-1, keepdim=True)
    stationary = w.new_full((n,), 1. / n)
    for iteration in range(1, max_iterations + 1):
        following = stationary @ transition
        if float((following - stationary).abs().max()) <= tolerance:
            stationary = following / following.sum()
            break
        stationary = following
    else:
        raise RuntimeError("preference walk did not converge within the declared budget")
    calibrated, exponent = power_temper(stationary, entropy_floor)
    proposal = n * calibrated - 1.
    alpha = clarity[off_diagonal].mean().clamp(lo, hi)
    mixed = (1. - alpha) * anchor + alpha * proposal
    advantages = standardize(mixed, epsilon)
    return advantages, {
        "anchor": anchor, "clarity": clarity, "cyclicity": cyclicity,
        "transition": transition, "stationary": stationary, "calibrated": calibrated,
        "graph_proposal": proposal, "mixing_coefficient": float(alpha),
        "tempering_exponent": exponent, "iterations": iteration,
        "stationary_residual": float((stationary @ transition - stationary).abs().max()),
        "normalized_entropy": float(_entropy(calibrated) / math.log(n)),
    }


def rap_walk_grpo_loss(current_log_probs, old_log_probs, response_mask, pairwise, *,
                       clip_epsilon=.2, reference_log_probs=None, kl_beta=0., **walk_options):
    """Token-level GRPO interface; graph advantages do not receive gradients."""
    if current_log_probs.ndim != 2 or current_log_probs.shape != old_log_probs.shape:
        raise ValueError("aligned group x token log probabilities required")
    if response_mask.shape != current_log_probs.shape or response_mask.dtype != torch.bool:
        raise ValueError("boolean token response mask required")
    if not bool(response_mask.any(-1).all()) or not 0 < clip_epsilon < 1 or kl_beta < 0:
        raise ValueError("each rollout needs valid tokens and a valid clip/KL coefficient")
    if not torch.isfinite(current_log_probs).all() or not torch.isfinite(old_log_probs).all():
        raise ValueError("finite policy log probabilities required")
    advantages, audit = rap_walk_advantages(pairwise, **walk_options)
    if len(advantages) != len(current_log_probs):
        raise ValueError("preference graph must match rollout group")
    advantages = advantages.to(current_log_probs).detach().unsqueeze(-1)
    ratio = (current_log_probs - old_log_probs.detach()).exp()
    token_loss = -torch.minimum(ratio * advantages,
                               ratio.clamp(1. - clip_epsilon, 1. + clip_epsilon) * advantages)
    if reference_log_probs is not None:
        if reference_log_probs.shape != current_log_probs.shape:
            raise ValueError("reference log probabilities must align")
        if not torch.isfinite(reference_log_probs).all():
            raise ValueError("finite reference log probabilities required")
        difference = reference_log_probs.detach() - current_log_probs
        token_loss = token_loss + kl_beta * (difference.exp() - difference - 1.)
    elif kl_beta:
        raise ValueError("positive KL coefficient requires frozen reference log probabilities")
    loss = ((token_loss * response_mask).sum(-1) / response_mask.sum(-1)).mean()
    if not torch.isfinite(loss):
        raise FloatingPointError("nonfinite GRPO surrogate; policy update rejected")
    return loss, audit
