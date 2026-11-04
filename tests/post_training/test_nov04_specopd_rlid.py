from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import pytest
import torch

from auto_research.post_training import rlid, specopd


def test_tree_preserves_ancestry_positions_and_predecessor_readout():
    tree = specopd.proposal_tree(5, torch.tensor([1, 3]), 3)
    assert tree.parent.tolist() == [-1, 0, 1, 2, 3, 1, 5, 6, 3, 8, 9]
    assert tree.positions.tolist() == [0, 1, 2, 3, 4, 2, 3, 4, 4, 5, 6]
    assert tree.prediction_rows.tolist() == [[1, 5, 6], [3, 8, 9]]
    assert tree.attention_mask[6].nonzero().ravel().tolist() == [0, 1, 5, 6]
    assert tree.attention_mask[9].nonzero().ravel().tolist() == [0, 1, 2, 3, 8, 9]
    assert not tree.attention_mask[5:, 4].any()
    assert not tree.attention_mask[:5, 5:].any()


def test_single_token_branch_and_duplicate_anchors_are_independent():
    tree = specopd.proposal_tree(1, torch.tensor([0, 0]), 1)
    assert tree.prediction_rows.tolist() == [[0], [0]]
    assert tree.attention_mask.tolist() == [[True, False, False], [True, True, False], [True, False, True]]
    hidden = torch.arange(6., dtype=torch.float64).reshape(3, 2)
    head = torch.tensor([[1., 2.], [-1., .5]], dtype=torch.float64)
    logits = specopd.prediction_logits(hidden, head, tree)
    assert torch.equal(logits[0], logits[1])
    assert torch.equal(logits[0, 0], hidden[0] @ head.T)


@pytest.mark.parametrize("length,anchors,width", [(0, [0], 2), (3, [-1], 2), (3, [3], 2), (3, [], 2), (3, [1], 0)])
def test_invalid_tree_rejected(length, anchors, width):
    with pytest.raises(ValueError):
        specopd.proposal_tree(length, torch.tensor(anchors, dtype=torch.long), width)


def test_tv_prefix_objective_exact_example_and_teacher_gradient():
    # overlap=.8,.5 gives mean prefix overlap (.8+.4)/2=.6.
    q = torch.tensor([[[.5, .5], [.9, .1]]], dtype=torch.float64).log().requires_grad_()
    p = torch.tensor([[[.7, .3], [.4, .6]]], dtype=torch.float64).log().requires_grad_()
    loss = specopd.e2e_tv_loss(q, p)
    assert float(loss.detach()) == pytest.approx(.4)
    loss.backward()
    assert p.grad is None and q.grad is not None and q.grad.isfinite().all()


def test_early_mismatch_costs_more_than_same_late_mismatch():
    q = torch.tensor([[[.5, .5], [.5, .5], [.5, .5]]], dtype=torch.float64).log()
    early = torch.tensor([[[.9, .1], [.5, .5], [.5, .5]]], dtype=torch.float64).log()
    late = early.flip(1)
    assert specopd.e2e_tv_loss(q, early) > specopd.e2e_tv_loss(q, late)
    assert specopd.e2e_tv_loss(q, q) == 0


def test_teacher_mass_outside_support_is_not_renormalized():
    q = torch.tensor([[[0., 0., float("nan")]]], dtype=torch.float64, requires_grad=True)
    p = torch.tensor([[[.4, .4, .2]]], dtype=torch.float64).log()
    support = torch.tensor([[[True, True, False]]])
    loss = specopd.e2e_tv_loss(q, p, support=support)
    assert float(loss.detach()) == pytest.approx(.2)
    loss.backward()
    assert q.grad[0, 0, 2] == 0 and q.grad.isfinite().all()


def test_loss_rejects_invalid_support_shape_and_nonfinite_teacher():
    logits = torch.zeros(1, 2, 3)
    with pytest.raises(ValueError):
        specopd.e2e_tv_loss(logits, logits, support=torch.zeros_like(logits, dtype=torch.bool))
    with pytest.raises(ValueError):
        specopd.e2e_tv_loss(logits, torch.full_like(logits, float("nan")))
    with pytest.raises(ValueError):
        specopd.e2e_tv_loss(logits[0], logits[0])


def test_e2e_tv_autograd_gradcheck():
    torch.manual_seed(41)
    q = torch.randn(2, 3, 4, dtype=torch.float64, requires_grad=True)
    p = torch.randn(2, 3, 4, dtype=torch.float64)
    assert torch.autograd.gradcheck(lambda x: specopd.e2e_tv_loss(x, p), (q,))


def test_half_probability_reductions_promote_to_float32():
    q = torch.zeros(1, 2, 3, dtype=torch.float16, requires_grad=True)
    p = torch.ones_like(q)
    assert specopd.e2e_tv_loss(q, p).dtype == torch.float32
    menu = torch.tensor([[True, True, False]])
    assert rlid.menu_log_probabilities(q[:, 0], menu).dtype == torch.float32


def test_rlid_calibration_padding_and_masked_gradient():
    logits = torch.tensor([[2., 1., float("nan")]], dtype=torch.float64, requires_grad=True)
    calibration = torch.tensor([[1., 0., float("nan")]], dtype=torch.float64, requires_grad=True)
    menu = torch.tensor([[True, True, False]])
    logp = rlid.menu_log_probabilities(logits, menu, calibration=calibration)
    assert torch.allclose(logp.exp(), torch.tensor([[.5, .5, 0.]], dtype=torch.float64))
    (-logp[0, 0]).backward()
    assert logits.grad[0, 2] == 0 and logits.grad.isfinite().all()
    assert calibration.grad is None


def test_decision_ppo_both_advantage_signs_and_clipping():
    # pi(a)=.6; old pi(a)=.3 -> ratio 2. Positive advantage is clipped,
    # negative advantage keeps the adverse ratio; neither can share a max.
    logits = torch.tensor([[.6, .4], [.6, .4]], dtype=torch.float64).log().requires_grad_()
    menu = torch.ones_like(logits, dtype=torch.bool)
    old = torch.full((2,), math.log(.3), dtype=torch.float64, requires_grad=True)
    advantages = torch.tensor([1., -1.], dtype=torch.float64, requires_grad=True)
    loss = rlid.decision_ppo_loss(logits, menu, torch.tensor([0, 0]), old, advantages)
    assert float(loss.detach()) == pytest.approx(.4)  # (-1.2 + 2)/2
    loss.backward()
    assert torch.equal(logits.grad[0], torch.zeros(2, dtype=torch.float64))
    assert logits.grad[1].norm() > 0
    assert old.grad is None and advantages.grad is None


def test_episode_weighting_is_mean_of_weighted_decisions():
    logits = torch.zeros(3, 2, dtype=torch.float64)
    mask = torch.ones_like(logits, dtype=torch.bool)
    advantages = torch.tensor([1., 1., -1.], dtype=torch.float64)
    weights = torch.tensor([.75, .75, 1.5], dtype=torch.float64)
    # Two-step episode has total 1.5, one-step episode also 1.5.
    loss = rlid.decision_ppo_loss(logits, mask, torch.zeros(3, dtype=torch.long), torch.full((3,), -math.log(2), dtype=torch.float64), advantages, weights=weights)
    assert float(loss) == pytest.approx(0)


def test_marginal_penalty_is_not_mean_per_decision_entropy():
    mask = torch.ones(2, 2, dtype=torch.bool)
    logits = torch.tensor([[8., -8.], [-8., 8.]], dtype=torch.float64)
    assert float(rlid.marginal_label_penalty(logits, mask)) == pytest.approx(0, abs=1e-12)
    biased = torch.tensor([[1000., -1000.], [1000., -1000.]], dtype=torch.float64)
    assert torch.isfinite(rlid.marginal_label_penalty(biased, mask))
    assert rlid.marginal_label_penalty(biased, mask) > 100


def test_same_policy_credit_identity_and_zero_realization_case():
    mapping = torch.tensor([0, 0, 1, 1])
    audit = rlid.credit_variance_audit(torch.tensor([.2, -.4, .6, .1]), mapping, torch.tensor([1., -1.]))
    assert float(audit["mean_update_max_error"]) < 1e-12
    assert float(audit["variance_identity_error"]) < 1e-12
    assert audit["text_variance_trace"] > audit["decision_variance_trace"]
    no_realization = rlid.credit_variance_audit(torch.tensor([.2, -.4]), torch.tensor([0, 1]), torch.tensor([1., -1.]))
    assert no_realization["realization_second_moment"] == 0


@pytest.mark.parametrize("invalid", ["empty_menu", "inadmissible_action", "positive_old", "ratio_overflow"])
def test_rlid_invalid_inputs_are_rejected(invalid):
    logits = torch.zeros(1, 2)
    menu = torch.tensor([[True, invalid != "inadmissible_action"]])
    actions = torch.tensor([1])
    old = torch.tensor([-1.])
    if invalid == "empty_menu":
        menu[:] = False
    if invalid == "positive_old":
        old[:] = 1
    if invalid == "ratio_overflow":
        old[:] = -1e5
    with pytest.raises(ValueError):
        rlid.decision_ppo_loss(logits, menu, actions, old, torch.tensor([1.]))


@pytest.mark.parametrize("module", [specopd, rlid])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostics_report_only_finite_mechanism_metrics(module, seed):
    result = module.diagnostic(seed, device="cpu")
    assert result["diagnostic_only"] and result["evaluation_tier"] == "l1_mechanism"
    assert result["metrics"]["model_calls"] == 0
    assert all(type(value) is bool and value for value in result["checks"].values()), result
    assert all(math.isfinite(value) for value in result["metrics"].values())


@pytest.mark.parametrize("key,paper_id,published_at", [
    ("specopd", "2611.02846", "2026-11-02T09:47:06Z"),
    ("rlid", "2611.02455", "2026-11-02T03:17:51Z"),
])
def test_documentation_cost_provenance_and_learning_contract(key, paper_id, published_at):
    root = Path(__file__).resolve().parents[2]
    catalog = json.loads((root / f"src/auto_research/paper_specs/catalog/post-training/{key}.json").read_text())
    assert catalog["published_at"] == published_at and catalog["announced_on"] == "2026-11-03"
    assert catalog["code"] is None and catalog["upstream_revision"] is None
    assert catalog["first_author"] and catalog["first_author_affiliation"]
    assert catalog["implementation_status"] == "component_only" and catalog["adapter"] is None
    assert catalog["diagnostic_only"] and not catalog["promotion_eligible"] and not catalog["evolve_integrated"]
    assert catalog["requires_gpu_validation"]
    assert catalog["full_experiment_status"] == "not_reproduced_high_cost"
    assert catalog["full_experiment_review_done"] and catalog["review_done"]
    assert not catalog["automatic_retry"] and not catalog["automatic_implementation_queue"]
    folder = root / f"docs/post-training/{paper_id}-{key}"
    source = (folder / "README.md").read_bytes()
    english = (folder / "README-en.md").read_text()
    for field in ("## 论文信息", "公司 / 作者机构", "原始发布日期", "原作者代码", "本地 Adapter / key", "本地代码", "成本过高，不复现（审查 DONE）", "未报告"):
        assert field in source.decode()
    assert f"<!-- source-sha256: {hashlib.sha256(source).hexdigest()} -->" in english
    assert "[简体中文](README.md)" in english
    provenance = json.loads((folder / "assets/provenance.json").read_text())
    image = folder / "assets" / provenance["local_path"]
    assert hashlib.sha256(image.read_bytes()).hexdigest() == provenance["sha256"]
    assert provenance["paper_id"] == paper_id + "v1" and provenance["license"] == "CC BY 4.0"
    assert provenance["transformation"] == "none" and provenance["visual_review"]
    qa = json.loads((root / "docs/learning/questions/nov04-post.json").read_text())
    questions = qa["papers"][f"post-training:{key}"]["questions"]
    assert {q["level"] for q in questions} == {"basics", "mechanism", "comparison", "implementation"}
    assert all(q["added"] == "2026-11-04" and q["example"] and q["source_sections"] for q in questions)
