"""Finite-policy APMD targets and squared-loss identities (2611.14467).

Exact numerical components, not an empirical PPO/Kimi trainer or a proof of the
paper's global finite-sample convergence guarantees. CPU only.
"""
from __future__ import annotations

import math
import numpy as np

REQUIRES_GPU_VALIDATION = False


def _policy(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=np.float64)
    if values.ndim != 2 or min(values.shape) < 1 or not np.isfinite(values).all() or np.any(values <= 0) or not np.allclose(values.sum(-1), 1., atol=1e-12, rtol=1e-12):
        raise ValueError("strictly positive normalized [prompt,response] policy required")
    return values


def _eta(value: float) -> None:
    if not math.isfinite(value) or value <= 0:
        raise ValueError("finite positive eta required")


def mirror_step(reference: np.ndarray, rewards: np.ndarray, eta: float) -> np.ndarray:
    """Eq. 13 exact target proportional to reference * exp(eta * reward)."""
    reference = _policy(reference)
    rewards = np.asarray(rewards, dtype=np.float64)
    _eta(eta)
    if rewards.shape != reference.shape or not np.isfinite(rewards).all():
        raise ValueError("finite aligned rewards required")
    logits = np.log(reference) + eta * (rewards - rewards.max(-1, keepdims=True))
    if not np.isfinite(logits).all():
        raise ValueError("reward scale overflows finite target arithmetic")
    logits -= logits.max(-1, keepdims=True)
    result = np.exp(logits)
    result /= result.sum(-1, keepdims=True)
    if np.any(result == 0):
        raise ValueError("numerical underflow would lose full support")
    return result


def exact_reset_path(base: np.ndarray, rewards: np.ndarray, eta: float, outer_steps: int) -> np.ndarray:
    """Exact special case of APMD: every next target uses the latest policy.

    Unlike approximate inner optimization, all responses/rewards are enumerated.
    This cannot claim the online sample-complexity guarantees of the paper.
    """
    if type(outer_steps) is not int or outer_steps < 1:
        raise ValueError("positive integer outer_steps required")
    path = [_policy(base).copy()]
    for _ in range(outer_steps):
        path.append(mirror_step(path[-1], rewards, eta))
    return np.stack(path)


def squared_losses(candidate: np.ndarray, reference: np.ndarray, rewards: np.ndarray, eta: float) -> dict[str, np.ndarray]:
    """Eqs. 36--37/40/42/44 with exact finite-response expectations.

    Kimi uses the mean-reward baseline and has a squared-KL bias term. Rebel's
    two responses are independent draws from the SAME reference, not winners
    and losers filtered by reward or a second draw from the base model.
    """
    candidate, reference = _policy(candidate), _policy(reference)
    rewards = np.asarray(rewards, dtype=np.float64)
    _eta(eta)
    if candidate.shape != reference.shape or rewards.shape != candidate.shape or not np.isfinite(rewards).all():
        raise ValueError("aligned finite policies and rewards required")
    log_ratio = (np.log(candidate) - np.log(reference)) / eta
    mean_ratio = (reference * log_ratio).sum(-1, keepdims=True)
    mean_reward = (reference * rewards).sum(-1, keepdims=True)
    residual = log_ratio - (rewards - mean_reward)
    mse = (reference * (residual - mean_ratio) ** 2).sum(-1)
    kimi = (reference * residual ** 2).sum(-1)
    pair_error = residual[..., :, None] - residual[..., None, :]
    rebel = (reference[..., :, None] * reference[..., None, :] * pair_error ** 2).sum((-1, -2))
    kl_reference_candidate = -(reference * (np.log(candidate) - np.log(reference))).sum(-1)
    return {"centered_mse": mse, "kimi_mean_baseline": kimi, "rebel_on_policy": rebel,
            "kimi_squared_kl_bias": (kl_reference_candidate / eta) ** 2}


def empirical_kimipo_loss(log_probability: np.ndarray, reference_log_probability: np.ndarray,
                         sampled_rewards: np.ndarray, independent_baseline_rewards: np.ndarray, eta: float) -> float:
    """Algorithm 3 Eq. 38; baseline samples are separate from trained responses."""
    log_probability, reference_log_probability, sampled_rewards, baseline = (
        np.asarray(x, dtype=np.float64) for x in (log_probability, reference_log_probability, sampled_rewards, independent_baseline_rewards))
    _eta(eta)
    if log_probability.ndim != 1 or log_probability.size < 1 or reference_log_probability.shape != log_probability.shape or sampled_rewards.shape != log_probability.shape or baseline.ndim != 2 or baseline.shape[0] != log_probability.size or baseline.shape[1] < 1:
        raise ValueError("N trained responses and aligned N by G independent baseline rewards required")
    if not all(np.isfinite(x).all() for x in (log_probability, reference_log_probability, sampled_rewards, baseline)):
        raise ValueError("finite samples required")
    residual = (log_probability - reference_log_probability) / eta - sampled_rewards + baseline.mean(-1)
    return float(np.mean(residual ** 2))


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("finite APMD reference is CPU-only")
    rng = np.random.default_rng(seed)
    base = rng.dirichlet(np.ones(7), size=3)
    rewards = rng.uniform(-.5, 1., base.shape)
    eta, steps = .4, 6
    path = exact_reset_path(base, rewards, eta, steps)
    closed = mirror_step(base, rewards, eta * steps)
    target = path[1]
    zero = squared_losses(target, base, rewards, eta)
    candidate = rng.dirichlet(np.ones(7), size=3)
    loss = squared_losses(candidate, base, rewards, eta)
    expected_rewards = (path * rewards).sum(-1)
    best = rewards == rewards.max(-1, keepdims=True)
    optimal_mass = (path * best).sum(-1)
    checks = {
        "reset_path_matches_closed_form": bool(np.allclose(path[-1], closed)),
        "exact_mirror_reward_nondecreasing": bool(np.all(np.diff(expected_rewards, axis=0) >= -1e-12)),
        "exact_mirror_optimal_response_mass_nondecreasing": bool(np.all(np.diff(optimal_mass, axis=0) >= -1e-12)),
        "mirror_target_zero_centered_mse": bool(np.max(zero["centered_mse"]) < 1e-25),
        "rebel_is_twice_centered_mse": bool(np.allclose(loss["rebel_on_policy"], 2 * loss["centered_mse"])),
        "kimi_mean_baseline_retains_squared_kl_bias": bool(np.allclose(loss["kimi_mean_baseline"], loss["centered_mse"] + loss["kimi_squared_kl_bias"])),
        "fixed_reference_target_is_not_repeated_reset": not bool(np.allclose(path[-1], target)),
    }
    return {"seed": seed, "device": device, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"closed_form_max_error": float(np.max(np.abs(path[-1] - closed))), "centered_mse": float(loss["centered_mse"].mean()), "rebel_on_policy_loss": float(loss["rebel_on_policy"].mean()), "kimi_bias_term": float(loss["kimi_squared_kl_bias"].mean()), "exact_reward_before": float(expected_rewards[0].mean()), "exact_reward_after": float(expected_rewards[-1].mean())}, "checks": checks}
