"""GPPO Eqs. 10--20 with explicit, probability-aware proximal regions.

The paper uses f_KL(r)=-log(r) in Eq.16/18 but a two-sided log bound in
Section 3.4. These are not the same MC sublevel set. We expose both explicitly:
``kl`` is the literal integrand and ``two_sided_log`` is the stated DAPO
mapping. Never silently add a linear term or advertise one as the other.
"""
from __future__ import annotations

import torch

GEOMETRIES = ("tv", "chi2", "hellinger", "kl", "two_sided_log")
TOPOLOGIES = ("mc", "atomic", "binary")


def integrand(ratio, geometry):
    if geometry == "tv":
        return .5 * (ratio - 1).abs()
    if geometry == "chi2":
        return (ratio - 1).square()
    if geometry == "hellinger":
        return (ratio.sqrt() - 1).square()
    if geometry == "kl":
        return -ratio.log()
    if geometry == "two_sided_log":
        return ratio.log().abs()
    raise ValueError(f"unknown divergence geometry: {geometry}")


def estimated_divergence(ratio, behavior_probability, *, geometry, topology):
    if topology not in TOPOLOGIES:
        raise ValueError("unknown estimator topology")
    if geometry == "two_sided_log" and topology != "mc":
        raise ValueError("two-sided log is only the paper's explicit MC/DAPO mapping")
    if (behavior_probability <= 0).any() or (behavior_probability >= 1).any():
        raise ValueError("sampled action probability must lie strictly between zero and one")
    if (ratio <= 0).any():
        raise ValueError("policy likelihood ratios must be positive")
    values = integrand(ratio, geometry)
    if topology == "mc":
        return values
    atomic = behavior_probability * values
    if topology == "atomic":
        return atomic
    complement = ((1 - behavior_probability * ratio) / (1 - behavior_probability)).clamp_min(
        torch.finfo(ratio.dtype).tiny)
    if (behavior_probability * ratio > 1 + 1e-6).any():
        raise ValueError("binary estimator received an invalid sampled-action probability")
    return atomic + (1 - behavior_probability) * integrand(complement, geometry)


def proximal_bounds(behavior_log_probability, *, geometry="chi2", topology="atomic", delta=.04,
                    iterations=64):
    if delta <= 0 or iterations < 1 or not torch.isfinite(behavior_log_probability).all():
        raise ValueError("finite behavior likelihood and positive trust-region budget required")
    if (behavior_log_probability > 0).any():
        raise ValueError("log probability cannot be positive")
    probabilities = behavior_log_probability.detach().double().exp()
    if (probabilities <= 0).any():
        raise ValueError("strictly positive behavior probability required")
    # A finite-precision log-softmax may round a nearly deterministic token
    # to log(p)=0. Use an interior machine-epsilon limit for the complement;
    # this is not an added exploration floor or a changed trust-region delta.
    probabilities = probabilities.clamp_max(1 - torch.finfo(probabilities.dtype).eps)
    ones = torch.ones_like(probabilities)
    tiny = torch.full_like(probabilities, torch.finfo(probabilities.dtype).tiny)
    maximum = (1 / probabilities) * (1 - 1e-12)

    def cost(ratio):
        return estimated_divergence(ratio, probabilities, geometry=geometry, topology=topology)

    with torch.no_grad():
        lower_inside = cost(tiny) <= delta
        low, high = tiny.log(), ones.log()
        for _ in range(iterations):
            middle = (low + high) / 2
            outside = cost(middle.exp()) > delta
            low = torch.where(outside, middle, low)
            high = torch.where(outside, high, middle)
        lower = torch.where(lower_inside, tiny, high.exp())
        upper_inside = cost(maximum) <= delta
        low, high = ones.log(), maximum.log()
        for _ in range(iterations):
            middle = (low + high) / 2
            inside = cost(middle.exp()) <= delta
            low = torch.where(inside, middle, low)
            high = torch.where(inside, high, middle)
        upper = torch.where(upper_inside, maximum, low.exp())
    return lower.to(behavior_log_probability.dtype), upper.to(behavior_log_probability.dtype)


def gppo_loss(current_log_probability, behavior_log_probability, advantages, mask, *,
              geometry="chi2", topology="atomic", delta=.04):
    if current_log_probability.shape != behavior_log_probability.shape or mask.shape != current_log_probability.shape:
        raise ValueError("token likelihood/mask shapes must match")
    if (mask.sum(-1) == 0).any():
        raise ValueError("each trajectory needs at least one response token")
    lower, upper = proximal_bounds(behavior_log_probability, geometry=geometry, topology=topology, delta=delta)
    ratio = (current_log_probability - behavior_log_probability.detach()).exp()
    clipped = torch.maximum(lower, torch.minimum(upper, ratio))
    advantage = advantages.detach()
    if advantage.ndim == ratio.ndim - 1:
        advantage = advantage[..., None]
    surrogate = torch.minimum(ratio * advantage, clipped * advantage)
    sequence_mean = (surrogate * mask).sum(-1) / mask.sum(-1)
    return -sequence_mean.mean(), {
        "geometry": geometry, "topology": topology,
        "clip_fraction": float((((ratio < lower) | (ratio > upper)) * mask).sum().detach() / mask.sum()),
        "lower_mean": float((lower * mask).sum() / mask.sum()),
        "upper_mean": float((upper * mask).sum() / mask.sum()),
    }
