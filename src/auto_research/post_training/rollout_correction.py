from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class RolloutCorrection:
    ratios: np.ndarray
    weights: np.ndarray
    kept: np.ndarray
    adjusted: np.ndarray


def truncated_importance_weights(
    training_probabilities: np.ndarray,
    rollout_probabilities: np.ndarray,
    maximum: float = 2.0,
) -> RolloutCorrection:
    """Apply one-sided TIS to the training-to-rollout probability ratio."""

    if maximum <= 0:
        raise ValueError("maximum must be positive")
    ratios = training_inference_ratios(
        training_probabilities, rollout_probabilities
    )
    adjusted = ratios > maximum
    return RolloutCorrection(
        ratios=ratios,
        weights=np.minimum(ratios, maximum),
        kept=np.ones_like(ratios, dtype=bool),
        adjusted=adjusted,
    )


def icepop_weights(
    training_probabilities: np.ndarray,
    rollout_probabilities: np.ndarray,
    lower: float = 0.5,
    upper: float = 5.0,
) -> RolloutCorrection:
    """Mask both tails of the training-to-rollout ratio without clamping."""

    if lower <= 0 or upper < lower:
        raise ValueError("IcePop bounds must satisfy 0 < lower <= upper")
    ratios = training_inference_ratios(
        training_probabilities, rollout_probabilities
    )
    kept = (ratios >= lower) & (ratios <= upper)
    return RolloutCorrection(
        ratios=ratios,
        weights=np.where(kept, ratios, 0.0),
        kept=kept,
        adjusted=~kept,
    )


def training_inference_ratios(
    training_probabilities: np.ndarray,
    rollout_probabilities: np.ndarray,
) -> np.ndarray:
    training = np.asarray(training_probabilities, dtype=np.float64)
    rollout = np.asarray(rollout_probabilities, dtype=np.float64)
    if training.shape != rollout.shape:
        raise ValueError("training and rollout probabilities must have the same shape")
    if np.any(training < 0) or np.any(rollout < 0):
        raise ValueError("probabilities must be non-negative")
    if not np.isclose(training.sum(), 1.0) or not np.isclose(rollout.sum(), 1.0):
        raise ValueError("training and rollout probabilities must each sum to one")
    return training / np.maximum(rollout, 1e-12)


def rollout_engine_probabilities(
    features: np.ndarray,
    rollout_weights: np.ndarray,
) -> np.ndarray:
    """Create a deterministic serving view with numerical and router mismatch."""

    training_logits = features @ rollout_weights
    signature_direction = np.linspace(
        -0.25, 0.25, features.shape[1], dtype=np.float64
    )
    signature = features @ signature_direction
    signature = (signature - signature.mean()) / (signature.std() + 1e-12)
    engine_delta = 0.08 * signature
    router_choice = int(np.argmax(features[:, -1] + 0.1 * features[:, 2]))
    engine_delta[router_choice] += 2.4
    shifted = training_logits + engine_delta
    shifted -= shifted.max()
    exponent = np.exp(shifted)
    return exponent / exponent.sum()
