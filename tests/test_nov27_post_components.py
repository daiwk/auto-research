import hashlib
import json
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from auto_research.post_training import cafa, elpsd


def test_cafa_mirror_mean_cancellation_does_not_cancel_covariance():
    bank = {"p": [("A", "B"), ("B", "A")]}
    mean = cafa.plan_report(bank, [[-1, 1]])
    cov = cafa.plan_report(bank, [[-1, 1]], mode="mean+cov")
    assert not mean.required and len(cov.required) == 2
    calls = []
    def scorer(prompt, response):
        calls.append((prompt, response))
        return {"A": 2., "B": 5.}[response]
    assert cafa.recover(mean, {}, scorer_version="v1", scorer=scorer)["mean"] == [0.]
    assert calls == []
    result = cafa.recover(cov, {}, scorer_version="v1", scorer=scorer)
    assert result["per_prompt_covariance"]["p"] == [[18.]]
    assert result["covariance"] == [[9.]]


def test_cafa_multiple_prompts_original_weights_and_zero_draws():
    bank = {"p": [("A", "A"), ("A", "B"), ("B", "A")], "q": [("A", "B"), ("A", "B")]}
    weights = {"p": Fraction(1, 3), "q": Fraction(2, 3)}
    plan = cafa.plan_report(bank, [[-1, 1], [1, 0]], mode="mean+cov", weights=weights)
    out = cafa.recover(plan, {}, scorer_version="v1", scorer=lambda p, y: 2. if y == "A" else 5.)
    np.testing.assert_allclose(out["mean"], [2., 7/3])
    np.testing.assert_allclose(out["per_prompt_covariance"]["p"], [[9., -4.5], [-4.5, 3.]])
    np.testing.assert_allclose(out["covariance"], np.array([[9., -4.5], [-4.5, 3.]])/27)


def test_cafa_exact_rational_coefficients_not_tolerance_cancellation():
    bank = {"p": [("A", "A", "A")]}
    assert not cafa.plan_report(bank, [["0.1", "0.2", "-0.3"]]).required
    tiny = cafa.plan_report(bank, [["0.1", "0.2", "-0.30000000000000001"]])
    assert tiny.required == frozenset({("p", "A")})


def test_cafa_scoring_identity_is_exact_prompt_text_and_scorer_version():
    bank = {"P": [("A", "a"), ("A", "A ")], "p": [("A", "a")]}
    plan = cafa.plan_report(bank, [[-1, 1]])
    assert len(plan.cache_support) == 5  # No lowercasing, trimming or cross-prompt merge.
    cache = {}
    one = cafa.recover(plan, cache, scorer_version="v1", scorer=lambda p, y: len(y))
    two = cafa.recover(plan, cache, scorer_version="v1", scorer=lambda p, y: 100.)
    three = cafa.recover(plan, cache, scorer_version="v2", scorer=lambda p, y: 100.)
    assert one["new_score_calls"] == 5 and two["new_score_calls"] == 0 and three["new_score_calls"] == 5


def test_cafa_missing_feedback_is_not_zero_or_silently_imputed():
    plan = cafa.plan_report({"p": [("A", "B"), ("B", "A")]}, [[-1, 1]], mode="mean+cov")
    def unavailable(p, y):
        raise RuntimeError("not available")
    incomplete = cafa.recover(plan, {}, scorer_version="v", scorer=unavailable)
    assert incomplete["status"] == "incomplete" and incomplete["mean"] is None
    bounded = cafa.recover(plan, {}, scorer_version="v", score_range=(0., 1.))
    assert bounded["mean_bounds"] == ([0.], [0.]) and bounded["covariance"] is None
    with pytest.raises(ValueError, match="at least two"):
        cafa.plan_report({"p": [("A", "B")]}, [[-1, 1]], mode="mean+cov")


def test_elpsd_response_weighting_mask_and_logit_offset_invariance():
    rng = np.random.default_rng(6)
    early, last, student = rng.normal(size=(3, 2, 3, 4))
    teacher = elpsd.extrapolated_teacher(early, last)
    mask = np.array([[True, True, True], [True, False, False]])
    result = elpsd.loss_gradient(student, teacher, mask=mask)
    expected = (result["per_prefix_kl"][0].mean()+result["per_prefix_kl"][1, 0])/2
    assert result["loss"] == pytest.approx(expected)
    shifted = elpsd.extrapolated_teacher(early+13, last-7)
    np.testing.assert_allclose(elpsd.loss_gradient(student+9, shifted, mask=mask)["gradient"], result["gradient"], atol=1e-14)
    assert not np.any(result["gradient"][~mask])
    np.testing.assert_allclose(result["gradient"].sum(axis=-1), 0., atol=1e-15)


def test_elpsd_frozen_teacher_and_initial_gap_versus_zero_weight():
    early, last = np.array([[[2., 0., -1.]]]), np.array([[[0., 1., -1.]]])
    teacher = elpsd.extrapolated_teacher(early, last)
    saved = teacher.logp.copy()
    early[:] = -99
    np.testing.assert_array_equal(teacher.logp, saved)
    with pytest.raises(ValueError):
        teacher.logp[0, 0, 0] = 0
    assert elpsd.loss_gradient(last, teacher)["loss"] > 0
    zero = elpsd.extrapolated_teacher(early, last, weight=0.)
    np.testing.assert_allclose(elpsd.loss_gradient(last, zero)["gradient"], 0., atol=1e-15)


@pytest.mark.parametrize("weight", [-1., float("nan"), float("inf"), True])
def test_elpsd_rejects_invalid_extrapolation(weight):
    with pytest.raises(ValueError):
        elpsd.extrapolated_teacher(np.zeros((1, 1, 2)), np.zeros((1, 1, 2)), weight=weight)


@pytest.mark.parametrize("module", [cafa, elpsd])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_cpu_diagnostics_are_finite_boolean_component_evidence(module, seed):
    out = module.diagnostic(seed)
    assert out["diagnostic_only"] and not out["training_executed"]
    assert out["evaluation_tier"] == "l1_mechanism" and not module.REQUIRES_GPU_VALIDATION
    assert all(type(v) is bool and v for v in out["checks"].values())
    assert all(type(v) in (int, float) and np.isfinite(v) for v in out["metrics"].values())
    with pytest.raises(ValueError):
        module.diagnostic(seed, device="cuda")


@pytest.mark.parametrize("paper", ["2611.31931-cafa", "2611.32452-elpsd"])
def test_nov27_post_bilingual_metadata_and_original_asset(paper):
    directory = Path(__file__).resolve().parents[1]/"docs/post-training"/paper
    cn, en = (directory/"README.md").read_bytes(), (directory/"README-en.md").read_text()
    assert f"<!-- source-sha256: {hashlib.sha256(cn).hexdigest()} -->" in en
    assert "[简体中文](README.md)" in en
    for token in ("## 论文信息", "首次公开日期", "公司 / 作者机构", "原作者开源代码", "本地adapter / 稳定键", "本地复现代码目录", "成本过高，不复现（审查 DONE）", "图片来自[原论文]", "版权归原作者所有"):
        assert token in cn.decode()
    provenance = json.loads((directory/"assets/provenance.json").read_text())
    assert hashlib.sha256((directory/"assets/paper-figure-01.png").read_bytes()).hexdigest() == provenance["asset_sha256"]
    assert provenance["visually_reviewed_on"] == "2026-11-27"
