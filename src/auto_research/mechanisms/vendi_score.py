"""Extracted unchanged from auto_research.foundation_latest_20260916; stable mechanism boundary."""
from __future__ import annotations

import numpy as np

def vendi_score(embeddings) -> float:
    values = np.asarray(embeddings, dtype=np.float64)
    values /= np.linalg.norm(values, axis=1, keepdims=True) + 1e-12
    spectrum = np.linalg.eigvalsh(values @ values.T / len(values))
    spectrum = np.clip(spectrum, 0.0, None)
    spectrum /= spectrum.sum() + 1e-12
    return float(np.exp(-(spectrum * np.log(spectrum + 1e-12)).sum()))

def r4t_targets(query, database, count: int = 6):
    """R4T composite set objective and a single-pass diffusion target set."""
    query = np.asarray(query, dtype=np.float64)
    database = np.asarray(database, dtype=np.float64)
    alignment = database @ query / ((np.linalg.norm(database, axis=1) * np.linalg.norm(query)) + 1e-12)
    selected = [int(np.argmax(alignment))]
    while len(selected) < min(count, len(database)):
        chosen = database[selected]
        redundancy = np.max(database @ chosen.T, axis=1)
        reward = 0.65 * alignment - 0.35 * redundancy
        reward[selected] = -np.inf
        selected.append(int(np.argmax(reward)))
    targets = database[selected]
    return targets, {
        "alignment": float(alignment[selected].mean()),
        "vendi_score": vendi_score(targets),
        "single_pass_targets": float(len(targets)),
    }
