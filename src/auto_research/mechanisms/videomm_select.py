"""Extracted unchanged from auto_research.foundation_latest_20260916_followup; stable mechanism boundary."""
from __future__ import annotations

import numpy as np

def videomm_select(tokens, query, group_size: int = 4, keep_groups: int = 2, consensus_margin: float = 0.08):
    """VideoMM macro proxy selection followed by adaptive micro activation."""
    tokens = np.asarray(tokens, dtype=np.float64)
    query = np.asarray(query, dtype=np.float64)
    if tokens.ndim != 2 or tokens.shape[1] != len(query):
        raise ValueError("tokens must be [N,D] and query must be [D]")
    groups = np.array_split(np.arange(len(tokens)), max(1, int(np.ceil(len(tokens) / group_size))))
    macro = np.stack([tokens[group].mean(axis=0) for group in groups])
    scores = macro @ query / ((np.linalg.norm(macro, axis=1) * np.linalg.norm(query)) + 1e-12)
    order = np.argsort(scores)[::-1]
    chosen = order[: max(1, min(int(keep_groups), len(groups)))]
    margin = float(scores[order[0]] - scores[order[1]]) if len(order) > 1 else 1.0
    # Ambiguous macro consensus recruits one extra high-fidelity region.
    if margin < consensus_margin and len(chosen) < len(groups):
        chosen = order[: len(chosen) + 1]
    indices = np.concatenate([groups[index] for index in chosen])
    return tokens[indices], indices, {
        "macro_groups": float(len(groups)),
        "activated_micro_tokens": float(len(indices)),
        "retained_fraction": float(len(indices) / max(1, len(tokens))),
        "consensus_margin": margin,
    }
