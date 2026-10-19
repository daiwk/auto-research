import importlib.util
from pathlib import Path

import pytest
import torch

from auto_research.reproductions.unirec.v3_objectives import (
    agrr_loss, confidence_pairs, cppa_loss, evidence_rewards, preference_evidence, quantile_groups,
)


def test_full_diagnostic_and_negative_controls():
    path = Path(__file__).resolve().parents[2] / "scripts/run_oct19_evening_unirec_components.py"
    spec = importlib.util.spec_from_file_location("unirec_v3_runner", path)
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    for seed in (42, 43, 44):
        assert runner.diagnostic(seed, "cpu")["ranking_target_gradient_blocked"]


def test_contradictory_evidence_not_majority_and_ties():
    predictions = torch.tensor([[1., 0., 1.], [0., 1., 1.]])
    positive, negative = preference_evidence(predictions, torch.ones(3))
    assert positive[0, 1] == negative[0, 1] == 1
    assert cppa_loss(torch.tensor([0., 0.]), positive, negative) > 0
    assert not confidence_pairs(positive, negative, 1).diagonal().any()
    assert confidence_pairs(positive, negative, 0).sum() == 0


def test_quantile_ties_and_skip_small_groups():
    attributes = torch.tensor([0., 1., 1., 1., 2., 3.])
    groups = quantile_groups(attributes, 3)
    assert len(set(groups[attributes == 1].tolist())) == 1
    scores = torch.tensor([1., 2.], requires_grad=True)
    loss = agrr_loss(scores, torch.zeros(2), torch.arange(2))
    loss.backward()
    assert loss == 0 and scores.grad.count_nonzero() == 0


def test_agrr_is_nonnegative_kl_and_equal_target_stops_gradient():
    rewards = torch.tensor([-1., .3, .7], dtype=torch.float64, requires_grad=True)
    advantage = (rewards.detach() - rewards.detach().mean()) / rewards.detach().std(unbiased=False)
    scores = advantage.clone().requires_grad_()
    loss = agrr_loss(scores, rewards, torch.zeros(3, dtype=torch.long))
    loss.backward()
    assert abs(float(loss.detach())) < 1e-12 and scores.grad.abs().max() < 1e-12 and rewards.grad is None


def test_input_fail_closed():
    p = torch.zeros(2, 2)
    with pytest.raises(ValueError):
        confidence_pairs(p, p, 2)
    with pytest.raises(ValueError):
        evidence_rewards(p, p, epsilon=0)
    with pytest.raises(ValueError):
        preference_evidence(torch.ones(2, 2), torch.tensor([1., -1.]))
    with pytest.raises(ValueError):
        cppa_loss(torch.ones(2), p, p, pair_mask=p)
