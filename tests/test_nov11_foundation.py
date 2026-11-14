import numpy as np
import pytest
import torch

from auto_research.foundation_models import adindex, b3
from auto_research.multimodal import steprefine


def test_adindex_teacher_maxes_normalized_per_query_distributions():
    scores = torch.tensor([[1., 2., 3.], [30., 20., 10.]], requires_grad=True)
    target = adindex.teacher_distribution(scores, 2)
    per_query = ((scores.detach() - scores.detach().mean(-1, keepdim=True))
                 / scores.detach().std(-1, correction=0, keepdim=True) / 3).softmax(-1)
    expected = per_query.amax(0)
    expected[1] = 0
    expected /= expected.sum()
    assert torch.allclose(target, expected) and not target.requires_grad
    assert not torch.allclose(target, scores.softmax(-1).mean(0))


def test_adindex_refinement_adds_new_tokens_but_not_future_or_incomplete_groups():
    scores = torch.arange(12, dtype=torch.float)
    bank = torch.tensor([0, 1])
    assert adindex.refine_indices(scores, bank, anchor=5, query=7, final_k=3, bank_budget=2).tolist() == [7, 6, 1]
    assert adindex.refine_indices(scores, bank, anchor=5, query=7, final_k=3,
                                 bank_budget=2, complete_group=False).tolist() == [7, 6, 5]
    assert adindex.union_capacity([{0, 1}, {1, 2}, {2, 3}, {3, 4}], 2) == 3
    with pytest.raises(ValueError):
        adindex.refine_indices(scores, torch.tensor([6, 7]), anchor=5, query=7, final_k=3, bank_budget=2)


def test_b3_uses_previous_pass_excluding_frontier_and_active_future():
    gate = b3.SpawnGate()
    gate.observe(np.array([1., 4., 9.]), np.array([True, False, False]), block_start=0)
    assert gate.observe(np.array([.1, .2, .3]), np.array([True, True, False]), block_start=0)
    assert gate.candidates == [1.0]  # not 4, not current-pass .1
    gate.observe(np.zeros(3), np.ones(3, dtype=bool), block_start=0, future_active=True)
    assert gate.candidates == [1.0]
    assert not gate.observe(np.zeros(3), np.ones(3, dtype=bool), block_start=0, predicts_eos=True)
    mask = b3.block_causal_mask(3)
    assert not mask[:3, 3:].any() and mask[3:, :3].all()


def test_steprefine_kl_direction_and_budget_are_not_interchangeable():
    new, old = np.array([[.9, .1], [.5, .5]]), np.array([[.5, .5], [.1, .9]])
    mask = np.array([True, False])
    expected = .9 * np.log(.9 / .5) + .1 * np.log(.1 / .5)
    assert steprefine.refinement_kl(new, old, mask) == pytest.approx(expected)
    assert steprefine.refinement_kl(new, old, mask) != pytest.approx(steprefine.refinement_kl(old, new, mask))
    assert steprefine.next_denoising_index(5, 2) == 2
    with pytest.raises(ValueError):
        steprefine.next_denoising_index(5, 5)


@pytest.mark.parametrize("module", [adindex, b3, steprefine])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_bounded_diagnostics_execute_real_arithmetic(module, seed):
    result = module.diagnostic(seed, device="cpu")
    assert result["diagnostic_only"] and result["checks"] and all(result["checks"].values())
    assert all(np.isfinite(value) for value in result["metrics"].values())
