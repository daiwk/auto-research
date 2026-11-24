import math
import hashlib
import json
from pathlib import Path
import re

import numpy as np
import pytest
from PIL import Image

from english_learning_sources import question_units

from auto_research.post_training import shpo, vopd


def test_cumulative_teacher_reward_is_masked_sum_not_length_average():
    teacher = [[-1., -2., -100.], [-1., -2., -3.]]
    reference = [[-2., -4., -1.], [-2., -4., -6.]]
    assert vopd.cumulative_teacher_rewards(teacher, reference, mask=[[True, True, False], [True]*3]).tolist() == [3., 6.]


def test_projection_is_population_correlation_and_not_raw_covariance():
    result = vopd.group_projection([0, 0, 1, 1], [-2., -1., 1., 2.])
    assert result.correlation == pytest.approx(np.corrcoef([0, 0, 1, 1], [-2., -1., 1., 2.])[0, 1])
    shifted = vopd.group_projection([0, 0, 1, 1], [100+3*x for x in [-2., -1., 1., 2.]])
    assert shifted.strength == pytest.approx(result.strength)
    assert vopd.group_projection([1, 1], [0., 2.], weight=10).strength == .25
    with pytest.raises(ValueError):
        vopd.group_projection([0, 1], [2., 2.])


@pytest.mark.parametrize("strength", [-.25, 0., .25, 2.])
def test_vopd_gradient_target_identity_and_finite_difference(strength):
    z, t, r = np.array([.3, -.4, .6]), [.7, -.2, .1], [-.2, .3, .1]
    row = vopd.local_loss_gradient(z, t, r, strength=strength)
    p, logq = row["student_probabilities"], row["target_log_probabilities"]
    residual = np.log(p)-logq
    assert row["gradient"] == pytest.approx(p*(residual-p@residual))
    for i in range(3):
        d = np.eye(3)[i]*1e-6
        numeric = (vopd.local_loss_gradient(z+d, t, r, strength=strength)["loss"]-
                   vopd.local_loss_gradient(z-d, t, r, strength=strength)["loss"])/2e-6
        assert row["gradient"][i] == pytest.approx(numeric, abs=1e-9)


def test_vopd_conditional_rb_integrates_new_token_not_observed_group():
    p, reward, correlation = np.array([.2, .3, .5]), np.array([1., -2., .4]), -.5
    first, variance = vopd.conditional_reward_gradient(p, reward, correlation=correlation, baseline=10.)
    second, _ = vopd.conditional_reward_gradient(p, reward, correlation=correlation, baseline=-8.)
    assert first == pytest.approx(correlation*p*(reward-p@reward))
    assert second == pytest.approx(first)
    assert variance > 0
    # A fixed observed group's coefficient is passed, never differentiated.
    assert vopd.local_loss_gradient([0., 0.], [1., -1.], [0., 0.], strength=0.)["gradient"].sum() == pytest.approx(0.)


def test_shpo_response_only_mean_pool_and_mask_validation():
    hidden = np.array([[[100., 200.], [1., 3.], [3., 5.]]])
    assert shpo.mean_pool_response(hidden, [[False, True, True]]).tolist() == [[2., 4.]]
    with pytest.raises(ValueError):
        shpo.mean_pool_response(hidden, [[False]*3])


def test_shpo_preserves_unit_normalization_antisymmetry_and_cycle_capacity():
    h = np.array([[1., 0.], [-.5, np.sqrt(3)/2], [-.5, -np.sqrt(3)/2]])
    v, _ = shpo.curl_embeddings(h, np.eye(2))
    assert np.linalg.norm(v, axis=1) == pytest.approx(np.ones(3))
    cycle = shpo.plane_features(v, np.roll(v, -1, axis=0))
    assert cycle[:, 0].sum() == pytest.approx(3*np.sqrt(3)/2)
    assert shpo.plane_features(np.roll(v, -1, axis=0), v) == pytest.approx(-cycle)
    # Any scalar-potential DPO edge score telescopes, unlike this plane.
    potential = np.array([.7, -.4, .1])
    assert np.sum(potential-np.roll(potential, -1)) == pytest.approx(0.)


def test_shpo_l1_subgradient_dpo_reduction_and_hidden_coupling():
    rng = np.random.default_rng(3)
    left, right, w = rng.normal(size=(2, 3)), rng.normal(size=(2, 3)), rng.normal(size=(3, 4))
    gamma = np.array([.3, -.4])
    logs = ([-2., -3.], [-3., -2.], [-2.5, -2.5], [-2.5, -2.5])
    base = shpo.loss_gradients(left, right, w, gamma, *logs, regularization=0.)
    sparse = shpo.loss_gradients(left, right, w, gamma, *logs, regularization=.02)
    assert sparse["loss"]-base["loss"] == pytest.approx(.02*.7)
    assert sparse["gamma_gradient"]-base["gamma_gradient"] == pytest.approx(.02*np.sign(gamma))
    assert np.linalg.norm(base["chosen_hidden_gradient"]) > 0
    zero = shpo.loss_gradients(left, right, w, np.zeros(2), *logs, regularization=0.)
    no_head = shpo.loss_gradients(left, right, w, gamma, *logs, alpha=0., regularization=0.)
    assert zero["loss"] == no_head["loss"]
    np.testing.assert_array_equal(no_head["chosen_hidden_gradient"], 0.)


def test_zero_projection_has_explicit_zero_embedding_backward_convention():
    row = shpo.loss_gradients([[1., 2.]], [[2., 3.]], np.zeros((2, 2)), [.2],
                               [-2.], [-3.], [-2.], [-3.])
    assert row["curl_scores"].tolist() == [0.]
    np.testing.assert_array_equal(row["projection_gradient"], 0.)
    np.testing.assert_array_equal(row["chosen_hidden_gradient"], 0.)


@pytest.mark.parametrize("call", [
    lambda: vopd.group_projection([.5, 1], [1., 2.]),
    lambda: vopd.group_projection([0, 1], [math.nan, 2.]),
    lambda: vopd.local_loss_gradient([1., 2.], [1.], [0., 1.], strength=.25),
    lambda: vopd.local_loss_gradient([1., 2.], [0., 1.], [0., 1.], strength=math.inf),
    lambda: vopd.cumulative_teacher_rewards([[-1.]], [[-1.]], mask=[[False]]),
    lambda: shpo.curl_embeddings([[1., 2.]], np.ones((2, 3))),
    lambda: shpo.curl_embeddings([[1e308, 1e308]], np.ones((2, 2))*1e308),
    lambda: shpo.curl_embeddings([[1e-320, 0.]], np.eye(2)),
    lambda: shpo.loss_gradients([[1., 2.]], [[1., 2.]], np.eye(2), [.1], [1.], [-1.], [-1.], [-1.]),
])
def test_invalid_and_overflowing_contracts_fail_closed(call):
    with pytest.raises(ValueError):
        call()


@pytest.mark.parametrize("module", [vopd, shpo])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_cpu_component_contract_and_actual_formula_gradients(module, seed):
    row = module.diagnostic(seed)
    assert row["checks"] and all(type(x) is bool and x for x in row["checks"].values())
    assert all(type(x) in (int, float) and math.isfinite(x) for x in row["metrics"].values())
    assert row["diagnostic_only"] is True and row["evaluation_tier"] == "l1_mechanism"
    assert row["training_executed"] is False and module.REQUIRES_GPU_VALIDATION is False
    with pytest.raises(ValueError):
        module.diagnostic(seed, "cuda")


def test_new_paper_metadata_figures_qa_and_reviewed_translation_fingerprints():
    root = Path(__file__).resolve().parents[1]
    audit = root/"docs/research-audits/nov24-latest"
    specs = json.loads((audit/"paper-proposals-post.json").read_text())["papers"]
    bundle = json.loads((audit/"post-authored-bundle.json").read_text())
    assert set(specs) == set(bundle["papers"]) == {"post-training:vopd", "post-training:shpo"}
    units = question_units({key: row["questions"] for key, row in bundle["papers"].items()})
    assert set(units) == set(bundle["english_question_units"])
    for uid, unit in units.items():
        english = bundle["english_question_units"][uid]
        assert english["reviewed"] is True and english["source_sha256"] == unit.source_sha256
        assert set(english["fields"]) == {"question", "answer", "example"}
    for identity, spec in specs.items():
        directory = root/"docs"/Path(spec["detail_path"]).parent
        cn = (directory/"README.md").read_text()
        en = (directory/"README-en.md").read_text()
        assert "论文信息" in cn and "原作者开源代码" in cn and "本地复现代码" in cn
        assert f"<!-- source-sha256: {hashlib.sha256(cn.encode()).hexdigest()} -->" in en
        assert "[简体中文](README.md)" in en
        headings = set(re.findall(r"^#{1,6} (.+)$", cn, re.MULTILINE))
        questions = bundle["papers"][identity]["questions"]
        assert {q["level"] for q in questions} == {"basics", "mechanism", "comparison", "implementation"}
        assert all(set(q["source_sections"]) <= headings for q in questions)
        provenance = json.loads((directory/"assets/provenance.json").read_text())
        png = directory/"assets/paper-figure-01.png"
        assert hashlib.sha256(png.read_bytes()).hexdigest() == provenance["image_sha256"]
        assert provenance["visually_reviewed"] and not provenance["scientific_content_modified"]
        assert Image.open(png).width >= 800
        assert spec["adapter"] is None and spec["requires_gpu_validation"] is False
        assert spec["full_experiment_review_done"] and not spec["automatic_retry"]
