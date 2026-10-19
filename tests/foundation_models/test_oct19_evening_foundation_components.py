"""Independent formula, isolation, gradient and negative-control contracts."""
from __future__ import annotations

import copy
import importlib.util
import math
from pathlib import Path

import pytest
import torch

from auto_research.foundation_models.bmuon import BudgetMuon, allocate_budget, polar, weighted_oracle
from auto_research.foundation_models.ego_p2c import (
    RoleDecoder, SegmentScores, role_context, sample_segment, score_segment, segment_mopd_loss,
)
from auto_research.foundation_models.sink_sparse import SinkMask, calibrate_sink_mask, hybrid_attention

torch.set_num_threads(1)


def test_bmuon_polar_rectangular_zero_and_spectral_bound():
    torch.manual_seed(4)
    for shape in ((6, 3), (3, 6)):
        matrix = torch.randn(*shape, dtype=torch.float64)
        factor = polar(matrix)
        assert torch.linalg.matrix_norm(factor, 2) <= 1 + 1e-12
        assert torch.allclose((factor * matrix).sum(), torch.linalg.svdvals(matrix).sum(), atol=1e-12)
    assert torch.equal(polar(torch.zeros(4, 2)), torch.zeros(4, 2))


def test_bmuon_mm_scalar_kkt_budget_and_zero_ties():
    scores = torch.tensor([.1, .5, 2., .3], dtype=torch.float64)
    result = allocate_budget(scores, 1.6, floor=.01)
    # alpha=.5: interior mu is proportional to a**2, with clipping.
    lo, hi = 0., 1000.
    for _ in range(100):
        scale = (lo + hi) / 2
        values = [min(1., max(.01, scale * a * a)) for a in scores.tolist()]
        if sum(values) > 1.6:
            hi = scale
        else:
            lo = scale
    assert torch.allclose(result, torch.tensor(values, dtype=torch.float64), atol=1e-12)
    assert abs(float(result.sum()) - 1.6) < 1e-12
    assert torch.allclose(allocate_budget(torch.zeros(4), 2.), torch.full((4,), .5))
    assert torch.allclose(allocate_budget(torch.tensor([1., 0., 0.]), 2.), torch.tensor([1., .5, .5]))


def test_bmuon_two_sided_oracle_not_ordinary_muon():
    torch.manual_seed(1)
    left, right = torch.randn(4, 3, dtype=torch.float64), torch.randn(2, 4, dtype=torch.float64)
    mu = torch.tensor([.1, .3, .7, .9], dtype=torch.float64)
    d = torch.diag(mu.sqrt())
    actual1, actual2 = weighted_oracle(left, right, mu)
    # Independent eigendecomposition gives polar(A)=A(A^T A)^(-1/2).
    def reference(matrix):
        vals, vecs = torch.linalg.eigh(matrix.T @ matrix)
        inv = torch.where(vals > 1e-12, vals.clamp_min(1e-12).rsqrt(), 0.)
        return matrix @ ((vecs * inv) @ vecs.T)
    assert torch.allclose(actual1, d @ reference(d @ left), atol=1e-11)
    assert torch.allclose(actual2, reference(right @ d) @ d, atol=1e-11)
    assert (actual1 - polar(left)).abs().max() > .05
    assert (actual2 - polar(right)).abs().max() > .05


def test_bmuon_subnormal_fp32_scores_do_not_underflow_log_lambda():
    scores = torch.tensor([1e-45, 2e-45, .2, .7], dtype=torch.float32)
    allocation = allocate_budget(scores, 1.2, alpha=.5, floor=1e-6)
    assert torch.isfinite(allocation).all()
    assert bool((allocation >= 1e-6).all()) and bool((allocation <= 1).all())
    assert abs(float(allocation.sum()) - 1.2) < 2e-6


def test_bmuon_optimizer_global_budget_actual_update_and_period():
    torch.manual_seed(3)
    blocks = [(torch.nn.Parameter(torch.randn(4, 3, dtype=torch.float64)),
               torch.nn.Parameter(torch.randn(2, 4, dtype=torch.float64))),
              (torch.nn.Parameter(torch.randn(3, 2, dtype=torch.float64)),
               torch.nn.Parameter(torch.randn(1, 3, dtype=torch.float64)))]
    optimizer = BudgetMuon(blocks, budget=2.3, allocation_period=2, lr=.01)
    before = [p.detach().clone() for pair in blocks for p in pair]
    for pair in blocks:
        for p in pair:
            p.square().sum().backward()
    optimizer.step()
    assert abs(float(torch.cat(optimizer.allocations).sum()) - 2.3) < 1e-12
    assert all(float((p.detach() - old).norm()) > 0 for p, old in zip([p for pair in blocks for p in pair], before, strict=True))
    allocation = torch.cat(optimizer.allocations).clone()
    optimizer.step()
    assert torch.equal(torch.cat(optimizer.allocations), allocation)


@pytest.mark.parametrize("scores,budget,kwargs", [([1., -1.], 1., {}), ([1., 2.], 3., {}),
                                                   ([1., 2.], 1., {"alpha": 1.}),
                                                   ([1., 2.], 1., {"floor": .5})])
def test_bmuon_invalid_budget(scores, budget, kwargs):
    with pytest.raises(ValueError):
        allocate_budget(torch.tensor(scores), budget, **kwargs)


def test_bmuon_missing_gradient_and_half_precision_rejected():
    left, right = torch.nn.Parameter(torch.ones(2, 3)), torch.nn.Parameter(torch.ones(3, 2))
    optimizer = BudgetMuon([(left, right)], budget=1.)
    left.grad = torch.ones_like(left)
    with pytest.raises(ValueError, match="every paired"):
        optimizer.step()
    with pytest.raises(ValueError, match="FP32"):
        BudgetMuon([(left.half(), right.half())], budget=1.)


def test_bmuon_state_dict_preserves_allocation_update_clock():
    left, right = torch.nn.Parameter(torch.ones(2, 3)), torch.nn.Parameter(torch.ones(3, 2))
    first = BudgetMuon([(left, right)], budget=1., allocation_period=3)
    left.grad, right.grad = torch.ones_like(left), torch.ones_like(right)
    first.step()
    restored = BudgetMuon([(left, right)], budget=1., allocation_period=3)
    restored.load_state_dict(copy.deepcopy(first.state_dict()))
    assert restored.steps == 1
    assert torch.equal(restored.allocations[0], first.allocations[0])
    restored.step()
    assert restored.steps == 2
    assert torch.equal(restored.allocations[0], first.allocations[0])


def test_sink_exact_block_mass_and_shortest_prefix():
    torch.manual_seed(9)
    q, k = torch.randn(3, 2, 8, 4, dtype=torch.float64), torch.randn(3, 2, 8, 4, dtype=torch.float64)
    mask = calibrate_sink_mask(q, k, block_size=2, coverage=.72)
    reference = torch.zeros(2, 4, 4, dtype=torch.float64)
    for obs in range(3):
        for h in range(2):
            for r in range(4):
                for i in range(r * 2, (r + 1) * 2):
                    row = [float(q[obs, h, i] @ k[obs, h, j]) / 2 for j in range(8)]
                    denominator = sum(math.exp(x) for x in row)
                    for c in range(4):
                        reference[h, r, c] += sum(math.exp(row[j]) / denominator for j in range(c * 2, (c + 1) * 2)) / 6
    assert torch.allclose(mask.mean_block_mass, reference, atol=1e-14)
    assert not mask.mean_block_mass.requires_grad
    for h in range(2):
        for r in range(4):
            kept = reference[h, r][mask.blocks[h, r]]
            assert float(kept.sum()) >= .72 - 1e-12
            assert float(kept.sum() - kept.min()) < .72 + 1e-12


def test_sink_independent_concatenated_partition_oracle_and_gradients():
    torch.manual_seed(8)
    q, k, v = [torch.randn(1, 1, 8, 3, dtype=torch.float64, requires_grad=True) for _ in range(3)]
    blocks = torch.tensor([[[True, False, True, False]] * 4])
    mask = SinkMask(blocks, torch.zeros(1, 4, 4), 2)
    actual, audit = hybrid_attention(q, k, v, mask, pool_gap=2)
    # Independent reference joins the exact sink logits with all pooled logits
    # plus log(gap), then normalizes ONCE across this virtual union.
    outputs = []
    for i in range(8):
        selected = [0, 1, 4, 5]
        scores = [q[0, 0, i] @ k[0, 0, j] / math.sqrt(3) for j in selected]
        values = [v[0, 0, j] for j in selected]
        for j in range(0, 8, 2):
            scores.append(q[0, 0, i] @ k[0, 0, j:j + 2].mean(0) / math.sqrt(3) + math.log(2))
            values.append(v[0, 0, j:j + 2].mean(0))
        outputs.append((torch.stack(scores).softmax(0)[:, None] * torch.stack(values)).sum(0))
    reference = torch.stack(outputs)[None, None]
    assert torch.allclose(actual, reference, atol=1e-12)
    gradients = torch.autograd.grad(actual.square().sum(), (q, k, v), retain_graph=True)
    oracle_gradients = torch.autograd.grad(reference.square().sum(), (q, k, v))
    assert all(torch.allclose(a, b, atol=1e-11) for a, b in zip(gradients, oracle_gradients, strict=True))
    assert all(float(g.norm()) > 0 for g in gradients)
    naive = .5 * (audit["sink"] + audit["compensation"])
    assert (naive - actual).abs().max() > .01
    wrong_alpha = torch.sigmoid(audit["sink_lse"] - audit["compensation_lse"])
    wrong = wrong_alpha[..., None] * audit["sink"] + (1 - wrong_alpha[..., None]) * audit["compensation"]
    assert (wrong - actual).abs().max() > .01


def test_sink_full_mask_gap_one_is_dense_and_calibration_is_static():
    torch.manual_seed(7)
    q, k, v = [torch.randn(2, 2, 6, 4, dtype=torch.float64) for _ in range(3)]
    mask = calibrate_sink_mask(q, k, block_size=2, coverage=1.)
    saved = mask.blocks.clone()
    q2 = q * 1.7
    result, _ = hybrid_attention(q2, k, v, mask, pool_gap=1)
    reference = (q2 @ k.transpose(-1, -2) / 2).softmax(-1) @ v
    assert torch.allclose(result, reference, atol=1e-12)
    assert torch.equal(mask.blocks, saved)


@pytest.mark.parametrize("block,coverage", [(0, .8), (3, .8), (2, 0.), (2, 1.1)])
def test_sink_invalid_calibration(block, coverage):
    q = torch.ones(1, 1, 8, 3)
    with pytest.raises(ValueError):
        calibrate_sink_mask(q, q, block_size=block, coverage=coverage)


def test_sink_empty_support_and_invalid_pool_rejected():
    q = torch.ones(1, 1, 8, 3)
    empty = SinkMask(torch.zeros(1, 4, 4, dtype=torch.bool), torch.zeros(1, 4, 4), 2)
    with pytest.raises(ValueError, match="at least one"):
        hybrid_attention(q, q, q, empty)
    valid = calibrate_sink_mask(q, q, block_size=2)
    with pytest.raises(ValueError, match="pooling"):
        hybrid_attention(q, q, q, valid, pool_gap=3)


def test_ego_allowlisted_contexts_and_no_private_direct_history():
    assert role_context("V", video=[4, 5], subquestion=[7]).visible_fields == ("video", "subquestion")
    with pytest.raises(ValueError, match="Perception"):
        role_context("V", video=[4], subquestion=[7], options=[9])
    with pytest.raises(ValueError, match="Perception"):
        role_context("V", video=[4], subquestion=[7], history=[9])
    with pytest.raises(ValueError, match="private history"):
        role_context("G", video=[4], question=[7], history=[9])


def test_ego_initial_identity_prefix_freezing_and_role_expert_isolation():
    torch.manual_seed(4)
    model = RoleDecoder().double()
    common = dict(video=[3, 4], question=[7, 8])
    pc, general = role_context("PC", **common), role_context("G", **common)
    before = model(pc).detach()
    assert torch.equal(before, model(general))
    model(pc)[-1].square().sum().backward()
    assert any(p.grad is not None and float(p.grad.norm()) > 0 for p in model.experts["PC"].parameters())
    assert all(p.grad is None for p in model.experts["V"].parameters())
    assert all(p.grad is None for p in model.experts["G"].parameters())
    assert all(p.grad is None for p in model.embedding.parameters())
    with torch.no_grad():
        model.q.b["PC"].add_(.1)
        model.experts["PC"][0].weight.add_(.2)
    changed = model(pc).detach()
    assert torch.equal(changed[:2], before[:2])
    assert not torch.equal(changed[2:], before[2:])
    assert torch.equal(model(general), before)


def test_ego_live_sampling_teacher_scoring_and_gradient_update():
    torch.manual_seed(2)
    student = RoleDecoder().double()
    teacher = copy.deepcopy(student).requires_grad_(False)
    with torch.no_grad():
        teacher.head.weight.add_(torch.randn_like(teacher.head.weight) * .2)
    context = role_context("PC", video=[3, 4], question=[7, 8])
    segment = sample_segment(student, context, steps=4, generator=torch.Generator().manual_seed(2))
    logits = score_segment(student, segment)
    selected = torch.tensor(segment.tokens)
    old = segment.rollout_log_probs.clone().requires_grad_()
    teacher_scores = score_segment(teacher, segment).log_softmax(-1).gather(-1, selected[:, None]).squeeze(-1).detach().requires_grad_()
    logp = logits.log_softmax(-1).gather(-1, selected[:, None]).squeeze(-1)
    assert torch.allclose(logp, old, atol=1e-12)
    logits.retain_grad()
    loss = segment_mopd_loss([SegmentScores("PC", logp, teacher_scores, old)])
    loss.backward()
    advantage = (teacher_scores - old).detach().clamp(-5, 5)
    expected = -(advantage / 4)[:, None] * (torch.nn.functional.one_hot(selected, 32) - logits.softmax(-1)).detach()
    assert torch.allclose(logits.grad, expected, atol=1e-12)
    assert teacher_scores.grad is None and old.grad is None
    assert all(p.grad is None for p in teacher.parameters())
    before = student.experts["PC"][0].weight.detach().clone()
    torch.optim.SGD([p for p in student.parameters() if p.requires_grad], lr=.01).step()
    assert float((student.experts["PC"][0].weight.detach() - before).norm()) > 0


def test_ego_role_total_normalization_and_clipping():
    lp = torch.tensor([-.2, -.4, -.8], dtype=torch.float64, requires_grad=True)
    old, teacher = lp.detach().clone().requires_grad_(), torch.tensor([4., -9., 3.], dtype=torch.float64, requires_grad=True)
    together = segment_mopd_loss([SegmentScores("V", lp, teacher, old)], clip=1.)
    split = segment_mopd_loss([SegmentScores("V", lp[:1], teacher[:1], old[:1]), SegmentScores("V", lp[1:], teacher[1:], old[1:])], clip=1.)
    assert torch.allclose(together, split, atol=1e-15, rtol=0)
    assert torch.allclose(torch.autograd.grad(together, lp)[0], torch.tensor([-1., 1., -1.], dtype=torch.float64) / 3)


def test_ego_general_residual_only_enabled_at_mopd():
    model = RoleDecoder()
    assert not model.q.b["G"].requires_grad
    model.enable_general_residual()
    assert model.q.b["G"].requires_grad
    assert not any(p.requires_grad for p in model.experts["G"].parameters())


def test_runner_synthetic_three_methods(tmp_path):
    root = Path(__file__).resolve().parents[2]
    spec = importlib.util.spec_from_file_location("oct19_evening_foundation_runner", root / "scripts/run_oct19_evening_foundation_components.py")
    if not spec or not spec.loader:
        raise AssertionError("runner loader missing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for function in (module.ego_diagnostic, module.bmuon_diagnostic, module.sink_diagnostic):
        result = function(42, "cpu")
        assert result["metrics"] and all(math.isfinite(v) for v in result["metrics"].values())
        assert result["audit"]
