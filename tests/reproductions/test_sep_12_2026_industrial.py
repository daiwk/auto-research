from pathlib import Path

import numpy as np

from auto_research.reproductions.latest_20260912 import bid_aware_mask, sketch_prototypes
from auto_research.reproductions.registry import get_adapter


def test_sep_12_adapters_have_full_text_online_evidence_and_execute():
    for key in ("unirec", "sequenceo1", "baff"):
        adapter = get_adapter(key)
        assert adapter.paper.has_online_ab
        assert adapter.paper.online_ab[0].source_location
        result = adapter.run(Path("data"), 42)
        assert result["manifest_ref"] == f"reproduction:{key}"


def test_baff_implements_strict_two_axis_filter():
    keep, d_ad, d_bp = bid_aware_mask(
        [0, 3, 1], [1.0, 1.0, 1.0], [1.0, 0.8, 0.2], 10, 0.2, 0.5
    )
    assert keep.tolist() == [True, False, False]
    assert np.all((0 <= d_ad) & (d_ad < 1))
    assert np.all((0 <= d_bp) & (d_bp < 1))


def test_sketch_attention_has_fixed_budget():
    rng = np.random.default_rng(42)
    assert sketch_prototypes(rng.normal(size=(100, 8)), budget=4).shape == (4, 8)
