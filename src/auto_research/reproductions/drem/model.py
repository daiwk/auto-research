from __future__ import annotations

import numpy as np


def _channels(data, history) -> np.ndarray:
    recent = np.asarray(history[-8:], dtype=np.int64)
    values = np.stack(
        (
            data.transition[recent].mean(0),
            data.cosine[recent].mean(0),
            data.popularity,
        )
    )
    low = values.min(axis=1, keepdims=True)
    high = values.max(axis=1, keepdims=True)
    return (values - low) / np.maximum(high - low, 1e-9)


def build_drem(data, seed: int, perturbations: int = 24) -> dict:
    rng = np.random.default_rng(seed)
    noise_scale = np.asarray((0.18, 0.12, 0.08), dtype=np.float64)
    noise = rng.normal(
        0.0,
        noise_scale[None, :, None],
        size=(perturbations, 3, data.item_count),
    )
    return {"noise": noise, "noise_scale": noise_scale}


def score_naive(data, history) -> np.ndarray:
    channels = _channels(data, history)
    return np.asarray((0.46, 0.36, 0.18)) @ channels


def score_drem(data, state: dict, history) -> np.ndarray:
    channels = _channels(data, history)
    logits = np.log(np.clip(channels, 1e-5, 1 - 1e-5)) - np.log(
        np.clip(1 - channels, 1e-5, 1 - 1e-5)
    )
    noisy = 1.0 / (1.0 + np.exp(-np.clip(logits[None] + state["noise"], -30, 30)))

    # Feature-side correction: retain only perturbations preserving the item's
    # relative position around each objective median, then average predictions.
    clean_side = channels >= np.median(channels, axis=1, keepdims=True)
    noisy_side = noisy >= np.median(noisy, axis=2, keepdims=True)
    preserve = noisy_side == clean_side[None]
    preserved_sum = (noisy * preserve).sum(axis=0)
    preserved_count = preserve.sum(axis=0)
    consistent = preserved_sum / np.maximum(preserved_count, 1)

    # Supervision-side correction: estimate pair-label flip probability and
    # invert symmetric label noise risk, with clipping for numerical stability.
    flip = np.mean(~preserve, axis=0)
    flip = np.clip(flip, 0.0, 0.45)
    corrected = np.clip((channels - flip) / np.maximum(1 - 2 * flip, 0.1), 0.0, 1.0)
    robust_channels = 0.55 * corrected + 0.45 * consistent
    return np.asarray((0.46, 0.36, 0.18)) @ robust_channels


def robustness_diagnostics(data, state: dict, history) -> dict[str, float]:
    clean = score_naive(data, history)
    channels = _channels(data, history)
    noisy_channels = np.clip(channels[None] + state["noise"], 0.0, 1.0)
    naive = np.einsum("pci,c->pi", noisy_channels, np.asarray((0.46, 0.36, 0.18)))
    robust = score_drem(data, state, history)
    return {
        "noise_perturbations": int(len(state["noise"])),
        "naive_mean_absolute_drift": float(np.abs(naive - clean[None]).mean()),
        "robust_mean_absolute_drift": float(np.abs(robust - clean).mean()),
        "risk_flip_probability_mean": float(
            np.mean(
                (noisy_channels >= np.median(noisy_channels, axis=2, keepdims=True))
                != (channels >= np.median(channels, axis=1, keepdims=True))[None]
            )
        ),
    }
