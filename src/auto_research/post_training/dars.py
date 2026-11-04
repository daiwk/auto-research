"""DARS outcome-density reward processing, arXiv:2611.04792 equations 1--4.

No policy objective is replaced. Frozen outcome features/rewards are detached;
the caller supplies the resulting advantages to its unchanged GRPO objective.
"""
from __future__ import annotations

import math

import torch

REQUIRES_GPU_VALIDATION = True


@torch.no_grad()
def density_scaled_advantages(outcomes, rewards, *, bandwidth=20., correction=0,
                              zero_variance='zero'):
    """Gaussian KDE INCLUDING self, independently for each leading group.

    outcomes: [..., group, feature]; rewards: [..., group]. Standard-deviation
    correction is explicit because the paper does not specify sample/population
    convention. A constant-scaled-reward group's mathematically undefined 0/0 either
    returns zero advantages (default) or raises, never silently adds epsilon.
    """
    if (outcomes.ndim < 2 or rewards.shape != outcomes.shape[:-1] or min(outcomes.shape) < 1
            or not outcomes.is_floating_point() or not rewards.is_floating_point()
            or outcomes.device != rewards.device or outcomes.dtype != rewards.dtype
            or not bool(torch.isfinite(outcomes).all()) or not bool(torch.isfinite(rewards).all())
            or bool((rewards < 0).any())):
        raise ValueError('finite, same-device/dtype outcomes [...,G,D] and nonnegative rewards [...,G] required')
    if not math.isfinite(bandwidth) or bandwidth <= 0:
        raise ValueError('finite positive Gaussian bandwidth required')
    group = outcomes.shape[-2]
    if type(correction) is not int or not 0 <= correction < group or zero_variance not in ('zero', 'raise'):
        raise ValueError('valid explicit std correction and zero-variance policy required')
    # Divide before squaring to avoid h*h overflow at the large-bandwidth limit.
    difference = (outcomes.unsqueeze(-2) - outcomes.unsqueeze(-3)) / bandwidth
    distances = difference.square().sum(-1)
    density = torch.exp(-.5 * distances).sum(-1)
    scaled = rewards / density
    centered = scaled - scaled.mean(-1, keepdim=True)
    variance = centered.square().sum(-1, keepdim=True) / (group - correction)
    deviation = variance.sqrt()
    if zero_variance == 'raise' and bool((deviation == 0).any()):
        raise ValueError('group-relative advantage is undefined for zero standard deviation')
    denominator = torch.where(deviation > 0, deviation, torch.ones_like(deviation))
    advantages = torch.where(deviation > 0, centered / denominator, torch.zeros_like(centered))
    if not all(bool(torch.isfinite(x).all()) for x in (density, scaled, advantages)):
        raise ValueError('nonfinite reward processing; check numerical scale')
    return {'density': density, 'scaled_rewards': scaled, 'advantages': advantages}


def diagnostic(seed=42, device='cpu'):
    generator = torch.Generator(device=device).manual_seed(seed)
    outcomes = torch.randn(2, 6, 3, generator=generator, device=device, dtype=torch.float64)
    rewards = torch.rand(2, 6, generator=generator, device=device, dtype=torch.float64)
    result = density_scaled_advantages(outcomes, rewards, bandwidth=.8)
    reference = torch.empty_like(rewards)
    for group in range(2):
        for i in range(6):
            reference[group, i] = sum(torch.exp(-((outcomes[group, i] - outcomes[group, j]) / .8).square().sum() / 2)
                                      for j in range(6))
    error = float((reference - result['density']).abs().max())
    detached = density_scaled_advantages(outcomes.requires_grad_(), rewards.requires_grad_(), bandwidth=.8)
    identical = density_scaled_advantages(torch.zeros_like(outcomes), rewards, bandwidth=.8)
    mean_error = float(result['advantages'].mean(-1).abs().max())
    variance_error = float((result['advantages'].square().mean(-1) - 1).abs().max())
    return {'seed': seed, 'diagnostic_only': True, 'evaluation_tier': 'l1_mechanism',
            'metrics': {'kde_reference_max_error': error, 'advantage_mean_error': mean_error,
                        'advantage_population_variance_error': variance_error,
                        'minimum_density': float(result['density'].min())},
            'checks': {'gaussian_reference_agrees': error < 1e-12, 'self_density_included': bool((result['density'] >= 1).all()),
                       'group_normalization': mean_error < 1e-12 and variance_error < 1e-12,
                       'frozen_outcome_reward_processing': all(not x.requires_grad for x in detached.values()),
                       'identical_density_is_group_size': bool((identical['density'] == 6).all())}}
