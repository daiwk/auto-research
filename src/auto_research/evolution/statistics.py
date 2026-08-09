from __future__ import annotations

from collections.abc import Mapping, Sequence

import numpy as np


def mean_with_std(rows: Sequence[Mapping[str, float]]) -> dict[str, float]:
    """Return per-seed means and population stds using stable ``*_std`` keys."""

    if not rows:
        raise ValueError("at least one seed result is required")
    result: dict[str, float] = {}
    for key in rows[0]:
        values = np.asarray([row[key] for row in rows], dtype=np.float64)
        result[key] = float(values.mean())
        result[f"{key}_std"] = float(values.std(ddof=1)) if len(values) > 1 else 0.0
    return result
