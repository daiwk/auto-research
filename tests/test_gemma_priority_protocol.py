"""Algebra, inference-failure and fixed author-log parity; no model inference."""
import json
from pathlib import Path

import numpy as np
import pytest

from auto_research.foundation_models.gemma_priority_protocol import (
    CONDITIONS, UPSTREAM_REVISION, analyze_cells, bca_interval, diagnostic,
    four_cell_effects, tost,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/gemma_priority_protocol/ad_cells.json"
DOC = ROOT / "docs/foundation-models/2609.30716-gemma-priority-protocol/README.md"


@pytest.fixture(scope="module")
def official():
    data = json.loads(FIXTURE.read_text())
    return data, analyze_cells(data["conditions"], data["items"])


def test_exact_orthogonal_four_way_contrasts():
    # Unit bases independently establish signs and scale of all four effects.
    bases = np.array([[1, 1, 1, 1], [1, 1, -1, -1],
                      [1, -1, 1, -1], [1, -1, -1, 1]])
    np.testing.assert_array_equal(four_cell_effects(bases), np.eye(4))
    np.testing.assert_array_equal(four_cell_effects([[-1, 1, 1, -1]])[0], [0, 0, 0, -1])
    np.testing.assert_array_equal(four_cell_effects(bases+10)[:, 1:], np.eye(4)[:, 1:])


@pytest.mark.parametrize("bad", [[], [1, 2, 3, 4], [[1, 2, 3]], [[True]*4],
                                  [["1", "2", "3", "4"]], [[1, 2, np.nan, 4]],
                                  [[1, 2, np.inf, 4]]])
def test_rejects_invalid_cells(bad):
    with pytest.raises(ValueError):
        four_cell_effects(bad)


def test_fixed_log_uses_one_global_mask(official):
    data, report = official
    assert data["upstream_revision"] == UPSTREAM_REVISION
    assert report["items_kept"] == data["expected_kept"]
    assert report["items_dropped"] == data["expected_dropped"] == ["Spec/Brief"]
    assert report["per_condition_flags"]["T5b"] == ["Spec/Brief"]
    assert all(not values for name, values in report["per_condition_flags"].items() if name != "T5b")
    assert report["primary"]["n"] == 13
    assert report["sensitivity"]["n"] == 14
    assert all(condition["serial"]["n"] == 13
               for condition in report["primary"]["conditions"].values())


def test_all_paired_contrasts_match_independent_published_log(official):
    data, report = official
    # These expected aggregates come from author JSON, not the local algorithm.
    for group in ("primary", "sensitivity"):
        expected = data[f"expected_{group}"]
        for name, result in report[group]["contrasts"].items():
            if name == "A4":
                # Released FINAL.json omits A4 although current author script
                # computes it. Check the paired vector independently below.
                continue
            key = next(key for key in expected if key.startswith(name+" "))
            reference = expected[key]
            assert result["n"] == reference["n"]
            assert result["mean"] == pytest.approx(reference["mean"], abs=1e-12)
            assert result["sd"] == pytest.approx(reference["sd"], abs=1e-12)
            assert result["ci95"]["status"] == "ok"
            assert result["ci95"]["low"] == pytest.approx(reference["ci_lo"], abs=1e-10)
            assert result["ci95"]["high"] == pytest.approx(reference["ci_hi"], abs=1e-10)
        assert sum(not key.startswith("F ") for key in expected) == 18
        assert report[group]["contrasts"]["A4"]["mean"] == pytest.approx(
            report[group]["contrasts"]["A1"]["mean"]
            - report[group]["contrasts"]["A2"]["mean"], abs=1e-12)
        for condition in CONDITIONS:
            reference = expected[f"F  serial {condition}"]
            assert report[group]["conditions"][condition]["serial"]["mean"] == pytest.approx(
                reference["mean"], abs=1e-12)
    assert report["primary"]["contrasts"]["D1"]["mean"] == pytest.approx(0.774, abs=0.0005)
    # Difference-of-absolute-values is per item; abs(mean) gives a different result.
    primary = report["primary"]["conditions"]["T5b"]
    wrong = abs(primary["role"]["mean"])-abs(primary["serial"]["mean"])
    assert abs(wrong-report["primary"]["contrasts"]["D1"]["mean"]) > 0.01
    assert all(not c["serial_tost"]["equivalent"]
               for c in report["primary"]["conditions"].values())


def test_missing_condition_alignment_and_global_keep_rejected():
    cells = {name: [[0, 0, 0, 0]]*4 for name in CONDITIONS}
    ids = ["a", "b", "c", "d"]
    with pytest.raises(ValueError, match="ten"):
        analyze_cells({"T1": cells["T1"]}, ids)
    with pytest.raises(ValueError, match="unique"):
        analyze_cells(cells, ["a"]*4)
    cells["T5b"] = [[0, 0, 0, 0]]*3
    with pytest.raises(ValueError, match="counts"):
        analyze_cells(cells, ids)
    cells["T5b"] = [[3, 3, 3, 3]]*4
    with pytest.raises(ValueError, match="keep"):
        analyze_cells(cells, ids)


def test_bca_failure_and_degenerate_tost_are_not_passes(monkeypatch):
    from scipy import stats

    def failed(*args, **kwargs):
        raise RuntimeError("simulated BCa failure")

    monkeypatch.setattr(stats, "bootstrap", failed)
    assert bca_interval([1, 2, 3, 4])["status"] == "failed"
    assert tost([-0.01, 0.01, -0.02, 0.02])["equivalent"] is None
    assert tost([0]*4)["status"] == "degenerate"
    assert tost([0]*4)["equivalent"] is None
    for bad in ([1, 2], [1, np.nan, 3]):
        with pytest.raises(ValueError):
            bca_interval(bad)
    with pytest.raises(ValueError):
        bca_interval([1, 2, 3], resamples=1)


def test_nontrivial_equivalence_vs_non_equivalence():
    assert tost([-0.01, 0.01, -0.02, 0.02], resamples=199)["equivalent"] is True
    assert tost([0.3, 0.4, 0.5, 0.6], resamples=199)["equivalent"] is False


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_seeded_protocol_diagnostic(seed):
    result = diagnostic(seed)
    assert all(result["checks"].values())
    assert result["metrics"]["model_calls"] == 0
    assert result["diagnostic_only"]
    assert not result["promotion_eligible"] and not result["evolve_integrated"]
    assert not result["requires_gpu_validation"]


def test_paper_metadata_and_boundaries_documented():
    text = DOC.read_text()
    for required in ("论文信息", "https://arxiv.org/abs/2609.30716v1", "Google",
                     "2026-09-25 02:43:40 UTC", UPSTREAM_REVISION, "Apache-2.0",
                     "adapter: null", "src/auto_research/foundation_models/gemma_priority_protocol.py",
                     "原始论文总结", "核心公式", "本地复现", "未报告生产线上 A/B",
                     "不是新模型推理", "J-Lens", "退化", "paper-figure-01.png"):
        assert required in text
