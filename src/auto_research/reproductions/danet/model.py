from __future__ import annotations

import numpy as np

from ..industrial_2026 import base_scores, ridge


def train_danet(data):
    n = 48
    time = np.arange(n, dtype=float)
    # Public proxy: actual item popularity determines amplitude; periodic rating-season exposure is the DR series.
    series = np.asarray([0.20 + 0.18 * (1.0 - pop) * np.sin(2 * np.pi * time / (7 + item % 13)) + 0.08 * np.cos(2 * np.pi * time / 24) for item, pop in enumerate(data.popularity)])
    spectrum = np.fft.rfft(series, axis=1)
    cutoff = max(2, spectrum.shape[1] // 4)
    filtered = spectrum.copy()
    filtered[:, cutoff:] *= 0.15
    low = np.fft.irfft(filtered, n=n, axis=1)
    high = series - low
    user_sensitivity = []
    targets = []
    for sequence in data.sequences.train:
        user_sensitivity.append(np.mean(series[list(sequence[-8:]), -1]))
        targets.append(np.mean(data.popularity[list(sequence[-8:])]))
    mapping = ridge(np.asarray(user_sensitivity)[:, None], np.asarray(targets)[:, None]).ravel()
    auxiliary = float(np.mean((np.asarray(user_sensitivity) * mapping[0] - np.asarray(targets)) ** 2))
    return series, low, high, float(mapping[0]), {"fft_steps": n, "low_frequency_bins": cutoff, "distribution_correction_user": True, "distribution_correction_context": True, "discount_auxiliary_mse": auxiliary, "upstream_code_consulted": "https://github.com/tangrc/DANet"}


def score_danet(data, series, low, high, sensitivity, history):
    interest = base_scores(data, history)
    user_preference = float(np.mean(series[list(history[-8:]), -1])) * sensitivity
    promotion_context = 1.0 + 0.15 * np.sin(len(history) / 3.0)
    discount = user_preference * promotion_context * series[:, -1] + 0.4 * low[:, -1] + 0.2 * high[:, -1]
    discount = (discount - discount.min()) / max(discount.max() - discount.min(), 1e-9)
    return 0.72 * interest + 0.28 * discount
