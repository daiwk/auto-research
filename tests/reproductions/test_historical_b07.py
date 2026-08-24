from pathlib import Path

import numpy as np

from auto_research.reproductions.historical_b07 import KEYS, reproduce
from auto_research.reproductions.registry import get_adapter


def test_b07_adapters_have_distinct_executable_paper_contracts():
    assert len(KEYS) == 9
    signatures = set()
    for key in KEYS:
        adapter = get_adapter(key)
        result = reproduce(key, Path("data"), seed=42)
        assert adapter.paper.published.startswith("2026-")
        assert adapter.paper.organization
        assert 0 <= result["baseline"]["accuracy"] <= 1
        assert 0 <= result["method"]["accuracy"] <= 1
        values = [
            value for value in result["method"].values()
            if isinstance(value, (int, float))
        ]
        assert all(np.isfinite(values))
        signatures.add(tuple(sorted(result["method"])))
    assert len(signatures) == len(KEYS)

