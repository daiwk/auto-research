import numpy as np
import pytest
import hashlib
import json
from pathlib import Path

from auto_research.post_training import epro
from auto_research.reproductions import larf_components as larf


def finite_difference(function, value):
    answer = np.zeros_like(value)
    for coordinate in np.ndindex(value.shape):
        delta = np.zeros_like(value)
        delta[coordinate] = 1e-6
        answer[coordinate] = (function(value+delta)-function(value-delta))/(2e-6)
    return answer


@pytest.mark.parametrize("head_size", [None, 2, 5])
def test_epro_exact_detached_gradient_and_head_tail(head_size):
    rng = np.random.default_rng(31)
    old, execution, current = rng.normal(size=(3, 3, 5))
    batch = epro.prepare_update(old, execution, current, [0, 2, 4], [1., -.7, .2],
                                mask=[True, False, True], head_size=head_size, scale=.8)
    result = epro.loss_gradient(current, batch)
    numerical = finite_difference(lambda z: epro.loss_gradient(z, batch)["loss"], current)
    np.testing.assert_allclose(result["gradient"], numerical, atol=1e-9)
    np.testing.assert_allclose(result["gradient"].sum(axis=1), 0, atol=1e-15)
    assert np.all(result["gradient"][1] == 0)
    # Equation 2's transported distribution must match explicit probabilities.
    p, q = np.exp(batch.old_training_logp), np.exp(batch.execution_anchor_logp)
    u = np.exp(current-current.max(axis=1, keepdims=True))
    u /= u.sum(axis=1, keepdims=True)
    expected = q*u/p
    expected /= expected.sum(axis=1, keepdims=True)
    np.testing.assert_allclose(result["transported_probabilities"], expected, atol=1e-15)
    assert not batch.coefficients.flags.writeable


def test_epro_outward_only_attenuation_and_stop_gradient_contract():
    old = np.zeros((3, 3))
    current = np.tile([1., -.3, -.7], (3, 1))
    batch = epro.prepare_update(old, old, current, [0, 0, 1], [1., -1., -1.], threshold=0., scale=.5)
    assert batch.attenuation[0] < 1
    assert batch.attenuation[1] == 1  # Negative advantage, increasing probability: inward.
    assert batch.attenuation[2] < 1
    # Differentiating a re-prepared loss also differentiates the gate/weight,
    # which is explicitly NOT the EPRO gradient in Eq.11.
    numerical_wrong = finite_difference(lambda z: epro.loss_gradient(z, epro.prepare_update(
        old, old, z, [0, 0, 1], [1., -1., -1.], threshold=0., scale=.5))["loss"], current)
    assert np.max(np.abs(numerical_wrong-epro.loss_gradient(current, batch)["gradient"])) > .01


def test_epro_reductions_shift_and_offset_invariance():
    old = np.array([[.3, -.1, .8, .2]])
    execution = np.array([[.1, .6, -.4, .7]])
    current = np.array([[-.1, .2, .9, -.3]])
    at_anchor = epro.prepare_update(old, execution, old, [2], [1.])
    assert at_anchor.policy_shift[0] == 0
    matched = epro.prepare_update(old, old, current, [2], [1.])
    shifted = epro.prepare_update(old+9, execution-3, current+5, [2], [1.])
    original = epro.prepare_update(old, execution, current, [2], [1.])
    np.testing.assert_allclose(epro.loss_gradient(current, original)["gradient"],
                               epro.loss_gradient(current+5, shifted)["gradient"], atol=1e-15)
    np.testing.assert_allclose(epro.loss_gradient(current, matched)["transported_probabilities"],
                               np.exp(epro._logsoftmax(current)))


@pytest.mark.parametrize("kwargs", [{"cap": 0}, {"scale": 0}, {"head_size": 0}, {"head_size": True}, {"mask": [False]}])
def test_epro_rejects_invalid_inputs(kwargs):
    with pytest.raises(ValueError):
        epro.prepare_update([[0., 1.]], [[1., 0.]], [[.5, .2]], [0], [1.], **kwargs)


def test_larf_ordinal_reward_and_group_ranking_boundaries():
    gold = np.tile([0, 2, 5], (5, 1)).T.astype(np.uint8)
    predicted = gold[::-1].copy()
    np.testing.assert_allclose(larf.attribute_reward(gold, predicted, weights=np.ones(5)),
                               [5*np.exp(-5), 5., 5*np.exp(-5)])
    ranking = larf.listwise_reward([0, 0, 5], [0, 0, 5], mean_group_size=9.)
    np.testing.assert_array_equal(ranking["comparable_pairs_per_document"], [1, 1, 2])
    np.testing.assert_allclose(ranking["reward"], .5)
    np.testing.assert_allclose(larf.listwise_reward([0, 2, 5], [1, 1, 1], mean_group_size=3.)["reward"], 0)
    with pytest.raises(ValueError, match="undefined"):
        larf.listwise_reward([2, 2], [0, 5], mean_group_size=3.)
    r = larf.combined_reward(gold, gold, weights=np.ones(5), rule_consistent=[True, False, True], mean_group_size=3.)
    np.testing.assert_array_equal(r["rule"], [1, -1, 1])
    np.testing.assert_allclose(r["total"], [7, 5, 7])


def test_larf_margin_full_logit_gradient_excludes_ambiguous_positions():
    rng = np.random.default_rng(17)
    logits = rng.normal(size=(4, 3, 11))
    mask = np.array([[False, True, False], [True, False, False], [True, True, False], [False, False, True]])
    labels = [0, 3, 2, 9]
    digits = [1, 3, 5, 7, 8, 10]
    result = larf.terminal_margin(logits, labels, mask, digit_indices=digits)
    numerical = finite_difference(lambda z: larf.terminal_margin(z, labels, mask, digit_indices=digits)["loss"], logits)
    np.testing.assert_allclose(result["gradient"], numerical, atol=1e-8)
    np.testing.assert_array_equal(result["valid"], [True, True, False, False])
    assert not np.any(result["gradient"][:, :, [0, 2, 4, 6, 9]])
    assert not np.any(result["gradient"][2:])
    with pytest.raises(ValueError, match="empty"):
        larf.terminal_margin(logits, [8]*4, mask, digit_indices=digits)


def test_larf_hinge_saturation_ties_and_local_subgradient():
    scores = np.zeros((1, 1, 6))
    result = larf.terminal_margin(scores, [0], [[True]], digit_indices=list(range(6)))
    np.testing.assert_array_equal(result["gradient"][0, 0], [-1, 1, 0, 0, 0, 0])
    scores[0, 0, 0] = 1.
    assert not np.any(larf.terminal_margin(scores, [0], [[True]], digit_indices=list(range(6)))["gradient"])


def test_larf_dual_head_loss_gradient_and_mask():
    rng = np.random.default_rng(2)
    cls, gen = rng.normal(size=(2, 5, 6)), rng.normal(size=(2, 3, 8))
    labels = rng.integers(0, 6, size=(2, 5))
    targets = rng.integers(0, 8, size=(2, 3))
    mask = np.array([[True, True, False], [True, False, False]])
    kwargs = {"classification_weight": .3, "generation_weight": .7}
    result = larf.dual_head_objective(cls, labels, gen, targets, mask, **kwargs)
    numerical_cls = finite_difference(lambda z: larf.dual_head_objective(z, labels, gen, targets, mask, **kwargs)["loss"], cls)
    numerical_gen = finite_difference(lambda z: larf.dual_head_objective(cls, labels, z, targets, mask, **kwargs)["loss"], gen)
    np.testing.assert_allclose(result["classification_gradient"], numerical_cls, atol=1e-8)
    np.testing.assert_allclose(result["generation_gradient"], numerical_gen, atol=1e-8)
    assert not np.any(result["generation_gradient"][~mask])
    removed = larf.dual_head_objective(cls, labels, gen, targets, mask, generation_weight=0.)
    assert not np.any(removed["generation_gradient"])
    np.testing.assert_allclose(removed["loss"], result["classification_loss"])


@pytest.mark.parametrize("module", [epro, larf])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_cpu_diagnostics_are_explicitly_not_training(module, seed):
    result = module.diagnostic(seed)
    assert result["diagnostic_only"] and not result["training_executed"]
    assert all(result["checks"].values()), result
    assert not module.REQUIRES_GPU_VALIDATION
    with pytest.raises(ValueError):
        module.diagnostic(seed, device="cuda")


@pytest.mark.parametrize("relative", ["post-training/2611.32810-epro", "recommendation-components/2611.32125-larf"])
def test_nov25_paper_docs_have_reviewed_english_original_figure_and_metadata(relative):
    root = Path(__file__).resolve().parents[1]
    directory = root/"docs"/relative
    source = directory/"README.md"
    chinese = source.read_text()
    english = (directory/"README-en.md").read_text()
    assert f"<!-- source-sha256: {hashlib.sha256(source.read_bytes()).hexdigest()} -->" in english
    assert "[简体中文](README.md)" in english
    for required in ("## 论文信息", "首次公开日期", "公司 / 作者机构", "原作者开源代码",
                     "本地adapter / 稳定键", "本地复现代码目录", "图片来自[原论文]", "版权归原作者所有",
                     "### 核心公式", "### 结果、负控与边界", "成本过高，不复现（审查 DONE）"):
        assert required in chinese
    asset = directory/"assets/paper-figure-01.png"
    provenance = json.loads((directory/"assets/provenance.json").read_text())
    assert hashlib.sha256(asset.read_bytes()).hexdigest() == provenance["asset_sha256"]
    assert provenance["visually_reviewed_on"] == "2026-11-25"
    assert json.loads((directory/"metrics/component-cpu-seeds42-44.json").read_text())["diagnostic_only"]
