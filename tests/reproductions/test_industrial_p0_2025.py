from pathlib import Path

import numpy as np

from auto_research.reproductions.industrial_p0_2025 import (
    SPECS,
    build_mechanism,
)
from auto_research.reproductions.registry import get_adapter


class _Data:
    item_count = 48
    train = tuple(
        tuple((user * 3 + offset * 5) % 48 for offset in range(12))
        for user in range(24)
    )
    validation = tuple((user * 3 + 13) % 48 for user in range(24))
    test = tuple((user * 3 + 17) % 48 for user in range(24))
    features = np.eye(48, 12, dtype=np.float32)
    popularity = np.arange(1, 49, dtype=np.float32)


def test_all_industrial_p0_adapters_preserve_online_evidence_and_dates():
    expected = {
        "mim": ("2025-02-01", True),
        "filterllm": ("2025-02-24", False),
        "fuxi-alpha": ("2025-02-05", True),
        "recgpt-v2": ("2025-12-16", False),
        "higr": ("2025-12-31", False),
        "drl-put": ("2025-09-05", False),
        "adaf2m2": ("2025-01-27", False),
        "mgoe": ("2025-06-12", True),
        "click-a-buy-b": ("2025-07-20", False),
    }
    for key, (published, has_code) in expected.items():
        adapter = get_adapter(key)
        assert adapter.paper.published == published
        assert adapter.paper.has_online_ab
        assert bool(adapter.paper.code_url) is has_code


def test_each_paper_executes_a_distinct_core_mechanism():
    diagnostics = {}
    for key in SPECS:
        baseline, method, diagnostic = build_mechanism(key, _Data(), seed=42)
        baseline_scores = baseline(0, _Data.train[0])
        method_scores = method(0, _Data.train[0])
        assert baseline_scores.shape == method_scores.shape == (_Data.item_count,)
        assert np.isfinite(method_scores).all()
        assert not np.allclose(baseline_scores, method_scores)
        diagnostics[key] = diagnostic

    assert "masked_reconstruction_mse" in diagnostics["mim"]
    assert "distribution_rank" in diagnostics["filterllm"]
    assert diagnostics["fuxi_alpha"]["channels"] == [
        "temporal",
        "semantic",
        "popularity",
    ]
    assert "constrained_policy_kl" in diagnostics["recgpt_v2"]
    assert diagnostics["higr"]["coarse_codes"] > 1
    assert diagnostics["drl_put"]["logged_policy_updates"] == 18
    assert diagnostics["adaf2m2"]["masked_forwards"] == 3
    assert len(diagnostics["mgoe"]["macro_task_graph"]) == 3
    assert diagnostics["click_a_buy_b"]["cross_item_pairs"] > 0


def test_generated_metric_artifacts_exist_for_every_paper():
    roots = {
        "mim": "2502.00321-mim",
        "filterllm": "2502.16924-filterllm",
        "fuxi-alpha": "2502.03036-fuxi-alpha",
        "recgpt-v2": "2512.14503-recgpt-v2",
        "higr": "2512.24787-higr",
        "drl-put": "2509.05292-drl-put",
        "adaf2m2": "2501.15816-adaf2m2",
        "mgoe": "2506.10520-mgoe",
        "click-a-buy-b": "2507.15113-click-a-buy-b",
    }
    repository = Path(__file__).resolve().parents[2]
    for slug in roots.values():
        metrics = (
            repository
            / "docs"
            / "reproductions"
            / slug
            / "metrics"
            / "movielens-1m-seed42.json"
        )
        assert metrics.exists()
