from __future__ import annotations

from datetime import datetime, timedelta, timezone

import numpy as np
import pytest

from auto_research.evaluation.layered_engagement import (
    Contrast, Interval, audit, paired_scoring_interval,
)


NOW = datetime(2026, 9, 21, tzinfo=timezone.utc)


def row(experiment: str, item: str, offline: Interval, online: Interval) -> Contrast:
    return Contrast(experiment, item, NOW, NOW + timedelta(days=1),
                    NOW + timedelta(days=2), offline, online)


def test_interval_audit_counts_wrong_direction_and_cluster_macro():
    rows = (
        row("a", "1", Interval(0.1, 0.3), Interval(0.2, 0.4)),
        row("a", "2", Interval(-0.3, -0.1), Interval(0.2, 0.4)),
        row("a", "3", Interval(-0.1, 0.1), Interval(-0.4, -0.2)),
        row("b", "1", Interval(0.2, 0.4), Interval(-0.2, 0.2)),
    )
    result = audit(rows)
    assert result["correct_decisive"] == 1
    assert result["wrong_direction"] == 1
    assert result["abstained"] == 1
    assert result["contrast_micro_f1"] == pytest.approx(2 / 6)
    assert result["experiment_macro_f1"] == pytest.approx(0.2)
    assert result["power_aware_precision"] == pytest.approx(0.5)


def test_paired_bootstrap_and_pre_exposure_gate():
    interval = paired_scoring_interval(np.zeros(100), np.ones(100) * 0.2,
                                       scale=2.0, draws=100, seed=7)
    assert interval.lower == pytest.approx(0.4)
    assert interval.upper == pytest.approx(0.4)
    with pytest.raises(ValueError, match="predate"):
        Contrast("a", "x", NOW, NOW + timedelta(days=2),
                 NOW + timedelta(days=1), Interval(0, 1), Interval(0, 1))
    with pytest.raises(ValueError, match="duplicate"):
        audit((row("a", "x", Interval(0, 1), Interval(0, 1)),
               row("a", "x", Interval(0, 1), Interval(0, 1))))
