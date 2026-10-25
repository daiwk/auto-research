"""Independent references/negative controls for six bounded historical components."""
from copy import deepcopy
import itertools
import hashlib
import json
import math
from pathlib import Path

import pytest
import torch
from torch.nn import functional as F

from auto_research.multimodal.cue2narrate_drl import description_ranking_loss
from auto_research.post_training.polaris_hri import hri_advantages, hri_grpo_loss
from auto_research.foundation_models.taskpress import taskpress_scores, symmetric_value_scale, prune_taskpress
from auto_research.foundation_models.interpolated_null_calibration import interpolated_null_calibration
from auto_research.foundation_models.combinatorial_watermark import biased_probabilities, pattern_statistics, detect
from auto_research.evaluation import xlgobench as xl
from auto_research.foundation_models.mechanistic_etm import MechanisticETM, topic_steering_vector, replace_topic_component


def test_drl_is_mean_log_likelihood_not_sequence_sum_or_margin_subtraction():
    p = torch.tensor([[[1., 2.], [2., 1.], [9., -9.]]], dtype=torch.float64, requires_grad=True)
    n = torch.tensor([[[1., 0.]] * 4], dtype=torch.float64, requires_grad=True)
    yp, yn = torch.tensor([[1, 0, -100]]), torch.tensor([[1, 1, 1, 1]])
    result = description_ranking_loss(p, yp, n, yn)
    pos = (p[0, 0].log_softmax(0)[1] + p[0, 1].log_softmax(0)[0]) / 2
    neg = n.log_softmax(-1)[0, :, 1].mean()
    oracle = -2 * pos - .2 * F.logsigmoid((pos - neg) / .5)
    torch.testing.assert_close(result["loss"], oracle)
    assert not torch.allclose(result["ranking"], F.softplus(-(2 * pos - 4 * neg) / .5))
    assert not torch.allclose(result["ranking"], F.softplus(-(pos - neg - .5)))
    gp, gn = torch.autograd.grad(result["loss"], (p, n))
    assert (gp[0, 2] == 0).all() and gn.norm() > 0
    doubled = description_ranking_loss(p, yp, n.repeat(1, 2, 1), yn.repeat(1, 2))
    torch.testing.assert_close(result["ranking"], doubled["ranking"])


@pytest.mark.parametrize("issue", ["empty", "wrong_label", "nan", "temperature"])
def test_drl_rejects_invalid_targets(issue):
    p, n, yp, yn = torch.zeros(1, 2, 3), torch.zeros(1, 2, 3), torch.tensor([[1, 2]]), torch.tensor([[1, 2]])
    kwargs = {}
    if issue == "empty": yp.fill_(-100)
    if issue == "wrong_label": yn[0, 0] = 4
    if issue == "nan": p[0, 0, 0] = float("nan")
    if issue == "temperature": kwargs["temperature"] = 0
    with pytest.raises(ValueError): description_ranking_loss(p, yp, n, yn, **kwargs)


def test_hri_sample_std_policy_only_and_linear_warmup():
    rewards = torch.tensor([[0., 1., 2., 3., 4.]], dtype=torch.float64, requires_grad=True)
    ref = torch.tensor([10.], dtype=torch.float64, requires_grad=True)
    a = hri_advantages(rewards, ref, step=3)
    std = math.sqrt(2.5)
    torch.testing.assert_close(a[0, :5], (rewards.detach()[0] - 2) / (std + 1e-6))
    assert a[0, -1] == pytest.approx(.4 * 3 / 15 * 8 / (std + 1e-6))
    assert not a.requires_grad
    for step in (15, 30):
        assert hri_advantages(rewards, ref, step=step)[0, -1] == pytest.approx(.4 * 8 / (std + 1e-6))
    b = hri_advantages(rewards, ref + 100, step=3)
    torch.testing.assert_close(a[:, :5], b[:, :5])
    # A wrong all6-member normalization changes policy advantages.
    all_rewards = torch.cat((rewards.detach(), ref.detach()[:, None]), -1)
    wrong = (all_rewards - all_rewards.mean(-1, keepdim=True)) / (all_rewards.std(-1, keepdim=True) + 1e-6)
    assert not torch.allclose(a, wrong)


def test_hri_reference_is_optimized_by_same_clipped_surrogate_once():
    current = torch.tensor([[[math.log(1.4)], [math.log(.6)], [0.]]], dtype=torch.float64, requires_grad=True)
    old = torch.zeros_like(current, requires_grad=True)
    adv = torch.tensor([[1., -1., 2.]], dtype=torch.float64, requires_grad=True)
    loss = hri_grpo_loss(current, old, torch.ones_like(current, dtype=torch.bool), adv)
    assert loss.item() == pytest.approx(-(1.2 - .8 + 2) / 3)
    loss.backward()
    assert current.grad[0, 0] == 0 and current.grad[0, 1] == 0 and current.grad[0, 2] < 0
    assert old.grad is None and adv.grad is None
    with pytest.raises(ValueError, match="nonfinite"):
        hri_grpo_loss(torch.full_like(current, 1e3), old, torch.ones_like(current, dtype=torch.bool), adv)


@pytest.mark.parametrize("dtype", [torch.float64, torch.float16, torch.bfloat16])
def test_hri_extreme_clipped_ratios_and_padding_have_finite_exact_gradients(dtype):
    current = torch.tensor([[[1000., -1000.], [-1000., 1000.], [0., 1000.]]], dtype=dtype, requires_grad=True)
    old = torch.zeros_like(current, requires_grad=True)
    mask = torch.tensor([[[True, False], [True, False], [True, False]]])
    advantages = torch.tensor([[1., -1., 0.]], dtype=dtype)
    loss = hri_grpo_loss(current, old, mask, advantages)
    assert loss.item() == pytest.approx(-(1.2 - .8) / 3, abs=1e-5)
    loss.backward()
    assert torch.isfinite(current.grad).all() and (current.grad == 0).all()
    assert old.grad is None
    # Negative A with a huge positive ratio is genuinely unbounded; do not clip
    # away this original-objective failure just to get a finite value.
    with pytest.raises(ValueError, match="nonfinite"):
        hri_grpo_loss(torch.full_like(current, 1000), old, mask, torch.full_like(advantages, -1))


def test_taskpress_pooling_boundary_quantization_product_and_independent_head_budget():
    attention = torch.tensor([[[[1., 2., 3., 4.]], [[4., 3., 2., 1.]]]], dtype=torch.float64)
    values = torch.tensor([[[[7.], [14.], [21.], [28.], [1e5]], [[28.], [21.], [14.], [7.], [1e5]]]], dtype=torch.float64)
    keys = values + 1
    scales = symmetric_value_scale(values[:, :, :4])
    expected = torch.tensor([[[1., 2., 3., 7 / 3], [7 / 3, 3., 2., 1.]]], dtype=torch.float64) * scales
    torch.testing.assert_close(taskpress_scores(attention, scales, kernel_size=3), expected)
    # Count_include_pad=False would average 2 tokens at the edge, a different Eq.1.
    assert expected[0, 0, 0] == 1
    kept = prune_taskpress(keys, values, attention, context_length=4, keep=2, kernel_size=3)
    torch.testing.assert_close(kept["positions"], torch.tensor([[[2, 3], [0, 1]]]))
    assert kept["keys"].shape[-2] == 2 and kept["positions"].max() < 4
    torch.testing.assert_close(kept["values"], values.gather(-2, kept["positions"][..., None]))
    with pytest.raises(ValueError): taskpress_scores(attention, scales, kernel_size=2)
    with pytest.raises(ValueError): taskpress_scores(attention, scales * -1, kernel_size=3)


def test_three_pass_calibration_endpoints_not_no_calibration_and_finite_guards():
    q, ni, nb = torch.tensor([.9, .8]), torch.tensor([.8, .1]), torch.tensor([.1, .1])
    a = interpolated_null_calibration(q, ni, nb, weight=0)
    b = interpolated_null_calibration(q, ni, nb, weight=1)
    torch.testing.assert_close(a["scores"], q - nb)
    torch.testing.assert_close(b["scores"], q - ni)
    assert not torch.equal(a["scores"], q) and not torch.equal(a["ranking"], b["ranking"])
    torch.testing.assert_close(interpolated_null_calibration(q, ni, nb, weight=.25)["scores"], q - nb - .25 * (ni - nb))
    with pytest.raises(ValueError): interpolated_null_calibration(q, ni, nb, weight=1.1)
    with pytest.raises(ValueError): interpolated_null_calibration(q, ni[:1], nb, weight=1)
    with pytest.raises(ValueError): interpolated_null_calibration(torch.full((2,), 3e38), torch.full((2,), -3e38), nb, weight=1)


def test_combinatorial_detector_enumerates_all_cyclic_phases_and_full_interior_windows():
    pattern = [0, 2, 0, 3, 1, 2, 1, 3]
    for phase in range(len(pattern)):
        tags = [pattern[(phase + i) % 8] for i in range(32)]
        actual = pattern_statistics(tags, pattern, window=8)
        assert actual["global_score"] == 1 and set(actual["local_scores"]) == {1.}
        assert actual["local_positions"] == list(range(7, 25))
    # Exact exhaustive independent binary-sequence reference.
    for sequence in itertools.product((0, 1), repeat=5):
        result = pattern_statistics(sequence, [0, 1], window=2)
        flags = [int(sequence[i] != sequence[i + 1]) for i in range(4)]
        assert result["global_score"] == sum(flags) / 4
        assert result["local_scores"] == [(flags[i - 1] + flags[i]) / 2 for i in range(1, 4)]
    clean = [0, 1] * 8
    # Deleting2 tags in binary pattern is inherently invisible, not "perfect detection".
    deleted = clean[:4] + clean[6:]
    assert not detect(deleted, [0, 1], window=2, watermark_threshold=.9, edit_threshold=.9)["edited"]
    probs = biased_probabilities([0., 0., 0., 0.], [0, 1, 0, 1], [0, 1], step=0, strength=math.log(3))
    assert probs == pytest.approx([.375, .125, .375, .125])
    with pytest.raises(ValueError): pattern_statistics([0, 1], [0, 1], window=2)


@pytest.mark.parametrize("task", xl.TASKS)
def test_xlgo_gold_stays_in_scorer_and_response_matching_is_exact(task):
    case = xl.make_case(task, 42)
    expected = xl._solve(case)
    assert xl.score_response(case, expected)
    assert not xl.score_response(case, {"gold": expected})
    assert not xl.score_response(case, "```json\n{}\n```")
    captured = []
    result = xl.evaluate(case, lambda payload: captured.append(payload) or {})
    assert not result["correct"] and set(captured[0]) == {"task", "problem"}
    assert set(captured[0]["problem"]) == xl.FIELDS[task]
    extra = deepcopy(case)
    extra["problem"]["gold"] = expected
    with pytest.raises(ValueError): xl.evaluate(extra, lambda payload: expected)
    if task == "pr_dsa":
        assert xl.score_response(case, {"states": list(reversed(expected["states"]))})
        assert not xl.score_response(case, {"states": expected["states"][:7] + [expected["states"][0]]})
    elif task == "slt":
        wrong = deepcopy(expected)
        wrong["chain"][0] += 1
        assert not xl.score_response(case, wrong)


def test_xlgo_unique_path_and_tournament_constraints_not_heuristic_scoring():
    graph = xl.make_case("graph_sp", 44)
    path = xl._solve(graph)["path"]
    assert len(path) == 4
    # Add a second shortest path; scorer refuses an ambiguous benchmark instance.
    graph["problem"]["edges"] += [["A0004", path[2]]]
    with pytest.raises(ValueError, match="unique shortest path"): xl._solve(graph)
    rank = xl.make_case("t_rank", 44)
    assert len(rank["problem"]["edges"]) == 3 * len(rank["problem"]["nodes"])
    ordering = xl._solve(rank)["ranking"]
    assert not xl.score_response(rank, {"ranking": list(reversed(ordering))})


def test_metm_uses_frozen_sae_encoder_while_steering_uses_independent_decoder():
    class Posterior(torch.nn.Module):
        def forward(self, counts):
            return counts.new_zeros((len(counts), 2)), counts.new_zeros((len(counts), 2))
    encoder = torch.tensor([[1., 0.], [0., 2.], [-1., 1.]], dtype=torch.float64, requires_grad=True)
    decoder = torch.tensor([[0., 3.], [2., 0.], [1., -2.]], dtype=torch.float64, requires_grad=True)
    model = MechanisticETM(encoder, 2, Posterior())
    with torch.no_grad():
        model.topic_vectors.copy_(torch.tensor([[.3, -.2], [.1, .4]], dtype=torch.float64))
    counts, lengths, noise = torch.tensor([[1., 2., 0.]], dtype=torch.float64), torch.tensor([3.]), torch.zeros(1, 2, dtype=torch.float64)
    result = model(counts, lengths, noise)
    expected_beta = torch.sigmoid(model.topic_vectors @ encoder.detach().T + model.feature_bias)
    wrong_beta = torch.sigmoid(model.topic_vectors @ decoder.detach().T + model.feature_bias)
    torch.testing.assert_close(result["topic_feature_probabilities"], expected_beta)
    assert not torch.allclose(expected_beta, wrong_beta)
    probability = result["document_topics"] @ expected_beta
    oracle = -torch.distributions.Binomial(total_count=lengths[:, None], probs=probability).log_prob(counts).sum()
    torch.testing.assert_close(result["loss"], oracle)  # zero Gaussian KL fixture
    result["loss"].backward()
    assert encoder.grad is None and decoder.grad is None and model.topic_vectors.grad.norm() > 0
    direction = topic_steering_vector(expected_beta[0].detach(), decoder)
    direct = expected_beta[0].detach() @ decoder.detach()
    torch.testing.assert_close(direction, direct / direct.norm())
    activations = torch.tensor([[1., 2.]], dtype=torch.float64)
    bias = torch.tensor([.2, .3], dtype=torch.float64)
    steered = replace_topic_component(activations, direction, bias, strength=2.)
    torch.testing.assert_close((steered - bias) @ direction, torch.tensor([2.], dtype=torch.float64))
    assert not torch.allclose(steered, activations + 2 * direction)


@pytest.mark.parametrize("module", ["multimodal.cue2narrate_drl", "post_training.polaris_hri", "foundation_models.taskpress",
    "foundation_models.interpolated_null_calibration", "foundation_models.combinatorial_watermark", "evaluation.xlgobench",
    "foundation_models.mechanistic_etm"])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostics_are_bounded_scalar_mechanism_or_protocol_not_capability(module, seed):
    import importlib
    result = importlib.import_module("auto_research." + module).diagnostic(seed)
    assert result["seed"] == seed and all(type(v) is bool and v for v in result["checks"].values())
    assert all(type(v) in (float, int) and math.isfinite(v) for v in result["metrics"].values())
    assert result["metrics"]["pretrained_model_calls"] == 0


@pytest.mark.parametrize("domain,key,arxiv,version,gpu", [
    ("multimodal-models", "cue2narrate-drl", "2609.01725", "v1", True),
    ("foundation-models", "mechanistic-etm", "2507.23220", "v3", True),
    ("multimodal-models", "naijas2st", "2604.16287", "v3", False),
    ("post-training", "polaris-hri", "2606.04095", "v2", True),
    ("foundation-models", "taskpress", "2608.03276", "v2", True),
    ("foundation-models", "combinatorial-watermark", "2510.01637", "v1", False),
    ("foundation-models", "interpolated-null-calibration", "2609.17764", "v1", True),
    ("multimodal-models", "mveb", "2606.14958", "v1", False),
    ("foundation-models", "xlgobench", "2605.30788", "v1", False),
])
def test_nine_paper_metadata_figures_and_version_cost_boundaries(domain, key, arxiv, version, gpu):
    root = Path(__file__).resolve().parents[1]
    record = json.loads((root / f"src/auto_research/paper_specs/catalog/{domain}/{key}.json").read_text())
    assert record["paper_url"] == f"https://arxiv.org/abs/{arxiv}v1"
    assert record["reviewed_version_url"].endswith(arxiv + version)
    assert record["published_at"].endswith("Z")
    assert record["first_author"] and record["first_author_affiliation"]
    assert record["requires_gpu_validation"] is gpu
    assert record["full_experiment_review_done"] and record["full_experiment_status"] == "not_reproduced_high_cost"
    assert record["review_done"] and not record["automatic_retry"] and not record["automatic_implementation_queue"]
    assert not record["promotion_eligible"] and not record["evolve_integrated"]
    folder = root / "docs" / Path(record["detail_path"]).parent
    text = (folder / "README.md").read_text()
    for item in ("## 论文信息", "### 背景与主要改动", "### 核心公式", "### 论文离线与线上效果", "## 本地复现",
                 "原作者代码", "本地复现代码目录", "图片来自[原论文]", "版权归原作者所有", "成本过高，不复现（审查 DONE）"):
        assert item in text
    provenance = json.loads((folder / "assets/provenance.json").read_text())
    assert provenance["visually_verified"]
    assert hashlib.sha256((folder / "assets/paper-figure-01.png").read_bytes()).hexdigest() == provenance["image_sha256"]
    if key in ("mveb", "naijas2st"):
        assert record["implementation_status"] == "deferred_high_cost"
        assert record["local_operator"] is None and record["local_command"] is None and record["gpu_validation_artifact"] is None
    if key == "mechanistic-etm":
        assert record["verified_priority_organizations"] == ["Google Research"]
        assert "encoder" in text and "decoder" in text
