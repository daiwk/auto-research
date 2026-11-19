"""Literal formulas and non-equivalent negative controls for Nov19 operators."""

import importlib
import hashlib
import json
import math
from pathlib import Path
import statistics

import pytest
import torch

from auto_research.post_training import dcc_aggregation as dcc
from auto_research.post_training import eca_credit as eca
from auto_research.post_training import led_edits as led
from auto_research.post_training import mrpd_replay as mrpd


def test_bilingual_paper_metadata_figures_and_twenty_reviewed_questions():
    root = Path(__file__).resolve().parents[2]
    review = json.loads((root / "docs/research-audits/nov19-latest/post-review.json").read_text())
    questions = json.loads((root / "docs/learning/questions/nov19-latest-post.json").read_text())["papers"]
    english = json.loads((root / "docs/en/learning/translations/qa-nov19-latest-post.json").read_text())["units"]
    assert len(review["accepted"]) == 5
    assert len(english) == 20
    for row in review["accepted"]:
        identity = "post-training:"+row["key"]
        spec = json.loads((root / f"src/auto_research/paper_specs/catalog/post-training/{row['key']}.json").read_text())
        path = root / "docs" / spec["detail_path"]
        cn = path.read_bytes()
        en = (path.parent / "README-en.md").read_text()
        assert f"<!-- source-sha256: {hashlib.sha256(cn).hexdigest()} -->" in en
        assert "[简体中文](README.md)" in en
        assert row["published_at"] in cn.decode() and row["published_at"] in en
        assert "成本过高，不复现（审查 DONE）" in cn.decode()
        provenance = json.loads((path.parent / "assets/provenance.json").read_text())["figures"][0]
        assert provenance["image_sha256"] == hashlib.sha256((path.parent / "assets/paper-figure-01.png").read_bytes()).hexdigest()
        assert provenance["visual_review_done"] is True and provenance["caption_included"] is True
        qrows = questions[identity]["questions"]
        assert {q["level"] for q in qrows} == {"basics", "mechanism", "comparison", "implementation"}
        for q in qrows:
            uid = f"qa/{identity}/{q['id']}"
            serialized = json.dumps(q, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            assert english[uid]["reviewed"] is True
            assert english[uid]["source_sha256"] == hashlib.sha256(serialized.encode()).hexdigest()
            assert all(section in cn.decode() for section in q["source_sections"])


def test_high_cost_hint_wam_is_terminal_without_placeholder_or_gpu_queue():
    root = Path(__file__).resolve().parents[2]
    spec = json.loads((root / "src/auto_research/paper_specs/catalog/post-training/hint-wam.json").read_text())
    assert spec["implementation_status"] == "deferred_high_cost"
    assert spec["review_done"] is True and spec["full_experiment_status"] == "not_reproduced_high_cost"
    assert spec["requires_gpu_validation"] is False and spec["automatic_retry"] is False
    assert spec["automatic_implementation_queue"] is False and "local_operator" not in spec
    assert "572" in spec["deferral_reason"] and "71.6" in spec["deferral_reason"]


@pytest.mark.parametrize("module", ["eca_credit", "mrpd_replay", "dcc_aggregation", "led_edits"])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_actual_diagnostics(module, seed):
    row = importlib.import_module("auto_research.post_training."+module).diagnostic(seed)
    assert row["seed"] == seed and row["diagnostic_only"] is True
    assert row["evaluation_tier"] == "l1_mechanism"
    assert row["checks"] and all(type(v) is bool and v for v in row["checks"].values())
    assert all(type(v) in {int, float} and math.isfinite(v) for v in row["metrics"].values())


def test_eca_telescope_not_step_clip_and_fixed_horizon():
    p = torch.tensor([[-8., -4., -7., -7.]]*8, requires_grad=True)
    assert eca.evidence_returns(p)[0].tolist() == pytest.approx([1/6, -0.5, 0])
    assert eca.evidence_returns(p, mode="step")[0].tolist() == pytest.approx([0, -1/3, 0])
    assert not eca.evidence_returns(p).requires_grad
    with pytest.raises(ValueError):
        eca.evidence_returns(torch.ones(8, 3))


def test_eca_cross_fold_excludes_self_and_novelty_retains_negative():
    u = torch.zeros(8, 3, dtype=torch.float64)
    u[0] = torch.tensor([0.25, -0.25, 0.5])
    folds = torch.tensor([0, 0, 0, 0, 1, 1, 1, 1])
    novelty = torch.ones(8, 3, dtype=torch.bool)
    novelty[0] = False
    out = eca.cross_fold_advantages(u, folds, novelty)
    assert out[0].tolist() == [0., -1., 0.]
    # All-group standardization would include this row in its own denominator.
    ungated = eca.cross_fold_advantages(u, folds, torch.ones_like(novelty))
    assert ungated[0].tolist() == [1., -1., 2.]
    changed = u.clone()
    changed[1:4] = 99
    assert torch.equal(eca.cross_fold_advantages(changed, folds, novelty)[0], out[0])
    with pytest.raises(ValueError):
        eca.cross_fold_advantages(u, torch.zeros(8, dtype=torch.long), novelty)


def test_eca_loss_is_unclipped_sequence_sum_not_token_mean():
    lp = torch.full((2, 3), math.log(3), dtype=torch.float64, requires_grad=True)
    old = torch.zeros_like(lp, requires_grad=True)
    a = torch.ones_like(lp, requires_grad=True)
    mask = torch.tensor([[True, False, False], [True, True, False]])
    loss = eca.policy_loss(lp, old, a, mask)
    assert loss.item() == pytest.approx(-4.5)
    loss.backward()
    assert old.grad is None and a.grad is None
    assert lp.grad[~mask].count_nonzero() == 0


def test_eca_masked_extreme_log_ratio_cannot_poison_loss_or_gradient():
    mask = torch.tensor([[True, False]])
    lp = torch.tensor([[-1., 0.]], dtype=torch.float64, requires_grad=True)
    old = torch.tensor([[-1., -1000.]], dtype=torch.float64)
    result = eca.policy_loss(lp, old, torch.ones_like(lp), mask)
    reference = eca.policy_loss(lp[:, :1], old[:, :1], torch.ones_like(lp[:, :1]), mask[:, :1])
    assert result.item() == reference.item() == -1.
    result.backward()
    assert lp.grad.tolist() == [[-1., 0.]]


def test_mrpd_tail_is_not_renormalized_topk_and_direction_is_reverse():
    p = torch.tensor([[[0.6, 0.3, 0.1]]], dtype=torch.float64)
    q = torch.tensor([[[0.2, 0.5, 0.3]]], dtype=torch.float64)
    # Expert top1 is token1; remaining student and teacher mass are .7 and .5.
    out = mrpd.coarsened_reverse_kl(p.log(), q.log(), k=1)
    expected = 0.3*math.log(0.3/0.5)+0.7*math.log(0.7/0.5)
    assert out.item() == pytest.approx(expected)
    assert out.item() > 0  # renormalizing the selected singleton would falsely give zero.
    forward = 0.5*math.log(0.5/0.3)+0.5*math.log(0.5/0.7)
    assert out.item() != pytest.approx(forward)
    full = (p*(p.log()-q.log())).sum()
    assert mrpd.coarsened_reverse_kl(p.log(), q.log(), k=3).item() == pytest.approx(full.item())


def test_mrpd_asymmetric_clip_response_mean_and_independent_dense_kl():
    s = torch.zeros(2, 2, 2, dtype=torch.float64, requires_grad=True)
    t = torch.zeros_like(s, requires_grad=True)
    ids = torch.zeros(2, 2, dtype=torch.long)
    # current selected probability=.5; choose logging probability=.25 -> ratio2.
    old = torch.full((2, 2), math.log(.25), dtype=torch.float64, requires_grad=True)
    m = torch.tensor([[True, False], [True, True]])
    out, pg, kl = mrpd.loss(s, t, ids, old, torch.tensor([1., -1.]), m, k=2)
    assert pg.item() == pytest.approx((-1.28+2)/2)
    assert kl.item() == pytest.approx(0)
    assert out.item() == pytest.approx(pg.item())
    out.backward()
    assert t.grad is None and old.grad is None and s.grad[~m].count_nonzero() == 0


def test_mrpd_rejects_shuffled_steps_instead_of_hiding_them():
    with pytest.raises(ValueError):
        mrpd.chronological_steps({"a": [{"step": 1}, {"step": 0}]})
    with pytest.raises(ValueError):
        mrpd.chronological_steps({"a": [{"step": 0}], "b": []})


def test_mrpd_masked_extreme_log_ratio_cannot_poison_loss_or_gradient():
    s = torch.tensor([[[0., 0.], [999., -999.]]], dtype=torch.float64, requires_grad=True)
    t = torch.tensor([[[1., 1.], [-999., 999.]]], dtype=torch.float64, requires_grad=True)
    ids = torch.zeros(1, 2, dtype=torch.long)
    old = torch.tensor([[-math.log(2), -1000.]], dtype=torch.float64)
    mask = torch.tensor([[True, False]])
    result = mrpd.loss(s, t, ids, old, -torch.ones(1), mask, k=2)[0]
    reference = mrpd.loss(s[:, :1], t[:, :1], ids[:, :1], old[:, :1], -torch.ones(1), mask[:, :1], k=2)[0]
    assert result.item() == reference.item() == 1.
    result.backward()
    assert t.grad is None
    assert bool(torch.isfinite(s.grad).all())
    assert s.grad[0, 1].count_nonzero() == 0


def test_dcc_exact_two_medians_against_independent_brute_force():
    values = [-8., -2., -2., 1., 3., 4., 100.]
    a = sorted(values)
    candidates = []
    for i in range(1, len(a)):
        if a[i] > a[i-1]:
            lo, hi = statistics.median(a[:i]), statistics.median(a[i:])
            cost = sum(abs(x-lo) for x in a[:i])+sum(abs(x-hi) for x in a[i:])
            candidates.append((cost, i, lo, hi))
    _, _, lo, hi = min(candidates)
    assert dcc.centers(values) == (lo, hi)
    assert dcc.centers([0., 1., 2.]) == (0., 1.5)
    assert dcc.centers([2., 2.]) == (2., 2.)


def test_dcc_weights_only_after_common_center_fit():
    rows = [[-3., -2.], [1., 100.], [2., 3.]]
    one, weighted = dcc.aggregate(rows), dcc.aggregate(rows, [1, 100])
    assert one["centers"] == weighted["centers"]
    assert one["clipped_scores"] == weighted["clipped_scores"]
    for bad in ([[True]], [[float("nan")]], [[1], [1, 2]], []):
        with pytest.raises(ValueError):
            dcc.aggregate(bad)
    with pytest.raises(ValueError):
        dcc.aggregate(rows, [0, 0])


def test_led_lcs_gap_rules_insert_once_before_right_anchor():
    labels, anchors = led.edit_targets(["a", "d", "x", "y"], ["a", "b", "c", "d"])
    assert anchors == ((0, 0), (1, 3))
    assert labels == ["a", led.INSERT, led.DELETE, led.DELETE]
    # A gap with two missing targets emits one insertion this round, not two.
    assert labels.count(led.INSERT) == 1
    assert led.apply_edits(["a", "d", "x", "y"], labels, [0, 1, 2, 3]) == ["a", led.MASK, "d", led.MASK]
    assert led.edit_targets(["a", "b"], ["a", "c"])[0] == ["a", "c"]


def test_led_selection_threshold_fallback_and_simultaneous_resize():
    src = [led.MASK, "a", led.MASK]
    pred, confidence = ["b", led.INSERT, "c"], [.1, .8, .2]
    assert led.selected_positions(src, pred, confidence, edit_threshold=.9) == (2,)
    assert led.selected_positions(src, pred, confidence, edit_threshold=.8) == (1, 2)
    assert led.apply_edits(src, pred, [1, 2]) == [led.MASK, led.MASK, "a"]
    with pytest.raises(ValueError):
        led.edit_targets(["a"], [led.MASK])
    with pytest.raises(ValueError):
        led.apply_edits(["a"], [led.DELETE], [0, 0])


@pytest.mark.parametrize("module", [eca, mrpd, dcc, led])
def test_boolean_seed_is_not_a_real_seed(module):
    with pytest.raises(ValueError):
        module.diagnostic(True)
